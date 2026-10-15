"""Full original two-cycle semantic/fault gate for both current Sonya/Sub-Zero roles.

Only true native victim ID and explicit additional scope/capture paths change.
All physical commands, health/ownership/geometry/descriptor/FIFO/recovery and
13 real actual-field faults per case are kept. Original Kitana matrix remains
accepted separately. Not full pixels/shadows/audio/KO/CPU/all-port acceptance.
"""
import inspect,json,traceback
from pathlib import Path
import verify_special_repeat_v5115 as original
import run_current_repeated_specials_v5288 as host
import current_payload_metadata_context_v5229 as current
ROOT,need,sha=current.ROOT,current.need,current.sha
OUT=ROOT/'audit_v5292_current_sonya_ring_subzero_repeat_checked'
def bindings():
    check=inspect.getsource(original.check)
    before='ids={side:identity,3-side:4}'
    need(check.count(before)==1,'Only actual new native Sub-Zero ID admission')
    check=check.replace(before,'ids={side:identity,3-side:8}',1)
    scope=dict(original.check.__globals__,native=current)
    exec(compile(check,__file__+'::entire_original_two_cycle_semantics_SubZero','exec'),scope)
    scoped_check=scope['check']
    load=inspect.getsource(original.load)
    for before,after in [
      ('audit_v5102_special_repeat_{move}_p{side}_kitana','audit_v5289_current_special_repeat_{move}_p{side}_sub_zero'),
      ('audit_v5103_special_repeat_{move}_p{side}_kitana_observed','audit_v5290_current_special_repeat_{move}_p{side}_sub_zero_observed')]:
        need(load.count(before)==1,'Only fresh actual native capture/report paths')
        load=load.replace(before,after,1)
    loadscope=dict(original.load.__globals__)
    exec(compile(load,__file__+'::entire_original_two_cycle_actual_capture_load','exec'),loadscope)
    main=inspect.getsource(original.main)
    for before,after in [
      ('for move in SPECS:',"for move in ('ring',):"),
      ('actualVerifiedSpecialCycles=32','actualVerifiedSpecialCycles=4'),
      ('allEightMovesBothPlayerSlotsRepeatTwiceAndRecoverVerified=True',
       'allEightMovesBothPlayerSlotsRepeatTwiceAndRecoverVerified=False,currentSonyaRingBothSlotsAgainstSubZeroRepeatTwiceAndRecoverVerified=True'),
      ('stationarySquareWhiffsExplicit=True','stationarySquareWhiffsExplicit=False')]:
        need(main.count(before)==1,'Exact additional tested scope; every original semantic/fault gate retained '+before)
        main=main.replace(before,after,1)
    mainscope=dict(original.main.__globals__,__file__=__file__,OUT=OUT,native=current,check=scoped_check,
      load=loadscope['load'])
    exec(compile(main,__file__+'::entire_original_semantics_and_26_actual_faults_new_scope','exec'),mainscope)
    return scoped_check,loadscope['load'],mainscope['main']
def main():
    baseline=ROOT/'audit_v5116_special_repeat_checked/report.json';old=json.loads(baseline.read_text())
    for module in (original,host.original):
        p=str(Path(module.__file__).resolve())
        need(sha(p)==old['inputHashes'][p],'Exact full accepted original capture/checker source')
    for side in (1,2):
        path=ROOT/f'audit_v5290_current_special_repeat_ring_p{side}_sub_zero_observed/report.json'
        need(path.exists(),'Await actual native terminal; pending is not failure/timeout restart')
        result=json.loads(path.read_text())
        need(result['passed']and result['victim']=='sub_zero'and result['nativeStderrEmpty']and
          all(sha(p)==h for p,h in result['inputHashes'].items()),
          'Exact current true victim/no-warning runtime inputs')
    _,_,verify=bindings();verify()
if __name__=='__main__':main()
