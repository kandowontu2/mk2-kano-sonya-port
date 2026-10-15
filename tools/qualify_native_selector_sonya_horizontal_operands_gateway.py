"""Full operand suite with the exact existing paired-throw boundary gateway.

Preserve both actual rejected sources/results. Reconstruct all gateway words
from the compiled canonical emitter, including every branch and untouched
padding; the rest of each motion routine must still equal the stock ROM.
No gameplay change, new capture, or broad source-comparison waiver.
"""
import json
import struct
from pathlib import Path
import qualify_native_selector_sonya_horizontal_operands_bound as previous
import verify_native_source_sync as migration

ROOT,need,sha=previous.ROOT,previous.need,previous.sha
SOURCE=ROOT/'mame-mkp/src/mame/midway/midtunit_m.cpp'
FAIL=ROOT/'audit_native_selector_sonya_horizontal_operands_bound_checked/failure.json'
need(json.loads(FAIL.read_text())['error']==
     "ValueError('Complete original native motion/store/clamp routines unchanged')",
     'Original actual boundary-source rejection preserved')


def boundary_source(guest,stock):
    need(sha(SOURCE)=='A32C860194808831589A7D06F47A564708162B723391801EC5A310113767ACDD',
         'Whole canonical compiled boundary emitter unchanged')
    expected=bytearray(b'\xff'*0x200);cursor=0;labels={};branches=[]
    address=lambda offset:0xff800000+(0xf1700+offset)*8
    def emit(*words):
        nonlocal cursor
        struct.pack_into('<'+'H'*len(words),expected,cursor,*words);cursor+=2*len(words)
    def branch(op,label):
        branches.append((cursor+2,label));emit(op,0,0)
    def label(name):labels[name]=cursor
    emit(0x07a3,0x0220,0x0106,0x4843);branch(0xcb80,'p2')
    emit(0x07a3,0x0260,0x0106);branch(0xc080,'process')
    label('p2');emit(0x07a3,0x0e30,0x0106)
    label('process');emit(0x4c63);branch(0xca80,'normal')
    emit(0xb465,0x01f0,0x0b45,0xfdea);branch(0xca80,'bicycle_pair')
    emit(0xb465,0x01f0,0x0b45,0xfeee);branch(0xca80,'leg_pair')
    emit(0x0b45,0xfeed);branch(0xcb80,'normal')
    emit(0xb665,0x0140,0xb4a5,0x01f0,0x0b45,0xffee);branch(0xcb80,'normal')
    emit(0xb663,0x0170,0xb463,0x01f0,0x0b43,0xfeee);branch(0xcb80,'normal');emit(0x0960)
    label('leg_pair');emit(0xb665,0x0140,0xb4a5,0x01f0,0x0b45,0xffed);branch(0xcb80,'normal')
    emit(0xb663,0x0170,0xb463,0x01f0,0x0b43,0xfeef);branch(0xcb80,'normal');emit(0x0960)
    label('bicycle_pair');emit(0xb665,0x0140,0xb4a5,0x01f0,0x0b45,0xffed);branch(0xcb80,'normal')
    emit(0xb663,0x0170,0xb463,0x01f0,0x0b43,0xfdeb);branch(0xcb80,'normal');emit(0x0960)
    label('normal');emit(0xb443,0x0090,0x4803,0xc080,0x5510,0xff80)
    for offset,name in branches:struct.pack_into('<I',expected,offset,address(labels[name]))
    need(guest[0xf1700:0xf1900]==expected,
         'All existing gateway selector/paired-state/branch/displaced MOVE-CMP/return words and padding source-exact')
    lo,hi=(0xff8054e0-0xff800000)//8,(0xff805680-0xff800000)//8
    need(stock[lo:lo+6]==struct.pack('<3H',0xb443,0x0090,0x4803),
         'Exact six displaced stock boundary bytes')
    original=bytearray(stock[lo:hi]);struct.pack_into('<HI',original,0,0xc080,address(0))
    need(guest[lo:hi]==original,
         'Only existing six-byte JA gateway differs; every remaining native boundary/clamp byte unchanged')
    return dict(passed=True,gatewayStart='FFF8B800',gatewayBytes=cursor,
                completeReservedBytes=512,branchOperands=len(branches),
                allOtherBoundaryBytesStock=True,gameplayChanged=False)


original_source=previous.original_source
original_failure=previous.original_failure
source=original_source.read_text()
for before,after in (
    ('else3191','else 3191'),
    ("OUT=ROOT/'audit_native_selector_sonya_horizontal_operands_checked'",
     "OUT=ROOT/'audit_native_selector_sonya_horizontal_operands_gateway_checked'"),
    ("need(guest[a:b]==stock[a:b],'Complete original native motion/store/clamp routines unchanged')",
     "need(guest[a:b]==stock[a:b] or ((lo,hi)==(0xff8054e0,0xff805680) and boundary_source(guest,stock)), 'Complete native motion routines and exact existing paired boundary gateway')"),
    ('for p in (Path(__file__),path,Path(prior.__file__),Path(geometry.__file__),',
     'for p in (Path(__file__),original_source,original_failure,Path(previous.__file__),FAIL,SOURCE,path,Path(prior.__file__),Path(geometry.__file__),')):
    need(source.count(before)==1,'Exact original suite boundary, no motion/operand/status/fault rule removed')
    source=source.replace(before,after,1)
exec(compile(source,str(original_source)+'::whole_operand_suite_exact_compiled_boundary_gateway','exec'))


original_execute=execute
def execute(state):
    # These isolated source faults must hit the newly explicit gateway proof,
    # not merely the independent whole-guest digest that precedes it.
    stock=(ROOT/'mk2/mk2-maincpu.bin').read_bytes()
    gateway=boundary_source(state['guest'],stock);faults=[]
    for label,at in (('gateway_target',(0xff8054f0-0xff800000)//8),
                     ('normal_clamp',(0xff805610-0xff800000)//8),
                     ('actor_selector',0xf1700+2),('paired_action',0xf1700+0x32),
                     ('displaced_move',0xf1700+gateway['gatewayBytes']-12),
                     ('ordinary_return',0xf1700+gateway['gatewayBytes']-4),
                     ('reserved_padding',0xf18fe)):
        bad=bytearray(state['guest']);bad[at]^=1
        try:boundary_source(bad,stock)
        except(ValueError,AssertionError)as error:faults.append(dict(kind=label,rejectedBy=str(error)))
        else:raise ValueError('Corrupted source gateway accepted: '+label)
    need(boundary_source(state['guest'],stock)==gateway,'Full untouched source gateway restored')
    result=original_execute(state)
    result['exactExistingBoundaryGateway']=gateway
    result['effectiveBoundarySourceFaultsRejected']=faults
    result['originalBoundarySourceFailurePreserved']=str(FAIL)
    (OUT/'report.json').write_text(json.dumps(result,indent=2)+'\n')
    return result
