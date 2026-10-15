"""Both blocked rings, native round history, exact87 callbacks/eight real views."""
import copy,inspect,json,sys
from pathlib import Path
import capture_native_selector_cpu_sonya_continuous_guard_layout as capture
import qualify_native_selector_cpu_guard_checkpoint as prior

ROOT,need,sha=capture.ROOT,capture.need,capture.sha
OUT=ROOT/'audit_native_selector_cpu_sonya_continuous_checkpoint_checked'


def image_gate(scenes,images,text):
    source=inspect.getsource(prior.image_gate)
    need(source.count('177')==2,'Only original native callback cardinality differs')
    source=source.replace('177','87')
    scope=dict(vars(prior),__file__=__file__)
    exec(compile(source,__file__+'::whole_original_callback_pixels_actual87','exec'),scope)
    return scope['image_gate'](scenes,images,text)


def execute(state,reviewed,view_native,view_host):
    need(not OUT.exists()and not capture.original.original.prior.prior.current.prior.identity.census(),
         'Same terminal game and original retained host; no native replay')
    folder,text,images=capture.RAM_CASES[capture.KEY]
    meta=json.loads((folder/'result.json').read_text());held=capture.NATIVE_HANDLES[capture.KEY]
    host=next(r for r in prior.identities.census_hosts()if r['ProcessId']==38752)
    need(host==view_host and (host['ParentProcessId'],host['createdUnix'])==(40316,1791734919.6266766)and
         host['CommandLine']=='"'+sys.executable+'" -B tools/capture_native_selector_special_shadow.py'and
         not meta['passed']and meta['error']=="ValueError(\"invalid literal for int() with base 10: 'continuous_guard'\")"and
         meta['nativeExit']==held['process'].poll()==0 and
         held['identity']==view_native==meta['nativeTerminal']['actualWindowsIdentity']and
         (view_native['ProcessId'],view_native['ParentProcessId'],view_native['createdUnix'])==
         (38512,38752,1791743126.3305721)and not meta['nativeTerminal']['hostDecodeErrors'],
         'Exact host/native kernel identity and terminal handle; original parser rejection remains false')
    positive=image_gate(meta['actualScenes'],images,text)
    need(len(reviewed)==8 and {r['index']for r in reviewed}=={21,24,28,33,35,38,66,85},
         'Exactly eight ACTUALLY inspected original flight/impact/clear and completed leg fields')
    by={p['index']:p for p in positive['exactPixelDigestProofs']}
    for r in reviewed:
        need(r['header']==meta['actualScenes'][r['index']]and r['SHA256']==by[r['index']]['SHA256']and
             r['nativeRGBSHA256']==by[r['index']]['nativeRGBSHA256']and r['actualReconstructedAlpha']==255 and
             r['identityRevalidatedBeforeAndAfter'],'Actually reviewed pixels bind exact original callback and live retained host')
    faults=[]
    for label in('callback_ordinal','native_frame','native_pixel_digest','actual_pixel_corruption'):
        changed=copy.deepcopy(meta['actualScenes']);changed_images=images
        if label=='callback_ordinal':changed[0]['callbackOrdinal']=1
        elif label=='native_frame':changed[0]['frame']+=1
        elif label=='native_pixel_digest':changed[0]['sha256']='0'*64
        else:
            changed_images=dict(images);key=changed[0]['imageKey'];changed_images[key]=images[key].copy()
            changed_images[key][0,0,0]^=1
        try:image_gate(changed,changed_images,text)
        except(ValueError,AssertionError)as error:faults.append(dict(fault=label,rejectedBy=str(error)))
        else:raise ValueError('Actual callback/pixel corruption admitted '+label)
    need(image_gate(meta['actualScenes'],images,text)==positive,'Entire exact original pixel positive restored')
    mechanics_path=ROOT/'audit_native_selector_cpu_sonya_continuous_ring_checked/report.json'
    mechanics=json.loads(mechanics_path.read_text())
    need(mechanics['passed']and mechanics['sameOriginalTerminalNativePID']==38512 and
         len(mechanics['actualFaultsRejected'])==23 and
         all(sha(p)==h for p,h in mechanics['inputHashes'].items()),'Whole same-game blocked-ring/native-pool/leg receipt unchanged')
    previous_path=ROOT/'audit_native_selector_cpu_startup_guard_checkpoint_checked/report.json'
    previous=json.loads(previous_path.read_text())
    need(previous['passed']and previous['goalStatus']=='active','Original full14 requirements and six remaining groups retained')
    pins=dict(mechanics['inputHashes'])
    for path in(Path(__file__),Path(prior.__file__),mechanics_path,previous_path,
                ROOT/'tools/read_native_selector_cpu_sonya_continuous_frames.py',
                ROOT/'tools/read_native_selector_cpu_sonya_continuous_frames_remote.py'):
        pins[str(path.resolve())]=sha(path)
    need(all(sha(p)==h for p,h in pins.items()),'Whole exact executed/read immutable inventory')
    OUT.mkdir();value=dict(passed=True,candidate=meta['candidate'],goalStatus='active',nativeIdentity=view_native,
        actualLiveRetainedHostIdentity=host,actualBlockedRingsAndPoolReceipt=str(mechanics_path),
        completeCallbackPixels=positive,actuallyReviewedNativeFields=reviewed,callbackPixelFaultsRejected=faults,
        totalCurrentRingLifetimePixelFaults=27,requirements=previous['requirements'],remainingGroups=previous['remainingGroups'],
        originalPolicyTokenCaptureRemainsRejected=True,initialFirstRoundProjectileAccepted=False,
        allCPUContextsArenasAccepted=False,fullBodyShadowArtAudioAcceptance=False,fullPortAcceptance=False,
        publicPlayableChanged=False,newNativeGames=0,newBuilds=0,newROMCopies=0,newRawMedia=0,newZIPs=0,
        previousGoalTurnClassification='no progress: status answer only',
        thisGoalTurnClassification='progress: distinct actual continuous physical guard; two genuinely blocked rings, native pool lifetimes and two completed legs,87 callback pixels and eight actual views',
        nextAction='First-round startup child ownership; other victims/slots/arenas, projectile audio, finishers/campaign/morph and final public release',
        inputHashes=pins)
    capture.original.original.prior.prior.current.prior.save(OUT/'report.json',value)
    print('PASS actual blocked rings/native pool,87 callback pixels/eight reviewed fields/27 faults',flush=True)
    return value
