"""Direct complete successor: corrected native opcode and unambiguous scope.

Keeps every original compiled whole-window/guard/ownership check, and additionally
requires native CMPI disassembly and rejects the actual predecessor ANDI code.
Executed failing wrappers and their original results are never changed.
"""
import inspect
from pathlib import Path
import check_native_shang_drain_source as original_module

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'audit_native_shang_drain_native_opcode_source'
FRAGMENT = ROOT / 'source_native_shang_drain_compare/native_shang_owned_drain.inc'


def main():
    scope = dict(vars(original_module), original_module=original_module, OUT=OUT,
                 FRAGMENT=FRAGMENT, GENERATION=FRAGMENT.parent / 'generation-report.json', __file__=__file__)
    for function, before, after in (
        (original_module.independent_router, 'emit(0x0b80,', 'emit(0x0b60,'),
        (original_module.run_router_model, 'elif op == 0x0b80:', 'elif op == 0x0b60:'),
    ):
        source = inspect.getsource(function)
        original_module.need(source.count(before) == 1, 'One exact opcode correction in independent assembler/interpreter')
        source = source.replace(before, after, 1)
        exec(compile(source, __file__ + '::' + function.__name__, 'exec'), scope)
    exec(compile(inspect.getsource(original_module.independent_guest),
                 __file__ + '::same_whole_guest_model_with_scoped_corrected_assembler', 'exec'), scope)
    source = inspect.getsource(original_module.main)
    def change(before, after):
        nonlocal source
        original_module.need(source.count(before) == 1, 'Exact complete predecessor checker boundary: ' + before)
        source = source.replace(before, after, 1)
    change("'ill' not in disasm.stdout.lower()",
           "'ill' not in disasm.stdout.lower() and 'ANDI' not in disasm.stdout and\n"
           "         all(disasm.stdout.count(f'CMPI   {addr(at):08X}h,A0') == 1 for row in PAL for at in row)")
    change('    model_cases = 0\n', '''    bad_opcode_model_rejected = False
    try:
        run_router_model(original_module.independent_router(), addr(PAL[0][0]), 17, 0, 0x12345678)
    except ValueError as error:
        need('Unexpected helper opcode 0B80' in str(error), 'Exact predecessor ANDI must be rejected, not an unrelated failure')
        bad_opcode_model_rejected = True
    need(bad_opcode_model_rejected, 'Original bad instruction sequence no longer passes the model')
    model_cases = 0
''')
    change('Path(__file__), FRAGMENT, GENERATION',
           "Path(__file__), Path(original_module.__file__),\n"
           "            ROOT / 'tools/check_native_shang_drain_compare_source.py',\n"
           "            ROOT / 'tools/check_native_shang_drain_compare_scoped_source.py',\n"
           "            ROOT / 'tools/stage_native_shang_drain_compare.py',\n"
           "            ROOT / 'tools/stage_native_shang_drain_tables.py',\n"
           "            ROOT / 'audit_native_shang_drain_opcode_failure/report.json',\n"
           "            ROOT / 'audit_native_shang_drain_compare_model_scope_failure/report.json',\n"
           "            ROOT / 'audit_native_shang_drain_compare_scope_alias_failure/report.json',\n"
           "            ROOT / 'mame-mkp/src/devices/cpu/tms34010/tms34010.h',\n"
           "            ROOT / 'mame-mkp/src/devices/cpu/tms34010/34010dsm.cpp',\n"
           "            ROOT / 'mame-mkp/src/devices/cpu/tms34010/34010ops.hxx', FRAGMENT, GENERATION")
    change('paletteRouterBytes=len(code),',
           'paletteRouterBytes=len(code), exactFourNativeCMPIInstructionsAccepted=True,\n'
           '                  actualPredecessorANDIOpcodeRejected=bad_opcode_model_rejected,\n'
           '                  predecessorSourceQualificationAccepted=False,')
    exec(compile(source, __file__ + '::entire_original_suite_plus_real_opcode_contract', 'exec'), scope)
    return scope['main']()


if __name__ == '__main__':
    main()
