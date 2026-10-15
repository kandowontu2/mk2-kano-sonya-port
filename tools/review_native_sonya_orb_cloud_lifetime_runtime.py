"""Actual P1/P2 cloud cleanup and longer-distance worker failure, separately.

51 full native frames actually inspected in RAM. The attempted320fixture
only reached304physically and never activated; its successful transport is
not gameplay acceptance. No narrowed parser limit, forced hide or winner
delay. Preserve every executed source/test/build before the next repair.
"""
import gzip
import json
from pathlib import Path
import qualify_native_sonya_orb_cloud_lifetime as source
import review_native_sonya_orb_palette_runtime as shared

ROOT=source.ROOT
OUT=ROOT/'audit_native_sonya_orb_cloud_lifetime_runtime_review'
need,sha=source.need,source.sha
RUNS=('audit_native_sonya_orb_cloud_lifetime_p1','audit_native_sonya_orb_cloud_lifetime_p2','audit_native_sonya_orb_wall_distance_p1')

def cloud_contract(text):
    born=[r for r in shared.rows(text,'TASK') if r['kind']=='smoke']
    fields=shared.rows(text,'CLOUD_FIELD');cleanup=shared.rows(text,'CLEANUP');retired=shared.rows(text,'RETIRE')
    need(len(born)==3 and len(fields)==195,'Exactly three independent clouds, each65consecutive actual native fields')
    result=[]
    for birth in born:
        job=birth['job'];observed=[r for r in fields if r['job']==job]
        need(len(observed)==65 and [int(r['cloud_age']) for r in observed]==list(range(65)),
             'Every cloud field observed continuously, including after native winner')
        for i,r in enumerate(observed):
            group=i//5
            need(r['actor']==birth['actor'] and r['type']=='0201' and r['cache_type']=='0109' and
                 r['pose']==f'{0xffd6f200+group*0x60:08X}' and r['cursor']==f'{0xffd6f820+group*0x20:08X}' and
                 r['active']=='yes' and r['free']=='no','Every actual full13x5 group/cursor/actor/category/cache and active allocation matches native sequence')
        own_cleanup=[r for r in cleanup if r['job']==job]
        own_retire=[r for r in retired if r['kind']=='smoke' and r['job']==job]
        need(len(own_cleanup)==2 and [r['kernel'] for r in own_cleanup]==['FF840450','FF80E0E0'] and
             own_cleanup[0]['a0']==birth['actor'] and own_cleanup[1]['a0']==observed[-1]['cache'] and
             len(own_retire)==1 and own_retire[0]['actor']==birth['actor'] and
             int(own_retire[0]['frame'])==int(birth['frame'])+65 and
             all(r['frame']==own_retire[0]['frame'] for r in own_cleanup),
             'Same original cloud allocation reaches owned object/palette cleanup, exact cache-process free, then one native retirement at field65')
        need(not any(r['target']==job for r in shared.rows(text,'MASS') if r['pc']=='FF80E550' and int(r['age'])<int(own_retire[0]['age'])),
             'Winner does not prematurely mass-unlink any live independent cloud')
        result.append(dict(birth=birth,groups=13,fieldsPerGroup=5,nativeFields=65,
                           afterWinnerStillActive=True,ownedCleanup=own_cleanup,retirement=own_retire[0]))
    return result

def worker_failure(text):
    birth=[r for r in shared.rows(text,'TASK') if r['kind']=='worker']
    need(len(birth)==1,'One actual long-distance worker allocation')
    job=birth[0]['job'];mass=[r for r in shared.rows(text,'MASS') if r['pc']=='FF80E550' and r['known']=='worker']
    need(len(mass)==1 and mass[0]['target']==job and mass[0]['age']=='198' and mass[0]['type']=='0100' and
         mass[0]['match']=='00000100' and mass[0]['mask']=='FFFFFFFF' and mass[0]['active']=='yes' and mass[0]['free']=='no',
         'Actual winner deletes the same still-active worker at198, not a reused allocation or inferred timeout')
    need(not any(r['job']==job for r in shared.rows(text,'CLEANUP')) and
         not any(r['job']==job and r['kind']=='worker' for r in shared.rows(text,'RETIRE')),
         'Original long-distance worker never reaches owned orb cleanup/retirement')
    child=[r for r in shared.rows(text,'CHILD') if r['job']==job and r['age']in('197','198','199','220')]
    need(len(child)==4 and all(r['child']==birth[0]['child'] and r['pose']=='FE8400A0' and
         r['palette']=='FFD7B400' and r['cache']==child[0]['cache'] for r in child),
         'Last orb retirement group/object/cache remains unchanged beyond premature worker deletion')
    return dict(birth=birth,actualPrematureMassUnlink=mass[0],actualLingeringChild=child,
        workerCleanupAccepted=False,actualRasterObservation='Magenta orb remains at280,450,600; clouds complete and clear independently.')

