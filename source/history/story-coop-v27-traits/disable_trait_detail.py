"""Remove the process-only detailed trait tracer."""
import ctypes as C
from ctypes import wintypes as W
import json
import struct
import sys

from build_traits import HERE


ENTRY = 0x4F3F40
ENTRY_PROLOGUE = bytes.fromhex("51 53 55 8b6c2410")
TAG = 0x80BA80
TAG_PROLOGUE = bytes.fromhex("50 51 52 8b4d08")


def main(pid):
    trace = json.loads(
        (HERE / f"trait-detail-{pid}.json").read_text(encoding="utf-8")
    )
    entry_thunk = int(trace["entry_thunk"], 16)
    tag_thunk = int(trace["tag_thunk"], 16)
    entry_hook = (
        b"\xe9"
        + struct.pack("<I", (entry_thunk - (ENTRY + 5)) & 0xFFFFFFFF)
        + b"\x90\x90"
    )
    tag_hook = (
        b"\xe9"
        + struct.pack("<I", (tag_thunk - (TAG + 5)) & 0xFFFFFFFF)
        + b"\x90"
    )

    kernel = C.WinDLL("kernel32", use_last_error=True)
    ntdll = C.WinDLL("ntdll")
    kernel.OpenProcess.argtypes = [W.DWORD, W.BOOL, W.DWORD]
    kernel.OpenProcess.restype = W.HANDLE
    kernel.ReadProcessMemory.argtypes = [
        W.HANDLE,
        C.c_void_p,
        C.c_void_p,
        C.c_size_t,
        C.POINTER(C.c_size_t),
    ]
    kernel.WriteProcessMemory.argtypes = kernel.ReadProcessMemory.argtypes
    kernel.VirtualProtectEx.argtypes = [
        W.HANDLE,
        C.c_void_p,
        C.c_size_t,
        W.DWORD,
        C.POINTER(W.DWORD),
    ]
    kernel.FlushInstructionCache.argtypes = [W.HANDLE, C.c_void_p, C.c_size_t]
    kernel.CloseHandle.argtypes = [W.HANDLE]
    ntdll.NtSuspendProcess.argtypes = [W.HANDLE]
    ntdll.NtSuspendProcess.restype = W.LONG
    ntdll.NtResumeProcess.argtypes = [W.HANDLE]
    ntdll.NtResumeProcess.restype = W.LONG

    process = kernel.OpenProcess(0x1C38, False, pid)
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

    def restore(address, current_expected, original):
        if read(address, len(original)) == original:
            return
        if read(address, len(current_expected)) != current_expected:
            raise RuntimeError(f"Unexpected hook bytes at {address:#x}.")
        old_protect = W.DWORD()
        if not kernel.VirtualProtectEx(
            process, address, len(original), 0x40, C.byref(old_protect)
        ):
            raise C.WinError(C.get_last_error())
        try:
            received = C.c_size_t()
            if not kernel.WriteProcessMemory(
                process,
                address,
                C.create_string_buffer(original),
                len(original),
                C.byref(received),
            ) or received.value != len(original):
                raise C.WinError(C.get_last_error())
        finally:
            ignored = W.DWORD()
            if not kernel.VirtualProtectEx(
                process,
                address,
                len(original),
                old_protect.value,
                C.byref(ignored),
            ):
                raise C.WinError(C.get_last_error())
        if not kernel.FlushInstructionCache(process, address, len(original)):
            raise C.WinError(C.get_last_error())

    try:
        if ntdll.NtSuspendProcess(process) != 0:
            raise RuntimeError("Could not suspend the isolated game.")
        try:
            restore(ENTRY, entry_hook, ENTRY_PROLOGUE)
            restore(TAG, tag_hook, TAG_PROLOGUE)
        finally:
            if ntdll.NtResumeProcess(process) != 0:
                raise RuntimeError("Could not resume the isolated game.")

        result = {
            "pid": pid,
            "detail_trace_disabled": (
                read(ENTRY, len(ENTRY_PROLOGUE)) == ENTRY_PROLOGUE
                and read(TAG, len(TAG_PROLOGUE)) == TAG_PROLOGUE
            ),
        }
        (HERE / f"trait-detail-disabled-{pid}.json").write_text(
            json.dumps(result, indent=2) + "\n", encoding="utf-8"
        )
        print(json.dumps(result))
    finally:
        kernel.CloseHandle(process)


if __name__ == "__main__":
    main(int(sys.argv[1]))
