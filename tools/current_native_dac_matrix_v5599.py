"""Whole native DAC-to-mixer waveform for both added victims/native slots.

Reuse source-qualified Kano-P1. Three physical cold boots retain the full
5573 physical/art/voice/announcer/priority case and5582 direct-source/return
gates. Add the already qualified5596 entire native DAC and source-clock
waveform capture. No game edits, builds, raw audio or release promotion.
"""
import json, traceback
from pathlib import Path
import current_baraka_direct_packet_matrix_v5582 as matrix
import current_native_dac_clock_v5596 as clock_model

ROOT,need,sha=matrix.ROOT,matrix.need,matrix.sha
direct,origin=matrix.direct,matrix.origin
capture=matrix.capture
PARENT=clock_model.OUT/'progress.json'
BASE=ROOT/'audit_v5600_current_native_dac_matrix_ram'
OUT=ROOT/'audit_v5601_current_native_dac_matrix_progress'
LUA=clock_model.original.LUA
COMPLETED=[]
capture.capture=clock_model.native_capture
capture.capture.__globals__.update(BASE=BASE,LUA=LUA,COMPLETED=COMPLETED)

# Canonical complete5573 case; restore the entire5582 additive gates rather
# than trying inspect.getsource on an exec-generated function.
source=matrix.original.source
edits={
    '    ann_faults = announcer.faults(log, guest)':
    '    ann_faults = announcer.faults(log, guest)\n'
    '    packet_sources = direct.gate(log, guest)\n'
    '    origin_faults = origin.faults(log, guest)\n'
    '    direct_faults = direct.faults(log, guest)\n'
    "    need(len(origin_faults)==10 and len(direct_faults)==12,'All original complete direct-source/return/full-word fault suites')\n"
    '    dac_source=meta["actualNativeDACSourceProof"];waveform=meta["nativeDACToMixedPCMComparison"]\n'
    '    dac_faults=meta["effectiveActualNativeDACFaults"]\n'
    '    need(dac_source["passed"] and dac_source["callbacks"]==685 and len(dac_faults)==4\n'
    '         and waveform["passed"] and waveform["differentChannelSamples"]==0\n'
    '         and waveform["comparedStereoFrames"]==657600\n'
    '         and waveform["predictedSHA256"]==waveform["actualSHA256"]\n'
    '         and len(waveform["effectiveActualWholeWaveformFaults"])==4,\n'
    '         "Entire actual native DAC and all source-clock predicted PCM samples/faults accepted in true victim slot")',
    '        qualifiedDualDispatcher=dual, effectiveActualAnnouncerFaults=ann_faults,':
    '        qualifiedDualDispatcher=dual, effectiveActualAnnouncerFaults=ann_faults,\n'
    '        actualDirectPacketSources=packet_sources, effectiveActualPacketOriginFaults=origin_faults,\n'
    '        effectiveDirectSourceBranchAndPortFaults=direct_faults,actualNativeDACSourceProof=dac_source,\n'
    '        effectiveActualNativeDACFaults=dac_faults,nativeDACToMixedPCMComparison=waveform,',
    "    print(f'{fighter} P{side} actual announcer source/table/queue/port/ADSP and12additional actual faults passed', flush=True)":
    "    print(f'{fighter} P{side} complete685 native DAC callbacks and657600stereo source-clock waveform frames exact; all prior gates passed', flush=True)",
}
for before,after in edits.items():
    need(source.count(before)==1,'Entire original5573 case plus5582 gates retained; only additive qualified DAC/full-waveform acceptance')
    source=source.replace(before,after,1)
scope=dict(matrix.original.scope,direct=direct,origin=origin,BASE=BASE,LUA=LUA,COMPLETED=COMPLETED,capture=capture)
exec(compile(source,__file__+'.entire5573_native_case_plus5582_packet_and5596_DAC_waveform_gates','exec'),scope)
case=scope['case']

# Canonical entire5582 full native terminal, source pins, nonperturbance,
# exact current binary, PNG accounting and force-LZX evidence audit.
source=matrix.source
before="""    need(parent['passed'] and parent['goalStatus'] == 'active'
         and parent['allCapturedKanoP1NormalBarakaDirectPacketSourceSemanticsAccepted']
         and len(parent['effectiveDirectSourceBranchAndPortFaults']) == 12,
         'Qualified actual current Kano-P1 complete direct packet source and full original objective retained')"""
