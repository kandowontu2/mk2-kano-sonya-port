"""Current announcer/table/priority/DCS delivery, both victims and slots.

Reuse qualified Kano-P1; three new physical cold boots only. Preserve entire
5560 physical/pixel/source-voice/priority fault case; add qualified announcer
source and twelve actual faults. Native direct packet programs and full DCS
waveform fidelity stay pending. No game edits, raw media files or builds.
"""
import concurrent.futures, datetime, inspect, json, subprocess, traceback
from pathlib import Path
from PIL import Image
import qualify_current_baraka_announcer_v5571 as announcer
import current_baraka_priority_matrix_v5560 as original

capture = announcer.capture
ROOT, need, sha = announcer.ROOT, announcer.need, announcer.sha
PARENT = announcer.OUT / 'progress.json'
BASE = ROOT / 'audit_v5574_current_baraka_announcer_matrix_ram'
OUT = ROOT / 'audit_v5575_current_baraka_announcer_matrix_progress'
LUA = announcer.observed.LUA
COMPLETED = []
capture.capture.__globals__.update(BASE=BASE, LUA=LUA, COMPLETED=COMPLETED)

source = inspect.getsource(original.case)
edits = {
    '    priority = qualified.gate(log, guest)':
    '    priority = qualified.gate(log, guest)\n'
    '    dual = announcer.gate(log, guest)\n'
    '    ann_faults = announcer.faults(log, guest)\n'
    "    need(len(ann_faults) == 12, 'All original actual announcer record/source/delivery faults retained')",
    '        effectiveActualPriorityFaults=rejected, audioTimerCoverage=coverage, sourceVoiceEffectRoutes=routes,':
    '        effectiveActualPriorityFaults=rejected, audioTimerCoverage=coverage, sourceVoiceEffectRoutes=routes,\n'
    '        qualifiedDualDispatcher=dual, effectiveActualAnnouncerFaults=ann_faults,',
    '    return result':
    "    print(f'{fighter} P{side} actual announcer source/table/queue/port/ADSP and12additional actual faults passed', flush=True)\n"
    '    return result',
}
for before, after in edits.items():
    need(source.count(before) == 1, 'Whole executed5560 physical/exact art/audio/priority case retained; only additive announcer gate')
    source = source.replace(before, after, 1)
scope = dict(original.__dict__, announcer=announcer, BASE=BASE, LUA=LUA, COMPLETED=COMPLETED)
exec(compile(source, __file__ + '.entire5560_actual_native_case_plus_qualified_announcer_source_delivery', 'exec'), scope)
case = scope['case']


