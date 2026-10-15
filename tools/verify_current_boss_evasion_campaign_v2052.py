"""Independent bounded native campaign proof; incomplete towers never pass clear."""
import argparse
import hashlib
import json
import re
import struct
from pathlib import Path
from verify_p2_campaign import expected_orders
import verify_ball_register_source_v1837 as current_source
import verify_current_interrupt_v1870 as current_launch
NAME=current_source.NAME

def matched(folder,pins):
    result=json.loads((folder/'result.json').read_text(encoding='utf-8-sig'))
    build=json.loads((ROOT/NAME/'build-info.json').read_text(encoding='utf-8-sig'))
    before=json.loads((folder/'input_hashes_before.json').read_text(encoding='utf-8-sig'))
    assert result['candidate']==NAME and result['executable_sha256']==build['executable_sha256']
    assert result['payload_sha256']==build['payload_sha256']and before==result['input_hashes']
    assert result['exit_code']==0 and not result['cheats_enabled']and result['assistance']=='none'
    assert all(before.get(p)==h for p,h in build['input_hashes'].items())
    for p,h in before.items():
        assert current_launch.sha(p)==h,'Changed current campaign input '+p;pins[p]=h
        if Path(p).suffix in('.json','.lua','.ps1'):
            frozen=folder/'input_sources'/Path(p).name
            assert current_launch.sha(frozen)==h,'Changed frozen campaign input';pins[str(frozen)]=h
        if Path(p).suffix=='.lua':
            assert not re.search(r'write_u\d+|:write_|load_?state|\.value\s*=(?!=)',Path(p).read_text())
    pins.update(current_launch.source_pins())
    runner=(folder/'input_sources/run_current_boss_evasion_campaign_v2050.ps1').read_text()
    assert '-nocheat'in runner and '-noautoframeskip -frameskip 0'in runner


ROOT = Path(__file__).resolve().parents[1]
HEX = {'schedule','actor','main','human_actor','human_main','cpu_actor','cpu_main','entry','pc','at','a0','a9','a8','a13','mask'}


def drawing_scope(fields, expected_side=None, expected_fighter=None):
    pairs=re.findall(r'(?:^|\s)(human_slot|fighter|writes|assistance)=(\S+)',fields)
    scope=dict(pairs)
    if len(pairs)!=4 or set(scope)!={'human_slot','fighter','writes','assistance'} or \
       scope.get('writes')!='0' or scope.get('assistance')!='none' or \
       scope.get('human_slot')not in('1','2') or scope.get('fighter')not in('kano','sonya') or \
       (expected_side is not None and scope['human_slot']!=str(expected_side)) or \
       (expected_fighter is not None and scope['fighter']!=expected_fighter):
        raise ValueError('Invalid actual drawing row scope: '+repr(scope))
    return scope


def parse(text, expected_side=None, expected_fighter=None):
    records=[]
    for match in re.finditer(r'^MK2_NAT_CAMPAIGN_(\w+) (.*)$',text,re.M):
        # Drawing rows are separately checked in full by the native raster/
        # cache/row-stream verifier. Do not retain millions of irrelevant
        # drawing dictionaries in the campaign-state proof; still validate
        # their declared unassisted physical scope against every actual line.
        if match[1].startswith(('FLOOR_','SHADOW_')):
            drawing_scope(match[2], expected_side, expected_fighter)
            continue
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


