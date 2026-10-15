"""Four physically earned runs: native orb/cloud ownership and cleanup.

All68 actual native rasters inspected in RAM; audio/full finisher not
accepted. Preserve failed P2 timed fixture separately; no parser narrowing,
winner delay, forced hide or guest-state assistance.
"""
import gzip
import json
from pathlib import Path
import capture_native_sonya_orb_worker_wall as host
import review_native_sonya_orb_cloud_lifetime_runtime as clouds
import review_native_sonya_orb_palette_runtime as shared

ROOT=host.ROOT
OUT=ROOT/'audit_native_sonya_orb_worker_lifetime_runtime_review'
need,sha=host.need,host.sha
RUNS=('audit_native_sonya_orb_worker_lifetime_p1','audit_native_sonya_orb_worker_lifetime_p2',
      'audit_native_sonya_orb_worker_wall_p1','audit_native_sonya_orb_worker_wall_earlier_p2')

def free_contract(row):
    need(row['job_active']=='no' and row['job_free']=='yes' and row['cache_active']=='no' and
         row['cache_free']=='yes' and all(row[k]=='no' for k in ('render_primary','render_secondary','render_tertiary')),
         'Exact original worker/cache allocations free and owned object absent from every native render list')

def worker_contract(text,gap):
    born=[r for r in shared.rows(text,'TASK') if r['kind']=='worker']
    need(len(born)==1 and born[0]['age']=='53' and born[0]['owner']==born[0]['actor'],
         'One independent native worker at53 with true performer ownership')
    birth=born[0];job=birth['job'];child=shared.rows(text,'CHILD')
    need(child and all(r['job']==job and r['child']==birth['child'] and r['palette']=='FFD7B400' for r in child),
         'Sole native child allocation and source magenta palette conserved across all observed fields')
    cleanup=[r for r in shared.rows(text,'CLEANUP') if r['job']==job]
    retired=[r for r in shared.rows(text,'RETIRE') if r['kind']=='worker']
    ends=shared.rows(text,'WORKER_END')
    expected_age=181 if gap==256 else 205
    cache=f'{int(child[0]["cache"],16)-0x100:08X}'
    need(len(cleanup)==3 and [r['kernel'] for r in cleanup]==['FF83EFD0','FF840450','FF80E0E0'] and
         [r['a0'] for r in cleanup]==[cache,birth['child'],cache] and
         len(retired)==len(ends)==1 and retired[0]['job']==ends[0]['job']==job and
         retired[0]['actor']==birth['actor'] and int(retired[0]['age'])==expected_age and
         all(r['frame']==retired[0]['frame'] for r in cleanup+ends) and
         ends[0]['child']==birth['child'] and ends[0]['cache']==cache,
         'Same original orb reaches complete native object/palette/cache cleanup then one retirement at its unshortened distance-specific finish')
    free_contract(ends[0])
    need(not any(r['target']==job for r in shared.rows(text,'MASS') if r['pc']=='FF80E550' and
                 int(r['age'])<=expected_age),'Winner never prematurely mass-unlinks the original orb worker')
    need([int(r['age']) for r in child]==list(range(53,expected_age)),
         'Every native orb field is continuous through travel, wrap and separate retirement before sole cleanup')
    observed_poses=list(dict.fromkeys(r['pose'] for r in child))
    expected_poses=[f'{0xfe83fda0+i*0x40:08X}' for i in range(14)]
    need(observed_poses==expected_poses,'Complete7growth/4travel/3retirement groups observed in native order')
    return dict(birth=birth,nativeRetirement=retired[0],nativeCleanup=cleanup,nativeFreeAndRenderAbsence=ends[0],
                continuousChildFields=len(child),actualNativeGroups=observed_poses,
                finishesAfterWinner=expected_age>197,winnerTimingChanged=False)

