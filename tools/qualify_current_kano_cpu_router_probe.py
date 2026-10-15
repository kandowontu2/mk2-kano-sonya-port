"""Natural real-ID Kano CPU move entries and observed router bindings."""
import copy,json
from collections import Counter
import verify_native_source_sync as sync
import check_campaign_stage_chronology as chronology

def gate(rows):
    specs=dict(knife=0xffffb000,ball=0xffffde00,blade=0xfff8cc00,choke=0xfff91400)
    moves=rows['CPU_MOVE'];assert moves
    for r in moves:
        address=specs[r['move']]
        assert int(r['entry'],16)==address and address<=int(r['pc'],16)<address+0x80
        assert r['slot']=='2' and r['human_slot']=='1' and r['id']==r['roster']=='17' and r['state']=='0'
        assert r['owner']==r['actor'] and r['actor']!=r['main'] and 0<int(r['hp'])<=161
        assert r['writes']=='0' and r['assistance']=='none' and r['stage']=='0'
    router=rows['CPU_ROUTER'];starts=[r for r in router if r['choice']=='entry'];choices=[r for r in router if r['choice']!='entry']
    assert len(starts)==len(choices)==3
    for start,choice in zip(starts,choices):
        assert start['at']=='FFFBC010'
        assert choice['at']==dict(knife='FFFBC0D0',ball='FFFBC100',blade='FFFBC130')[choice['choice']]
        assert choice['pc']==choice['at']
        assert all(start[k]==choice[k] for k in ('frame','slot','actor','main','owner','id','roster','state','hp','stage'))
        matched=[r for r in moves if r['frame']==choice['frame'] and r['move']==choice['choice']]
        assert len(matched)==1 and all(matched[0][k]==choice[k] for k in ('slot','actor','main','owner','id','roster','state','hp','stage'))
    return dict(Counter(r['move'] for r in moves))

def main():
    source_sync=sync.verify()
    out=sync.ROOT/'audit_current_kano_cpu_router_probe_checked';assert not out.exists()
    folder=sync.ROOT/'audit_current_kano_cpu_router_probe_runtime'
    lua=sync.ROOT/'audit_current_kano_cpu_router_probe_preparation/campaign.lua'
    terminal=json.loads((folder/'terminal.json').read_text())
    assert terminal['exitCode']==0 and terminal['limitReason'] is None and terminal['observerSha256']==sync.sha(lua)
    assert terminal['peakWorkingSetBytes']<=320*1024*1024 and terminal['elapsedSeconds']<=90 and terminal['logBytes']<=10*1024*1024
    assert not (folder/'stderr.log').read_text().strip()
    assert not any(p.suffix.lower() in ('.png','.bin','.wav') for p in folder.rglob('*'))
    rows=chronology.load(folder/'run.log')
    assert all(r['human']=='18:18' and r['cpu']=='17:17' for r in rows['LIVE'])
    assert rows['RESULT'][0]['frame']=='12000'
    counts=gate(rows);assert counts==dict(choke=30,blade=2,knife=1)
    bad=copy.deepcopy(rows);bad['CPU_MOVE'][0]['id']='1'
    try:gate(bad)
    except AssertionError:pass
    else:raise AssertionError('Proxy Liu CPU identity accepted')
    report=dict(passed=True,sourceSync=source_sync,terminal=terminal,actualCpuMoveEntries=counts,
        observedRouterChoicesMatchActualEntries=True,proxyIdentityRejected=True,
        logSHA256=sync.sha(folder/'run.log'),allFourKanoCpuMovesAccepted=False,
        fullCpuChoreographyAccepted=False,fullPortAcceptance=False,
        scope='Cold physical P1 Sonya guard versus naturally scheduled actual Kano17 CPU: 30choke, two blade and one knife entries bound to CPU actor/Main/owner/trueID/roster/state; all three observed traveling-router choices match same-field action. Ball unobserved; not full move contact/recovery/art/audio, opposite-slot/all CPU/campaign/release acceptance.')
    out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(passed=True,actualCpuMoveEntries=counts,allFourKanoCpuMovesAccepted=False)))

if __name__=='__main__':main()
