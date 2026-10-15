"""Preserve failed later selection, qualify whole initial scene, retire reviewed RAM.

Never promote the failed native trial. The original deadline/observer error
and actual wrongly confirmed opponent stay explicit. All original initial
movie/ground/stock-shadow/earned/fault gates execute on the same held capture.
"""
import gzip
import hashlib
import inspect
import json
from pathlib import Path
import run_native_current_cross_pit_render as pit
import run_native_tomb_transition_scanout_checked as later

need,sha=pit.need,pit.sha


def retire(ram,viewed):
    folder,output=ram['folder'],ram['output'];receipt=output/'cursor_initialization_race_preservation_and_ram_retirement.json'
    need(not receipt.exists()and not pit.census.census(),'Exact terminal native, fresh preservation only')
    report=json.loads((output/'report.json').read_text());meta=json.loads((folder/'result.json').read_text())
    need(not report['passed']and meta==json.loads(json.dumps(ram['terminal']))and
         meta['exit_code']==0 and not meta['modelErrors']and meta['observedRGBFields']==meta['modelExactFields']==677 and
         meta['ramGuestSHA256']==hashlib.sha256(ram['guest']).hexdigest().upper(),
         'Actual failed whole trial and complete initial677-field native model, no relabelling')
    text=gzip.open(folder/'run.log.gz','rt').read();stderr=(folder/'stderr.log').read_text()
    need('whole3594_Tomb_then_physical_paid_rejoin:188: assertion failed!'in stderr and
         'MK2_TOMB_REJOIN_SELECT frame=29629 writes=0 assistance=none slot=2 target=18 route=\n'in text and
         'MK2_TOMB_REJOIN_SELECT_ID frame=29775 writes=0 assistance=none slot=2 actual=9 target=18'in text and
         'MK2_TOMB_REJOIN_DEADLINE frame=32026 writes=0 assistance=none admitted=-1'in text and
         'MK2_STAGE_RESULT frame=32027'in text,
         'Actual empty route, wrong native confirmation, missing intended admission and normal deadline terminal')
    records,states=ram['post_records'],ram['post_states'];scene=ram['scene']
    need(json.loads((folder/'continuous_scene_records.json').read_text())==scene.records and
         json.loads((folder/'post_scene_records.json').read_text())==records and
         json.loads((folder/'post_state_records.json').read_text())==states and
         json.loads((folder/'post_buffer_digests.json').read_text())==ram['post_transport'].records and
         not scene.raw and not scene.rgb and not scene.events and not ram['post_raw']and not ram['post_failures'],
         'All original initial and later native records/transport retained exactly')
    need(len(records)==len(states)==2923 and [r['frame']for r in records]==list(range(29104,32027)),
         'Entire actual failed later chronology, including deadline')
    for s,r in zip(states,records,strict=True):
        t=r['timing'];start=(t['dpyadr']+(t['vsblnk']-t['veblnk'])*(t['control']&0x03fc))&0xffff
        need(s=={k:r[k]for k in s}and r['passed']and r['pixels']==101600 and
             r['nativeDPYADRSourceDefinedAddressOnly']and r['currentVRAMNeverSelectedAsPassingTarget']and
             r['effectiveNativeStart']==start and t['vcount']==t['vsblnk']-1 and t['vsblnk']-t['veblnk']==254 and
             t['control']&0x03fc==16,'Every failed-trial native pixel still bound to source-defined scanout')
    rejected=None
    try:later.verify_rejoin(text,records,states,[17,18])
    except ValueError as error:rejected=str(error)
    need(rejected=='No failed deadline or native observer errors','Original complete positive gate rejects this actual trial')
    contract=pit.contract.scene_contract
    body=pit.contract.executed.source
    before=" need([s for s in log.splitlines()if s.startswith(physical)]==\n      [s for s in previous.splitlines()if s.startswith(physical)],\n      'Entire independent enabled-audio physical paid selection/health/KO/action/cleanup trajectory')"
    need(body.count(before)==1 and contract.__code__.co_code==pit.contract.executed.scene_contract.__code__.co_code,
         'Whole declared initial Pit contract, only independently exact later terminal difference')
    body=body.replace(before,' physical_extension(log,previous,physical)',1)
    namespace=dict(contract.__globals__,physical_extension=later.physical_extension)
    exec(compile(body,__file__+'::entire_original_initial_Pit_movie_floor_stock_shadow_and_faults','exec'),namespace)
    reference=next(c for c in ram['historical']['cases']if c['fighter']=='kano'and c['physicalSlot']==1)['capture']
    payload=(pit.ROOT/meta['candidate']/'roms/mk2ks/mk2ks.mdata').read_bytes()
    initial=namespace['scene_contract'](scene,text,ram['guest'],payload,'kano',1,Path(reference),(17,18))
    need(initial['passed']and initial['nativeState']['earned_matches']==7 and len(initial['actualMovieFaultsRejected'])==31 and
         len(initial['actualEarnedFaultsRejected'])==12 and len(initial['actualNativePhaseGroundFaultsRejected'])==6 and
         len(initial['actualNativePitShadowPolicy']['actualShadowPolicyFaultsRejected'])==5,
         'Whole original initial scene executes every original native/fault gate; not later rejoin acceptance')
    boundary=[r for r in states if 29626<=r['frame']<=29634]
    need([(r['frame'],r['mode'],r['state2'],r['roster2'])for r in boundary[:4]]==
         [(29626,3,2,18),(29627,3,2,18),(29628,4,3,18),(29629,4,3,9)],
         'Actual previous18 read precedes native cursor9 initialization, not a human-selected Sonya substitution')
    images=ram['review_images'];ledger={r['frame']:r for r in scene.records};ledger.update({r['frame']:r for r in records})
    need(len(viewed)==len(set(viewed))==len(images)==57 and set(viewed)==set(images),'Every actual held raster inspected now')
    views=[]
    for frame,rgb in sorted(images.items()):
        digest=hashlib.sha256(rgb.tobytes()).hexdigest().upper()
        need(rgb.shape==(254,400,3)and digest==ledger[frame]['rgbSHA256'],'Every reviewed raster bound to exact original field')
        views.append(dict(frame=frame,rgbSHA256=digest,individuallyViewedNow=True))
    pins=dict(meta['input_hashes']);pins.update(ram['extensionSourceHashes'])
    for p in(Path(__file__).resolve(),Path(pit.__file__),Path(later.__file__),output/'report.json',
             *(p for p in folder.rglob('*')if p.is_file())):pins[str(p)]=sha(p)
    need(all(sha(p)==h for p,h in pins.items()),'Entire actual failed source/native/log/record evidence unchanged')
    need(not any(p.suffix.lower()in('.png','.wav','.bin','.zip','.exe')for p in folder.rglob('*')if p.is_file()),'No raw native copies')
    identity=json.loads((folder/'native_identity.json').read_text())
    need(identity==ram['identity']and identity['ProcessId']==json.loads((folder/'process.json').read_text())['pid'],
         'Exact original native birth/path/parent/command')
    proof=dict(passed=True,preservationAndRAMRetirementOnly=True,fullOriginalTrialAccepted=False,
               originalPositiveRejoinGateRejectedBy=rejected,exactTerminalNativeIdentity=identity,
               actualInitialFullPitScene=initial,initialIndependentFields=677,laterSourceDefinedNativeFields=2923,
               laterSourceDefinedNativeRGBPixels=2923*101600,actualCursorInitializationBoundary=boundary,
               actualWronglyConfirmedOpponent=9,intendedOpponent=18,actualIntendedAdmission=False,
               nativeObserverError=stderr.strip(),individuallyReviewedFields=views,
               actualVisualObservations='Own Sonya Pit movie clears via normal shutters/continue. Native CSS initializes P2 on Reptile; driver never moves that cursor, confirms Reptile, and Battle8 correctly shows Kano/Reptile. Selection icons/poses clear before Portal entry, actual Kano floor shadow/name shadow present. This is NOT Sonya rejoin acceptance.',
               fullPortAcceptance=False,goalStatus='active',publicPlayableChanged=False,inputHashes=pins)
    ram['server'].shutdown();ram['server'].server_close()
    for key in('images','post_images','review_images'):ram[key].clear()
    ram.clear();proof.update(originalNativeRasterBuffersReleased=57,reviewServerClosed=True,originalCaptureRAMDictionaryCleared=not ram)
    receipt.write_text(json.dumps(proof,indent=2)+'\n')
    print(json.dumps(dict(passed=True,preservationOnly=True,releasedRasters=57,receipt=str(receipt)),indent=2),flush=True)
    return proof
