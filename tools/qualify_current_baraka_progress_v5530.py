"""Qualify the executed Baraka matrix without another boot or build.

Retain the failed allocated-palette model and all five native terminal runs.
Account native timed-exit PNGs and compact retained text without changing bytes.
This is normal-costume Dead Pool evidence, not whole-port acceptance.
"""
import datetime,json,subprocess,traceback
from pathlib import Path
from PIL import Image
import current_baraka_source_contract_v5521 as model

ROOT,need,sha=model.ROOT,model.need,model.sha
PARENT=ROOT/'audit_v5520_current_cage_sections_qualified_progress/progress.json'
ACCEPTED=ROOT/'audit_v5529_current_baraka_pixels_progress/progress.json'
FAILED=ROOT/'audit_v5525_current_baraka_pixels_progress/progress.json'
OUT=ROOT/'audit_v5531_current_baraka_qualified_progress'
LEAVES=[ROOT/f'audit_v{v}_current_baraka_pixels_ram'for v in(5524,5528)]


def run():
    model.current.expected()
    parent=json.loads(PARENT.read_text());accepted=json.loads(ACCEPTED.read_text())
    failure=json.loads(FAILED.read_text());_,physical_sha=model.physical_contract()
    need(parent['passed']and parent['goalStatus']=='active'and accepted['passed']and accepted['goalStatus']=='active'
         and accepted['remaining']==parent['remaining']and accepted['parentAdditiveJournal']==str(PARENT),
         'Original full remaining scope and actual completed native matrix retained')
    need(accepted['currentNormalBarakaBothVictimsBothSlotsAccepted']and accepted['newNativeBoots']==4
         and accepted['newBuilds']==0 and not accepted['fullPortAcceptance'],
         'Four current normal victim contexts, no game build or broad acceptance claim')
    need(not failure['passed']and not failure['completedCases']and
         failure['error']=="ValueError('Other legitimate occluder is true original Baraka, never substituted victim art')",
         'Preserve actual stricter verifier counterexample, not silently discarded evidence')
    pins=dict(parent['newInputHashes']);pins.update(accepted['newInputHashes'])
    for p in(PARENT,ACCEPTED,FAILED,Path(__file__)):pins[str(p.resolve())]=sha(p)
    cases=[]
    for fighter in('kano','sonya'):
        for side in(1,2):
            folder=LEAVES[-1]/f'{fighter}_p{side}';path=folder/'result.json';c=json.loads(path.read_text())
            process=c['process'];before=json.loads((folder/'input_hashes_before.json').read_text())
            need(c['passed']and process['exit_code']==0 and process['player']==fighter and process['victim_slot']==side
                 and process['winner_slot']==3-side and process['candidate']==model.current.NAME
                 and process['executable_sha256']==model.current.EXE_SHA and process['payload_sha256']==model.current.PAYLOAD_SHA
                 and process['input_hashes']==before and process['entireOriginal921PhysicalControllerRetained']
                 and process['killer']=='baraka'and process['command']=='bbbb_hp'and process['target_gap']==64
                 and process['assistance']=='none'and not process['cheats_enabled'],
                 'True-ID native original-controller context/process/immutable inputs')
            need(all(sha(p)==h for p,h in before.items()),'Executed source/public/asset inputs still exact')
            pins.update(before)
            physical=c['actualNativeContract'];visual=c['actualNativeHeadBodyPixelsAndScanout']
            need(c['originalFullPhysicalArtContractSHA256']==physical_sha and physical['victim']==fighter
                 and physical['slot']==side and physical['damage']==322 and physical['nativeWrapAge']==174
                 and physical['headPoses']==physical['bodyPoses']==list(range(7))and physical['ownedDMAs']>1000
                 and physical['groundedBodyDMAs']>100 and physical['hardwarePaletteDumps']==14
                 and physical['posePictures']==14 and physical['periodicPictures']==61
                 and len(physical['pixelMatches'])==14 and all(p['exactRasterGateRequired']for p in physical['pixelMatches']),
                 'Entire original native health/parser/Block/head/body/floor/palette/cleanup criteria')
            ages={'head':[59,64,68,72,76,80,84],'body':[59,107,113,119,185,191,197]}
            need(all(physical['firstPoseAges'][kind][str(p)]==age+side-1
                     for kind,values in ages.items()for p,age in enumerate(values)),
                 'Every original native first phase timing retained for physical side')
            need(len(c['effectiveActualNativeRecordFaults'])==15 and len(c['actualDisplayHeaders'])>=75,
                 'Actual native-record counterexamples and original requested pictures retained')
            parts=visual['parts']
            need(visual['passed']and visual['everyEmittedOwnedHeadBodyAndLegitimateForegroundPixelExact']
                 and len(parts)==14 and {(p['kind'],p['pose'])for p in parts}=={(k,p)for k in('head','body')for p in range(7)}
                 and visual['wholeNativeScanoutPixels']==1422400
                 and all(p['passed']and p['pixels']==101600 and p['ownVisiblePixels']>10
                         and p['ownVisiblePixels']+p['ownedNativeOccludedPixels']==p['originalOpaquePixels']for p in parts),
                 'All fourteen whole actual scanouts and every source-owned emitted/occluded pixel exact')
            faults=visual['effectiveActualRAMFaults']
            need(len(faults)==28+sum(p['ownedNativeOccludedPixels']>0 for p in parts)
                 and all(sum(f['kind']==p['kind']and f['pose']==p['pose']for f in faults)==
                         2+(p['ownedNativeOccludedPixels']>0)for p in parts),
                 'Effective pen/RGB faults per phase and overlap faults per genuinely occluded part')
            kinds={kind for p in parts for kind in p['nativeOccluders'].values()}
            need({f['kind']for f in visual['effectiveActualNativeForegroundOwnerFaults']}==kinds
                 and len(visual['effectiveActualNativeForegroundOwnerFaults'])==len(kinds),
                 'Whole verifier rejects actual foreign identity for every native foreground type')
            cases.append(dict(result=str(path),resultSHA256=sha(path),fighter=fighter,side=side,nativePID=process['nativePID'],
                nativeExit=0,originalFullPhysicalArtContractSHA256=physical_sha,physical=physical,
                actualNativeHeadBodyPixelsAndScanout=visual,actualRequestedRAMFrames=len(c['actualDisplayHeaders']),
                effectiveActualNativeRecordFaults=15))
    terminal=[];automatic=[];compacted=[]
    for leaf in LEAVES:
        need(leaf.is_dir(),'Preserve actual captures and executed verifier failure')
        for folder in sorted(p for p in leaf.iterdir()if p.is_dir()and(p/'process.json').is_file()):
            process=json.loads((folder/'process.json').read_text());result=json.loads((folder/'terminal.json').read_text())
            log=(folder/'run.log').read_text()
            need(result['exit_code']==0 and result['nativePID']==process['pid']and
                 'MK2_STOCK_HEAD_V921_RESULT frame=5198'in log and 'damage=322 wins=2'in log
                 and 'Average speed:'in log and not(folder/'stderr.log').read_text(),
                 'Actual process genuinely terminal0, not an expired observation or missing runtime')
            terminal.append(dict(folder=str(folder),pid=process['pid'],terminalField=5198,nativeExit=0,
                acceptedGameplayAndPixelCase=(folder/'result.json').is_file()))
            for p in folder.rglob('*'):
                if not p.is_file():continue
                need(p.suffix.lower()not in('.bin','.wav','.rgb','.pcm'),'No persistent raw requested RAM buffers')
                if p.suffix.lower()=='.png':
                    with Image.open(p)as im:need(p==folder/'snap/mk2ks/0000.png'and im.size==(400,254),
                        'Only explicitly accounted native timed-exit screenshot')
                    automatic.append(dict(path=str(p),bytes=p.stat().st_size,sha256=sha(p)))
                if p.suffix.lower()in('.log','.json','.txt','.cfg'):
                    before=sha(p);cp=subprocess.run(['compact.exe','/C','/EXE:LZX','/I','/Q',str(p)],capture_output=True)
                    need(cp.returncode==0 and sha(p)==before,'Lossless native terminal evidence compression')
                    compacted.append(str(p))
                pins[str(p.resolve())]=sha(p)
    need(len(terminal)==len(automatic)==5 and sum(c['acceptedGameplayAndPixelCase']for c in terminal)==4,
         'All five actual boots, including preserved verifier failure, and native exit PNGs accounted')
    for p in(ROOT/'tools/current_baraka_source_contract_v5521.py',ROOT/'mk2ks_current_baraka_ram_v5522.lua',
              ROOT/'tools/verify_current_baraka_pixels_v5523.py',ROOT/'tools/inspect_current_baraka_foreground_v5526.py',
              ROOT/'tools/verify_current_baraka_pixels_v5527.py'):
        pins[str(p.resolve())]=sha(p)
    need(all(sha(p)==h for p,h in pins.items()),'Source/public/art/current ROM/evidence hashes stable at completed qualification')
    frames=sum(c['actualRequestedRAMFrames']for c in cases)
    ram_faults=sum(len(c['actualNativeHeadBodyPixelsAndScanout']['effectiveActualRAMFaults'])for c in cases)
    owner_faults=sum(len(c['actualNativeHeadBodyPixelsAndScanout']['effectiveActualNativeForegroundOwnerFaults'])for c in cases)
    need(frames==accepted['actualRequestedRAMDisplayCallbacks']and ram_faults==accepted['effectiveActualRAMFaults']
         and owner_faults==accepted['effectiveActualNativeForegroundOwnerFaults']
         and accepted['exactWholeNativeScanoutPixels']==5689600 and accepted['effectiveActualNativeRecordFaults']==60,
         'Aggregate counts agree with actual accepted four-case evidence')
    return dict(passed=True,observedUTC=datetime.datetime.now(datetime.timezone.utc).isoformat(),goalStatus='active',
        remaining=parent['remaining'],parentAdditiveJournal=str(PARENT),parentJournalClassification=parent['thisGoalTurnClassification'],
        previousGoalTurnClassification='progress: retained executed native palette-allocation counterexample and independently corrected the exact original gore allocation verifier; started the current four-case physical matrix',
        thisGoalTurnClassification='progress: completed actual current normal Baraka decapitation matrix for both true-ID victims in both slots; entire original physical control/health/parser/palette/FIFO/head rotations/body collapse/floor/cleanup contract; 56 exact native scanouts, every emitted pixel and source-owned native foreground; actual record/RAM/full-foreground identity faults; preserved executed palette-allocation verifier failure; all five native terminal PNGs accounted and terminal text losslessly compacted',
        currentNormalBarakaBothVictimsBothSlotsAccepted=True,cases=cases,
        independentCurrentSourceArtReference=accepted['independentSourceArtReference'],
        actualAcceptedRequestedRAMDisplayCallbacks=frames,exactWholeNativeScanoutPixels=5689600,
        effectiveActualNativeRecordFaults=60,effectiveActualComponentRGBAndOverlapRAMFaults=ram_faults,
        effectiveActualNativeForegroundOwnerFaults=owner_faults,actualNativeTerminalRuns=terminal,
        persistentNativeAutomaticExitPNGs=automatic,persistentNativeAutomaticPNGFiles=5,
        persistentNativeAutomaticPNGBytes=sum(p['bytes']for p in automatic),requestedGuestGFXVRAMPaletteRGBPCMWAVFilesWritten=0,
        newNativeBootsSinceParentThisWork=5,acceptedNativeBoots=4,preservedVerifierFailureNativeBoots=1,newNativeBootsForQualifier=0,
        newBuilds=0,newDeletedFiles=0,terminalTextFilesLosslesslyCompacted=len(compacted),publicPlayableChanged=False,
        refreshedReleaseZIP=False,allFinisherVictimArenaOrCostumeContextsAccepted=False,allArenasAccepted=False,
        completeBarakaFinisherAudioAccepted=False,
        continuousWholeSceneRasterAccepted=False,fullPortAcceptance=False,newInputHashes=pins,
        nextAction='Continue remaining original finisher/victim/arena/audio/CPU/secret/cinematic contexts; retain all five remaining groups, then combined acceptance and refreshed public release.')


if __name__=='__main__':
    need(not OUT.exists(),'Fresh immutable completed Baraka/full-scope qualification')
    try:report=run()
    except Exception as error:report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),goalStatus='active',fullPortAcceptance=False)
    OUT.mkdir();(OUT/'progress.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in report.items()if k not in('remaining','cases','newInputHashes','actualNativeTerminalRuns',
        'persistentNativeAutomaticExitPNGs','independentCurrentSourceArtReference')},indent=2),flush=True)
    raise SystemExit(0 if report['passed']else 1)
