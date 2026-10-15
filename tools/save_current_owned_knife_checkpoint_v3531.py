"""Source-bound actual boss Knife children; both natural clears retained."""
import json,subprocess
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import verify_current_owned_knife_callback_v3533 as native
ROOT=native.ROOT;need=native.need;sha=native.sha
PREVIOUS=ROOT/'audit_v3520_current_both_natural_clear_full_scope_checkpoint/checkpoint.json'
OUT=ROOT/'audit_v3532_current_owned_knife_full_scope_checkpoint'
def main():
    need(not OUT.exists(),'Immutable full-scope checkpoint')
    state=json.loads(PREVIOUS.read_text());remaining=state['remaining'];fresh={}
    need(state['goalStatus']=='active' and len(remaining)==5 and not state['fullPortAcceptance']
       and not state['finishedRelease'] and state['current3172BothTrueCharacterP1NaturalCampaignClearsOwnStoryAndAttractAccepted'],
       'Original full scope and both actual natural clears retained')
    def pin(path,digest=None):
        key=str(Path(path).resolve());digest=digest or sha(key)
        need(key not in fresh or fresh[key]==digest,'Consistent fresh actual proof')
        need(key not in state['inputHashes'] or state['inputHashes'][key]==digest,'Never relabel parent evidence')
        fresh[key]=digest
    proof_path=ROOT/'audit_v3534_current_owned_knife_callback_checked/report.json'
    proof=json.loads(proof_path.read_text());contact=proof['actualNativeContact']
    need(proof['passed'] and not proof['fullPortAcceptance'] and proof['samePathOriginalNativeContactPositiveAccepted']
       and proof['actualSharedVictimActorA1AndCallbackA2AndRawDamageA10Accepted']
       and len(proof['actualQualifiedRuntimeFaults'])==4,'Actual source-bound child/contact/lifetime fault rejections, same-path positive')
    need(contact['actualOwnParentEntries']==contact['actualNativeChildBirths']==contact['actualNativeChildRetirements']==30
       and contact['actualNativeChildFields']==1601 and contact['actualOwnedChildCollisionStores']==30
       and contact['actualOwnedChildDamage']==426 and contact['actualNativeBranchCounts']=={'blocked':2,'normal':28}
       and contact['actualDamageHistogram']=={'4':2,'16':26,'1':2}
       and contact['actualOwnedClampedKOFrames']==[80764,81767]
       and contact['actualNativeRetirementModes']=={'2':27,'5':2,'11':1}
       and contact['allObservedBossCollisionStoresAttributed']
       and not contact['fullPhasePixelsGroundShadowAudioOrAllContextsAccepted'],
       'All30actual own17 children and true13 victim, original branch/extraction/scaler/zero-clamped HP/retirement through finalboss death; not all art/audio')
    pin(proof_path)
    for file,digest in proof['inputHashes'].items():pin(file,digest)
    pin(ROOT/'tools/verify_current_owned_knife_boss_v3529.py')
    for relative in(state['currentCMD'],state['currentPlaytestZIP'],
       'diagnostic_v1836_ball_register_boundary/mkport_candidate.exe','diagnostic_v1836_ball_register_boundary/roms/mk2ks/mk2ks.mdata'):
        key=str((ROOT/relative).resolve());pin(key,state['inputHashes'][key])
    pin(PREVIOUS);pin(__file__)
    with ThreadPoolExecutor(max_workers=4)as pool:
        for(file,digest),actual in zip(fresh.items(),pool.map(sha,fresh)):need(actual==digest,'Fresh actual source/capture/public bytes unchanged')
    state['inputHashes']=fresh
    state.update(inputHashInheritance=dict(schema=1,parentCheckpoint=str(PREVIOUS),parentCheckpointSHA256=fresh[str(PREVIOUS)],
       mergeRule='Resolve parent recursively preserving retired/deleted exclusions. Fresh pins agree with inherited keys; never flatten/copy historical map.'),
       previousCheckpoint=str(PREVIOUS),previousGoalTurnClassification=state['thisGoalTurnClassification'],
       thisGoalTurnClassification='progress: inspect actual3521campaign/3508observer/3518source/3516terminal trace. Independently parse30parent entries/30childbirths/1601observed childfields/30original retirements.3529 failed checker wrongly treated A3 as common victim-ID. Original disassembly shows blocked FF8360A0 loads A3, normal FF835D20 path does not; shared original dispatcher callback uses A1 actual victim actor,A2 callback,A10 raw damage.3533/3534 preserve failed3529 and prove actual17independent child/parent and13victim, original native branch/extraction/Shao callback6→4 and22→16,26full16hits2blocked4chips2clamped1KOs,30stores426damage, all opponent stores attributed rather than temporal proximity. Whole original guard/retire code compared, source/model/full already accepted campaign byte pins unchanged. Native retirements27mode2,2mode5,1mode11 including decidingbossKO; no children remain. Four actual wrong-parent/scaled-damage/native-branch/post-retirement-orphan faults reject intended invariants; same-path original positive. No new runtime/build/ROM/WAV copies or game/public changes; both native P1 clears retained and all five original requirement groups remain.',
       currentKnifeBossChildParentGuardAndNativeDamageAndRetirementAccepted=True,
       currentKnifeBossChildParentGuardAndFullRuntimeContactAccepted=True,
       currentKnifeBossOwnedContactReport=str(proof_path),
       currentKnifeBossActualOwnChildBirths=30,currentKnifeBossActualOriginalRetirements=30,
       currentKnifeBossActualObservedChildFields=1601,currentKnifeBossOwnedNativeCollisionStores=30,
       currentKnifeBossOwnedNativeCollisionDamage=426,currentKnifeBossActualBlockedHits=2,currentKnifeBossActualNormalHits=28,
       currentKnifeBossActualOwnedClampedKOFrames=[80764,81767],currentKnifeBossActualRetirementModes={'2':27,'5':2,'11':1},
       currentKnifeBossQualifiedActualRuntimeFaults=4,currentKnifeBossActualSharedCallbackABI='A1=victim actor; A2=original callback; A10=raw damage. A3 is not a shared victim-ID register.',
       currentKnifeBossFullPhasePixelsGroundShadowAudioOrAllContextsAccepted=False,
       gameSourceAndPlayableBytesChangedThisTurn=False,nativeGuestProgramChangedThisTurn=False,
       publicLauncherChangedThisTurn=False,publicReleaseZIPChangedThisTurn=False,newExecutableROMOrRawAudioCopiesThisTurn=0,
       inheritedHistoricalGraphRevalidatedInFullThisTurn=False,revalidatedFreshRelevantFilePins=len(fresh),historicalPinMapCopiedAgain=False,
       nextAction='Do not rerun3534or completed3516/3521/3523/3525 for continuity. Actual native boss Knife ownership/branch/raw6or22→4or16/clampedHP/retirement now proven on all30observed children, including finalKO. Both current P1 natural clears/own stories/attract remain accepted, no universal art/audio claim. Audit authoritative evidence against the original five broad groups to choose the next concrete missing fidelity gate rather than merely carrying forward their labels. In particular current-vs-old Pit/Tomb victim/branch/audio and other native finisher/morph/cinematic coverage, full current move-phase art/ground/shadow/repeat/KO/overlap, own ending pixels/audio and combined UI/audio/cleanup/refreshedZIP. Ring3490 still lacks actual boss child/parent/guard trace; use only a fresh compressed frozen read-only companion if stronger runtime attribution is necessary, not a restart of a completed handle. No new game power/difficulty/AI/RNG/HP changes, build/WAV/retired recovery copies or broad historical rehash.')
    need(state['remaining']==remaining,'Original full objective remains intact')
    OUT.mkdir();path=OUT/'checkpoint.json';path.write_text(json.dumps(state,indent=2)+'\n');digest=sha(path)
    result=subprocess.run(['compact.exe','/C','/I','/Q',str(path)],capture_output=True,text=True)
    need(result.returncode==0 and sha(path)==digest,'Lossless full-scope checkpoint compression')
    print(json.dumps(dict(saved=str(path),goalStatus='active',remainingGroups=5,actualKnifeOwnershipGuardDamageRetirementAccepted=True,
       bothNaturalClearsRetained=True,freshPins=len(fresh),fullPortAcceptance=False),indent=2),flush=True)
if __name__=='__main__':main()
