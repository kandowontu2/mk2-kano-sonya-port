"""Finite linked table bounds/values, not arbitrary caller or runtime proof."""
import hashlib
import json
from pathlib import Path
import re
import struct

PORT=Path(__file__).resolve().parent
SRC=PORT.parent/'baseline/mk2-rebuild-main/srcp'
sha=lambda raw:hashlib.sha256(raw).hexdigest().upper()
symbols={n:int(a,16) for a,n in re.findall(r'\b([0-9a-fA-F]{8})\s+([A-Za-z_]\w*)',(SRC/'MK2P.MAP').read_text())}
rom=bytearray(1048576)
for lane in (0,1):
    rom[lane::2]=b''.join((SRC/f'rom/P12{part}.{lane}').read_bytes() for part in ('F8','FC'))

def local(listing,name):
    matches=re.findall(r'^\s+\d+\s+([0-9a-fA-F]{8})\s+'+re.escape(name)+r'\s*$',listing,re.M)
    assert len(matches)==1,(name,matches)
    return int(matches[0],16)

def table(module,anchor,name,count,code):
    listing=(SRC/(module+'.LST')).read_text()
    address=symbols[anchor]-local(listing,anchor)+local(listing,name)
    size=struct.calcsize('<'+code*count)
    assert address%8==0 and 0xff800000<=address and address+size*8<=0x100000000
    values=list(struct.unpack_from('<'+code*count,rom,(address-0xff800000)//8))
    return dict(address=hex(address),values=values)

getup=table('MKREACT','getup_local_reaction_exit','getup_speeds',19,'H')
sweep=table('MKREACT','getup_local_reaction_exit','sweepup_speeds',19,'H')
assert getup==sweep
assert getup['values']==[2 if i==7 else 4 for i in range(19)]
reaction=table('MKREACT','getup_local_reaction_exit','rs_calls',19,'I')
assert reaction['values'][17:]==[0,0]
throws=table('MKSLAM','do_body_slam','throw_ani_speeds',19,'H')
assert throws['values'][17:]==[4,4]
anti=table('MKDRONE','drone_getup','rh_air_distances',19,'H')
assert anti['values']==[0x40]*19
fatal=table('MKDRONE','drone_getup','ochar_fatality_distances',38,'H')
assert fatal['values'][34:]==[0x40,0xc0,0xc0,0xe0]
clapped=table('MKDEATH','disable_repell','clapped_lineups',38,'h')
assert clapped['values']==[-0x50,0]+[-0x60,0]*15+[-0x60,0,-0x60,8,-0x60,7]
death_listing=(SRC/'MKDEATH.LST').read_text()
assert local(death_listing,'do_tongue')-local(death_listing,'clapped_lineups')==19*32

report=dict(scope='Seven named linked table labels including shared getup alias',
    programSHA256=sha(rom),getup=getup,sweepup=sweep,reactionHooks=reaction,
    throwSpeeds=throws,antiAirDistances=anti,fatalityDistancePairs=fatal,clappedVictimLineups=clapped,
    ownIDSlotsVerified=True,allCallerDataflowVerified=False,
    runtimeGetupAndFatalityAIQualified=False,fullPortVerified=False,releaseReady=False)
paths=[Path(__file__),SRC/'MK2P.MAP']
for name in ('MKREACT','MKSLAM','MKDRONE','MKDEATH'):
    paths.extend((SRC/(name+'.ASM'),SRC/(name+'.LST')))
report['evidenceSHA256']={str(p):sha(p.read_bytes()) for p in paths}
(PORT/'COMMON_TABLE_LINK_QUALIFICATION.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items() if k!='evidenceSHA256'},indent=2))
