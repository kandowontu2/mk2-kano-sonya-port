"""Bind actual palette-cache reference inputs; do not invent their arithmetic.

The native count is a measured cache input, not a count of visible blood.
Preserve actual refs2->3 counterexample and all former assertions. Independently
bind each modeled reference count to its immutable native read recording.
Hidden cache-owner and increment/decrement arithmetic remain explicitly open.
"""
import gzip
import inspect
import json
import re
from pathlib import Path
import qualify_native_selector_sonya_pressure_blood_epoch as epoch

ROOT,need,sha=epoch.ROOT,epoch.need,epoch.sha
OUT=ROOT/'audit_native_selector_sonya_pressure_blood_refs_checked'
FAILURE=epoch.OUT/'failure.json'
REFERENCE_INPUTS=None
SCOPE=None


def reference_inputs():
    capture=epoch.palette.original.previous.original.capture
    native=capture.NATIVE_HANDLES[capture.KEY]
    need(native['process'].poll()==0,'Original45272 reference inputs remain terminal')
    folder=capture.RAM_CASES[capture.KEY][0];log=folder/'run.log.gz'
    proof=json.loads((capture.OUT/'report.json').read_text())
    need(sha(log)==proof['inputHashes'][str(log.resolve())],
         'Whole original immutable compressed native read recording intact')
    result={}
    with gzip.open(log,'rt',encoding='utf-8')as source:
        for line in source:
            if not line.startswith('MK2_EFFECT_QUEUE '):continue
            r=dict(re.findall(r'(\w+)=([^\s]+)',line))
            key=int(r['frame']),int(r['cursor'],16),int(r['actor'],16),int(r['bank'],16)
            need(key not in result and r['writes']=='0'and r['assistance']=='none',
                 'Every native cache-input read capsule unique and passive')
            result[key]=int(r['refs'])
    return result


def gate(groups,guest):
    need(REFERENCE_INPUTS is not None,'Actual native cache-input capsule independently loaded')
    for q in groups['QUEUE']:
        key=q['frame'],q['cursor'],q['actor'],q['bank']
        need(key in REFERENCE_INPUTS and q['refs']==REFERENCE_INPUTS[key],
             'Every modeled cache-reference input equals its actual immutable native word read')
    result=epoch.gate(groups,guest)
    result['actualReferenceCountInputProvenanceAccepted']=True
    result['actualNativeReferenceInputCapsules']=len(REFERENCE_INPUTS)
    result['nativeReferenceIncrementDecrementArithmeticAccepted']=False
    result['unpublishedPaletteOwnersIndividuallyAccepted']=False
    return result


def safe_execute(state):
    global REFERENCE_INPUTS,SCOPE
    failed=json.loads(FAILURE.read_text())
    need(not failed['passed']and failed['error']==
         "ValueError('Effective actual blood counterexample accepted: actual_blood_publication_refs')",
         'Actual reference-input counterexample preserved, no source or native replay')
    REFERENCE_INPUTS=reference_inputs()
    bound=epoch.palette.original
    source=inspect.getsource(bound.execute)
    before='for p in (Path(__file__),Path(previous.__file__),parent_path,'
    need(source.count(before)==1,'Entire original22-fault/full-positive/companion contract retained')
    source=source.replace(before,
        'for p in (Path(__file__),Path(epoch.__file__),FAILURE,Path(epoch.palette.__file__),epoch.FAILURE,Path(bound.__file__),epoch.palette.FAILURE,Path(previous.__file__),parent_path,',1)
    SCOPE=dict(bound.__dict__,OUT=OUT,__file__=__file__,gate=gate,epoch=epoch,FAILURE=FAILURE,bound=bound)
    exec(compile(source,__file__+'::whole_actual22_faults_reference_input_provenance_not_arithmetic_substitute','exec'),SCOPE)
    wrapper=inspect.getsource(bound.safe_execute)
    exec(compile(wrapper,__file__+'::whole_original_failure_preservation','exec'),SCOPE)
    return SCOPE['safe_execute'](state)
