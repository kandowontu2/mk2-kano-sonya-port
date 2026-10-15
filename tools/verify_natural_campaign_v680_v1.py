"""Independent bounded native campaign proof; incomplete towers never pass clear."""
import argparse
import hashlib
import json
import re
import struct
from pathlib import Path
from verify_p2_campaign import expected_orders

ROOT = Path(__file__).resolve().parents[1]
HEX = {'schedule','actor','human_actor','human_main','cpu_actor','cpu_main','entry','pc','at','a0','a9','a8','a13','mask'}


def parse(text):
    records=[]
    for match in re.finditer(r'^MK2_NAT_CAMPAIGN_(\w+) (.*)$',text,re.M):
        row=dict(re.findall(r'(\w+)=([^\s]+)',match[2]))
        row.update(tag=match[1], event=match.start())
        for key,value in tuple(row.items()):
            if key in HEX: row[key]=int(value,16)
            elif re.fullmatch(r'-?\d+',str(value)): row[key]=int(value)
        records.append(row)
    return records


def digest(path):
    h=hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda: stream.read(1024*1024),b''): h.update(block)
    return h.hexdigest().upper()


def verify(folder, check_hashes=True):
    result=json.loads((folder/'result.json').read_text(encoding='utf-8-sig'))
    text=(folder/'run.log').read_text(encoding='utf-8-sig')
    errors=[]
    need=lambda ok,label: errors.append(label) if not ok else None
    side=result['human_slot'];identity={'kano':17,'sonya':18}[result['player']]
    need(side in (1,2) and result['cpu_slot']==3-side, 'Actual physical slots')
    need(result['exit_code']==0 and result['assistance']=='none', 'Terminal unassisted capture')
    need(result['candidate']=='diagnostic_v680_native_pit_initial_cache','Current candidate')
    if check_hashes:
        for name,sha in result['input_hashes'].items():
            need(digest(Path(name))==sha,'Frozen input changed: '+name)
    harness=folder/'input_sources/mk2ks_natural_campaign_probe_v30.lua'
    need(harness.is_file(),'Frozen current observer v30')
    if harness.is_file():
        source=harness.read_text()
        need(not re.search(r':write_|\bload\s*\(|\bdofile\s*\(|\beval\b',source),'No guest writes/dynamic delegated code')
        need('roster)<=18 then' in source,'Wait for valid native continue selection ID')
    need(not re.search(r'\[LUA ERROR\]|fatal error|access violation|exception at',text,re.I),'No observer or native runtime errors')
    rows=parse(text)
    need(all(r.get('writes')==0 and r.get('assistance')=='none' and r.get('human_slot')==side and
             r.get('fighter')==result['player'] for r in rows),'Every native record scope')
    boots=[r for r in rows if r['tag']=='BOOT']
    need(len(boots)==1 and boots[0]['schema']==30,'Exactly one current cold driver')
    orders=expected_orders();schedules={}
    for row in [r for r in rows if r['tag']=='ROM']:
        n=row['order'];ids=tuple(map(int,row['ids'].split(',')))
        need(n in range(6) and n not in schedules,'Unique original schedule')
        if n in range(6):need(ids==orders[n] and row['list']==f'{0xfffa3000+n*0x180:08X}' and row['table']=='FFFA2C00','Original-derived true-ID schedule')
        schedules[n]=ids
    need(set(schedules)==set(range(6)),'All six actual schedules')
    stages=[r for r in rows if r['tag']=='STAGE']
    wins=[r for r in rows if r['tag']=='WIN']
    losses=[r for r in rows if r['tag']=='LOSS']
    live=[r for r in rows if r['tag']=='LIVE']
    states=[r for r in rows if r['tag']=='STATE']
    need(bool(stages) and stages[0]['stage']==0,'Cold natural campaign begins at zero')
    schedule=stages[0]['schedule'] if stages else -1
    order=next((n for n in range(6) if schedule==0xfffa3000+n*0x180),None)
    need(order is not None,'Selected native schedule pointer')
    need(all(r['schedule']==schedule for r in stages+live),'Schedule unchanged throughout campaign')
    original=(ROOT/'mk2/mk2-maincpu.bin').read_bytes()
    for address,words in ((0xff86e650,(0xb128,0x1f0)),(0xffa166e0,(0xb008,0x1f0))):
        need(struct.unpack_from('<2H',original,(address-0xff800000)//8)==words,'Original Shang store signature')
    id_writes=[r for r in rows if r['tag']=='CPU_ID']
    for row in id_writes:
        pc=row['pc'];new=row['after']
        need(row['mask']==0xffff and row['a8']==row['actor'] and
             ((pc==0xff86e670 and new in range(12) and new==row['a9']&0xffff) or
              (pc==0xffa16700 and new==6 and new==row['a0']&0xffff)), 'Original CPU morph/restore provenance')
    for row in live:
        stage=row['stage'];human=tuple(map(int,row['human'].split(':')));cpu=tuple(map(int,row['cpu'].split(':')))
        need(human==(identity,identity),'True live human ID/Main, no proxy')
        need(all(0x01000000<=row[k]<0x01100000 for k in ('human_actor','human_main','cpu_actor','cpu_main')),'Actual live actor/Main pointers')
        need(order is not None and stage in range(17),'Valid live native stage')
        if order is None or stage not in range(17):continue
        expected=orders[order][stage]
        owned=cpu==(expected,expected)
        if not owned and expected==6 and stage==14 and cpu[0]==6:
            previous=[r for r in id_writes if r['event']<row['event'] and r['actor']==row['cpu_actor']]
            owned=bool(previous and previous[-1]['after']==cpu[1] and previous[-1]['a13']==row['cpu_main'])
        need(owned,'Scheduled CPU true ID or original proven morph')
    for row in wins:
        slot=row['slot'];id_=row['id'];hp=tuple(map(int,row['health'].split(',')))
        need(row['entry']==0xfffef800+id_*32 and row['pc']==0xff8296b0,'Actual native winner-table call')
        need(slot in (1,2) and hp[slot-1]>hp[2-slot],'Native winning health, not fabricated KO')
        need(slot!=side or id_==identity,'Own actual winning fighter')
        following=[r for r in states if r['frame']==row['frame']+1]
        need(bool(following) and following[0]['mode'] in (5,11) and following[0]['winner']==slot and following[0]['health']==row['health'],'Matching next-field native winner scene')
    for before,after in zip(stages,stages[1:]):
        jump=after['stage']-before['stage']
        need(jump==1 or(jump==2 and before['stage']==12 and after['stage']==14 and orders[order][13]==14),'Only original endurance sentinel may be skipped')
        last_loss=max([r['event'] for r in losses if r['event']<after['event'] and r['stage']==before['stage']]+[before['event']])
        earned=[r for r in wins if last_loss<r['event']<after['event'] and r['stage']==before['stage'] and r['slot']==side]
        need(len(earned)>=2,'Advance after two wins in actual successful attempt, not accumulated failed matches')
    negative=[r for r in rows if r['tag']=='HEALTH' and r['after']<r['before']]
    damage=[r for r in negative if r['pc']==0xff836700]
    need(bool(damage),'Actual original combat damage stores')
    # Other original stores include round/health-bar teardown; do not mistake
    # their real native writes for combat damage or count them as earned hits.
    need(all(0xff800000<=r['pc']<=0xffffffff for r in negative),'No non-native health mutation writer')
    own_wins=[r for r in wins if r['slot']==side]
    starts=[r for r in rows if r['tag']=='ENDING_START']
    completed=[r for r in rows if r['tag']=='ENDING_COMPLETED']
    mandatory=list(range(13))+[14,15,16]
    reached=[r['stage'] for r in stages]
    clear=(not errors and reached==mandatory and any(r['stage']==16 for r in own_wins) and len(starts)==len(completed)==1)
    if clear:
        start,end=starts[0],completed[0]
        need(start['winner']==side and start['roster']==identity and start['actors']=='00000000,00000000','Owned boss ending retirement')
        need(end['frame']-start['frame']==end['age'] and end['age']>1200 and end['mode']==11,'Actual ending completion chronology')
        need(min(map(int,end['pictures'].split(',')))>0 and min(map(int,end['texts'].split(',')))>0,'Both own native picture/story pages')
        need(tuple(map(int,end['roster'].split(',')))[side-1]!=identity,'Original return to attract roster')
    finals=[r for r in rows if r['tag']=='RESULT']
    need(len(finals)==1 and finals[0]['schema']==30 and finals[0]['native_win_reads']==len(wins) and
         finals[0]['seen_stages']==len(stages),'Terminal native accounting')
    return dict(passed=not errors,bounded_campaign_evidence_proven=not errors,
                unassisted_clear_proven=clear and not errors,errors=sorted(set(errors)),
                player=result['player'],human_slot=side,stages_reached=reached,
                native_own_round_wins=len(own_wins),native_combat_damage_stores=len(damage),
                paid_continue_losses=len(losses),ending_starts=len(starts),ending_completions=len(completed),
                fullPortAcceptance=False,scope='Actual input-only native campaign progression/ownership/damage/win calls; no universal combat, all-ending pixels/audio or whole-port acceptance')


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('folder',type=Path)
    args=parser.parse_args();report=verify(args.folder)
    print(json.dumps(report,indent=2));raise SystemExit(0 if report['passed'] else 1)