def restore_boss_observation_window(text):
    original=ROOT/'mk2ks_natural_campaign_floor_v1566.lua'
    assert digest(original)=='2D3880B339A6D5F7302E3D25B57F2C52AE0ACA857220908165EF96D2AD9C0C38'
    marker='local floor_origin,floor_pending=nil,nil\n-- Earlier read-only observation for the actual native Kintaro stage only.\n-- Gameplay controls, schedules, health, CPU and all other arena windows stay unchanged.\nlocal function floor_min_age()return p:read_u16(0x01061b30)==15 and 0 or 208 end'
    assert text.count(marker)==1
    restored=text.replace(marker,'local floor_origin,floor_pending=nil,nil')
    restored=restored.replace('frame-floor_origin<floor_min_age()','frame-floor_origin<208').replace('age<floor_min_age()','age<208').replace('frame-floor_origin>=(floor_min_age()==0 and 8 or 216)','frame-floor_origin>=216')
    assert restored==original.read_text(),'Only read-only boss capture window differs; all controls byte-exact'
    return restored

def restore_boss_input_policy(text):
    baseline=ROOT/'mk2ks_natural_campaign_probe_v850.lua'
    assert digest(baseline)=='EC7ADC60ABA59E44EA26E2AB403EBA03C4ADB742D7059811EF8CCEA755E2282D'
    changed=ROOT/'mk2ks_natural_campaign_boss_tactics_v1735.lua'
    assert digest(changed)=='5D9FEB182D5E0DD9E9A5045231869B26F4F0B4C58295722C279F2EA71732FE00'
    original=baseline.read_text()
    first=original.index("   elseif strategy=='zoning' and other.roster==12 then")
    last=original.index("   elseif strategy=='zoning' then",first+1)
    begin='   -- BEGIN actual-input boss tactics v1735; no guest/CPU/difficulty writes.\n'
    end='   -- END actual-input boss tactics v1735.\n'
    assert text.count(begin)==text.count(end)==1
    start=text.index(begin);stop=text.index(end,start)+len(end)
    restored=text[:start]+original[first:last]+text[stop:]
    assert restored==original,'Only actual human boss-button decisions differ; selection, health/win/ending observers and all ordinary controls exact'
    return restored

def restore_boss_evasion_policy(text):
    baseline=ROOT/'mk2ks_natural_campaign_probe_v850.lua'
    assert digest(baseline)=='EC7ADC60ABA59E44EA26E2AB403EBA03C4ADB742D7059811EF8CCEA755E2282D'
    assert digest(ROOT/'mk2ks_natural_campaign_boss_evasion_v1740.lua')=='4DCA2E6A3EE93A11E08F49B6EE79AEE47877077BDA178FBF2DA4AC8A6AAA6CBD'
    original=baseline.read_text()
    text=text.replace('\nlocal boss_escape_direction=nil -- v1740 physical evasion state only','',1)
    text=text.replace("   if (leg_tactic or strategy=='lowkick'or strategy=='throw') and other.roster~=12 and other.roster~=13 then","   if leg_tactic or strategy=='lowkick'or strategy=='throw'then",1)
    first=original.index("   elseif strategy=='zoning' and other.roster==12 then")
    last=original.index("   elseif strategy=='zoning' then",first+1)
    begin='   -- BEGIN actual-input boss tactics v1740; no guest/CPU/difficulty writes.\n'
    end='   -- END actual-input boss tactics v1740.\n'
    assert text.count(begin)==text.count(end)==1
    start=text.index(begin);stop=text.index(end,start)+len(end)
    restored=text[:start]+original[first:last]+text[stop:]
    assert restored==original,'Only boss physical human input decisions differ; all ordinary controls and native progression observers exact'
    return restored

