"""Same terminal guard run: whole callback transport plus12 actually reviewed fields.

Add the complete existing body/shadow and real Block-contact receipts without
promoting ordinary blocking to blocked knife or sampled images to full art.
"""
import copy,hashlib,json,re,sys
from collections import Counter
from pathlib import Path
import numpy as np
import capture_native_selector_cpu_guard_shadow as capture
import read_live_shang_drain_frames as identities

ROOT,need,sha=capture.ROOT,capture.need,capture.sha
OUT=ROOT/'audit_native_selector_cpu_guard_checkpoint_checked'


def image_gate(scenes,images,text):
    records=[dict(re.findall(r'(\w+)=([^\s]+)',s))for s in text.splitlines()
             if s.startswith('MK2_HPHASE_RGB_DIGEST ')]
    need(len(scenes)==len(records)==len(images)==177,'All original actual callback requests retained')
    keys=[];proofs=[]
    for index,(row,actual)in enumerate(zip(scenes,records)):
        key=f"ui_{row['frame']:04d}_{index:04d}.png"
        need(row['imageKey']==key and row['callbackOrdinal']==index and
             all(str(row[k])==actual[k]for k in('frame','stage','attempt','width','height','bytes','sha256'))and
             row['rawMediaFilesWritten']==0,
             'Original raw-block field/stage/digest/order, with separate callback identity; no invented frames')
        rgb=images[key];need(rgb.shape==(254,400,3)and rgb.dtype==np.uint8,'Entire original unscaled RGB')
        raw=np.empty((254,400,4),np.uint8);raw[:,:,:3]=rgb[:,:,::-1];raw[:,:,3]=255
        need(hashlib.sha256(raw.tobytes()).hexdigest().upper()==row['sha256'],
             'Every original native pixel reconstructs complete original BGRX callback digest')
        keys.append(key);proofs.append(dict(index=index,frame=row['frame'],imageKey=key,
            SHA256=row['sha256'],nativeRGBSHA256=hashlib.sha256(rgb.tobytes()).hexdigest().upper()))
    need(len(set(keys))==len(keys)and set(keys)==set(images),'No callback overwritten or quietly discarded')
    repeated={f:n for f,n in Counter(r['frame']for r in scenes).items()if n>1}
    need(repeated,'Actual same-field callbacks observed and retained, not a synthetic-only key test')
    return dict(passed=True,completeNativeCallbacks=177,actualSameFieldCallbackCounts=repeated,
        exactPixelDigestProofs=proofs,allFramesOrPixelsArtisticallyAccepted=False)


