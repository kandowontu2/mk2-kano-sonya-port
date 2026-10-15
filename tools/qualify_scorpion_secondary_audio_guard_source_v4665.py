"""Entire4659 source gates, with runtime-safe native-write call syntax guard.

Literal text ':write_' in the retained palette assertion is not a write call.
The failed native boot and all original sources remain immutable.
"""
import ast,inspect,json,re,struct,subprocess
from pathlib import Path
import qualify_scorpion_secondary_audio_source_v4659 as original
import run_scorpion_secondary_audio_ram_v4664 as capture
ROOT,need,sha=capture.ROOT,capture.need,capture.sha
OUT=ROOT/'audit_v4666_scorpion_secondary_audio_guard_source_checked'
CHANGES=original.CHANGES
source=inspect.getsource(original.boundary)
before="assert(not source:find(':write_',1,true))"
after="assert(not source:match(':write_[%w_]+%s*%('))"
need(source.count(before)==1,'Only original exact wrapper runtime assertion changes')
source=source.replace(before,after)
scope=dict(vars(original),capture=capture,ROOT=ROOT,CHANGES=CHANGES)
exec(compile(source,__file__+'::whole4659_write_call_guard_boundary','exec'),scope)
whole_boundary=scope['boundary']

def boundary(wrapper=None,body=None):
    result=whole_boundary(wrapper,body)
    old=(ROOT/'mk2ks_scorpion_secondary_audio_ram_v4657.lua').read_text()
    new=(ROOT/capture.LUA).read_text()
    need(old.count(before)==1 and old.replace(before,after)==new,'Byte-exact single guard correction; no control/native/audio/tap changes')
    failed=ROOT/'audit_v4661_scorpion_secondary_kano_p1_audio_samples'
    meta=json.loads((failed/'result.json').read_text());error=(failed/'stderr.log').read_text()
    need(meta['exit_code']==3 and meta['mixedPCMUpdates']==0 and meta['nativeRGBFramesDigested']==0 and
         '4657.lua:15: assertion failed!'in error,'Actual first preboot failure retained; zero audio/gameplay accepted')
    # Equivalent match grammar on the actual retained text: assertion text is
    # admitted, actual native write invocation syntax is not. No guest write
    # is executed; counterexamples are source strings only.
    text=(ROOT/'mk2ks_jax_arms_audio_routes_ram_v4210.lua').read_text()
    pattern=r':write_[\w_]+\s*\('
    need(':write_'in text and re.search(pattern,text)is None,'Actual palette safety literal is not a native call')
    for call in('p:write_u16(0x01060280,1)','p:write_u32 (0x01060220,0)'):
        need(re.search(pattern,text+'\n'+call)is not None,'Native write call syntax counterexample rejected without execution')
    return dict(result,actualFailedNativeBootPreserved=True,onlyOneRuntimeLexicalGuardChanged=True)

main_source=inspect.getsource(original.main)
before_files="    files.extend(Path(p)for p in build['input_hashes'])"
need(main_source.count(before_files)==1,'Entire original source/fault/pin contract retained')
main_source=main_source.replace(before_files,
 "    files.extend([Path(original.__file__).resolve(),Path(capture.old.__file__).resolve(),ROOT/'mk2ks_scorpion_secondary_audio_ram_v4657.lua',ROOT/'audit_v4662_scorpion_secondary_kano_p1_audio_observed/report.json',ROOT/'audit_v4661_scorpion_secondary_kano_p1_audio_samples/result.json',ROOT/'audit_v4661_scorpion_secondary_kano_p1_audio_samples/stderr.log'])\n"+before_files)
scope=dict(vars(original),__file__=__file__,original=original,capture=capture,boundary=boundary,ROOT=ROOT,OUT=OUT)
exec(compile(main_source,__file__+'::whole4659_source_negative_and_hash_contract','exec'),scope)
main=scope['main']

if __name__=='__main__':main()
