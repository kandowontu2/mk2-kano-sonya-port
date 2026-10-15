"""Bounded native Friendship ownership/history/choreography verification.

Audio candidate choreography check; actual audible mix is checked separately.
Stock controls, broader input/CPU/arena checks and whole-port regression remain.
"""
import argparse
import hashlib
import json
from pathlib import Path
import re
import struct
import numpy as np
from PIL import Image
import build_native_friendship_art_v759 as art
from native_babality_runtime_checks_v739 import image_match

BASE=0xff800000
def off(address):return(address-BASE)//8
def check(value,message):
    if not value:raise ValueError(message)
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest().upper()
def parse(path):
    rows=[]
    for line in path.read_text(encoding='utf-8-sig').splitlines():
        match=re.match(r'MK2_FRIEND_(\w+) (.*)',line)
        if match:rows.append((match[1],dict(re.findall(r'(\w+)=([^\s]+)',match[2]))))
    return rows
def select(rows,tag):return[r for kind,r in rows if kind==tag]

def guest_check(old,new):
    check(len(old)==len(new)==0x100000,'Complete actual guest required')
    sites={off(0xff8808a0):BASE+0xf98a0*8,off(0xff880930):BASE+0xf99c0*8,
           off(0xff880d40):BASE+0xf98f0*8,0xff270+17*4:BASE+0xf9980*8,
           0xff220+18*4:BASE+0xf99a0*8}
    expected=bytearray(old)
    check(all(x==255 for x in old[0xf98a0:0xfa700]),'Original reserved scene storage occupied')
    expected[0xf98a0:0xfa700]=new[0xf98a0:0xfa700]
    for at,value in sites.items():struct.pack_into('<I',expected,at,value)
    check(new==expected,'Guest changed outside exact Friendship storage and five bindings')
    check(new[0xf98a0:0xf98a0+17*4]==old[off(0xff880a70):off(0xff880a70)+17*4],'Stock command rows changed')
    check(new[0xf98f0:0xf98f0+17*4]==old[off(0xff880d90):off(0xff880d90)+17*4],'Stock action rows changed')
    histories=((40,3,2,2,4,0,0,3,2,2,4,0,0),(42,6,7,8,7,0,0,6,8,7,8,0,0))
    for index,history in enumerate(histories):
        record=0xf9940+index*0x20;wrapper=0xf9980+index*0x20
        check(struct.unpack_from('<13H',new,record)==history,'Character-owned translated command changed')
        check(struct.unpack_from('<I',new,0xf98a0+(17+index)*4)[0]==BASE+record*8,'Wrong command ID row')
        check(struct.unpack_from('<I',new,0xf98f0+(17+index)*4)[0]==BASE+(0xf9a00+index*0x200)*8,'Wrong action ID row')
        fallback=BASE+(0xf5500 if index==0 else 0xf0000)*8
        check(struct.unpack_from('<6H',new,wrapper)==(0x0d5f,0x0770,0xff88,0xc080,fallback&65535,fallback>>16),'Native gate/fallback wrapper changed')
    check(struct.unpack_from('<11H',new,0xf99c0)==(0xb504,0x01f0,0x0b44,0xffee,0xca03,0xc080,0x75d0,0xff87,0xc080,0x7580,0xff87),'True-ID matcher routing changed')
    return sum(a!=b for a,b in zip(old,new))

