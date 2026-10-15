"""Qualify earned Tomb physical-Down fall, not universal stage acceptance."""
import copy,json
import qualify_current_native_tomb_case as base
import verify_native_source_sync as sync

def gate(rows):
    proof=base.gate(rows)
    assert [int(r['age']) for r in rows['DROP_INPUT']]==list(range(32,64))
    branches=rows['DROP_BRANCH']
    assert [r['entry'] for r in branches]==['FF8EB0D0','FF8EB1B0','FF8EB200','FF8EB290','FF876650','FF8EB3C0']
    first=rows['FIELD'][0]
    for row in branches:
        assert int(row['pc'],16)==int(row['entry'],16)+16
        assert row['id']=='18' and row['a8']==row['actor']==first['victim']
        assert row['a13']==row['main']==first['victim_main']
    assert all(r['io0']=='FFFFFDFD' for r in branches[:2])
    assert all(r['io0']=='FFFFFFFF' for r in branches[2:])
    fields={int(r['age']):r for r in rows['FIELD']}
    assert fields[120]['victim_y']=='-174' and fields[400]['victim_y']=='85'
    assert fields[600]['own']==fields[600]['victim']=='00000000'
    assert fields[600]['mode']=='3' and fields[600]['arena']=='2'
    return proof

def main():
    source=sync.verify()
    folder=sync.ROOT/'audit_current_native_tomb_pressed_kano_p1_runtime'
    out=sync.ROOT/'audit_current_native_tomb_pressed_checked';assert not out.exists()
    terminal=json.loads((folder/'terminal.json').read_text())
    assert terminal['exitCode']==0 and terminal['limitReason'] is None
    assert terminal['elapsedSeconds']<=90 and terminal['peakWorkingSetBytes']<=320*1024*1024 and terminal['logBytes']<=10*1024*1024
    assert terminal['observerSha256']==sync.sha(sync.ROOT/'audit_current_native_tomb_pressed_preparation/stage.lua')
    assert not (folder/'stderr.log').read_text().strip()
    assert not any(p.suffix.lower() in ('.png','.bin','.wav') for p in folder.rglob('*'))
    rows=base.load(folder/'run.log');proof=gate(rows)
    for tag,key,value in [('DROP_BRANCH','id','1'),('FIELD','victim_y','-174')]:
        bad=copy.deepcopy(rows)
        if tag=='FIELD':next(r for r in bad[tag] if r['age']=='400')[key]=value
        else:bad[tag][0][key]=value
        try:gate(bad)
        except AssertionError:pass
        else:raise AssertionError('Invalid identity or missing fall accepted')
    report=dict(passed=True,sourceSync=source,terminal=terminal,scene=proof,
                logSHA256=sync.sha(folder/'run.log'),proxyAndMissingFallRejected=True,
                fullPortAcceptance=False,scope='Earned KanoP1/SonyaP2 Tomb, real both-Down ages32..63, native non-RNG drop branch, true victim ownership, ceiling-to-floor motion and actor retirement. No continuous raster/audio or other roles/branches acceptance.')
    out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(passed=True,nativePressedTombFall=True,fullPortAcceptance=False)))

if __name__=='__main__':main()
