"""Additive finite Sub-Zero floor-shadow and full current P1 ending progress.

All five original unfinished groups remain verbatim. Complete per-field
native renderer acceptance never substitutes for unsampled artistic/audio
contexts or independent stock transition choreography.
"""
import datetime,json
from pathlib import Path
import current_payload_metadata_context_v5229 as current
ROOT,need,sha=current.ROOT,current.need,current.sha
PARENT=ROOT/'audit_v5298_current_projectile_roles_and_sonya_ending_progress/progress.json'
OUT=ROOT/'audit_v5305_current_subzero_shadows_and_complete_sonya_ending_progress'
def main():
    need(not OUT.exists(),'Fresh immutable additive whole-goal progress')
    parent=json.loads(PARENT.read_text())
    need(parent['goalStatus']=='active'and len(parent['remaining'])==5 and
      all(sha(p)==h for p,h in parent['newInputHashes'].items()),
      'Every earlier group, real failure, role, source and retained input remains unchanged')
    current.expected()
    pins={str(PARENT):sha(PARENT),str(Path(__file__).resolve()):sha(__file__)}
    shadows=[]
    for move in ('knife','ring'):
        for side in (1,2):
            path=ROOT/f'audit_v5303_current_special_shadow_{move}_p{side}_sub_zero_checked/report.json'
            result=json.loads(path.read_text());case=result['case']
            observed=ROOT/f'audit_v5301_current_special_shadow_{move}_p{side}_sub_zero_observed/report.json'
            runtime=json.loads(observed.read_text())
            need(result['passed']and runtime['passed']and runtime['nativeExit']==0 and
              runtime['victim']=='sub_zero'and runtime['nativeStderrEmpty']and
              result['candidate']==current.NAME and result['executableSHA256']==current.EXE_SHA and
              case['entryBodyPublicationProven']and case['everyReadyBodyComponentSourceBound']and
              case['state']['trueIdentity']==(17 if move=='knife'else 18)and
              len(case['state']['cycles'])==2 and len(result['actualSemanticFaultsRejected'])==11 and
              not case['originalStockSmallRawStreams']and not result['fullPortAcceptance']and
              all(sha(p)==h for p,h in result['inputHashes'].items()),
              'Every actual full entry/body/native projection/ROM stream/DMA row and11faults for true added fighter vs8')
            pins[str(path)]=sha(path);pins[str(observed)]=sha(observed)
            shadows.append(dict(report=str(path),move=move,physicalSlot=side,trueVictimID=8,
              ownTrueIdentity=case['state']['trueIdentity'],physicalCycles=2,
              completeActorPostFields=case['actualContiguousActorFields'],
              fullOwnedBodyCandidates=case['actualNativeBodyCandidates'],
              nativeSourceBoundShadowCopies=case['actualSourceBoundShadowCopies'],
              ownAddedFighterNativeShadowCopies=case['actualAddedFighterShadowCopies'],
              actualSemanticFaultsRejected=11,
              scope='Actual Prison/Sub-Zero repeated projectile and ordinary-control follow-up only. Entire original full body/shadow gates retained. Old inherited Kitana scope prose in source report is not the actual selected victim.',
              otherMoveArenaCPUOrKOArtAudioAccepted=False))
    need(sum(c['completeActorPostFields']for c in shadows)==3210 and
      sum(c['nativeSourceBoundShadowCopies']for c in shadows)==206399 and
      sum(c['ownAddedFighterNativeShadowCopies']for c in shadows)==97307 and
      sum(c['fullOwnedBodyCandidates']for c in shadows)==6588,
      'Every actual newly completed Sub-Zero case precisely accounted')
    endings=[]
    for fighter in ('kano','sonya'):
        pixel=ROOT/f'audit_v5281_{fighter}_current_p1_ending_terminal_pixels_checked/report.json'
        pages=ROOT/f'audit_v5283_{fighter}_current_p1_original_ending_pages_checked/report.json'
        hardware=ROOT/f'audit_v5285_{fighter}_current_p1_complete_native_pixels_hardware_checked/report.json'
        p,a,h=[json.loads(q.read_text())for q in (pixel,pages,hardware)]
        need(p['passed']and a['passed']and h['passed']and
          p['actualCurrentP1EndingAttractNativeRendererVideoAccepted']and
          a['actualCurrentP1EndingEarlyLatePhotoTextShadowCommonBackgroundAccepted']and
          h['fullEndingVRAMRGBPixelsAccepted']and p['physicalSlot']==a['physicalSlot']==h['physicalSlot']==1 and
          p['exactConsecutiveNativeVideoFields']==(3040 if fighter=='kano'else 3042)and
          not h['fullPortAcceptance']and not h['independentStockTransitionChoreographyAccepted']and
          all(sha(k)==v for report in (p,a,h)for k,v in report['inputHashes'].items()),
          'Every actual source-timed P1 field/native boundary/photo/font/shadow/background/hardware original fault proof')
        for q in (pixel,pages,hardware):pins[str(q)]=sha(q)
        endings.append(dict(fighter=fighter,physicalSlot=1,pixelReport=str(pixel),
          pageReport=str(pages),hardwareReport=str(hardware),
          exactNativeVRAMRGBFields=p['exactConsecutiveNativeVideoFields'],
          actualEndingStart=p['endingStart'],actualAttractStart=p['endingAttract'],
          actualLastCompletedField=p['lastCompletedRendererField'],actualAttractFields=300,
          actualPixelBitFaultsRejected=len(p['actualNativePixelFaultsRejected']),
          fullCurrentP1NativeRendererWindowAccepted=True,
          independentStockTransitionChoreographyAccepted=False,otherCinematicAudioContextsAccepted=False))
    failure=ROOT/'audit_v5264_sonya_current_p1_ending_pixels_checked/report.json'
    failed=json.loads(failure.read_text())
    need(not failed['passed']and failed['error']==
      "ValueError('One base only, all actual targets consumed; no floor classification substituted for cinematic semantics')",
      'Real actual native0 post-pixel shutdown guard failure remains preserved')
    pins[str(failure)]=sha(failure)
    for name in ('tools/run_current_shadow_repeat_v5299.py','tools/verify_current_subzero_special_shadow_v5302.py'):
        path=ROOT/name;pins[str(path)]=sha(path)
    need(all(sha(p)==h for p,h in pins.items()),'Every final actual terminal and full semantic evidence stable')
    report=dict(schema=1,observedUTC=datetime.datetime.now(datetime.timezone.utc).isoformat(),
      parentAdditiveJournal=str(PARENT),goalStatus='active',remaining=parent['remaining'],
      thisGoalTurnClassification='progress: four fresh current native Sub-Zero projectile roles completed. Entire every-ready-field body and shadow gate independently accepted all entry phases,6588owned body components,206399native shadow copies,44real faults. Same54808 Sonya native0/347965 ending-attract capture completed;3042every-field RAM VRAM/RGB exports retained. Actual single unrendered stop notifier seed qualified separately without dropping any pixel or hardware error; original failed final guard preserved. Full original pages and complete hardware/all original faults accepted. Both current true P1 own ending/300attract native renderer windows now accepted, not all port art/audio/cinematics.',
      mergeRule='Additive finite instances only. Every original unfinished group remains verbatim. No proxy, guest writes, forced opponents, pixel substitution, target reanchor, timeout acceptance or release promotion.',
      currentSubZeroRepeatedProjectileShadows=shadows,
      actualCurrentP1CompleteNativeEndingContexts=endings,
      actualAddedShadowCycles=8,actualCompleteShadowActorPostFields=3210,
      actualAddedFighterSourceBoundNativeShadowCopies=97307,
      actualNewShadowSemanticFaultsRejected=44,
      newBuilds=0,newRawROMVRAMImageAudioFilesWritten=0,newDeletedFiles=0,
      publicPlayableChanged=False,refreshedReleaseZIP=False,fullPortAcceptance=False,
      newInputHashes=pins,
      nextAction='Continue remaining native stage/victim/mirror branches and effect/audio fidelity; complete other move-phase/arena/CPU/repeated/KO/overlap art/shadow coverage, other finishers/morphs/secrets/cinematics and independent stock transition choreography. Then full combined selection/ladder/names/audio regression, dependency-aware obsolete cleanup and refreshed release ZIP. No complete/block status change justified.')
    OUT.mkdir();(OUT/'progress.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(journal=str(OUT/'progress.json'),goalStatus='active',
      actualNativeShadowCases=4,actualAddedFighterShadowCopies=97307,
      actualFullCurrentP1EndingContexts=2,fullPortAcceptance=False,newBuilds=0),indent=2),flush=True)
if __name__=='__main__':main()
