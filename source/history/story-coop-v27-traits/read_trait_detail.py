"""Read and decode the process-only detailed trait trace."""
import ctypes as C
from ctypes import wintypes as W
import json
import re
import struct
import sys

from build_traits import DIAG, HERE


def main(pid):
    trace = json.loads(
        (HERE / f"trait-detail-{pid}.json").read_text(encoding="utf-8")
    )
    kernel = C.WinDLL("kernel32", use_last_error=True)
    kernel.OpenProcess.argtypes = [W.DWORD, W.BOOL, W.DWORD]
    kernel.OpenProcess.restype = W.HANDLE
    kernel.ReadProcessMemory.argtypes = [
        W.HANDLE,
        C.c_void_p,
        C.c_void_p,
        C.c_size_t,
        C.POINTER(C.c_size_t),
    ]
    kernel.CloseHandle.argtypes = [W.HANDLE]
    process = kernel.OpenProcess(0x1010, False, pid)
    if not process:
        raise C.WinError(C.get_last_error())

    def read(address, size):
        buffer = C.create_string_buffer(size)
        received = C.c_size_t()
        if not kernel.ReadProcessMemory(
            process, address, buffer, size, C.byref(received)
        ) or received.value != size:
            raise C.WinError(C.get_last_error())
        return buffer.raw

    try:
        def hash_name(text):
            value = 0
            for char in text.encode():
                value = (value * 0x1003F + char) & 0xFFFFFFFF
            return value

        lua = (
            HERE.parent
            / "story-coop-v14-transitions"
            / "game"
            / "data"
            / "bootstrap"
            / "skins.lua"
        ).read_text(encoding="utf-8")
        names = {
            hash_name(name): name
            for name in re.findall(r'\b(?:name|tag)\s*=\s*"([^"]+)"', lua)
        }

        counters = int(trace["counters"], 16)
        entry_count, tag_count = struct.unpack("<2I", read(counters, 8))
        p1 = struct.unpack("<I", read(DIAG + 12, 4))[0]
        p2 = struct.unpack("<I", read(DIAG + 16, 4))[0]

        def decode_entries():
            base = int(trace["entry_records"], 16)
            count = min(entry_count, 128)
            raw = read(base, 128 * 0x30)
            values = []
            for index in range(count):
                row = struct.unpack_from("<12I", raw, index * 0x30)
                if not any(row):
                    continue
                values.append(
                    {
                        "arg": hex(row[0]),
                        "return": hex(row[1]),
                        "entry_ecx": hex(row[2]),
                        "thread": row[3],
                        "actor": hex(row[4]),
                        "actor_vtable": hex(row[5]),
                        "simulation": hex(row[6]),
                        "actor_38": hex(row[7]),
                        "actor_e4": row[8],
                        "actor_148": hex(row[9]),
                        "actor_150": hex(row[10]),
                        "actor_158": hex(row[11]),
                        "actor_is_p1": row[4] == p1,
                        "actor_is_p2": row[4] == p2,
                    }
                )
            return values

        def decode_tags():
            base = int(trace["tag_records"], 16)
            count = min(tag_count, 128)
            raw = read(base, 128 * 0x20)
            values = []
            for index in range(count):
                row = struct.unpack_from("<6I", raw, index * 0x20)
                if not any(row):
                    continue
                values.append(
                    {
                        "actor": hex(row[0]),
                        "tag": names.get(row[1], hex(row[1])),
                        "tag_hash": hex(row[1]),
                        "tag_multiplier": struct.unpack("<f", struct.pack("<I", row[2]))[0],
                        "before": struct.unpack("<f", struct.pack("<I", row[3]))[0],
                        "return": hex(row[4]),
                        "thread": row[5],
                        "actor_is_p1": row[0] == p1,
                        "actor_is_p2": row[0] == p2,
                    }
                )
            return values

        result = {
            "pid": pid,
            "entry_count": entry_count,
            "tag_count": tag_count,
            "current_p1": hex(p1),
            "current_p2": hex(p2),
            "entries": decode_entries(),
            "tags": decode_tags(),
        }
        report = json.dumps(result, indent=2)
        print(report)
        (HERE / "latest-detail.json").write_text(report + "\n", encoding="utf-8")
    finally:
        kernel.CloseHandle(process)


if __name__ == "__main__":
    main(int(sys.argv[1]))
