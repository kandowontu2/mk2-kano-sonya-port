"""Qualify neutral ownership and stance references, not displayed sole parity."""
import json,re,struct
from pathlib import Path
import verify_native_source_sync as sync
from classify_observed_native_pose_sequences import classify

def main():
    root=sync.ROOT
    case=root/'audit_bounded_twohuman_sonya_kitana_idle_runtime'
    terminal=json.loads((case/'terminal.json').read_text())
    assert terminal['exitCode']==0 and terminal['limitReason'] is None
    assert terminal['peakWorkingSetBytes']<320*1024*1024
    text=(case/'run.log').read_text()
    assert '[LUA ERROR]' not in text and '_FAILED ' not in text
    assert 'IDLE_TERMINAL frame=1424' in text and 'READY frame=1304' in text
    rows=[];poses={18:set(),4:set()}
    for line in text.splitlines():
        r=dict(re.findall(r'(\w+)=([^\s]+)',line))
        if '_FIELD ' in line and 1304<=int(r['frame'])<1424:
            slot=int(r['slot']);assert int(r['id'])==({1:18,2:4}[slot])
            assert r['id']==r['roster'] and r['state']=='1' and int(r['hp'])>0
            assert r['actor']==r['owner'] and r['y']==r['floor']
            for key in ('vx','vy','gravity','flags','body','trail'):assert int(r[key],16)==0
            rows.append(r);poses[int(r['id'])].add(r['pose'])
        if '_INPUT ' in line:assert int(r['frame'])<1304
    assert len(rows)==240 and len({(r['frame'],r['slot']) for r in rows})==240
    payload=(sync.BUILD/'roms/mk2ks/mk2ks.mdata').read_bytes()
    stock=(root/'mk2/mk2-maincpu.bin').read_bytes()
    roots={18:0xff020000,4:struct.unpack_from('<I',stock,0x020c2a+4*4)[0]}
    census={str(i):classify(payload if i==18 else stock,0xfe800000 if i==18 else 0xff800000,
                          roots[i],sorted(poses[i])) for i in (18,4)}
    for fighter,entries in census.items():
        for pose,refs in entries.items():assert refs and set(refs).issubset({0,64}),(fighter,pose,refs)
    out=root/'audit_bounded_twohuman_idle_checked';out.mkdir(exist_ok=False)
    result=dict(passed=True,neutralActorFields=len(rows),stanceReferenceCensus=census,
                terminal=terminal,sourceSync=sync.verify(),logSha=sync.sha(case/'run.log'),
                checkerSha=sync.sha(Path(__file__)),standingSoleParityAccepted=False,
                clippedScanoutProven=False,fullGoalComplete=False)
    (out/'report.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(dict(passed=True,neutralActorFields=len(rows),stanceReferenceCensus=census)))

if __name__=='__main__':main()
