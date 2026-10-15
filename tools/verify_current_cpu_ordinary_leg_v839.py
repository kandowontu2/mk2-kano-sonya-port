"""Current native CPU Sonya leg grab -> ordinary recovery/display supplement."""
import hashlib
import json
import sys
from pathlib import Path
import verify_current_cpu_pair_display_v835 as v

CASES={'audit_v838_cpu_queue_sonya_cage':('cage','ordinary'),
       'audit_v838_cpu_queue_sonya_sub_zero':('sub_zero','ordinary'),
       'audit_v838_cpu_queue_sonya_raiden':('raiden','ordinary')}


def main():
    out=v.ROOT/'audit_v839_current_cpu_ordinary_leg_checked'
    v.require(not out.exists(),'Refusing to overwrite evidence')
    cases={name:v.verify(v.ROOT/name,player,profile)for name,(player,profile)in CASES.items()}
    inputs={}
    for name,case in cases.items():
        inputs.update(case.pop('inputHashes'))
        for path in (v.ROOT/name).rglob('*'):
            if path.is_file():inputs[str(path.resolve())]=hashlib.sha256(path.read_bytes()).hexdigest().upper()
    for module in tuple(sys.modules.values()):
        value=getattr(module,'__file__',None)
        if value:
            path=Path(value).resolve()
            if path.is_relative_to(v.ROOT/'tools')and path.suffix=='.py':
                inputs[str(path)]=hashlib.sha256(path.read_bytes()).hexdigest().upper()
    path=v.ROOT/'mk2/mk2-maincpu.bin';inputs[str(path)]=hashlib.sha256(path.read_bytes()).hexdigest().upper()
    proof={'passed':True,'candidate':v.NAME,'cases':cases,'inputHashes':inputs,
           'scope':'three_current_P1_CPU_Sonya_leg_to_ordinary_cleanup_display_paths_only',
           'fullPortAcceptance':False,'CPU_acceptance':False}
    out.mkdir();(out/'verification.json').write_text(json.dumps(proof,indent=2)+'\n')
    print(json.dumps({'passed':True,'cases':len(cases),'sampled_frames':sum(c['sampled_frames']for c in cases.values()),
        'exact_display_pixels':sum(c['exact_screen_pixels']for c in cases.values()),
        'exact_body_pixels':sum(c['exact_body_pixels']for c in cases.values())},indent=2))


if __name__=='__main__':main()
