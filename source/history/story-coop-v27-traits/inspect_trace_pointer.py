"""Inspect the unmatched native object passed by ranged damage."""
import ctypes as C
from ctypes import wintypes as W
import json
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
        values = struct.unpack("<7I", read(counters, 28))
        unmatched = values[6]
        simulation = struct.unpack("<I", read(DIAG + 36, 4))[0]
        p1 = struct.unpack("<I", read(DIAG + 12, 4))[0]
        p2 = struct.unpack("<I", read(DIAG + 16, 4))[0]
        object_bytes = read(unmatched, 0x400)
        dwords = struct.unpack("<256I", object_bytes)
        hits = {}
        for target, name in ((simulation, "simulation"), (p1, "p1"), (p2, "p2")):
            hits[name] = [
                hex(index * 4)
                for index, value in enumerate(dwords)
                if value == target
            ]
        result = {
            "unmatched": hex(unmatched),
            "simulation": hex(simulation),
            "p1": hex(p1),
            "p2": hex(p2),
            "object_dwords": {
                hex(index * 4): hex(value)
                for index, value in enumerate(dwords[:64])
                if value
            },
            "reference_offsets": hits,
        }
        print(json.dumps(result, indent=2))
    finally:
        kernel.CloseHandle(process)


if __name__ == "__main__":
    main(int(sys.argv[1]))