def run():
    guest = capture.original.model.current.expected()
    parent = json.loads(PARENT.read_text())
    need(parent['passed'] and parent['goalStatus'] == 'active'
         and len(parent['effectiveActualAnnouncerFaults']) == 12
         and len(parent['retainedOriginalPriorityFaults']) == 22
         and parent['actualDualDispatcher']['actualAnnouncerCalls'] == 7
         and parent['actualDualDispatcher']['allObservedPriorityQueuesBoundToSourceDispatcher'],
         'Qualified actual current Kano-P1 announcer source plus full original objective retained')
    pins = dict(parent['newInputHashes'])
    for p in (PARENT, Path(__file__), Path(original.__file__), Path(announcer.__file__),
              Path(announcer.observed.__file__), LUA):
        pins[str(p.resolve())] = sha(p)
    need(all(sha(p) == h for p,h in pins.items()), 'Every source/current/public/retained evidence hash stable before three physical runs')
    payload = (ROOT / capture.original.model.current.NAME / 'roms/mk2ks/mk2ks.mdata').read_bytes()
    reference, gfx = capture.original.model.source_art(guest, payload, pins)
    image = capture.original.transport.source_graphics(payload, pins)
    cases, errors = [], []
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
        jobs = {pool.submit(case, spec, guest, payload, gfx, reference, pins, image): spec
                for spec in [('kano',2), ('sonya',1), ('sonya',2)]}
        for future in concurrent.futures.as_completed(jobs):
            try: cases.append(future.result())
            except Exception as error:
                errors.append(dict(context=jobs[future],error=repr(error),traceback=''.join(traceback.format_exception(error))))
    need(not errors, 'Actual native announcer matrix errors: ' + json.dumps(errors))
    cases.sort(key=lambda c:(c['fighter'],c['side']))
    pngs, compacted, terminals = [], [], []
    for c in cases:
        folder = Path(c['nativeResult']).parent
        meta = json.loads((folder/'result.json').read_text())
        terminal = json.loads((folder/'terminal.json').read_text())
        process = json.loads((folder/'process.json').read_text())
        need(meta['passed'] and terminal == meta['process'] and terminal['exit_code'] == 0
             and terminal['nativePID'] == process['pid'] == c['nativePID']
             and terminal['player'] == c['fighter'] and terminal['victim_slot'] == c['side']
             and terminal['killer'] == 'baraka' and terminal['command'] == 'bbbb_hp'
             and terminal['assistance'] == 'none' and not terminal['cheats_enabled']
             and terminal['entireOriginal921PhysicalControllerRetained']
             and not (folder/'stderr.log').read_text(), 'Each actual native true-ID context really terminal0, no guest assistance')
        need(terminal['candidate'] == capture.original.model.current.NAME
             and terminal['executable_sha256'] == capture.original.model.current.EXE_SHA
             and terminal['payload_sha256'] == capture.original.model.current.PAYLOAD_SHA,
             'Every actual current native executable/payload identity retained')
        pins.update(terminal['input_hashes'])
        terminals.append(dict(fighter=c['fighter'],side=c['side'],nativePID=process['pid'],nativeExit=0,terminalField=5198))
    for p in sorted(BASE.rglob('*')):
        if not p.is_file(): continue
        need(p.suffix.lower() not in ('.bin','.wav','.rgb','.pcm'), 'No requested raw guest/GFX/raster/audio media persisted')
        if p.suffix.lower() == '.png':
            with Image.open(p) as im:
                need(p.name == '0000.png' and p.parent.name == 'mk2ks' and p.parent.parent.name == 'snap'
                     and im.size == (400,254), 'Only original native automatic timed-exit PNGs')
            pngs.append(dict(path=str(p),bytes=p.stat().st_size,sha256=sha(p)))
        if p.suffix.lower() in ('.log','.json','.cfg','.txt'):
            before = sha(p)
            cp = subprocess.run(['compact.exe','/C','/F','/EXE:LZX','/Q',str(p)],capture_output=True)
            need(cp.returncode == 0 and sha(p) == before, 'Finished native text really force-LZX compressed without changing bytes')
            compacted.append(str(p))
        pins[str(p.resolve())] = sha(p)
    need(len(cases) == len(pngs) == len(COMPLETED) == 3
         and all(c['qualifiedDualDispatcher']['actualAnnouncerCalls'] == 7
                 and c['qualifiedDualDispatcher']['allObservedPriorityQueuesBoundToSourceDispatcher'] for c in cases)
         and all(sha(p) == h for p,h in pins.items()), 'All new actual announcer contexts, full source gates and automatic PNGs sealed with unchanged hashes')
    return dict(passed=True,observedUTC=datetime.datetime.now(datetime.timezone.utc).isoformat(),goalStatus='active',
        remaining=parent['remaining'],parentAdditiveJournal=str(PARENT),previousGoalTurnClassification=parent['thisGoalTurnClassification'],
        thisGoalTurnClassification='progress: actual original announcer source/dual-table/priority/queue/packet/port/ADSP delivery both victims and native slots; qualified firstKano-P1 reused, three new entire native physical/art/PCM/old-priority cases with36announcer and66priority effective actual faults; original125-raster/full-PCM nonperturbance per context, source-correct native name trampoline, three native automatic PNGs accounted and force-LZX retained evidence',
        retainedKanoP1Evidence=str(PARENT),cases=cases,actualNewNativeTerminals=terminals,
        newNativeBoots=3,reusedPriorQualifiedNativeBoots=1,newBuilds=0,newDeletedFiles=0,
        effectiveNewActualAnnouncerFaults=36,effectiveAllFourContextActualAnnouncerFaults=48,
        effectiveNewActualPriorityFaults=66,effectiveAllFourContextActualPriorityFaults=88,
        allNormalBarakaVictimsAndSlotsObservedAnnouncerPriorityDeliveryAccepted=True,
        allNativeQueueSuppressionCausesAccepted=False,sourceQualifiedNativeDCSWaveformAccepted=False,
        completeBarakaFinisherAudioAccepted=False,fullPortAcceptance=False,
        persistentNewNativeAutomaticExitPNGs=pngs,persistentNewNativeAutomaticPNGBytes=sum(p['bytes'] for p in pngs),
        terminalTextFilesForceLZXCompacted=len(compacted),requestedRawGuestGFXVRAMRGBPCMFilesWritten=0,
        publicPlayableChanged=False,refreshedReleaseZIP=False,newInputHashes=pins,
        nextAction='Independently bind native direct packet programs outside the priority path and full original DCS waveform; retain completed four-context native announcer/source/physical/raster/audio evidence while continuing all original remaining requirement groups.')


if __name__ == '__main__':
    need(not OUT.exists() and not BASE.exists(), 'Fresh immutable actual native announcer matrix')
    try: report = run()
    except Exception as error:
        report = dict(passed=False,error=repr(error),traceback=traceback.format_exc(),completedNativeCaptures=COMPLETED,
                      goalStatus='active',fullPortAcceptance=False)
    OUT.mkdir();capture.save(OUT/'progress.json',report)
    print(json.dumps({k:v for k,v in report.items() if k not in ('remaining','newInputHashes','cases','completedNativeCaptures')},indent=2),flush=True)
    raise SystemExit(0 if report['passed'] else 1)
