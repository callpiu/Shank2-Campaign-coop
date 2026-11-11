"""Build the audio-only v0.9.1 update from the sealed v0.9 full release."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import zipfile

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
OLD = ROOT / 'outputs/Shank2-StoryCoop-v0.9-CHS'
DEST = ROOT / 'outputs/Shank2-StoryCoop-v0.9.1-CHS'
OLD_SHA = '227cf6988bb2c47d78219d81f389c3615986fc5996c369af38070ee6e18f3a67'


def sha(path):
    with path.open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def read(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))


def write(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def prepare(stage, reports):
    archive = OLD.parent / (OLD.name + '.zip')
    assert sha(archive) == OLD_SHA
    with zipfile.ZipFile(archive) as bundle:
        for entry in bundle.namelist():
            rel = Path(entry)
            assert not rel.is_absolute() and '..' not in rel.parts
        bundle.extractall(stage)
    patch = stage / 'patch'
    manifest = read(patch / 'manifest.json')
    shutil.copyfile(patch / 'manifest.json', patch / 'previous-manifest.json')
    movies = read(patch / 'movie-assets.json')
    records = {row['file']: row for row in reports['files']}
    assert set(records) == {row['file'] for row in movies} and len(records) == 27
    for item in manifest['files']:
        source = patch / 'payload' / item['path']
        assert sha(source) == item['sha256']
        if item['group'] == 'Movies':
            row = records[source.name]
            assert item['sha256'] == row['input_sha256']
            remixed = HERE / 'remixed' / source.name
            assert sha(remixed) == row['output_sha256']
            shutil.copyfile(remixed, source)
            item['sha256'] = row['output_sha256']
            item['size'] = row['bytes']
    for movie in movies:
        digest = records[movie['file']]['output_sha256']
        movie.update(input_sha256=digest, output_sha256=digest)
    write(patch / 'manifest.json', manifest)
    write(patch / 'movie-assets.json', movies)
    for name in ['Coop-Localization.ps1', 'Manage-Coop.ps1', 'Remove-Coop.ps1', 'Launcher-Strings.ps1', 'Localization-Manager.ps1']:
        script = patch / name
        content = script.read_text(encoding='utf-8-sig').replace('v0.9', 'v0.9.1')
        if name == 'Coop-Localization.ps1':
            old_error = 'Old Chinese movie patch detected. Uninstall localization with your OLD v0.5/v0.4 package first, then install v0.8. Keep the .storycoop-chs backup folder.'
            new_error = '检测到旧版过场资源。请先用旧包的“一键卸载汉化.cmd”卸载，再安装本版。Keep the .storycoop-chs backups; use the previous bundle to remove its localization before installing v0.9.1.'
            assert old_error in content
            content = content.replace(old_error, new_error)
        script.write_text(content, encoding='utf-8-sig')
    readme = stage / 'README.md'
    content = readme.read_text(encoding='utf-8').replace('v0.9 ·', 'v0.9.1 ·', 1)
    lines = content.splitlines()
    for index, line in enumerate(lines):
        if line.startswith('3. 已使用'):
            lines[index] = '3. 已装旧版：关闭游戏，先用旧包的“一键卸载汉化.cmd”，再用新包的“一键安装汉化.cmd”。不必卸载双人 MOD；要保留启动器设置，可复制旧包 patch/loadouts.json、patch/launcher-settings.json 到新包的 patch/。'
        if line.startswith('4. v0.4'):
            lines[index] = '4. 若只想替换过场：用旧包运行 `Remove-CHS.cmd -Group Movies`，再用新包运行 `Install-CHS.cmd -Group Movies`。保留游戏目录的 .storycoop-chs 原件备份。'
        if line == '## 本版新增与修复':
            lines[index] = '## v0.9.1 过场音量\n\n相对 v0.9：从混合音轨估算对白、背景音乐和音效；对白乘 1.8、音乐乘 0.3，音效及剩余成分保留。响峰做限幅以防削波。分轨为估算，实际听感随场景而变。27 段过场的画面帧和中文字幕未重新编码。采用 [TIGER-DnR](https://huggingface.co/audiojs/tiger-dnr) 在本地离线处理，发行包不需要安装模型。\n\n## v0.9 双人功能与修复'
        if line.startswith('English: '):
            lines[index] = line.replace('Existing v0.8+ Chinese/movie assets need no reinstall.', 'Upgrading? Close the game, run Remove-CHS.cmd from the old bundle, then install with this bundle. This version remixes cutscene dialogue at 1.8× and music at 0.3× using estimated stems.')
    readme.write_text('\n'.join(lines) + '\n', encoding='utf-8')
    validation = read(patch / 'VALIDATION.json')
    validation.update(version='0.9.1-CHS', movie_profile=reports['profile']['id'],
                      upgrade='remove old localization with old bundle, then install new; or swap Movies only',
                      user_confirmed_camera_and_first_intro='previous v0.9 mix only',
                      new_mix_in_game_listening_confirmed=False,
                      localization_receipt_unchanged=False)
    return validation


def validate_install(stage, fixture):
    shutil.copytree(HERE.parent / 'story-coop-v09-fixes/upgrade-fixture', fixture)
    powershell = Path(os.environ['WINDIR']) / 'System32/WindowsPowerShell/v1.0/powershell.exe'
    patch = stage / 'patch'
    old = OLD / 'patch'
    manifest = read(patch / 'manifest.json')

    def run(package, script, action, *args, error=None):
        result = subprocess.run([str(powershell), '-NoProfile', '-ExecutionPolicy', 'Bypass', '-File',
                                 str(package / script), '-GamePath', str(fixture), '-Action', action, *args],
                                capture_output=True, timeout=120, text=True, encoding='utf-8', errors='replace')
        if error:
            assert result.returncode and error in result.stderr + result.stdout, result.stderr
        else:
            assert result.returncode == 0, result.stderr

    def localize(package, action, group='All', error=None):
        run(package, 'Coop-Localization.ps1', action, '-Group', group, '-NoUI', error=error)

    def verify_files(key):
        for item in manifest['files']:
            assert sha(fixture / item['path']) == item[key], item['path']
        for path, digest in manifest['guards'].items():
            assert sha(fixture / path) == digest, path

    localize(patch, 'Install')
    localize(patch, 'Verify')
    verify_files('sha256')
    localize(patch, 'Remove')
    verify_files('original_sha256')
    localize(old, 'Install')
    localize(patch, 'Install', error='use the previous bundle')
    localize(old, 'Verify')
    localize(old, 'Remove', 'Movies')
    localize(patch, 'Install', 'Movies')
    localize(patch, 'Verify')
    verify_files('sha256')
    for mode in ['Keyboard', 'Pads']:
        run(patch, 'Manage-Coop.ps1', 'Verify', '-InputMode', mode)
    verifier = Path('G:/DeepSeekData/.codex/skills/localize-game-text/scripts/verify_overlay_manifest.py')
    subprocess.run([sys.executable, str(verifier), '--manifest', str(patch / 'manifest.json'),
                    '--root', str(fixture), '--json', str(HERE / 'installed-manifest.json')],
                   check=True, stdout=subprocess.DEVNULL)
    localize(patch, 'Remove')
    verify_files('original_sha256')
    return {'fresh_install': True, 'old_receipt_rejected_without_writes': True,
            'movies_only_upgrade': True, 'both_launcher_modes_verify': True, 'restored_assets': len(manifest['files'])}


def main():
    archive = DEST.parent / (DEST.name + '.zip')
    assert not DEST.exists() and not archive.exists(), 'Release output already exists.'
    reports = read(HERE / 'remix-validation.json')
    assert sum(row['video_frames_unchanged'] for row in reports['files']) == 18822
    assert all(not row['clipped_samples'] for row in reports['files'])
    codec = read(HERE / 'codec-validation.json')
    assert set(codec['movies']) == {row['file'] for row in reports['files']}
    with tempfile.TemporaryDirectory(prefix='release-', dir=HERE) as temporary:
        temp = Path(temporary).resolve()
        assert temp.parent == HERE
        stage = temp / 'stage'
        validation = prepare(stage, reports)
        validation['v091_audio_update'] = validate_install(stage, temp / '隔离测试')
        validation['v091_native_codec_movie_count'] = len(codec['movies'])
        write(stage / 'patch/VALIDATION.json', validation)
        files = sorted(path for path in stage.rglob('*') if path.is_file() and path.name != 'SHA256SUMS.txt')
        assert not any(path.suffix.lower() in {'.exe', '.dll', '.onnx'} for path in files)
        checksums = ''.join(f'{sha(path)}  {path.relative_to(stage).as_posix()}\n' for path in files)
        (stage / 'SHA256SUMS.txt').write_text(checksums, encoding='utf-8')
        tempzip = temp / archive.name
        with zipfile.ZipFile(tempzip, 'w', zipfile.ZIP_DEFLATED, compresslevel=6) as bundle:
            for path in sorted(stage.rglob('*')):
                if path.is_file():
                    bundle.write(path, path.relative_to(stage).as_posix())
        with zipfile.ZipFile(tempzip) as bundle:
            assert bundle.testzip() is None and len(bundle.namelist()) == len(files) + 1
        shutil.move(stage, DEST)
        shutil.move(tempzip, archive)
    result = {'archive': str(archive), 'bytes': archive.stat().st_size, 'sha256': sha(archive),
              'files': len(files) + 1, 'install_checks': validation['v091_audio_update']}
    write(HERE / 'release.json', result)
    print(json.dumps(result, ensure_ascii=False), flush=True)


if __name__ == '__main__':
    main()
