"""Read the process-only v27 trait-call trace counters."""
import ctypes as C
from ctypes import wintypes as W
import json
from pathlib import Path
import struct
import sys

from build_traits import DIAG, HERE


def main(pid):
    trace = json.loads(
        (HERE / f"trait-trace-{pid}.json").read_text(encoding="utf-8")
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
    try:
        def read(address, size):
            buffer = C.create_string_buffer(size)
            received = C.c_size_t()
            if not kernel.ReadProcessMemory(
                process, address, buffer, size, C.byref(received)
            ) or received.value != size:
                raise C.WinError(C.get_last_error())
            return buffer.raw

        counters = int(trace["counters"], 16)
        total, p1, p2, last_p1, last_p2, other, last_other = struct.unpack(
            "<7I", read(counters, 28)
        )
        result = {
            "pid": pid,
            "total_calls": total,
            "p1_calls": p1,
            "p2_calls": p2,
            "other_calls": other,
            "last_p1": hex(last_p1),
            "last_p2": hex(last_p2),
            "last_other": hex(last_other),
            "current_p1": hex(struct.unpack("<I", read(DIAG + 12, 4))[0]),
            "current_p2": hex(struct.unpack("<I", read(DIAG + 16, 4))[0]),
        }
        print(json.dumps(result, indent=2))
    finally:
        kernel.CloseHandle(process)


if __name__ == "__main__":
    main(int(sys.argv[1]))
