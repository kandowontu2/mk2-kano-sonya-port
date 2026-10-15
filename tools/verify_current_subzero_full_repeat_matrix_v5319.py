"""Full original physical repeat/fault matrix, true Sub-Zero8 in both roles.

All eight Kano/Sonya specials repeat twice and recover in this actual Prison
matrix. Original stationary Square Wave whiffs remain distinguished from
separately proven airborne contacts. Full every-ready-field body/shadows are
verified separately; no other arena, CPU, KO, overlap or audio acceptance.
"""
import inspect,json
from pathlib import Path
import verify_special_repeat_v5115 as original
import verify_current_projectile_repeat_v5295 as context
import current_payload_metadata_context_v5229 as current
ROOT,need,sha=current.ROOT,current.need,current.sha
OUT=ROOT/'audit_v5320_current_subzero_full_repeat_matrix_checked'
def replace_once(text,before,after):
    need(text.count(before)==1,'Exact sole source substitution: '+before)
    return text.replace(before,after,1)
def bindings():
    check,_,_=context.bindings()
    source=inspect.getsource(original.load)
    for before,after in (
      ('audit_v5102_special_repeat_{move}_p{side}_kitana','audit_v5300_current_special_shadow_{move}_p{side}_sub_zero'),
      ('audit_v5103_special_repeat_{move}_p{side}_kitana_observed','audit_v5301_current_special_shadow_{move}_p{side}_sub_zero_observed')):
        source=replace_once(source,before,after)
    scope=dict(original.load.__globals__)
    exec(compile(source,__file__+'::entire_original_actual_capture_load','exec'),scope)
    full_load=scope['load']
    def finite_load(move,side):
        b=full_load(move,side)
        frames={s['frame']for s in b['report']['actualScenes']}
        entry=original.SPECS[move][1]
        entries={original.num(t,'frame')for t in b['rows']['MK2_HSPECIAL_EVENT']if original.num(t,'entry')==entry}
        for tag in ('MK2_HPHASE_CANDIDATE','MK2_HPHASE_QUEUE'):
            b['rows'][tag]=[t for t in b['rows'][tag]if original.num(t,'frame')in frames-entries]
        return b
    source=replace_once(inspect.getsource(original.main),
      'allEightMovesBothPlayerSlotsRepeatTwiceAndRecoverVerified=True',
      'allEightMovesBothPlayerSlotsRepeatTwiceAndRecoverVerified=True,currentTrueSubZeroNativeVictimBothRolesAllEightMovesVerified=True')
    scope=dict(original.main.__globals__,__file__=__file__,__doc__=__doc__,OUT=OUT,
      native=current,check=check,load=finite_load)
    exec(compile(source,__file__+'::entire_original_all8moves_bothroles_and194real_faults','exec'),scope)
    return scope['main']
def main():
    baseline=ROOT/'audit_v5116_special_repeat_checked/report.json';old=json.loads(baseline.read_text())
    need(old['passed']and old['allEightMovesBothPlayerSlotsRepeatTwiceAndRecoverVerified']and
      sha(original.__file__)==old['inputHashes'][str(Path(original.__file__).resolve())],
      'Entire original actually passed physical semantics and fault matrix source unchanged')
    for move in original.SPECS:
        for side in (1,2):
            path=ROOT/f'audit_v5301_current_special_shadow_{move}_p{side}_sub_zero_observed/report.json'
            need(path.exists(),'Await actual native terminal; never restart on observation timeout')
            result=json.loads(path.read_text())
            need(result['passed']and result['nativeExit']==0 and result['victim']=='sub_zero'and
              result['nativeStderrEmpty']and all(sha(p)==h for p,h in result['inputHashes'].items()),
              'Every actual current physical native role/capture source unchanged')
    bindings()()
if __name__=='__main__':main()
