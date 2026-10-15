"""Whole original stock capture; fix only port-specific CSS/win addresses.

Preserve the actual first failure and its sources. No changes to the failed
files, original guest, physical inputs, sound source or waveform predictor.
"""
import json
import traceback
from pathlib import Path
import capture_original_mk2_baraka_audio_v5603 as original

ROOT = original.ROOT
FAILURE = original.OUT / 'progress.json'
FOLDER = ROOT / 'audit_v5608_original_mk2_native_tables_audio_ram/cage_p1'
OUT = ROOT / 'audit_v5609_original_mk2_native_tables_audio_progress'
LUA = ROOT / 'mk2_stock_baraka_audio_native_tables_v5606.lua'
source = Path(original.__file__).read_text()
edits = {
    "FOLDER = ROOT / 'audit_v5604_original_mk2_baraka_audio_ram/cage_p1'":
        "FOLDER = ROOT / 'audit_v5608_original_mk2_native_tables_audio_ram/cage_p1'",
    "OUT = ROOT / 'audit_v5605_original_mk2_baraka_audio_progress'":
        "OUT = ROOT / 'audit_v5609_original_mk2_native_tables_audio_progress'",
    "LUA = ROOT / 'mk2_stock_baraka_audio_reference_v5602.lua'":
        "LUA = ROOT / 'mk2_stock_baraka_audio_native_tables_v5606.lua'",
    "    for p in (PARENT, Path(__file__), LUA, STOCK, EXE, Path(clock.__file__), Path(rom.__file__),":
        "    for p in (PARENT, Path(__file__), LUA, STOCK, EXE, Path(clock.__file__), Path(rom.__file__),\n"
        "              Path(original.__file__), FAILURE, ROOT/'mk2_stock_baraka_audio_reference_v5602.lua',",
}
for before, after in edits.items():
    original.need(source.count(before) == 1, 'Whole stock capture with only fresh leaf/Lua and preserved failure pins')
    source = source.replace(before, after, 1)
scope = dict(__name__='original_stock5607_guarded_whole_capture', __file__=__file__, original=original, FAILURE=FAILURE)
exec(compile(source, __file__+'.entire5603_capture_native_table_wrapper_only', 'exec'), scope)


if __name__ == '__main__':
    original.need(not FOLDER.exists() and not OUT.exists(), 'Fresh immutable corrected original reference')
    failure = json.loads(FAILURE.read_text())
    original.need(not failure['passed'] and failure['error'] == "ValueError('Actual stock process terminal0, no script/transport errors')",
                  'Actual first original selection-controller failure retained')
    old = original.FOLDER
    original.need(json.loads((old/'terminal.json').read_text())['exit_code'] == 0
                  and 'No native CSS route' in (old/'stderr.log').read_text()
                  and 'sha256=45B3285496DB555EFAF4A3608A4F59845DD47A82E4A0593607E0592F47B36F23' in (old/'run.log').read_text(),
                  'Original first process genuinely terminal0, stock guest source exact, actual failed native route')
    try:
        report = scope['run']()
    except Exception as error:
        report = dict(passed=False, error=repr(error), traceback=traceback.format_exc(), goalStatus='active',
                      fullPortAcceptance=False, parentAdditiveJournal=str(original.PARENT))
    report.update(preservedOriginalStockSelectionFailure=str(FAILURE), newNativeBootsSincePortFrontier=2,
                  correctedNativeTableAddresses=dict(left='FF898000', right='FF8980C0', down='FF897F40', roundWins='FF822280'))
    scope['seal'](report)
    print(json.dumps({k: report[k] for k in ('passed', 'error', 'nativeTerminal', 'originalPCMCallbacks',
        'originalPCMBytes', 'persistentNativeAutomaticPNGBytes') if k in report}, indent=2), flush=True)
    if report.get('originalPacketQualification'):
        print('Original packet gate passed=' + str(report['originalPacketQualification']['passed']), flush=True)
    raise SystemExit(0 if report['passed'] else 1)
