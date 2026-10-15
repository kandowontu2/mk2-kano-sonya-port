"""Retain actual announcer source failure; qualify complete name trampoline.

Only the incorrect stock-ROM assumption at the existing name trampoline is
replaced by its complete independently encoded program and actual fallback
branch. Whole native source/priority/queue/packet/port/ADSP gate remains.
No replay, raw buffer files, guest writes, builds or public release changes.
"""
import datetime, inspect, json, re, struct, subprocess, traceback
from pathlib import Path
from PIL import Image
import current_baraka_announcer_capture_v5566 as observed

prior, capture = observed.prior, observed.capture
ROOT, need, sha = observed.ROOT, observed.need, observed.sha
PARENT = observed.PARENT
FAILURE = observed.OUT / 'progress.json'
FOLDER = observed.BASE / 'kano_p1_samples'
OUT = ROOT / 'audit_v5572_current_baraka_announcer_qualified'


def reference(guest, stock, name, address, call):
    need(0xff800000 <= address <= 0xfffffe00, 'Actual native announcer reference in guest ROM')
    if name == 'caller' and address == 0xfffb70d0:
        words = (0x0b40,0xff01,0xca80,0x70e0,0xfffb,0x0b40,0xff02,0xca80,0x70e0,0xfffb,
                 0x0d5f,0x2430,0xffa1,0x0960,0x0b20,0xff00,0,0x0580,0x1030,0x01d0,
                 0x0b20,0x0100,0xffff,0x0960)
        need(struct.unpack_from('<24H', guest, prior.off(0xfffb7000)) == words,
             'Entire existing own-name trampoline compares254/253, preserves actual native CALLA and full import branch')
        need(call['command'] == call['a0'] == '00000009',
             'Actual original Baraka name selector9 takes native fallback, never synthetic254/253 import branch')
        need(struct.unpack_from('<3H', guest, prior.off(address-48)) == (0x0d5f,0x2430,0xffa1),
             'Actual fallback CALLA targets original announcer dispatcher and returns to observed address')
    else:
        at = prior.off(address)
        need(guest[at:at+16] == stock[at:at+16], 'Actual native announcer script/stock caller remains original source bytes')
        if name == 'caller':
            wanted = struct.pack('<5H',0x09c0,int(call['command'],16),0x0d5f,0x2430,0xffa1)
            at = prior.off(address-80)
            need(guest[at:at+10] == stock[at:at+10] == wanted,
                 'Entire original literal announcer command plus native CALLA bound to real return address')


source = inspect.getsource(observed.gate)
before = """                need(0xff800000 <= address <= 0xfffffe00
                     and guest[prior.off(address):prior.off(address)+16] == stock[prior.off(address):prior.off(address)+16],
                     'Actual native announcer script/caller remains original source bytes')"""
need(source.count(before) == 1, 'Only incorrect source-origin assumption replaced; complete actual announcer algorithm retained')
source = source.replace(before, '                reference(guest, stock, name, address, call)', 1)
scope = dict(observed.__dict__, reference=reference)
exec(compile(source, __file__ + '.entire5566_native_announcer_with_complete_existing_name_trampoline', 'exec'), scope)
gate = scope['gate']
source = inspect.getsource(observed.faults)
scope = dict(observed.__dict__, gate=gate)
exec(compile(source, __file__ + '.entire5566_actual_announcer_fault_suite_complete_source_binding', 'exec'), scope)
faults = scope['faults']


