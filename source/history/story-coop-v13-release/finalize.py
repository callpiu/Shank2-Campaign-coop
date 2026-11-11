"""Record the audited deliverable without modifying its frozen contents."""
import hashlib
import json
from pathlib import Path
import zipfile
from build_release import HERE, ROOT, OUTPUT, BASE

release=json.loads((HERE/'release.json').read_text())
archive=Path(release['archive'])
assert hashlib.sha256(archive.read_bytes()).hexdigest()==release['sha256']
assert json.loads((HERE/'archive-equality.json').read_text())['archive_matches_directory']
audit=json.loads((HERE/'size-audit.json').read_text())
assert audit['audit_ok'] and 0<audit['comparison']['archive_bytes_delta']<100000
with zipfile.ZipFile(archive) as z, zipfile.ZipFile(BASE) as base:
    rows=z.read('SHA256SUMS.txt').decode().splitlines()
    assert len(rows)==len(z.namelist())-1==137
    for row in rows:
        expected,name=row.split('  ',1)
        assert hashlib.sha256(z.read(name)).hexdigest()==expected
    assets=[name for name in z.namelist() if name.startswith('patch/payload/')]
    assert len(assets)==96
    assert all(z.read(name)==base.read(name) for name in assets)

resume=f'''# v0.8.3 完整汉化整合发行包

2026-11-06：继续项目后，把已获用户实测确认的分数保留与延后角色切换整合进完整汉化包，不添加新玩法，不改动现有游戏和旧发行 ZIP。

交付：`{archive.as_posix()}`，{release['bytes']} 字节（约 325.4 MiB），138 文件。
SHA-256：`{release['sha256']}`。

来源为冻结 v0.8.1-CHS-Test.zip 与 v0.8.3-Character-Test.zip；四种配方精确重建 v12 开发版。69 汉化资源及 27 份增强中文字幕视频与旧完整包字节一致。未打包 EXE、DLL、存档、个人设置、Boss 探针或测试无敌。原生玩家受伤入口及两个诊断区域的离线检查通过。

验证：39 次实际安装／升级／重复安装／陌生程序拒绝／卸载／回退操作，键盘／手柄×英文／中文四种重建，96 原件还原；图形管理器 5 操作及标签边界；中文 CMD 等 4 入口及失败退出码；全部 17 头像、语言切换／持久化启动器自检。初次头像失败由精简 fixture 缺原生纹理导致，已仅为临时游戏复制纹理，未带入发行包。manifest、137 条 UTF-8 SHA 校验、138 文件目录与 ZIP 等同性、体积审计全通过。新 ZIP 比旧包仅增加 {audit['comparison']['archive_bytes_delta']} 字节。两组字体纹理重复因不同原生字体部署目标保留，本次未改去重映射。

未启动 Steam 或游戏；四种输出与已测开发版相同，不声称精确新包完整运行／全战役回归通过。人物切换实机有效为用户报告，未宣称每个跨关和输入组合都测过。Steam 成就为用户导入通关档后实际解锁，未逐条验证自然触发。独眼巨人处决已证实正常扣 240，本包不修改 Boss 伤害。

安装：首次先 Install-CHS.cmd，再 Launch-Coop.cmd；现有 v0.8+ 汉化资源不需重装，新解压文件夹选择原游戏目录即可，按需复制旧启动器两份配置。v0.4/v0.5 先用旧包卸载。已知启动器覆盖关前选装限制仍明确红字提示。角色下关／重试生效、F7 镜头切换保持。

可复现脚本：build_release.py（prepare 不覆盖现成目录；--archive 在验证报告通过后打包）、validate.py、finalize.py。证据：validation.json、manager-validation.json、installed-manifest.json、archive-equality.json、size-audit.json、release.json。

下一步按用户新反馈推进；若继续稳定性回归，优先自然跨关携带配装／角色、剧情战斗边界。无需重复已经确认的按键、F6、两处虚焦、分数和成就同步。用户允许启动 Steam／游戏，早先登出已由用户确认非本项目；诊断 PID 若仍开着不要擅自重启。保留余额剩 3% 暂停约定。
'''
(HERE/'RESUME.md').write_text(resume,encoding='utf-8')
note=f"2026-11-06 v0.8.3完整汉化整合包已完成：{release['bytes']}bytes/138files/SHA "+release['sha256']+'。从冻结ZIP重建，96资源字节不变，39安装操作、GUI5、CMD4、双语17头像、四种精确构建、137条SHA及目录ZIP一致性通过。无个人配置/存档/EXE/DLL/测试无敌/诊断，旧包与用户游戏未改，未启动Steam或游戏。证据与后续交接work/story-coop-v13-release/RESUME.md。'
for filename in ('progress.md','findings.md'):
    with (ROOT/filename).open('a',encoding='utf-8') as stream:stream.write('\n'+note+'\n')
plan=ROOT/'task_plan.md'
text=plan.read_text(encoding='utf-8')
text=text.replace('33. [in_progress] 整合v0.8.3完整汉化包：','33. [complete/2026-11-06] 整合v0.8.3完整汉化包：')
plan.write_text(text+'\n33完成证据：'+note+'\n',encoding='utf-8')
print('PASS: frozen payload equality, all archive checksums, release record and project handoff.')
