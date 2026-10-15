"""Verified damage interpretation and one pending natural campaign; full scope retained."""
import json
import subprocess
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import verify_current_campaign_shao_highkick_v3423 as native

ROOT=native.ROOT;need=native.need;sha=native.sha
PREVIOUS=ROOT/'audit_v3416_current_kintaro_campaign_full_scope_checkpoint/checkpoint.json'
CAPTURE=ROOT/'audit_v3421_current_sonya_natural_highkick_campaign'
OUT=ROOT/'audit_v3425_current_highkick_pending_full_scope_checkpoint'

def main():
    need(not OUT.exists(),'Immutable full-scope checkpoint')
    state=json.loads(PREVIOUS.read_text());remaining=state['remaining']
    need(state['goalStatus']=='active' and len(remaining)==5 and not state['fullPortAcceptance']
         and not state['finishedRelease'] and not state['actualEndingsAccepted'],'Original unfinished full objective retained')
    fresh={}
    def pin(path,digest=None):
        path=Path(path).resolve();key=str(path);digest=digest or sha(path)
        need(key not in fresh or fresh[key]==digest,'Consistent fresh evidence')
        need(key not in state['inputHashes'] or state['inputHashes'][key]==digest,'Never relabel parent evidence')
        fresh[key]=digest
    proofpath=ROOT/'audit_v3418_current_lowkick_damage_model_checked/report.json'
    proof=json.loads(proofpath.read_text());model=proof['actualCurrentDamageModel']
    need(proof['passed'] and not proof['fullPortAcceptance'] and not proof['gameOrCaptureChanged']
         and model['rawNormalDamage']==6 and model['rawBlockDamage']==2
         and model['actualDamageHistogram']=={'4':26,'1':4} and model['totalDamage']==108
         and model['branchClassificationIsSourceDerivedInferenceNotDirectBranchTrace']
         and model['allThirtyHitsBlockedClaimRejected'] and len(proof['specificActualCounterexamples'])==4
         and proof['samePathPositiveControlAccepted'],'Actual original damage model and qualified controls only')
    pin(proofpath)
    for file,digest in proof['inputHashes'].items():pin(file,digest)
    native.source_boundary()
    need(not (CAPTURE/'result.json').exists(),'Pending campaign must not be labelled terminal')
    before=json.loads((CAPTURE/'input_hashes_before.json').read_text(encoding='utf-8-sig'))
    snapshots=json.loads((CAPTURE/'source_snapshot_paths.json').read_text(encoding='utf-8-sig'))
    for file,digest in before.items():
        pin(file,digest)
        if Path(file).suffix in ('.lua','.ps1','.json'):
            target=Path(snapshots[file]).resolve()
            need(target.is_relative_to(CAPTURE.resolve()),'Frozen hierarchy stays in exact capture')
            pin(target,digest)
    for name in ('input_hashes_before.json','source_snapshot_paths.json','guest_maincpu.bin'):pin(CAPTURE/name)
    need(sha(CAPTURE/'guest_maincpu.bin')=='65CE02355CD6B2830F4635FF1B8D55C1D0D22BA22E37ECF17B820DF26DA020E7','Actual current guest captured')
    for relative in (state['currentCMD'],state['currentPlaytestZIP'],
                     'diagnostic_v1836_ball_register_boundary/mkport_candidate.exe',
                     'diagnostic_v1836_ball_register_boundary/roms/mk2ks/mk2ks.mdata'):
        key=str((ROOT/relative).resolve());need(key in state['inputHashes'],'Retained public playable guard')
        pin(key,state['inputHashes'][key])
    pin(PREVIOUS);pin(__file__);pin(native.__file__)
    with ThreadPoolExecutor(max_workers=4) as pool:
        for (file,digest),actual in zip(fresh.items(),pool.map(sha,fresh)):
            need(actual==digest,'All fresh source/capture/public input bytes unchanged')
    state['inputHashes']=fresh
    state.update(inputHashInheritance=dict(schema=1,parentCheckpoint=str(PREVIOUS),
        parentCheckpointSHA256=fresh[str(PREVIOUS)],
        mergeRule='Resolve parent recursively, preserving retired/deleted exclusions. Fresh inputHashes must agree with inherited keys; do not flatten/copy the historical map.'),
        historicalPinMapCopiedAgain=False,previousCheckpoint=str(PREVIOUS),
        previousGoalTurnClassification=state['thisGoalTurnClassification'],
        thisGoalTurnClassification='progress: independent current whole-guest/original-MK2 lowkick damage model matches all30actual Shao stores:26x4 and4x1,108total. Four qualified model faults and same-path positive accepted. Supersedes unsupported all30blocked wording: normal/block classification is source-derived inference, not direct branch trace. New ordinary-input-only Sonya cold campaign uses crouching highkick and earlier guard release solely in stage16; whole ordinary/Kintaro/native observers exact. Existing3172 reused, no WAV/build/ROM copies. Capture3421 live11731; not accepted until terminal full verifier. Successor3423 corrects mixed-separator accepted-hash lookup; static source boundary/current verifier construction passed. Full five groups retained.',
        currentLowkickDamageModelReport=str(proofpath),currentLowkickDamageModel=model,
        previousAllThirtyShaoHitsBlockedWordingSuperseded=True,
        pendingCurrentNaturalHighkickCampaign=dict(capture=str(CAPTURE),execSessionId=11731,
            player='sonya',humanSlot=1,strategy='zoning',seconds=3900,bootFrame=600,
            candidate='diagnostic_v3172_native_morph_shadow',terminal=False,
            acceptance=False,verifier=str(Path(native.__file__).resolve())),
        pendingCampaignLogNotPinnedWhileMutable=True,
        current3172NaturalShaoClearAccepted=False,actualEndingsAccepted=False,
        currentRealShaoKahnMatchClears=0,currentNaturalHighkickControllerImprovementAccepted=False,
        gameSourceAndPlayableBytesChangedThisTurn=False,nativeGuestProgramChangedThisTurn=False,
        newExecutableROMOrRawAudioCopiesThisTurn=0,publicLauncherChangedThisTurn=False,publicReleaseZIPChangedThisTurn=False,
        inheritedHistoricalGraphRevalidatedInFullThisTurn=False,revalidatedFreshRelevantFilePins=len(fresh),
        goalStatus='active',fullPortAcceptance=False,finishedRelease=False,
        nextAction='Poll exact live11731; never restart on observation timeout. When3421 terminal, execute3423 whole-campaign verifier into fresh output. Do not infer victory or gameplay defect from intended inputs/losing controller. Preserve current Kano natural Kintaro clear and corrected3418 damage interpretation. All original arena/victim/effect/audio, move-phase/CPU/arena/repeat/KO/overlap/shadow, finisher/morph/secret/cinematic, boss/own-ending/attract, final integrated UI/audio/cleanup/refreshed-release groups remain. No raw audio/build copies or historical graph flattening.')
    need(state['remaining']==remaining,'Full objective not narrowed')
    OUT.mkdir();path=OUT/'checkpoint.json';path.write_text(json.dumps(state,indent=2)+'\n');digest=sha(path)
    compact=subprocess.run(['compact.exe','/C','/I','/Q',str(path)],capture_output=True,text=True)
    need(compact.returncode==0 and sha(path)==digest,'Lossless checkpoint compression')
    print(json.dumps(dict(saved=str(path),goalStatus='active',remainingGroups=5,
        capturePending=True,execSessionId=11731,freshPins=len(fresh),fullPortAcceptance=False),indent=2),flush=True)

if __name__=='__main__':main()
