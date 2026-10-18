"""Record remaining throw-helper bounds without claiming runtime coverage."""
import hashlib
import json
import re
from pathlib import Path
from inventory_character_tables import source_tables

PORT=Path(__file__).resolve().parent
SRC=PORT.parent/'baseline/mk2-rebuild-main/srcp'
requirements={'MKSLAM.ASM':{'body_slam_jumps':32,'back_break_adjusts':32,'throw_ani_speeds':16,'ochar_nonflip_adjx':16},
              'MKREACT.ASM':{'post_fb_xfers':32,'flip_damage_table':16}}
report={};hashes={}
for filename,names in requirements.items():
    payload=(SRC/filename).read_bytes();hashes[filename]=hashlib.sha256(payload).hexdigest().upper()
    tables=source_tables(payload.decode())
    for name,stride in names.items():
        bits=sum({'word':16,'long':32,'byte':8}[row['type']]*len(row['values']) for row in tables[name]['rows'])
        assert bits%stride==0
        report[name]={'source':filename,'entries':bits//stride,'strideBits':stride,'coversIDs17And18':bits//stride>=19}
coverage=json.loads((PORT/'generated_roster_roots/ROOT_COVERAGE.json').read_text())
assert hashlib.sha256((PORT/'generated_roster_roots/KSROOT.ASM').read_bytes()).hexdigest().upper()==coverage['sourceSHA256']
roots=coverage['fighters']
entry=(SRC/'MKSLAM.ASM').read_text().split('\ndo_body_slam\n',1)[1].split('\tcalla\tinit_special',1)[0]
assert all(token in entry for token in ('cmpi 17,a0','cmpi 18,a0','jauc ks_kano_throw','jauc ks_sonya_throw'))
move_text=(SRC/'MOVES.ASM').read_text()
block_table=source_tables(move_text)['char_block']
block_rows=[value.strip() for row in block_table['rows'] for value in row['values']]
assert len(block_rows)==19 and block_rows[10]=='sc_block'
assert block_rows[17:19]==['sucide','ks_sonya_block']
air_callers=[]
for path in sorted(SRC.glob('*.ASM')):
    for line,raw in enumerate(path.read_text().splitlines(),1):
        code=raw.split(';',1)[0].strip()
        if re.match(r'(?:movi|calla|callr|jauc|jsrp)\s+do_air_body_slam\b',code):
            air_callers.append(dict(file=path.name,line=line,code=code))
assert len(air_callers)==1 and air_callers[0]['file']=='MOVES.ASM'
scorpion=move_text.split('\nsc_block\n',1)[1].split('\njx_hi_kick\n',1)[0]
assert 'movi\tdo_air_body_slam,a7' in scorpion
own=(PORT/'asm/KSTHROW.ASM').read_text()
assert 'movi 34,a10' in own and 'jauc land_on_my_back' in own
assert not re.search(r'\b(tossed_flight|post_fb_xfers|flip_damage_table|do_air_body_slam)\b',own)
result={'sourceSHA256':hashes,'tables':report,
        'ownGroundThrowBypassesIncompatibleNativeDispatch':True,
        'bypassScope':'Dedicated do_body_slam guard only; not a general bounds-safety proof',
        'backBreakMain3fMissing':{actor:63 in data['missingMainEntries'] for actor,data in roots.items()},
        'directAirThrowCallers':air_callers,
        'directAirThrowCallerIsScorpionBlockHandler':True,
        'ownBlockHandlersDoNotSelectScorpionBlock':True,
        'ownThrowReleaseUsesExplicit34Damage':True,
        'ordinaryAirThrowDirectSourceCallerAuditComplete':True,
        'arbitraryIndirectOrMorphCallerAuditComplete':False,'fullPortVerified':False}
(PORT/'THROW_HELPER_AUDIT.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
