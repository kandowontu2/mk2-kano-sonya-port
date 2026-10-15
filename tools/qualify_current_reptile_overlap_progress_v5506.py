"""Qualify completed actual cases without another boot; account native exit PNGs.

5504 stopped only on its overbroad no-PNG assertion AFTER all cases passed.
MAME video.cpp explicitly saves one native screenshot for -str exit. Preserve
and account those actual images; all31 requested frames/case remain RAM-only.
Keep every original remaining requirement and all immutable failed evidence.
"""
import datetime, json, re, subprocess
from pathlib import Path
from PIL import Image
import current_reptile_victims_ram_v5467 as original

ROOT,need,sha=original.ROOT,original.need,original.sha
PARENT=original.PARENT
OUT=ROOT/'audit_v5507_current_reptile_overlap_qualified_progress'
FAILED=ROOT/'audit_v5504_current_reptile_overlap_progress/progress.json'
SPECS=[('kano',1,5496),('sonya',1,5496),('kano',2,5503),('sonya',2,5503)]
LEAVES=[ROOT/f'audit_v{v}_{name}'for v,name in(
 (5478,'current_reptile_victims_ram'),(5481,'current_reptile_victims_ram'),
 (5484,'current_reptile_victims_ram'),(5487,'current_reptile_victims_ram'),
 (5490,'current_reptile_pixel_diagnostic_ram'),(5493,'current_reptile_overlap_ram'),
 (5496,'current_reptile_overlap_ram'),(5503,'current_reptile_p2_overlap_ram'))]


