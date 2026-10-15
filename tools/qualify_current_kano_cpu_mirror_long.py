"""Current completed mirror plus prior reciprocal victim CPU branch coverage."""
import json,copy
import verify_native_source_sync as sync
import check_campaign_stage_chronology as chronology
import qualify_current_kano_cpu_mirror_probe as prior

def main():
    source_sync=sync.verify()
    out=sync.ROOT/'audit_current_kano_cpu_mirror_long_checked';assert not out.exists()
    folder=sync.ROOT/'audit_current_kano_cpu_mirror_long_runtime'
    lua=sync.ROOT/'audit_current_kano_cpu_mirror_long_preparation/campaign.lua'
    terminal=json.loads((folder/'terminal.json').read_text())
    assert terminal['exitCode']==0 and terminal['limitReason'] is None and terminal['observerSha256']==sync.sha(lua)
    assert terminal['peakWorkingSetBytes']<=320*1024*1024 and terminal['elapsedSeconds']<=90 and terminal['logBytes']<=10*1024*1024
    assert not (folder/'stderr.log').read_text().strip()
    assert not any(p.suffix.lower() in ('.png','.bin','.wav') for p in folder.rglob('*'))
    rows=chronology.load(folder/'run.log');counts=prior.gate(rows)
    assert counts==dict(choke=49,knife=4,ball=1)
    assert all(r['human']==r['cpu']=='17:17' for r in rows['LIVE'])
    assert rows['RESULT'][0]['frame']=='20000'
    earlier=sync.ROOT/'audit_current_kano_cpu_router_probe_checked/report.json'
    receipt=json.loads(earlier.read_text());assert receipt['passed']
    log=sync.ROOT/'audit_current_kano_cpu_router_probe_runtime/run.log'
    assert sync.sha(log)==receipt['logSHA256']
    earlier_counts=prior.gate(chronology.load(log));assert earlier_counts==receipt['actualCpuMoveEntries']
    assert set(counts)|set(earlier_counts)=={'choke','knife','blade','ball'}
    bad=copy.deepcopy(rows);next(r for r in bad['CPU_MOVE'] if r['move']=='ball')['move']='knife'
    try:prior.gate(bad)
    except AssertionError:pass
    else:raise AssertionError('Kano Ball target misclassified accepted')
    report=dict(passed=True,sourceSync=source_sync,terminal=terminal,actualMirrorCpuEntries=counts,
        reciprocalVictimCpuEntries=earlier_counts,parentSHA256=sync.sha(earlier),
        allFourKanoCpuSpecialEntriesObservedAcrossTwoVictims=True,mirrorOnlyAllFourObserved=False,
        wrongBallTargetRejected=True,logSHA256=sync.sha(folder/'run.log'),
        fullCpuChoreographyAccepted=False,fullPortAcceptance=False,
        scope='Completed20000field physical Kano mirror CPU probe, native Ball choice and same-field own action; prior completed Sonya-victim CPU probe supplies actual blade branch. Both current genuine scheduled CPU17 contexts cover all four own special entries, not full contact/recovery/pixel/audio, all player sides or campaign/release acceptance.')
    out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(passed=True,allFourKanoCpuSpecialEntriesObserved=True,mirrorEntries=counts,fullPortAcceptance=False)))

if __name__=='__main__':main()
