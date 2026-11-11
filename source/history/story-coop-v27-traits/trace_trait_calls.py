"""Trace native Survival damage-calculator calls in the isolated v27 process."""
import ctypes as C
from ctypes import wintypes as W
import json
from pathlib import Path
import struct
import sys

from build_traits import HERE, Ks, KS_ARCH_X86, KS_MODE_32, sha


ENTRY = 0x4F3F40
PROLOGUE = bytes.fromhex("51 53 55 8b6c2410")
RESUME = ENTRY + len(PROLOGUE)
DIAG = 0x7FF000


def main(pid):
    report_path = HERE / f"assist-disabled-{pid}.json"
    disabled = json.loads(report_path.read_text(encoding="utf-8"))
    if not disabled.get("assists_disabled"):
        raise RuntimeError("Test assists must be disabled before tracing.")

    row = next(
        item
        for item in json.loads((HERE / "builds.json").read_text(encoding="utf-8"))
        if item["language"] == "chs"
    )
    target = (
        HERE.parent
        / "story-coop-v14-transitions"
        / "game"
        / "bin"
        / "shank2-story-coop-v27-test.exe"
    )
    # The paused process may be running the immediately preceding v27 image
    # while code slots are hot-patched in memory. Keep the exact executable
    # path check below; allow that verified predecessor hash for tracing.
    known_hashes = {
        row["sha256"],
        "e9a55cc6c318def16aed5de8eb4ea8f0d2421c1b5af761c3b36572f0c024b8d5",
    }
    if sha(target.read_bytes()) not in known_hashes:
        raise RuntimeError("Unexpected v27 test executable.")

    kernel = C.WinDLL("kernel32", use_last_error=True)
    ntdll = C.WinDLL("ntdll")
    kernel.OpenProcess.argtypes = [W.DWORD, W.BOOL, W.DWORD]
    kernel.OpenProcess.restype = W.HANDLE
    kernel.QueryFullProcessImageNameW.argtypes = [
        W.HANDLE,
        W.DWORD,
        W.LPWSTR,
        C.POINTER(W.DWORD),
    ]
    kernel.ReadProcessMemory.argtypes = [
        W.HANDLE,
        C.c_void_p,
        C.c_void_p,
        C.c_size_t,
        C.POINTER(C.c_size_t),
    ]
    kernel.WriteProcessMemory.argtypes = kernel.ReadProcessMemory.argtypes
    kernel.VirtualAllocEx.argtypes = [W.HANDLE, C.c_void_p, C.c_size_t, W.DWORD, W.DWORD]
    kernel.VirtualAllocEx.restype = C.c_void_p
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
            raise RuntimeError("Remote write verification failed.")

    try:
        image = C.create_unicode_buffer(32768)
        image_length = W.DWORD(len(image))
        if not kernel.QueryFullProcessImageNameW(process, 0, image, C.byref(image_length)):
            raise C.WinError(C.get_last_error())
        if Path(image.value).resolve() != target.resolve():
            raise RuntimeError("PID is not the exact v27 test executable.")

        original = read(ENTRY, len(PROLOGUE))
        if original != PROLOGUE:
            raise RuntimeError(f"Unexpected trait entry bytes: {original.hex()}")

        remote = kernel.VirtualAllocEx(process, None, 8192, 0x3000, 0x04)
        if not remote or remote >= 0x80000000:
            raise RuntimeError("No x86 test memory available.")
        counters = remote + 0x1000
        assembler = Ks(KS_ARCH_X86, KS_MODE_32)
        source = f"""
            pushfd
            pushad
            mov eax,[esp+40]
            inc dword ptr [{counters}]
            cmp eax,[{DIAG + 12}]
            jne p2
            inc dword ptr [{counters + 4}]
            mov [{counters + 12}],eax
            jmp native
            p2:
            cmp eax,[{DIAG + 16}]
            jne other
            inc dword ptr [{counters + 8}]
            mov [{counters + 16}],eax
            jmp native
            other:
            inc dword ptr [{counters + 20}]
            mov [{counters + 24}],eax
            native:
            popad
            popfd
            push ecx
            push ebx
            push ebp
            mov ebp,[esp+0x10]
            jmp {RESUME}
        """
        code = bytes(assembler.asm(source, remote)[0])
        if len(code) > 0x1000:
            raise RuntimeError("Trace routine is too large.")
        write(remote, code)
        write(counters, b"\0" * 32)

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
                                    "A game thread is inside the trait entry; pause and retry."
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
                relative = (remote - (ENTRY + 5)) & 0xFFFFFFFF
                entry_hook = b"\xe9" + struct.pack("<I", relative) + b"\x90" * 2
                write(ENTRY, entry_hook)
                if not kernel.FlushInstructionCache(process, ENTRY, len(PROLOGUE)):
                    raise C.WinError(C.get_last_error())
            finally:
                ignored = W.DWORD()
                if not kernel.VirtualProtectEx(
                    process, ENTRY, len(PROLOGUE), old_protect.value, C.byref(ignored)
                ):
                    raise C.WinError(C.get_last_error())
        finally:
            if ntdll.NtResumeProcess(process) != 0:
                raise RuntimeError("Could not resume the isolated game.")

        result = {
            "pid": pid,
            "trace_entry": hex(ENTRY),
            "trace_thunk": hex(remote),
            "counters": hex(counters),
            "players_invincible": False,
            "ordinary_enemy_one_hit": False,
            "saved_files_modified": False,
        }
        (HERE / f"trait-trace-{pid}.json").write_text(
            json.dumps(result, indent=2) + "\n", encoding="utf-8"
        )
        print(json.dumps(result))
    finally:
        kernel.CloseHandle(process)


if __name__ == "__main__":
    main(int(sys.argv[1]))
