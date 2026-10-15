"""Paired native-only control: verify mixed-output convergence after real hit."""
import copy,json,re
from decimal import Decimal
from pathlib import Path
import verify_native_source_sync as sync
import check_bounded_native_retained_tap as trace

def load(folder):
    rows=[]
    with (folder/'run.log').open() as stream:
        for line in stream:
            assert '[LUA ERROR]' not in line
            if line.startswith('MK2_HIT_PCM '):rows.append(dict(re.findall(r'(\w+)=([^\s]+)',line)))
    return rows

def gate(on,off,tick):
    assert len(on)==len(off)==184
    for a,b in zip(on,off):
        assert all(a[k]==b[k] for k in ('frame','seconds','bytes','writes','raw_media'))
    before=[(a,b) for a,b in zip(on,off) if tick-Decimal('.5')<Decimal(a['seconds'])<tick]
    after=[(a,b) for a,b in zip(on,off) if Decimal(a['seconds'])>tick+Decimal('.1')]
    assert before and any(a['sha256']!=b['sha256'] for a,b in before),'No positive imported contribution before hit'
    assert len(after)>20 and all(a==b for a,b in after),'Post-hit mixed output differs from native-only control'
    assert Decimal(after[-1][0]['seconds'])>tick+Decimal('.5')
    mismatches=[a['seconds'] for a,b in zip(on,off) if a!=b]
    return dict(postHitIdenticalUpdates=len(after),lastDifferentUpdateSeconds=mismatches[-1],
        lastObservedSeconds=after[-1][0]['seconds'],positivePreHitContributionObserved=True,
        settledPostHitMixedOutputEqualsNativeOnlyControl=True,settlingAllowanceSeconds='.1')

def main():
    onfolder=sync.ROOT/'audit_bounded_voice_hit_pcm_window_runtime'
    offolder=sync.ROOT/'audit_bounded_voice_hit_pcm_disabled_runtime'
    out=offolder/'convergence_check.json';assert not out.exists()
    prior=json.loads((onfolder/'pcm_window_check.json').read_text());assert prior['passed']
    assert sync.sha(onfolder/'run.log')==prior['logSHA256']
    terminal=json.loads((offolder/'terminal.json').read_text());assert terminal['exitCode']==0 and terminal['limitReason'] is None
    assert not (offolder/'stderr.log').read_text().strip()
    assert trace.scan(onfolder)['digest']==trace.scan(offolder)['digest']
    stop=json.loads((sync.ROOT/'audit_bounded_native_voice_channels_runtime/channel_stop_check.json').read_text())
    tick=Decimal(stop['ownerTiming']['predictedHealthTimerTickSeconds'])
    on,off=load(onfolder),load(offolder);result=gate(on,off,tick);faults=[]
    bad=copy.deepcopy(off);next(r for r in bad if Decimal(r['seconds'])>tick+Decimal('.1'))['sha256']='0'*64
    try:gate(on,bad,tick)
    except AssertionError:faults.append('lingering_output_difference')
    else:raise AssertionError('Output fault accepted')
    try:gate(off,off,tick)
    except AssertionError:faults.append('missing_positive_voice_contribution')
    else:raise AssertionError('Positive-control fault accepted')
    report=dict(passed=True,**result,unchangedActualGameplayAndOwnerTrace=True,
        rejectedFaults=faults,terminal=terminal,sourceSync=sync.verify(),heardCutoffAccepted=False,
        immediateSampleAccurateBoundaryAccepted=False,fullGoalComplete=False,
        logPins={str(p):sync.sha(p) for p in (onfolder/'run.log',offolder/'run.log')},checkerSHA256=sync.sha(Path(__file__)))
    out.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(dict(passed=True,**result)))

if __name__=='__main__':main()
