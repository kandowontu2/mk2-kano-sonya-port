"""Current ROM descriptors/table alignment and exact native-render name pixels."""
import csv
import json
from pathlib import Path
import re
import struct
import sys
import zipfile
from PIL import Image
from qualify_bubble import BASE,HERE,SRC,sha
from inventory_character_tables import source_tables

run=BASE/sys.argv[1]
capture=run/'snap'/sys.argv[2]
left,right=sys.argv[3:5]
execution=json.loads((run/'execution.json').read_text())
assert execution['exitCode']==0 and not execution['timedOut']
assert not execution['customDriver'] and not execution['gameMemoryWrites']
assert execution['controllerSHA256']==sha(run/'autoboot.lua')
assert execution['emulatorSHA256']=='AF6966108D9B52C22465C6D50F4E5D50CC371B50F2D27DC443935F287AAD37A3'
assert '[LUA ERROR]' not in (run/'mame.log').read_text()
data=json.loads((HERE/'generated_names/NAMES_DATA.json').read_text())
with zipfile.ZipFile(run/'roms/mk3.zip') as z:
    lanes=[z.read(f'mk321u{chip}.bin') for chip in [54,63]]
    for lane,raw in enumerate(lanes):
        assert raw==b''.join((SRC/f'rom/P12{part}.{lane}').read_bytes() for part in ['F8','FC'])
    for chip in range(114,122):
        name=f'l1_mortal_kombat_3_u{chip}_game_rom.u{chip}'
        assert z.read(name)==(HERE/'generated_names'/name).read_bytes()
rom=bytearray(1048576);rom[::2]=lanes[0];rom[1::2]=lanes[1]
symbols={n:int(a,16) for a,n in re.findall(r'\b([0-9a-fA-F]{8})\s+([A-Za-z_]\w*)',(SRC/'MK2P.MAP').read_text())}
def read(address):return struct.unpack_from('<I',rom,(address-0xff800000)//8)[0]
tables=source_tables((SRC/'MKDISP.ASM').read_text())
for side in [1,2]:
    values=[v for row in tables[f'p{side}_powerbar_names']['rows'] for v in row['values']]
    assert len(values)==38
    pattern=bytearray()
    for actor,name in [(17,'KANO'),(18,'SONYA')]:
        width=data['names'][name]['width']
        assert values[actor*2]=='ks_bar_'+name.lower()
        pattern.extend(struct.pack('<II',symbols['ks_bar_'+name.lower()],(30<<16)|(29 if side==1 else 367-width)))
    # Local labels are not exported in MAP; locate the exact pair in linked ROM.
    assert rom.count(pattern)==1
image=Image.open(capture).convert('RGB');assert image.size==(400,254)
packed=(HERE/'generated_names/fighter_ui_finish_names_graphics.bin').read_bytes()
palette_at=(symbols['SCORE_P']-0xff800000)//8
colors=struct.unpack_from('<64H',rom,palette_at+2)
def rgb(c):return tuple(((c>>s)&31)*8+((c>>s)&31)//4 for s in (10,5,0))
counts={}
for side,name in [(1,left),(2,right)]:
    item=data['names'][name];width=item['width'];offset=item['packedByteOffset']
    descriptor=symbols['ks_bar_'+name.lower()]
    at=(descriptor-0xff800000)//8
    assert struct.unpack_from('<4HIH',rom,at)==(width,10,0,0,(0xc00000+offset)*8,0x4000)
    x=29 if side==1 else 367-width
    count=shadow=0
    for i in range(width*10):
        index=(packed[offset+i//2]>>(4*(i%2)))&15
        if not index:continue
        assert image.getpixel((x+i%width,30+i//width))==rgb(colors[index]),(side,name,i,index)
        count+=1;shadow+=index==2
    assert count>100 and shadow>20
    counts[f'P{side}_{name}']=dict(nonTransparentPixels=count,exactNativeShadowPixels=shadow)
report=dict(scope='finite exact rendered native name pixels and all four linked name table entries',
            exactNativePaletteAndShadowPixels=True,shadowRGB=rgb(colors[2]),names=counts,
            fullPortVerified=False,releaseReady=False)
paths=[run/'execution.json',run/'autoboot.lua',capture,SRC/'MK2P.OUT',SRC/'MK2P.MAP',SRC/'MKDISP.ASM',
       SRC/'KSNAMES.ASM',HERE/'generate_hud_names.py',HERE/'generated_names/NAMES_DATA.json',Path(__file__)]
report['pins']={str(p):sha(p) for p in paths}
(run/'hud_qualification.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items() if k!='pins'},indent=2))