def main():
    need(not OUT.exists() and not source.prior.prior.prior.prior.visual.native.census(),'Fresh evidence; all same native handles actually terminal')
    OUT.mkdir();records=[];pins={}
    for name in RUNS:
        folder=ROOT/name;report=json.loads((folder/'report.json').read_text());text=gzip.open(folder/'run.log.gz','rt').read()
        need(report['passed'] and report['transportOnlyAccepted'] and report['nativeExit']==0 and report['wholeGuestMatched'] and
             not report['finisherAccepted'] and all(sha(p)==h for p,h in report['inputHashes'].items()),'Every actual earned native trace and executed input preserved')
        entry=shared.rows(text,'ENTRY');win=shared.rows(text,'WINNER');stop=shared.rows(text,'STOP');frames=shared.rows(text,'RGB_DIGEST')
        need(len(entry)==len(win)==len(stop)==1 and win[0]['age']=='197' and stop[0]['mode']=='3' and
             stop[0]['bones']=='32' and stop[0]['clouds']=='3' and len(frames)==17 and not shared.rows(text,'OVERRUN'),
             'True earned action, normal native win/continue, complete frames and no old cursor overrun')
        need(entry[0]['gap']==('304' if name.endswith('distance_p1') else '256'),'Actual physical distance, never injected actor coordinates')
        clouds=cloud_contract(text)
        worker=[r for r in shared.rows(text,'TASK') if r['kind']=='worker'][0]
        if name.endswith('distance_p1'):failure=worker_failure(text)
        else:
            retired=[r for r in shared.rows(text,'RETIRE') if r['kind']=='worker']
            need(len(retired)==1 and int(retired[0]['age'])in(180,181),'Middle-distance orb worker retires normally before winner')
        records.append(dict(run=name,physicalSlot=report['side'],nativeIdentity=report['actualWindowsIdentity'],entry=entry[0],
            nativeWinner=win[0],nativeContinue=stop[0],clouds=clouds,actualFrames=frames,actualFramesVisuallyReviewed=17,
            cloudAnimationAndNativeCleanupCallsAccepted=True,wholeFinisherAccepted=False))
        for p in (folder/'report.json',folder/'run.log.gz',folder/'executed_sources.json.gz'):pins[str(p)]=sha(p)
    attempted=ROOT/'audit_native_sonya_orb_max_distance_p1';attempt_report=json.loads((attempted/'report.json').read_text())
    text=gzip.open(attempted/'run.log.gz','rt').read();combat=shared.rows(text,'COMBAT')
    need(attempt_report['passed'] and attempt_report['nativeExit']==0 and attempt_report['nativeRGBFrames']==0 and
         not shared.rows(text,'ENTRY') and not shared.rows(text,'COMMAND_READY') and
         max(int(r['gap']) for r in combat if r['flag']=='3')==304 and
         all(sha(p)==h for p,h in attempt_report['inputHashes'].items()),'Attempted320fixture actually hits304wall bound and never issues finish command; transport green is not finisher proof')
    fixture=dict(run=attempted.name,requestedGap=320,actualMaximumObservedGap=304,commandIssued=False,
                 nativeExit=0,gameplayAccepted=False,actualFrames=0,interpretation='Fixture wall bound, not evidence of parser rejection; full208..320input range remains unchanged.')
    for p in (attempted/'report.json',attempted/'run.log.gz',attempted/'executed_sources.json.gz'):pins[str(p)]=sha(p)
    faults=[];text=gzip.open(ROOT/RUNS[0]/'run.log.gz','rt').read()
    for name,wrong in [('unsafe_cloud_category',text.replace('type=0201','type=0100')),
        ('early_retirement',text.replace('frame=3293 side=1 age=235','frame=3292 side=1 age=234')),
        ('wrong_cleanup_actor',text.replace('a0=01030030','a0=0107C6D0'))]:
        try:cloud_contract(wrong)
        except ValueError as error:faults.append(dict(name=name,rejected=str(error)))
        else:raise ValueError('Unsafe/incomplete actual cloud cleanup admitted: '+name)
    receipt=json.loads((source.OUT/'report.json').read_text())
    for p in (Path(__file__),source.OUT/'report.json',ROOT/'PLAY_LATEST_KANO_SONYA.cmd'):pins[str(p)]=sha(p)
    result=dict(passed=True,nativeFiniteCloudLifetimeAccepted=True,finisherAccepted=False,fullPortAcceptance=False,
        previousGoalTurnClassification='progress: actual three-cloud winner unlink proved; native201 cloud immediate source-qualified and one private build launched',
        thisGoalTurnClassification='progress: private compile terminal/restored/cache-retired;51actualP1/P2/wall-distance frames checked; complete cloud13x5/cleanup proven; real304pixel worker still killed at198 and orb left behind',
        actualNativeRuns=records,totalActualFramesVisuallyReviewed=51,wallFixtureNonActivation=fixture,
        actualRemainingWorkerFailure=failure,actualCloudFaultsRejected=faults,
        originalNaturalIntegrationRequirements=receipt['originalNaturalIntegrationRequirements'],
        originalRemainingWorkGroups=receipt['originalRemainingWorkGroups'],goalStatus='active',inputHashes=pins,
        latestPlayableChanged=False,newBuilds=1,newROMCopies=0,newRawMedia=0,newZIPs=0,compilerCacheAbsent=True,
        limitations=['Native cloud gate only. Full Sonya finisher, long-distance worker cleanup, original audio, CPU/other victims/arena and full release gates remain unaccepted.',
            '304 is this fixture wall bound, not a new parser maximum. No320native activation proof.',
            'Native cache/object cleanup calls observed with correct pointers and normal visual retirement; no wider subsequent join/reset acceptance.'],
        nextAction='Give independent orb worker native201 lifetime as well, conserving all choreography and winner timing; private build and earned near-wall/both-slot cleanup tests, then remaining full integration/audio/Kano laser/release gates.')
    (OUT/'report.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(dict(passed=True,cloudNativeFields=390,reviewedFrames=51,workerFailureAtActualGap=304,finisherAccepted=False)))

if __name__=='__main__':main()
