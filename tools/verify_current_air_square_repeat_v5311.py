"""Entire original airborne Square Wave two-cycle semantic and fault gate.

Current metadata candidate and real Sub-Zero8 replace only old candidate,
Kitana4 and its ROM-defined floor anchor. All airborne contact, exact damage,
physical inputs, own actors, recovery, descriptor/FIFO and real faults remain.
"""
import inspect,json
from pathlib import Path
import verify_square_air_repeat_v5123 as original
import verify_current_projectile_repeat_v5295 as floor_context
import current_payload_metadata_context_v5229 as current
ROOT,need,sha=current.ROOT,current.need,current.sha
OUT=ROOT/'audit_v5312_current_air_square_subzero_repeat_checked'
def replace_once(text,before,after):
    need(text.count(before)==1,'Exact sole source substitution: '+before)
    return text.replace(before,after,1)
def bindings():
    check=inspect.getsource(original.check)
    check=replace_once(check,'ids={side:identity,3-side:4}','ids={side:identity,3-side:8}')
    check=replace_once(check,'floors[3-side]==83','floors[3-side]==subzero_floor(guest)')
    scope=dict(original.check.__globals__,native=current,subzero_floor=floor_context.subzero_floor)
    exec(compile(check,__file__+'::entire_original_air_contact_SubZero','exec'),scope)
    scoped_check=scope['check']
    load=inspect.getsource(original.load)
    for before,after in (
      ('audit_v5118_square_air_repeat_{move}_p{side}_kitana','audit_v5307_current_air_square_shadow_{move}_p{side}_sub_zero'),
      ('audit_v5119_square_air_repeat_{move}_p{side}_kitana_observed','audit_v5308_current_air_square_shadow_{move}_p{side}_sub_zero_observed')):
        load=replace_once(load,before,after)
    scope=dict(original.load.__globals__)
    exec(compile(load,__file__+'::entire_original_actual_capture_load','exec'),scope)
    scoped_load=scope['load']
    main=inspect.getsource(original.main)
    main=replace_once(main,"air_index,'y','83')","air_index,'y',str(subzero_floor(guest)))")
    main=replace_once(main,'airborneSquareBothPlayerSlotsRepeatTwiceAndRecoverVerified=True',
      'airborneSquareBothPlayerSlotsRepeatTwiceAndRecoverVerified=True,currentTrueSubZeroBothRolesVerified=True')
    # The old physical gate's exact finite publication view is separate from
    # the full every-ready-field body/shadow gate; do not drop records there.
    def finite_load(move,side):
        b=scoped_load(move,side)
        frames={s['frame']for s in b['report']['actualScenes']}
        entry=original.SPECS[move][1]
        entries={original.num(t,'frame')for t in b['rows']['MK2_HSPECIAL_EVENT']if original.num(t,'entry')==entry}
        for tag in ('MK2_HPHASE_CANDIDATE','MK2_HPHASE_QUEUE'):
            b['rows'][tag]=[t for t in b['rows'][tag]if original.num(t,'frame')in frames-entries]
        return b
    scope=dict(original.main.__globals__,__file__=__file__,OUT=OUT,native=current,
      subzero_floor=floor_context.subzero_floor,check=scoped_check,load=finite_load)
    exec(compile(main,__file__+'::entire_original_semantics_and_26_real_faults_current','exec'),scope)
    return scoped_check,scoped_load,scope['main']
def main():
    baseline=ROOT/'audit_v5124_special_repeat_checked/report.json';old=json.loads(baseline.read_text())
    need(old['passed']and old['airborneSquareBothPlayerSlotsRepeatTwiceAndRecoverVerified']and
      sha(original.__file__)==old['inputHashes'][str(Path(original.__file__).resolve())],
      'Entire original actually accepted airborne physical semantic source unchanged')
    for side in (1,2):
        path=ROOT/f'audit_v5308_current_air_square_shadow_square_p{side}_sub_zero_observed/report.json'
        need(path.exists(),'Await actual native terminal; timeout/pending is never accepted')
        result=json.loads(path.read_text())
        need(result['passed']and result['nativeExit']==0 and result['nativeStderrEmpty']and
          result['trueVictimID']==8 and all(sha(p)==h for p,h in result['inputHashes'].items()),
          'Actual successful native current-candidate air contact capture inputs unchanged')
    _,_,verify=bindings();verify()
if __name__=='__main__':main()
