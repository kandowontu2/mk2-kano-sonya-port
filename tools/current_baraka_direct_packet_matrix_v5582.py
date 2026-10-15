"""Complete normal victim/slot direct-packet source, actual return and delivery.

Retain the whole executed5573 native physical/art/audio/announcer/priority
case and its full terminal/pin/storage audit. Add independent packet-stack
and original direct-program/full16-bit port gates; three physical boots,
qualified Kano-P1 reused. No game edits, builds or public release changes.
"""
import inspect, json, traceback
from pathlib import Path
import current_baraka_announcer_matrix_v5573 as original
import qualify_current_baraka_direct_packets_v5580 as direct

origin = direct.observed
ROOT, need, sha = direct.ROOT, direct.need, direct.sha
capture = direct.capture
PARENT = direct.OUT / 'progress.json'
BASE = ROOT / 'audit_v5583_current_baraka_direct_packet_matrix_ram'
OUT = ROOT / 'audit_v5584_current_baraka_direct_packet_matrix_progress'
LUA = origin.LUA
COMPLETED = []
capture.capture.__globals__.update(BASE=BASE, LUA=LUA, COMPLETED=COMPLETED)

# This is the canonical full case source retained by5573, not a smaller
# replacement and not inspect.getsource on an exec-generated function.
source = original.source
edits = {
    '    ann_faults = announcer.faults(log, guest)':
    '    ann_faults = announcer.faults(log, guest)\n'
    '    packet_sources = direct.gate(log, guest)\n'
    '    origin_faults = origin.faults(log, guest)\n'
    '    direct_faults = direct.faults(log, guest)\n'
    "    need(len(origin_faults) == 10 and len(direct_faults) == 12, 'Entire actual origin and direct-source/full-word fault suites')",
    '        qualifiedDualDispatcher=dual, effectiveActualAnnouncerFaults=ann_faults,':
    '        qualifiedDualDispatcher=dual, effectiveActualAnnouncerFaults=ann_faults,\n'
    '        actualDirectPacketSources=packet_sources, effectiveActualPacketOriginFaults=origin_faults,\n'
    '        effectiveDirectSourceBranchAndPortFaults=direct_faults,',
    "    print(f'{fighter} P{side} actual announcer source/table/queue/port/ADSP and12additional actual faults passed', flush=True)":
    "    print(f'{fighter} P{side} actual complete direct-source/return/full-word/ADSP and22additional faults passed', flush=True)",
}
for before, after in edits.items():
    need(source.count(before) == 1, 'Entire original5573 actual native case retained with additive direct-packet gates')
    source = source.replace(before, after, 1)
scope = dict(original.scope, direct=direct, origin=origin, BASE=BASE, LUA=LUA, COMPLETED=COMPLETED)
exec(compile(source, __file__ + '.entire5573_native_case_plus_original_direct_packet_semantics', 'exec'), scope)
case = scope['case']

source = inspect.getsource(original.run)
before = """    need(parent['passed'] and parent['goalStatus'] == 'active'
         and len(parent['effectiveActualAnnouncerFaults']) == 12
         and len(parent['retainedOriginalPriorityFaults']) == 22
         and parent['actualDualDispatcher']['actualAnnouncerCalls'] == 7
         and parent['actualDualDispatcher']['allObservedPriorityQueuesBoundToSourceDispatcher'],
         'Qualified actual current Kano-P1 announcer source plus full original objective retained')"""
after = """    need(parent['passed'] and parent['goalStatus'] == 'active'
         and parent['allCapturedKanoP1NormalBarakaDirectPacketSourceSemanticsAccepted']
         and len(parent['effectiveDirectSourceBranchAndPortFaults']) == 12,
         'Qualified actual current Kano-P1 complete direct packet source and full original objective retained')"""
need(source.count(before) == 1, 'Whole actual native matrix run with qualified direct-source parent')
source = source.replace(before, after, 1)
edits = {
    '              Path(announcer.observed.__file__), LUA):':
    '              Path(announcer.observed.__file__), Path(direct.__file__), Path(origin.__file__), LUA):',
    "'All new actual announcer contexts, full source gates and automatic PNGs sealed with unchanged hashes'":
    "'All new actual direct packet contexts, entire prior source gates and automatic PNGs sealed with unchanged hashes'",
    "thisGoalTurnClassification='progress: actual original announcer source/dual-table/priority/queue/packet/port/ADSP delivery both victims and native slots; qualified firstKano-P1 reused, three new entire native physical/art/PCM/old-priority cases with36announcer and66priority effective actual faults; original125-raster/full-PCM nonperturbance per context, source-correct native name trampoline, three native automatic PNGs accounted and force-LZX retained evidence'":
    "thisGoalTurnClassification='progress: all four normal true victim/slot contexts complete original direct packet programs and actual branch flags bound to real caller/stack/return and full16-bit port/ADSP delivery; qualified Kano-P1 reused and three whole native physical/art/PCM/announcer/priority captures,30new origin and36new direct-source/full-word faults; every125-raster/full-PCM baseline unchanged, three timed PNGs accounted and finished evidence force-LZX compressed'",
    '        allNormalBarakaVictimsAndSlotsObservedAnnouncerPriorityDeliveryAccepted=True,':
    '        allNormalBarakaVictimsAndSlotsObservedAnnouncerPriorityDeliveryAccepted=True,\n'
    '        allNormalBarakaVictimsAndSlotsDirectPacketSourceAndReturnDeliveryAccepted=True,\n'
    '        effectiveNewActualPacketOriginFaults=30, effectiveAllFourContextActualPacketOriginFaults=40,\n'
    '        effectiveNewDirectSourceBranchAndPortFaults=36, effectiveAllFourContextDirectSourceBranchAndPortFaults=48,\n'
    '        allNativeDirectBranchCombinationsAccepted=False,',
    "nextAction='Independently bind native direct packet programs outside the priority path and full original DCS waveform; retain completed four-context native announcer/source/physical/raster/audio evidence while continuing all original remaining requirement groups.'":
    "nextAction='Independently qualify full original DCS waveform and broaden actual native branch/stage/finisher contexts; retain completed four-context direct/source/return/full-word/ADSP and entire original physical/art/audio proof while continuing every original remaining requirement group.'",
}
for before, after in edits.items():
    need(source.count(before) == 1, 'Full5573 native terminal/pins/nonperturbance/storage audit retained: '+before)
    source = source.replace(before, after, 1)
scope = dict(original.__dict__, direct=direct, origin=origin, case=case, ROOT=ROOT, PARENT=PARENT,
             BASE=BASE, OUT=OUT, LUA=LUA, COMPLETED=COMPLETED, capture=capture, __file__=__file__)
exec(compile(source, __file__ + '.entire5573_native_matrix_audit_plus_direct_packet_acceptance', 'exec'), scope)
run = scope['run']

if __name__ == '__main__':
    need(not OUT.exists() and not BASE.exists(), 'Fresh immutable actual native direct packet matrix')
    try:
        report = run()
    except Exception as error:
        report = dict(passed=False, error=repr(error), traceback=traceback.format_exc(),
                      completedNativeCaptures=COMPLETED, goalStatus='active', fullPortAcceptance=False)
    OUT.mkdir(); capture.save(OUT / 'progress.json', report)
    print(json.dumps({k:v for k,v in report.items() if k not in ('remaining','newInputHashes','cases','completedNativeCaptures')},indent=2),flush=True)
    raise SystemExit(0 if report['passed'] else 1)
