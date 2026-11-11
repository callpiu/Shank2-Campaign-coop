"""Read trait-swap counters and current player trait stats."""
import ctypes as C
from ctypes import wintypes as W
import json
import struct
import sys

from build_traits import DIAG, HERE


def main(pid):
    state = json.loads(
        (HERE / f"trait-swap-{pid}.json").read_text(encoding="utf-8")
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
        counters = int(state["counters"], 16)
        swaps, p1_swaps, p2_swaps = struct.unpack("<3I", read(counters, 12))
        p1 = struct.unpack("<I", read(DIAG + 12, 4))[0]
        p2 = struct.unpack("<I", read(DIAG + 16, 4))[0]
        result = {
            "pid": pid,
            "swaps": swaps,
            "p1_swaps": p1_swaps,
            "p2_swaps": p2_swaps,
            "current_p1": hex(p1),
            "current_p2": hex(p2),
            "p1_id": hex(struct.unpack("<I", read(p1 + 0xD4, 4))[0]) if p1 else None,
            "p2_id": hex(struct.unpack("<I", read(p2 + 0xD4, 4))[0]) if p2 else None,
        }
        print(json.dumps(result, indent=2))
    finally:
        kernel.CloseHandle(process)


if __name__ == "__main__":
    main(int(sys.argv[1]))
