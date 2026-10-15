"""Exact finite counter work, full-goal carry-forward and lossless compression.

Accepted input/recovery evidence is not incoming-hit or release acceptance.
Preserve every failed source/capture/report and all prior original scope.
"""
import gzip,json,re,subprocess
from pathlib import Path
import kano_ball_launch_context_v6642 as current
import native_process_census_v6647 as process
from inventory_current_port_storage_v4200 import allocated
ROOT,need,sha=current.ROOT,current.need,current.sha
OUT=ROOT/'audit_native_input_correction_progress_storage'

def main():
    need(not OUT.exists() and not process.census(),'Fresh journal; authoritative native census empty')
    current.expected();pins={};migrations=[]
    parent_path=ROOT/'audit_v6702_launch_interruption_progress_storage_checked/report.json'
    parent=json.loads(parent_path.read_text());need(parent['passed'] and len(parent['remaining'])==6,'Whole objective carried forward')
    for p,h in parent['inputHashes'].items():
        path=Path(p).resolve()
        if path.parent==ROOT and path.name in ('CURRENT_PLAYTEST_STATUS.md','WORKSPACE_CLEANUP_CURRENT.md'):
            old=ROOT/'status_history_native_input_correction'/path.name
            need(sha(old)==h,'Exact preceding documentation recovered, not edited old evidence')
            migrations.append(dict(priorLogicalPath=str(path),priorSHA256=h,exactHistoricalBytes=str(old),currentSHA256=sha(path)))
            path=old
        need(sha(path)==h,'Protected prior source/evidence pin intact: '+str(path));pins[str(path)]=h
    pins[str(parent_path)]=sha(parent_path)
    proof_paths=[ROOT/'audit_native_input_delivery_address_correction/report.json',
                 ROOT/'audit_native_close_recovery_checked/report.json',ROOT/'audit_native_close_recovery_faults/report.json']
    proofs=[json.loads(p.read_text()) for p in proof_paths]
    need(all(p['passed'] and not p['fullPortAcceptance'] and not p['gameplayInterruptionAccepted'] for p in proofs),'Three finite evidence receipts, no interruption or release promotion')
    delivery=proofs[0]['nativeInputDelivery']
    need(delivery['completeNativeReads']=={'01600000':2264,'01600020':1164} and delivery['completeIRQFields']=={'01600000':668,'01600020':668},'Whole actual both-slot bit delivery')
    need(not proofs[0]['unchangedWholeRecoveryQualifier']['passed'] and proofs[1]['wholePhysicalAndBodyContract']['twoRealSpecialCyclesAndCleanupVerified'] and
         len(proofs[2]['actualSemanticFaultsRejected'])==4,'Preserved standing-jab rejection, actual corrected full recovery and four native-close faults')
    for path,proof in zip(proof_paths,proofs,strict=True):
        pins[str(path)]=sha(path)
        for p,h in proof['inputHashes'].items():need(sha(p)==h,'Actual executed qualifier/capture/candidate source intact: '+p);pins[p]=h
    attempt_names=[
        'audit_v6705_launch_ground_counter_ball_p1_delay6','audit_v6705_launch_ground_counter_ball_p1_delay12',
        'audit_v6705_launch_ground_counter_bicycle_p1_delay9','audit_v6685_launch_precrouch_ball_p1_delay7',
        'audit_v6708_launch_ground_io_bicycle_p1_delay12','audit_v6711_launch_ground_io_fixed_bicycle_p1_delay12',
        'audit_v6711_launch_ground_io_fixed_bicycle_p1_delay18','audit_v6711_launch_ground_io_fixed_bicycle_p1_delay22',
        'audit_v6718_roll_block_counter_ball_p1_delay24','audit_launch_jump_io_bicycle_p2_delay1',
        'audit_launch_jump_io_bicycle_p2_delay18','audit_launch_jump_late_bicycle_p2_delay1']
    attempts=[]
    for name in attempt_names:
        folder=ROOT/name;terminal=json.loads((folder/'native_terminal.json').read_text());report=json.loads((folder/'report.json').read_text())
        need(not terminal['hostDecodeErrors'],'All actual observer transports decoded without hidden error')
        with gzip.open(folder/'run.log.gz','rt',encoding='utf-8') as log:text=log.read()
        if terminal['nativeExit']==3:
            need(name=='audit_v6708_launch_ground_io_bicycle_p1_delay12' and not report['passed'] and
                 'attempt to perform arithmetic on a string value' in (folder/'stderr.log').read_text(),'Exact saved actual observer error retained')
            incoming=[];classification='failed observer boot, not gameplay acceptance'
        else:
            need(terminal['nativeExit']==0 and report['passed'] and report['transportOnlyAccepted'] and not report['gameplayInterruptionAccepted'],'Actual terminal transport-only scope')
            health=[dict(re.findall(r'(\w+)=([^\s]+)',s)) for s in text.splitlines() if s.startswith('MK2_INTERRUPT_HEALTH ')]
            incoming=[r for r in health if int(r['slot'])==report['side'] and int(r['after'])<int(r['before'])]
            need(not incoming,'Do not silently miss a genuine native interruption requiring separate qualification')
            classification='unexercised for incoming-hit interruption: no actual incoming health store'
        attempts.append(dict(folder=str(folder),nativePID=terminal['pid'],nativeExit=terminal['nativeExit'],classification=classification,
                             incomingHealthStores=incoming,gameplayInterruptionAccepted=False))
    need(len(attempts)==12 and sum(a['nativeExit']==0 for a in attempts)==11,'All twelve actual attempts, eleven normal terminals and one actual observer failure')
    leaves=[ROOT/name for name in attempt_names]+[p.parent for p in proof_paths]+[
        ROOT/'source_history_v6714',ROOT/'audit_v6714_input_inventory_rejection',ROOT/'status_history_native_input_correction']
    source_names=['tools/save_native_input_delivery_receipt.py','tools/qualify_native_close_recovery.py','tools/check_native_close_recovery_faults.py',
                  'tools/capture_launch_jump_io.py','tools/capture_launch_jump_late.py','tools/journal_native_input_correction.py',
                  'mk2ks_launch_jump_io.lua','mk2ks_launch_jump_late.lua']
    def version(p):
        match=re.search(r'_v(\d+)',p.name);return int(match[1]) if match else -1
    files={p for leaf in leaves for p in leaf.rglob('*') if p.is_file()}
    files.update(ROOT/name for name in source_names)
    files.update(p for base in (ROOT,ROOT/'tools') for p in base.iterdir() if p.is_file() and 6703<=version(p)<=6717)
    files.update(ROOT/name for name in ('CURRENT_PLAYTEST_STATUS.md','WORKSPACE_CLEANUP_CURRENT.md'))
    need(all(p.resolve().is_relative_to(ROOT) and not p.is_symlink() for p in files),'All exact finite resolved compression targets inside the port')
    need(not any(p.suffix.lower() in ('.png','.wav','.bin','.exe','.zip') for p in files),'No new ROM, build, authored asset or raw media allocations')
    storage=[];seen=set();total=0
    for p in sorted(files):
        h=sha(p);stat=p.stat();key=stat.st_dev,stat.st_ino;before=allocated(p)
        need(subprocess.run(['compact.exe','/C','/EXE:LZX','/F','/I','/Q',str(p)],capture_output=True).returncode==0 and sha(p)==h,'Lossless exact-target compression')
        after=allocated(p);unique=key not in seen;seen.add(key)
        if unique:total+=after
        storage.append(dict(path=str(p),sha256=h,logicalBytes=stat.st_size,beforeAllocatedBytes=before,allocatedBytes=after,uniqueSelectedAllocation=unique));pins[str(p)]=h
    builds=[p for p in ROOT.iterdir() if p.is_dir() and (p/'mkport_candidate.exe').is_file()]
    launcher=ROOT/'PLAY_MK2_KANO_SONYA.cmd'
    checked=ROOT/'PLAY_CURRENT_V6508_CHECKED.cmd'
    need(launcher.read_text().count('PLAY_CURRENT_V6508_CHECKED.cmd')==1 and
         'diagnostic_v6508_native_projectile_identifiers' in checked.read_text() and
         'diagnostic_v6640' not in launcher.read_text()+checked.read_text(),'Normal public CMD delegates to its unchanged checked v6508 target')
    pins[str(launcher)]=sha(launcher)
    pins[str(checked)]=sha(checked)
    need(len(builds)==16 and not (ROOT/'mame-mkp/build/mingw-gcc').exists() and not process.census(),'Sixteen retained compiled folders, absent cache and no native jobs')
    need(all(sha(p)==h for p,h in pins.items()),'Every protected source/evidence byte unchanged')
    report=dict(passed=True,goalStatus='active',fullPortAcceptance=False,remaining=parent['remaining'],candidate=current.NAME,
                finiteProofs=[str(p) for p in proof_paths],nativeInputDelivery=delivery,twoNativeBicycleRecoveriesAccepted=True,
                actualCloseRecoveryFaultsRejected=4,actualInputFaultsRejected=4,actualNativeAttempts=attempts,
                genuineNewIncomingHitInterruptions=0,unexercisedAttempts=11,failedObserverBoots=1,publicPlayableChanged=False,
                previousSubstantiveGoalTurnClassification='progress: four real both-slot Square contacts, exact complete audio, recovery and ownership accepted',
                previousAssistantTurnClassification='no progress: acknowledgement only',
                thisGoalTurnClassification='progress: corrected actual input register provenance, complete bit timeline, native close-punch recovery and actual fault rejections; measured counter trajectories change next test route',
                nextAction='Use a source-timed native projectile counter or source-bound attack-box/flight intersection; do not keep calling unlanded grounded/jump counters interruptions.',
                intentionalDocumentationPinMigrations=migrations,inputHashes=pins,exactCompressedTargets=storage,
                selectedFileCount=len(files),uniqueSelectedAllocatedBytes=total,retainedCompiledCandidates=len(builds),compilerCacheAbsent=True,
                newNativeBootsThisGoalTurn=5,newBuilds=0,newROMCopies=0,newZIPs=0,newRawMedia=0,deletedOldArtifacts=0)
    OUT.mkdir();p=OUT/'report.json';p.write_text(json.dumps(report,indent=2)+'\n');h=sha(p)
    need(subprocess.run(['compact.exe','/C','/EXE:LZX','/F','/I','/Q',str(p)],capture_output=True).returncode==0 and sha(p)==h,'Lossless finite journal')
    print(json.dumps({k:report[k] for k in ('passed','unexercisedAttempts','failedObserverBoots','selectedFileCount','uniqueSelectedAllocatedBytes','newBuilds','publicPlayableChanged')}),flush=True)

if __name__=='__main__':main()
