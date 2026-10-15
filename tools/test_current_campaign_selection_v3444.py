"""Actual bounded terminal CSS faults; never excuse a completed bad selection."""
import json,re,subprocess
from pathlib import Path
import verify_current_campaign_shao_highkick_v3440 as current
ROOT=current.ROOT;need=current.need;sha=current.sha
CASE=ROOT/'audit_v3421_current_sonya_natural_highkick_campaign'
OUT=ROOT/'audit_v3445_current_campaign_selection_counterexamples'

def main():
    need(not OUT.exists(),'Immutable actual CSS fault report')
    proofpath=ROOT/'audit_v3441_current_sonya_zoning_campaign_checked/report.json'
    proof=json.loads(proofpath.read_text())
    need(proof['passed'] and proof['allCompletedSelectionConfirmationChecksRetained']
         and proof['incompleteFinalSelectionNotAcceptedAsConfirmed'],'Actual bounded selection result first')
    native=current.make_verifier(current.current.expected_current())
    log=(CASE/'run.log').read_text(encoding='utf-8-sig')
    line=next(x for x in log.splitlines()if x.startswith('MK2_NAT_CAMPAIGN_SELECT_ID '))
    frame=int(re.search(r' frame=(\d+)',line)[1]);number=int(re.search(r' number=(\d+)',line)[1])
    need(number==1 and 'roster=18 state=3'in line,'Actual first completed native own confirmation')
    late=line.replace(f'frame={frame}', 'frame=213383').replace('number=1 ','number=57 ')
    resultline=next(x for x in log.splitlines()if x.startswith('MK2_NAT_CAMPAIGN_RESULT '))
    variants=[('missing_completed_confirmation',log.replace(line+'\n','',1)),
        ('wrong_completed_own_identity',log.replace(line,line.replace('roster=18','roster=17'),1)),
        ('completed_confirmation_shifted_one_field',log.replace(line,line.replace(f'frame={frame}',f'frame={frame+1}'),1)),
        ('fabricated_future_confirmation_after_time_limit',log.replace(resultline,late+'\n'+resultline,1))]
    faults=[]
    for label,changed in variants:
        need(changed!=log,'Non-vacuous actual selection fault')
        value=native(CASE,text_override=changed)
        need(not value['passed'] and 'Every due native selection check retains own true ID'in value['errors'],
             'Specific due-time/true-ID rejection, not unrelated exception')
        faults.append(label);print('Rejected '+label,flush=True)
    positive=native(CASE)
    need(positive['passed'] and positive['stages_reached']==[0] and not positive['unassisted_clear_proven'],
         'Same-path original campaign positive remains bounded and not a clear')
    pins=dict(proof['inputHashes']);pins[str(proofpath.resolve())]=sha(proofpath)
    pins[str(Path(current.__file__).resolve())]=sha(current.__file__)
    pins[str(Path(__file__).resolve())]=sha(__file__)
    for file,digest in pins.items():need(sha(file)==digest,'Captured game/native controls/selection records unchanged')
    value=dict(passed=True,actualSpecificCounterexamples=faults,samePathWholeNativeCampaignPositiveAccepted=True,
        unconfirmedFinalSelectionNeverAcceptedAsCompleted=True,actualCaptureOrGameChanged=False,
        fullPortAcceptance=False,inputHashes=pins)
    OUT.mkdir();path=OUT/'report.json';path.write_text(json.dumps(value,indent=2)+'\n');digest=sha(path)
    result=subprocess.run(['compact.exe','/C','/I','/Q',str(path)],capture_output=True,text=True)
    need(result.returncode==0 and sha(path)==digest,'Lossless fault-report compression')
    print(json.dumps({k:v for k,v in value.items()if k!='inputHashes'},indent=2),flush=True)

if __name__=='__main__':main()
