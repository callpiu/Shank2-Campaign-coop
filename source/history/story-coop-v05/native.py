"""Bounded read-only views of the original Steam executable."""
from pathlib import Path
import sys,struct,re,json,hashlib
sys.path.insert(0,r'G:\DeepSeekData\Workspaces\Codex\2026-10-28\shank2-mod-e-steamlibrary-steamapps-common\work\pydeps')
import pefile
from capstone import Cs,CS_ARCH_X86,CS_MODE_32
GAME=Path(r'E:\SteamLibrary\steamapps\common\Shank 2')
original=GAME/'bin/shank2.exe'
b=original.read_bytes()
# Steam integration intentionally installs the clean MOD at Steam's default
# executable name. Reverse-engineering/build tools must still read stock
# instructions from the verified original backup, never treat MOD hooks as
# an unmodified Steam baseline.
receipt=GAME/'.storycoop-steam/state.json'
if receipt.exists():
 state=json.loads(receipt.read_text(encoding='utf8'))
 if state.get('Enabled') and hashlib.sha256(b).hexdigest()==state.get('ActiveModSHA256'):
  original=GAME/'.storycoop-steam/shank2.original.exe'
  b=original.read_bytes()
  assert hashlib.sha256(b).hexdigest()==state['OriginalSHA256']=='3cd7aeb0d9f135dc82c4bba491463ecb85fec9aa33b9189ab2cee5160dd045d3'
pe=pefile.PE(data=b)
off=lambda va:pe.get_offset_from_rva(va-0x400000)
def dis(va,size):
 return '\n'.join(f'{i.address:08x} {i.bytes.hex():20} {i.mnemonic} {i.op_str}' for i in Cs(CS_ARCH_X86,CS_MODE_32).disasm(b[off(va):off(va)+size],va))
if __name__=='__main__':
 for arg in sys.argv[1:]:
  parts=arg.split(':');v=int(parts[0],16);n=int(parts[1]) if len(parts)>1 else 200;print(dis(v,n))
