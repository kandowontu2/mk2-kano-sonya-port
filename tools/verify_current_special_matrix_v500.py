"""Current 52-case human matrix, six original references, explicit wider counterexamples."""
import json
import re
from pathlib import Path
import verify_native_candidate_v500 as build
import verify_human_special_matrix as positive
import verify_human_special_negative_v3 as negative
import verify_original_ball_v1 as original
from verify_ko_round_floor_shadows import need,digest,rgb

ROOT=build.ROOT
def source_delta(inputs):
    old=ROOT/'diagnostic_v471_owned_palette_floor_shadow/input_sources/midtunit_m.cpp'
    new=ROOT/'mame-mkp/src/mame/midway/midtunit_m.cpp'
    need(digest(old)=='1F9E368A0763D63DF928D04E8A0CAE3B78A79DEC911FDB85308A92A99D0B1C97',
         'Exact original gameplay source retained')
    need(digest(new)=='6EA98224EB2D4B6AECF04A8303E2C465A7512052FBE28613CC985E2714D3B9EF',
         'Exact new gameplay source')
    before=old.read_text();after=new.read_text()
    need(after.count('mk2_ground_contact_extension')==4,'Ground translation has only declared uses')
    normalized=after.replace('constexpr unsigned mk2_ground_contact_extension = 5;','')
    for a,b in [('139 - mk2_ground_contact_extension','134'),('140 - mk2_ground_contact_extension','135'),
                ('14 - mk2_ground_contact_extension','14')]:normalized=normalized.replace(a,b)
    def code(s):return re.sub(r'\s+','',re.sub(r'/\*.*?\*/|//[^\n]*','',s,flags=re.S))
    need(code(before)==code(normalized),'Only cannonball Y-plane emitted value changes; floor values remain 134/135')
    oldbuild=json.loads((ROOT/'diagnostic_v471_owned_palette_floor_shadow/build-info.json').read_text(encoding='utf-8-sig'))
    newbuild=json.loads((ROOT/build.NAME/'build-info.json').read_text(encoding='utf-8-sig'))
    need(oldbuild['payload_sha256']==newbuild['payload_sha256']==build.PAYLOAD,
         'Same payload bytes despite different matched-build directories')
    for path,sha in oldbuild['input_hashes'].items():
        if path==str(new):continue
        if Path(path).name=='mk2ks.mdata':
            need(sha==build.PAYLOAD and digest(Path(path))==sha,'Exact older payload source')
            inputs[path]=sha
            continue
        need(newbuild['input_hashes'].get(path)==sha,'Other original build input changed: '+path)
    inputs[str(old)]=digest(old);inputs[str(new)]=digest(new)
    inputs[str(ROOT/'diagnostic_v471_owned_palette_floor_shadow/build-info.json')]=digest(ROOT/'diagnostic_v471_owned_palette_floor_shadow/build-info.json')

def verify():
    inputs={};source_delta(inputs)
    negative_report=negative.verify();inputs.update(negative_report['inputHashes'])
    cases=[]
    for move in positive.SPECS:
        for side in(1,2):
            for air in((False,True)if move=='square'else(False,)):
                folder=ROOT/f'audit_v504_positive_{move}{"_air"if air else""}_p{side}'
                build.matched(folder,inputs)
                r=json.loads((folder/'result.json').read_text(encoding='utf-8-sig'))
                need((r['move'],r['side'],r['air'])==(move,side,air),'Exact positive command launch')
                cases.append(positive.verify_log((folder/'run.log').read_text(encoding='utf-8-sig'),move,side,air))
                for name in('special_before.png','special_recovered.png','special_final.png'):
                    file=folder/'snap'/name;need(rgb(file).shape==(254,400,3),'Native screenshot dimensions')
                    inputs[str(file)]=digest(file)
    refs=original.verify(inputs)
    wider=[]
    # This remains diagnostic, never green evidence for universal duck immunity.
    # Same passive native duck input, complete exact identities and health writes.
    for victim in negative.VICTIMS:
        for side in(1,2):
            folder=ROOT/f'audit_v506_cannonball_duck_p{side}_{victim}'
            build.matched(folder,inputs)
            log=(folder/'run.log').read_text(encoding='utf-8-sig')
            need(not re.search(r'Lua error|LUA ERROR|Fatal error|access violation',log,re.I), 'Wider runtime error')
            results=negative.rows(log,'RESULT');need(len(results)==1 and not negative.rows(log,'FAILED'),'Complete wider observation')
            r=results[0];fields=negative.rows(log,'FIELD');by={(f['frame'],f['slot']):f for f in fields}
            need(len(fields)==len(by)==(r['frame']-r['ready']+1)*2,'Complete wider paired field inventory')
            for field in fields:
                need(field['id']==field['roster']==(17 if field['slot']==side else negative.VICTIMS[victim]) and
                     field['owner']==field['actor'] and field['state']==1 and field['mode']==2 and field['writes']==0,
                     'Actual wider human pair and selected identity')
            health=[h for h in negative.rows(log,'HEALTH')if r['entry']<=h['frame']<=r['recovered']]
            for h in health:
                need(h['slot']==3-side and h['pc']==0xff836700 and h['mask']==0xffff and
                     h['before']==161 and h['after']==137 and by[h['frame'],3-side]['action']==0x302,
                     'Actual 24-damage collision against native duck')
            detail=None
            status='duck_contact_needs_fidelity_review'
            if not health:
                try:
                    negative.verify_log(log,'ball',side,'miss',victim)
                    status='verified_duck_miss'
                except ValueError as error:
                    # Explicit counterexample, NOT a relaxed passing contract.
                    status='duck_miss_kinematics_unproven';detail=str(error)
            wider.append(dict(victim=victim,side=side,damage=sum(h['before']-h['after']for h in health),
                              status=status,detail=detail))
    phases=original.verify_phases(inputs)
    for name in('tools/verify_current_special_matrix_v500.py','tools/verify_human_special_matrix.py',
                'tools/verify_original_ball_v1.py','tools/test_current_special_matrix_v500.py'):
        file=ROOT/name;inputs[str(file)]=digest(file)
    return dict(passed=False,boundedMatrixPassed=True,fullPortAcceptance=False,candidate=build.NAME,
                scope='52 bounded current human cases versus Sub-Zero plus six complete original MK3 references. '
                      '28 wider duck observations explicitly report contacts needing fidelity review; not universal acceptance. '
                      'No full current CPU/UI/tower/continue/boss/finisher/ending/audio or release acceptance.',
                positiveCases=cases,negativeCases=negative_report['cases'],originalCases=refs,
                originalDuckPhaseCases=phases,widerDuckObservations=wider,
                pairedFields=sum(c['fields']for c in cases+negative_report['cases']),
                inputHashes=inputs)

if __name__=='__main__':print(json.dumps(verify(),indent=2))
