"""Natural current Kano CPU choke on Sonya and actual ordinary continuation.

This capture did not enter blade: require the original typed ordinary contract,
not a renamed signature miss. Retain the v1883 exact complete-scene renderer.
"""
import json,struct
from pathlib import Path
import verify_current_cpu_square_followup_v1883 as display
import verify_physical_p1_cpu_pair_v1457 as ordinary

ROOT=display.ROOT;CASE=ROOT/'audit_v1931_current_kano_cpu_choke_follow_human_sonya'
OUT=ROOT/'audit_v1934_current_kano_sonya_cpu_display_checked'

def verify_log(log):
    proof=ordinary.verify_log(log,'sonya')
    assert proof['passed'],proof['errors']
    assert proof['target']=='kano'and proof['native_followup']['kind']=='ordinary'
    guest,_,_=display.active.expected()
    for r in ordinary.rows(log,'FIELD'):
        assert r['id']==17 and r['vid']==18 and r['floor']==r['stage_floor']-134 and r['vfloor']==r['stage_floor']-135
    for r in ordinary.flag_rows(log):
        assert struct.unpack_from('<HH',guest,(r['pc']-32-0xff800000)//8)==(r['op0'],r['op1']),'Every original instruction word matches current whole guest'
    return proof

class CurrentOrdinary:
    CPU_SLOT,HUMAN_SLOT=1,2
    def verify_log(self,log,player):
        assert player=='sonya'
        proof=verify_log(log);proof['pairs']=[dict(proof)]
        return proof

def report():
    case=display.verify(CASE,'sonya',CurrentOrdinary())
    pins=case.pop('inputHashes')
    for path in CASE.rglob('*'):
        if path.is_file():pins[str(path)]=display.current.digest(path)
    display.active_launch.module_pins(pins)
    for file,value in pins.items():assert display.current.digest(file)==value
    return dict(passed=True,candidate=display.NAME,proof=case,inputHashes=pins,
        gameBytesChanged=False,fullPortAcceptance=False,allCPUAccepted=False,scope=__doc__)

if __name__=='__main__':
    assert not OUT.exists(),'Preserve executed evidence'
    try:result=report()
    except Exception as error:result=dict(passed=False,error=repr(error),fullPortAcceptance=False)
    OUT.mkdir();(OUT/'report.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:result[k]for k in('passed','error')if k in result}),flush=True)
    if result['passed']:print(json.dumps({k:result['proof'][k]for k in('sampled_frames','exact_body_pixels','exact_screen_pixels','fullPhysicalPaletteSamples')}),flush=True)
    raise SystemExit(0 if result['passed']else 1)