def run():
    parent=json.loads(PARENT.read_text())
    need(parent['passed']and parent['goalStatus']=='active','Authoritative current primary/audio frontier retained')
    failure=json.loads(FAILED.read_text())
    need(not failure['passed']and failure['error']=="ValueError('No raw media files')",'Exact final packaging/accounting assertion, not a failed gameplay/pixel case')
    pins=dict(parent['newInputHashes']);pins[str(PARENT)]=sha(PARENT)
    cases=[]
    for fighter,side,version in SPECS:
        name='current_reptile_overlap_ram'if version==5496 else'current_reptile_p2_overlap_ram'
        folder=ROOT/f'audit_v{version}_{name}'/f'{fighter}_p{side}'
        result_path=folder/'result.json';case=json.loads(result_path.read_text())
        process=case['process'];before=json.loads((folder/'input_hashes_before.json').read_text())
        need(case['passed']and process['exit_code']==0 and process['player']==fighter and process['victim_slot']==side and
             process['candidate']==original.current.NAME and process['executable_sha256']==original.current.EXE_SHA and
             process['payload_sha256']==original.current.PAYLOAD_SHA and process['input_hashes']==before,
             'Every exact native context/terminal/frozen executed input map accepted')
        need(all(sha(p)==h for p,h in before.items()),'Every original source/public/asset dependency remains unchanged')
        pins.update(before)
        log=(folder/'run.log').read_text()
        need(not(folder/'stderr.log').read_text()and
             f'RESULT frame=5198 victim={fighter} side={side} writes=0 assistance=none damage=322 wins=2'in log,
             'Full original genuine controller,322 actual damage,two earned wins and terminal field retained')
        need(len(case['actualDisplayHeaders'])==31 and len(case['effectiveActualNativeRecordFaults'])==21,'Whole original snapshots and effective native-record faults')
        visual=case['actualNativeBodyBloodPixelsAndScanout']
        need(visual['passed']and len(visual['targets'])==3 and visual['completeNativeSceneScanoutPixels']==304800 and
             [r['age']for r in visual['targets']]==[150,200,250]and
             all(r['everyOriginalOpaqueBodyAndNativeBloodPixelExact']and r['ownVisiblePixels']+r['sourceROMBloodOccludedPixels']==r['originalOpaquePixels']for r in visual['targets']),
             'All original opaque body pixels accounted as own source or exact individually owned stock blood; whole12 native scanouts')
        need(len(visual['effectiveActualRAMFaults'])==(12 if side==1 else 6),'Every actual effective pixel/source/overlap counterexample retained')
        automatic=folder/'snap/mk2ks/0000.png'
        need(automatic.is_file()and Image.open(automatic).size==(400,254),'Actual single native -str exit image preserved')
        # Earlier case flags describe the requested RAM captures, not this
        # independently accounted native automatic timed-exit screenshot.
        cases.append(dict(result=str(result_path),resultSHA256=sha(result_path),fighter=fighter,side=side,
          nativePID=process['nativePID'],nativeExit=0,originalFullPhysicalArtContractSHA256=case['originalFullPhysicalArtContractSHA256'],
          physical=case['actualNativeContract'],stateFaults=21,actualNativeBodyBloodPixelsAndScanout=visual,
          requestedNativeFrameCallbacksOnlyInRAM=31,automaticNativeTimedExitScreenshots=1,
          automaticExitScreenshot=str(automatic),automaticExitScreenshotBytes=automatic.stat().st_size))
    # Bind the automatic media to the actual source behavior, not a rewritten
    # claim of zero persistent media. No gameplay or controller change/reboot.
    video=ROOT/'mame-mkp/src/emu/video.cpp';text=video.read_text()
    need('if (m_seconds_to_run != 0 && emutime.seconds() >= m_seconds_to_run)'in text and
         '// create a final screenshot'in text and 'machine().schedule_exit();'in text,
         'Original MAME timed-exit source explicitly writes native PNG then exits')
    automatic_all=[];terminal_runs=[];compacted=[]
    for leaf in LEAVES:
        need(leaf.is_dir(),'Every actual preserved native run remains available')
        for folder in sorted(p for p in leaf.iterdir()if p.is_dir()and(p/'process.json').is_file()):
            process=json.loads((folder/'process.json').read_text());log=(folder/'run.log').read_text()
            need('RESULT frame=5198'in log and 'Average speed:'in log and not(folder/'stderr.log').read_text(),
                 'Each earlier native run genuinely terminal, not an expired observation')
            terminal_runs.append(dict(folder=str(folder),pid=process['pid'],originalTerminalField=5198))
            for file in folder.rglob('*'):
                if not file.is_file():continue
                if file.suffix.lower()in('.bin','.wav','.rgb'):raise ValueError('Unexpected persisted guest/graphics/audio buffer')
                if file.suffix.lower()=='.png':
                    need(file==folder/'snap/mk2ks/0000.png'and Image.open(file).size==(400,254),'Only original native timed-exit image exists')
                    automatic_all.append(dict(path=str(file),bytes=file.stat().st_size,sha256=sha(file)))
                if file.suffix.lower()in('.json','.log','.txt','.cfg'):
                    before=sha(file);cp=subprocess.run(['compact.exe','/C','/EXE:LZX','/I','/Q',str(file)],capture_output=True)
                    need(cp.returncode==0 and sha(file)==before,'Lossless retained terminal text compression')
                    compacted.append(str(file))
                pins[str(file)]=sha(file)
    need(len(terminal_runs)==len(automatic_all)==12,'All12 actually executed Reptile-family runs, including preserved diagnostic failures, accounted')
    cleanup_path=ROOT/'audit_v5505_verified_old_release_copy_cleanup/result.json';cleanup=json.loads(cleanup_path.read_text())
    need(cleanup['passed']and cleanup['deletedDuplicateFiles']==42 and sha(cleanup['recoveryZIP'])==cleanup['recoveryZIPSHA256']and
         sha(cleanup['cleanupScript'])==cleanup['cleanupScriptSHA256'],'Exact recovery ZIP and executed cleanup script unchanged after42 duplicate deletions')
    copy=Path(cleanup['target']);remaining=list(copy.rglob('*'));remaining=[p for p in remaining if p.is_file()]
    need(len(remaining)==3 and {p.relative_to(copy).as_posix():sha(p)for p in remaining}==cleanup['preservedUniqueFiles'],
         'Only all three preserved unique config/NVRAM files remain in removed old extracted copy')
    for p in(FAILED,cleanup_path,Path(cleanup['recoveryZIP']),Path(cleanup['cleanupScript']),video,Path(__file__).resolve(),
             *(ROOT/'tools'/name for name in('verify_current_reptile_overlap_v5492.py','verify_current_reptile_overlap_v5495.py',
               'verify_current_reptile_p2_overlap_v5499.py','verify_current_reptile_p2_overlap_v5502.py')),
             *(ROOT/name for name in('mk2ks_current_reptile_overlap_v5492.lua','mk2ks_current_reptile_ram_v5483.lua')),
             *(ROOT/f'audit_v{v}_{name}/progress.json'for v,name in((5494,'current_reptile_overlap_progress'),
               (5497,'current_reptile_overlap_progress'),(5501,'current_reptile_overlap_progress')))):
        pins[str(p.resolve())]=sha(p)
    need(all(sha(p)==h for p,h in pins.items()),'All source/current/public/retained native evidence pins stable at qualified completion')
    return dict(passed=True,observedUTC=datetime.datetime.now(datetime.timezone.utc).isoformat(),goalStatus='active',
      parentAdditiveJournal=str(PARENT),remaining=parent['remaining'],previousGoalTurnClassification=parent['thisGoalTurnClassification'],
      thisGoalTurnClassification='progress: completed actual current Reptile victim matrix for own17/18 in both physical slots; original full controller/damage/head/body/palette/floor/FIFO/retirement gate, exact own art + individually native-ROM-owned blood overlap and12 complete hardware scanouts;84 native record and36 actual RAM counterexamples; native automatic screenshots accurately accounted, retained text compacted;42 archive-identical obsolete release copies removed,140MiB recovered with config/NVRAM/ZIP/source/public preserved',
      currentReptileVictimsBothCharactersBothSlotsAccepted=True,cases=cases,actualRequestedFrameCallbacks=124,
      exactWholeNativeScanoutPixels=1219200,effectiveActualNativeRecordFaults=84,effectiveActualPixelSourceAndOverlapFaults=36,
      actualEarlierAndCurrentTerminalRuns=terminal_runs,preservedActualNativeTimedExitImages=automatic_all,
      all31RequestedFrameBuffersPerCaseOnlyInRAM=True,guestGFXVRAMPalettePCMOrWAVRawFilesWritten=0,
      persistentNativeAutomaticPNGFiles=len(automatic_all),persistentNativeAutomaticPNGBytes=sum(r['bytes']for r in automatic_all),
      acceptedNativeBoots=4,newNativeBootsSinceParentThisTurn=7,earlierDiagnosticNativeBootsRetained=5,newNativeBootsForThisQualifier=0,
      newBuilds=0,cleanup=cleanup,terminalTextFilesLosslesslyCompacted=len(compacted),
      publicPlayableChanged=False,refreshedReleaseZIP=False,allFinishersOrAllVictimsAccepted=False,
      allArenasAccepted=False,completeReptileFinisherAudioAccepted=False,continuousWholeSceneRasterAccepted=False,
      fullPortAcceptance=False,newInputHashes=pins,
      nextAction='Continue remaining original native victim/finisher and arena/audio/CPU/secret/cinematic contexts; retain all five original remaining groups, then final combined acceptance and refreshed release promotion.')


if __name__=='__main__':
    need(not OUT.exists(),'Fresh immutable completed Reptile/additive-cleanup journal')
    try:report=run()
    except Exception as error:report=dict(passed=False,error=repr(error),goalStatus='active',fullPortAcceptance=False)
    OUT.mkdir();original.save(OUT/'progress.json',report)
    print(json.dumps({k:v for k,v in report.items()if k not in('cases','newInputHashes','remaining','actualEarlierAndCurrentTerminalRuns','preservedActualNativeTimedExitImages','cleanup')},indent=2),flush=True)
    raise SystemExit(0 if report['passed']else 1)
