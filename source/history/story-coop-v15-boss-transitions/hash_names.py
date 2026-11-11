import re
from find_anim import hash_name
from inspect_native import b
from investigate import HERE
targets={0x3f9129c8,0x4f1858a5,0x39368afd,0x26cfb6e6,0xb1fd2882}
words=set(re.findall(rb'[A-Za-z_][A-Za-z_0-9]{2,80}',b))
for p in HERE.glob('*.json'):words.update(re.findall(rb'[A-Za-z_][A-Za-z_0-9]{2,80}',p.read_bytes()))
print([(v.decode(),hex(hash_name(v.decode()))) for v in words if hash_name(v.decode()) in targets])
