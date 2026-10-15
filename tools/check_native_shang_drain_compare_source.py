"""Full successor qualification, with exact opcode semantics and ANDI rejection.

The executed predecessor source/results remain intact but are NOT accepted.
All original whole-window, typed stream and fault tests are retained unchanged.
"""
import inspect
from pathlib import Path
import check_native_shang_drain_source as prior

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'audit_native_shang_drain_compare_source'
FRAGMENT = ROOT / 'source_native_shang_drain_compare/native_shang_owned_drain.inc'


def main():
    scope = dict(vars(prior), prior=prior, OUT=OUT, FRAGMENT=FRAGMENT,
                 GENERATION=FRAGMENT.parent / 'generation-report.json', __file__=__file__)
    for function, old, new in ((prior.independent_router, 'emit(0x0b80,', 'emit(0x0b60,'),
                               (prior.run_router_model, 'elif op == 0x0b80:', 'elif op == 0x0b60:')):
        source = inspect.getsource(function)
        prior.need(source.count(old) == 1, 'Exact independent assembler/interpreter native-opcode correction')
        source = source.replace(old, new, 1)
        exec(compile(source, __file__ + '::' + function.__name__, 'exec'), scope)
    source = inspect.getsource(prior.main)
    old = "'ill' not in disasm.stdout.lower()"
    new = ("'ill' not in disasm.stdout.lower() and 'ANDI' not in disasm.stdout and\n"
           "         all(disasm.stdout.count(f'CMPI   {addr(at):08X}h,A0') == 1 for row in PAL for at in row)")
    prior.need(source.count(old) == 1, 'Real native instruction text must prove all FOUR nonmutating compares')
    source = source.replace(old, new, 1)
    old = '    model_cases = 0\n'
    new = '''    bad_opcode_model_rejected = False
    try:
        run_router_model(prior.independent_router(), addr(PAL[0][0]), 17, 0, 0x12345678)
    except ValueError as error:
        need('Unexpected helper opcode 0B80' in str(error), 'Reject actual predecessor ANDI, not an unrelated error')
        bad_opcode_model_rejected = True
    need(bad_opcode_model_rejected, 'The exact original bad instruction sequence is no longer accepted')
    model_cases = 0
'''
    prior.need(source.count(old) == 1, 'Entire original ownership/stack/status model retained plus actual ANDI rejection')
    source = source.replace(old, new, 1)
    old = 'Path(__file__), FRAGMENT, GENERATION'
    new = ("Path(__file__), Path(prior.__file__), ROOT / 'tools/stage_native_shang_drain_compare.py',\n"
           "            ROOT / 'tools/stage_native_shang_drain_tables.py',\n"
           "            ROOT / 'audit_native_shang_drain_opcode_failure/report.json',\n"
           "            ROOT / 'mame-mkp/src/devices/cpu/tms34010/tms34010.h',\n"
           "            ROOT / 'mame-mkp/src/devices/cpu/tms34010/34010dsm.cpp',\n"
           "            ROOT / 'mame-mkp/src/devices/cpu/tms34010/34010ops.hxx', FRAGMENT, GENERATION")
    prior.need(source.count(old) == 1, 'Pin the complete predecessor and authoritative local CPU instruction definitions')
    source = source.replace(old, new, 1)
    old = 'paletteRouterBytes=len(code),'
    new = ("paletteRouterBytes=len(code), exactFourNativeCMPIInstructionsAccepted=True,\n"
           "                  actualPredecessorANDIOpcodeRejected=bad_opcode_model_rejected,\n"
           "                  predecessorSourceQualificationAccepted=False,")
    prior.need(source.count(old) == 1, 'Do not silently promote the known wrong predecessor')
    source = source.replace(old, new, 1)
    exec(compile(source, __file__ + '::whole_original_qualification_plus_exact_instruction_semantics', 'exec'), scope)
    return scope['main']()


if __name__ == '__main__':
    main()
