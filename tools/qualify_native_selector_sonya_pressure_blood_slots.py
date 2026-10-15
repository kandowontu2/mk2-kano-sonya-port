"""Preserve actual169-slot rejection; execute whole stock final-link semantics.

FF80E070 zeroes *A2, not *A1: its final link to the extra169th address is
overwritten. The source-defined native list contains168 records. No game
change, dropped callback or weaker ownership/projection/pool assertion.
"""
import inspect
import json
from pathlib import Path
import qualify_native_selector_sonya_pressure_blood as original

ROOT,need,sha=original.ROOT,original.need,original.sha
OUT=ROOT/'audit_native_selector_sonya_pressure_blood_slots_checked'
FAILURE=original.OUT/'failure.json'
SCOPE=None


def stock_main_records(final_pointer='A2'):
    # Exact already-disassembled original initialization, including the final
    # destination operand. The emulator's DSJS decrements before testing zero.
    a0,a3,a1=0,0xa8,0x01068ea0;head=a1;memory={}
    while True:
        a2=a1;a1+=0x6f0;memory[a2]=a1;a3-=1
        if a3==0:break
    memory[a2 if final_pointer=='A2'else a1]=a0
    records=[];at=head
    while at:
        need(at in memory and at not in records,'Whole source-defined Main initialization links')
        records.append(at);at=memory[at]
    return set(records)


def task_lists(groups):
    source=inspect.getsource(original.task_lists)
    before='expected={0x01068ea0+i*0x6f0 for i in range(169)}'
    need(source.count(before)==1,'One exact incorrect derived pool-size assumption')
    source=source.replace(before,'expected=stock_main_records()',1)
    source=source.replace('source-defined169 Main','source-defined168 Main')
    scope=dict(original.task_lists.__globals__,stock_main_records=stock_main_records)
    exec(compile(source,__file__+'::whole_original_list_gates_exact_final_A2_store','exec'),scope)
    return scope['task_lists'](groups)


def gate(groups,guest):
    source=inspect.getsource(original.gate)
    need(source.count('wholeMainSlotsPerSnapshot=169')==1,'One corresponding report-count assumption')
    source=source.replace('wholeMainSlotsPerSnapshot=169','wholeMainSlotsPerSnapshot=168',1)
    scope=dict(original.gate.__globals__,task_lists=task_lists)
    exec(compile(source,__file__+'::whole_original_blood_gate_stock168_linked_slots','exec'),scope)
    return scope['gate'](groups,guest)


def safe_execute(state):
    global SCOPE
    failed=json.loads(FAILURE.read_text())
    need(not failed['passed']and failed['error']==
         "ValueError('Entire source-defined169 Main records partition into native active/free lists')",
         'Actual original169-slot rejection preserved unchanged')
    need(len(stock_main_records())==168 and len(stock_main_records('A1'))==169,
         'Exact final A2 store differs effectively from incorrect A1 substitute')
    cpu_source=ROOT/'diagnostic_native_selector_layers_long/input_sources/mame-mkp/src/devices/cpu/tms34010/34010ops.hxx'
    code=cpu_source.read_text();start=code.index('#define DSJS(R)');end=code.index('void tms340x0_device::dsjs_a',start)
    need('if (--R##REG(DSTREG(op)))'in code[start:end],'Compiled DSJS decrement/test-zero semantics')
    source=inspect.getsource(original.execute)
    before="for p in (Path(__file__),Path(disasm.__file__),ROOT/'mame-mkp/unidasm.exe',ROOT/'mk2/mk2-maincpu.bin',parent_path):"
    need(source.count(before)==1,'Keep whole original positive/pin/publication contract')
    source=source.replace(before,
        "for p in (Path(__file__),Path(original.__file__),FAILURE,cpu_source,Path(disasm.__file__),ROOT/'mame-mkp/unidasm.exe',ROOT/'mk2/mk2-maincpu.bin',parent_path):",1)
    SCOPE=dict(original.__dict__,OUT=OUT,__file__=__file__,gate=gate,original=original,FAILURE=FAILURE,cpu_source=cpu_source)
    exec(compile(source,__file__+'::whole_actual_blood_proof_exact_source_link_count','exec'),SCOPE)
    wrapper=inspect.getsource(original.safe_execute)
    exec(compile(wrapper,__file__+'::whole_original_failure_preservation','exec'),SCOPE)
    return SCOPE['safe_execute'](state)
