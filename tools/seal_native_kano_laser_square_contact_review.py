"""Record individual review of all captured airborne-contact frames; retire RAM."""
import hashlib
import json
import socket
import subprocess
from pathlib import Path
import capture_native_kano_laser_audio as current

ROOT, need, sha = current.ROOT, current.need, current.sha
SOURCE = ROOT / 'audit_native_kano_laser_square_contact_checked/report.json'
VISUAL = ROOT / 'audit_native_kano_laser_square_contact_visual_review'
RETIRE = ROOT / 'audit_native_kano_laser_square_contact_ram_retirement'


def seal(cases):
    need(not VISUAL.exists(), 'Fresh immutable original visual receipt')
    report = json.loads(SOURCE.read_text())
    need(report['passed'] and report['actualAirborneContactCycles'] == 4 and
         report['actualSquareContactVerified'] and report['everyReadyOwnedBodyShadowFieldSourceBound'],
         'Both actual player-slot physical airborne contact gates')
    for group in ('inputHashes', 'outputHashes'):
        need(all(sha(p) == h for p,h in report[group].items()), 'Actual immutable sources and terminal records')
    need(set(cases) == {'square_p1', 'square_p2'}, 'Exactly both original live-host captures')
    records = []
    for case in report['cases']:
        key = f"square_p{case['side']}"
        folder, text, images = cases[key]
        need(set(images) == {f"ui_{s['frame']:04d}.png" for s in case['actualScenes']}, 'Every captured raster accounted')
        for scene in case['actualScenes']:
            pixels = images[f"ui_{scene['frame']:04d}.png"]
            need(pixels.shape == (254,400,3), 'Entire original native 400x254 field')
            records.append(dict(case=key, frame=scene['frame'], attempt=scene['attempt'], stage=scene['stage'],
                                sourceRawBGRXSHA256=scene['sha256'],
                                nativeRGBSHA256=hashlib.sha256(pixels.tobytes()).hexdigest().upper(),
                                individuallyViewed=True))
    value = dict(passed=True, candidate=current.NAME, sourceReportSHA256=sha(SOURCE),
                 reviewSourceSHA256=sha(Path(__file__)), individuallyViewedNativeRasters=records,
                 observations=['Original Square Wave approach, airborne opponent reaction, landing and recovery in both player slots',
                               'Own Sonya body, native black ground shadow, and MK2-style lifebar identity remain consistent',
                               'Both recovered actors respond to the subsequent physical movement/jump/punch sequence'],
                 actualSquareContactVerified=True, allCapturedContactRastersIndividuallyViewed=True,
                 fullVisualTimelineAccepted=False, allArenasAccepted=False, fullAudioAcceptance=False,
                 fullPortAcceptance=False, publicPlayableChanged=False,
                 requirements=['selection','transition','identity','names','human_moves','cpu_moves','ordinary_combat',
                               'ground_shadows','audio','finishers_victims','stage_finishers','campaign_cinematics','cmd_release','storage'],
                 remainingGroups=['startup_audio_full_UI_ground','broader_CPU_projectile_arena_shadow_audio',
                                  'stage_reselect_rejoin_postending','Pit_Tomb_stock_victims_sound_priority',
                                  'secret_morph_cinematic','combined_acceptance_CMD_finished_ZIP'],
                 newBuilds=0,newNativeBoots=0,newROMCopies=0,newRawMedia=0,newZIPs=0,goalStatus='active')
    VISUAL.mkdir()
    (VISUAL/'report.json').write_text(json.dumps(value,indent=2)+'\n')
    print(json.dumps(dict(passed=True,individuallyViewedNativeRasters=len(records),fullPortAcceptance=False)),flush=True)


def retire():
    need(not RETIRE.exists(), 'Fresh immutable exact-handle retirement')
    report = json.loads(SOURCE.read_text())
    visual_path = VISUAL/'report.json'
    visual = json.loads(visual_path.read_text())
    need(report['passed'] and visual['passed'] and visual['sourceReportSHA256']==sha(SOURCE), 'Same reviewed actual terminals')
    for group in ('inputHashes','outputHashes'):
        need(all(sha(p)==h for p,h in report[group].items()), 'All executed evidence retained')
    parents={r['nativeTerminal']['actualWindowsIdentity']['ParentProcessId'] for r in report['cases']}
    need(parents=={187720}, 'Exact original airborne-contact RAM host')
    pids=[187720]+[r['nativeTerminal']['pid'] for r in report['cases']]
    command='$ids=@('+','.join(str(p) for p in pids)+'); @(Get-CimInstance Win32_Process | Where-Object { $_.ProcessId -in $ids } | Select-Object ProcessId,ParentProcessId,ExecutablePath) | ConvertTo-Json -Compress'
    result=subprocess.run(['powershell','-NoProfile','-Command',command],capture_output=True,text=True)
    need(result.returncode==0 and not result.stderr and result.stdout.strip()in('', '[]'), 'Exact parent and both native handles absent')
    sock=socket.socket()
    sock.settimeout(1)
    try:
        need(sock.connect_ex(('127.0.0.1',55498))!=0, 'Exact airborne-contact RAM server retired')
    finally:
        sock.close()
    need(not(ROOT/'mame-mkp/build/mingw-gcc').exists(), 'No generated compiler cache')
    cmd=ROOT/'PLAY_LATEST_KANO_SONYA.cmd'
    need(sha(cmd)=='D6BABF8CBC1F4CB020F3D7F3A2C8C5A3A762B946E83D56FC1E5BA3B398129DE5', 'Public CMD unchanged')
    files=[p for name in ('audit_native_kano_laser_square_contact_ram','audit_native_kano_laser_square_contact_checked',
                         'audit_native_kano_laser_square_contact_visual_review') for p in(ROOT/name).rglob('*')if p.is_file()]
    need(all(p.suffix.lower()not in('.png','.wav','.bin','.exe','.zip')for p in files), 'No new raw media or duplicate build')
    value=dict(passed=True,actualAbsentPIDs=pids,retiredRAMPorts=[55498],allOriginalContactRastersReleasedFromRAM=True,
               individuallyViewedNativeRasters=len(visual['individuallyViewedNativeRasters']),
               inputHashes={str(p.resolve()):sha(p)for p in(Path(__file__),SOURCE,visual_path,cmd)},
               evidenceLogicalBytes=sum(p.stat().st_size for p in files), actualSquareContactVerified=True,
               fullPortAcceptance=False,publicPlayableChanged=False,newBuilds=0,newROMCopies=0,newRawMedia=0,newZIPs=0,
               generatedCompilerCacheAbsent=True,goalStatus='active')
    RETIRE.mkdir()
    (RETIRE/'report.json').write_text(json.dumps(value,indent=2)+'\n')
    print(json.dumps(dict(passed=True,exactProcessesAndRAMRetired=True)),flush=True)


if __name__=='__main__':
    retire()
