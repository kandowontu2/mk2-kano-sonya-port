"""Corruption fixtures plus rejection of the genuinely floating prior build."""
import json
import re
import verify_jax_clap_positions_v1036 as proof

OUT=proof.ROOT/'audit_v1037_jax_clap_proof_units'
if OUT.exists():raise ValueError('Preserve fixture results')
texts={case:(proof.ROOT/case/'run.log').read_text(encoding='utf-8-sig') for case in proof.CASES}
original_match=proof.heads.pixel_match
cache={}
def cached(path,indices,palette,flip):
    # Cache only exact immutable PNG and exact pixels/palette/flip inputs.
    key=(proof.digest(path),indices.tobytes(),palette.tobytes(),flip)
    if key not in cache:cache[key]=original_match(path,indices,palette,flip)
    return cache[key]
proof.heads.pixel_match=cached
results=[]
try:
    assert proof.verify(texts,check_files=False)['passed']
    case=proof.CASES[0];text=texts[case]
    alterations={
        'proxy_identity':text.replace('ids=11,17','ids=11,1',1),
        'wrong_native_row':text.replace('value=0005FFA0','value=FFFBFFA0',1),
        'wrong_wrap_timing':text.replace('age=188 actor=','age=189 actor=',1),
        'invalid_collision_chain':text.replace('before=161 after=121 pc=FF836700','before=160 after=121 pc=FF836700',1),
        'body_float':re.sub(r'(_QUEUE[^\n]*source=0F600000[^\n]* y=)82( floor=82)',r'\g<1>72\2',text,count=1),
        'omitted_release_hold':re.sub(r'^MK2_STOCK_HEAD_V921_INPUT frame=3091[^\n]*button=Low_Punch\r?\n','',text,count=1,flags=re.M),
    }
    for name,changed in alterations.items():
        assert changed!=text,'Fixture did not change '+name
        report=proof.verify({**texts,case:changed},check_files=False)
        assert not report['passed'],'Corrupt fixture accepted: '+name
        results.append({'fixture':name,'rejected':True,'errors':report['errors']})
    saved=proof.CANDIDATE,proof.CASES
    proof.CANDIDATE='diagnostic_v1024_native_jax_clap_positions'
    proof.CASES=tuple(f'audit_v1025_jax_{name}_p{side}_clap_positions' for name in ('kano','sonya') for side in (1,2))
    try:
        report=proof.verify(check_files=False)
        assert not report['passed'] and any('no floating' in error for error in report['errors'])
        results.append({'fixture':'actual_negative_offset_candidate1024','rejected':True,'errors':report['errors']})
    finally:
        proof.CANDIDATE,proof.CASES=saved
finally:
    proof.heads.pixel_match=original_match
OUT.mkdir()
(OUT/'unit-results.json').write_text(json.dumps({'passed':True,'baselineAccepted':True,'corruptionAndActualRejectedBuildChecks':len(results),'results':results},indent=2)+'\n')
print(json.dumps({'passed':True,'checks':len(results)}))
