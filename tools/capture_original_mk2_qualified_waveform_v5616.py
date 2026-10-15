"""Whole stock RAM capture with qualified physical/name gates before buffer disposal.

Reuse the exact native5606 Lua, no new game/controller edits. Preserve every
old failure and the completed no-replay5615 physical/source proof. Actual
stock DAC/PCM are compared in RAM using the original integer source clock.
This stock control is not a substitute for full added-character acceptance.
"""
import inspect
import json
import struct
import traceback
from pathlib import Path
import capture_original_mk2_native_tables_v5607 as transport
import qualify_original_mk2_baraka_provenance_v5614 as qualified

original=transport.original
ROOT,need,sha=original.ROOT,original.need,original.sha
PARENT=qualified.OUT/'progress.json'
FOLDER=ROOT/'audit_v5617_original_mk2_qualified_waveform_ram/cage_p1'
OUT=ROOT/'audit_v5618_original_mk2_qualified_waveform_progress'
source=transport.source
old_physical=inspect.getsource(original.physical)
need(source.count(old_physical)==1,'One entire canonical physical gate, not an inspect of a generated function')
source=source.replace(old_physical,qualified.source,1)
edits={
    "PARENT = ROOT / 'audit_v5601_current_native_dac_matrix_progress/progress.json'":
        "PARENT = ROOT / 'audit_v5615_original_mk2_baraka_control_provenance_qualified/progress.json'",
    "FOLDER = ROOT / 'audit_v5608_original_mk2_native_tables_audio_ram/cage_p1'":
        "FOLDER = ROOT / 'audit_v5617_original_mk2_qualified_waveform_ram/cage_p1'",
    "OUT = ROOT / 'audit_v5609_original_mk2_native_tables_audio_progress'":
        "OUT = ROOT / 'audit_v5618_original_mk2_qualified_waveform_progress'",
    "              Path(original.__file__), FAILURE, ROOT/'mk2_stock_baraka_audio_reference_v5602.lua',":
        "              Path(original.__file__), FAILURE, ROOT/'mk2_stock_baraka_audio_reference_v5602.lua',\n"
        "              Path(transport.__file__), Path(qualified.__file__), Path(qualified.previous.__file__),\n"
        "              ROOT/'tools/qualify_original_mk2_baraka_control_v5610.py',",
    "    state = physical(log)":
        "    state = physical(log)\n    physical_faults=qualified.previous.scope['physical_faults'](log)",
    """    # The current packet gate may expose stock-specific callers. Retain that
    # result honestly; original waveform transport acceptance does not hide it.
    try:
        packets = dict(passed=True, proof=direct.gate(log, stock), effectiveFaults=direct.faults(log, stock))
    except Exception as error:
        packets = dict(passed=False, error=repr(error), traceback=traceback.format_exc())""":
        "    packets = qualified.previous.scope['packet_gate'](log, stock)\n"
        "    need(packets['passed'] and len(packets['effectiveFaults'])==12 and len(physical_faults)==9,\n"
        "         'Actual complete stock name/source/packet gate and all prior physical faults retained')",
    "        nativeCaptureResult=str(FOLDER / 'result.json'), nativeTerminal=terminal, originalPhysicalProof=state,":
        "        nativeCaptureResult=str(FOLDER / 'result.json'), nativeTerminal=terminal, originalPhysicalProof=state,\n"
        "        effectiveOriginalPhysicalFaults=physical_faults, sourceQualifiedOriginalMixedWaveformAccepted=True,",
    "previousGoalTurnClassification='no progress: acknowledgement and read-only cleanup status did not change implementation or qualification'":
        "previousGoalTurnClassification=parent['thisGoalTurnClassification']",
}
for before,after in edits.items():
    need(source.count(before)==1,'Whole native stock capture retains all source/transport/PCM/DAC/fault/terminal/storage gates')
    source=source.replace(before,after,1)
scope=dict(__name__='whole_stock5616_qualified_live_capture',__file__=__file__,struct=struct,
           original=original,transport=transport,qualified=qualified,FAILURE=transport.FAILURE)
exec(compile(source,__file__+'.entire5607_stock_capture_with_whole5614_physical_and_stock_name_source_gates','exec'),scope)

if __name__=='__main__':
    need(not FOLDER.exists() and not OUT.exists(),'Fresh immutable full original native waveform capture')
    parent=json.loads(PARENT.read_text())
    need(parent['passed'] and parent['originalPacketQualification']['passed']
         and len(parent['effectiveOriginalPhysicalFaults'])==9 and not parent['sourceQualifiedOriginalMixedWaveformAccepted'],
         'Completed genuine stock physical/source control and honest earlier unexecuted waveform status')
    try:
        report=scope['run']()
        waveform=report['originalDACToMixedPCMProof']
        need(waveform['passed'] and waveform['comparedStereoFrames']==657600 and waveform['differentChannelSamples']==0
             and len(report['effectiveActualDCSROMByteFaults'])==8
             and len(report['effectiveOriginalDACFaults'])==4
             and len(waveform['effectiveActualWholeWaveformFaults'])==4,
             'Every original whole mixed-waveform sample plus actual ROM/DAC/waveform faults accepted')
        report['thisGoalTurnClassification']='progress: fresh genuine original mk2 Cage2/Baraka3 physical control with corrected, previously qualified input/direction/name/source gates retained; both whole stock sound ROM checkpoints source-exact with8actual byte faults, all685actualDACcallbacks signed16 normalization exact with4actual faults and657600stereo frames source-clock exact with4whole-waveform faults. Complete9physical and12source/full-word/packet/return/ADSP faults retained. Original waveform is now qualified; equality to added-character gameplay and every original remaining group remain unproven.'
        report['nextAction']='Compare corresponding source-owned stock and added-character sound routes, priority decisions, native effect packets and waveform phases without fitted timing/gain or whole-scene identity substitution; retain qualified original/port source-clock proof and advance all original stage/move/finisher/CPU/campaign/UI/cleanup/release requirements.'
    except Exception as error:
        report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),goalStatus='active',
                    fullPortAcceptance=False,parentAdditiveJournal=str(PARENT))
    scope['seal'](report)
    print(json.dumps({k:report[k] for k in ('passed','error','nativeTerminal','originalPCMCallbacks','originalPCMBytes',
        'sourceQualifiedOriginalMixedWaveformAccepted','persistentNativeAutomaticPNGBytes') if k in report},indent=2),flush=True)
    raise SystemExit(0 if report['passed']else 1)
