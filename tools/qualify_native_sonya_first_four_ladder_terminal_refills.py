"""Complete actual native refill chains plus exact explicitly stopped tail.

The last run ended at355187 while its next match was filling the bars. Keep
both actual 26-store partial chains, verify every recorded step, and never
claim their missing final161 stores or subsequent combat were observed.
"""
import inspect
import json
from pathlib import Path
import qualify_native_sonya_first_four_ladder_refills as refill

ROOT, need, sha = refill.ROOT, refill.need, refill.sha
OUT = ROOT / 'audit_native_sonya_first_four_ladder_terminal_refills_checked'


def source_proof():
    report=json.loads((refill.INIT/'report.json').read_text())
    need(report['passed'] and report['sourceOnlyAccepted'] and report['wholeExpectedGuestSHA256']==
         '8234D0D3E25480018C3F4A68B5F5C8F24A1839F54E7887C260084D43E6B6C479' and
         report['smallInitializerProbesCompiled']==1 and not report['nativeGameplayAccepted'] and
         not any(p.suffix.lower() in ('.exe','.bin') for p in refill.INIT.rglob('*')),
         'Same already executed whole-guest/original-kernel initializer, generated probe absent')
    return dict(originalRefillKernelSHA256=report['wholeOriginalNativeRefillKernelSHA256'],wholeGuestSHA256=report['wholeExpectedGuestSHA256'])


def run():
    previous_failure=refill.OUT/'failure.json'
    need(previous_failure.exists() and not json.loads(previous_failure.read_text())['passed'],
         'Original complete-chain assumption failure preserved')
    stop=json.loads((refill.prior.FOLDER/'explicit_unsuccessful_physical_policy_stop.json').read_text())
    need(stop['physicalPolicyUnsuccessful'] and not stop['stoppedSolelyForObservationTimeout'],
         'Actual explicit unsuccessful policy stop, not a naturally completed next round')
    scope=dict(vars(refill),__file__=__file__,OUT=OUT,expected_guest=source_proof,previous_failure=previous_failure)
    source=inspect.getsource(refill.refills)
    before="            for age,value in enumerate([*range(4,161,2),161]):"
    after="""            observed=80 if index!=starts[-1][0] else len(stores)-index-1
            need(observed==80 or (index==starts[-1][0] and frame==355163 and observed==25 and
                 int(stores[-1]['frame'])==355187 and stores[-1]['after']=='52'),
                 'Only exact original last25-step native fill prefix after explicit stop may be incomplete')
            for age,value in enumerate([*range(4,161,2),161][:observed]):"""
    need(source.count(before)==1, 'Exact full previous refill grammar retained; only actual explicitly stopped final prefix accounted')
    source=source.replace(before,after)
    before="actualStores=81,actor=actor,main=task"
    after="actualStores=observed+1,complete=(observed==80),actor=actor,main=task"
    need(source.count(before)==1, 'No completed refill credited for incomplete actual final tail')
    source=source.replace(before,after)
    before="return dict(completeNativeRefillSequences=446,totalNativeRefillStores=446*81,completeAllHealthStoreCoverage=True,source=REFILL_PROOF)"
    after="""need(sum(q['complete'] for q in sequences)==444 and sum(not q['complete'] for q in sequences)==2,
         '444 complete native refills; only two terminal partial physical-slot chains remain incomplete')
    return dict(completeNativeRefillSequences=444,totalNativeRefillStores=sum(q['actualStores'] for q in sequences),
        partialTerminalRefills=[q for q in sequences if not q['complete']],
        incompleteFinalRefillsNotAcceptedAsCompleted=True,completeObservedHealthStoreCoverage=True,source=REFILL_PROOF)"""
    need(source.count(before)==1, 'Honest complete/prefix health coverage report')
    exec(compile(source.replace(before,after),__file__+'::whole_original_refills_and_exact_terminal_prefix','exec'),scope)
    source=inspect.getsource(refill.run)
    before="for p in (Path(prior.__file__).resolve(),failure,INIT/'report.json',ROOT/'mk2/mk2-maincpu.bin',Path(audio.__file__).resolve()):"
    after="for p in (Path(refill.__file__).resolve(),previous_failure,Path(prior.__file__).resolve(),failure,INIT/'report.json',ROOT/'mk2/mk2-maincpu.bin',Path(audio.__file__).resolve()):"
    need(source.count(before)==1, 'All original failed checkers/outcomes plus native-source proofs retained')
    scope['refill']=refill
    exec(compile(source.replace(before,after),__file__+'::whole_original_progression_and_semantic_fault_suite','exec'),scope)
    return scope['run']()


if __name__=='__main__':
    try: run()
    except Exception as error:
        need(not OUT.exists(),'Preserve original actual successor outcome')
        OUT.mkdir();(OUT/'failure.json').write_text(json.dumps(dict(passed=False,error=repr(error),fullPortAcceptance=False),indent=2)+'\n')
        raise
