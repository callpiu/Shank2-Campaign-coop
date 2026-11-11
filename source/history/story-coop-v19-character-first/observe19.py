import importlib.util
import json
import sys
from flow19 import HERE,BASE,DATA

spec=importlib.util.spec_from_file_location('prelevel18_observer',BASE/'observe.py')
previous=importlib.util.module_from_spec(spec);spec.loader.exec_module(previous)
p=previous.memory.Process(int(sys.argv[1]))
try:
    row=previous.sample(p)
    if row:
        row['role_confirmed']=p.u32(DATA+0x3c)
        row['current_step']='equipment' if row['role_confirmed'] else 'character'
    print(json.dumps(row,indent=2))
    (HERE/f'latest-{sys.argv[1]}.json').write_text(json.dumps(row,indent=2)+'\n',encoding='utf-8')
finally:p.close()
