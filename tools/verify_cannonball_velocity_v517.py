"""Nine targeted passing current cases, one retained crouch counterexample. Not full acceptance."""
import json
import re
import verify_native_candidate_v517 as build
import verify_human_special_matrix as positive
import verify_human_special_negative_v4 as negative
from verify_ko_round_floor_shadows import need,digest,rgb

ROOT=build.ROOT
def source_delta(inputs):
    old=ROOT/'diagnostic_v500_native_cannonball_plane/input_sources/midtunit_m.cpp'
    new=ROOT/'mame-mkp/src/mame/midway/midtunit_m.cpp'
    need(digest(old)=='6EA98224EB2D4B6AECF04A8303E2C465A7512052FBE28613CC985E2714D3B9EF','Frozen v500 source')
    need(digest(new)=='B8542F4777E4F100EC4E86771AD70EC867522FE106DD51E6F164E408489722D3','Exact current v517 source')
    def code(s):return re.sub(r'\s+','',re.sub(r'/\*.*?\*/|//[^\n]*','',s,flags=re.S))
    before,after=code(old.read_text()),code(new.read_text())
    for text in('ball_repel=0xffba0,','emit(ball_repel,{0x09c0,3,0x0580,0x19d0,0x0106,0x0960});',
                'ball_movi(0,4);ball_code({0x0580,0x19d0,0x0106});',
                'ball_movi(0,3);ball_code({0x0580,0x19d0,0x0106});',
                'ball_call(0xff876be0);ball_code({0xb208,0x0040});ball_movi(0,13);',
                'ball_movi(6,native_address(ball_repel));'):
        need(after.count(text)==1,'One bounded cannonball-only emitted change');after=after.replace(text,'')
    after=after.replace('ball_cooperate(0xff876660);','ball_cooperate(0xff876650);')
    need(before==after,'No changes outside native cannonball flight/rebound handoff')
    inputs[str(old)]=digest(old);inputs[str(new)]=digest(new)
    return dict(old='diagnostic_v500_native_cannonball_plane',current=build.NAME,
                unchanged='Floor values, attack descriptor, all other gameplay emission and rendering/payload/audio.')

def verify():
    inputs={};delta=source_delta(inputs);cases=[]
    for side in(1,2):
        folder=ROOT/f'audit_v518_positive_ball_p{side}'
        build.matched(folder,inputs);log=(folder/'run.log').read_text(encoding='utf-8-sig')
        case=positive.verify_log(log,'ball',side);case.update(negative.verify_rebound(log,side,False));cases.append(case)
        for name in('special_before.png','special_recovered.png','special_final.png'):
            file=folder/'snap'/name;need(rgb(file).shape==(254,400,3),'Native snapshots');inputs[str(file)]=digest(file)
        for victim,scenario in(('sub_zero','block'),('sub_zero','miss'),('kung_lao','miss'),('liu_kang','miss')):
            folder=ROOT/(f'audit_v518_negative_ball_{scenario}_p{side}_sub_zero'if victim=='sub_zero'
                         else f'audit_v518_cannonball_duck_p{side}_{victim}')
            build.matched(folder,inputs);log=(folder/'run.log').read_text(encoding='utf-8-sig')
            if victim=='liu_kang'and side==1:
                try:negative.verify_log(log,'ball',side,scenario,victim)
                except ValueError as error:
                    need(str(error)=='Own special contact damage (excludes initial ordinary charged kick)',
                         'Expected current crouch-contact counterexample, not an unrelated broken fixture')
                else:raise ValueError('Unresolved crouch fixture unexpectedly counted as a passing miss')
                r=negative.rows(log,'RESULT')[0]
                health=[h for h in negative.rows(log,'HEALTH')if r['entry']<=h['frame']<=r['recovered']]
                need(len(health)==1 and health[0]['before']-health[0]['after']==24 and health[0]['pc']==0xff836700,
                     'Actual retained current crouch contact')
                continue
            case=negative.verify_log(log,'ball',side,scenario,victim);negative.verify_repel(log,side)
            if scenario=='block':case.update(negative.verify_rebound(log,side,True))
            case['victim']=victim;cases.append(case)
            for name in('special_before.png','special_recovered.png','special_final.png'):
                file=folder/'snap'/name;need(rgb(file).shape==(254,400,3),'Native snapshots');inputs[str(file)]=digest(file)
    for name in('tools/verify_cannonball_velocity_v517.py','tools/verify_human_special_negative_v4.py',
                'tools/verify_native_candidate_v517.py','tools/verify_human_special_matrix.py',
                'tools/verify_ko_round_floor_shadows.py','tools/inspect_ground_presentation.py',
                'tools/test_cannonball_velocity_v517.py'):
        file=ROOT/name;inputs[str(file)]=digest(file)
    return dict(passed=False,targetedCasesPassed=True,fullPortAcceptance=False,candidate=build.NAME,
                scope='Nine targeted current cases: hit/block recoil, full constant-speed Sub-Zero/Kung-Lao/Liu-P2 duck misses, '
                      'native short-counter expiry and ordinary recovery/follow-up. '
                      'Liu P1 still takes 24 while ducking; all-victim/current full-matrix/interruption/KO/CPU/UI/campaign/finishers/audio/release remain open.',
                sourceDelta=delta,cases=cases,knownCounterexample='audit_v518_cannonball_duck_p1_liu_kang',
                pairedFields=sum(c['fields']for c in cases),inputHashes=inputs)

if __name__=='__main__':print(json.dumps(verify(),indent=2))
