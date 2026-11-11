exec(open(r'G:\shank2\work\story-coop-v02\native_types.py').read().split('for name in sys.argv[1:]')[0])
import json
out={}
for name in ['Group','Instance','Image','Label','ProgressBar','Button','Anim','Spinner','NumericSpinner','CheckBox','ListBox','Grid','ScrollList','MoviePlayer']:
 o=b.find(('.?AV'+name+'Definition@UI@@').encode());td=va(o-8)
 for m in re.finditer(re.escape(struct.pack('<I',td)),b):
  col=m.start()-12
  if col<0 or u(col)!=0 or u(col+4)>100:continue
  for n in re.finditer(re.escape(struct.pack('<I',va(col))),b):
   vt=n.start()+4;f=u(vt+4);fo=p.get_offset_from_rva(f-base)
   code=b[fo:fo+6]
   if code[0]!=0xb8:continue
   typeid=struct.unpack_from('<I',code,1)[0]
   out[typeid]={'name':name,'read':hex(u(vt+8)),'write':hex(u(vt+12))}
Path(r'G:\shank2\work\story-coop-v03\ui-types.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
