"""Hot-load the ranged-owner-aware scope into the paused v27 process."""
import ctypes as C
from ctypes import wintypes as W
import json
from pathlib import Path
import struct
import sys

from build_traits import HERE, Ks, KS_ARCH_X86, KS_MODE_32, routines


def main(pid):
    row = next(
        item
        for item in json.loads((HERE / "builds.json").read_text(encoding="utf-8"))
        if item["language"] == "chs"
    )
    code = int(row["code"], 16)
    data = int(row["data"], 16)
    scope = code + 0x1800
    hot = code + 0x2000
    blob = routines(code, data)["scope"][1]

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

    def write(address, value):
        received = C.c_size_t()
        if not kernel.WriteProcessMemory(
            process, address, C.create_string_buffer(value), len(value), C.byref(received)
        ) or received.value != len(value):
            raise C.WinError(C.get_last_error())
        if read(address, len(value)) != value:
            raise RuntimeError("Runtime scope write verification failed.")

    try:
        relative = (hot - (scope + 5)) & 0xFFFFFFFF
        hook = b"\xe9" + struct.pack("<I", relative) + b"\x90\x90"
        current = read(scope, 5)
        if current == hook[:5]:
            if read(hot, len(blob)) != blob:
                raise RuntimeError("Scope jump exists but hotpatch body is incomplete.")
            result = {
                "pid": pid,
                "scope_hotpatched": True,
                "scope_entry": hex(scope),
                "scope_entry_bytes": current.hex(),
                "expected_hook": hook.hex(),
                "scope_thunk": hex(hot),
                "scope_bytes": len(blob),
                "ranged_owner_supported": True,
                "players_invincible": False,
                "ordinary_enemy_one_hit": False,
                "saved_files_modified": False,
            }
            (HERE / f"scope-hotpatch-{pid}.json").write_text(
                json.dumps(result, indent=2) + "\n", encoding="utf-8"
            )
            print(json.dumps(result))
            return
        if current[:2] != b"\x31\xc0" and current != hook:
            raise RuntimeError(f"Unexpected current scope entry: {current.hex()}")
        free = read(hot, len(blob))
        if any(byte not in (0x00, 0xCC) for byte in free):
            raise RuntimeError("Selected hotpatch area is not empty.")

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
                            if scope <= eip < scope + 0x100:
                                raise RuntimeError(
                                    "A game thread is inside the old scope; "
                                    "pause the game and retry."
                                )
                        finally:
                            kernel.CloseHandle(thread)
                    more = kernel.Thread32Next(snapshot, C.byref(item))
            finally:
                kernel.CloseHandle(snapshot)

            old_protect = W.DWORD()
            if not kernel.VirtualProtectEx(
                process, hot, len(blob), 0x40, C.byref(old_protect)
            ):
                raise C.WinError(C.get_last_error())
            try:
                write(hot, blob)
                if not kernel.FlushInstructionCache(process, hot, len(blob)):
                    raise C.WinError(C.get_last_error())
            finally:
                ignored = W.DWORD()
                if not kernel.VirtualProtectEx(
                    process, hot, len(blob), old_protect.value, C.byref(ignored)
                ):
                    raise C.WinError(C.get_last_error())

            if not kernel.VirtualProtectEx(
                process, scope, len(hook), 0x40, C.byref(old_protect)
            ):
                raise C.WinError(C.get_last_error())
            try:
                write(scope, hook)
                if not kernel.FlushInstructionCache(process, scope, len(hook)):
                    raise C.WinError(C.get_last_error())
            finally:
                ignored = W.DWORD()
                if not kernel.VirtualProtectEx(
                    process, scope, len(hook), old_protect.value, C.byref(ignored)
                ):
                    raise C.WinError(C.get_last_error())
        finally:
            if ntdll.NtResumeProcess(process) != 0:
                raise RuntimeError("Could not resume the isolated game.")

        result = {
            "pid": pid,
            "scope_hotpatched": read(scope, 5) == hook[:5],
            "scope_entry": hex(scope),
            "scope_entry_bytes": read(scope, 5).hex(),
            "expected_hook": hook.hex(),
            "scope_thunk": hex(hot),
            "scope_bytes": len(blob),
            "ranged_owner_supported": True,
            "players_invincible": False,
            "ordinary_enemy_one_hit": False,
            "saved_files_modified": False,
        }
        (HERE / f"scope-hotpatch-{pid}.json").write_text(
            json.dumps(result, indent=2) + "\n", encoding="utf-8"
        )
        print(json.dumps(result))
    finally:
        kernel.CloseHandle(process)


if __name__ == "__main__":
    main(int(sys.argv[1]))
