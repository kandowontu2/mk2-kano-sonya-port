"""Record original CPU rasters with accepted mirror/rejected cross scopes distinct."""
import hashlib
import json
import socket
import subprocess
from pathlib import Path
import capture_native_kano_laser_cpu_choke_approach as actual

ROOT,need,sha=actual.ROOT,actual.need,actual.sha
OUT=ROOT/'audit_native_kano_laser_cpu_choke_visual_review'
RETIRE=ROOT/'audit_native_kano_laser_cpu_choke_ram_retirement'
FAULT=ROOT/'audit_native_kano_laser_cpu_choke_canonical_fault_checked/report.json'


def seal(cases):
    need(not OUT.exists(),'Fresh original native CPU visual receipt')
    fault=json.loads(FAULT.read_text())
    need(fault['passed'] and fault['actualFaultsRejected']==15 and fault['actualCPUKanoMirrorOnly'] and
         fault['crossCPUSonyaTrialStillRejected'], 'Accepted Kano mirror is not cross/Sonya acceptance')
    need(all(sha(p)==h for p,h in fault['inputHashes'].items()), 'Every actual checker and candidate input conserved')
    need(set(cases)=={'choke_cpu_kano_human_kano','choke_cpu_kano_human_sonya'}, 'Both original actual terminal captures')
    records=[];paths=[]
    for human in('kano','sonya'):
        key=f'choke_cpu_kano_human_{human}'
        folder,text,images=cases[key]
        path=folder/'result.json';paths.append(path);report=json.loads(path.read_text())
        need(report['nativeExit']==0 and report['passed']==(human=='kano'), 'Exact original terminal acceptance/rejection retained')
        need(len(report['actualScenes'])==(28 if human=='kano'else 16) and
             set(images)=={f"ui_{s['frame']:04d}.png"for s in report['actualScenes']}, 'All actual captured native rasters reviewed')
        for scene in report['actualScenes']:
            rgb=images[f"ui_{scene['frame']:04d}.png"]
            need(rgb.shape==(254,400,3), 'Entire original 400x254 native field')
            records.append(dict(physicalHuman=human,actualCPU=17 if human=='kano'else 18,
                frame=scene['frame'],stage=scene['stage'],sourceRawBGRXSHA256=scene['sha256'],
                nativeRGBSHA256=hashlib.sha256(rgb.tobytes()).hexdigest().upper(),individuallyViewed=True,
                finiteGameplayAccepted=human=='kano',diagnosticOnly=human=='sonya'))
    value=dict(passed=True,acceptedKanoMirrorRasters=28,rejectedSonyaDiagnosticRasters=16,
        individuallyViewedNativeRasters=records,sourceFaultReportSHA256=sha(FAULT),
        inputHashes={str(p.resolve()):sha(p)for p in(Path(__file__),FAULT,*paths)},
        observations=['Kano mirror has native selection, teardown, own lifebar identities, complete held choke poses and later ordinary recovery',
                      'Actors naturally cross screen sides; CPU ownership follows native actor/Main/state, not color or screen-left',
                      'Kano mirror black floor shadows remain present throughout sampled choke poses',
                      'The rejected cross trial actually has CPU Sonya18/human Sonya18 and repeated leg grabs; diagnostic visuals are not full physical/body/shadow acceptance'],
        requirements=['selection','transition','identity','names','human_moves','cpu_moves','ordinary_combat',
                      'ground_shadows','audio','finishers_victims','stage_finishers','campaign_cinematics','cmd_release','storage'],
        remainingGroups=['startup_audio_full_UI_ground','broader_CPU_projectile_arena_shadow_audio',
                         'stage_reselect_rejoin_postending','Pit_Tomb_stock_victims_sound_priority',
                         'secret_morph_cinematic','combined_acceptance_CMD_finished_ZIP'],
        currentFiniteCPUKanoMirrorAccepted=True,crossCPUSonyaTrialStillRejected=True,
        allCPUContextsAccepted=False,allArenasAccepted=False,fullVisualTimelineAccepted=False,fullAudioAcceptance=False,
        fullPortAcceptance=False,publicPlayableChanged=False,newBuilds=0,newNativeBoots=0,
        newROMCopies=0,newRawMedia=0,newZIPs=0,goalStatus='active')
    OUT.mkdir();actual.prior.base.save(OUT/'report.json',value)
    print(json.dumps(dict(passed=True,acceptedMirrorRasters=28,rejectedDiagnosticRasters=16,fullPortAcceptance=False)),flush=True)


