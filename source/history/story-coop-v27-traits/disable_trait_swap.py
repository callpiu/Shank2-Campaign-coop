"""Remove the process-only attacking-player trait swap."""
import ctypes as C
from ctypes import wintypes as W
import json
import struct
import sys

from build_traits import HERE


ENTRY = 0x4F3F40
ENTRY_PROLOGUE = bytes.fromhex("51 53 55 8b6c2410")
RETURN = 0x4F4061
RETURN_PROLOGUE = bytes.fromhex("5f 5e 5d 5b 59")


def main(pid):
    state = json.loads(
        (HERE / f"trait-swap-{pid}.json").read_text(encoding="utf-8")
    )
    entry_thunk = int(state["entry_thunk"], 16)
    return_thunk = int(state["return_thunk"], 16)
    entry_hook = (
        b"\xe9"
        + struct.pack("<I", (entry_thunk - (ENTRY + 5)) & 0xFFFFFFFF)
        + b"\x90\x90"
    )
    return_hook = (
        b"\xe9"
        + struct.pack("<I", (return_thunk - (RETURN + 5)) & 0xFFFFFFFF)
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

    def restore(address, expected, original):
        current = read(address, len(original))
        if current == original:
            return
        if current != expected:
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
            restore(RETURN, return_hook, RETURN_PROLOGUE)
        finally:
            if ntdll.NtResumeProcess(process) != 0:
                raise RuntimeError("Could not resume the isolated game.")

        result = {
            "pid": pid,
            "trait_swap_disabled": (
                read(ENTRY, len(ENTRY_PROLOGUE)) == ENTRY_PROLOGUE
                and read(RETURN, len(RETURN_PROLOGUE)) == RETURN_PROLOGUE
            ),
        }
        (HERE / f"trait-swap-disabled-{pid}.json").write_text(
            json.dumps(result, indent=2) + "\n", encoding="utf-8"
        )
        print(json.dumps(result))
    finally:
        kernel.CloseHandle(process)


if __name__ == "__main__":
    main(int(sys.argv[1]))