def verify(folder, check_hashes=True, text_override=None):
    # Exact current provenance is mandatory even for in-memory log regressions.
    current_inputs={};matched(folder,current_inputs)
    result=json.loads((folder/'result.json').read_text(encoding='utf-8-sig'))
    text=text_override if text_override is not None else (folder/'run.log').read_text(encoding='utf-8-sig')
    errors=[]
    need=lambda ok,label: errors.append(label) if not ok else None
    side=result['human_slot'];identity={'kano':17,'sonya':18}[result['player']]
    need(side in (1,2) and result['cpu_slot']==3-side, 'Actual physical slots')
    need(result['exit_code']==0 and result['assistance']=='none', 'Terminal unassisted capture')
    need(result['candidate']==NAME,'Current candidate')
    if check_hashes:
        for name,sha in result['input_hashes'].items():
            need(digest(Path(name))==sha,'Frozen input changed: '+name)
    harnesses=list((folder/'input_sources').glob('mk2ks_natural_campaign_*v*.lua'))
    need(len(harnesses)==1 and harnesses[0].name in('mk2ks_natural_campaign_probe_v842.lua','mk2ks_natural_campaign_probe_v848.lua','mk2ks_natural_campaign_probe_v850.lua','mk2ks_natural_campaign_probe_v1548.lua','mk2ks_natural_campaign_floor_v1560.lua','mk2ks_natural_campaign_floor_v1566.lua','mk2ks_natural_campaign_floor_v1698.lua','mk2ks_natural_campaign_boss_tactics_v1735.lua','mk2ks_natural_campaign_boss_evasion_v1740.lua'),
         'One actual whitelisted frozen current physical-input driver')
    harness=harnesses[0]if len(harnesses)==1 else folder/'missing_current_driver.lua'
    if harness.is_file():
        source=harness.read_text()
        if harness.name=='mk2ks_natural_campaign_boss_evasion_v1740.lua':
            source=restore_boss_evasion_policy(source)
            current_inputs[str(ROOT/'mk2ks_natural_campaign_probe_v850.lua')]=digest(ROOT/'mk2ks_natural_campaign_probe_v850.lua')
        if harness.name=='mk2ks_natural_campaign_boss_tactics_v1735.lua':
            source=restore_boss_input_policy(source)
            current_inputs[str(ROOT/'mk2ks_natural_campaign_probe_v850.lua')]=digest(ROOT/'mk2ks_natural_campaign_probe_v850.lua')
        if harness.name=='mk2ks_natural_campaign_floor_v1698.lua':
            source=restore_boss_observation_window(source)
            current_inputs[str(ROOT/'mk2ks_natural_campaign_floor_v1566.lua')]=digest(ROOT/'mk2ks_natural_campaign_floor_v1566.lua')
        need(not re.search(r':write_|\bload\s*\(|\bdofile\s*\(|\beval\b',source),'No guest writes/dynamic delegated code')
        need('roster)<=18 then' in source,'Wait for valid native continue selection ID')
        if harness.name in('mk2ks_natural_campaign_floor_v1560.lua','mk2ks_natural_campaign_floor_v1566.lua','mk2ks_natural_campaign_floor_v1698.lua'):
            baseline=ROOT/'mk2ks_natural_campaign_probe_v850.lua'
            need(digest(baseline)=='EC7ADC60ABA59E44EA26E2AB403EBA03C4ADB742D7059811EF8CCEA755E2282D','Exact immutable accepted physical-input policy')
            current_inputs[str(baseline)]=digest(baseline)
            removed=re.sub(r'-- Read-only native drawing observer, layered over the byte-exact v850 input policy\.[\s\S]*?(?=local adjacency=)', '', source, count=1)
            removed=re.sub(r"   floor_origin=frame;floor_epoch=floor_epoch\+1;floor_latches=\{\};floor_queues=\{\}\n   log\('FLOOR_BEGIN',[^\n]*\n", '', removed, count=1)
            removed=removed.replace('  if frame-floor_origin>=216 and frame-floor_origin<=336 and frame%8==0 then floor_pending=true end\n','',1)
            removed=re.sub(r" log\('FLOOR_RESULT',[^\n]*\n", '', removed, count=1)
            need(removed==baseline.read_text(),'Entire remaining driver exactly equals accepted v850: all physical gameplay inputs untouched')
    need(not re.search(r'\[LUA ERROR\]|fatal error|access violation|exception at',text,re.I),'No observer or native runtime errors')
    rows=parse(text,side,result['player'])
    specials=[r for r in rows if r['tag']=='SPECIAL']
    moves={'knife':(17,0xffffb000,32),'ball':(17,0xffffde00,48),'blade':(17,0xfff8cc00,48),'choke':(17,0xfff91400,48),
           'ring':(18,0xffffb400,32),'square':(18,0xffffca00,48),'bicycle':(18,0xfff9a400,48),'leg':(18,0xfff80800,48)}
    if result['strategy']in('leg','defensive_leg'):
        need(any(r['move']=='leg'for r in specials),'Actual leg entries, not just planned inputs')
    elif result['strategy']=='zoning':
        need(any(r['move']==('knife'if identity==17 else'ring')for r in specials),'Actual native zoning projectile entries')
    for row in specials:
        move_identity,entry,delta=moves.get(row['move'],(-1,-1,-1))
        if harness.name=='mk2ks_natural_campaign_probe_v842.lua':
            # The preserved original projectile-only observer fixes its tap
            # to entry+16 but predates the explicit at field. It cannot stand
            # in for the new four-move observation schema.
            need(row['move']==('knife'if identity==17 else'ring')and 'at'not in row,
                 'Exact original projectile-only schema, never substituted for a new move')
            observed_at=entry+16
        else:observed_at=row['at']
        need(move_identity==identity and row['entry']==entry and observed_at==entry+16 and row['pc']==entry+delta and
             row['actor']==row['a8'] and row['main']==row['a13'] and
             row['id']==row['roster']==identity and
             all(0x01000000<=row[k]<0x01100000 for k in('actor','main')),
             'Actual native special instruction fetch and true human actor/Main registers')
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
    guest_path=ROOT/'audit_v2041_current_sonya_p2_cpu_square_display_kano/guest_maincpu.bin'
    guest=guest_path.read_bytes()
    need(guest==current_source.expected()[0],'Same-candidate initialized guest independently reconstructed; not a campaign-time ROM dump')
    need(hashlib.sha256(original).hexdigest().upper()=='45B3285496DB555EFAF4A3608A4F59845DD47A82E4A0593607E0592F47B36F23',
         'Exact original native program')
    need(guest==current_source.expected()[0],
         'Actual exact-current same-candidate guest snapshot')
    current_inputs[str(guest_path)]=hashlib.sha256(guest).hexdigest().upper()
    current_inputs[str(ROOT/'mk2/mk2-maincpu.bin')]=hashlib.sha256(original).hexdigest().upper()
    word=lambda a:struct.unpack_from('<H',original,(a-0xff800000)//8)[0]
    need((word(0xff8366c0),word(0xff8366f0))==(0x4541,0x8026),'Original native damage subtract/store instructions')
    for address,words in ((0xff86e650,(0xb128,0x1f0)),(0xffa166e0,(0xb008,0x1f0))):
        need(struct.unpack_from('<2H',original,(address-0xff800000)//8)==words,'Original Shang store signature')
    # All observed health writes, including zero damage and positive native
    # bar/reset stores, must come from the actual original per-slot writer.
    # Do not count health-bar animation as earned damage or healing assistance.
    health_pcs={1:{0xff836700,0xff825930,0xff9dece0,0xff9def40},
                2:{0xff836700,0xff825960,0xff9ded10,0xff9def70}}
    for pc in sorted((health_pcs[1]|health_pcs[2])-{0xff836700}):
        at=(pc-48-0xff800000)//8
        need(guest[at:at+6]==original[at:at+6],'Actual unchanged original absolute health-store instruction')
        instruction=struct.unpack_from('<3H',original,at)
        slot=1 if pc in health_pcs[1]else 2
        need(instruction in((0x0580,0x02f0 if slot==1 else 0x0ec0,0x0106),
                            (0x058a,0x02f0 if slot==1 else 0x0ec0,0x0106)),
             'Exact original native absolute store and physical health address')
    at=(0xff8366c0-0xff800000)//8
    need(guest[at:at+8]==original[at:at+8],'Actual unchanged original collision subtract/store code')
    for row in(r for r in rows if r['tag']=='HEALTH'):
        slot=row['slot']
        need(slot in health_pcs and row['pc']in health_pcs.get(slot,set())and
             row['at']==(0x010602f0 if slot==1 else 0x01060ec0),
             'Every observed health store uses its exact original writer and physical slot')
        if row['pc']==0xff836700:
            need(0<=row['after']<=row['before']<=161,'Original collision never heals or supplies health')
    morph_ids=(0,1,2,3,4,5,5,7,8,9,10,11,17,18)
    need(struct.unpack_from('<14H',guest,0xf9040)==morph_ids,'Native fourteen-choice morph roster includes true Kano/Sonya, preserving original stock mapping')
    id_writes=[r for r in rows if r['tag']=='CPU_ID']
    for row in id_writes:
        pc=row['pc'];new=row['after']
        need(row['mask']==0xffff and row['a8']==row['actor'] and
             ((pc==0xff86e670 and new in morph_ids and new==row['a9']&0xffff) or
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
    selections=[r for r in rows if r['tag']=='SELECT']
    inputs=[r for r in rows if r['tag']=='INPUT']
    need([r['number'] for r in selections]==list(range(1,len(selections)+1)),'Sequential genuine selections')
    for selection in selections:
        need(selection['target']==identity and selection['initial']<=18 and selection['schedule']==schedule,'Actual native selection target/starting ID/schedule')
        confirmed=[r for r in rows if r['tag']=='SELECT_ID' and r['number']==selection['number']]
        need(len(confirmed)==2 and all(r['roster']==identity and r['state']==3 for r in confirmed),'Own true ID before native confirm')
        if selection['number']>1:
            preceding=[r for r in losses if r['event']<selection['event']]
            need(bool(preceding),'Continue follows actual native loss')
            if not preceding:continue
            loss=preceding[-1]
            need(selection['continue']==loss['frame'] and selection['stage']==loss['stage'],'Original continue retains its lost stage')
            events=[r for r in inputs if loss['event']<r['event']<selection['event']]
            need(any(r['button']=='Coin' for r in events) and any(r['button']=='Start' for r in events),'Coin and start inputs before real continue selection')
    negative=[r for r in rows if r['tag']=='HEALTH' and r['after']<r['before']]
    damage=[r for r in negative if r['pc']==0xff836700]
    need(bool(damage),'Actual original combat damage stores')
    # Other original stores include round/health-bar teardown; do not mistake
    # their real native writes for combat damage or count them as earned hits.
    need(all(r['pc'] in (0xff836700,0xff9def40,0xff9def70) for r in negative),'Only observed original combat/health-bar writers, no other health decrement writer')
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
                native_owned_special_entries=len(specials),native_special_moves={move:sum(r['move']==move for r in specials)for move in moves
                                                                              if any(r['move']==move for r in specials)},inputHashes=current_inputs,
                fullPortAcceptance=False,scope='Actual input-only native campaign progression/ownership/damage/win calls; no universal combat, all-ending pixels/audio or whole-port acceptance')


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('folder',type=Path)
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args()
    if args.output.exists():raise ValueError('Refusing to overwrite evidence')
    report=verify(args.folder)
    for path in args.folder.rglob('*'):
        if path.is_file():report['inputHashes'][str(path.resolve())]=digest(path)
    for path in(Path(__file__),ROOT/'tools/verify_active_launch_timer_v1520.py',ROOT/'tools/verify_p2_campaign.py'):
        report['inputHashes'][str(path.resolve())]=digest(path)
    current_launch.module_pins(report['inputHashes'])
    args.output.mkdir();(args.output/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:value for k,value in report.items()if k!='inputHashes'},indent=2))
    raise SystemExit(0 if report['passed']else 1)
