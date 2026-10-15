"""Whole current player-one campaign grammar and physical-input replay.

Retains original source/guest/selection/schedule/morph/special/health/winner/
continue/boss/ending/attract checks. Slot-specific provenance and supplemental
Sonya replay scope change only. Native ending pixels/audio remain separate.
"""
import argparse,hashlib,inspect,json,re,subprocess,traceback
from pathlib import Path
import verify_kano_current_p2_whole_campaign_v4487 as kano
import verify_kintaro_pressure_guard_long_whole_campaign_v4442 as sonya
import verify_sonya_zoning700_campaign_v4015 as base
import run_current_p1_campaign_ram_v4782 as capture
import qualify_current_p1_campaign_source_v4783 as boundary
ROOT,need,sha,NAME=capture.ROOT,capture.need,capture.sha,capture.NAME

def clone(function,changes,scope):
    text=inspect.getsource(function)
    for before,after in changes:
        need(text.count(before)==1,'Unique complete native algorithm slot/provenance adaptation '+before)
        text=text.replace(before,after,1)
    exec(compile(text,__file__+'::whole_'+function.__name__,'exec'),scope)
    return scope[function.__name__]

matched=clone(base.matched,[
  ("meta['human_slot']==2 and meta['cpu_slot']==1","meta['human_slot']==1 and meta['cpu_slot']==2"),
  ('transport_boundary()','boundary.source_boundary()'),
  ("meta['player']=='sonya'and meta['strategy']=='zoning'and meta['boot_frame']==700",
   "meta['player']in('kano','sonya')and meta['strategy']==('zoning'if meta['player']=='kano'else'guard_punish')and meta['boot_frame']==600"),
  ('Terminal actual P2 input-only3680 capture','Terminal actual P1 input-only3836 capture')],
  dict(vars(base),__file__=__file__,capture=capture,boundary=boundary,NAME=NAME))
ram_guest=clone(base.ram_guest,[('mk2ks_guarded_campaign_guest_ram_v4006.lua',capture.LUA)],
  dict(vars(base),__file__=__file__,capture=capture))

def ram_guest_checked(folder,pins,wanted,text,errors):
    try:return ram_guest(folder,pins,wanted,text)
    except ValueError as error:errors.append(str(error));return wanted

guard_replay=clone(sonya.physical.replay,[
  ("f['human_slot'] == '2'","f['human_slot'] == '1'"),
  ("r['slot'] == '2'","r['slot'] == '1'"),
  ('Actual true Sonya P2 identity','Actual true Sonya P1 identity')],dict(vars(sonya.physical)))
range_replay=clone(sonya.spacing.replay,[
  ("f['human_slot']=='2'","f['human_slot']=='1'"),
  ("r['slot']=='2'","r['slot']=='1'"),
  ('True SonyaP2 versus scheduled','True SonyaP1 versus scheduled')],dict(vars(sonya.spacing)))

sonya_make_native=clone(sonya.make_native,[
  ('physical.replay(text)','guard_replay(text)'),('spacing.replay(text)','range_replay(text)')],
  dict(vars(sonya),__file__=__file__,capture=capture,boundary=boundary,NAME=NAME,
       matched=matched,ram_guest_checked=ram_guest_checked,guard_replay=guard_replay,range_replay=range_replay))

def make_native(fighter):
    expected=kano.expected_current()
    native=kano.make_native(expected)if fighter=='kano'else sonya_make_native(expected)
    if fighter=='kano':native.__globals__.update(NAME=NAME,matched=matched,ram_guest_checked=ram_guest_checked)
    return native

