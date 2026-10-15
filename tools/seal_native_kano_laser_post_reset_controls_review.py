"""Actual same-job next-round controls, CPU paired move, bodies and shadows.

Twelve new native rasters individually inspected;21 earlier native rasters
match SHA256 of previously inspected same-candidate backing. Do not claim
old unavailable buffers byte-compared, broad CPU/arena/PCM or full port done.
"""
import hashlib
import json
from pathlib import Path
import verify_native_kano_laser_post_reset_body_complete_fields as bodies
import verify_native_kano_laser_post_reset_controls_complete_fields as controls

ROOT,need,sha,base=bodies.ROOT,bodies.need,bodies.prior.sha,bodies.base
OUT=ROOT/'audit_native_kano_laser_post_reset_controls_review'
CTRL=[2874,2895,3025,3043,3103,3163]
CPU=[3125,3155,3159,3163,3167,3219]


def run(actual):
    need(not OUT.exists()and not base.identity.census(),'Same native job terminal; no replay')
    folder,text,images=actual.RAM_CASES[actual.KEY]
    original=json.loads((folder/'result.json').read_text())
    control=json.loads((controls.OUT/'report.json').read_text())
    body=json.loads((bodies.OUT/'report.json').read_text())
    guard_path=ROOT/'audit_native_kano_laser_cpu_leg_children_guard_review/report.json'
    guard=json.loads(guard_path.read_text())
    need(control['passed']and body['passed']and guard['passed']and
         len(control['actualSemanticFaultsRejected'])==21 and len(body['actualSemanticFaultsRejected'])==17 and
         control['actualSemanticFaultsRejected'][-1]['rejectedBy'].startswith('Every actual both-slot post-reset draw field'),
         'Whole actual response/body suites and every semantic fault; missing fields reject explicitly, not parser exceptions')
    for report in (control,body,guard):
        need(all(sha(p)==h for p,h in report['inputHashes'].items()),'Every actual immutable source/compiled/proof input stable')
    need(original['nativeExit']==0 and original['error']=="IndexError('list index out of range')"and
         not original['nativeTerminal']['hostDecodeErrors']and not(folder/'stderr.log').read_text()and
         not base.re.search(r'LUA ERROR|stack traceback|fatal error|access violation|WRONG CHECKSUMS|might not run correctly',text,base.re.I),
         'Original failed checker retained; actual native transport terminal0 without warnings')
    pair=bodies.prior.controls.mutation.pair
    cpu=pair.verify_pair(text,'sonya',4,actual.guest)
    need(cpu['passed']and cpu['held_fields']==46 and cpu['damage']==35 and
         control['actualControls']['round']['actualNativeResume']<cpu['start']<cpu['complete'],
         'Entire original CPU paired contact/phase/flight/cleanup/individual handoffs occurs in the actual next round')
    mutation=bodies.prior.controls.mutation
    mutate=lambda tag,key,value,predicate:mutation.mutate_line(text,tag,key,value,predicate)
    def remove(tag,predicate):
        line=next(s for s in text.splitlines()if s.startswith(tag+' ')and predicate(dict(base.re.findall(r'(\w+)=([^\s]+)',s))))
        return text.replace(line+'\n','',1)
    cycle=lambda r:r['cycle']=='4'
    trials=[
        ('next_round_actual_entry_missing',remove('MK2_CPU_PAIR_ENTRY',cycle)),
        ('next_round_actual_phase_step_missing',remove('MK2_CPU_PAIR_EVENT',lambda r:cycle(r)and r['kind']=='step')),
        ('next_round_actual_attack_descriptor_wrong',mutate('MK2_CPU_PAIR_EVENT','word','999',lambda r:cycle(r)and r['kind']=='attack')),
        ('next_round_actual_fling_operand_wrong',mutate('MK2_CPU_PAIR_EVENT','a8','01000000',lambda r:cycle(r)and r['kind']=='fling')),
        ('next_round_actual_own_cleanup_store_wrong',mutate('MK2_CPU_PAIR_FLAG','after','FFFF',lambda r:cycle(r)and r['kind']=='body'and r['pc']=='FF83EEB0')),
        ('next_round_actual_victim_regain_missing',remove('MK2_CPU_PAIR_VICTIM_REGAIN',cycle))]
    faults=[]
    for label,changed in trials:
        need(changed!=text,'Genuine change to an actual next-round CPU record')
        rejected=pair.verify_pair(changed,'sonya',4,actual.guest)
        need(not rejected['passed']and rejected['errors'],'Whole original next-round CPU contract rejects '+label)
        faults.append(dict(fault=label,rejectedBy=rejected['errors']))
    need(pair.verify_pair(text,'sonya',4,actual.guest)==cpu,'Whole unchanged next-round CPU positive restores')
    old={r['frame']:r for r in guard['individuallyReviewedOriginalRasters']}
    newly=[];backing=[]
    for scene in original['actualScenes']:
        frame=scene['frame'];is_control=scene['transportTag']=='MK2_POST_CTRL_RGB'
        name=f"{'control'if is_control else'ui'}_{frame:04d}.png";rgb=images[name]
        need(rgb.shape==(254,400,3),'Whole actual unscaled native raster')
        digest=hashlib.sha256(rgb.tobytes()).hexdigest().upper()
        row=dict(frame=frame,nativeRasterFrame=scene['nativeRasterFrame'],stage=scene['stage'],
                 transportTag=scene['transportTag'],nativeRGBSHA256=digest,sourceRawBGRXSHA256=scene['sha256'])
        if frame in old:
            need(not is_control and digest==old[frame]['nativeRGBSHA256']and scene['sha256']==old[frame]['sourceRawBGRXSHA256'],
                 'Every actual earlier native raster matches both SHA256s of its previously individually viewed same-candidate backing')
            row.update(previouslyViewedNativeBackingHashVerified=True,allActualRGBBytesCompared=False);backing.append(row)
        else:
            need(frame in (CTRL if is_control else CPU)and scene['nativeRasterFrame']==frame-(1 if is_control else 0),
                 'Only exact twelve individually viewed new native rasters, with accurate pre-callback frame labels')
            row['individuallyViewed']=True;newly.append(row)
    need(len(images)==len(original['actualScenes'])==33 and len(newly)==12 and len(backing)==21 and
         len({(r['transportTag'],r['frame'])for r in newly})==12,'All33 exact actual native rasters accounted for; no same-frame alias conflation')
    pins=dict(body['inputHashes']);pins.update(control['inputHashes'])
    for p in (Path(__file__),Path(controls.__file__),Path(bodies.__file__),Path(bodies.prior.__file__),
              Path(bodies.prior.controls.__file__),Path(pair.__file__),guard_path,
              controls.OUT/'report.json',bodies.OUT/'report.json',actual.OUT/'failure.json'):
        pins[str(p.resolve())]=sha(p)
    for p in folder.rglob('*'):
        if p.is_file():
            need(p.suffix.lower()not in('.png','.wav','.bin','.exe','.zip'),'No new raw media, build, ROM or archive')
            pins[str(p.resolve())]=sha(p)
    need(all(sha(p)==h for p,h in pins.items()),'All exact immutable inputs/evidence unchanged at seal')
    OUT.mkdir();base.save(OUT/'report.json',dict(passed=True,candidate=original['candidate'],
        actualNativeRoundControls=control['actualControls'],nativeControlStores=control['nativeControlStoreProvenance'],
        actualPostResetBodyShadow=body['actualPostResetBodyShadow'],actualNextRoundOriginalCPUPair=cpu,
        actualNextRoundCPUFaultsRejected=faults,actualControlFaultsRejected=21,actualBodyShadowFaultsRejected=17,
        actualCounterexamplesRejected=44,individuallyReviewedNewNativeRasters=newly,previouslyViewedNativeBackingHashesVerified=backing,
        originalUniqueRAMRastersToRelease=33,originalLookupAndOmissionFailuresPreserved=True,
        actualHumanNeutralJumpNotOpponentLift=True,actualFullRecoveryAnd180SurvivalFieldsVerified=True,
        postResetFiniteBodyShadowAccepted=True,postResetFiniteNativeRastersReviewed=True,
        fullCPUOrArenaAcceptance=False,fullAudioAcceptance=False,fullPortAcceptance=False,inputHashes=pins,
        gameplayReplayed=False,newBuilds=0,newROMCopies=0,newRawMedia=0,newZIPs=0,publicPlayableChanged=False,goalStatus='active',
        nextAction='Broaden native CPU/move/opponent/arena and sound coverage, reselect/rejoin/campaign, remaining finishers/cinematics and full combined release acceptance.'))
    print(json.dumps(dict(passed=True,actualCounterexamplesRejected=44,newNativeRastersReviewed=12,
                         earlierNativeBackingHashesVerified=21,originalUniqueRAMRastersToRelease=33,fullPortAcceptance=False)),flush=True)


def execute(actual):
    try:run(actual)
    except Exception as error:
        import traceback
        need(not OUT.exists(),'Preserve exact actual review failure');OUT.mkdir()
        base.save(OUT/'failure.json',dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False))
        print(json.dumps(dict(passed=False,error=repr(error))),flush=True)
