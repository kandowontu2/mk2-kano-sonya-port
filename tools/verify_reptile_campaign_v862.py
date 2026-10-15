"""Prove the native Reptile table overrun repair, not full fatality art/port."""
import argparse
import hashlib
import json
import re
import struct
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OLD=ROOT/'audit_v858_sonya_p2_cache_failure'
NEW=ROOT/'audit_v861_sonya_p2_reptile_replay'
OLD_GUEST=ROOT/'audit_v790_kano_friendship_p1/guest_maincpu.bin'
CANDIDATE=ROOT/'diagnostic_v860_native_reptile_victims'
OLD_SHA='9F55AA553617BD761BD3F5DD6D9701439DD98BA69527544DBB4DD744DC14CA12'
NEW_SHA='C52742158221D0221397D0D1709BE47012F3024AE21738BA1C8A178ECCF648EB'
EXE_SHA='2A544841C8F89C8C12597B70CA3E86CEA3ACFE3008D5540D8648A323EC020CE8'
PAYLOAD_SHA='7896C93822473376AD724BB5E747EDE88C198203786F3F9B928CD1D860BAE019'
FAIL_FRAME=79346

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()

def at(address):
    return (address-0xff800000)//8

def rows(text):
    return [(m[1],dict(re.findall(r'(\w+)=([^\s]+)',m[2])))
            for m in re.finditer(r'^MK2_NAT_CAMPAIGN_(\w+) (.*)$',text,re.M)]

