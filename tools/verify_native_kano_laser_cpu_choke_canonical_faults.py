"""Same actual terminal and initializer: canonical JSON integer-key comparison.

Preserve the executed host comparison rejection. JSON stringifies integer
dictionary keys; no native field, health total, or fault gate is changed.
"""
import hashlib
import inspect
import json
from pathlib import Path
import verify_native_kano_laser_cpu_choke_approach as prior

OUT=prior.ROOT/'audit_native_kano_laser_cpu_choke_canonical_fault_checked'


def verify(cases,failed_locals):
    need,sha=prior.need,prior.sha
    case=failed_locals['case'];positive=failed_locals['positive']
    need(not prior.OUT.exists() and not OUT.exists() and
         case!=positive['sourceBoundBodyShadowSemantics'] and
         json.loads(json.dumps(case))==positive['sourceBoundBodyShadowSemantics'] and
         case['state']['wholeNativeHealthHistory']['totalNativeDamageByPhysicalSlot']=={1:42,2:0},
         'Exact original rejection is solely native integer dictionary keys versus persisted JSON keys')
    prior.OUT.mkdir()
    failure_path=prior.OUT/'failure.json'
    prior.live.base.save(failure_path,dict(passed=False,
        error="ValueError('Exact original positive restored before actual faults')",
        nativeReplay=False,actualNativeExit=positive['nativeExit'],
        originalCheckerSHA256=sha(prior.__file__),jsonCanonicalEquality=True,
        actualNativeDamageByPhysicalSlot=case['state']['wholeNativeHealthHistory']['totalNativeDamageByPhysicalSlot'],
        fullPortAcceptance=False,goalStatus='active'))
    guest=failed_locals['guest'];build=failed_locals['build']
    need(hashlib.sha256(guest).hexdigest().upper()==build['expected_guest_sha256'],
         'Reuse same entire independently compiled expected guest, never replay native gameplay')
    source=inspect.getsource(prior.verify)
    first=source.index('    scope=dict(vars(live.base.ui)');last=source.index('    native,',first)
    source=source[:first]+"    guest,gfx,build=(original_failed_locals[k]for k in('guest','gfx','build'))\n"+source[last:]
    before='gfx32=live.base.reconstruct(native,pins)'
    need(source.count(before)==1,'Exact retained ROM reconstruction boundary')
    source=source.replace(before,"gfx32=original_failed_locals['gfx32']")
    before="need(case==positive['sourceBoundBodyShadowSemantics'],'Exact original positive restored before actual faults')"
    need(source.count(before)==1,'Exact original failed comparison only')
    source=source.replace(before,"need(json.loads(json.dumps(case))==positive['sourceBoundBodyShadowSemantics'],'Exact original positive restored after native JSON key canonicalization')")
    before='for p in(Path(__file__),source_path,'
    need(source.count(before)==1,'Pin preserved failed checker and actual retained initializer')
    source=source.replace(before,'for p in(failure_path,Path(prior.__file__),Path(__file__),source_path,')
    scope=dict(vars(prior),OUT=OUT,__file__=__file__,prior=prior,failure_path=failure_path,original_failed_locals=failed_locals)
    exec(compile(source,__file__+'::whole_original_fault_checks_same_actual_RAM_after_JSON_key_canonicalization','exec'),scope)
    return scope['verify'](cases)
