"""Counterexamples are in-memory only; never change actual runtime evidence."""
import json,re
from unittest.mock import patch
import verify_native_split_v1124 as verifier

OUT = verifier.ROOT/'audit_v1125_owned_split_corruption_checks'
if OUT.exists():
    raise ValueError('Preserve corruption evidence')
baseline = verifier.reconstruct()
texts = {case:(verifier.ROOT/case/'run.log').read_text(encoding='utf-8-sig') for case in verifier.CASES}
results = {}
with patch.object(verifier,'reconstruct',return_value=baseline):
    good = verifier.verify(texts,check_files=False)
    assert good['passed'],good['errors']
    results['baseline'] = {'passed':True,'cases':len(good['cases'])}
    case = verifier.CASES[0]
    for name,pattern,replace in (
        ('half_timing_one_field',r'(MK2_SPLIT_V1098_STATE[^\n]*age=)(\d+)( at=FF842630[^\n]*id=17)',lambda m:m[1]+str(int(m[2])+1)+m[3]),
        ('lost_native_x_mirror',r'(MK2_SPLIT_V1098_STATE[^\n]*at=FF842630[^\n]*id=17[^\n]* flags=)([0-9A-F]+)',lambda m:m[1]+f'{int(m[2],16)^16:04X}'),
        ('foreign_split_actor_id',r'(MK2_SPLIT_V1098_STATE[^\n]*at=FF8CF030[^\n]* other_id=)17',r'\g<1>1'),
        ('wrong_second_cursor',r'(MK2_SPLIT_V1098_STATE[^\n]*at=FF842690[^\n]*id=17[^\n]* a9=)([0-9A-F]+)',lambda m:m[1]+f'{int(m[2],16)+32:08X}'),
        ('wrong_actual_ground',r'(MK2_ROLLING_HEAD_V1003_DMA[^\n]*source=0FB00000[^\n]* y=)(\d+)',lambda m:m[1]+str(int(m[2])+1)),
        ('missing_actual_native_pose',r'^MK2_ROLLING_HEAD_V1003_POSE_SNAPSHOT[^\n]*source=0FB00000[^\n]*\n',''),
    ):
        mutated,count = re.subn(pattern,replace,texts[case],count=1,flags=re.M)
        assert count==1,name+' matched original counterexample'
        changed = {**texts,case:mutated}
        result = verifier.verify(changed,check_files=False)
        assert not result['passed'] and result['errors'],name+' must be rejected'
        results[name] = {'rejected':True,'errors':result['errors']}
    original_bytes = verifier.Path.read_bytes
    actual_open = verifier.previous.Image.open
    guest_path = verifier.ROOT/case/'guest_maincpu.bin'
    picture_path = verifier.Path(good['cases'][case]['pixelMatches'][0]['picture'])
    for name,target,kind in (('whole_guest_byte',guest_path,'guest'),('actual_png_bytes',picture_path,'png')):
        def corrupt(path,selected=target,typ=kind):
            data = original_bytes(path)
            if path!=selected:
                return data
            if typ=='png':
                import io
                image = actual_open(io.BytesIO(data)).convert('RGB')
                image.paste((0,0,0),(0,0,image.width,image.height))
                buffer = io.BytesIO();image.save(buffer,format='PNG')
                return buffer.getvalue()
            edited=bytearray(data);edited[-1]^=1
            return bytes(edited)
        # PIL opens a path directly, so an in-memory black PNG must also reach
        # the actual pixel comparator, not only the hash function.
        if kind=='png':
            def open_changed(path,*args,**kwargs):
                if isinstance(path,(str,verifier.Path)) and verifier.Path(path)==target:
                    import io
                    return actual_open(io.BytesIO(corrupt(target)),*args,**kwargs)
                return actual_open(path,*args,**kwargs)
            with patch.object(verifier.Path,'read_bytes',corrupt),patch.object(verifier.previous.Image,'open',open_changed):
                result=verifier.verify(texts,check_files=False)
        else:
            with patch.object(verifier.Path,'read_bytes',corrupt):
                result=verifier.verify(texts,check_files=False)
        assert not result['passed'] and result['errors'],name+' must be rejected'
        results[name]={'rejected':True,'errors':result['errors']}
source_path = verifier.ROOT/'mame-mkp/src/mame/midway/midtunit_m.cpp'
real_bytes = verifier.Path.read_bytes
def wrong_compiled_source(path):
    data=real_bytes(path)
    return data+b'\n// in-memory source corruption\n' if path==source_path else data
with patch.object(verifier.Path,'read_bytes',wrong_compiled_source):
    try:
        verifier.reconstruct()
    except AssertionError:
        results['compiled_source_changed']={'rejected':True,'stage':'exact whole source digest before asset reconstruction'}
    else:
        raise AssertionError('Changed compiled source must not pass reconstruction')
OUT.mkdir()
(OUT/'report.json').write_text(json.dumps(dict(passed=True,checks=results,inMemoryOnly=True,
    baselineReconstruction='independent v1124 reconstruction, cached unchanged only for repeated runtime counterexamples',
    runtimeEvidenceModified=False,scope='baseline and nine scoped corruption checks, not full port acceptance',
    fullPortAccepted=False),indent=2)+'\n')
print(json.dumps(dict(passed=True,checks=len(results),actualEvidenceModified=False)))
