"""Bind the existing typed Friendship entry router and actual frame-zero callback.

Preserve the failed all-stock-entry assumption. All arithmetic/source/cache/FIFO
and23 fault checks are retained; only the real compiled entry wrapper and the
actual native callback schedule are modeled. No game rerun or source mutation.
"""
import inspect
import json
import struct
from pathlib import Path
import qualify_native_selector_sonya_pressure_palette as previous

ROOT,need,sha=previous.ROOT,previous.need,previous.sha
OUT=ROOT/'audit_native_selector_sonya_pressure_palette_router_checked'
FAILURE=previous.OUT/'failure.json'
SCOPE=None


def expected_guest():
    result=bytearray((ROOT/'mk2/mk2-maincpu.bin').read_bytes())
    address=lambda at:0xff800000+at*8
    cursor=0xfc540
    def emit(*words):
        nonlocal cursor
        data=struct.pack('<'+'H'*len(words),*words)
        result[cursor:cursor+len(data)]=data;cursor+=len(data)
    def branch(op,target):
        at=cursor+2;emit(op,target&65535,target>>16);return at
    def movi(reg,value):emit(0x09e0+reg,value&65535,value>>16)
    need(result[0xfc540:0xfc600]==b'\xff'*0xc0, 'Independently reserved router/prologue space')
    emit(0x01e0,0x0b60,0x08ef,0x0132)
    other=branch(0xcb80,0)
    emit(0x01c0,0x098f,0x0400)
    movi(5,0);movi(0,address(0xfc500));branch(0x0d5f,address(0xfc5c0))
    emit(0x09af,0x0020,0x0960)
    struct.pack_into('<I',result,other,address(cursor))
    emit(0x01c0);branch(0xc080,address(0xfc5c0))
    need(cursor<=0xfc5c0, 'Full typed router fits original reservation')
    cursor=0xfc5c0
    emit(0x098f,0x7800,0x09c3,0x003c)
    branch(0xc080,0xff80cfa0)
    need(cursor<=0xfc600, 'Exact stolen prologue and original continuation fit')
    struct.pack_into('<4H',result,(0xff80cf60-0xff800000)//8,
                     0xc080,address(0xfc540)&65535,address(0xfc540)>>16,0x0300)
    return bytes(result)


def source_gate(guest):
    original=(ROOT/'mk2/mk2-maincpu.bin').read_bytes()
    value=previous.source_gate(original)
    model=expected_guest()
    ranges=tuple(value['ranges'])+((0xff800000+0xfc540*8,0xff800000+0xfc600*8),)
    for lo,hi in ranges:
        a,z=(lo-0xff800000)//8,(hi-0xff800000)//8
        need(guest[a:z]==model[a:z], 'Whole actual typed entry/router/prologue and unchanged native arithmetic')
    value['ranges']=ranges
    value['actualTypedFriendshipEntryRouterIndependentlyAssembled']=True
    value['originalNativeReferenceArithmeticUnchanged']=True
    value['actualNativeFrameDoneSchedule']='0..3617; initial0; terminal3618; no terminal frame_done fabricated'
    return value


def safe_execute(state,events=None):
    global SCOPE
    failure=json.loads(FAILURE.read_text())
    need(not failure['passed'] and failure['error']==
         "ValueError('Entire original native palette arithmetic/reset source unchanged')",
         'Actual original patched-entry assumption failure preserved')
    execute_source=inspect.getsource(previous.execute)
    before="SOURCE=dict(source,stock=(ROOT/'mk2/mk2-maincpu.bin').read_bytes())"
    need(execute_source.count(before)==1, 'Only actual compiled palette-entry model boundary')
    execute_source=execute_source.replace(before,'SOURCE=dict(source,stock=expected_guest())',1)
    before='for p in (Path(__file__),Path(observed.__file__),binding.OUT/\'report.json\',ROOT/\'mame-mkp/unidasm.exe\'):'
    need(execute_source.count(before)==1, 'Whole original source/evidence inventory retained')
    execute_source=execute_source.replace(before,
        'for p in (Path(__file__),Path(previous.__file__),FAILURE,Path(observed.__file__),binding.OUT/\'report.json\',ROOT/\'mame-mkp/unidasm.exe\'):',1)
    gate_source=inspect.getsource(previous.gate)
    before='frames==list(range(1,3619))'
    need(gate_source.count(before)==1, 'Original whole callback schedule gate retained')
    gate_source=gate_source.replace(before,'frames==list(range(0,3618))',1)
    SCOPE=dict(previous.__dict__,previous=previous,OUT=OUT,FAILURE=FAILURE,
               expected_guest=expected_guest,source_gate=source_gate,__file__=__file__)
    exec(compile(gate_source,__file__+'::whole_arithmetic_real_native_frame_zero','exec'),SCOPE)
    exec(compile(execute_source,__file__+'::whole23_faults_actual_compiled_entry','exec'),SCOPE)
    exec(compile(inspect.getsource(previous.safe_execute),__file__+'::failure_preservation','exec'),SCOPE)
    return SCOPE['safe_execute'](state,events)
