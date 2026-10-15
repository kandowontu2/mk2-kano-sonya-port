"""Native decision-to-action bindings; actual four-move CPU entry coverage."""
import copy,json
from collections import Counter
import verify_native_source_sync as sync
import check_campaign_stage_chronology as chronology
import qualify_current_native_cpu_move_observer as prior

def choices_gate(rows):
    moves=rows['CPU_MOVE'];prior.entry_gate(moves)
    router=rows['CPU_ROUTER'];assert router
    starts=[r for r in router if r['choice']=='entry']
    choices=[r for r in router if r['choice']!='entry']
    assert len(starts)==len(choices)
    for start,choice in zip(starts,choices):
        assert all(start[k]==choice[k] for k in ('frame','slot','actor','main','owner','id','roster','state','hp','stage'))
        assert choice['choice'] in ('ring','square','bicycle')
        assert start['at']=='FFFBC210'
        assert choice['at']==dict(ring='FFFBC2D0',square='FFFBC300',bicycle='FFFBC330')[choice['choice']]
        assert choice['pc']==choice['at']
        matched=[r for r in moves if r['frame']==choice['frame'] and r['move']==choice['choice']]
        assert len(matched)==1
        assert all(matched[0][k]==choice[k] for k in ('slot','actor','main','owner','id','roster','state','hp','stage'))
    assert {'ring','square','bicycle','leg'}=={r['move'] for r in moves}
    return dict(Counter(r['choice'] for r in choices))

def main():
    source_sync=sync.verify()
    out=sync.ROOT/'audit_current_sonya_cpu_router_probe_checked';assert not out.exists()
    folder=sync.ROOT/'audit_current_sonya_cpu_router_probe_runtime'
    lua=sync.ROOT/'audit_current_sonya_cpu_router_probe_preparation/campaign.lua'
    terminal=json.loads((folder/'terminal.json').read_text())
    assert terminal['exitCode']==0 and terminal['limitReason'] is None and terminal['observerSha256']==sync.sha(lua)
    assert terminal['peakWorkingSetBytes']<=320*1024*1024 and terminal['elapsedSeconds']<=90 and terminal['logBytes']<=10*1024*1024
    assert not (folder/'stderr.log').read_text().strip()
    assert not any(p.suffix.lower() in ('.png','.bin','.wav') for p in folder.rglob('*'))
    rows=chronology.load(folder/'run.log')
    assert all(r['human']==r['cpu']=='18:18' for r in rows['LIVE'])
    assert rows['RESULT'][0]['frame']=='30000'
    decisions=choices_gate(rows)
    bad=copy.deepcopy(rows);next(r for r in bad['CPU_MOVE'] if r['move']=='bicycle')['move']='ring'
    try:choices_gate(bad)
    except AssertionError:pass
    else:raise AssertionError('Wrong actual decision target accepted')
    report=dict(passed=True,sourceSync=source_sync,terminal=terminal,actualDecisions=decisions,
        actualCpuMoveEntries=dict(Counter(r['move'] for r in rows['CPU_MOVE'])),
        allFourSonyaCpuSpecialEntriesObserved=True,wrongDecisionTargetRejected=True,
        logSHA256=sync.sha(folder/'run.log'),fullCpuChoreographyAccepted=False,fullPortAcceptance=False,
        scope='Cold unassisted Sonya18 mirror ladder CPU under physical human approach/guard inputs: all four own specials actually entered; every observed variety-router choice bound to same-field action/CPU actor/Main/owner/ID/state. Not full hit/block/miss/recovery/art/audio, opposite-slot/Kano/whole campaign/release acceptance.')
    out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(passed=True,allFourSonyaCpuSpecialEntriesObserved=True,decisions=decisions,fullPortAcceptance=False)))

if __name__=='__main__':main()
