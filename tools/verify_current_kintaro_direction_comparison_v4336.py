"""Native identical approach, actual backward inputs and worse bounded outcomes.

Does not claim statistical AI dominance, an engine defect, full move rendering,
audio, Kintaro match clear or complete port. Altered records are counterexamples
only, never presented as a native capture or a positive gameplay event.
"""
import collections,json,re,subprocess
from pathlib import Path
import verify_kintaro_backward_escape_whole_campaign_v4328 as current
ROOT,need,sha=current.ROOT,current.need,current.sha
OLD=ROOT/'audit_v4304_sonya_shang_jump_retry_p2_campaign'
NEW=current.FOLDER
OUT=ROOT/'audit_v4337_current_kintaro_direction_comparison'

def controls(text):
    rows=current.spacing.parse(text)
    fields={r['frame']:r for r in rows if r['tag']=='BOSS_FIELD' and r['stage']=='15'}
    plans=[r for r in rows if r['tag']=='BOSS_PLAN' and r['stage']=='15' and r['move']=='close_pressure_jumpkick_attempt']
    need(plans,'Actual Kintaro pressure plans')
    inputs=collections.defaultdict(list)
    for r in rows:
        if r['tag']=='INPUT':inputs[r['frame']].append(r['button'])
    for plan in plans:
        f=fields[plan['frame']]
        need(f['human_id']=='18' and f['cpu_id']=='12' and f['writes']=='0' and f['assistance']=='none',
             'Actual own Sonya versus Kintaro')
        forward='Right' if int(f['h_x'])<int(f['c_x']) else 'Left'
        back='Left' if forward=='Right' else 'Right'
        need(plan['direction']==back,'Each actual Kintaro pressure plan independently points backward')
        need(inputs[plan['frame']]==['Up',back],'Actual Up/back edges required, not a recorded intention alone')
    return dict(actualBackwardPressurePlans=len(plans),firstActualDirectionChangeFrame=plans[0]['frame'])

def main():
    need(not OUT.exists(),'Fresh immutable native comparison')
    proofs=(ROOT/'audit_v4309_shang_jump_retry_whole_campaign_checked/report.json',
            ROOT/'audit_v4329_kintaro_backward_escape_whole_campaign_checked/report.json')
    accepted=[json.loads(p.read_text()) for p in proofs]
    need(all(r['passed'] and r['case']['actualWholeCampaignGrammarRetained'] for r in accepted),
         'Both complete native campaigns and their exact physical policies qualified first')
    old=(OLD/'run.log').read_text();new=(NEW/'run.log').read_text()
    positive=controls(new);first=positive['firstActualDirectionChangeFrame']
    old_rows=current.spacing.parse(old);new_rows=current.spacing.parse(new)
    before_old=[r for r in old_rows if r['frame']<first]
    before_new=[r for r in new_rows if r['frame']<first]
    need(before_old==before_new and before_old,'All actual native campaign observations/inputs before first direction change identical')
    counts=[]
    for rows in (old_rows,new_rows):
        own=[r for r in rows if r['tag']=='WIN' and r['stage']=='15' and r['slot']=='2']
        lost=[r for r in rows if r['tag']=='LOSS' and r['stage']=='15']
        counts.append(dict(actualOwnKintaroRoundWins=len(own),actualKintaroPaidLosses=len(lost),
                           actualEarnedKintaroRounds=own))
    need(counts[0]['actualOwnKintaroRoundWins']==2 and counts[1]['actualOwnKintaroRoundWins']==0,
         'Observed backward run has no native own Kintaro round wins, not an improvement to promote')
    rows=new_rows;plan=next(r for r in rows if r['tag']=='BOSS_PLAN' and r['frame']==first)
    forward='Left' if plan['direction']=='Right' else 'Right'
    rejected=[]
    for tag,key,value in (('BOSS_PLAN','direction',forward),('INPUT','button','High_Punch')):
        corrupted=current.physical.change(new,tag,first,key,value)
        try:controls(corrupted)
        except ValueError as error:rejected.append(dict(tag=tag,key=key,rejectedBy=str(error)))
        else:raise ValueError('Actual new-direction fault accepted')
        need(controls(new)==positive,'Actual positive restored after each input/plan counterexample')
    pins={}
    for r in accepted:
        for p,h in r['case']['inputHashes'].items():
            need(p not in pins or pins[p]==h,'Shared original proof pin exact');pins[p]=h
    for p in (*proofs,Path(__file__).resolve(),Path(current.__file__).resolve(),OLD/'run.log',NEW/'run.log'):
        pins[str(p.resolve())]=sha(p)
    need(all(sha(p)==h for p,h in pins.items()),'Every actual native/source/comparison byte unchanged')
    return dict(passed=True,actualNativeControls=positive,identicalNativePrefixRows=len(before_old),
      oldForwardPressureOutcome=counts[0],newBackwardPressureOutcome=counts[1],
      actualCounterexamplesRejected=rejected,inputHashes=pins,
      backwardPolicyPromoted=False,naturalTowerClearAccepted=False,fullPortAcceptance=False,scope=__doc__)

if __name__=='__main__':
    need(not OUT.exists(),'Fresh immutable comparison output');report=main()
    OUT.mkdir();need(subprocess.run(['compact.exe','/C','/I','/Q','/S:'+str(OUT)],capture_output=True).returncode==0,'Compress before writing')
    (OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k!='inputHashes'},indent=2),flush=True)
