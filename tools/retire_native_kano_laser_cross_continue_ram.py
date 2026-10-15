"""Retire the exact four terminal continue captures, without deleting files."""
import hashlib
import json
import os
import socket
import subprocess
from pathlib import Path
import review_native_kano_laser_cross_continue_matrix as matrix

ROOT, need, sha = matrix.ROOT, matrix.need, matrix.sha
PREP = ROOT/'audit_native_kano_laser_cross_continue_retirement_prepare'
OUT = ROOT/'audit_native_kano_laser_cross_continue_retirement'
PARENT, PORT = 94140, 63011
GAMES = {'kano_p1_to_sonya':86804, 'kano_p2_to_sonya':132800,
         'sonya_p1_to_kano':157592, 'sonya_p2_to_kano':157740}


def absent_games(ids):
    query = 'Get-CimInstance Win32_Process -Filter "'+' OR '.join('ProcessId='+str(pid) for pid in ids)+'" | Select-Object ProcessId,ParentProcessId,ExecutablePath | ConvertTo-Json -Compress'
    result = subprocess.run(['powershell.exe','-NoProfile','-Command',query],capture_output=True,text=True)
    need(result.returncode == 0 and not result.stdout.strip() and not result.stderr.strip(),
         'Exact original native/RAM process identities absent')


def prepare(scope, carrier, server):
    need(not PREP.exists() and os.getpid()==PARENT and server.server_port==PORT,
         'Exact retained original RAM parent and review server')
    absent_games(GAMES.values())
    report_path = matrix.OUT/'report.json'
    report = json.loads(report_path.read_text())
    need(report['passed'] and report['actualContinueRoutes']==4 and
         report['totalActualSemanticFaultsRejected']==143 and
         report['originalUniqueNativeRAMRastersToRelease']==689 and
         all(sha(p)==h for p,h in report['inputHashes'].items()),
         'Complete immutable four-route current-source acceptance sealed')
    need(set(scope['RAM_CASES'])==set(GAMES) and len(carrier['rgbFrames'])==12,
         'Exactly original four games and twelve inspected aliases')
    raw_ids=set(); inventories=[]
    for key, (folder, text, images, metadata) in scope['RAM_CASES'].items():
        terminal=json.loads((folder/'native_terminal.json').read_text())
        need(terminal['nativePID']==GAMES[key] and terminal['exitCode']==0 and
             not terminal['observationErrors'] and not (folder/'stderr.log').read_text().strip() and
             metadata['nativeIdentity']['ParentProcessId']==PARENT,
             'Every actual producer naturally terminated zero without warning')
        need(all(q['everyActualByteComparedInRAM'] for q in metadata['actualGuestGFXProofs'].values()) and
             all(hashlib.sha256(scope[k]).hexdigest().upper()==metadata['actualGuestGFXProofs'][k]['sha256']
                 for k in ('guest','gfx')), 'Whole current guest and art still source-bound in RAM')
        for q in metadata['actualFullRGBDigests']:
            raw=images[q['frame'],q['label']]
            need(len(raw)==406400 and hashlib.sha256(raw).hexdigest().upper()==q['sha256'],
                 'Every original raw native raster still matches its actual callback digest')
        raw_ids.update(id(raw) for raw in images.values())
        inventories.append(dict(case=key, nativePID=GAMES[key], sourceProofs=metadata['actualGuestGFXProofs'],
                                uniqueOriginalRasters=len(images)))
    need(len(raw_ids)==689 and all(id(q['pixels']) in raw_ids for q in carrier['rgbFrames']),
         '689 original raster buffers; twelve review aliases allocate no extra raw buffers')
    pins=dict(report['inputHashes'])
    for p in (Path(__file__),report_path): pins[str(p.resolve())]=sha(p)
    PREP.mkdir()
    matrix.capture.native_base.save(PREP/'report.json',dict(passed=True,parent=PARENT,port=PORT,
        actualRoutes=4,actualSemanticFaultsRejected=143,originalUniqueNativeRAMRastersToRelease=689,
        aliasBufferCopies=0,inventories=inventories,inputHashes=pins,fullPortAcceptance=False))
    print(json.dumps(dict(passed=True,parent=PARENT,originalUniqueNativeRAMRastersToRelease=689)),flush=True)


def run():
    need(not OUT.exists(),'Fresh exact RAM retirement receipt')
    prepared_path=PREP/'report.json'; prepared=json.loads(prepared_path.read_text())
    need(prepared['passed'] and prepared['parent']==PARENT and prepared['port']==PORT and
         all(sha(p)==h for p,h in prepared['inputHashes'].items()),'Immutable original preparation retained')
    absent_games([PARENT,*GAMES.values()])
    with socket.socket() as connection:
        connection.settimeout(1)
        need(connection.connect_ex(('127.0.0.1',PORT))!=0,'Exact original RAM preview port closed')
    dirs=[p for p in ROOT.iterdir() if p.is_dir() and p.name.startswith('audit_native_kano_laser_cross_continue')]
    need(all(p.resolve().parent==ROOT.resolve() for p in dirs),'Exact this-batch evidence directories')
    files=[p for d in dirs for p in d.rglob('*') if p.is_file()]
    need(not any(p.suffix.lower() in ('.png','.wav','.bin','.exe','.zip') for p in files),
         'This batch created no raw media, ROM, build or archive')
    need(not (ROOT/'mame-mkp/build/mingw-gcc').exists() and
         sha(ROOT/'PLAY_LATEST_KANO_SONYA.cmd')=='D6BABF8CBC1F4CB020F3D7F3A2C8C5A3A762B946E83D56FC1E5BA3B398129DE5',
         'Build cache remains absent and public launcher unchanged')
    pins={str(p.resolve()):sha(p) for p in [Path(__file__),*files]}
    OUT.mkdir()
    matrix.capture.native_base.save(OUT/'report.json',dict(passed=True,exactRAMParentRetired=PARENT,
        exactNativeGamesRetired=GAMES,exactReviewPortClosed=PORT,originalUniqueNativeRAMRastersReleased=689,
        aliasBufferCopies=0,actualNativeGameBoots=4,batchEvidenceLogicalBytes=sum(p.stat().st_size for p in files),
        inputHashes=pins,earlierFailuresPreserved=True,previousPolicyRetainedScreenshotUntouched=True,
        publicPlayableChanged=False,newBuilds=0,newROMCopies=0,newRawMedia=0,newZIPs=0,
        fullPortAcceptance=False,goalStatus='active'))
    print(json.dumps(dict(passed=True,exactNativeAndRAMHandlesRetired=True,originalNativeRAMRastersReleased=689)),flush=True)


if __name__=='__main__': run()
