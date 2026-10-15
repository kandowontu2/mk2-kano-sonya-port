"""Whole six-fight proof; source-native absolute round-reset HP stores.

A8 is unused by the two absolute global reset stores, not a fighter pointer.
Require original full reset/damage/refill kernels, actual physical HP targets,
valid task, and exact following complete refill; never waive combat ownership.
"""
import inspect
import json
import struct
from pathlib import Path
import qualify_native_sonya_first_six_ladder_paid_controls as paid
import qualify_native_sonya_first_four_ladder_refills as original_initializer

ROOT,need,sha=paid.ROOT,paid.need,paid.sha
OUT=ROOT/'audit_native_sonya_first_six_global_reset_checked'
INIT=ROOT/'audit_native_sonya_first_six_global_reset_initializer'


def kernel():
    source=inspect.getsource(original_initializer.expected_guest)
    before="    return dict(originalRefillKernelSHA256=hashlib.sha256(guest[a:b]).hexdigest().upper(),wholeGuestSHA256=proof['sha256'])"
    after="""    for lo,hi in ((0xff8258b0,0xff8259a0),(0xff836650,0xff836750)):
        start,end=(lo-0xff800000)//8,(hi-0xff800000)//8
        need(guest[start:end]==stock[start:end], 'Entire actual current original reset/damage instruction kernel unchanged')
    for pc,address in ((0xff825930,0x010602f0),(0xff825960,0x01060ec0)):
        need(struct.unpack_from('<3H',guest,(pc-48-0xff800000)//8)==(0x0580,address&65535,address>>16),
             'Actual original reset MOVW A0 to absolute physical lifebar HP slot; A8 is unused')
    return dict(originalRefillKernelSHA256=hashlib.sha256(guest[a:b]).hexdigest().upper(),wholeGuestSHA256=proof['sha256'],
        wholeNativeResetAndDamageKernelsUnchanged=True,absoluteResetHPTargets=[0x010602f0,0x01060ec0])"""
    need(source.count(before)==1,'Entire independently reconstructed full guest plus exact original reset/damage source binding')
    scope=dict(vars(original_initializer),__file__=__file__,INIT=INIT)
    exec(compile(source.replace(before,after),__file__+'::whole_original_initializer_and_absolute_native_reset_instructions','exec'),scope)
    proof=scope['expected_guest']()
    (INIT/'native_reset_kernel_report.json').write_text(json.dumps(dict(passed=True,sourceOnlyAccepted=True,
        proof=proof,smallInitializerProbesCompiled=1,emulatorBuilds=0,nativeGameplayAccepted=False,
        inputHashes={str(Path(__file__).resolve()):sha(__file__),str(Path(original_initializer.__file__).resolve()):sha(original_initializer.__file__),
            str(ROOT/'mk2/mk2-maincpu.bin'):sha(ROOT/'mk2/mk2-maincpu.bin')},fullPortAcceptance=False),indent=2)+'\n')
    return proof


def run():
    failure_path=paid.OUT/'failure.json'
    need(failure_path.exists() and not json.loads(failure_path.read_text())['passed'], 'Original incorrect global-reset actor assumption retained')
    proof=kernel()
    scope=dict(vars(paid),__file__=__file__,OUT=OUT,reset_kernel_proof=proof)
    source=inspect.getsource(paid.prior.health_history)
    before="            need(all(0x01000000<=int(q[k],16)<0x01100000 for k in ('a8','a13')), 'Actual native health-writer actor/task context in RAM')"
    after="""            need(0x01000000<=int(q['a13'],16)<0x01100000, 'Actual native health writer task remains valid')
            if q['pc']==reset_pc:
                need(reset_kernel_proof['wholeNativeResetAndDamageKernelsUnchanged'] and index+1<len(chain) and
                     chain[index+1]['pc']==start_pc and int(chain[index+1]['frame'])==int(q['frame'])+1 and q['after']=='161',
                     'Original absolute global round-reset store immediately followed by complete native slot refill')
            else:
                need(0x01000000<=int(q['a8'],16)<0x01100000, 'Every combat/refill writer actual actor context remains in RAM')"""
    need(source.count(before)==1,'Only original absolute global reset A8 interpretation corrected')
    source=source.replace(before,after).replace('wholeObservedHPHistoryExplained=True)',
        'wholeObservedHPHistoryExplained=True,globalResetUsesAbsoluteNativeHealthStores=True,unusedGlobalResetA8NotClaimedAsActor=True)')
    exec(compile(source,__file__+'::whole_native_HP_ledger_with_absolute_global_reset','exec'),scope)
    source=inspect.getsource(paid.run)
    before='scope=dict(vars(prior),__file__=__file__,OUT=OUT)'
    after='scope=dict(vars(prior),__file__=__file__,OUT=OUT,health_history=health_history)'
    need(source.count(before)==1,'Whole existing six-fight/paid-input/fault gates use complete native HP ledger')
    source=source.replace(before,after)
    before="for p in (Path(prior.__file__).resolve(),failure,controller,"
    extra=[Path(paid.__file__).resolve(),failure_path,INIT/'report.json',INIT/'native_reset_kernel_report.json',Path(original_initializer.__file__).resolve()]
    after="for p in ("+','.join('Path('+repr(p.as_posix())+')' for p in extra)+",Path(prior.__file__).resolve(),failure,controller,"
    need(source.count(before)==1,'All original failed checker and native source proof files also pinned')
    exec(compile(source.replace(before,after),__file__+'::whole_existing_progression_and_semantic_fault_suite','exec'),scope)
    return scope['run']()


if __name__=='__main__':
    try:run()
    except Exception as error:
        need(not OUT.exists(),'Preserve actual absolute-reset successor outcome')
        OUT.mkdir();(OUT/'failure.json').write_text(json.dumps(dict(passed=False,error=repr(error),fullPortAcceptance=False),indent=2)+'\n')
        raise
