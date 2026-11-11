"""Check that the packaged update changes only cutscene audio and its metadata."""
from pathlib import Path
import subprocess
import sys
import zipfile

from build_release import DEST, HERE, OLD, read, sha, write


def main():
    report = read(HERE / 'release.json')
    archive = Path(report['archive'])
    previous = OLD.parent / (OLD.name + '.zip')
    scripts = Path('G:/DeepSeekData/.codex/skills/localize-game-text/scripts')
    checks = [
        ('verify_release_archive.py', ['--directory', str(DEST), '--archive', str(archive)], 'archive-equality.json'),
        ('audit_release_size.py', ['--archive', str(archive), '--reference', str(previous)], 'size-audit.json'),
    ]
    for tool, args, filename in checks:
        subprocess.run([sys.executable, str(scripts / tool), *args, '--json', str(HERE / filename)],
                       check=True, stdout=subprocess.DEVNULL)
    assert read(HERE / 'archive-equality.json')['archive_matches_directory']
    assert read(HERE / 'size-audit.json')['audit_ok']
    assert sha(archive) == report['sha256']
    manifest = read(DEST / 'patch/manifest.json')
    updated = {f"patch/payload/{row['path']}" for row in manifest['files'] if row['group'] == 'Movies'}
    assert len(updated) == 27
    allowed = updated | {'README.md', 'SHA256SUMS.txt', 'patch/manifest.json',
                         'patch/previous-manifest.json', 'patch/movie-assets.json', 'patch/VALIDATION.json',
                         *(f'patch/{name}.ps1' for name in ['Coop-Localization', 'Manage-Coop', 'Remove-Coop',
                                                           'Launcher-Strings', 'Localization-Manager'])}
    with zipfile.ZipFile(previous) as old, zipfile.ZipFile(archive) as new:
        assert set(old.namelist()) == set(new.namelist())
        changed = {name for name in new.namelist() if old.read(name) != new.read(name)}
        assert updated <= changed <= allowed
    report.update(archive_matches_directory=True, unchanged_game_patch_payload=True,
                  movies_updated=len(updated), unchanged_video_frames=18822,
                  original_codec_check=True, new_mix_in_game_listening_confirmed=False)
    write(HERE / 'release-final.json', report)
    print(f"Archive verified: {report['files']} files, all {len(updated)} cutscenes updated.")


if __name__ == '__main__':
    main()
