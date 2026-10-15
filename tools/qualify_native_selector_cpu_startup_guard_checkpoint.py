"""Same actual blocked-knife trial:120 callback pixel proofs/eight viewed fields.

Keep the complete native knife/pool lifetime receipt and its31 actual faults.
Pixel transport is not full artistic, all-arena or PCM acceptance. First-round
startup child ownership and every other original goal requirement remain open.
"""
import copy,inspect,json,sys
from pathlib import Path
import numpy as np
import capture_native_selector_cpu_startup_guard as capture
import qualify_native_selector_cpu_guard_checkpoint as prior

ROOT,need,sha=capture.ROOT,capture.need,capture.sha
OUT=ROOT/'audit_native_selector_cpu_startup_guard_checkpoint_checked'


def image_gate(scenes,images,text):
    source=inspect.getsource(prior.image_gate)
    need(source.count('177')==2,'Only actual callback cardinality changes; whole pixel model retained')
    source=source.replace('177','120')
    scope=dict(vars(prior),__file__=__file__)
    exec(compile(source,__file__+'::whole_original_callback_pixel_gate_actual120','exec'),scope)
    return scope['image_gate'](scenes,images,text)


def execute(state,reviewed,view_native,view_host):
    need(not OUT.exists()and not capture.prior.prior.current.prior.identity.census(),
         'Same original native terminal, no replay')
    folder,text,images=capture.RAM_CASES[capture.KEY]
    meta=json.loads((folder/'result.json').read_text());held=capture.NATIVE_HANDLES[capture.KEY]
    host=next(r for r in prior.identities.census_hosts()if r['ProcessId']==38752)
    need(host==view_host and host['ParentProcessId']==40316 and host['createdUnix']==1791734919.6266766 and
         host['CommandLine']=='"'+sys.executable+'" -B tools/capture_native_selector_special_shadow.py'and
         meta['passed']and meta['nativeExit']==held['process'].poll()==0 and
         held['identity']==view_native==meta['nativeTerminal']['actualWindowsIdentity']and
         (view_native['ProcessId'],view_native['ParentProcessId'],view_native['createdUnix'])==
         (39784,38752,1791740868.5522785)and not meta['nativeTerminal']['hostDecodeErrors'],
         'Exact original host/native kernel identity and terminal handle before/after passive raster viewing')
    positive=image_gate(meta['actualScenes'],images,text)
    need(len(reviewed)==8 and {r['index']for r in reviewed}==set(range(107,115)),
         'Exactly eight ACTUALLY inspected native launch/flight/impact/recovery/clear fields')
    by={p['index']:p for p in positive['exactPixelDigestProofs']}
    for r in reviewed:
        need(r['header']==meta['actualScenes'][r['index']]and
             r['SHA256']==by[r['index']]['SHA256']and r['nativeRGBSHA256']==by[r['index']]['nativeRGBSHA256']and
             r['actualReconstructedAlpha']==255 and r['identityRevalidatedBeforeAndAfter'],
             'Actually viewed complete native callback pixels/header/digest under original host')
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
        else:raise ValueError('Actual callback/pixel fault admitted '+label)
    need(image_gate(meta['actualScenes'],images,text)==positive,'Entire exact pixel positive restored')
    mechanics_path=ROOT/'audit_native_selector_cpu_startup_guard_knife_checked/report.json'
    mechanics=json.loads(mechanics_path.read_text())
    need(mechanics['passed']and mechanics['sameOriginalTerminalNativePID']==39784 and
         len(mechanics['actualFaultsRejected'])==31 and
         all(sha(p)==h for p,h in mechanics['inputHashes'].items()),
         'Same original full knife and allocated-pool lifetime gate, all31 faults unchanged')
    previous_path=ROOT/'audit_native_selector_cpu_guard_checkpoint_checked/report.json'
    previous=json.loads(previous_path.read_text())
    need(previous['passed']and previous['goalStatus']=='active','Original full goal scope retained')
    pins=dict(mechanics['inputHashes'])
    for path in(Path(__file__),Path(prior.__file__),mechanics_path,previous_path,
                ROOT/'tools/read_native_selector_cpu_startup_guard_frames.py',
                ROOT/'tools/read_native_selector_cpu_startup_guard_frames_remote.py'):
        pins[str(path.resolve())]=sha(path)
    need(all(sha(p)==h for p,h in pins.items()),'Whole executed/read inventories unchanged')
    OUT.mkdir();value=dict(passed=True,candidate=meta['candidate'],goalStatus='active',
        nativeIdentity=view_native,actualLiveRetainedHostIdentity=host,
        actualBlockedKnifeAndPoolReceipt=str(mechanics_path),completeCallbackPixels=positive,
        actuallyReviewedNativeFields=reviewed,callbackPixelFaultsRejected=faults,
        totalCurrentKnifeLifetimePixelFaults=35,requirements=previous['requirements'],
        remainingGroups=previous['remainingGroups'],initialFirstRoundProjectileAccepted=False,
        allCPUContextsArenasAccepted=False,fullArtAudioAcceptance=False,fullPortAcceptance=False,
        publicPlayableChanged=False,newNativeGames=0,newBuilds=0,newROMCopies=0,newRawMedia=0,newZIPs=0,
        previousGoalTurnClassification='no progress: status answer only',
        thisGoalTurnClassification='progress: distinct real guard-from-start native run; actual blocked knife/pool lifetime, all120 callback pixels and eight reviewed fields',
        nextAction='First-round startup projectile ownership; blocked Sonya ring/other victims/slots/arenas and projectile audio',
        inputHashes=pins)
    capture.prior.prior.current.prior.save(OUT/'report.json',value)
    print('PASS current blocked knife/pool/120 callback pixels/eight reviewed fields/35 faults',flush=True)
    return value
