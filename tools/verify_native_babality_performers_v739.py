"""Bounded true-ID human Babality integration proof; not full finisher/port acceptance."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import struct
import numpy as np
from PIL import Image
import native_babality_runtime_checks_v739 as v

BASE=0xFF800000
WINNERS={'kano':17,'sonya':18,'kitana':4}
HISTORIES=((40,7,7,9,9,0,0,7,7,8,8,0,0),(40,9,7,7,0,0,0,8,7,7,0,0,0))

def offset(address): return (address-BASE)//8

def guest_check(old,new,original,donor):
    v.check(len(old)==len(new)==len(original)==len(donor)==0x100000,'complete original/actual guest required')
    expected=bytearray(old)
    v.check(set(old[0xf97a0:0xf98a0])=={255},'reserved space was not empty')
    struct.pack_into('<I',expected,offset(0xff87e250),BASE+0xf97a0*8)
    expected[0xf97a0:0xf97a0+68]=original[offset(0xff87e3a0):offset(0xff87e3a0)+68]
    for index,(record,destination,parser,fallback) in enumerate(((0xff986470,0xf97f0,0xf9840,BASE+0xf5440*8),
                                                               (0xff98aa80,0xf9810,0xf9860,0xff80de20))):
        source=offset(record)
        v.check(struct.unpack_from('<IIHII',donor,source)==(0x20000,0x200000,7,0xff993660,0xff97f390),
                'not original LK Babality record')
        history=struct.unpack_from('<13H',donor,source+18)
        v.check(history==HISTORIES[index],'original character command changed')
        native=tuple(value-1 if word and value else value for word,value in enumerate(history))
        struct.pack_into('<13H',expected,destination,*native)
        struct.pack_into('<I',expected,0xf97a0+(17+index)*4,BASE+destination*8)
        struct.pack_into('<6H',expected,parser,0x0d5f,0xe120,0xff87,0xc080,fallback&0xffff,fallback>>16)
        struct.pack_into('<I',expected,0xff2c0+(17+index)*4,BASE+parser*8)
    v.check(new==expected,'guest differs outside exact performer table/commands/bindings')
    return sum(a!=b for a,b in zip(old,new))

def provenance(result):
    v.check(result['exit_code']==0 and result['guest_writes']==0 and result['assistance']=='none',
            'failed or assisted runner')
    for path,value in result['input_hashes'].items():
        v.check(v.sha(Path(path))==value.upper(),'executed input changed: '+path)
    harness=next(Path(path) for path in result['input_hashes'] if path.endswith('performer_probe_v738.lua'))
    v.check(not re.search(r':write_|\bdofile\s*\(|\bloadfile\s*\(',harness.read_text()),'guest writes/delegating harness')

def command_check(rows,winner,side,command):
    result=v.entries(rows,'RESULT')[0]
    v.check(result['winner']==winner and result['case']==command,'wrong command case')
    window=int(result['window'])
    initial=next(r for r in v.entries(rows,'FIELD') if r['age']=='0' and int(r['slot'])==side)
    opponent=next(r for r in v.entries(rows,'FIELD') if r['age']=='0' and int(r['slot'])!=side)
    forward='Right' if int(initial['x'])<int(opponent['x']) else 'Left'
    if command=='wrong_direction': forward='Left' if forward=='Right' else 'Right'
    expected=([(20,forward),(32,forward),(44,'Down'),(56,'Down'),(58,'Low_Kick')] if winner=='kano' else
              [(20,'Down'),(32,'Down'),(44,forward),(46,'Low_Kick')] if winner=='sonya' else
              [(20,'Down'),(32,'Down'),(44,'Down'),(46,'Low_Kick')])
    actual=[(int(r['frame'])-window,r['button']) for r in v.entries(rows,'INPUT')
            if int(r['slot'])==side and int(r['frame'])>=window]
    v.check(all(item in actual for item in expected),'character-owned physical command missing')
    if command=='positive':
        v.check(int(result['action'])-window==(60 if winner=='kano' else 48), 'wrong native activation time')

def negative_check(rows,winner,victim,side,command):
    v.check(len(v.entries(rows,'BOOT'))==len(v.entries(rows,'RESULT'))==1,'reboot or incomplete run')
    result=v.entries(rows,'RESULT')[0]
    v.check(result['action']=='-1' and result['wins']=='2' and result['damage']=='322','negative not genuinely earned/rejected')
    for tag,row in rows:
        v.check(row['victim']==victim and int(row['winner_slot'])==side and row['writes']=='0' and
                row['assistance']=='none','mixed or assisted negative')
    selected=v.entries(rows,'SELECT_ID')
    v.check(len(selected)==2,'missing physical selection')
    for row in selected:
        wanted=WINNERS[winner] if int(row['slot'])==side else v.IDS[victim]
        v.check(int(row['actual'])==int(row['target'])==wanted,'negative proxy selection')
    damage=v.entries(rows,'DAMAGE')
    v.check(sum(int(r['before'])-int(r['after']) for r in damage)==322 and
            sum(r['after']=='0' for r in damage)==2 and all(r['pc']=='FF836700' for r in damage),
            'non-native negative knockouts')
    finish=v.entries(rows,'FINISH_WINDOW')
    v.check(len(finish)==1 and finish[0]['native_kos']=='2','missing native finish window')
    hp=[int(x) for x in finish[0]['hp_counters'].split(',')]
    lp=[int(x) for x in finish[0]['lp_counters'].split(',')]
    if command=='punch_used':
        v.check(hp[side-1]>0 and len(v.entries(rows,'PUNCH_ELIGIBILITY'))==2,'punch restriction not exercised')
    else:
        v.check(hp==lp==[0,0],'wrong-direction control was ineligible')
    calls=v.entries(rows,'ENTRY')
    v.check(any(r['entry']=='FF87E120' for r in calls),'negative bypassed native gate')
    v.check(not any(r['entry'] in ('FF87E520','FF87E8D0','FF87EB20') for r in calls) and
            not v.entries(rows,'CONSTRUCT') and not v.entries(rows,'LOOKUP'),'rejected command entered action')
    initial=[r for r in v.entries(rows,'FIELD') if r['age']=='0']
    v.check(len(initial)==2,'negative pre-command owners missing')
    for row in initial:
        v.check(row['owner']==row['actor'] and int(row['id'])==
                (WINNERS[winner] if int(row['slot'])==side else v.IDS[victim]),'negative owner/ID mismatch')
    v.check(any(r['mode']=='3' and int(r['frame'])>int(result['window']) for r in v.entries(rows,'STATE')),
            'negative native next-screen missing')
    command_check(rows,winner,side,command)

def original_reference(root):
    for name in ('audit_v734_original_babality_commands','audit_v735_original_babality_directions'):
        case=root/name
        result=json.loads((case/'result.json').read_text(encoding='utf-8-sig'))
        v.check(result['passed'] and result['exit_code']==0 and result['ram_writes']==0 and not result['cheats'],
                'bad original routing reference')
        for path,value in result['input_hashes'].items(): v.check(v.sha(Path(path))==value.upper(),'reference input changed')
        text=(case/'run.log').read_text(encoding='utf-8-sig')
        v.check('actors=010394B0:id0:slotflag1,010396C0:id1:slotflag2' in text,'original selection missing')
        for actor,record,history in (('010394B0:id0:slotflag1','FF986470',HISTORIES[0]),
                                     ('010396C0:id1:slotflag2','FF98AA80',HISTORIES[1])):
            target=f'actor={actor} record={record} masks=00020000,00200000 type=7 gate=FF993660 action=FF97F390 history='+','.join(map(str,history))
            v.check(target in text,'actual fighter LK record missing')
        if 'directions' in name:
            for side,first in ((1,5110),(2,5590)):
                for index,code in enumerate((6,7,8,9)):
                    v.check(re.search(rf'MK3_BABA_DIRECTION frame={first+index*120} slot={side} .*latest={code:04X}[0-9A-F]{{4}}',text),
                            'physical direction encoding not traced')

def verify(root):
    original_reference(root)
    prior_path=root/'audit_v733_native_babality_victims_checked_inputs/verification.json'
    v.check(v.sha(prior_path)=='156CBBB42710B4B4E82EA5CB516AB99C2953B0E187FA23F5B0411E9E5E3CD9B9',
            'frozen victim checkpoint changed')
    prior=json.loads(prior_path.read_text())
    def baseline_input(path):
        expected=prior['input_hashes'].get(str(path.resolve()))
        v.check(expected and v.sha(path)==expected,'frozen baseline input changed: '+str(path))
    reference_path=root/'audit_v726_original_baby_reference/reference.json'
    reference=json.loads(reference_path.read_text())
    for path,value in reference['input_hashes'].items(): v.check(v.sha(Path(path))==value.upper(),'baby oracle input changed')
    old_path=root/'audit_v732_native_baby_kano_p1/guest_maincpu.bin'
    baseline_input(old_path)
    old=old_path.read_bytes()
    original=(root/'mk2/mk2-maincpu.bin').read_bytes()
    donor=(root/'mk3/mk3-maincpu.bin').read_bytes()
    report={'candidate':'diagnostic_v737_native_babality_performers','cases':[],
            'fullPortAcceptance':False,'fullFinisherAcceptance':False,
            'scope':'human own Babalities both slots/facings, wrong direction and punch restriction, stock Babality rendering'}
    for winner,victim,label,side,command in (
        ('kano','sonya','kano_babality',1,'positive'),('kano','sonya','kano_babality',2,'positive'),
        ('sonya','kano','sonya_babality',1,'positive'),('sonya','kano','sonya_babality',2,'positive'),
        ('kano','sonya','kano_wrong',1,'wrong_direction'),('sonya','kano','sonya_wrong',1,'wrong_direction'),
        ('kano','sonya','kano_punch',2,'punch_used'),('sonya','kano','sonya_punch',2,'punch_used'),
        ('kitana','liu_kang','stock_liu',1,'positive'),('kitana','liu_kang','stock_liu',2,'positive')):
        prefix='audit_v740' if winner=='kitana' and side==2 else 'audit_v738'
        case=root/f'{prefix}_{label}_p{side}'
        result=json.loads((case/'result.json').read_text(encoding='utf-8-sig'))
        provenance(result)
        v.check(result['winner']==winner and result['victim']==victim and result['winner_side']==side and
                result['command_case']==command and result['candidate']==report['candidate'],'mixed runner metadata')
        text=(case/'run.log').read_text(encoding='utf-8-sig')
        v.check(not re.search(r'Lua error|fatal error|Error running',text,re.I),'runtime error')
        rows=v.records(text)
        delta=guest_check(old,(case/'guest_maincpu.bin').read_bytes(),original,donor)
        pixels=0
        if command=='positive':
            v.runtime_check(rows,victim,side,reference,winner_id=WINNERS[winner])
            command_check(rows,winner,side,command)
            if victim in v.FRAMES:
                needle=np.asarray(Image.open(reference_path.parent/f'{victim}_baby.png').convert('RGBA'))
                v.check(hashlib.sha256(needle.tobytes()).hexdigest()==reference['records'][victim]['rgba_sha256'],
                        'original baby pixels changed')
                for age in (160,200,240):
                    _,count=v.image_match(np.asarray(Image.open(case/f'snap/babality_{age}.png').convert('RGB')),needle)
                    pixels+=count
            else:
                before=root/f'audit_v732_native_baby_stock_liu_p{3-side}'
                for name in ('guest_maincpu.bin','run.log','result.json'):baseline_input(before/name)
                v.check((before/'guest_maincpu.bin').read_bytes()==old,'stock guest baseline mismatch')
                for age in range(0,721,8):
                    baseline_input(before/f'snap/babality_{age}.png')
                    a=np.asarray(Image.open(case/f'snap/babality_{age}.png').convert('RGB'))
                    b=np.asarray(Image.open(before/f'snap/babality_{age}.png').convert('RGB'))
                    v.check(np.array_equal(a,b),'stock rendered Babality changed')
                    pixels+=a.shape[0]*a.shape[1]
        else: negative_check(rows,winner,victim,side,command)
        report['cases'].append({'case':case.name,'guest_changed_bytes':delta,'checked_display_pixels':pixels,
                                'winner':winner,'winner_side':side,'command_case':command})
    report['boundedHumanBabalityAcceptance']=True
    return report

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('root',type=Path)
    parser.add_argument('--out',type=Path)
    args=parser.parse_args()
    report=verify(args.root)
    serialized=json.dumps(report,indent=2)
    if args.out:
        with args.out.open('x',encoding='utf-8') as handle: handle.write(serialized+'\n')
    print(serialized)
