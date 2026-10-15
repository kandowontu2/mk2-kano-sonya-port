"""Read-only terminal/storage/public-entrypoint audit after RAM host exits."""
import json
import socket
import subprocess
from pathlib import Path
import capture_native_kano_laser_audio as current

ROOT,need,sha=current.ROOT,current.need,current.sha
OUT=ROOT/'audit_native_kano_laser_ground_ram_retirement'

def main():
    need(not OUT.exists(),'Fresh immutable retirement receipt')
    paths=[ROOT/'audit_native_kano_laser_ui_checked/report.json',ROOT/'audit_native_kano_laser_ui_visual_review/report.json',
           ROOT/'audit_native_kano_laser_ground_complete_buffers_checked/report.json',ROOT/'audit_native_kano_laser_ground_visual_review/report.json']
    ui,ui_visual,ground,visual=[json.loads(p.read_text())for p in paths]
    need(all(r['passed'] and not r['fullPortAcceptance'] and not r['publicPlayableChanged']for r in(ui,ui_visual,ground,visual)),
         'All actual finite acceptance scopes retained, no finished release claim')
    need(ground['nativeGroundShadowCopies']==120162 and ground['actualDisplayedNativeRasters']==148 and
         len(ground['faultChecks'])==28 and len(visual['individuallyViewedNativeRasters'])==24 and
         len(ui_visual['sampledNativeRasters'])==12,'Exact accepted native evidence counts')
    for report in(ui,ground):need(all(sha(p)==h for p,h in report['inputHashes'].items()),'Actual executed proof/build inputs conserved')
    need(visual['sourceReportSHA256']==sha(paths[2]) and ui_visual['sourceReportSHA256']==sha(paths[0]) and
         all(sha(p)==h for p,h in visual['inputHashes'].items()),'Same actual reviewed native rasters/source proofs')
    pids=[187540]+[r['nativeTerminal']['pid']for report in(ui,ground)for r in report['cases']]
    command='$ids=@('+','.join(str(p)for p in pids)+'); @(Get-CimInstance Win32_Process | Where-Object { $_.ProcessId -in $ids } | Select-Object ProcessId,ParentProcessId,ExecutablePath) | ConvertTo-Json -Compress'
    result=subprocess.run(['powershell','-NoProfile','-Command',command],capture_output=True,text=True)
    need(result.returncode==0 and not result.stderr and result.stdout.strip()in('', '[]'),'Exact RAM parent and all eight native handles absent')
    for port in(59134,58957):
        sock=socket.socket();sock.settimeout(1)
        try:need(sock.connect_ex(('127.0.0.1',port))!=0,'Retired exact UI/ground RAM server')
        finally:sock.close()
    need(not(ROOT/'mame-mkp/build/mingw-gcc').exists(),'No retained generated compiler cache')
    cmd=ROOT/'PLAY_LATEST_KANO_SONYA.cmd'
    need(sha(cmd)=='D6BABF8CBC1F4CB020F3D7F3A2C8C5A3A762B946E83D56FC1E5BA3B398129DE5','Public playable CMD unchanged')
    folders=[ROOT/'audit_native_kano_laser_ground_ram',ROOT/'audit_native_kano_laser_ground_ram_source',
             ROOT/'audit_native_kano_laser_ground_checked',ROOT/'audit_native_kano_laser_ground_kano_p1_complete_buffers_recheck',
             ROOT/'audit_native_kano_laser_ground_complete_buffers_checked',ROOT/'audit_native_kano_laser_ground_visual_review']
    outputs=[p for folder in folders for p in folder.rglob('*')if p.is_file()]
    need(all(p.suffix.lower()not in('.png','.wav','.bin','.exe','.zip')for p in outputs),'No new raw media/ROM/build/ZIP files')
    OUT.mkdir()
    value=dict(passed=True,actualAbsentPIDs=pids,retiredRAMPorts=[59134,58957],allActualNativeHandlesTerminal=True,
        wholeRastersAndVideoBuffersReleasedFromRAM=True,newGroundEvidenceLogicalBytes=sum(p.stat().st_size for p in outputs),
        inputHashes={str(p.resolve()):sha(p)for p in[Path(__file__),cmd,*paths]},
        oldFailedCountGatePreserved=True,firstKanoHandleRequalifiedWithoutReplay=True,
        boundedBothSlotDeadPoolGroundShadowAcceptance=True,allArenaFloorAcceptance=False,
        fullPortAcceptance=False,publicPlayableChanged=False,newBuilds=0,newROMCopies=0,newRawMedia=0,newZIPs=0,
        generatedCompilerCacheAbsent=True,goalStatus='active')
    (OUT/'report.json').write_text(json.dumps(value,indent=2)+'\n')
    print(json.dumps(dict(passed=True,nativeHandlesAndRAMRetired=True,newGroundEvidenceLogicalBytes=value['newGroundEvidenceLogicalBytes'],publicPlayableChanged=False)),flush=True)

if __name__=='__main__':main()
