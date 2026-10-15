"""Actual Kintaro damage/input timing; sampled states are not attack causality."""
import collections,json,subprocess
from pathlib import Path
import verify_shang_jump_retry_prefix_v4306 as native
ROOT,need,sha=native.ROOT,native.need,native.sha
FOLDER=native.FOLDER
OUT=ROOT/'audit_v4315_current_kintaro_damage_windows'

def analyze(text):
    rows=native.parse(text)
    fields={r['frame']:r for r in rows if r['tag']=='BOSS_FIELD' and r['stage']=='15'}
    need(fields,'Actual Kintaro fields required')
    for f in fields.values():
        need(f['human_id']=='18' and f['cpu_id']=='12' and f['writes']=='0' and f['assistance']=='none',
             'True own Sonya and native Kintaro; no input intent credited as an action')
    actions=[r for r in rows if r['tag']=='BOSS_ACTION' and r['stage']=='15']
    for r in actions:
        need(r['id']==r['roster']=='18' and r['actor']==r['owner'] and r['main']==r['a13'] and
             int(r['at'],16)==int(r['main'],16)+0x1f0 and r['mask']=='FFFF',
             'Actual own Main action store identity/owner/address/mask')
    jumps=[r for r in actions if r['after']==str(0x308)]
    kicks=[r for r in actions if r['after']==str(0x200)]
    need(jumps and kicks and all(r['pc']=='FF831360' for r in jumps) and
         all(r['pc']=='FF871F50' for r in kicks),'Original native jump and air-kick setter PCs')
    damage=[r for r in rows if r['tag']=='HEALTH' and r['frame'] in fields and
            int(r['before'])>int(r['after'])]
    by_slot=collections.defaultdict(collections.Counter)
    for r in damage:
        f=fields[r['frame']]
        need(r['pc']=='FF836700' and r['at']=={'1':'010602F0','2':'01060EC0'}[r['slot']] and
             0<=int(r['after'])<int(r['before'])<=161,'Actual original collision health subtract/store')
        # This is a same-frame observed-state partition, not attack ownership.
        by_slot[r['slot']][f['human_action']]+=int(r['before'])-int(r['after'])
    plans=[r for r in rows if r['tag']=='BOSS_PLAN' and r['stage']=='15']
    paired=[]
    for kick in kicks:
        prior=[r for r in jumps if 0<kick['frame']-r['frame']<60 and
               r['actor']==kick['actor'] and r['main']==kick['main']]
        if prior:
            jump=prior[-1];f=fields.get(kick['frame'])
            paired.append(dict(jumpFrame=jump['frame'],kickFrame=kick['frame'],delay=kick['frame']-jump['frame'],
              gap=int(f['gap']) if f else None,height=int(f['height']) if f else None))
    wins=[r for r in rows if r['tag']=='WIN' and r['stage']=='15']
    return dict(actualFields=len(fields),actualNativeJumps=len(jumps),actualNativeAirKicks=len(kicks),
      physicalPlans=dict(collections.Counter(r['move'] for r in plans)),
      actualCollisionDamageByTargetAndSampledHumanAction={k:dict(v) for k,v in by_slot.items()},
      nativeJumpKickPairs=paired,actualNativeRoundResults=wins,
      sampledActionNotAttackCausality=True,naturalKintaroMatchClearAccepted=False,
      nativeFloorShadowArtAudioAccepted=False,fullPortAcceptance=False)

if __name__=='__main__':
    need(not OUT.exists(),'Fresh immutable actual timing report')
    path=ROOT/'audit_v4309_shang_jump_retry_whole_campaign_checked/report.json'
    proof=json.loads(path.read_text())
    need(proof['passed'] and proof['case']['actualWholeCampaignGrammarRetained'],
         'Independent complete native campaign and physical grammar required first')
    actual=analyze((FOLDER/'run.log').read_text())
    paths=(Path(__file__).resolve(),Path(native.__file__).resolve(),path,FOLDER/'run.log',FOLDER/'result.json')
    report=dict(passed=True,actualKintaroTiming=actual,inputHashes={str(p):sha(p) for p in paths},
      naturalTowerClearAccepted=False,fullPortAcceptance=False,scope=__doc__)
    OUT.mkdir();need(subprocess.run(['compact.exe','/C','/I','/Q','/S:'+str(OUT)],capture_output=True).returncode==0,'Compress before writes')
    (OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in actual.items() if k not in ('nativeJumpKickPairs','actualNativeRoundResults')},indent=2),flush=True)
    print(json.dumps(dict(nativePairCount=len(actual['nativeJumpKickPairs']),
      pairDelays=dict(collections.Counter(p['delay'] for p in actual['nativeJumpKickPairs']))),indent=2),flush=True)
