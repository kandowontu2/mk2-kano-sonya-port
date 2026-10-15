"""Preserve5586 actual verifier failure; bind shared source reference explicitly.

The generated run and native capture have their own global namespaces. The
independently defined ROM gate must also receive the source bytes. Retain the
entire capture, source decoder, byte faults, all physical/art/audio gates and
real terminal audit. No edits to pinned5586 or its live/retained capture.
"""
import json, subprocess, traceback
from pathlib import Path
from PIL import Image
import current_dcs_rom_source_capture_v5586 as original

ROOT,need,sha=original.ROOT,original.need,original.sha
BASE=ROOT/'audit_v5590_current_dcs_rom_source_bound_ram'
OUT=ROOT/'audit_v5591_current_dcs_rom_source_bound_progress'
FAILURE=original.OUT/'progress.json'
COMPLETED=[]
original.native_capture.__globals__.update(BASE=BASE,COMPLETED=COMPLETED)

source=original.source
before="    EXPECTED,rom_sources=expected_region(pins);native_capture.__globals__['EXPECTED']=EXPECTED"
after=before+"\n    original.EXPECTED=EXPECTED # The complete independent gates share their defining module namespace."
need(source.count(before)==1,'Only omitted independent source-reference binding corrected in whole actual-native run')
source=source.replace(before,after,1)
before='    for p in (PARENT,Path(__file__),LUA,Path(announcer.__file__),Path(announcer.observed.__file__)):'
after='    for p in (PARENT,Path(__file__),Path(original.__file__),FAILURE,LUA,Path(announcer.__file__),Path(announcer.observed.__file__)):'
need(source.count(before)==1,'Preserve executed failure and all original source/native input pins')
source=source.replace(before,after,1)
scope=dict(original.scope,original=original,BASE=BASE,OUT=OUT,COMPLETED=COMPLETED,FAILURE=FAILURE,__file__=__file__)
exec(compile(source,__file__+'.entire5586_native_source_ROM_audit_with_explicit_shared_reference','exec'),scope)
native_run=scope['run']

def run():
    failed=json.loads(FAILURE.read_text())
    need(not failed['passed'] and failed['goalStatus']=='active' and failed['error']==
         "ValueError('Every actual startup sound ROM byte equals independent stock firmware/data/lane/mirror reconstruction')",
         'Retain exact real executed verifier namespace failure, never alter source or claim a game failure')
    folder=original.BASE/'kano_p1_samples'
    terminal=json.loads((folder/'terminal.json').read_text())
    need(terminal['exit_code']==0 and terminal['candidate']==original.capture.original.model.current.NAME
         and terminal['assistance']=='none' and not terminal['cheats_enabled']
         and not (folder/'stderr.log').read_text(), 'Preserved first native capture genuinely terminal0, not restarted for timeout')
    pins={str(FAILURE):sha(FAILURE)}
    expected,sources=original.expected_region(pins)
    rows=[]
    log=(folder/'run.log').read_text()
    for line in log.splitlines():
        if line.startswith('MK2_NATIVE_DCS_ROM_DIGEST '):
            row=dict(original.re.findall(r'(\w+)=([^\s]+)',line));rows.append(row)
    for phase,frame in (('startup','1'),('terminal','5198')):
        actual=[r for r in rows if r['phase']==phase]
        need(len(actual)==192 and [int(r['offset'])for r in actual]==list(range(0,0xc00000,65536))
             and all(r['frame']==frame and r['bytes']=='65536' and r['size']=='12582912'
                     and r['writes']=='0' and r['assistance']=='none'
                     and r['sha256']==original.hashlib.sha256(expected[int(r['offset']):int(r['offset'])+65536]).hexdigest().upper()
                     for r in actual), 'Retained real first-run full sound-region chunk digests source-exact, no regenerated observations')
    need('MK2_NATIVE_DCS_ROM_RESULT frame=5198 checks=2 writes=0 assistance=none' in log
         and 'MK2_PORIGIN_RESULT frame=5198 calls=26 pending=0' in log and 'Average speed:' in log,
         'Preserved native first run and every passive audio packet really completed')
    pngs=[];compacted=[]
    for p in folder.rglob('*'):
        if not p.is_file():continue
        need(p.suffix.lower()not in('.bin','.wav','.rgb','.pcm'),'First verifier failure preserved no requested raw buffers')
        if p.suffix.lower()=='.png':
            with Image.open(p) as im:need(p==folder/'snap/mk2ks/0000.png' and im.size==(400,254),'First real timed automatic PNG accounted')
            pngs.append(dict(path=str(p),bytes=p.stat().st_size,sha256=sha(p)))
        if p.suffix.lower()in('.log','.json','.cfg','.txt'):
            before=sha(p);cp=subprocess.run(['compact.exe','/C','/F','/EXE:LZX','/Q',str(p)],capture_output=True)
            need(cp.returncode==0 and sha(p)==before,'Preserved failed verifier evidence force-LZX without byte changes')
            compacted.append(str(p))
        pins[str(p.resolve())]=sha(p)
    need(len(pngs)==1,'One actual automatic PNG from first verifier-failed native run')
    report=native_run()
    need(report['passed'] and all(sha(p)==h for p,h in pins.items()),'Entire qualified native run and preserved failure/source bytes unchanged')
    report['newInputHashes'].update(pins)
    report.update(preservedExecutedVerifierFailure=str(FAILURE),preservedFirstNativeTerminal=terminal,
                  preservedFirstActualSourceExactROMChunkDigests=384,preservedFirstNativeAutomaticPNGs=pngs,
                  preservedFirstAutomaticPNGBytes=sum(p['bytes']for p in pngs),
                  preservedFailureTextFilesForceLZXCompacted=len(compacted),newNativeBoots=2,
                  newNativeBootsForQualifiedRun=1,sourceQualifiedNativeDCSWaveformAccepted=False,
                  fullPortAcceptance=False)
    return report

if __name__=='__main__':
    need(not BASE.exists() and not OUT.exists(),'Fresh guarded source-bound whole native ROM capture')
    try:report=run()
    except Exception as error:
        report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),completedNativeCaptures=COMPLETED,
                    goalStatus='active',fullPortAcceptance=False)
    OUT.mkdir();original.capture.save(OUT/'progress.json',report)
    print(json.dumps({k:v for k,v in report.items()if k not in ('remaining','newInputHashes','actualPacketOrigins',
        'effectiveActualPacketOriginFaults','retainedActualAnnouncerFaults','retainedActualPriorityFaults',
        'actualTimerCoverage','actualSourceVoiceEffectRoutes','completedNativeCaptures','qualifiedDirectSourceAndFullWordDelivery',
        'effectiveDirectSourceBranchAndPortFaults','preservedFirstNativeTerminal')},indent=2),flush=True)
    raise SystemExit(0 if report['passed']else 1)
