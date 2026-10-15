"""Reject actual-field and input corruptions in every one of 52 fresh fixtures.

Mutations are in-memory only. Actual guest inputs, logs and captured pixels
are never edited. This does not accept the unresolved blade scene differences.
"""
import json,re
from pathlib import Path
import verify_native_palette_special_state_v2792 as current

ROOT=current.ROOT;OUT=ROOT/'audit_v2795_native_palette_special_state_units'

def tests():
    proof_path=current.OUT/'report.json';proof=json.loads(proof_path.read_text())
    current.assembly.need(proof['passed'] and proof['candidate']==current.NAME and proof['current52CaseHumanStateMatrixAccepted'],'Actual fresh complete state proof')
    pins={str(proof_path):current.assembly.sha(proof_path)}
    for file,wanted in proof['inputHashes'].items():
        current.assembly.need(current.assembly.sha(file)==wanted,'Unchanged accepted state evidence '+file)
    rejected=[]
    for move,side,scenario,air in current.dispatch.fixtures:
        suffix=move+('_air' if air else '_'+scenario if scenario else '')
        path=ROOT/f'audit_v2791_human_{suffix}_p{side}'/'run.log'
        log=path.read_text(encoding='utf-8-sig');pins[str(path)]=current.assembly.sha(path)
        model=current.negative if scenario else current.positive
        def verify(value):
            if scenario:return model.verify_log(value,move,side,scenario)
            return model.verify_log(value,move,side,air)
        verify(log)
        result,=model.rows(log,'RESULT');lines=log.splitlines(keepends=True)
        def index(tag,frame,slot=None,extra=None):
            matches=[i for i,line in enumerate(lines) if line.startswith('MK2_HSPECIAL_'+tag+' ') and f'frame={frame} ' in line and (slot is None or f'slot={slot} ' in line) and (extra is None or extra in line)]
            current.assembly.need(len(matches)==1,'One real target field for counterexample')
            return matches[0]
        first=index('FIELD',result['ready']+1,side)
        recovery=index('FIELD',result['recovered'],side)
        entry=index('EVENT',result['entry'],extra=f'entry={model.SPECS[move][1]:08X}')
        command=next(i for i,line in enumerate(lines) if line.startswith('MK2_HSPECIAL_INPUT ') and f'slot={side} ' in line and result['command']<=int(re.search(r'\bframe=(\d+)',line)[1])<result['followup'])
        own_recovery=next(f for f in model.rows(log,'FIELD') if f['frame']==result['recovered'] and f['slot']==side)
        first_owner=int(re.search(r'\bowner=([0-9A-F]+)',lines[first])[1],16)
        mutations=[('Liu_proxy',first,'id','1'),('wrong_owner',first,'owner',f'{first_owner+16:08X}'),
            ('missing_field',first,None,None),('guest_write_assistance',first,'writes','1'),
            ('incomplete_floor_recovery',recovery,'floor',str(own_recovery['floor']+1)),
            ('unexplained_health',first,'hp','160'),('missing_native_entry',entry,None,None),
            ('missing_command_input',command,None,None)]
        for label,target,key,value in mutations:
            altered=lines.copy()
            if key is None:altered[target]=''
            else:
                altered[target],count=re.subn(r'\b'+key+r'=[^\s]+',key+'='+value,altered[target])
                current.assembly.need(count==1 and altered[target]!=lines[target],'Actual specific evidence mutation')
            try:verify(''.join(altered))
            except ValueError as error:
                rejected.append(dict(case=path.parent.name,label=label,rejection=str(error)))
            else:raise ValueError('Actual state corruption was accepted: '+path.parent.name+' '+label)
    current.assembly.need(len(rejected)==416,'Eight actual corruptions rejected in all 52 fixtures')
    for module in (current,current.positive,current.negative,current.assembly,current.dispatch):
        pins[str(Path(module.__file__).absolute())]=current.assembly.sha(module.__file__)
    pins[str(Path(__file__).absolute())]=current.assembly.sha(__file__)
    return dict(passed=True,candidate=current.NAME,cases=52,actualSpecificCounterexamplesRejected=416,
        rejected=rejected,originalCapturesUnmodified=True,allEndpointScenesAccepted=False,
        fullPortAccepted=False,inputHashes=pins,scope=__doc__)

if __name__=='__main__':
    current.assembly.need(not OUT.exists(),'Immutable fresh unit evidence')
    try:report=tests()
    except Exception as error:report=dict(passed=False,error=repr(error),fullPortAccepted=False)
    OUT.mkdir();(OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:report.get(k) for k in ('passed','error','cases','actualSpecificCounterexamplesRejected')},indent=2),flush=True)
    raise SystemExit(0 if report['passed'] else 1)
