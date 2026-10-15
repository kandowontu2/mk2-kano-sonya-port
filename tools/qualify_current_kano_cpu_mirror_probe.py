"""Real native Kano mirror CPU ownership and finite move-choice bindings."""
import inspect,json,copy
from collections import Counter
import verify_native_source_sync as sync
import check_campaign_stage_chronology as chronology
import qualify_current_kano_cpu_router_probe as prior

source=inspect.getsource(prior.gate)
marker='assert len(starts)==len(choices)==3';assert source.count(marker)==1
source=source.replace(marker,'assert starts and len(starts)==len(choices)')
namespace=dict(Counter=Counter);exec(compile(source,__file__+'::same_native_gate','exec'),namespace)
gate=namespace['gate']

def main():
    source_sync=sync.verify()
    out=sync.ROOT/'audit_current_kano_cpu_mirror_probe_checked';assert not out.exists()
    folder=sync.ROOT/'audit_current_kano_cpu_mirror_probe_runtime'
    lua=sync.ROOT/'audit_current_kano_cpu_router_probe_preparation/campaign.lua'
    terminal=json.loads((folder/'terminal.json').read_text())
    assert terminal['exitCode']==0 and terminal['limitReason'] is None and terminal['observerSha256']==sync.sha(lua)
    assert terminal['peakWorkingSetBytes']<=320*1024*1024 and terminal['elapsedSeconds']<=90 and terminal['logBytes']<=10*1024*1024
    assert not (folder/'stderr.log').read_text().strip()
    assert not any(p.suffix.lower() in ('.png','.bin','.wav') for p in folder.rglob('*'))
    rows=chronology.load(folder/'run.log')
    assert all(r['human']==r['cpu']=='17:17' for r in rows['LIVE'])
    assert rows['BOOT'][0]['boot']=='600' and rows['RESULT'][0]['frame']=='12000'
    counts=gate(rows);assert counts==dict(choke=29,knife=3)
    bad=copy.deepcopy(rows);bad['CPU_MOVE'][0]['slot']='1'
    try:gate(bad)
    except AssertionError:pass
    else:raise AssertionError('Human mirror actor counted as CPU actor')
    report=dict(passed=True,sourceSync=source_sync,terminal=terminal,actualCpuMoveEntries=counts,
        actualMirrorHumanAndCpuIDs17=True,humanCpuRoleConfusionRejected=True,
        logSHA256=sync.sha(folder/'run.log'),allFourKanoCpuMovesAccepted=False,
        fullCpuChoreographyAccepted=False,fullPortAcceptance=False,
        scope='Cold genuine P1 Kano/P2 CPU Kano17 mirror through ordinary selector and ladder: native29choke and3knife entries bind CPU slot/state/actor/Main/owner and all observed router choices to correct own action; all sampled live actors true17. No complete contact/recovery/art/audio or ball/blade choice coverage claimed for this mirror context.')
    out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(passed=True,actualMirrorCPU=True,actualCpuMoveEntries=counts,fullPortAcceptance=False)))

if __name__=='__main__':main()