def runtime(rows,winner,side,case):
    fid=17 if winner=='kano'else 18
    boot=select(rows,'BOOT');final=select(rows,'RESULT');windows=select(rows,'WINDOW')
    check(len(boot)==len(final)==len(windows)==1,'Nonterminal native attempt')
    check(all(r['writes']=='0' and r['assistance']=='none'for _,r in rows),'Not physical-input-only gameplay')
    check(int(boot[0]['own_id'])==fid and int(boot[0]['victim_id'])==35-fid,'Wrong character ownership')
    selections=select(rows,'SELECT_ID')
    check(len(selections)==2 and all(r['actual']==r['target']for r in selections),'Native selection did not construct actual IDs')
    damage=select(rows,'DAMAGE')
    check(int(final[0]['kos'])==2 and sum(int(r['before'])-int(r['after'])for r in damage)==322 and
          all(r['pc']=='FF836700'for r in damage)and sum(r['after']=='0'for r in damage)==2,'Not two genuine native round wins')
    counter_fields=('hp_counters','lp_counters')
    counters=[int(value)for key in counter_fields for value in windows[0][key].split(',')]
    if case=='punch_used':check(counters[side-1]>0,'Actual winning-round HP restriction not exercised')
    else:check(not any(counters),'Command test was ineligible due to punches')
    entries=select(rows,'ENTRY');poses=select(rows,'POSE')
    if case!='positive':
        check(int(final[0]['action'])==-1 and final[0]['cleanup']=='false' and not poses and not select(rows,'PART'),'Ineligible/wrong command activated scene')
    else:
        check(int(final[0]['action'])>int(final[0]['window']) and final[0]['cleanup']=='true' and final[0]['retired']=='true','Native action/cleanup/transition incomplete')
        check(all(int(r['id'])==fid and r['owner']==r['actor'] and int(r['roster'])==fid for r in poses),'Body ownership or actual fighter ID changed')
        expected_groups=art.KANO_BODY if winner=='kano'else art.SONYA_BODY[:7]
        scene=[r for r in poses if int(r['pose'],16)+0x1000000 in expected_groups]
        check(len(scene)>=len(expected_groups),'Intro poses missing')
        check([int(r['pose'],16)+0x1000000 for r in scene[:len(expected_groups)]]==list(expected_groups),'Original body order changed')
        check([int(r['age'])for r in scene[:len(expected_groups)]]==list(range(48,48+5*len(expected_groups),5)),'Original five-field body timing changed')
        check(len({(r['x'],r['y'],r['floor'])for r in poses})==1 and all(r['y']==r['floor']for r in poses),'Scene moved the fighter off its native ground anchor')
        common=[r for r in entries if r['entry']=='FF880CC0']
        check(len(common)==1 and int(common[0]['frame'])-int(final[0]['action'])==(193 if winner=='kano'else 176),'Native Friendship finish handoff changed')
        if winner=='sonya':
            tail=[r for r in poses if int(r['age'])>=83]
            cycle=(7,8,9,10,9,8,7,6,5,4,3,4,5,6)
            check(all(int(r['pose'],16)+0x1000000==art.SONYA_BODY[cycle[i%14]] and int(r['age'])==83+i*3 for i,r in enumerate(tail)),'Chicken loop order/three-field cadence changed')
        else:
            parts=select(rows,'PART')
            check([int(r['pose'],16)+0x1000000 for r in parts]==list(art.KANO_BUBBLE),'Bubble frames missing or reordered')
            check([int(r['age'])for r in parts]==[138,143,148,153,158,183,188],'Bubble choreography timing changed')
            expected_words=struct.unpack_from('<16H',bytes.fromhex('10001f00dd7f9b7f597f177fb57e737e327ef17db07d707d2f7def7caf7c907c517c'),2)
            # The first construction log is before MKII's deferred palette copy.
            check(all([int(x,16)for x in r['colors'].split(',')]==list(expected_words)for r in parts[1:]),'Bubble palette was not independently loaded')
            check(len({r['actor']for r in parts})==1 and all(r['actor']!=poses[0]['actor']and(r['x'],r['y'])==(poses[0]['x'],poses[0]['y'])for r in parts),'Bubble did not remain a separate attached object')
    fields=select(rows,'FIELD')
    check(fields and fields[-1]['mode']=='3' and fields[-1]['finish']!='3','Finish window did not cleanly leave for next screen')
    return {'native_kos':2,'damage':322,'action':int(final[0]['action']),'cleanup':final[0]['cleanup'],'scope':'human dispatch/owned choreography, not full finisher acceptance'}

