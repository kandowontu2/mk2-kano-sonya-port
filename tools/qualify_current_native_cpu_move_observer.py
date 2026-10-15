"""Actual natural CPU-owned Sonya special entries, finite branch coverage only."""
import copy,json
from collections import Counter
import verify_native_source_sync as sync
import check_campaign_stage_chronology as chronology

def entry_gate(entries):
    specs={'ring':0xffffb400,'square':0xffffca00,'bicycle':0xfff9a400,'leg':0xfff80800}
    assert entries
    for r in entries:
        address=specs[r['move']]
        assert int(r['entry'],16)==address and address<=int(r['pc'],16)<address+0x80
        assert r['slot']=='1' and r['human_slot']=='2' and r['id']==r['roster']=='18' and r['state']=='0'
        assert r['owner']==r['actor'] and r['main']!=r['actor']
        assert 0<int(r['hp'])<=161 and r['writes']=='0' and r['assistance']=='none'
        assert int(r['stage'])==0

def main():
    source_sync=sync.verify()
    out=sync.ROOT/'audit_current_native_cpu_move_observer_checked';assert not out.exists()
    folder=sync.ROOT/'audit_current_native_cpu_move_observer_runtime'
    lua=sync.ROOT/'audit_current_native_cpu_move_observer_preparation/campaign.lua'
    terminal=json.loads((folder/'terminal.json').read_text())
    assert terminal['exitCode']==0 and terminal['limitReason'] is None and terminal['observerSha256']==sync.sha(lua)
    assert terminal['peakWorkingSetBytes']<=320*1024*1024 and terminal['elapsedSeconds']<=90 and terminal['logBytes']<=10*1024*1024
    assert not (folder/'stderr.log').read_text().strip()
    assert not any(p.suffix.lower() in ('.png','.bin','.wav') for p in folder.rglob('*'))
    rows=chronology.load(folder/'run.log');entries=rows['CPU_MOVE'];entry_gate(entries)
    assert all(r['human']==r['cpu']=='18:18' for r in rows['LIVE'])
    assert chronology.check(rows,2,18,list(range(13))+[14,15,16])==[0]
    assert rows['BOOT'][0]['boot']=='600' and rows['BOOT'][0]['strategy']=='zoning'
    assert rows['RESULT'][0]['frame']=='12000'
    counts=dict(Counter(r['move'] for r in entries));assert counts==dict(leg=19,ring=4,square=1)
    bad=copy.deepcopy(entries);bad[0]['slot']='2'
    try:entry_gate(bad)
    except AssertionError:pass
    else:raise AssertionError('Human-owned action counted as native CPU move')
    report=dict(passed=True,sourceSync=source_sync,terminal=terminal,actualCpuMoveEntries=counts,
        humanActionMisclassificationRejected=True,logSHA256=sync.sha(folder/'run.log'),
        allCpuMovesAccepted=False,fullCpuChoreographyAccepted=False,fullPortAcceptance=False,
        scope='Cold real Sonya18 mirror ladder opponent, physical human P2 zoning policy: 19 actual CPU leg, four ring and one square native action entries bound to CPU slot/state/actor/Main/owner/trueID/roster. Bicycle unobserved; no full contact/recovery/art/audio, opposite-slot/Kano/campaign/release acceptance.')
    out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(passed=True,actualCpuMoveEntries=counts,allCpuMovesAccepted=False)))

if __name__=='__main__':main()
