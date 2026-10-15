"""Qualify actual four-case Cage section evidence; no additional native boots.

Keep original full goal scope, correctly account all six native timed-exit
PNGs (including two executed verifier failures), and compact retained text
without discarding diagnostics, user assets/configuration or public releases.
"""
import datetime,json,subprocess,traceback
from pathlib import Path
from PIL import Image
import current_cage_torso_source_v5508 as model

ROOT,need,sha=model.ROOT,model.need,model.sha
PARENT=ROOT/'audit_v5507_current_reptile_overlap_qualified_progress/progress.json'
ACCEPTED=ROOT/'audit_v5518_current_cage_sections_progress/progress.json'
OUT=ROOT/'audit_v5520_current_cage_sections_qualified_progress'
LEAVES=[ROOT/f'audit_v{version}_current_cage_sections_ram'for version in(5510,5513,5517)]


def run():
    guest=model.current.expected();parent=json.loads(PARENT.read_text());accepted=json.loads(ACCEPTED.read_text())
    need(parent['passed']and parent['goalStatus']=='active'and accepted['passed']and accepted['goalStatus']=='active'and
         accepted['remaining']==parent['remaining']and accepted['parentAdditiveJournal']==str(PARENT),
         'Complete original remaining requirements and current successful native matrix retained')
    need(accepted['currentCageSectionsBothVictimsBothSlotsAccepted']and accepted['newNativeBoots']==4 and accepted['newBuilds']==0,
         'Actual four cold-boot normal-costume/current-player-slot contexts, no new game build')
    pins=dict(parent['newInputHashes']);pins.update(accepted['newInputHashes']);pins[str(PARENT)]=sha(PARENT);pins[str(ACCEPTED)]=sha(ACCEPTED)
    cases=[]
    for fighter in('kano','sonya'):
        for side in(1,2):
            folder=LEAVES[-1]/f'{fighter}_p{side}';path=folder/'result.json';c=json.loads(path.read_text())
            process=c['process'];before=json.loads((folder/'input_hashes_before.json').read_text())
            need(c['passed']and process['exit_code']==0 and process['player']==fighter and process['victim_slot']==side and
                 process['candidate']==model.current.NAME and process['executable_sha256']==model.current.EXE_SHA and
                 process['payload_sha256']==model.current.PAYLOAD_SHA and process['input_hashes']==before and
                 process['entireOriginal921PhysicalControllerRetained']and process['killer']=='cage'and process['command']=='ddff_lp'and
                 process['target_gap']==64 and process['winner_slot']==3-side and process['assistance']=='none'and not process['cheats_enabled'],
                 'Exact true-ID native original-controller context/process/frozen inputs')
            need(all(sha(p)==h for p,h in before.items()),'Every executed immutable source/public/asset input unchanged')
            pins.update(before)
            physical=c['actualNativeContract'];visual=c['actualNativeSectionPixelsAndScanout']
            need(physical['nativeDamage']==322 and physical['nativeWrapAge']==185 and physical['sectionDMAs']>1000 and
                 physical['groundedLowerDMAs']>100 and physical['groundedUpperDMAs']>100 and physical['hardwarePaletteDumps']==12 and
                 physical['originalVisiblePoses']==[0,1,2,3,5,6]and physical['periodicPictures']==61 and physical['sectionPictures']==6,
                 'Full original health/native control/palette/FIFO/component/floor/phase/retirement contract')
            need(len(c['actualDisplayHeaders'])==93 and len(c['effectiveActualNativeRecordFaults'])==15,
                 'All actual original requested frames and effective actual native-record faults')
            need(visual['passed']and visual['everyEmittedOwnedSectionPixelAndLegitimateForegroundExact']and
                 len(visual['sections'])==6 and {s['pose']for s in visual['sections']}=={0,1,2,3,5,6}and
                 visual['wholeNativeScanoutPixels']==609600 and all(s['pixels']==101600 and
                 s['ownVisiblePixels']+s['ownedNativeOccludedPixels']==s['originalOpaquePixels']for s in visual['sections']),
                 'Six complete section scanouts; all original emitted pixels explicitly own or original native foreground')
            need(len(visual['effectiveActualRAMFaults'])==21 and len(visual['effectiveActualNativeForegroundOwnerFaults'])==3,
                 'Actual component/display/overlap and complete native-owner counterexamples retained')
            cases.append(dict(result=str(path),resultSHA256=sha(path),fighter=fighter,side=side,nativePID=process['nativePID'],nativeExit=0,
              originalFullPhysicalArtContractSHA256=c['originalFullPhysicalArtContractSHA256'],physical=physical,
              actualNativeSectionPixelsAndScanout=visual,actualRequestedRAMFrames=93,effectiveActualNativeRecordFaults=15))
    terminal=[];automatic=[];compacted=[]
    for leaf in LEAVES:
        need(leaf.is_dir(),'Preserve actual native captures and executed verifier counterexamples')
        for folder in sorted(p for p in leaf.iterdir()if p.is_dir()and(p/'process.json').is_file()):
            process=json.loads((folder/'process.json').read_text());result=json.loads((folder/'terminal.json').read_text())
            log=(folder/'run.log').read_text()
            need(result['exit_code']==0 and result['nativePID']==process['pid']and
                 'MK2_STOCK_HEAD_V921_RESULT frame=5198'in log and 'damage=322 wins=2'in log and 'Average speed:'in log and
                 not(folder/'stderr.log').read_text(),'Every actual native process genuinely terminal0, not an expired observation')
            terminal.append(dict(folder=str(folder),pid=process['pid'],terminalField=5198,nativeExit=0,
                                 acceptedGameplayAndPixelCase=(folder/'result.json').is_file()))
            for p in folder.rglob('*'):
                if not p.is_file():continue
                need(p.suffix.lower()not in('.bin','.wav','.rgb','.pcm'),'No persistent raw guest/graphics/VRAM/palette/audio buffers')
                if p.suffix.lower()=='.png':
                    need(p==folder/'snap/mk2ks/0000.png'and Image.open(p).size==(400,254),'Only accurately accounted original MAME native timed-exit PNG')
                    automatic.append(dict(path=str(p),bytes=p.stat().st_size,sha256=sha(p)))
                if p.suffix.lower()in('.log','.json','.txt','.cfg'):
                    before=sha(p);cp=subprocess.run(['compact.exe','/C','/EXE:LZX','/I','/Q',str(p)],capture_output=True)
                    need(cp.returncode==0 and sha(p)==before,'Retained native evidence losslessly compacted')
                    compacted.append(str(p))
                pins[str(p.resolve())]=sha(p)
    need(len(terminal)==len(automatic)==6 and sum(c['acceptedGameplayAndPixelCase']for c in terminal)==4,
         'All six actual native boots and automatic exit screenshots, including two verifier failures, accounted')
    video=ROOT/'mame-mkp/src/emu/video.cpp';source=video.read_text()
    need('if (m_seconds_to_run != 0 && emutime.seconds() >= m_seconds_to_run)'in source and
         '// create a final screenshot'in source and 'machine().schedule_exit();'in source,'Native timed-exit screenshot source behavior unchanged')
    for p in(video,Path(__file__),ROOT/'tools/current_cage_torso_source_v5508.py',ROOT/'tools/verify_current_cage_sections_v5509.py',
             ROOT/'tools/verify_current_cage_sections_v5512.py',ROOT/'tools/inspect_current_cage_foreground_v5515.py',
             ROOT/'tools/verify_current_cage_sections_v5516.py',ROOT/'mk2ks_current_cage_ram_v5509.lua',
             ROOT/'audit_v5511_current_cage_sections_progress/progress.json',ROOT/'audit_v5514_current_cage_sections_progress/progress.json'):
        pins[str(p.resolve())]=sha(p)
    need(all(sha(p)==h for p,h in pins.items()),'All current/public/source/asset/retained-evidence pins stable at qualified completion')
    return dict(passed=True,observedUTC=datetime.datetime.now(datetime.timezone.utc).isoformat(),goalStatus='active',remaining=parent['remaining'],
      parentAdditiveJournal=str(PARENT),previousGoalTurnClassification=parent['thisGoalTurnClassification'],
      thisGoalTurnClassification='progress: completed actual current normal-costume Cage torso-rip victim matrix for own17/18 in both physical player slots; entire original physical controller/damage/parser/palette/FIFO/ground/retirement contract; independent28-component source-PNG and52word-native-control model;24 complete hardware scanouts with every emitted component and source-ROM Cage/gore/opposite-section occluder exact;60 native-record,84 actual RAM and12 full native-foreground-owner counterexamples; two executed verifier model failures retained, six automatic native PNGs accounted, all retained native text losslessly compacted',
      currentNormalCageTorsoRipBothVictimsBothSlotsAccepted=True,cases=cases,independentCurrentSourceArtReference=accepted['independentSourceArtReference'],
      actualAcceptedRequestedRAMDisplayCallbacks=372,exactWholeNativeScanoutPixels=2438400,effectiveActualNativeRecordFaults=60,
      effectiveActualComponentRGBAndOverlapRAMFaults=84,effectiveActualNativeForegroundOwnerFaults=12,
      actualNativeTerminalRuns=terminal,persistentNativeAutomaticExitPNGs=automatic,persistentNativeAutomaticPNGFiles=6,
      persistentNativeAutomaticPNGBytes=sum(p['bytes']for p in automatic),requestedGuestGFXVRAMPaletteRGBPCMWAVFilesWritten=0,
      newNativeBootsSinceParentThisTurn=6,acceptedNativeBoots=4,preservedVerifierFailureNativeBoots=2,newNativeBootsForQualifier=0,
      newBuilds=0,newDeletedFiles=0,terminalTextFilesLosslesslyCompacted=len(compacted),publicPlayableChanged=False,refreshedReleaseZIP=False,
      allFinisherVictimArenaOrCostumeContextsAccepted=False,unusedNativePose4RuntimeAccepted=False,allArenasAccepted=False,
      completeCageFinisherAudioAccepted=False,continuousWholeSceneRasterAccepted=False,fullPortAcceptance=False,newInputHashes=pins,
      nextAction='Continue actual remaining original native finisher/victim/arena/audio/CPU/secret/cinematic contexts, preserve all five original remaining requirement groups, then full applicable combined acceptance and refreshed public release.')


if __name__=='__main__':
    need(not OUT.exists(),'Fresh immutable completed Cage/additive full-scope journal')
    try:report=run()
    except Exception as error:report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),goalStatus='active',fullPortAcceptance=False)
    OUT.mkdir();(OUT/'progress.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in report.items()if k not in('remaining','cases','newInputHashes','actualNativeTerminalRuns','persistentNativeAutomaticExitPNGs','independentCurrentSourceArtReference')},indent=2),flush=True)
    raise SystemExit(0 if report['passed']else 1)
