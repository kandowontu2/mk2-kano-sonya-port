"""Verify native lookup operand and all added bloody-palette table entries."""
import json
import re
import struct
import zipfile
from pathlib import Path
from inventory_character_tables import source_tables
PORT=Path(__file__).resolve().parent
BUILD=PORT.parent/'baseline/mk2-rebuild-main/srcp'
symbols={n:int(a,16) for a,n in re.findall(r'\b([0-9a-fA-F]{8})\s+([A-Za-z_]\w*)',(BUILD/'MK2P.MAP').read_text())}
source=(BUILD/'MKGUYS.ASM').read_text()
table=source_tables(source)['bloody_palettes']
values=[v for r in table['rows'] for v in r['values']]
assert len(values)==38 and all(r['type']=='long' for r in table['rows'])
with zipfile.ZipFile('C:/Users/kando/Downloads/mk2-rebuild-main.zip') as z:
    original=z.read('mk2-rebuild-main/src/MKGUYS.ASM').decode('cp437')
old=[v for r in source_tables(original)['bloody_palettes']['rows'] for v in r['values']]
assert values[:30]==old and len(old)==30
lanes=[b''.join((BUILD/f'rom/P12{p}.{i}').read_bytes() for p in ('F8','FC')) for i in (0,1)]
program=bytearray(0x100000);program[::2]=lanes[0];program[1::2]=lanes[1]
def read(a,fmt):return struct.unpack_from('<'+fmt,program,(a-0xff800000)//8)
# Read the relocated ADDI immediate, not an inferred map location for a local.
entry=symbols['change_to_bloody_pal']
assert read(entry+0x30,'H')==(0x0b20,)
address=read(entry+0x40,'I')[0]
expected=['noob_p','noob_p','JADE_P','JADE_P',
          'ks_kano_primary_palette','ks_kano_alternate_palette',
          'ks_sonya_primary_palette','ks_sonya_alternate_palette']
assert values[30:]==expected
folded={name.lower():value for name,value in symbols.items()}
added=read(address+15*64,'8I')
assert added[:2]==read(address+13*64,'2I') # Original noob pair.
assert added[2]==added[3] and 0xff800000<=added[2]<0x100000000
assert read(added[2],'H')[0] in (64,65)
assert added[4:]==tuple(folded[n.lower()] for n in expected[4:])
result=dict(nativeRows=19,original15RowsPreserved=True,ownPalettePointersVerified=4,
            noobPointersMatchOriginal=True,jadePairValidPaletteHeader=True,
            nativeLookupOperandVerified=True,visualAcceptance=False,fullPortVerified=False)
(PORT/'BLOODY_PALETTE_QUALIFICATION.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result))
