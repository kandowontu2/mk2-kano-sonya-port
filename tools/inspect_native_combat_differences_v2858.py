"""Inventory all actual participant-field differences from checked v1836.
No changed value is masked, normalized, or declared harmless by this diagnostic.
"""
import json
from collections import Counter
from pathlib import Path
import verify_native_combat_regression_v2854 as model

ROOT=model.ROOT
OUT=ROOT/'audit_v2859_native_combat_differences'
if __name__=='__main__':
    model.assembly.need(not OUT.exists(),'Immutable actual difference inventory')
    proof_path=model.OUT/'report.json';proof=json.loads(proof_path.read_text())
    model.assembly.need(proof['passed'] and len(proof['cases'])==20,'Actual original-contract verified full fixture inventory')
    pins=dict(proof['inputHashes']);pins[str(proof_path)]=model.assembly.sha(proof_path)
    cases=[]
    for case in proof['cases']:
        kind,move,side,victim=case['kind'],case['move'],case['side'],case['victim']
        current_path=ROOT/case['case']/'run.log'
        old_path=ROOT/(f'audit_v1869_interrupt_{move}_p{side}_{victim}' if kind=='interrupt' else f'audit_v1871_ko_{move}_p{side}_{victim}')/'run.log'
        parse=model.interrupt.rows if kind=='interrupt' else model.lifecycle.rows
        actual=parse(current_path.read_text(encoding='utf-8-sig'),'FIELD')
        previous=parse(old_path.read_text(encoding='utf-8-sig'),'FIELD')
        key=(lambda r:(r['frame'],r['slot'])) if kind=='interrupt' else (lambda r:(r['cycle'],r['age'],r['slot']))
        now={key(r):r for r in actual};before={key(r):r for r in previous}
        model.assembly.need(len(now)==len(actual) and len(before)==len(previous),'Unique actual original participant observations')
        common=set(now)&set(before);changed=[];counts=Counter()
        for at in sorted(common):
            differences={name:dict(actual=now[at].get(name),previous=before[at].get(name))
                         for name in set(now[at])|set(before[at]) if now[at].get(name)!=before[at].get(name)}
            if differences:changed.append(dict(key=at,differences=differences));counts.update(differences)
        row=dict(case=case['case'],kind=kind,commonFields=len(common),missingCurrentKeys=sorted(set(before)-set(now)),
                 missingPriorKeys=sorted(set(now)-set(before)),changedParticipantFields=len(changed),
                 changedKeyCounts=dict(counts),firstDifference=changed[0] if changed else None,allDifferences=changed,
                 noValuesMaskedOrNormalized=True,sourceBoundCauseAccepted=False if changed else None)
        cases.append(row)
        print(json.dumps({k:v for k,v in row.items() if k!='allDifferences'}),flush=True)
    for file in (Path(__file__),Path(model.__file__)):
        pins[str(file.resolve())]=model.assembly.sha(file)
    for file,wanted in pins.items():model.assembly.need(model.assembly.sha(file)==wanted,'Actual source/capture unchanged '+file)
    report=dict(passed=True,diagnosticOnly=True,candidate=model.assembly.NAME,cases=cases,
                differencesNotAutomaticallyAccepted=True,fullPortAcceptance=False,inputHashes=pins,scope=__doc__)
    OUT.mkdir();(OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
