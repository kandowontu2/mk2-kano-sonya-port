"""Four current real-input Sonya ring/leg cases, not complete Sonya/port acceptance."""
import json
import verify_native_candidate_v517 as build
import verify_human_special_matrix as positive
from verify_ko_round_floor_shadows import digest,need,rgb

def verify():
    inputs={};cases=[]
    for move in('ring','leg'):
        for side in(1,2):
            folder=build.ROOT/f'audit_v520_sonya_smoke_{move}_p{side}'
            build.matched(folder,inputs)
            cases.append(positive.verify_log((folder/'run.log').read_text(encoding='utf-8-sig'),move,side))
            for name in('special_before.png','special_recovered.png','special_final.png'):
                file=folder/'snap'/name;need(rgb(file).shape==(254,400,3),'Native screenshot dimensions');inputs[str(file)]=digest(file)
    for name in('tools/verify_sonya_smoke_v517.py','tools/verify_native_candidate_v517.py','tools/verify_human_special_matrix.py',
                'tools/verify_ko_round_floor_shadows.py','tools/inspect_ground_presentation.py'):
        file=build.ROOT/name;inputs[str(file)]=digest(file)
    return dict(passed=True,fullPortAcceptance=False,candidate=build.NAME,cases=cases,
                pairedFields=sum(c['fields']for c in cases),inputHashes=inputs,
                scope='Current real-input ring and leg-grab hit/recovery/follow-up in both slots with true Sonya ID18 and Main ownership. '
                      'Not all Sonya moves/victims/CPU/UI/campaign/finishers/audio or full acceptance.')

if __name__=='__main__':print(json.dumps(verify(),indent=2))
