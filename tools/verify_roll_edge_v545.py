"""One-pixel native-plane fit, not all crouch phases/roster or full integration."""
import re
import struct
import verify_native_candidate_v545 as build
import verify_human_special_matrix as positive
import verify_human_special_negative_v5 as negative
from verify_ko_round_floor_shadows import need,digest

ROOT=build.ROOT
SOURCE='217D08ED8CB6F4D03D1A6F24C3E43555204B9FA7B52B63C43FE8E5421157ED35'

def source_delta(inputs):
    old=ROOT/'audit_v519_cannonball_velocity_checked_inputs/input_sources/midtunit_m_v517.cpp'
    new=ROOT/'mame-mkp/src/mame/midway/midtunit_m.cpp'
    need(digest(old)=='B8542F4777E4F100EC4E86771AD70EC867522FE106DD51E6F164E408489722D3' and digest(new)==SOURCE,'Exact before/after gameplay sources')
    code=lambda s:re.sub(r'\s+','',re.sub(r'/\*.*?\*/|//[^\n]*','',s,flags=re.S))
    before,after=code(old.read_text()),code(new.read_text())
    original='emit(ball_attack,{57,14-mk2_ground_contact_extension,72,31,0x1417,0x1805,0,0,1});'
    current='emit(ball_attack,{57,14-mk2_ground_contact_extension-1,72,31,0x1417,0x1805,0,0,1});'
    need(before.count(original)==after.count(current)==1 and after.replace(current,original)==before,'Only one attack-plane operand changed; no identity, input, state or duck bypass')
    # CMPXY equality must be evaluated from native instructions, not fitted
    # to absence of damage in one fixture. All four edge comparisons are strict.
    program=ROOT/'mk2/mk2-maincpu.bin';data=program.read_bytes()
    need(digest(program)=='45B3285496DB555EFAF4A3608A4F59845DD47A82E4A0593607E0592F47B36F23','Exact original collision instructions')
    words=struct.unpack_from('<6H',data,(0xff835b70-0xff800000)//8)
    need(words==(0xe4a2,0xc92e,0xcd2d,0xe483,0xc42b,0xc22a),'Original CMPXY/JRNC/JRNV/CMPXY/JRLT/JRLS rejection sequence')
    for p in (old,new,program):inputs[str(p)]=digest(p)
    return dict(operandBefore=9,operandAfter=8,hitboxSize=[72,31],physicsRenderingIdentityDamageUnchanged=True)

def verify_targets(inputs):
    cases=[]
    for side in (1,2):
        for kind in ('positive','block'):
            folder=ROOT/(f'audit_v548_positive_ball_p{side}' if kind=='positive' else f'audit_v548_negative_ball_block_p{side}_sub_zero')
            build.matched(folder,inputs);log=(folder/'run.log').read_text(encoding='utf-8-sig')
            case=positive.verify_log(log,'ball',side) if kind=='positive' else negative.verify_log(log,'ball',side,'block')
            case.update(negative.verify_rebound(log,side,kind=='block'));case['capture']=folder.name;cases.append(case)
        for victim in negative.VICTIMS:
            folder=ROOT/(f'audit_v546_cannonball_duck_p{side}_{victim}' if victim=='liu_kang' else f'audit_v547_cannonball_duck_p{side}_{victim}')
            build.matched(folder,inputs);log=(folder/'run.log').read_text(encoding='utf-8-sig')
            try:
                case=negative.verify_log(log,'ball',side,'miss',victim);negative.verify_repel(log,side);case['verifiedMiss']=True
            except ValueError as error:
                # Retain native contacts as unresolved roster findings. This
                # does not turn them into accepted duck-miss cases.
                need(str(error)=='Own special contact damage (excludes initial ordinary charged kick)','No hidden failure besides declared contact')
                result=negative.rows(log,'RESULT')[0]
                hits=[h for h in negative.rows(log,'HEALTH') if result['entry']<=h['frame']<=result['recovered']]
                need(len(hits)==1 and hits[0]['before']-hits[0]['after']==24 and hits[0]['pc']==0xff836700,'Actual unresolved native roster contact')
                case=dict(side=side,nativeContactDamage=24,verifiedMiss=False,accepted=False)
            case.update(victim=victim,capture=folder.name);cases.append(case)
    misses=[c for c in cases if c.get('verifiedMiss')]
    contacts=[c for c in cases if c.get('verifiedMiss') is False]
    need(len(misses)==23 and len(contacts)==5 and all(any(c.get('victim')=='liu_kang' and c.get('side')==s for c in misses) for s in (1,2)),'Observed bounded inventory, not all-roster miss acceptance')
    return dict(targetedCorrectionVerified=True,fullPortAcceptance=False,passingDuckMisses=len(misses),unresolvedDuckContacts=contacts,cases=cases)