def run(fighter):
    folder=ROOT/f'audit_v4785_{fighter}_current_p1_campaign_ram'
    observationpath=ROOT/f'audit_v4786_{fighter}_current_p1_campaign_observed/report.json'
    observation=json.loads(observationpath.read_text());meta=json.loads((folder/'result.json').read_text())
    need(observation['passed']and observation['nativeExit']==meta['exit_code']==0 and observation['physicalSlot']==1 and
         observation['capture']==str(folder),'Actual player-one terminal and full native RAM guest/RGB capture before campaign qualification')
    native=make_native(fighter);positive=native(folder)
    need(positive['passed'],'Whole unchanged original campaign/physical-input gate: '+repr(positive['errors']))
    text=(folder/'run.log').read_text();rows=kano.original.knife.old.parse(text,1,fighter)
    faults=[]
    def reject(label,damaged,expected_error):
        need(damaged!=text,'Actual native record corruption, not fixture')
        result=native(folder,text_override=damaged)
        need(not result['passed']and any(expected_error in e for e in result['errors']),
             'Specific original native campaign gate rejects '+label)
        faults.append(dict(kind=label,rejectedBy=expected_error))
        need(native(folder)==positive,'Complete actual player-one positive restored after each real row fault')
    first=lambda tag:next(r for r in rows if r['tag']==tag)
    change=kano.original.change
    r=first('LIVE');reject('proxy_live_identity',change(text,'LIVE',r['frame'],'human','1:1'),'True live human ID')
    r=first('SELECT_ID');reject('wrong_selected_roster',change(text,'SELECT_ID',r['frame'],'roster',1),'selection check retains own true ID')
    r=next(r for r in rows if r['tag']=='HEALTH'and r['pc']==0xff836700 and r['after']<r['before'])
    reject('foreign_health_writer',change(text,'HEALTH',r['frame'],'pc','FFF00000'),'exact original writer')
    reject('negative_collision_health',change(text,'HEALTH',r['frame'],'after',-1),'collision never heals')
    r=first('WIN');reject('wrong_winner_instruction',change(text,'WIN',r['frame'],'pc','FFF00000'),'winner-table call')
    reject('fabricated_winner_health',change(text,'WIN',r['frame'],'health','0,0'),'Native winning health')
    r=first('ROM');reject('foreign_native_schedule',change(text,'ROM',r['frame'],'ids',r['ids'].replace('18','1',1)),'Original-derived true-ID schedule')
    r=first('SPECIAL');reject('foreign_special_actor',change(text,'SPECIAL',r['frame'],'a8','01000000'),'special instruction fetch')
    reject('foreign_special_instruction',change(text,'SPECIAL',r['frame'],'pc','FFF00000'),'special instruction fetch')
    fields={r['frame']for r in rows if r['tag']=='BOSS_FIELD'}
    attack=next((r for r in rows if r['tag']=='INPUT'and r['frame']in fields and r['button']in('High_Punch','Low_Punch')),None)
    if attack:
        line=next(l for l in text.splitlines()if l.startswith(f"MK2_NAT_CAMPAIGN_INPUT frame={attack['frame']} ")and f"button={attack['button']} "in l)
        reject('missing_actual_boss_attack',text.replace(line+'\n','',1),'independently replayed native state')
    if any(r['tag']=='ENDING_COMPLETED'for r in rows):
        r=first('ENDING_COMPLETED')
        reject('missing_own_ending_pages',change(text,'ENDING_COMPLETED',r['frame'],'pictures','0,0'),'Both own native picture/story pages')
        reject('retained_ending_roster',change(text,'ENDING_COMPLETED',r['frame'],'roster',f'{17 if fighter=="kano"else 18},1'),'return to attract roster')
    proof=json.loads((folder/'guest_memory_proof.json').read_text());guest=kano.expected_current()[0]
    for key,value in(('sha256','0'*64),('bytes',1048575),('everyActualByteComparedInRAM',False),
                      ('captureSourceSHA256','0'*64),('transportSourceSHA256','0'*64),('guestDumpFilesWritten',1)):
        bad=dict(proof);bad[key]=value
        try:ram_guest(folder,{},guest,text,proof_override=bad)
        except ValueError as error:faults.append(dict(kind='actual_RAM_guest_'+key,rejectedBy=str(error)))
        else:raise ValueError('Actual RAM guest fault admitted '+key)
        need(ram_guest(folder,{},guest,text)==guest,'Whole actual initialized RAM guest positive restored')
    header=next(l for l in text.splitlines()if l.startswith('MK2_CAMPAIGN_GUEST_RAM_DIGEST '))
    reject('missing_actual_guest_digest',text.replace(header+'\n','',1),'Exactly one actual digest')
    reject('foreign_actual_guest_digest',text.replace(header,header.replace(proof['sha256'],'0'*64),1),'Exactly one actual digest')
    cache=[r for r in text.splitlines()if r.startswith('MK2_MILEENA_CAMPAIGN_RESULT ')]
    need(len(cache)==1 and 'global_cache_stores=0'in cache[0]and
         not any(r.startswith('MK2_MILEENA_CAMPAIGN_OVERRUN ')for r in text.splitlines()),
         'No native global cache overrun through actual player-one terminal')
    finals=[r for r in rows if r['tag']=='RESULT'];ending=[r for r in rows if r['tag']=='ENDING_COMPLETED']
    if positive['unassisted_clear_proven']:
        need(len(ending)==1 and finals[0]['frame']==ending[0]['frame']+300,
             'Actual natural ending-to-attract plus all300ordinary fields, not host deadline')
    deadline=re.findall(r'^MK2_CAMPAIGN_HOST_DEADLINE seconds=([\d.]+) limit=(\d+) assistance=none writes=0$',text,re.M)
    if deadline:need(len(deadline)==1 and deadline[0][1]=='5900'and 5900<=float(deadline[0][0])<5900.03,
                     'Actual finite host-only deadline is not a tower clear')
    pins=dict(positive['inputHashes'])
    for p,h in observation['inputHashes'].items():need(p not in pins or pins[p]==h,'Consistent actual executed player-one sources');pins[p]=h
    for p in[Path(__file__).resolve(),Path(capture.__file__).resolve(),Path(boundary.__file__).resolve(),
             Path(kano.__file__).resolve(),Path(sonya.__file__).resolve(),Path(base.__file__).resolve(),
             Path(sonya.physical.__file__).resolve(),Path(sonya.spacing.__file__).resolve(),observationpath,
             boundary.OUT/'report.json']:pins[str(p.resolve())]=sha(p)
    need(all(sha(p)==h for p,h in pins.items()),'Every complete original/source/actual native evidence byte unchanged')
    return dict(passed=True,fighter=fighter,physicalSlot=1,identity=17 if fighter=='kano'else 18,
      case=positive,inputHashes=pins,actualRowAndRAMGuestFaultsRejected=faults,
      originalWholeCampaignGrammarRetained=True,actualNaturalP1TowerOwnEndingAttractAccepted=positive['unassisted_clear_proven'],
      endingPixelsAccepted=False,completeCampaignAudioAccepted=False,fullPortAcceptance=False,scope=__doc__)

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--fighter',required=True,choices=('kano','sonya'));args=parser.parse_args()
    out=ROOT/f'audit_v4788_{args.fighter}_current_p1_whole_campaign_checked'
    need(not out.exists(),'Fresh immutable actual whole player-one campaign result')
    need((ROOT/f'audit_v4786_{args.fighter}_current_p1_campaign_observed/report.json').exists(),
         'Await actual native terminal before complete whole campaign qualifier')
    try:report=run(args.fighter)
    except Exception as error:report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
    out.mkdir();need(subprocess.run(['compact.exe','/C','/I','/Q','/S:'+str(out)],capture_output=True).returncode==0,'Compressed before writes')
    (out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items()if k not in('inputHashes','case')},indent=2),flush=True)
    raise SystemExit(0 if report['passed']else 1)
