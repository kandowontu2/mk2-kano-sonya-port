"""Three bounded PNGs bound to complete unchanged Tomb scalar baseline."""
import json
import verify_native_source_sync as sync
from qualify_current_native_tomb_case import load,gate

def main():
    source=sync.verify();folder=sync.ROOT/'audit_current_native_tomb_visual_kano_p1_runtime'
    out=sync.ROOT/'audit_current_native_tomb_visual_kano_p1_checked';assert not out.exists()
    terminal=json.loads((folder/'terminal.json').read_text())
    assert terminal['exitCode']==0 and terminal['limitReason'] is None
    assert terminal['elapsedSeconds']<=90 and terminal['peakWorkingSetBytes']<=320*1024*1024 and terminal['logBytes']<=10*1024*1024
    assert terminal['observerSha256']==sync.sha(sync.ROOT/'audit_current_native_tomb_visual_preparation/stage.lua')
    assert not (folder/'stderr.log').read_text().strip()
    rows=load(folder/'run.log');proof=gate(rows)
    original=sync.ROOT/'audit_current_native_tomb_kano_p1_runtime/run.log'
    prefix='MK2_STAGE_'
    actual=[l for l in (folder/'run.log').read_text().splitlines() if l.startswith(prefix) and not l.startswith(prefix+'VISUAL_SAVED ')]
    expected=[l for l in original.read_text().splitlines() if l.startswith(prefix)]
    assert actual==expected
    assert [r['age'] for r in rows['VISUAL_SAVED']]==['15','120','600']
    assert all(int(r['frame'])==proof['actionFrame']+int(r['age']) for r in rows['VISUAL_SAVED'])
    images=list(folder.rglob('*.png'));assert len(images)==3
    assert {p.name for p in images}=={'tomb_15.png','tomb_120.png','tomb_600.png'}
    total=sum(p.stat().st_size for p in images);assert total<=512*1024
    assert not any(p.suffix.lower() in ('.bin','.wav') for p in folder.rglob('*'))
    report=dict(passed=True,sourceSync=source,terminal=terminal,scene=proof,
                completeScalarBaselineUnchanged=True,totalPNGBytes=total,
                screenshots=[dict(name=p.name,sha256=sync.sha(p),bytes=p.stat().st_size) for p in images],
                continuousRasterAccepted=False,fullPortAcceptance=False,
                scope='Three current native earned Tomb screenshots at ages15/120/600 with whole original scalar trace identical. True Kano/Sonya role and complete earned admission/followthrough gates retained. Not all visual fields, Tomb branches, sound, other roles, Pit or release acceptance.')
    out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(passed=True,totalPNGBytes=total,fullPortAcceptance=False)))

if __name__=='__main__':main()
