"""Hotpatch native Survival trait calculation to use the attacking player.

The damage event stores the attacked actor at +8 and the attacking actor ID at
+0x44.  When that ID belongs to a registered co-op player, this process-only
wrapper temporarily substitutes the attacking player at event+8 for the native
damage-bonus calculation, then restores the attacked actor before returning.
"""
import ctypes as C
from ctypes import wintypes as W
import json
from pathlib import Path
import struct
import sys

from build_traits import HERE, Ks, KS_ARCH_X86, KS_MODE_32, sha


ENTRY = 0x4F3F40
ENTRY_PROLOGUE = bytes.fromhex("51 53 55 8b6c2410")
ENTRY_RESUME = ENTRY + len(ENTRY_PROLOGUE)

RETURN = 0x4F4061
RETURN_PROLOGUE = bytes.fromhex("5f 5e 5d 5b 59")

DIAG = 0x7FF000


def main(pid):
    raise RuntimeError('Withdrawn experiment: do not replace event+8. Use the scoped projectile-construction gate in build_traits.py.')
    disabled_path = HERE / f"trait-detail-disabled-{pid}.json"
    if not disabled_path.exists() or not json.loads(
        disabled_path.read_text(encoding="utf-8")
    ).get("detail_trace_disabled"):
        raise RuntimeError("Disable the detail trace before installing trait swap.")

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
    kernel.VirtualAllocEx.argtypes = [
        W.HANDLE,
        C.c_void_p,
        C.c_size_t,
        W.DWORD,
        W.DWORD,
    ]
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
            process,
            address,
            C.create_string_buffer(data),
            len(data),
            C.byref(received),
        ) or received.value != len(data):
            raise C.WinError(C.get_last_error())
        if read(address, len(data)) != data:
            raise RuntimeError("Remote write verification failed.")

    def patch(address, old, new):
        if read(address, len(old)) != old:
            raise RuntimeError(
                f"Unexpected bytes at {address:#x}: {read(address, len(old)).hex()}"
            )
        old_protect = W.DWORD()
        if not kernel.VirtualProtectEx(
            process, address, len(old), 0x40, C.byref(old_protect)
        ):
            raise C.WinError(C.get_last_error())
        try:
            write(address, new)
        finally:
            ignored = W.DWORD()
            if not kernel.VirtualProtectEx(
                process, address, len(old), old_protect.value, C.byref(ignored)
            ):
                raise C.WinError(C.get_last_error())
        if not kernel.FlushInstructionCache(process, address, len(new)):
            raise C.WinError(C.get_last_error())

    try:
        image = C.create_unicode_buffer(32768)
        image_length = W.DWORD(len(image))
        if not kernel.QueryFullProcessImageNameW(
            process, 0, image, C.byref(image_length)
        ):
            raise C.WinError(C.get_last_error())
        if Path(image.value).resolve() != target.resolve():
            raise RuntimeError("PID is not the exact v27 test executable.")

        if read(ENTRY, len(ENTRY_PROLOGUE)) != ENTRY_PROLOGUE:
            raise RuntimeError("Trait entry is not in its native state.")
        if read(RETURN, len(RETURN_PROLOGUE)) != RETURN_PROLOGUE:
            raise RuntimeError("Trait return site is not in its native state.")

        remote = kernel.VirtualAllocEx(process, None, 0x8000, 0x3000, 0x04)
        if not remote or remote >= 0x80000000:
            raise RuntimeError("No x86 test memory available.")
        entry_thunk = remote
        return_thunk = remote + 0x800
        counters = remote + 0x1000
        shadow = remote + 0x2000

        assembler = Ks(KS_ARCH_X86, KS_MODE_32)
        entry_source = f"""
            pushfd
            pushad
            mov eax,[esp+40]
            test eax,eax
            jz native
            mov edx,[eax+0x44]
            mov ecx,[{DIAG+12}]
            test ecx,ecx
            jz try_p2
            cmp edx,[ecx+0xd4]
            je p1
            try_p2:
            mov ecx,[{DIAG+16}]
            test ecx,ecx
            jz native
            cmp edx,[ecx+0xd4]
            je p2
            jmp native
            p1:
            inc dword ptr [{counters+4}]
            mov edx,ecx
            jmp swap
            p2:
            inc dword ptr [{counters+8}]
            mov edx,ecx
            swap:
            inc dword ptr [{counters}]
            mov ecx,dword ptr fs:[0x24]
            mov edi,ecx
            and edi,255
            imul edi,edi,12
            add edi,{shadow}
            mov [edi],ecx
            mov [edi+4],eax
            mov ecx,[eax+8]
            mov [edi+8],ecx
            mov [eax+8],edx
            native:
            popad
            popfd
            push ecx
            push ebx
            push ebp
            mov ebp,[esp+0x10]
            jmp {ENTRY_RESUME}
        """
        return_source = f"""
            pushfd
            pushad
            mov eax,dword ptr fs:[0x24]
            mov edx,eax
            and edx,255
            imul edx,edx,12
            add edx,{shadow}
            cmp [edx],eax
            jne native_return
            mov ecx,[edx+4]
            test ecx,ecx
            jz clear_shadow
            mov eax,[edx+8]
            mov [ecx+8],eax
            clear_shadow:
            mov dword ptr [edx],0
            native_return:
            popad
            popfd
            pop edi
            pop esi
            pop ebp
            pop ebx
            pop ecx
            ret 4
        """
        entry_code = bytes(assembler.asm(entry_source, entry_thunk)[0])
        return_code = bytes(assembler.asm(return_source, return_thunk)[0])
        if len(entry_code) > 0x800 or len(return_code) > 0x800:
            raise RuntimeError("Trait swap routine is too large.")
        write(entry_thunk, entry_code)
        write(return_thunk, return_code)
        write(counters, b"\0" * 0x20)
        write(shadow, b"\0" * 0xC00)

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
                            eip = struct.unpack(
                                "<I", C.string_at(context + 184, 4)
                            )[0]
                            if ENTRY <= eip < ENTRY + len(ENTRY_PROLOGUE):
                                raise RuntimeError(
                                    "A game thread is inside the trait entry; pause and retry."
                                )
                            if RETURN <= eip < RETURN + len(RETURN_PROLOGUE):
                                raise RuntimeError(
                                    "A game thread is inside the trait return site; pause and retry."
                                )
                        finally:
                            kernel.CloseHandle(thread)
                    more = kernel.Thread32Next(snapshot, C.byref(item))
            finally:
                kernel.CloseHandle(snapshot)

            entry_hook = (
                b"\xe9"
                + struct.pack("<I", (entry_thunk - (ENTRY + 5)) & 0xFFFFFFFF)
                + b"\x90\x90"
            )
            return_hook = (
                b"\xe9"
                + struct.pack("<I", (return_thunk - (RETURN + 5)) & 0xFFFFFFFF)
            )
            patch(ENTRY, ENTRY_PROLOGUE, entry_hook)
            patch(RETURN, RETURN_PROLOGUE, return_hook)
        finally:
            if ntdll.NtResumeProcess(process) != 0:
                raise RuntimeError("Could not resume the isolated game.")

        result = {
            "pid": pid,
            "entry": hex(ENTRY),
            "return_site": hex(RETURN),
            "entry_thunk": hex(entry_thunk),
            "return_thunk": hex(return_thunk),
            "counters": hex(counters),
            "shadow": hex(shadow),
            "players_invincible": False,
            "ordinary_enemy_one_hit": False,
            "saved_files_modified": False,
        }
        (HERE / f"trait-swap-{pid}.json").write_text(
            json.dumps(result, indent=2) + "\n", encoding="utf-8"
        )
        print(json.dumps(result))
    finally:
        kernel.CloseHandle(process)


if __name__ == "__main__":
    main(int(sys.argv[1]))