after="""    need(parent['passed'] and parent['goalStatus']=='active'
         and parent['allObservedKanoP1NativeDACToMixerWaveformSourceExact']
         and parent['nativeDACToMixedPCMComparison']['differentChannelSamples']==0
         and len(parent['nativeDACToMixedPCMComparison']['effectiveActualWholeWaveformFaults'])==4,
         'Actual completed Kano-P1 whole source-clock native waveform and full original objective retained')"""
need(source.count(before)==1,'Complete native matrix starts from actual executed whole waveform proof')
source=source.replace(before,after,1)
edits={
    '              Path(announcer.observed.__file__), Path(direct.__file__), Path(origin.__file__), LUA):':
    '              Path(announcer.observed.__file__), Path(direct.__file__), Path(origin.__file__),\n'
    '              Path(matrix.__file__),Path(clock_model.__file__),Path(clock_model.original.__file__),LUA):',
    "thisGoalTurnClassification='progress: all four normal true victim/slot contexts complete original direct packet programs and actual branch flags bound to real caller/stack/return and full16-bit port/ADSP delivery; qualified Kano-P1 reused and three whole native physical/art/PCM/announcer/priority captures,30new origin and36new direct-source/full-word faults; every125-raster/full-PCM baseline unchanged, three timed PNGs accounted and finished evidence force-LZX compressed'":
    "thisGoalTurnClassification='progress: all four normal true victim/slot contexts entire native DAC-to-mixer waveform source-exact without timing/gain fits; reuse qualified Kano-P1 and three whole physical/art/voice/announcer/priority/direct-source/return/ADSP/PCM captures, every685DAC callbacks and657600stereo frames per context exact,12new DAC and12new whole-waveform faults with all original fault suites retained; every125-raster/full-PCM baseline unchanged, three timed PNGs accounted and terminal evidence force-LZX compressed'",
    '        allNativeDirectBranchCombinationsAccepted=False,':
    '        allNativeDirectBranchCombinationsAccepted=False,\n'
    '        allNormalBarakaVictimsAndSlotsObservedNativeDACToMixerWaveformSourceExact=True,\n'
    '        allFourContextDACCallbacks=2740,allFourContextStereoFramesCompared=2630400,\n'
    '        effectiveNewActualNativeDACFaults=12,effectiveAllFourContextActualNativeDACFaults=16,\n'
    '        effectiveNewActualWholeWaveformFaults=12,effectiveAllFourContextActualWholeWaveformFaults=16,\n'
    '        independentOriginalStockMixedWaveformOracleAccepted=False,',
    "nextAction='Independently qualify full original DCS waveform and broaden actual native branch/stage/finisher contexts; retain completed four-context direct/source/return/full-word/ADSP and entire original physical/art/audio proof while continuing every original remaining requirement group.'":
    "nextAction='Capture genuine original MK2 sound references through physical play using the confirmed stock mk2 driver, without guest writes/proxies or synthetic audio; retain completed four-context entire DAC-to-mixer/source/return/ADSP proof and continue all original stage/move/finisher/CPU/campaign/combined-UI/cleanup/release requirements.'",
}
for before,after in edits.items():
    need(source.count(before)==1,'Entire5582 terminal/source/nonperturbance/storage audit preserved with additive full waveform matrix: '+before)
    source=source.replace(before,after,1)
scope=dict(matrix.scope,ROOT=ROOT,PARENT=PARENT,BASE=BASE,OUT=OUT,LUA=LUA,COMPLETED=COMPLETED,
           capture=capture,case=case,matrix=matrix,clock_model=clock_model,__file__=__file__)
exec(compile(source,__file__+'.entire5582_actual_native_matrix_audit_plus_entire_source_clock_waveform','exec'),scope)
run=scope['run']

if __name__=='__main__':
    need(not BASE.exists() and not OUT.exists(),'Fresh immutable entire native DAC/waveform matrix')
    try:report=run()
    except Exception as error:
        report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),completedNativeCaptures=COMPLETED,
                    goalStatus='active',fullPortAcceptance=False)
    OUT.mkdir();capture.save(OUT/'progress.json',report)
    print(json.dumps({k:v for k,v in report.items()if k not in ('remaining','newInputHashes','cases','completedNativeCaptures')},indent=2),flush=True)
    raise SystemExit(0 if report['passed']else 1)
