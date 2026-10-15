"""Preserve a failed observer trial, its real gameplay facts and reviewed pixels."""
import copy
import gzip
import hashlib
import json
import re
from pathlib import Path
import native_process_census_v6647 as census


def need(value, message):
    if not value:
        raise ValueError(message)


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest().upper()


def state_facts(text, states):
    rows = lambda tag: [dict(re.findall(r'(\w+)=([^\s]+)',line)) for line in text.splitlines()
                        if line.startswith('MK2_TOMB_REJOIN_'+tag+' ')]
    a,c = rows('ADMITTED'),rows('COMPLETE')
    need(len(a)==len(c)==1 and not rows('DEADLINE'), 'Actual unique admission and ordinary completion, no deadline')
    af,cf = int(a[0]['frame']),int(c[0]['frame'])
    need(a[0]['ids']=='17,18' and int(c[0]['admitted'])==af and cf-af==int(c[0]['alive_fields'])==180,
         'Actual true Kano/Sonya admission and complete180 later fields')
    need([r['frame'] for r in states]==list(range(states[0]['retired']+31,cf+1)),
         'Entire actual later native state chronology, no missing or extra tail')
    final = re.findall(r'^MK2_STAGE_RESULT frame=(\d+) ',text,re.M)
    need(len(final)==1 and int(final[0])==cf+1,'Native exits at next frame boundary after completed raster field')
    for slot,identity in ((1,17),(2,18)):
        selected = [r for r in rows('SELECT_ID') if r['slot']==str(slot)]
        need(len(selected)==1 and selected[0]['actual']==selected[0]['target']==str(identity) and
             int(selected[0]['frame'])<af,'Actual native selected ID before admission')
        for button in ('Coin','Start'):
            need(any(r['slot']==str(slot) and r['button']==button and int(r['frame'])<af
                     for r in rows('INPUT')),'Actual ordinary paid Coin/Start in both slots')
    live = [r for r in states if af<=r['frame']<=cf]
    need(len(live)==181 and live[0]['hp1']==live[0]['hp2']==161, 'Fresh native full-health admission, every resumed state')
    for r in live:
        need(r['writes']==0 and r['assistance']=='none' and r['mode']==2 and r['admitted']==af and all(
             r[f'actor{s}']==r[f'owner{s}']!=0 and r[f'main{s}']!=0 and r[f'state{s}']==1 and
             r[f'id{s}']==r[f'roster{s}']==(17 if s==1 else 18) for s in (1,2)),
             'True native owned actors/Main/rosters throughout entire resumed window')
    drops = [dict(frame=r['frame'],slot=s,before=prior[f'hp{s}'],after=r[f'hp{s}'])
             for prior,r in zip(live,live[1:]) for s in (1,2) if r[f'hp{s}']<prior[f'hp{s}']]
    need(drops and all(0<=r[f'hp{s}']<=161 for r in live for s in (1,2)),
         'Actual resumed native damage observed, not merely applied input buttons')
    for slot,button in ((1,'Right'),(2,'Left'),(1,'Up'),(2,'High_Punch'),(1,'Block'),(1,'Low_Kick')):
        need(any(r['slot']==str(slot) and r['button']==button and af<int(r['frame'])<cf
                 for r in rows('INPUT')),'All declared later ordinary physical inputs really applied')
    return dict(actualPaidRejoinObserved=True,actualTruePhysicalIDs=[17,18],admitted=af,completed=cf,
                resumedNativeFields=181,completedLaterFields=180,actualHealthDecrements=drops,
                fullVisualTrialAccepted=False,observerErrorNotSilentlyIgnored=True)


