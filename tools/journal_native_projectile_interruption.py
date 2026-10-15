"""Finite terminal projectile proofs, unchanged full objective and compact storage."""
import gzip,json,re,subprocess
from pathlib import Path
import kano_ball_launch_context_v6642 as current
import native_process_census_v6647 as process
from inventory_current_port_storage_v4200 import allocated
ROOT,need,sha=current.ROOT,current.need,current.sha
OUT=ROOT/'audit_native_projectile_interruption_progress_storage'

def main():
    need(not OUT.exists() and not process.census(),'Fresh journal and no native jobs')
    current.expected();pins={};migrations=[]
    parent_path=ROOT/'audit_native_input_correction_progress_storage/report.json'
    parent=json.loads(parent_path.read_text())
    need(parent['passed'] and len(parent['remaining'])==6,'Entire preceding objective remains')
    for p,h in parent['inputHashes'].items():
        path=Path(p).resolve()
        if path.parent==ROOT and path.name in ('CURRENT_PLAYTEST_STATUS.md','WORKSPACE_CLEANUP_CURRENT.md'):
            old=ROOT/'status_history_native_projectile_interruption'/path.name
            need(sha(old)==h,'Exact previous document bytes retained')
            migrations.append(dict(priorLogicalPath=str(path),priorSHA256=h,exactHistoricalBytes=str(old),currentSHA256=sha(path)))
            path=old
        need(sha(path)==h,'Protected prior pin unchanged: '+str(path));pins[str(path)]=h
    pins[str(parent_path)]=sha(parent_path)
    names=['audit_launch_fireball_faults_checked_bicycle_p1_delay1','audit_launch_fireball_faults_checked_bicycle_p2_delay1',
           'audit_launch_roll_fireball_checked_ball_p1_delay16','audit_launch_roll_fireball_checked_ball_p2_delay16']
    summaries=[];frames=hits=0
    for name in names:
        path=ROOT/name/'report.json';proof=json.loads(path.read_text())
        need(proof['passed'] and proof['candidate']==current.NAME and proof['nativeTerminal']['nativeExit']==0 and
             not proof['nativeTerminal']['hostDecodeErrors'] and not proof['fullPortAcceptance'] and
             not proof['fullInterruptionCoverageAccepted'] and not proof['fullRasterAcceptance'],'Finite terminal qualification, no full-port promotion')
        ownership=proof['physicalAndOwnership'];wave=proof['completeSourceWaveform']
        need(ownership['passed'] and ownership['wholePhysicalAndSourceBodyContract']['twoRealSpecialCyclesAndCleanupVerified'] and
             len(ownership['actualInterruptedCycles'])==2 and wave['passed'] and wave['differentChannelSamples']==0 and
             wave['actualSHA256']==wave['predictedSHA256'],'Whole two-hit recovery and exact complete source waveform')
        need(proof['physicalInputs']['realIN0IN2BitDelivery']['wholeBothPlayerPhysicalBitDeliveryAccepted'],'Whole actual physical button delivery')
        fault_counts=dict(semantic=len(proof['actualSemanticFaultsRejected']),waveform=len(wave['actualRawAndSourceFaultsRejected']),
                          dac=len(proof['actualDACFaultsRejected']),soundROM=len(proof['actualSoundROMFaultsRejected']))
        need(fault_counts==dict(semantic=25,waveform=8,dac=4,soundROM=8),'All original actual negative-control suites')
        need(all(c['healthBefore']-c['healthAfter']==22 for c in ownership['actualInterruptedCycles']),'Two genuine native projectile doses')
        frames+=wave['comparedStereoFrames'];hits+=len(ownership['actualInterruptedCycles'])
        summaries.append(dict(report=str(path),nativePID=proof['nativeTerminal']['pid'],cycles=ownership['actualInterruptedCycles'],
                              stereoFrames=wave['comparedStereoFrames'],rejectedActualFaults=fault_counts))
        pins[str(path)]=sha(path)
        for p,h in proof['inputHashes'].items():
            need(sha(p)==h,'Actual executed source/capture/asset unchanged: '+p);pins[p]=h
    need(frames==2137920 and hits==8,'All four entire native waveform windows and eight genuine incoming hits')
    attempts=[]
    capture_names=['audit_launch_fireball_counter_bicycle_p1_delay1','audit_launch_fireball_counter_bicycle_p2_delay1',
                   'audit_launch_low_fireball_counter_ball_p1_delay16','audit_launch_low_fireball_counter_ball_p2_delay16',
                   'audit_launch_fireball_counter_ball_p2_delay20']
    for name in capture_names:
        folder=ROOT/name;terminal=json.loads((folder/'native_terminal.json').read_text());report=json.loads((folder/'report.json').read_text())
        need(terminal['nativeExit']==0 and not terminal['hostDecodeErrors'] and report['passed'] and report['transportOnlyAccepted'],'Actual clean terminal transport')
        with gzip.open(folder/'run.log.gz','rt',encoding='utf-8') as log: text=log.read()
        health=[dict(re.findall(r'(\w+)=([^\s]+)',s)) for s in text.splitlines() if s.startswith('MK2_INTERRUPT_HEALTH ')]
        incoming=[r for r in health if int(r['slot'])==report['side'] and int(r['after'])<int(r['before'])]
        unexercised=name=='audit_launch_fireball_counter_ball_p2_delay20'
        need(len(incoming)==(0 if unexercised else 2),'Actual complete incoming health ledger, no unlanded green test')
        attempts.append(dict(folder=str(folder),nativePID=terminal['pid'],nativeExit=0,incomingHealthStores=incoming,
                             classification='unexercised: roll hit before high-fireball release' if unexercised else 'two genuine contacts, complete source qualification',
                             gameplayInterruptionAccepted=not unexercised))
    source_names=['mk2ks_launch_fireball_counter.lua','mk2ks_launch_low_fireball_counter.lua',
                  'tools/capture_launch_fireball_counter.py','tools/capture_launch_low_fireball_counter.py',
                  'tools/launch_fireball_interruption_model.py','tools/qualify_launch_fireball_interruption.py',
                  'tools/qualify_launch_fireball_faults.py','tools/launch_roll_fireball_model.py',
                  'tools/qualify_launch_roll_fireball.py','tools/journal_native_projectile_interruption.py']
    leaves=[ROOT/name for name in names+capture_names]+[ROOT/'audit_launch_fireball_fault_adapter_rejection',
           ROOT/'audit_launch_low_descriptor_scope_rejection',ROOT/'status_history_native_projectile_interruption']
    files={p for leaf in leaves for p in leaf.rglob('*') if p.is_file()}
    files.update(ROOT/name for name in source_names+['CURRENT_PLAYTEST_STATUS.md','WORKSPACE_CLEANUP_CURRENT.md'])
    need(all(p.resolve().is_relative_to(ROOT) and not p.is_symlink() for p in files),'Exact finite compression paths within named port')
    need(not any(p.suffix.lower() in ('.png','.wav','.bin','.exe','.zip') for p in files),'No raw media/build/ROM/ZIP compression allocations')
    storage=[];seen=set();total=0
    for p in sorted(files):
        h=sha(p);stat=p.stat();key=stat.st_dev,stat.st_ino;before=allocated(p)
        need(subprocess.run(['compact.exe','/C','/EXE:LZX','/F','/I','/Q',str(p)],capture_output=True).returncode==0 and sha(p)==h,'Lossless exact-target compression')
        after=allocated(p);unique=key not in seen;seen.add(key)
        if unique:total+=after
        storage.append(dict(path=str(p),sha256=h,logicalBytes=stat.st_size,beforeAllocatedBytes=before,allocatedBytes=after,uniqueSelectedAllocation=unique));pins[str(p)]=h
    builds=[p for p in ROOT.iterdir() if p.is_dir() and (p/'mkport_candidate.exe').is_file()]
    launcher=ROOT/'PLAY_MK2_KANO_SONYA.cmd';checked=ROOT/'PLAY_CURRENT_V6508_CHECKED.cmd'
    need(launcher.read_text().count('PLAY_CURRENT_V6508_CHECKED.cmd')==1 and
         'diagnostic_v6508_native_projectile_identifiers' in checked.read_text() and
         'diagnostic_v6640' not in launcher.read_text()+checked.read_text(),'Normal launcher unchanged on checked v6508')
    for p in (launcher,checked):pins[str(p)]=sha(p)
    need(len(builds)==16 and not (ROOT/'mame-mkp/build/mingw-gcc').exists() and not process.census(),'Sixteen retained builds, no compiler cache or native jobs')
    need(all(sha(p)==h for p,h in pins.items()),'All protected source/evidence bytes unchanged')
    report=dict(passed=True,goalStatus='active',fullPortAcceptance=False,remaining=parent['remaining'],candidate=current.NAME,
                finiteProofs=summaries,actualNativeAttempts=attempts,genuineNewIncomingHitInterruptions=hits,completeStereoFrames=frames,
                actualFaultsRejected=dict(semantic=100,waveform=32,dac=16,soundROM=32),unexercisedAttempts=1,
                publicPlayableChanged=False,allFiveRAMHostsReleasedAfterProofOrDiagnosis=True,
                previousSubstantiveGoalTurnClassification='progress: actual input provenance, complete native close recovery and actual faults',
                thisGoalTurnClassification='progress: eight genuine both-slot roll/Bicycle incoming hits, full physical/body recovery, exact source stops and complete audio, all negative controls',
                nextAction='Audit overlap/relaunch/KO/selection/reset/morph ownership and current full UI/ground/render/audio; retain all original integration and matching release requirements.',
                intentionalDocumentationPinMigrations=migrations,inputHashes=pins,exactCompressedTargets=storage,
                selectedFileCount=len(files),uniqueSelectedAllocatedBytes=total,retainedCompiledCandidates=len(builds),compilerCacheAbsent=True,
                newNativeBootsThisGoalTurn=5,newBuilds=0,newROMCopies=0,newZIPs=0,newRawMedia=0,deletedOldArtifacts=0)
    OUT.mkdir();p=OUT/'report.json';p.write_text(json.dumps(report,indent=2)+'\n');h=sha(p)
    need(subprocess.run(['compact.exe','/C','/EXE:LZX','/F','/I','/Q',str(p)],capture_output=True).returncode==0 and sha(p)==h,'Lossless finite journal')
    print(json.dumps({k:report[k] for k in ('passed','genuineNewIncomingHitInterruptions','completeStereoFrames','selectedFileCount','uniqueSelectedAllocatedBytes','newBuilds','publicPlayableChanged')}),flush=True)

if __name__=='__main__':main()
