"""Remove the process-only trait-call tracer."""
import ctypes as C
from ctypes import wintypes as W
import json
from pathlib import Path
import struct
import sys

from build_traits import HERE


ENTRY = 0x4F3F40
PROLOGUE = bytes.fromhex("51 53 55 8b6c2410")


def main(pid):
    trace = json.loads(
        (HERE / f"trait-trace-{pid}.json").read_text(encoding="utf-8")
    )
    thunk = int(trace["trace_thunk"], 16)
    relative = (thunk - (ENTRY + 5)) & 0xFFFFFFFF
    hook = b"\xe9" + struct.pack("<I", relative) + b"\x90\x90"

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
    kernel.CreateToolhelp32Snapshot.argtypes = [W.DWORD, W.DWORD]
    kernel.CreateToolhelp32Snapshot.restype = W.HANDLE
    kernel.OpenThread.argtypes = [W.DWORD, W.BOOL, W.DWORD]
    kernel.OpenThread.restype = W.HANDLE
    kernel.Wow64GetThreadContext.argtypes = [W.HANDLE, C.c_void_p]

    class Thread(C.Structure):
        _fields_ = [
            ("size", W.DWORD),
            ("usage", W.DWORD),
            ("id", W.DWORD),
            ("owner", W.DWORD),
            ("priority", W.LONG),
            ("delta", W.LONG),
            ("flags", W.DWORD),
        ]

    kernel.Thread32First.argtypes = [W.HANDLE, C.POINTER(Thread)]
    kernel.Thread32Next.argtypes = kernel.Thread32First.argtypes

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

    def write(address, data):
        received = C.c_size_t()
        if not kernel.WriteProcessMemory(
            process, address, C.create_string_buffer(data), len(data), C.byref(received)
        ) or received.value != len(data):
            raise C.WinError(C.get_last_error())
        if read(address, len(data)) != data:
            raise RuntimeError("Trace restore verification failed.")

    try:
        current = read(ENTRY, len(PROLOGUE))
        if current == PROLOGUE:
            disabled = True
        elif current != hook:
            raise RuntimeError(f"Unexpected trace hook bytes: {current.hex()}")
        else:
            if ntdll.NtSuspendProcess(process) != 0:
                raise RuntimeError("Could not suspend the isolated game.")
            try:
                snapshot = kernel.CreateToolhelp32Snapshot(4, 0)
                if snapshot == C.c_void_p(-1).value:
                    raise C.WinError(C.get_last_error())
                try:
                    item = Thread()
                    item.size = C.sizeof(item)
                    more = kernel.Thread32First(snapshot, C.byref(item))
                    while more:
                        if item.owner == pid:
                            thread = kernel.OpenThread(0x48, False, item.id)
                            if not thread:
                                raise C.WinError(C.get_last_error())
                            try:
                                storage = C.create_string_buffer(732)
                                context = (C.addressof(storage) + 15) & ~15
                                C.memmove(context, struct.pack("<I", 0x10001), 4)
                                if not kernel.Wow64GetThreadContext(thread, context):
                                    raise C.WinError(C.get_last_error())
                                eip = struct.unpack("<I", C.string_at(context + 184, 4))[0]
                                if ENTRY <= eip < ENTRY + len(PROLOGUE):
                                    raise RuntimeError(
                                        "A game thread is inside the trace entry; "
                                        "pause the game and retry."
                                    )
                            finally:
                                kernel.CloseHandle(thread)
                        more = kernel.Thread32Next(snapshot, C.byref(item))
                finally:
                    kernel.CloseHandle(snapshot)

                old_protect = W.DWORD()
                if not kernel.VirtualProtectEx(
                    process, ENTRY, len(PROLOGUE), 0x40, C.byref(old_protect)
                ):
                    raise C.WinError(C.get_last_error())
                try:
                    write(ENTRY, PROLOGUE)
                finally:
                    ignored = W.DWORD()
                    if not kernel.VirtualProtectEx(
                        process, ENTRY, len(PROLOGUE), old_protect.value, C.byref(ignored)
                    ):
                        raise C.WinError(C.get_last_error())
                if not kernel.FlushInstructionCache(process, ENTRY, len(PROLOGUE)):
                    raise C.WinError(C.get_last_error())
            finally:
                if ntdll.NtResumeProcess(process) != 0:
                    raise RuntimeError("Could not resume the isolated game.")
            disabled = read(ENTRY, len(PROLOGUE)) == PROLOGUE

        result = {
            "pid": pid,
            "trace_disabled": disabled,
            "entry": hex(ENTRY),
            "entry_bytes": read(ENTRY, len(PROLOGUE)).hex(),
        }
        (HERE / f"trait-trace-disabled-{pid}.json").write_text(
            json.dumps(result, indent=2) + "\n", encoding="utf-8"
        )
        print(json.dumps(result))
    finally:
        kernel.CloseHandle(process)


if __name__ == "__main__":
    main(int(sys.argv[1]))
