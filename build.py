"""Build the English Campaign Co-op release using only Python's standard library."""
import argparse
import base64
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import shutil
import tempfile
import zipfile
import zlib


ROOT = Path(__file__).resolve().parent
PATCH = ROOT / "source/release-v0.10.3-mod/patch"
WRAPPERS = ROOT / "source/package-inputs/MOD"
META = ("Coop-Key-Settings.ps1", "Game-Paths.ps1", "Install-Patch.ps1",
        "PatchManager.ps1", "exe-recipe.json", "manifest.json", "VALIDATION.json")


def sha(data):
    return hashlib.sha256(data).hexdigest()


def require(condition, message):
    if not condition:
        raise ValueError(message)


def payload_path(name):
    path = PurePosixPath(name)
    require(path.parts and path.parts[0] == "payload" and len(path.parts) > 1
            and all(re.fullmatch(r"[a-zA-Z0-9_.-]+", part) and part not in (".", "..")
                    for part in path.parts) and path.as_posix() == name,
            f"Invalid payload path: {name}")
    return name


def verify_game(game, manifest, recipe):
    for name, expected in manifest["guards"].items():
        require(sha((game / name).read_bytes()) == expected, f"Unsupported Steam file: {name}")
    stock = (game / "bin/shank2.exe").read_bytes()
    require(len(stock) == recipe["source_size"] and sha(stock) == recipe["input_sha256"],
            "Unsupported bin/shank2.exe; provide an unmodified supported Steam copy.")
    rebuilt = bytearray(stock)
    end = 0
    for edit in sorted(recipe["patches"], key=lambda item: item["offset"]):
        offset = edit["offset"]
        before, after = bytes.fromhex(edit["before"]), bytes.fromhex(edit["after"])
        require(end <= offset and offset + len(before) <= len(stock) and
                len(before) == len(after) and stock[offset:offset + len(before)] == before,
                f"Executable patch precondition failed at {offset:#x}")
        end = offset + len(before)
        rebuilt[offset:end] = after
    rebuilt.extend(base64.b64decode(recipe["append"], validate=True))
    require(len(rebuilt) == recipe["target_size"] and sha(rebuilt) == recipe["output_sha256"],
            "Reconstructed executable does not match the release manifest.")
    print(f"Verified reconstructed EXE: {recipe['output_sha256']}")


def collect(game):
    files = {name: (WRAPPERS / name).read_bytes()
             for name in ("Install.cmd", "Uninstall.cmd", "README.md")}
    files.update({f"patch/{name}": (PATCH / name).read_bytes() for name in META})
    manifest = json.loads(files["patch/manifest.json"])
    recipe = json.loads(files["patch/exe-recipe.json"])
    require(manifest["format"] == 1 and recipe["format"] == 1 and
            manifest["includes_mod"] and not manifest["includes_localization"],
            "Expected the English MOD and a format-1 recipe.")
    require(manifest["original_exe_sha256"] == recipe["input_sha256"],
            "Original executable hash disagrees with recipe.")
    targets = set()
    for row in manifest["files"]:
        target = row["path"]
        require(target.casefold() not in targets and target == row["targetRelative"],
                f"Invalid or duplicate install target: {target}")
        targets.add(target.casefold())
        if "recipe" in row:
            require(target in ("bin/shank2.exe", "bin/shank2-story-coop.exe")
                    and row["recipe"] == "exe-recipe.json"
                    and row["sha256"] == recipe["output_sha256"]
                    and row["size"] == recipe["target_size"],
                    f"Executable recipe does not match manifest: {target}")
        else:
            name = payload_path(row["relative"])
            data = (PATCH / name).read_bytes()
            require(len(data) == row["size"] and sha(data) == row["sha256"],
                    f"Payload does not match manifest: {name}")
            files[f"patch/{name}"] = data
    require({"bin/shank2.exe", "bin/shank2-story-coop.exe"} <= targets,
            "Missing executable entries.")
    if game:
        verify_game(game, manifest, recipe)
    for name, data in files.items():
        suffix = PurePosixPath(name).suffix.lower()
        require(name.isascii() and suffix in {".cmd", ".ps1", ".md", ".json", ".chui"},
                f"Unexpected English release member: {name}")
        if suffix != ".chui":
            require(not re.search(r"[\u3400-\u9fff\uf900-\ufaff]", data.decode("utf-8-sig")),
                    f"Chinese text in English release member: {name}")
    files["patch/SHA256SUMS.txt"] = "".join(
        f"{sha(data)}  {name}\n" for name, data in sorted(files.items())
    ).encode("ascii")
    require(re.fullmatch(r"\d+\.\d+\.\d+", manifest["version"]), "Invalid release version.")
    return f"Shank2-v{manifest['version']}-MOD", files


def package(out, name, files):
    out = out.resolve()
    require(not out.exists(), f"Output already exists; choose a new directory: {out}")
    out.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix=".shank2-build-", dir=out.parent) as work:
        stage = Path(work) / "result"
        folder = stage / name
        folder.mkdir(parents=True)
        archive = stage / f"{name}.zip"
        with zipfile.ZipFile(archive, "w") as z:
            for member, data in sorted(files.items()):
                path = folder / member
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(data)
                info = zipfile.ZipInfo(member, date_time=(1980, 1, 1, 0, 0, 0))
                info.create_system = 3
                info.external_attr = 0o100644 << 16
                z.writestr(info, data, compress_type=zipfile.ZIP_DEFLATED, compresslevel=6)
        with zipfile.ZipFile(archive) as z:
            require(z.namelist() == sorted(files) and
                    all(z.read(member) == (folder / member).read_bytes() for member in files),
                    "ZIP does not match the release directory.")
        digest = sha(archive.read_bytes())
        stage.rename(out)
    print(f"{digest}  {out / archive.name} (zlib {zlib.ZLIB_RUNTIME_VERSION})")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--game-dir", type=Path, help="Verify an unmodified Steam game, read-only")
    mode.add_argument("--package-only", action="store_true", help="Package without game-side verification")
    parser.add_argument("--out", type=Path, default=ROOT / "dist", help="New output directory")
    args = parser.parse_args()
    try:
        package(args.out, *collect(args.game_dir))
    except (OSError, ValueError) as error:
        parser.exit(1, f"Build failed: {error}\n")


if __name__ == "__main__":
    main()
