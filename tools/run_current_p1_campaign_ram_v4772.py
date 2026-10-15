"""Actual current3836 player-one solo campaigns, no proxy or state assistance.

Retains the complete original4439 initialized-guest/RGB RAM collector and the
previously tested physical policies. Player slot, exact wrapper and fresh
leaves change; actual tower/ending acceptance requires independent verification.
"""
import argparse,inspect,json,subprocess,traceback
from pathlib import Path
import run_kintaro_pressure_guard_long_campaign_v4439 as previous
ROOT,need,sha,NAME=previous.ROOT,previous.need,previous.sha,previous.NAME
LUA='mk2ks_current_p1_campaign_ram_v4771.lua'
PREFLIGHT=ROOT/'audit_v4774_current_p1_campaign_source_checked/report.json'

def collector_source():
    text=inspect.getsource(previous.capture)
    changes=[
      ("need(fighter=='sonya','Actual unfinished Sonya P2 context only')",
       "need(fighter in('kano','sonya'),'Only actual true17/18 player-one campaigns')"),
      ("ROOT/'audit_v4438_kintaro_pressure_guard_long_source_preflight/report.json'",'PREFLIGHT'),
      ('audit_v4440_{fighter}_kintaro_pressure_guard_long_p2_campaign','audit_v4775_{fighter}_current_p1_campaign_ram'),
      ("MK2KS_CAMPAIGN_SIDE='2'","MK2KS_CAMPAIGN_SIDE='1'"),
      ("MK2KS_CAMPAIGN_STRATEGY='guard_punish'","MK2KS_CAMPAIGN_STRATEGY='zoning'if fighter=='kano'else'guard_punish'"),
      ('human_slot=2,cpu_slot=1','human_slot=1,cpu_slot=2'),
      ('{fighter} P2 actual3836 campaign started','{fighter} P1 actual3836 campaign started'),
      ('{fighter} P2 terminal0;','{fighter} P1 terminal0;')]
    for before,after in changes:
        need(text.count(before)==1,'Unique exact host role/slot/path collector adaptation '+before)
        text=text.replace(before,after,1)
    return text

def capture(fighter):
    import qualify_current_p1_campaign_source_v4773 as source
    source.source_boundary();proof=json.loads(PREFLIGHT.read_text())
    need(proof['passed']and all(sha(p)==h for p,h in proof['inputHashes'].items()),
         'Actual whole retained slot-polymorphic source and unchanged true17/18 build before first player-one boot')
    scope=dict(vars(previous),__file__=__file__,source=source,LUA=LUA,PREFLIGHT=PREFLIGHT)
    exec(compile(collector_source(),__file__+'::whole4439_player_one_inputs_only','exec'),scope)
    return scope['capture'](fighter)

def run(fighter):
    folder,headers,images=capture(fighter)
    text=(folder/'run.log').read_text();rows=previous.knife.old.parse(text,1,fighter)
    meta=json.loads((folder/'result.json').read_text())
    need(meta['exit_code']==0 and meta['human_slot']==1 and meta['cpu_slot']==2 and
         meta['nativeGuestBytesVerifiedInRAM']==1048576 and meta['guestDumpFilesWritten']==0 and
         meta['rawRasterFilesWritten']==0 and meta['raw_audio_files_written']==0,
         'Actual player-one terminal and complete native initialized guest/RGB RAM transport; never inferred from player two')
    pins=dict(meta['input_hashes'])
    for p in folder.rglob('*'):
        if p.is_file():pins[str(p.resolve())]=sha(p)
    pins[str(Path(__file__).resolve())]=sha(__file__)
    need(all(sha(p)==h for p,h in pins.items()),'Every actually executed current/native source and terminal evidence unchanged')
    return dict(passed=True,candidate=NAME,fighter=fighter,physicalSlot=1,identity=17 if fighter=='kano'else 18,
      nativeExit=0,capture=str(folder),actualStages=[r['stage']for r in rows if r['tag']=='STAGE'],
      endingStarts=sum(r['tag']=='ENDING_START'for r in rows),endingCompletions=sum(r['tag']=='ENDING_COMPLETED'for r in rows),
      actualNativeRGBFrameCallbacks=len(headers),inputHashes=pins,fullIndependentCampaignVerificationPending=True,
      actualNaturalTowerClearAccepted=False,fullEndingVRAMRGBAccepted=False,completeCampaignAudioAccepted=False,
      rawMediaGuestROMOrBuildFilesWritten=0,publicPlayableChanged=False,fullPortAcceptance=False,scope=__doc__)

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--fighter',required=True,choices=('kano','sonya'));args=parser.parse_args()
    out=ROOT/f'audit_v4776_{args.fighter}_current_p1_campaign_observed'
    need(not out.exists()and not(ROOT/f'audit_v4775_{args.fighter}_current_p1_campaign_ram').exists(),
         'Fresh actual player-one campaign; never overwrite/restart an executed leaf')
    try:report=run(args.fighter)
    except Exception as error:report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
    out.mkdir();need(subprocess.run(['compact.exe','/C','/I','/Q','/S:'+str(out)],capture_output=True).returncode==0,'Compressed before writes')
    (out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items()if k!='inputHashes'},indent=2),flush=True)
    raise SystemExit(0 if report['passed']else 1)
