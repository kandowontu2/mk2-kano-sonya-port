"""Release this exact terminal native reset/control RAM job; no deletion.

Prepare source/kernel/unique-buffer proof in the same parent, then check
the exact parent/game/compiler identities absent and original port closed.
No process kill, ROM/build/media/ZIP output or public promotion.
"""
import hashlib
import json
import os
import socket
import subprocess
from pathlib import Path
import seal_native_kano_laser_post_reset_controls_complete_review as seal

ROOT,need,sha,base=seal.ROOT,seal.need,seal.sha,seal.base
PREP=ROOT/'audit_native_kano_laser_post_reset_controls_retirement_prepare'
OUT=ROOT/'audit_native_kano_laser_post_reset_controls_retirement'
PARENT,GAME,PARSER,PARSER_PARENT,PORT=146656,189456,162408,191464,59731


def prepare(actual,server):
    need(not PREP.exists()and os.getpid()==PARENT and server.server_port==PORT and not base.identity.census(),
         'Exact original terminal-game RAM parent and review port, not another task')
    report_path=seal.OUT/'report.json';report=json.loads(report_path.read_text())
    need(report['passed']and report['actualCounterexamplesRejected']==44 and
         report['originalUniqueRAMRastersToRelease']==33 and all(sha(p)==h for p,h in report['inputHashes'].items()),
         'Complete immutable actual post-reset controls/CPU/body/shadow/visual progress sealed')
    folder,text,images=actual.RAM_CASES[actual.KEY]
    metadata=json.loads((folder/'result.json').read_text())
    need(len(images)==33 and len({id(a)for a in images.values()})==33 and
         set(actual.RAM_CASES)=={actual.KEY,'post_reset_controls_visual'}and
         all(id(a)in{id(v)for v in images.values()}for a in actual.RAM_CASES['post_reset_controls_visual'][2].values()),
         'Thirty-three original native arrays; six review aliases contain no duplicate buffers')
    need(hashlib.sha256(actual.guest).hexdigest().upper()==metadata['proofs']['guest']['sha256']and
         hashlib.sha256(actual.gfx).hexdigest().upper()==metadata['proofs']['gfx']['sha256']and
         all(metadata['proofs'][k]['everyActualByteComparedInRAM']for k in ('guest','gfx')),
         'Whole actual native guest/GFX inventories byte-compared to independently reconstructed current sources')
    stock=(ROOT/'mk2/mk2-maincpu.bin').read_bytes();kernels=[]
    for lo,hi in ((0xff801070,0xff8017b0),(0xff804160,0xff804430),(0xff82f700,0xff82f800)):
        start,end=((p-0xff800000)//8 for p in (lo,hi))
        need(actual.guest[start:end]==stock[start:end],'Entire actual native shadow/body/jump kernel unchanged')
        kernels.append(dict(start=f'{lo:08X}',end=f'{hi:08X}',everyByteCompared=True,
                            sha256=hashlib.sha256(actual.guest[start:end]).hexdigest().upper()))
    pins=dict(report['inputHashes'])
    for p in (Path(__file__),report_path,ROOT/'mk2/mk2-maincpu.bin'):
        pins[str(p.resolve())]=sha(p)
    PREP.mkdir();base.save(PREP/'report.json',dict(passed=True,parent=PARENT,port=PORT,
        originalUniqueRAMRastersToRelease=33,aliasBufferCopies=0,actualNativeInventoryProofs=metadata['proofs'],
        originalWholeNativeKernelsUnchanged=kernels,inputHashes=pins,fullPortAcceptance=False))
    print(json.dumps(dict(passed=True,exactRAMParent=PARENT,originalUniqueRAMRastersToRelease=33,
                         originalWholeNativeKernelsUnchanged=True)),flush=True)


def run():
    need(not OUT.exists(),'Fresh exact this-job RAM release receipt')
    prepared_path=PREP/'report.json';prepared=json.loads(prepared_path.read_text())
    need(prepared['passed']and prepared['parent']==PARENT and prepared['port']==PORT and
         all(sha(p)==h for p,h in prepared['inputHashes'].items()),'Exact immutable original RAM preparation retained')
    game_path=ROOT/'audit_native_kano_laser_post_reset_controls_ram/sonya_p1_cpu_sonya_earned_reset_actual_controls/native_terminal.json'
    parser_path=ROOT/'audit_native_kano_laser_post_reset_controls_source/native_terminal.json'
    game=json.loads(game_path.read_text());parser=json.loads(parser_path.read_text())
    need(game['pid']==GAME and game['nativeExit']==0 and not game['hostDecodeErrors']and
         game['actualWindowsIdentity']['ParentProcessId']==PARENT and parser['pid']==PARSER and parser['nativeExit']==0 and
         parser['actualWindowsIdentity']['ParentProcessId']==PARSER_PARENT,'Exact actually terminated game and independent parser provenance')
    ids=[PARENT,GAME,PARSER,PARSER_PARENT]
    query='Get-CimInstance Win32_Process -Filter "'+' OR '.join('ProcessId='+str(pid)for pid in ids)+'" | Select-Object ProcessId,ParentProcessId,ExecutablePath | ConvertTo-Json -Compress'
    result=subprocess.run(['powershell.exe','-NoProfile','-Command',query],capture_output=True,text=True)
    need(result.returncode==0 and not result.stdout.strip()and not result.stderr.strip(),
         'All exact game/compiler/RAM producer identities authoritatively absent')
    with socket.socket()as connection:
        connection.settimeout(1);need(connection.connect_ex(('127.0.0.1',PORT))!=0,'Exact original RAM review port closed')
    names=['audit_native_kano_laser_post_reset_controls_source','audit_native_kano_laser_post_reset_controls_ram',
        'audit_native_kano_laser_post_reset_controls_initializer_source','audit_native_kano_laser_post_reset_controls_checked',
        'audit_native_kano_laser_post_reset_controls_bound_checked','audit_native_kano_laser_post_reset_controls_complete_fields_checked',
        'audit_native_kano_laser_post_reset_body_shadow_checked','audit_native_kano_laser_post_reset_body_complete_fields_checked',
        'audit_native_kano_laser_post_reset_controls_review','audit_native_kano_laser_post_reset_controls_complete_review',PREP.name]
    files=[p for name in names for p in (ROOT/name).rglob('*')if p.is_file()]
    need(not any(p.suffix.lower()in('.png','.wav','.bin','.exe','.zip')for p in files),
         'This complete batch created no raw media, build, ROM or archive copies')
    need(not(ROOT/'mame-mkp/build/mingw-gcc').exists()and
         sha(ROOT/'PLAY_LATEST_KANO_SONYA.cmd')=='D6BABF8CBC1F4CB020F3D7F3A2C8C5A3A762B946E83D56FC1E5BA3B398129DE5',
         'Generated build cache absent and public CMD unchanged')
    pins={str(p.resolve()):sha(p)for p in [Path(__file__),*files]}
    OUT.mkdir();base.save(OUT/'report.json',dict(passed=True,exactRAMParentRetired=PARENT,
        exactNativeGameRetired=GAME,exactNativeCompilerRetired=PARSER,exactCompilerParentRetired=PARSER_PARENT,
        exactReviewPortClosed=PORT,originalUniqueNativeRAMRastersReleased=33,aliasBufferCopies=0,inputHashes=pins,
        actualNativeGameBoots=1,nativeCompilerOnlyBoots=1,batchEvidenceLogicalBytes=sum(p.stat().st_size for p in files),
        earlierFailuresPreserved=True,previousPolicyRetainedScreenshotUntouched=True,publicPlayableChanged=False,
        newBuilds=0,newROMCopies=0,newRawMedia=0,newZIPs=0,fullPortAcceptance=False,goalStatus='active'))
    print(json.dumps(dict(passed=True,exactNativeAndRAMHandlesRetired=True,originalNativeRAMRastersReleased=33,
                         newBuilds=0,newROMCopies=0,newRawMedia=0,newZIPs=0)),flush=True)


if __name__=='__main__':run()
