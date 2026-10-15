"""Preserve actual current CPU follow-up identities and failed old expectation.

No gameplay or capture changes. Profiles are declared, never auto-selected to
make a failed check pass; raw action entry and the strict alternatives remain.
"""
import hashlib
import json
from pathlib import Path
import verify_current_cpu_pair_display_v832 as v


def main():
    out=v.ROOT/'audit_v834_current_cpu_profile_diagnosis'
    if out.exists():raise ValueError('Refusing to overwrite evidence')
    cases={};inputs={}
    for name,(player,profile) in v.CASES.items():
        folder=v.ROOT/name;v.matched(folder,inputs)
        log=(folder/'run.log').read_text(encoding='utf-8-sig')
        declared=v.ordinary.verify_log(log,player) if profile=='ordinary' else v.special.verify_log(log,player,profile)
        actions=[r for r in v.ordinary.rows(log,'FOLLOW_INSTRUCTION') if r['kind']=='action']
        cases[name]={'declared_profile':profile,'declared_result':declared,'actual_actions':actions}
        if name=='audit_v831_cpu_queue_sonya_mirror':
            cases[name]['strict_square_result']=v.special.verify_log(log,player,'square')
    for path in (Path(__file__),Path(v.__file__),v.ROOT/'tools/cpu_followup_contract_v545.py'):
        inputs[str(path.resolve())]=hashlib.sha256(path.read_bytes()).hexdigest().upper()
    report={'passed':False,'reason':'Historical bicycle expectation contradicts actual current mirror square entry',
            'cases':cases,'inputHashes':inputs,'fullPortAcceptance':False}
    out.mkdir();(out/'verification.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({n:{'expected':c['declared_profile'],'passed':c['declared_result']['passed'],
                        'actual':[(a['move'],hex(a['entry']))for a in c['actual_actions']],
                        'strict_square_passed':c.get('strict_square_result',{}).get('passed')}for n,c in cases.items()},indent=2))


if __name__=='__main__':main()