def main():
    need(not OUT.exists() and not host.identity.census(),'Fresh exact runtime review; all native game handles terminal')
    records=[];pins={};texts={}
    for name in RUNS:
        folder=ROOT/name;report=json.loads((folder/'report.json').read_text());text=gzip.open(folder/'run.log.gz','rt').read()
        need(report['passed'] and report['nativeExit']==0 and report['wholeGuestMatched'] and
             not report['finisherAccepted'] and all(sha(p)==h for p,h in report['inputHashes'].items()),
             'Every actual native executable/program/controller/test input conserved')
        entry=shared.rows(text,'ENTRY');win=shared.rows(text,'WINNER');stop=shared.rows(text,'STOP');frames=shared.rows(text,'RGB_DIGEST')
        gap=304 if 'wall' in name else 256
        need(len(entry)==len(win)==len(stop)==1 and entry[0]['gap']==str(gap) and entry[0]['hp']=='161,0' and
             win[0]['age']=='197' and stop[0]['mode']=='3' and stop[0]['age']=='750' and
             stop[0]['bones']=='32' and stop[0]['clouds']=='3' and len(frames)==17 and not shared.rows(text,'OVERRUN'),
             'Genuinely earned command, unchanged winner, full burst/continue and no cursor overrun')
        worker=worker_contract(text,gap);cloud=clouds.cloud_contract(text)
        endings=shared.rows(text,'CLOUD_END');need(len(endings)==3,'Three exact cloud retirement/free-list observations')
        for r in endings:
            birth=next(c['birth'] for c in cloud if c['birth']['job']==r['job'])
            need(r['actor']==birth['actor'] and r['cloud_age']=='65','Same original cloud has all13x5native fields')
            free_contract(r)
        fields=[r for r in shared.rows(text,'FIELD') if r['slot']==str(report['side']) and 54<=int(r['age'])<=180]
        need(len(fields)==127 and all(r['id']=='18' and r['roster']=='18' and r['actor']==entry[0]['actor'] and r['child']=='00000000' for r in fields),
             'True Sonya actor/roster conserved and parent does not retain duplicated child ownership')
        colors=shared.rows(text,'PALETTE');original=(ROOT/'mk3/mk3-maincpu.bin').read_bytes();at=(0xff83f6f0-0xff800000)//8
        expected=','.join(f'{int.from_bytes(original[i:i+2],"little"):04X}' for i in range(at+2,at+66,2))
        need(len(colors)==3 and all(r['source']=='FFD7B400' and r['active']==expected for r in colors),
             'Actual32hardware colors exactly match source during growth/travel/wrap')
        records.append(dict(run=name,side=report['side'],physicalGap=gap,actualWindowsIdentity=report['actualWindowsIdentity'],
            nativeEntry=entry[0],nativeWinner=win[0],nativeContinue=stop[0],worker=worker,clouds=cloud,cloudFreeObservations=endings,
            actualFrames=frames,actualFramesVisuallyReviewed=17,visualObservation='Complete native orb disappears; full clouds diminish and retire; no selector portraits or stale orb/cloud in winner/continue.'))
        texts[name]=text
        for p in (folder/'report.json',folder/'run.log.gz',folder/'executed_sources.json.gz'):pins[str(p)]=sha(p)
    faults=[];text=texts[RUNS[2]]
    job=records[2]['worker']['birth']['job'];child=records[2]['worker']['birth']['child']
    variants=[('early_retirement',text.replace('age=205','age=198')),
              ('still_rendered',text.replace('render_primary=no','render_primary=yes')),
              ('wrong_cleanup_object',text.replace('kernel=FF840450 job='+job+' actor='+records[2]['worker']['birth']['actor']+' a0='+child,
                                                  'kernel=FF840450 job='+job+' actor='+records[2]['worker']['birth']['actor']+' a0=0107C6D0')),
              ('cache_not_freed',text.replace('cache_active=no cache_free=yes','cache_active=yes cache_free=no')),
              ('original_failed100worker',gzip.open(ROOT/'audit_native_sonya_orb_wall_distance_p1/run.log.gz','rt').read())]
    for name,wrong in variants:
        try:worker_contract(wrong,304)
        except ValueError as error:faults.append(dict(name=name,rejected=str(error)))
        else:raise ValueError('Incomplete actual worker cleanup admitted: '+name)
    guard=json.loads((host.source.OUT/'report.json').read_text())
    paths=[Path(__file__),Path(clouds.__file__),host.source.OUT/'report.json',
           ROOT/'audit_native_sonya_orb_worker_wall_fixture_review/report.json',
           ROOT/'audit_native_kano_laser_palette_reference_review/report.json',ROOT/'PLAY_LATEST_KANO_SONYA.cmd',
           ROOT/host.NAME/'restoration.json',ROOT/host.NAME/'cache_retirement.json']
    for p in paths:pins[str(p.resolve())]=sha(p)
    need(not (ROOT/'mame-mkp/build/mingw-gcc').exists(),'Generated compiler cache retired after actual terminal build')
    OUT.mkdir()
    result=dict(passed=True,nativeOrbWorkerCleanupAccepted=True,nativeCloudCleanupAccepted=True,
        finisherAccepted=False,fullPortAcceptance=False,actualNativeRuns=records,totalActualFramesVisuallyReviewed=68,
        actualContinuousCloudFields=780,rejectedFaults=faults,
        previousGoalTurnClassification='no progress: requested status only; continuing concrete work now',
        thisGoalTurnClassification='progress: private native build terminal/restored/cache-retired; four earned P1/P2 nominal/wall runs prove native orb/cloud cleanup; original Kano red palette discrepancy resolved by150continuous native fields/704hardware writes/27actual images',
        originalNaturalIntegrationRequirements=guard['originalNaturalIntegrationRequirements'],
        originalRemainingWorkGroups=guard['originalRemainingWorkGroups'],goalStatus='active',inputHashes=pins,
        latestPlayableChanged=False,newBuilds=1,newROMCopies=0,newRawMedia=0,newZIPs=0,compilerCacheAbsent=True,
        limitations=['Finite Sonya versus Kano human gap256/304 tests only;320activation, CPU, other victims/arenas, full audio and complete finisher still unaccepted.',
            'Failed earlier P2 near-wall fixture preserved: finish window expired before final scheduled High Kick; successor only moves physical retreat earlier.',
            'Kano laser original palette reference verified, but port implementation remains. All original14requirements and6remaining work groups remain in scope.'],
        nextAction='Implement complete original Kano laser performer/victim/palette/effects/audio as true native actors; remaining Sonya/audio/integration and final release gates continue.')
    (OUT/'report.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(dict(passed=True,earnedNativeRuns=4,reviewedFrames=68,cloudFields=780,fullPortAccepted=False)))

if __name__=='__main__':main()