def retire(ram, viewed_later_frames):
    folder,output = ram['folder'],ram['output']
    receipt = output/'failed_observer_trial_preservation_and_ram_retirement.json'
    need(not receipt.exists() and not census.census(),'Fresh preservation after exact native normal termination')
    report = json.loads((output/'report.json').read_text())
    meta = json.loads((folder/'result.json').read_text())
    need(not report['passed'] and meta==json.loads(json.dumps(ram['terminal'])) and
         meta['captureCompleted'] and meta['exit_code']==0 and len(meta['modelErrors'])==1 and
         meta['modelErrors'][0]['header'].startswith('MK2_TOMB_POST_PIXELS frame=9626 '),
         'Actual failing capture and first native display mismatch preserved, never relabelled pass')
    text = gzip.open(folder/'run.log.gz','rt').read()
    stderr = (folder/'stderr.log').read_text()
    need('Missing native selection route' in stderr,'Actual observer route failure remains explicit')
    states = json.loads((folder/'post_state_records.json').read_text())
    records = json.loads((folder/'post_scene_records.json').read_text())
    need(states==ram['post_states'] and records==ram['post_records'] and
         json.loads((folder/'continuous_scene_records.json').read_text())==ram['scene'].records,
         'Whole actual RAM and saved diagnostic state/scene evidence unchanged')
    facts = state_facts(text,states)
    rejected = []
    af = facts['admitted']
    for name,mutate in (
        ('missing later state',lambda s:s.pop()),
        ('duplicated later state',lambda s:s.append(s[-1])),
        ('wrong actual player ID',lambda s:next(r for r in s if r['frame']==af).__setitem__('id1',1)),
        ('wrong actor owner',lambda s:next(r for r in s if r['frame']==af).__setitem__('owner2',0)),
        ('wrong actual roster',lambda s:next(r for r in s if r['frame']==af).__setitem__('roster2',1)),
        ('wrong gameplay mode',lambda s:next(r for r in s if r['frame']==af).__setitem__('mode',3)),
        ('injected guest writes',lambda s:next(r for r in s if r['frame']==af).__setitem__('writes',1)),
        ('wrong fresh health',lambda s:next(r for r in s if r['frame']==af).__setitem__('hp1',0)),
    ):
        altered = copy.deepcopy(states);mutate(altered)
        try:state_facts(text,altered)
        except ValueError:rejected.append(name)
        else:raise ValueError('Actual state fault wrongly admitted: '+name)
    for name,altered in (
        ('missing ordinary coins',re.sub(r'^MK2_TOMB_REJOIN_INPUT .*button=Coin\n','',text,flags=re.M)),
        ('missing ordinary start',re.sub(r'^MK2_TOMB_REJOIN_INPUT .*button=Start\n','',text,flags=re.M)),
        ('missing native confirmation',re.sub(r'^MK2_TOMB_REJOIN_SELECT_ID .*\n','',text,flags=re.M)),
        ('missing actual completion',re.sub(r'^MK2_TOMB_REJOIN_COMPLETE .*\n','',text,flags=re.M)),
    ):
        try:state_facts(altered,states)
        except ValueError:rejected.append(name)
        else:raise ValueError('Actual physical input fault wrongly admitted: '+name)
    state_facts(text,states)
    need(set(viewed_later_frames)==set(ram['post_images']) and len(viewed_later_frames)==len(ram['post_images']),
         'Every held later native raster individually inspected')
    root = folder.parent
    prior_path = root/'audit_native_current_cross_tomb_kano_p1_render_checked/native_visual_review_and_ram_retirement.json'
    prior = json.loads(prior_path.read_text())
    need(prior['passed'] and all(sha(p)==h for p,h in prior['inputHashes'].items()),
         'Earlier individually viewed source-identical native bitmaps frozen')
    known = {r['frame']:r['rgbSHA256'] for r in prior['individuallyViewedFields']}
    original = {r['frame']:r for r in ram['scene'].records}
    for frame,rgb in ram['images'].items():
        need(hashlib.sha256(rgb.tobytes()).hexdigest().upper()==known[frame]==original[frame]['rgbSHA256'],
             'Every earlier-viewed original raster byte-identical to same actual scene field')
    ledger = {r['frame']:r for r in records}
    views = []
    for frame,rgb in sorted(ram['post_images'].items()):
        digest = hashlib.sha256(rgb.tobytes()).hexdigest().upper()
        need(rgb.shape==(254,400,3) and digest==ledger[frame]['rgbSHA256'] and ledger[frame]['pixels']==101600,
             'Each reviewed later raster is exact native latch/VRAM/palette before first mismatch')
        views.append(dict(frame=frame,rgbSHA256=digest,individuallyViewed=True))
    pins = dict(meta['input_hashes'])
    for p in (Path(__file__),output/'report.json',folder/'result.json',prior_path,
              folder/'run.log.gz',folder/'stderr.log',folder/'post_state_records.json',
              folder/'post_scene_records.json',folder/'continuous_scene_records.json',folder/'native_identity.json'):
        pins[str(p.resolve())]=sha(p)
    need(all(sha(p)==h for p,h in pins.items()),'Original whole executed source, failed outcome and actual observations frozen')
    identity = json.loads((folder/'native_identity.json').read_text())
    need(identity==ram['identity'] and identity['ProcessId']==
         json.loads((folder/'process.json').read_text())['pid'],'Exact actual original native identity retained')
    proof = dict(passed=True,preservationAndRetirementOnly=True,fullOriginalTrialAccepted=False,
                 exactTerminalNativeIdentity=identity,actualNativeGameplayFacts=facts,
                 actualStateAndInputFaultsRejected=rejected,firstDisplayMismatch=meta['modelErrors'][0],
                 observerLuaError=stderr.strip(),laterVerifiedDisplayFields=len(records),
                 originalSceneFields=len(ram['scene'].records),individuallyViewedLaterFields=views,
                 sourceIdenticalPreviouslyViewedOriginalFrames=sorted(ram['images']),
                 actualVisualObservation='Native shutters replace fatality with normal prepare/continue screen; later selection has dedicated Kano/Sonya portraits, centered P1/P2 numbers and their own animated bodies. No later VS/fight rasters qualified after9625.',
                 fullPortAcceptance=False,goalStatus='active',publicPlayableChanged=False,
                 newEmulatorBuilds=0,rawImageAudioVRAMCopiesWritten=0,inputHashes=pins)
    count = len(ram['review_images'])
    ram['server'].shutdown();ram['server'].server_close()
    for key in ('images','post_images','review_images'):ram[key].clear()
    ram.clear()
    proof.update(originalNativeRasterBuffersReleased=count,reviewServerClosed=True,
                 originalCaptureRAMDictionaryCleared=not ram)
    receipt.write_text(json.dumps(proof,indent=2)+'\n')
    print(json.dumps(dict(passed=True,preservationOnly=True,actualGameplayFacts=facts,
                         rawNativeRastersReleased=count,receipt=str(receipt)),indent=2),flush=True)
    return proof
