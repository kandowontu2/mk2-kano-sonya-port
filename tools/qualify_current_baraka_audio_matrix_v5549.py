"""Qualify actual both-slot/both-victim Baraka audio, no additional boot.

Combine the retained first pair with six new native captures. Every original
physical/exact14-part art gate, whole paired PCM/packet gate and source-owned
voice/effect gate remains required. Account all eight exit PNGs, compact logs.
Original DCS waveform and unobserved queue-suppression fidelity stay pending.
"""
import datetime,json,subprocess,traceback
from pathlib import Path
from PIL import Image
import current_baraka_audio_matrix_v5546 as matrix

ROOT,need,sha=matrix.ROOT,matrix.need,matrix.sha
PARENT=matrix.PARENT
PAIRS=ROOT/'audit_v5553_current_baraka_audio_records_progress'
ACCEPTED=PAIRS/'progress.json'
OUT=ROOT/'audit_v5550_current_baraka_audio_matrix_qualified'
BASES=[ROOT/'audit_v5538_current_baraka_audio_ram',matrix.BASE]


def run():
    matrix.capture.original.model.current.expected()
    parent=json.loads(PARENT.read_text());accepted=json.loads(ACCEPTED.read_text())
    need(parent['passed']and parent['goalStatus']=='active'and accepted['passed']and accepted['goalStatus']=='active'
         and accepted['parentAdditiveJournal']==str(PARENT)and accepted['remaining']==parent['remaining']
         and accepted['newNativeBoots']==6 and accepted['reusedPriorAcceptedNativeBoots']==2
         and accepted['allNormalVictimSlotsNativeBarakaVoiceEffectAndPacketDeliveryAccepted'],
         'Retain actual extended matrix, prior first pair, and complete original remaining requirements')
    pins=dict(parent['newInputHashes']);pins.update(accepted['newInputHashes'])
    for p in(PARENT,ACCEPTED,Path(__file__),Path(matrix.__file__)):pins[str(p.resolve())]=sha(p)
    contexts=[];terminal=[];pngs=[];compacted=[];phase_faults=[]
    for fighter in('kano','sonya'):
        for side in(1,2):
            reused=fighter=='kano'and side==1
            base=BASES[0]if reused else BASES[1]
            if reused:
                route_records=[c['routes']for c in parent['cases']]
                need(len(route_records)==2 and all(r['passed']and r['fighter']==fighter and r['side']==side for r in route_records),
                     'Only exact retained original current Kano-P1 pair reused, never another victim/slot')
                source_fault_count=sum(len(c['faults'])for c in parent['cases'])
            else:
                pair_path=PAIRS/f'{fighter}_p{side}_paired.json';pair=json.loads(pair_path.read_text())
                matches=[c for c in accepted['cases']if c['fighter']==fighter and c['side']==side]
                need(len(matches)==1 and pair==matches[0],'Fresh context sidecar exactly equals authoritative executed comparison result')
                pins[str(pair_path.resolve())]=sha(pair_path)
                need(pair['passed']and pair['fighter']==fighter and pair['side']==side
                     and pair['pairedNativeAudio']['passed']and pair['pairedNativeAudio']['fullNativePCMOnOffExactlyEqual']
                     and pair['entireOriginalPhysicalAndExactFourteenPartRasterGatesRetained'],
                     'Exact actual paired context and full original native/raster/whole PCM gates')
                route_records=[r['routes']for r in pair['sourceBoundVoiceEffectRoutes']]
                source_fault_count=sum(len(r['effectiveActualRouteFaults'])for r in pair['sourceBoundVoiceEffectRoutes'])
                need(len(route_records)==2 and all(r['passed']and r['fighter']==fighter and r['side']==side for r in route_records),
                     'Both true victim/player-slot original source voice/gender/blade delivery gates retained')
            need(source_fault_count==20,'Entire actual source/voice/owner/queue/packet fault suite per context')
            records=[]
            for suffix in('samples','nosamples'):
                folder=base/f'{fighter}_p{side}_{suffix}';meta=json.loads((folder/'result.json').read_text())
                process=meta['process'];native=json.loads((folder/'process.json').read_text());log=(folder/'run.log').read_text()
                need(meta['passed']and process['exit_code']==0 and process['nativePID']==native['pid']
                     and process['player']==fighter and process['victim_slot']==side and process['winner_slot']==3-side
                     and process['candidate']==matrix.capture.original.model.current.NAME
                     and process['executable_sha256']==matrix.capture.original.model.current.EXE_SHA
                     and process['payload_sha256']==matrix.capture.original.model.current.PAYLOAD_SHA
                     and process['assistance']=='none'and not process['cheats_enabled']
                     and process['killer']=='baraka'and process['command']=='bbbb_hp'and process['target_gap']==64
                     and process['entireOriginal921PhysicalControllerRetained']and meta['samplesEnabled']==(suffix=='samples'),
                     'Each actual current native true-ID/physical/input/sample/process context exact')
                need(all(sha(p)==h for p,h in process['input_hashes'].items()),'All actually executed immutable input hashes still exact')
                pins.update(process['input_hashes'])
                need('MK2_STOCK_HEAD_V921_RESULT frame=5198'in log and 'Average speed:'in log and not(folder/'stderr.log').read_text(),
                     'Every actual native run genuinely completed5198 and terminal0, not observation expiry')
                state=meta['actualNativeContract'];visual=meta['actualNativeHeadBodyPixelsAndScanout']
                need(state['damage']==322 and state['nativeWrapAge']==174 and state['headPoses']==state['bodyPoses']==list(range(7))
                     and state['groundedBodyDMAs']>100 and state['hardwarePaletteDumps']==14 and state['posePictures']==14
                     and state['periodicPictures']==61 and len(meta['effectiveActualNativeRecordFaults'])==15
                     and visual['passed']and visual['everyEmittedOwnedHeadBodyAndLegitimateForegroundPixelExact']
                     and len(visual['parts'])==14 and visual['wholeNativeScanoutPixels']==1422400
                     and len(meta['actualDisplayHeaders'])==125,
                     'Full original physical/rotation/collapse/palette/ground/cleanup and exact14 native scanouts retained')
                coverage=matrix.phase.coverage(log,meta)
                chunk=next(s for s in log.splitlines()if s.startswith('MK2_BBAUDIO_PCM_DIGEST '))
                damaged=matrix.capture.re.sub(r'frame=\d+','frame=0',chunk,count=1)
                for label,bad in(('actual sound callback omitted',log.replace(chunk+'\n','',1)),
                                  ('actual sound callback video label corrupted',log.replace(chunk,damaged,1))):
                    try:matrix.phase.coverage(bad,meta)
                    except ValueError as error:phase_faults.append(dict(fighter=fighter,side=side,suffix=suffix,label=label,rejectedBy=str(error)))
                    else:raise ValueError('Accepted actual audio timer coverage fault')
                need(matrix.phase.coverage(log,meta)==coverage,'Entire actual timer coverage positive restored after effective faults')
                records.append(dict(result=str(folder/'result.json'),resultSHA256=sha(folder/'result.json'),nativePID=native['pid'],nativeExit=0,
                    physical=state,visual=visual,coverage=coverage,actualPCMUpdates=meta['actualPCMUpdates'],actualPCMBytes=meta['actualPCMBytes'],
                    actualMixedPCMSHA256=meta['actualMixedPCMSHA256'],actualWholeDisplayedFrames=125,effectiveNativeRecordFaults=15))
                terminal.append(dict(folder=str(folder),nativePID=native['pid'],nativeExit=0,terminalField=5198))
                for p in folder.rglob('*'):
                    if not p.is_file():continue
                    need(p.suffix.lower()not in('.bin','.wav','.rgb','.pcm'),'No requested guest/raster/audio buffers persisted')
                    if p.suffix.lower()=='.png':
                        with Image.open(p)as im:need(p==folder/'snap/mk2ks/0000.png'and im.size==(400,254),
                            'Only accurately accounted original native timed-exit PNG')
                        pngs.append(dict(path=str(p),bytes=p.stat().st_size,sha256=sha(p)))
                    if p.suffix.lower()in('.log','.json','.cfg'):
                        before=sha(p);cp=subprocess.run(['compact.exe','/C','/EXE:LZX','/I','/Q',str(p)],capture_output=True)
                        need(cp.returncode==0 and sha(p)==before,'Retained native terminal text losslessly compacted');compacted.append(str(p))
                    pins[str(p.resolve())]=sha(p)
            need(records[0]['actualMixedPCMSHA256']==records[1]['actualMixedPCMSHA256']and
                 records[0]['actualPCMUpdates']==records[1]['actualPCMUpdates']and records[0]['actualPCMBytes']==records[1]['actualPCMBytes'],
                 'Exact actual full joined native waveforms/update counts/byte counts match paired proof')
            contexts.append(dict(fighter=fighter,side=side,reusedPriorPair=reused,nativeRuns=records,
                nativeSourceVoiceEffectRoutes=route_records,effectiveActualRouteFaults=20))
    need(len(terminal)==len(pngs)==8 and len(phase_faults)==16 and all(sha(p)==h for p,h in pins.items()),
         'All eight actual native runs/automatic PNGs,16effective phase faults, unchanged current/public/source/evidence')
    return dict(passed=True,observedUTC=datetime.datetime.now(datetime.timezone.utc).isoformat(),goalStatus='active',remaining=parent['remaining'],
        parentAdditiveJournal=str(PARENT),previousGoalTurnClassification=parent['thisGoalTurnClassification'],
        thisGoalTurnClassification='progress: actual current normal Baraka both true victims/both physical slots, eight samples-on/off full native physical/raster/PCM/packet/ADSP recordings; source-owned death/gender/player voice and original blade effect and selected command tables/queues;120native record,80source-route,16actual timer faults;112exact owned-phase hardware scanouts,1000actual whole displayed frames; all eight native exit PNGs accounted and retained text compacted',
        contexts=contexts,actualNativeTerminalRuns=terminal,persistentNativeAutomaticExitPNGs=pngs,
        persistentNativeAutomaticPNGFiles=8,persistentNativeAutomaticPNGBytes=sum(p['bytes']for p in pngs),
        actualNativePairedContexts=4,actualAcceptedNativeRecordings=8,actualWholeDisplayedFrameCallbacks=1000,
        exactWholeNativeOwnedPhaseScanoutPixels=11379200,effectiveActualNativeRecordFaults=120,
        effectiveActualSourceVoiceEffectRouteFaults=80,effectiveActualAudioTimerFaults=16,actualAudioTimerFaults=phase_faults,
        effectiveActualAdditionalPairedRecordFaults=accepted['effectiveActualPairedRecordFaults'],
        newNativeBootsSinceParentThisTurn=6,reusedPriorAcceptedNativeBoots=2,newNativeBootsForQualifier=0,
        newBuilds=0,newDeletedFiles=0,terminalTextFilesLosslesslyCompacted=len(compacted),
        requestedGuestGFXVRAMPaletteRGBPCMOrWAVFilesWritten=0,publicPlayableChanged=False,refreshedReleaseZIP=False,
        allNormalVictimSlotsNativeBarakaVoiceEffectAndPacketDeliveryAccepted=True,
        allNativeQueueSuppressionCausesAccepted=False,sourceQualifiedNativeDCSWaveformAccepted=False,
        completeBarakaFinisherAudioAccepted=False,allArenasAndCostumesAccepted=False,fullPortAcceptance=False,newInputHashes=pins,
        nextAction='Independently qualify actual original DCS waveform and omitted queue branches, then continue all original finisher/stage/CPU/campaign/UI requirements and complete applicable release acceptance.')


if __name__=='__main__':
    need(not OUT.exists(),'Fresh immutable completed both-slot/victim native audio matrix qualification')
    try:report=run()
    except Exception as error:report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),goalStatus='active',fullPortAcceptance=False)
    OUT.mkdir();matrix.capture.save(OUT/'progress.json',report)
    print(json.dumps({k:v for k,v in report.items()if k not in('remaining','contexts','newInputHashes','actualNativeTerminalRuns',
        'persistentNativeAutomaticExitPNGs','actualAudioTimerFaults')},indent=2),flush=True)
    raise SystemExit(0 if report['passed']else 1)
