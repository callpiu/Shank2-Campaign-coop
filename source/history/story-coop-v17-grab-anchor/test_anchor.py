"""Reuse the deferred lifetime regression, then check actual x86 alignment."""
import os
from pathlib import Path
import struct
import subprocess
import tempfile
from anchor import HERE, load_anchor, routine
import test_deferred as fixture

source=load_anchor()
ks=fixture.ks;asm=lambda s,a:bytes(ks.asm(s,a)[0])
buf=bytearray(fixture.buf)
code=routine(asm,fixture.B,diag=fixture.B+0x3000,native=fixture.B+0x1000,
    lookup=fixture.B+0x1100,metrics=fixture.B+0x3040)
assert len(code)<0x800
buf[:0x800]=bytes(0x800);buf[:len(code)]=code
struct.pack_into('<6f',buf,0x503c,1,0,55752.27734375,0,1,1365.2650146484375)
with tempfile.TemporaryDirectory(dir=HERE,prefix='align-') as folder:
    f=Path(folder)/'test.bin';f.write_bytes(buf)
    ps=Path(os.environ['WINDIR'])/'SysWOW64/WindowsPowerShell/v1.0/powershell.exe'
    subprocess.run([str(ps),'-NoProfile','-ExecutionPolicy','Bypass','-File',
        str(HERE/'test_anchor.ps1'),str(f),str(HERE/'anchor-validation.json'),
        *map(str,source['local_pelvis'])],check=True)