def run():
    guest = capture.original.model.current.expected()
    parent, failed = (json.loads(p.read_text()) for p in (PARENT, FAILURE))
    need(parent['passed'] and parent['goalStatus'] == 'active' and not failed['passed']
         and failed['error'] == "ValueError('Actual native announcer script/caller remains original source bytes')",
         'Preserve actual completed capture and exact executed stock-source-origin failure')
    pins = dict(parent['newInputHashes'])
    for p in (PARENT, FAILURE, Path(__file__), Path(observed.__file__), observed.LUA,
              ROOT / 'tools/verify_jax_clap_native_audio_routes_v4066.py'):
        pins[str(p.resolve())] = sha(p)
    meta = json.loads((FOLDER / 'result.json').read_text())
    terminal = json.loads((FOLDER / 'terminal.json').read_text())
    process = json.loads((FOLDER / 'process.json').read_text())
    log = (FOLDER / 'run.log').read_text()
    need(meta['passed'] and terminal == meta['process'] and terminal['exit_code'] == 0
         and terminal['nativePID'] == process['pid'] and terminal['player'] == 'kano' and terminal['victim_slot'] == 1
         and terminal['killer'] == 'baraka' and terminal['command'] == 'bbbb_hp'
         and terminal['entireOriginal921PhysicalControllerRetained'] and terminal['assistance'] == 'none'
         and not terminal['cheats_enabled'] and not (FOLDER / 'stderr.log').read_text()
         and 'MK2_STOCK_HEAD_V921_RESULT frame=5198' in log and 'Average speed:' in log,
         'Actual unassisted physical native capture genuinely terminal0/5198, never an observation timeout')
    need(terminal['candidate'] == capture.original.model.current.NAME
         and terminal['executable_sha256'] == capture.original.model.current.EXE_SHA
         and terminal['payload_sha256'] == capture.original.model.current.PAYLOAD_SHA,
         'Exact current executable, guest/payload and native context')
    pins.update(terminal['input_hashes'])
    need(all(sha(p) == h for p,h in pins.items()), 'Every executed immutable input/evidence/current/public hash stable')
    visual, state = meta['actualNativeHeadBodyPixelsAndScanout'], meta['actualNativeContract']
    need(state['damage'] == 322 and state['nativeWrapAge'] == 174
         and state['headPoses'] == state['bodyPoses'] == list(range(7))
         and state['groundedBodyDMAs'] > 100 and state['hardwarePaletteDumps'] == 14
         and len(meta['effectiveActualNativeRecordFaults']) == 15 and visual['passed']
         and visual['everyEmittedOwnedHeadBodyAndLegitimateForegroundPixelExact']
         and len(visual['parts']) == 14 and visual['wholeNativeScanoutPixels'] == 1422400
         and len(meta['actualDisplayHeaders']) == 125,
         'Entire native physical/true-owner/floor/cleanup and actually executed exact14-part RAM pixel gate retained')
    positive = gate(log, guest)
    rejected = faults(log, guest)
    old_faults = observed.qualified.faults(log, guest)
    need(len(rejected) == 12 and len(old_faults) == 22, 'Entire actual new announcer and original fighter priority fault suites')
    c = next(r['call'] for r in positive['delivered'] if r['call']['caller'] == 'FFFB70D0')
    source_faults = []
    for offset, label in ((prior.off(0xfffb7000), 'first own-name branch comparator corrupted'),
                          (prior.off(0xfffb70a0), 'native fallback CALLA target corrupted'),
                          (prior.off(0xfffb70e0), 'complete own-name import branch corrupted')):
        bad = bytearray(guest); bad[offset] ^= 1
        need(bytes(bad) != guest, 'Effective independent source-program fault in verifier RAM only')
        try: gate(log, bytes(bad))
        except ValueError as error: source_faults.append(dict(label=label, rejectedBy=str(error)))
        else: raise ValueError('Accepted corrupted complete name trampoline')
    need(gate(log, guest) == positive, 'Complete source and actual native positive restored after every source fault')
    coverage = prior.phase.coverage(log, meta)
    voice = prior.routes.gate(log, guest, 'kano', 1)
    old = json.loads((ROOT / 'audit_v5556_current_baraka_priority_ram/kano_p1_samples/result.json').read_text())
    need(meta['actualDisplayHeaders'] == old['actualDisplayHeaders']
         and meta['actualMixedPCMSHA256'] == old['actualMixedPCMSHA256']
         and meta['actualPCMUpdates'] == old['actualPCMUpdates'] and meta['actualPCMBytes'] == old['actualPCMBytes'],
         'All125 actual whole raster buffers and full native joined PCM hash/bytes/counts unchanged by additional passive taps')
    pngs, compacted = [], []
    for p in sorted(FOLDER.rglob('*')):
        if not p.is_file(): continue
        need(p.suffix.lower() not in ('.bin','.wav','.rgb','.pcm'), 'No requested raw game/raster/audio buffers persisted')
        if p.suffix.lower() == '.png':
            with Image.open(p) as im:
                need(p == FOLDER/'snap/mk2ks/0000.png' and im.size == (400,254), 'Only accounted actual native timed-exit PNG')
            pngs.append(dict(path=str(p),bytes=p.stat().st_size,sha256=sha(p)))
        if p.suffix.lower() in ('.log','.json','.cfg','.txt'):
            before = sha(p)
            cp = subprocess.run(['compact.exe','/C','/F','/EXE:LZX','/Q',str(p)],capture_output=True)
            need(cp.returncode == 0 and sha(p) == before, 'Actual retained terminal text force-LZX compressed, no byte changes')
            compacted.append(str(p))
        pins[str(p.resolve())] = sha(p)
    need(len(pngs) == 1 and pngs == meta['nativeAutomaticTerminalPNGs']
         and all(sha(p) == h for p,h in pins.items()), 'Actual one timed PNG and unchanged source/public/evidence hashes')
    return dict(passed=True,observedUTC=datetime.datetime.now(datetime.timezone.utc).isoformat(),goalStatus='active',
        remaining=parent['remaining'],parentAdditiveJournal=str(PARENT),preservedExecutedSourceFailure=str(FAILURE),
        previousGoalTurnClassification=parent['thisGoalTurnClassification'],
        thisGoalTurnClassification='progress: actual original dual-dispatcher announcer/priority/packet/port/ADSP evidence qualified without replay; existing complete24-word name trampoline and true native Baraka9 fallback source bound instead of false stock-source assumption;12actual announcer,22original priority and3independent source-program faults rejected, whole physical/raster/timer/source voice and RGB/PCM nonperturbance retained',
        actualDualDispatcher=positive,effectiveActualAnnouncerFaults=rejected,retainedOriginalPriorityFaults=old_faults,
        effectiveIndependentTrampolineSourceFaults=source_faults,actualNameTrampolineFallback=c,
        actualTimerCoverage=coverage,actualSourceVoiceEffectRoutes=voice,nativeCaptureResult=str(FOLDER/'result.json'),
        persistentNativeAutomaticExitPNGs=pngs,persistentNativeAutomaticPNGBytes=sum(p['bytes'] for p in pngs),
        terminalTextFilesForceLZXCompacted=len(compacted),newNativeBootsSinceParent=1,newNativeBootsForQualifier=0,
        newBuilds=0,newDeletedFiles=0,requestedRawGuestGFXVRAMRGBPCMFilesWritten=0,
        publicPlayableChanged=False,refreshedReleaseZIP=False,allNativeQueueSuppressionCausesAccepted=False,
        sourceQualifiedNativeDCSWaveformAccepted=False,completeBarakaFinisherAudioAccepted=False,fullPortAcceptance=False,
        newInputHashes=pins,
        nextAction='Extend qualified actual announcer source/priority delivery to both victims/slots; independently bind direct packet programs outside priority path and original full DCS waveform; continue every remaining original requirement group.')


if __name__ == '__main__':
    need(not OUT.exists(), 'Fresh immutable actual announcer source qualification')
    try: report = run()
    except Exception as error:
        report = dict(passed=False,error=repr(error),traceback=traceback.format_exc(),goalStatus='active',fullPortAcceptance=False)
    OUT.mkdir();capture.save(OUT/'progress.json',report)
    print(json.dumps({k:v for k,v in report.items() if k not in ('remaining','newInputHashes','actualDualDispatcher',
        'effectiveActualAnnouncerFaults','retainedOriginalPriorityFaults','effectiveIndependentTrampolineSourceFaults',
        'actualNameTrampolineFallback','actualTimerCoverage','actualSourceVoiceEffectRoutes')},indent=2),flush=True)
    raise SystemExit(0 if report['passed'] else 1)
