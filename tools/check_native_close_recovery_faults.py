"""Actual retained-run close-elbow counterexamples, complete positive restored."""
import json,re,subprocess
from pathlib import Path
import qualify_native_close_recovery as model
ROOT,need,sha=model.ROOT,model.need,model.sha

def run(carrier):
    out=ROOT/'audit_native_close_recovery_faults'
    need(not out.exists(), 'Fresh immutable native close-recovery fault proof')
    positive=model.phase(carrier)
    followup=int(model.model.rows(carrier['text'],'MK2_HSPECIAL_RESULT')[0]['followup'])
    first=followup+114;hit=first+6;side=carrier['side']
    faults=[]
    tests=[('close startup action','MK2_HPHASE_POST_FIELD',first,side,'action','4'),
           ('native close contact action','MK2_HPHASE_POST_FIELD',hit,side,'action','1548'),
           ('close startup floor','MK2_HPHASE_POST_FIELD',first,side,'y','80'),
           ('native close damage','MK2_HSPECIAL_HEALTH',hit,3-side,'after','92')]
    for label,tag,frame,slot,key,value in tests:
        line=next(s for s in carrier['text'].splitlines() if s.startswith(tag+' ') and f'frame={frame} ' in s+' ' and f'slot={slot} ' in s+' ')
        changed,count=re.subn(r'\b'+key+r'=\S+',key+'='+value,line,count=1)
        need(count==1 and changed!=line,'Change exactly one actual observed native field')
        try:model.phase(dict(carrier,text=carrier['text'].replace(line,changed,1)))
        except ValueError as error:faults.append(dict(fault=label,rejectedBy=str(error)))
        else:raise ValueError('Actual close-recovery counterexample admitted')
        print('Rejected actual '+label,flush=True)
    need(model.phase(carrier)==positive,'Whole untouched actual recovery/body/health contract restored')
    proof=ROOT/'audit_native_close_recovery_checked/report.json'
    pins=dict(json.loads(proof.read_text())['inputHashes'])
    for p in (proof,Path(__file__),ROOT/'mk2/mk2-maincpu.bin'):
        pins[str(p.resolve())]=sha(p)
    need(all(sha(p)==h for p,h in pins.items()),'Every actual source/evidence pin intact')
    report=dict(passed=True,nativeTerminal=carrier['terminal'],wholePhysicalAndBodyContract=positive,
                originalNativeCloseElbowInterval=[0xff873a70,0xff873bb0],originalCloseElbowAction=0x114,originalContactRecoveryAction=0x60b,
                actualSemanticFaultsRejected=faults,inputHashes=pins,gameplayInterruptionAccepted=False,sourceWaveformAccepted=False,
                fullPortAcceptance=False,goalStatus='active',newBuilds=0,newROMCopies=0,newZIPs=0,newRawMedia=0)
    out.mkdir();p=out/'report.json';p.write_text(json.dumps(report,indent=2)+'\n');h=sha(p)
    need(subprocess.run(['compact.exe','/C','/EXE:LZX','/F','/I','/Q',str(p)],capture_output=True).returncode==0 and sha(p)==h,'Lossless exact fault receipt')
    print(json.dumps(dict(passed=True,actualFaultsRejected=len(faults))),flush=True)
    return report
