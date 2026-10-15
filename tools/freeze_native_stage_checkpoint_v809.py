"""Freeze bounded current stage-performer proofs with preceding actual regression."""
import argparse
import hashlib
import json
from pathlib import Path

def need(ok,message):
    if not ok:raise ValueError(message)
def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('root',type=Path);parser.add_argument('output',type=Path)
    args=parser.parse_args();root,output=args.root.resolve(),args.output.resolve()
    need(not output.exists(),'Do not overwrite checkpoint')
    tracked={}
    def track(path,wanted=None):
        path=Path(path);actual=hashlib.sha256(path.read_bytes()).hexdigest().upper()
        need(wanted is None or wanted==actual,'Changed proof input: '+str(path))
        tracked[str(path.resolve())]=actual
    track(Path(__file__))
    documents={}
    for name in ('audit_v804_current_fatality_pit_checkpoint','audit_v807_native_stage_performers_checked','audit_v808_native_stage_performer_units'):
        path=root/name/'verification.json';track(path);document=json.loads(path.read_text());documents[name]=document
        for target,wanted in document['checked_inputs'].items():track(target,wanted)
    proof=documents['audit_v807_native_stage_performers_checked'];units=documents['audit_v808_native_stage_performer_units']
    need(proof['passed'] and proof['nativeStagePerformerInputAcceptance'] and proof['positive_cases']==8
         and proof['rejection_cases']==12 and len(proof['cases'])==20,'Stage proof scope')
    need(units['passed'] and units['methods']==20 and units['baseline_cases']==20,'Unit acceptance')
    log=root/'audit_v808_native_stage_performer_units/unit-tests.log';track(log)
    need('Ran 20 tests' in log.read_text() and log.read_text().rstrip().endswith('OK'),'Unit output missing')
    for name in ('audit_v807_native_stage_performers_checked','audit_v808_native_stage_performer_units'):
        need(documents[name]['fullPortAcceptance'] is False,'Whole-port scope overclaim')
    output.mkdir()
    report={'candidate':proof['candidate'],'checked_inputs':tracked,'checked_input_count':len(tracked),
        'nativeStagePerformerInputAcceptance':True,'positive_stage_cases':8,'negative_stage_cases':12,
        'fullStageCinematicAcceptance':False,'fullFinisherAcceptance':False,
        'unassistedTowerClearAcceptance':False,'fullPortAcceptance':False,
        'remaining':['remaining finisher/cinematic/art/audio variants','broader selection/ladder/name/floor-shadow/move/CPU/interruption/secret-stage checks',
                     'complete genuine towers through bosses, continues and endings','matching final launcher and release ZIP'],
        'limits':proof['limits'],'release_promoted':False}
    (output/'verification.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:report[k]for k in ('checked_input_count','positive_stage_cases','negative_stage_cases','nativeStagePerformerInputAcceptance','fullPortAcceptance')}))
if __name__=='__main__':main()