def verify(old_guest=None,new_guest=None,old_text=None,new_text=None,check_hashes=True):
    before=OLD_GUEST.read_bytes()if old_guest is None else old_guest
    after=(NEW/'guest_maincpu.bin').read_bytes()if new_guest is None else new_guest
    old_text=(OLD/'run.log').read_text(encoding='utf-8-sig')if old_text is None else old_text
    new_text=(NEW/'run.log').read_text(encoding='utf-8-sig')if new_text is None else new_text
    errors=[]
    def need(ok,label):
        if not ok:errors.append(label)
    need(len(before)==len(after)==0x100000,'Full native guest snapshots')
    if len(before)!=0x100000 or len(after)!=0x100000:return {'passed':False,'errors':errors}
    need(hashlib.sha256(before).hexdigest().upper()==OLD_SHA,'Exact failed-build guest')
    need(hashlib.sha256(after).hexdigest().upper()==NEW_SHA,'Exact repaired-build guest')
    result=json.loads((NEW/'result.json').read_text(encoding='utf-8-sig'))
    need(result['exit_code']==0 and result['human_slot']==2 and result['player']=='sonya'and
         result['strategy']=='defensive_leg'and result['assistance']=='none'and
         result['cheats_enabled']is False and result['seconds']==1800,
         'Same unassisted physical-slot replay, terminal completion')
    need(result['executable_sha256']==EXE_SHA and result['payload_sha256']==PAYLOAD_SHA,
         'Exact matched native candidate and unchanged art payload')
    pinned={str(OLD_GUEST):digest(OLD_GUEST),str(NEW/'guest_maincpu.bin'):digest(NEW/'guest_maincpu.bin')}
    if check_hashes:
        for name,sha in result['input_hashes'].items():
            need(digest(Path(name))==sha,'Frozen input changed: '+name)
            pinned[name]=sha
        need(digest(CANDIDATE/'mkport_candidate.exe')==EXE_SHA,'Exact repaired executable')
    original=at(0xff8c9900);operand=at(0xff8c8a70);storage=0xfa800
    expected=bytearray(before)
    need(before[storage:storage+19*8]==b'\xff'*(19*8),'Native allocation previously empty')
    need(struct.unpack_from('<I',before,operand)[0]==0xff8c9900,'Exact old fatality consumer')
    expected[storage:storage+17*8]=before[original:original+17*8]
    struct.pack_into('<4H',expected,storage+17*8,0xff3b,0,16,32)
    struct.pack_into('<4H',expected,storage+18*8,0xff3f,0xfffb,16,0)
    struct.pack_into('<I',expected,operand,0xff800000+storage*8)
    need(after==expected,'Only 19-row table and one pointer changed; native code/timing untouched')
    bad=struct.unpack_from('<4H',before,original+18*8)
    need(bad==(0xff84,0x0d5f,0x2710,0xff84),'Sonya previously read executable code as animation settings')
    old_rows=rows(old_text);new_rows=rows(new_text)
    need(any(tag=='CACHE_OVERWRITE'and row.get('frame')==str(FAIL_FRAME)for tag,row in old_rows)and
         any(tag=='REENTRY'for tag,row in old_rows),'Preserved actual original corruption and reset')
    need(not re.search(r'\[LUA ERROR\]|fatal error|access violation|exception at',new_text,re.I),
         'No native or observer runtime errors')
    need(not any(tag in('CACHE_OVERWRITE','REENTRY')for tag,row in new_rows),'No body overrun or machine reset')
    tags={'BOOT','MORPH_ROM','ROM','STATE','LOSS','SELECT','SELECT_ID','SELECT_EXIT','FIGHT',
          'STAGE','LIVE','DECISION','INPUT','SPECIAL','HEALTH','WIN','CPU_ID'}
    def prefix(text):
        lines=[]
        for line in text.splitlines():
            m=re.match(r'MK2_NAT_CAMPAIGN_(\w+) frame=(\d+) ',line)
            if m and m[1]in tags and int(m[2])<FAIL_FRAME:lines.append(line)
        return lines
    old_prefix=prefix(old_text);new_prefix=prefix(new_text)
    need(len(old_prefix)>30000 and old_prefix==new_prefix,'Identical actual campaign/input/state chronology before original fault')
    native_rows=[r for t,r in new_rows if t=='REPTILE_ROW'and r['frame']==str(FAIL_FRAME)]
    need(len(native_rows)==4 and [int(r['field'])for r in native_rows]==[0,1,2,3]and
         [int(r['data'],16)for r in native_rows]==[0xff3f,0xfffb,16,0]and
         all(r['row']=='18'and int(r['mask'],16)==0xffff and
             int(r['at'],16)==0xff800000+storage*8+18*64+int(r['field'])*16 for r in native_rows),
         'Actual native four-field read of independent true Sonya victim row')
    draws=[r for t,r in new_rows if t=='REPTILE_DRAW'and r['frame']==str(FAIL_FRAME)]
    need(len(draws)==1 and draws[0]['a9']=='FF024FF0'and
         draws[0]['words'].startswith('FF02FA00,FF02FA60,FF02FA00,FF02FAC0,00000000'),
         'Original animation interpreter receives real Sonya high-hit stream, not descriptor/code data')
    wraps=[r for t,r in new_rows if t=='REPTILE_WRAP']
    need(any(int(r['frame'])==FAIL_FRAME+90 and int(r['age'])==90 for r in wraps),'Original Reptile fatality reaches native completion at its actual age')
    next_fights=[r for t,r in new_rows if t=='FIGHT'and int(r['frame'])>FAIL_FRAME]
    need(any(r['human']=='18:18'and int(r['selection'])>30 for r in next_fights),
         'Actual paid continue/reselection returns real Sonya to combat after original fault')
    hp={1:0x010602f0,2:0x01060ec0}
    writers={1:{0xff836700,0xff825930,0xff9dece0,0xff9def40},
             2:{0xff836700,0xff825960,0xff9ded10,0xff9def70}}
    health=[r for t,r in new_rows if t=='HEALTH']
    for row in health:
        slot=int(row['slot']);pc=int(row['pc'],16)
        need(pc in writers[slot]and int(row['at'],16)==hp[slot],'Only exact original physical-slot health writers')
        if pc==0xff836700:
            need(0<=int(row['after'])<=int(row['before'])<=161,'Native collision damage never supplies health')
    terminal=[r for t,r in new_rows if t=='RESULT']
    need(len(terminal)==1 and int(terminal[0]['frame'])>FAIL_FRAME+15000,'Full replay extends well beyond fault')
    # Known separate fidelity gap: native main-61 heads still contain Liu's
    # single-frame descriptors. Do not promote this memory-safety repair to
    # full native fatality-art or whole-port acceptance.
    payload=(CANDIDATE/'roms/mk2ks/mk2ks.mdata').read_bytes()
    heads={}
    for name,base in(('kano',0x100000),('sonya',0x104000)):
        stream=struct.unpack_from('<I',payload,base+61*4)[0]
        first=struct.unpack_from('<I',payload,(stream-0xfe800000)//8)[0]
        heads[name]={'main61':f'{stream:08X}','firstDescriptor':f'{first:08X}',
                     'stillStockLiu':first==0xffb4a4b0}
    return {'passed':not errors,'errors':sorted(set(errors)),
            'native_table_overrun_repair_proven':not errors,
            'full_native_reptile_art_acceptance':False,'full_port_acceptance':False,
            'same_prefix_records':len(old_prefix),'observed_native_health_writes':len(health),
            'post_fault_own_fights':len(next_fights),'guest_changed_bytes':sum(a!=b for a,b in zip(before,after)),
            'remaining_head_art_gap':heads,'inputHashes':pinned}

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args()
    if args.output.exists():raise ValueError('Refusing to overwrite evidence')
    report=verify();args.output.mkdir()
    (args.output/'verification.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items()if k!='inputHashes'},indent=2))
    raise SystemExit(0 if report['passed']else 1)

if __name__=='__main__':main()