def execute(state,reviewed,view_native,view_host):
    need(not OUT.exists()and not capture.prior.current.prior.identity.census(),
         'Same original terminal capture; no game replay')
    folder,text,images=capture.RAM_CASES[capture.KEY]
    meta=json.loads((folder/'result.json').read_text());held=capture.NATIVE_HANDLES[capture.KEY]
    host=next(r for r in identities.census_hosts()if r['ProcessId']==38752)
    need(host==view_host and (host['ParentProcessId'],host['createdUnix'])==(40316,1791734919.6266766)and
         host['CommandLine']=='"'+sys.executable+'" -B tools/capture_native_selector_special_shadow.py'and
         meta['passed']and meta['nativeExit']==held['process'].poll()==0 and
         held['identity']==view_native==meta['nativeTerminal']['actualWindowsIdentity']and
         (view_native['ProcessId'],view_native['ParentProcessId'],view_native['createdUnix'])==
         (42288,38752,1791739187.1680584)and not meta['nativeTerminal']['hostDecodeErrors'],
         'Exact live original host and original native kernel PID/parent/birth/full command/terminal')
    positive=image_gate(meta['actualScenes'],images,text)
    need(len(reviewed)==12 and {r['index']for r in reviewed}==
         {3,79,85,93,104,121,125,126,140,150,168,176},'All12 actually inspected native fields, not all177 claimed reviewed')
    by={p['index']:p for p in positive['exactPixelDigestProofs']}
    for r in reviewed:
        need(r['header']==meta['actualScenes'][r['index']]and r['SHA256']==by[r['index']]['SHA256']and
             r['nativeRGBSHA256']==by[r['index']]['nativeRGBSHA256']and
             r['actualReconstructedAlpha']==255 and r['identityRevalidatedBeforeAndAfter'],
             'Actual reviewed native callback binds original metadata/whole digest/host identity')
    faults=[]
    for label in('callback_ordinal','native_frame','native_pixel_digest'):
        changed=copy.deepcopy(meta['actualScenes'])
        if label=='callback_ordinal':changed[0]['callbackOrdinal']=1
        elif label=='native_frame':changed[0]['frame']+=1
        else:changed[0]['sha256']='0'*64
        try:image_gate(changed,images,text)
        except(ValueError,AssertionError)as error:faults.append(dict(fault=label,rejectedBy=str(error)))
        else:raise ValueError('Actual callback/pixel corruption accepted '+label)
    need(image_gate(meta['actualScenes'],images,text)==positive,'Exact complete callback positive restored')
    body_path=ROOT/'audit_native_selector_cpu_guard_body_shadow_syntax_checked/report.json'
    contacts_path=ROOT/'audit_native_selector_cpu_guard_contacts_checked/report.json'
    body=json.loads(body_path.read_text());contacts=json.loads(contacts_path.read_text())
    need(body['passed']and contacts['passed']and
         body['originalNativePID']==contacts['actualOriginalNativePID']==42288 and
         len(body['originalBodyShadowFaultsRejected'])==11 and len(body['additionalNativePostEntryFaultsRejected'])==4 and
         len(contacts['actualFaultsRejected'])==14,
         'Complete same-native body/shadow and actual real-input block gates/faults retained')
    pins=dict(meta['inputHashes'])
    for proof in(body,contacts):
        need(all(sha(p)==h for p,h in proof['inputHashes'].items()),'Whole original source/native receipts unchanged')
        pins.update(proof['inputHashes'])
    for path in(Path(__file__),Path(identities.__file__),body_path,contacts_path,
        ROOT/'tools/read_native_selector_cpu_guard_frames.py',
        ROOT/'tools/read_native_selector_cpu_guard_frames_remote.py'):
        pins[str(path.resolve())]=sha(path)
    need(all(sha(p)==h for p,h in pins.items()),'Final exact full executed/read inventory stable')
    OUT.mkdir();value=dict(passed=True,candidate=meta['candidate'],goalStatus='active',
        actualNativeIdentity=view_native,actualLiveRetainedHostIdentity=host,
        completeNativeCallbackTransport=positive,actualReviewedNativeFields=reviewed,
        bodyShadowReceipt=str(body_path),actualBlockContactReceipt=str(contacts_path),
        callbackFaultsRejected=faults,totalCurrentBodyBlockCallbackFaults=32,
        previousGoalTurnClassification='progress: current actual unblocked knife/state/KO-reset and28 faults',
        thisGoalTurnClassification='progress: distinct real guard-hold, live body/shadow across KO/reset,32 blocked direct contacts, all177 callback pixels retained and12 actually reviewed',
        requirements=['selection','transition','identity','names','human_moves','cpu_moves','ordinary_combat',
            'ground_shadows','audio','finishers_victims','stage_finishers','campaign_cinematics','cmd_release','storage'],
        remainingGroups=['startup cue/CPU/overlap/hit/KO/selection/reset/morph ownership cleanup/full UI ground/audio',
            'broader CPU projectile arena shadow/audio','later-stage controls/continue audio/post-ending fresh join',
            'remaining Pit/Tomb/stock victim finishers/sound priority','secret/morph/cinematics',
            'final combined visual/audio/gameplay and matching public CMD/finished ZIP'],
        blockedKnifeAccepted=False,CPUBladeOrAllSlotsArenasAccepted=False,
        fullArtAudioAcceptance=False,fullPortAcceptance=False,publicPlayableChanged=False,
        newNativeGames=0,newBuilds=0,newROMCopies=0,newRawMedia=0,newZIPs=0,inputHashes=pins)
    capture.prior.current.prior.save(OUT/'report.json',value)
    print('PASS all177 actual callbacks /12 actually reviewed /32 total current faults; full goal remains active',flush=True)
    return value
