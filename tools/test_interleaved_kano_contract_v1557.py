"""Reject in-memory contradictions without changing the preserved native capture."""
import hashlib,json,re,sys
from pathlib import Path
import verify_interleaved_kano_cpu_v1556 as contract
ROOT=contract.ROOT;OUT=ROOT/'audit_v1557_interleaved_kano_counterexamples'

def change(text,pattern,replacement):
    changed,count=re.subn(pattern,replacement,text,count=1,flags=re.M)
    assert count==1 and changed!=text,'Counterexample anchor must exist exactly in actual capture'
    return changed

if __name__=='__main__':
    assert not OUT.exists(),'Never overwrite evidence'
    positive_path=ROOT/'audit_v1556_interleaved_kano_display_checked/report.json'
    positive=json.loads(positive_path.read_text());assert positive['passed'] and positive['sampledNativeScanouts']==119
    pins=dict(positive['inputHashes'])
    for name,wanted in pins.items():assert contract.display.current.digest(name)==wanted,'Changed current accepted evidence'
    text=(contract.FOLDER/'run.log').read_text(encoding='utf-8-sig')
    cases={
        'missing_paired_callback':change(text,r'^MK2_CPU_PAIR_FIELD frame=1780 .*\n',''),
        'wrong_live_cpu_identity':change(text,r'(^MK2_CPU_PAIR_FIELD frame=1780 .*? id=)17 ',r'\g<1>18 '),
        'unlogged_native_damage':change(text,r'(^MK2_CPU_PAIR_HEALTH frame=1775 .*? after=)147 ',r'\g<1>148 '),
        'wrong_followup_instruction':change(text,r'(^MK2_CPU_PAIR_FOLLOW_INSTRUCTION frame=1832 .*? entry=)FFF8CC00 ',r'\g<1>FFF8CC20 '),
        'broken_owned_state_store':change(text,r'(^MK2_CPU_PAIR_FLAG frame=1832 .*?kind=action .*? after=)0117 ',r'\g<1>0116 '),
        'false_clean_victim_handoff':change(text,r'(^MK2_CPU_PAIR_VICTIM_REGAIN frame=1871 .*? vgravity=)00000000 ',r'\g<1>00008000 '),
    }
    rejected={}
    for name,corrupted in cases.items():
        try:contract.verify(log_override=corrupted,pixels=False)
        except Exception as error:rejected[name]=repr(error)
        else:raise AssertionError('Contradictory evidence accepted: '+name)
    for module in tuple(sys.modules.values()):
        value=getattr(module,'__file__',None)
        if value:
            path=Path(value).resolve()
            if path.is_relative_to(ROOT/'tools') and path.suffix=='.py':pins[str(path)]=hashlib.sha256(path.read_bytes()).hexdigest().upper()
    pins[str(positive_path)]=hashlib.sha256(positive_path.read_bytes()).hexdigest().upper()
    OUT.mkdir();(OUT/'report.json').write_text(json.dumps(dict(passed=True,rejected=rejected,
        actualCaptureUnmodified=True,positiveScanouts=119,inputHashes=pins,fullPortAcceptance=False),indent=2)+'\n')
    print(json.dumps(dict(passed=True,counterexamplesRejected=len(rejected),fullPortAcceptance=False)),flush=True)
