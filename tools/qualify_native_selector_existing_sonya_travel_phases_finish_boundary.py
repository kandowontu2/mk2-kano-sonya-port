"""Exact adjacent finisher table operand, not a changed native fall routine.

Old range ends halfway through FF876B50's finisher-table pointer. Prove the
full source-derived32-bit replacement and every surrounding byte. Preserve
both original failures, whole phases and corrected actual store timing.
"""
import inspect
import struct
import qualify_native_selector_existing_sonya_travel_phases as original
import qualify_native_selector_existing_sonya_travel_phases_store_timing as timing

ROOT,need,sha=original.ROOT,original.need,original.sha
OUT=ROOT/'audit_native_selector_existing_sonya_travel_phases_finish_boundary_checked'
need(sha(timing.__file__)=='7E2FB686A107C983205FDD0DAD444B21C5BA541F1FE428D8AF590DE21DC64561' and
     sha(timing.OUT/'failure.json')=='F21D2A4CFD21F5B2A767C2CBB4F7CFAF53EF2E31CB89E4ADACC9A7BADC03F330',
     'Exact original fall-range rejection preserved')


def adjacent_finish_operand(guest,stock):
    lo,hi=(0xff876650-0xff800000)//8,(0xff876b70-0xff800000)//8
    at=(0xff876b50-0xff800000)//8
    need(struct.unpack_from('<I',stock,at)[0]==0xff8ba210 and
         struct.unpack_from('<I',guest,at)[0]==0xff800000+0xf4320*8,
         'Only full source-derived native19-row finisher table pointer')
    expected=bytearray(stock[lo:hi])
    struct.pack_into('<I',expected,at-lo,0xff800000+0xf4320*8)
    need(guest[lo:hi]==expected,'Every fall byte and full neighboring operand, no blanket source exception')
    table=(0xff8ba210-0xff800000)//8
    need(guest[0xf4320:0xf4320+17*4]==stock[table:table+17*4],
         'All seventeen existing effective finisher rows preserved')
    return True


scope=dict(vars(original),OUT=OUT,original=original,timing=timing,
           adjacent_finish_operand=adjacent_finish_operand,__file__=__file__)
for function in (original.square_followup,original.square_gate,original.bicycle_gate,original.gate,original.execute):
    source=inspect.getsource(function)
    if function is original.square_followup:
        source=original.replace(source,'[(2036,2),(2047,2)]','[(2035,2),(2046,2)]')
    if function is original.bicycle_gate:
        marker="    source=replace(source,\"pair=state.verify_log(log,'kano',guest)\",\"pair=ledger.gate(log,guest);source_gate(log,guest)\")"
        source=original.replace(source,marker,marker+'''
    source=replace(source,"assert guest[a:b]==original[a:b],'Original physical fall/cleanup/ready unchanged'",
        "assert guest[a:b]==original[a:b] or ((lo,hi)==(0xff876650,0xff876b60) and adjacent_finish_operand(guest,original)), 'Original fall/cleanup/ready plus exact adjacent finisher operand'")
    source=replace(source,"directNativeFallTapAccepted=False", "directNativeFallTapAccepted=False,adjacentFinisherOperandSourceQualified=True")
''')
        source=original.replace(source,'ledger=ledger,source_gate=source_gate)',
                                'ledger=ledger,source_gate=source_gate,adjacent_finish_operand=adjacent_finish_operand)')
    if function is original.execute:
        source=original.replace(source,'paths=[Path(__file__),PARENT,',
            "paths=[Path(__file__),Path(original.__file__),original.OUT/'failure.json',Path(timing.__file__),timing.OUT/'failure.json',PARENT,")
    exec(compile(source,__file__+'::whole_original_'+function.__name__,'exec'),scope)
execute=scope['execute']
gate=scope['gate']
