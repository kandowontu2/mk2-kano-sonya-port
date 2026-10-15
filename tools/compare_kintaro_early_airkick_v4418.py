"""Actual native input divergence/airkick timing/outcomes; no inferred victories."""
import collections,json,re,subprocess
from pathlib import Path
import verify_kintaro_early_airkick_whole_campaign_v4416 as current
ROOT,need,sha=current.ROOT,current.need,current.sha
OLD=ROOT/'audit_v4304_sonya_shang_jump_retry_p2_campaign'
NEW=current.FOLDER
OUT=ROOT/'audit_v4419_kintaro_early_airkick_native_comparison'

def controls(text):
    rows=current.spacing.parse(text)
    fields={r['frame']:r for r in rows if r['tag']=='BOSS_FIELD' and r['stage']=='15'}
    inputs=collections.defaultdict(list)
    for r in rows:
        if r['tag']=='INPUT':inputs[r['frame']].append(r['button'])
    rising=[]
    for frame,f in fields.items():
        if 'High_Kick' not in inputs[frame]:continue
        need(f['human_id']=='18' and f['cpu_id']=='12' and f['writes']=='0' and f['assistance']=='none',
          'Actual human Sonya versus native Kintaro; physical HK not a claimed activation')
        need(8<int(f['height'])<90 and int(f['gap'])<100 and frame%6<3,
          'Every actual Kintaro airkick input has declared native height/proximity/edge cadence')
        need(inputs[frame].count('High_Kick')==1 and len(inputs[frame])<=2 and
          set(inputs[frame]).issubset({'Left','Right','High_Kick'}),
          'Only declared ordinary flight direction/High Kick edges in actual kick fields')
        if int(f['human_vy'],16)>=0x80000000:rising.append(frame)
    need(rising,'Actual new rising-flight HK input required; no unchanged trial promoted')
    actions=[r for r in rows if r['tag']=='BOSS_ACTION' and r['stage']=='15']
    jumps=[];kicks=[];excluded=[]
    for r in actions:
        if int(r['after']) not in (0x308,0x200):continue
        need(r['id']==r['roster']=='18' and r['actor']==r['owner']==r['a8'] and r['main']==r['a13'] and
          int(r['at'],16)==int(r['main'],16)+0x1f0 and r['mask']=='FFFF',
          'Actual native move writer owns genuine human actor/Main/address/mask')
        need(r['pc']==('FF831360' if int(r['after'])==0x308 else 'FF871F50'),
          'Actual original jump308 or airkick200 setter, never hurt/throw sampled category')
        (jumps if int(r['after'])==0x308 else kicks).append(r)
    need(jumps and kicks,'Actual native jump and airkick writers required, not intended input counts')
    early=[];pairs=[]
    for kick in kicks:
        prior=[j for j in jumps if 0<kick['frame']-j['frame']<60 and
          j['actor']==kick['actor'] and j['main']==kick['main']]
        if not prior:continue
        jump=prior[-1];f=fields.get(kick['frame'])
        pairs.append(dict(jumpFrame=jump['frame'],kickFrame=kick['frame'],delay=kick['frame']-jump['frame']))
        if kick['frame'] in rising:
            need(f is not None and f['human_actor']==kick['actor'] and f['human_main']==kick['main'],
              'Actual rising-flight airkick writer corroborated by same-field native task')
            early.append(kick)
    need(early,'Actual native rising-flight airkick200 writer required; HK input alone insufficient')
    return dict(actualRisingFlightHKFields=len(rising),firstActualNewRisingInputFrame=rising[0],
      actualNativeJumpWriters=len(jumps),actualNativeAirKickWriters=len(kicks),
      actualNativeRisingFlightKickWriters=len(early),nativeJumpKickPairs=pairs,
      nativeKickDelayCounts=dict(collections.Counter(p['delay'] for p in pairs)),
      nonActorStoresNeverCreditedAsActivations=True)

def main():
    need(not OUT.exists(),'Fresh immutable actual campaign comparison')
    paths=[ROOT/'audit_v4309_shang_jump_retry_whole_campaign_checked/report.json',
      ROOT/'audit_v4417_kintaro_early_airkick_whole_campaign_checked/report.json']
    proofs=[json.loads(p.read_text()) for p in paths]
    need(all(p['passed'] and p['case']['passed'] and p['case']['actualWholeCampaignGrammarRetained'] for p in proofs),
      'Both complete actual native campaigns independently qualified before outcome comparison')
    old=(OLD/'run.log').read_text();new=(NEW/'run.log').read_text();positive=controls(new)
    first=positive['firstActualNewRisingInputFrame']
    oldrows=current.spacing.parse(old);newrows=current.spacing.parse(new)
    a=[r for r in oldrows if r['frame']<first];b=[r for r in newrows if r['frame']<first]
    need(a and a==b,'Entire actual native prefix before first changed kick input identical')
    outcomes=[]
    for rows in (oldrows,newrows):
        wins=[r for r in rows if r['tag']=='WIN' and r['stage']=='15' and r['slot']=='2']
        losses=[r for r in rows if r['tag']=='LOSS' and r['stage']=='15']
        outcomes.append(dict(actualOwnKintaroRoundWins=len(wins),actualKintaroPaidLosses=len(losses),
          actualOwnRoundResults=wins,actualShaoStageEntered=any(r['tag']=='STAGE' and r['stage']=='16' for r in rows),
          actualEndingStarts=sum(r['tag']=='ENDING_START' for r in rows),
          actualEndingCompletions=sum(r['tag']=='ENDING_COMPLETED' for r in rows)))
    faults=[]
    for tag,key,value in [('INPUT','button','High_Punch'),('BOSS_FIELD','human_id','0'),
      ('BOSS_FIELD','height','0'),('BOSS_FIELD','gap','200')]:
        try:controls(current.physical.change(new,tag,first,key,value))
        except Exception as error:faults.append(dict(tag=tag,key=key,rejectedBy=str(error)))
        else:raise ValueError('Actual early kick source/field/input fault accepted: '+tag+':'+key)
    pins={}
    for proof in proofs:
        for p,h in proof['case']['inputHashes'].items():
            need(p not in pins or pins[p]==h,'Shared original input byte identity');pins[p]=h
    for p in (*paths,Path(__file__).resolve(),Path(current.__file__).resolve(),OLD/'run.log',NEW/'run.log'):
        pins[str(p.resolve())]=sha(p)
    need(all(sha(p)==h for p,h in pins.items()),'Every actual source/native comparison byte unchanged')
    return dict(passed=True,actualNativeControls=positive,identicalNativePrefixRows=len(a),
      originalForwardOutcome=outcomes[0],earlierKickOutcome=outcomes[1],actualFaultsRejected=faults,inputHashes=pins,
      naturalTowerClearAccepted=proofs[1]['actualNaturalSonyaP2TowerClearAccepted'],
      earlierKickPolicyPromoted=outcomes[1]['actualShaoStageEntered'],
      resultNotStatisticalAIDominance=True,nativeFloorShadowArtAudioAccepted=False,fullPortAcceptance=False,scope=__doc__)

if __name__=='__main__':
    report=main();OUT.mkdir()
    need(subprocess.run(['compact.exe','/C','/I','/Q','/S:'+str(OUT)],capture_output=True).returncode==0,'Compress before writes')
    (OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k not in ('inputHashes','actualNativeControls')},indent=2),flush=True)
    print(json.dumps({k:v for k,v in report['actualNativeControls'].items() if k!='nativeJumpKickPairs'},indent=2),flush=True)
