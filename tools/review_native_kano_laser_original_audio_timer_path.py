"""Preserve real original fourth-slot timer early-return path.

Actual FFAA8570 JRNE FFAA87B0 skips fifth-slot timer while fourth slot
remains nonzero. The initial simplified all-five decrement model failed at
age206: fifth slot was0027, not invented0026. Correct from whole original
instructions and observed state, preserving that failed checker/evidence.
"""
import inspect
import struct
from pathlib import Path
import review_native_kano_laser_original_audio_allocator as prior

ROOT=prior.ROOT
OUT=ROOT/'audit_native_kano_laser_original_audio_timer_path_review'


def main():
    failure=prior.OUT/'failure.txt'
    prior.need('Every actual sound-helper priority/time/continuation state' in failure.read_text(),
               'Actual initial uniform-timer model failure conserved')
    blob=(ROOT/'mk3/mk3-maincpu.bin').read_bytes()
    prior.need(struct.unpack_from('<H',blob,(0xffaa8570-0xff800000)//8)[0]==0xcb23,
               'Actual complete original branch is JRNE to shared return, not next-slot timer')
    scope=dict(vars(prior),OUT=OUT,__file__=__file__)
    contract=inspect.getsource(prior.contract)
    old="""next_state=[]
            for priority,duration,stream in state:
                need(stream==0,'This earned trace uses no unmodeled continuation stream')
                after=max(0,duration-1)
                next_state.append((0 if duration==1 else priority,after,0))
            state=next_state"""
    new="""next_state=list(state)
            for slot,(priority,duration,stream) in enumerate(state):
                need(stream==0,'This earned trace uses no unmodeled continuation stream')
                after=max(0,duration-1)
                next_state[slot]=(0 if duration==1 else priority,after,0)
                if slot==3 and duration>1:break
            state=next_state"""
    prior.need(contract.count(old)==1,'Only real source timer branch semantics corrected')
    contract=contract.replace(old,new)
    old='sourceTimerInvocations=301,sourceTimerThroughAge=300,'
    new="sourceTimerInvocations=301,sourceTimerThroughAge=300,fifthSlotPostponementInvocations=sum(parse_slots(r)[3][1]>1 and parse_slots(r)[4][1]>0 for r in timer),sourceTimerEarlyReturnPC='FFAA8570',"
    prior.need(contract.count(old)==1,'Actual nonvacuous skipped-slot count reported')
    contract=contract.replace(old,new)
    exec(compile(contract,__file__+'::complete_actual_timer_path','exec'),scope)
    source=inspect.getsource(prior.main)
    changes=[('paths=[Path(__file__),Path(burst.__file__),',
        "paths=[Path(__file__),ROOT/'tools/review_native_kano_laser_original_audio_allocator.py',ROOT/'audit_native_kano_laser_original_audio_allocator_review/failure.txt',Path(burst.__file__),"),
        ('scope_path=ROOT/',"""try:original_uniform_contract(text)
        except ValueError as error:faults.append(dict(name='uniform_all_five_timer_model',rejected=str(error)))
        else:raise ValueError('Unsupported uniform timer admitted')
        need(result['fifthSlotPostponementInvocations']>0,'Real fourth/fifth-slot timer overlap is nonvacuous')
        scope_path=ROOT/"""),
        ("'Preserve five independent source sound slots and derive packet offset from slot, not a hardcoded observed packet.',",
         "'Preserve five independent source sound slots and derive packet offset from slot, not a hardcoded observed packet.',\n                'Preserve actual fourth-slot remaining-timer early return atFFAA8570; do not uniformly decrement fifth-slot lifetime while fourth remains nonzero.',")]
    for old,new in changes:
        prior.need(source.count(old)==1,'Complete failed-model provenance and strict source timer gate')
        source=source.replace(old,new)
    scope['original_uniform_contract']=prior.contract
    exec(compile(source,__file__+'::all_original_records_packets_and_states','exec'),scope)
    scope['main']()


if __name__=='__main__':main()
