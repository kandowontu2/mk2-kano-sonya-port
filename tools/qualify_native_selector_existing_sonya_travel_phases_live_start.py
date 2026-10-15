"""Whole square/bicycle phases in actual startup and native follow-up context.

Include the additional original startup flag-clear before action setup. It is
qualified, not omitted from the whole state ledger or counted as a move lock.
Preserve all earlier observer/profile binding rejections and their source.
"""
import inspect
import struct
from pathlib import Path
import qualify_native_selector_existing_sonya_travel_phases as original
import qualify_native_selector_existing_sonya_travel_phases_store_timing as timing
import qualify_native_selector_existing_sonya_travel_phases_finish_boundary as boundary
import qualify_native_selector_existing_sonya_travel_phases_finish_bound as bound

ROOT,need,sha=original.ROOT,original.need,original.sha
OUT=ROOT/'audit_native_selector_existing_sonya_travel_phases_live_start_checked'


def startup_flags(log,guest,actor,main,start,end):
    flags=[r for r in original.bicycle.state.original.flag_rows(log) if
           r['slot']==2 and start<=r['frame']<=end]
    extra=[r for r in flags if r['kind']=='flags' and r['pc']==0xff9b3b40]
    need(len(extra)==1,'One actual original AI startup clear, not arbitrary ignored stores')
    r=extra[0]
    need(r['frame']==start and r['before']==r['after']==0 and r['at']==main+0x210 and
         (r['actor'],r['main'],r['a8'],r['a13'],r['id'],r['state'])==(actor,main,actor,main,18,0) and
         struct.unpack_from('<HH',guest,(r['pc']-32-0xff800000)//8)==(r['op0'],r['op1']),
         'Exact instruction/operands/owner and zero-valued native startup store')
    first_setup=next(r for r in flags if r['kind']=='action')
    need(flags.index(extra[0])<flags.index(first_setup), 'Startup clear precedes actual special setup')
    return [r for r in flags if r is not extra[0]]


scope=dict(vars(original),OUT=OUT,original=original,timing=timing,boundary=boundary,bound=bound,
           adjacent_finish_operand=boundary.adjacent_finish_operand,startup_flags=startup_flags,__file__=__file__)
for function in (original.square_followup,original.square_gate,original.bicycle_gate,original.gate,original.execute):
    source=inspect.getsource(function)
    if function is original.square_followup:
        source=original.replace(source,'[(2036,2),(2047,2)]','[(2035,2),(2046,2)]')
    if function is original.bicycle_gate:
        marker="    source=replace(source,\"pair=state.verify_log(log,'kano',guest)\",\"pair=ledger.gate(log,guest);source_gate(log,guest)\")"
        source=original.replace(source,marker,marker+'''
    source=replace(source,"assert guest[a:b]==original[a:b],'Original physical fall/cleanup/ready unchanged'",
        "assert guest[a:b]==original[a:b] or ((lo,hi)==(0xff876650,0xff876b60) and adjacent_finish_operand(guest,original)), 'Original fall/cleanup/ready plus exact adjacent finisher operand'")
    source=replace(source,"flags=[r for r in state.original.flag_rows(log)if r['slot']==2 and start<=r['frame']<=end]",
        "flags=startup_flags(log,guest,actor,main,start,end)")
''')
        source=original.replace(source,'ledger=ledger,source_gate=source_gate)',
            'ledger=ledger,source_gate=source_gate,adjacent_finish_operand=adjacent_finish_operand,startup_flags=startup_flags)')
    if function is original.execute:
        source=original.replace(source,'paths=[Path(__file__),PARENT,',
            "paths=[Path(__file__),*(Path(m.__file__) for m in (original,timing,boundary,bound)),*(m.OUT/'failure.json' for m in (original,timing,boundary,bound)),PARENT,")
    exec(compile(source,__file__+'::whole_original_'+function.__name__,'exec'),scope)
execute=scope['execute']
gate=scope['gate']
