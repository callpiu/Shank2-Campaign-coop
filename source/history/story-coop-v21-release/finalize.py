"""Record the v0.9 deliverable after independent archive validation."""
import hashlib
import json
from pathlib import Path
import zipfile

from build_release import HERE, OUTPUT, ROOT, sha, save


def main():
    archive = Path(json.loads((HERE / "release.json").read_text())["archive"])
    release = json.loads((HERE / "release.json").read_text())
    equality = json.loads((HERE / "archive-equality.json").read_text())
    audit = json.loads((HERE / "size-audit.json").read_text())
    installer = json.loads((HERE / "validation.json").read_text())
    recovery = json.loads((HERE / "recovery-validation.json").read_text())
    manager = json.loads((HERE / "manager-validation.json").read_text(encoding="utf-8-sig"))

    assert sha(archive) == release["sha256"]
    assert equality["archive_matches_directory"]
    assert audit["audit_ok"]
    assert installer["four_variants_exact"]
    assert installer["no_godmode_or_probe"]
    assert installer["restores_all_96_originals"]
    assert installer["launcher_smoke"]
    assert installer["new_ui_exact"]
    assert installer["ui_removal"]
    assert installer["custom_ui_rejected"]
    assert recovery["passed"] and recovery["originals_restored"]
    assert manager["localized_labels_fit"]

    forbidden_names = {"loadouts.json", "launcher-settings.json", "features.json"}
    with zipfile.ZipFile(archive) as bundle:
        names = bundle.namelist()
        assert bundle.testzip() is None
        assert len(names) == release["files"] == 142
        assert not any(Path(name).is_absolute() or ".." in Path(name).parts for name in names)
        assert not any(
            name.lower().endswith((".exe", ".dll"))
            or Path(name).name in forbidden_names
            for name in names
        )
        assert sum(name.lower().endswith(".bik") for name in names) == 27
        checksum_rows = bundle.read("SHA256SUMS.txt").decode("utf-8").splitlines()
        assert len(checksum_rows) == 141
        for row in checksum_rows:
            expected, name = row.split("  ", 1)
            assert hashlib.sha256(bundle.read(name)).hexdigest() == expected
        top = sorted({name.split("/", 1)[0] for name in names})
        assert top == sorted(
            [
                "FONT-LICENSE.txt",
                "Install-CHS.cmd",
                "Launch-Coop.cmd",
                "patch",
                "README.md",
                "Remove-CHS.cmd",
                "Remove-v08.cmd",
                "SHA256SUMS.txt",
                "一键安装汉化.cmd",
                "一键卸载汉化.cmd",
                "启动中文补丁管理器.cmd",
                "检查汉化安装.cmd",
            ]
        )

    evidence = dict(
        version="0.9-CHS",
        archive=str(archive),
        archive_bytes=release["bytes"],
        archive_sha256=release["sha256"],
        files=release["files"],
        archive_matches_directory=True,
        archive_size_audit_ok=True,
        four_exact_builds=True,
        installer_operations=installer["operations"],
        recovery_cases=len(recovery["cases"]),
        gui_operations=installer["gui_operations"],
        command_checks=len(installer["command_checks"]),
        restored_localization_assets=96,
        enhanced_movies=27,
        test_assists_included=False,
        personal_configuration_included=False,
        game_executables_or_dlls_included=False,
        live_game_started_for_packaging=False,
    )
    save(HERE / "release-final.json", evidence)

    note = (
        "2026-11-06 v0.9完整汉化整合包已打包："
        f"{release['bytes']} bytes / {release['files']} files / SHA256 {release['sha256']}。"
        "包含双人关前1P选人配装→2P选人配装、跨Shank/Corina换人、邪恶角色介绍/图标/头像、"
        "第一关女性角色Boss抓取修复及第二关Slums过场双人传送修复。"
        "四种构建精确重建、43次安装操作、6项异常/共存恢复、96汉化原件还原、"
        "GUI与4个CMD入口、目录ZIP逐字节一致、体积审计均通过；"
        "正式包不含EXE/DLL、个人配置、无敌或普通敌人一击必杀。"
    )
    for name in ("progress.md", "findings.md"):
        with (ROOT / name).open("a", encoding="utf-8") as stream:
            stream.write("\n" + note + "\n")
    plan = ROOT / "task_plan.md"
    text = plan.read_text(encoding="utf-8")
    text = text.replace("40. [in_progress]", "40. [complete/2026-11-06]")
    plan.write_text(text + "\n40完成证据：" + note + "\n", encoding="utf-8")
    (HERE / "RESUME.md").write_text(
        "# v0.9 完整汉化整合包\n\n"
        f"交付：`{archive.as_posix()}`，{release['bytes']} 字节，{release['files']} 个文件。\n\n"
        f"SHA-256：`{release['sha256']}`\n\n"
        "基于冻结 v0.8.3 完整汉化包重建，继承 96 个汉化／增强视频资源；"
        "MOD 部分来自已获用户实测确认的 v17 Boss 修复和 v20 双人关前选人／配装版。"
        "正式包不包含开发 EXE、DLL、测试辅助、个人设置或存档。\n\n"
        "验证证据：`validation.json`、`recovery-validation.json`、"
        "`manager-validation.json`、`installed-manifest.json`、"
        "`archive-equality.json`、`size-audit.json`、`release-final.json`。"
        "运行时完整战役和所有角色组合仍未穷尽验证。\n",
        encoding="utf-8",
    )
    print(json.dumps(evidence, ensure_ascii=False))


if __name__ == "__main__":
    main()
