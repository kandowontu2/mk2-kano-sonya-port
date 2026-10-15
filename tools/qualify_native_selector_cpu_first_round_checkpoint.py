"""Original first-round knife: full142 callback pixels/eight actual views.

Keep original initial-entry, owned knife and native pool/source-facing rules.
The impact smoke visible after primary child retirement is NOT claimed cleared.
Full14 requirements/six groups and public release remain open.
"""
import copy,inspect,json,sys
from pathlib import Path
import qualify_native_selector_cpu_startup_guard_checkpoint as prior
import capture_native_selector_cpu_first_round_projectile as capture

ROOT,need,sha=capture.ROOT,capture.need,capture.sha
OUT=ROOT/'audit_native_selector_cpu_first_round_checkpoint_checked'


def image_gate(scenes,images,text):
    source=inspect.getsource(prior.prior.image_gate)
    need(source.count('177')==2,'Only actual callback cardinality changes')
    scope=dict(vars(prior.prior),__file__=__file__)
    exec(compile(source.replace('177','142'),__file__+'::whole142_native_pixels','exec'),scope)
    return scope['image_gate'](scenes,images,text)


def execute(state,reviewed,view_native,view_host):
    need(not OUT.exists()and not capture.prior.prior.current.prior.identity.census(),
         'Same terminal original game; no native replay')
    folder,text,images=capture.RAM_CASES[capture.KEY]
    meta=json.loads((folder/'result.json').read_text());held=capture.NATIVE_HANDLES[capture.KEY]
    host=next(r for r in prior.prior.identities.census_hosts()if r['ProcessId']==38752)
    need(host==view_host and host['ParentProcessId']==40316 and host['createdUnix']==1791734919.6266766 and
         host['CommandLine']=='"'+sys.executable+'" -B tools/capture_native_selector_special_shadow.py'and
         held['identity']==view_native==meta['nativeTerminal']['actualWindowsIdentity']and
         (view_native['ProcessId'],view_native['ParentProcessId'],view_native['createdUnix'])==
         (44324,38752,1791744064.988737)and
         meta['passed']and meta['nativeExit']==held['process'].poll()==0 and not meta['nativeTerminal']['hostDecodeErrors'],
         'Exact original host/kernel native identity and terminal0, before and after actual viewing')
    positive=image_gate(meta['actualScenes'],images,text)
    need(len(reviewed)==8 and {r['index']for r in reviewed}=={3,7,13,15,17,20,22,26},
         'Eight ACTUALLY inspected original entry/intro/hit/impact/retirement/recovery views')
    by={r['index']:r for r in positive['exactPixelDigestProofs']}
    for r in reviewed:
        need(r['header']==meta['actualScenes'][r['index']]and
             all(r[k]==by[r['index']][k]for k in('SHA256','nativeRGBSHA256'))and
             r['actualReconstructedAlpha']==255 and r['identityRevalidatedBeforeAndAfter'],
             'Every actually reviewed whole pixel block/header binds original callback')
    faults=[]
    for label in('callback_ordinal','native_frame','native_pixel_digest','actual_pixel_corruption'):
        altered=copy.deepcopy(meta['actualScenes']);changed=images
        if label=='callback_ordinal':altered[0]['callbackOrdinal']=1
        elif label=='native_frame':altered[0]['frame']+=1
        elif label=='native_pixel_digest':altered[0]['sha256']='0'*64
        else:
            changed=dict(images);key=altered[0]['imageKey'];changed[key]=images[key].copy();changed[key][0,0,0]^=1
        try:image_gate(altered,changed,text)
        except(AssertionError,ValueError)as error:faults.append(dict(fault=label,rejectedBy=str(error)))
        else:raise ValueError('Actual callback/pixel fault admitted '+label)
    need(image_gate(meta['actualScenes'],images,text)==positive,'Whole unmodified actual pixel positive restored')
    mechanics_path=ROOT/'audit_native_selector_cpu_first_round_knife_facing_checked/report.json'
    mechanics=json.loads(mechanics_path.read_text())
    need(mechanics['passed']and mechanics['sameOriginalTerminalNativePID']==44324 and
         mechanics['actualNativeIdentity']==view_native and len(mechanics['actualFaultsRejected'])==37 and
         all(sha(p)==h for p,h in mechanics['inputHashes'].items()),
         'Same original entire first-round knife/source-derived facing/native pool gate and37 actual faults')
    previous_path=ROOT/'audit_native_selector_cpu_sonya_continuous_checkpoint_checked/report.json'
    previous=json.loads(previous_path.read_text())
    need(previous['passed']and len(previous['requirements'])==14 and len(previous['remainingGroups'])==6,
         'Original full goal scope remains active')
    pins=dict(mechanics['inputHashes'])
    for path in(Path(__file__),Path(prior.__file__),Path(prior.prior.__file__),mechanics_path,previous_path,
        ROOT/'tools/read_native_selector_cpu_first_round_frames.py',
        ROOT/'tools/read_native_selector_cpu_first_round_frames_remote.py',
        ROOT/'mame-mkp/src/mame/midway/midtunit_m.cpp',ROOT/'mame-mkp/src/mame/midway/midtunit.cpp',
        ROOT/'mame-mkp/src/mame/midway/midtunit.h',ROOT/'PLAY_LATEST_KANO_SONYA.cmd',
        ROOT/'release_v5986_current_playtest/MK2_Kano_Sonya_v5219_CURRENT_PLAYTEST.zip'):
        pins[str(path.resolve())]=sha(path)
    need(all(sha(p)==h for p,h in pins.items()),'Complete authoritative inputs unchanged')
    OUT.mkdir();report=dict(passed=True,goalStatus='active',nativeIdentity=view_native,
        actualLiveRetainedHostIdentity=host,completeCallbackPixels=positive,actuallyReviewedNativeFields=reviewed,
        wholeFirstRoundKnifePoolFacingReceipt=str(mechanics_path),callbackPixelFaultsRejected=faults,
        totalCurrentFirstRoundFaults=41,requirements=previous['requirements'],remainingGroups=previous['remainingGroups'],
        actualViewedFloorShadowsAndShadowedKanoNames=True,largeCSSPortraitPoseLeaksVisible=False,
        impactParticlesStillVisibleAfterPrimaryRetirement=True,allImpactParticleCleanupAccepted=False,
        allStartupContextsSlotsArenasAccepted=False,fullArtAudioAcceptance=False,fullPortAcceptance=False,
        previousGoalTurnClassification='no progress: status answer only',
        thisGoalTurnClassification='progress: same captured first-round native knife source-facing/pool qualification and actual pixel review',
        nextAction='Capture current native projectile PCM and source ownership; other contexts/arenas/finishers/campaign/morph/endings/final release',
        publicPlayableChanged=False,newNativeGames=0,newBuilds=0,newROMCopies=0,newRawMedia=0,newZIPs=0,inputHashes=pins)
    capture.prior.prior.current.prior.save(OUT/'report.json',report)
    print('PASS original first-round knife/pool/source-facing, all142 callback pixels/eight views/41 faults; full goal active',flush=True)
    return report