def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('root',type=Path);parser.add_argument('output',type=Path);args=parser.parse_args()
    check(not args.output.exists(),'Do not overwrite verification')
    tracked={};reports={};root=args.root
    def track(path,wanted=None):
        actual=sha(path);check(wanted is None or actual==wanted,'Executed input changed: '+str(path));tracked[str(path.resolve())]=actual
    old=root/'audit_v738_kano_babality_p1/guest_maincpu.bin';track(old);baseline=old.read_bytes()
    track(Path(__file__));track(Path(art.__file__))
    import native_babality_runtime_checks_v739 as shared
    track(Path(shared.__file__))
    oracle_path=root/'audit_v756_original_friendship_art_checked/verification.json'
    track(oracle_path);oracle=json.loads(oracle_path.read_text())
    for path,value in oracle['checked_inputs'].items():track(Path(path),value)
    import_path=root/'audit_v759_native_friendship_art_only/import.json'
    track(import_path);imported=json.loads(import_path.read_text())
    for path,value in imported['input_hashes'].items():track(Path(path),value)
    original_path=root/'mk3/mk3-maincpu.bin'
    donor_path=root/'diagnostic_v737_native_babality_performers/roms/mk2ks/mk2ks.mdata'
    donor=bytearray(donor_path.read_bytes());rebuilt=art.build(donor,original_path.read_bytes())
    check(rebuilt['after_sha256']==imported['after_sha256'] and rebuilt['changed_bytes']==161,
          'Artwork import is not reproducible from the verified previous payload')
    payload_path=root/'diagnostic_v777_native_friendship_audio/roms/mk2ks/mk2ks.mdata'
    track(payload_path,imported['after_sha256']);check(payload_path.read_bytes()==donor,'Candidate did not use the exact artwork import')
    reference=json.loads((root/'audit_v755_original_friendship_art/reference.json').read_text())
    for winner in('kano','sonya'):
        specs=[(1,'positive',f'{winner}_friendship_p1'),(2,'positive',f'{winner}_friendship_p2'),
               (1,'wrong_command',f'{winner}_wrong_p1'),(2,'punch_used',f'{winner}_punch_p2')]
        for side,case,suffix in specs:
            folder=root/f'audit_v777_{suffix}';result=json.loads((folder/'result.json').read_text(encoding='utf-8-sig'))
            check(result['exit_code']==0 and result['guest_writes']==0 and result['winner']==winner and result['side']==side and result['command_case']==case,'Wrong or unfinished executed case')
            for path,value in result['input_hashes'].items():track(Path(path),value)
            for name in('result.json','run.log','guest_maincpu.bin'):track(folder/name)
            data=parse(folder/'run.log');report=runtime(data,winner,side,case)
            report['guest_changed_bytes']=guest_check(baseline,(folder/'guest_maincpu.bin').read_bytes())
            if winner=='kano'and case=='positive':
                report['bubble_pixel_checks']=[]
                for part in select(data,'PART'):
                    group=int(part['pose'],16)+0x1000000
                    asset=next(g for g in reference['records']['kano']['groups']if g['group']==group)
                    sprite_path=root/'audit_v755_original_friendship_art'/asset['file'];track(sprite_path)
                    sprite=np.asarray(Image.open(sprite_path).convert('RGBA'));match=None
                    for age in range(int(part['age'])+1,int(part['age'])+5):
                        photo=folder/'snap'/f'native_field_{age}.png';actual=np.asarray(Image.open(photo).convert('RGB'))
                        for flip in(False,True):
                            try:origin,pixels=image_match(actual,sprite[:,::-1]if flip else sprite)
                            except ValueError:continue
                            match={'group':group,'age':age,'flip':flip,'origin':origin,'pixels':pixels};track(photo);break
                        if match:break
                    check(match is not None,'Native bubble image not pixel-exact: '+hex(group));report['bubble_pixel_checks'].append(match)
            reports[folder.name]=report
    args.output.mkdir(parents=True)
    report={'scope':__doc__,'cases':reports,'checked_inputs':tracked,'boundedHumanFriendshipDispatchAcceptance':True,
            'fullPortAcceptance':False,'fullFinisherAcceptance':False}
    (args.output/'verification.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({'cases':len(reports),'checked_inputs':len(tracked),'fullFinisherAcceptance':False},indent=2))

if __name__=='__main__':main()
