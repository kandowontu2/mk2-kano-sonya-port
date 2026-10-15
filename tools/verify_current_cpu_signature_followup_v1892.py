"""Current natural P1 CPU grab and independently typed native follow-up.

Reuse the unchanged exact composite/raster contract and the original v1423
typed blade/bicycle/Square continuation contract. Never substitute an ordinary
attack or a clean endpoint for a complete signature-move continuation.
"""
import argparse
import json
import re
from pathlib import Path
import verify_current_cpu_square_followup_v1883 as display
import verify_cpu_followup_v1423 as state
from verify_human_special_phases_v1767 import sha

ROOT=display.ROOT

class Signature:
    CPU_SLOT,HUMAN_SLOT=1,2
    def __init__(self,move):self.move=move
    def verify_log(self,log,player):
        proof=state.verify_log(log,player,self.move)
        if proof['passed']:proof['pairs']=[dict(proof)]
        return proof

def verify(folder,player,move):
    case=display.verify(folder,player,Signature(move))
    case['scope']='One actual native P1 '+case['target']+' CPU grab and complete owned '+move+' miss; exact sampled body/scenery/foreground scanout and palettes. Not all AI, repeat/KO/round paths, pixels, opponents, arenas, audio or full port.'
    pins=case.pop('inputHashes')
    for path in folder.rglob('*'):
        if path.is_file():pins[str(path)]=sha(path)
    display.active_launch.module_pins(pins)
    for file,wanted in pins.items():assert sha(file)==wanted,'Changed actual CPU evidence '+file
    return dict(passed=True,candidate=display.NAME,case=folder.name,proof=case,inputHashes=pins,
                originalStateRasterContractsUnchanged=True,fullPortAcceptance=False,allCPUAccepted=False)

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--case',required=True)
    parser.add_argument('--player',choices=tuple(display.ordinary.HUMANS),required=True)
    parser.add_argument('--move',choices=('blade','bicycle','square'),required=True)
    parser.add_argument('--output',required=True);args=parser.parse_args()
    assert re.fullmatch(r'audit_v\d+_[a-z0-9_]+',args.case)and re.fullmatch(r'audit_v\d+_[a-z0-9_]+',args.output)
    folder=ROOT/args.case;out=ROOT/args.output
    assert not out.exists(),'Preserve executed evidence'
    try:report=verify(folder,args.player,args.move)
    except Exception as error:
        pins={str(path):sha(path)for path in folder.rglob('*')if path.is_file()}
        display.active_launch.module_pins(pins)
        report=dict(passed=False,error=repr(error),candidate=display.NAME,case=folder.name,inputHashes=pins,
                    fullPortAcceptance=False,allCPUAccepted=False)
    out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({key:report[key]for key in ('passed','candidate','case','error')if key in report}),flush=True)
    if report['passed']:
        print(json.dumps({key:report['proof'][key]for key in ('sampled_frames','exact_body_pixels','exact_screen_pixels','fullPhysicalPaletteSamples')}),flush=True)
    raise SystemExit(0 if report['passed']else 1)
