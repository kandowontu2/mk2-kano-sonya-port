"""Accept actual native effect colours only in their source-bound state; reject mutations."""
import json
from pathlib import Path
import numpy as np
import verify_native_campaign_palette_v1580 as palette
import verify_active_launch_cpu_display_v1525 as native

ROOT=palette.ROOT;OUT=ROOT/'audit_v1582_native_palette_contexts_checked'

def verify():
    guest,_,_=native.grab.expected_guest();pins={};palette.sources(guest,pins)
    accepted=[];rejected=[]
    for fighter,side,kind in(('kano',1,'native_frozen'),('sonya',2,'native_sonya_ring_charge')):
        path=ROOT/f'audit_v1579_{fighter}_campaign_palette_diagnostic/report.json';proof=json.loads(path.read_text())
        assert proof['diagnosticCompleted']and proof['fighter']==fighter and proof['humanSlot']==side
        for file,wanted in proof['inputHashes'].items():assert palette.campaign.digest(Path(file))==wanted;pins[file]=wanted
        pins[str(path)]=palette.campaign.digest(path)
        for failure in proof['actualFailures']:
            q=failure['actualQueue'];file=ROOT/failure['paletteFile'];colors=np.fromfile(file,dtype='<u4')
            ids=(17,None)if fighter=='kano'else(None,18)
            result=palette.check(q,colors,guest,ids,side);assert result['kind']==kind
            accepted.append(dict(fighter=fighter,frame=failure['frame'],pose=q['pose'],action=q['action'],kind=kind))
            bad_colors=colors.copy();bad_colors[result['bank']+2]^=1
            wrong_state=dict(q)
            if fighter=='kano':wrong_state['action']=4
            else:wrong_state['pose']=0xfe831700
            wrong_owner=dict(q,slot=3-side)
            for label,record,actual in(('changed_native_colour',q,bad_colors),('effect_in_wrong_state',wrong_state,colors),('wrong_physical_owner',wrong_owner,colors)):
                try:palette.check(record,actual,guest,ids,side)
                except (ValueError,AssertionError):rejected.append(dict(fighter=fighter,frame=failure['frame'],case=label))
                else:raise AssertionError('Invalid effect accepted: '+label)
    assert len(accepted)==32 and len(rejected)==96
    for module in(palette,native):pins[str(Path(module.__file__).resolve())]=palette.campaign.digest(Path(module.__file__))
    pins[str(Path(__file__).resolve())]=palette.campaign.digest(Path(__file__))
    return dict(passed=True,actualNativeEffectPaletteChecks=accepted,inMemoryCounterexamplesRejected=rejected,
                exactOriginalFreezeActionAndLookupBound=True,originalDonorEffectColoursIndependentlyBound=True,
                gameAndCapturesUnchanged=True,fullPortAcceptance=False,inputHashes=pins)

if __name__=='__main__':
    assert not OUT.exists(),'Never overwrite evidence'
    report=verify();OUT.mkdir();(OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(passed=True,actualNativeEffectChecks=len(report['actualNativeEffectPaletteChecks']),
                         badCasesRejected=len(report['inMemoryCounterexamplesRejected']),fullPortAcceptance=False)),flush=True)