def retire():
    need(not RETIRE.exists(),'Fresh immutable exact-handle retirement')
    visual_path=OUT/'report.json';visual=json.loads(visual_path.read_text())
    fault=json.loads(FAULT.read_text())
    need(visual['passed'] and fault['passed'] and visual['sourceFaultReportSHA256']==sha(FAULT) and
         all(sha(p)==h for p,h in visual['inputHashes'].items()) and
         all(sha(p)==h for p,h in fault['inputHashes'].items()), 'All actual terminal and reviewed evidence conserved')
    guard_path=actual.prior.GUARD/'native_terminal.json';guard=json.loads(guard_path.read_text())
    pids=[183860,190244,184692,187636,131196,152904,guard['pid']]
    command='$ids=@('+','.join(str(p)for p in pids)+'); @(Get-CimInstance Win32_Process | Where-Object { $_.ProcessId -in $ids } | Select-Object ProcessId,ParentProcessId,ExecutablePath) | ConvertTo-Json -Compress'
    result=subprocess.run(['powershell','-NoProfile','-Command',command],capture_output=True,text=True)
    need(result.returncode==0 and not result.stderr and result.stdout.strip()in('', '[]'),'All exact native/Python handles absent')
    for port in(53215,60128,64148):
        sock=socket.socket();sock.settimeout(1)
        try:need(sock.connect_ex(('127.0.0.1',port))!=0,'All exact prior and current RAM ports retired')
        finally:sock.close()
    cmd=ROOT/'PLAY_LATEST_KANO_SONYA.cmd'
    need(sha(cmd)=='D6BABF8CBC1F4CB020F3D7F3A2C8C5A3A762B946E83D56FC1E5BA3B398129DE5', 'Public playable remains unchanged')
    need(not(ROOT/'mame-mkp/build/mingw-gcc').exists(),'No generated compiler cache')
    folders=[actual.BASE,actual.prior.BASE,actual.OUT,actual.prior.OUT,OUT,actual.prior.GUARD,
             ROOT/'audit_native_kano_laser_cpu_choke_shadow_terminal_checked',
             ROOT/'audit_native_kano_laser_cpu_choke_approach_fault_checked',FAULT.parent]
    files=[p for folder in folders for p in folder.rglob('*')if p.is_file()]
    need(all(p.suffix.lower()not in('.png','.wav','.bin','.exe','.zip')for p in files),'No raw media or duplicate ROM/build/release files')
    RETIRE.mkdir();actual.prior.base.save(RETIRE/'report.json',dict(passed=True,actualAbsentPIDs=pids,
        retiredRAMPorts=[53215,60128,64148],allOriginalCPURastersAndInitializerBuffersReleasedFromRAM=True,
        inputHashes={str(p.resolve()):sha(p)for p in(Path(__file__),visual_path,FAULT,guard_path,cmd)},
        evidenceLogicalBytes=sum(p.stat().st_size for p in files),preservedGuardedKOAndCrossAndHostCheckerFailures=True,
        acceptedKanoMirrorOnly=True,allCPUContextsAccepted=False,fullPortAcceptance=False,publicPlayableChanged=False,
        newBuilds=0,newROMCopies=0,newRawMedia=0,newZIPs=0,generatedCompilerCacheAbsent=True,goalStatus='active'))
    print(json.dumps(dict(passed=True,allExactNativeHandlesAndRAMRetired=True)),flush=True)


if __name__=='__main__':retire()
