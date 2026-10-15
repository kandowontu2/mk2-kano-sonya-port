"""Entire original every-field body/shadow gate in current Sub-Zero cases.

Only current metadata context, real native victim8, and fresh evidence paths
change. Every original pose/ownership/projection/stream/DMA/entry/fault gate
is preserved. Physical controls and observed game data are never changed.
"""
import inspect,json,types
from pathlib import Path
import verify_square_air_shadow_v5147 as original
import verify_current_air_square_repeat_v5311 as physical
import current_payload_metadata_context_v5229 as current
ROOT,need,sha=current.ROOT,current.need,current.sha
def replace_once(text,before,after):
    need(text.count(before)==1,'Exact sole source substitution: '+before)
    return text.replace(before,after,1)
def bindings():
    actual_check,_,_=physical.bindings()
    human=types.SimpleNamespace(**dict(vars(original.human),check=actual_check))
    load=inspect.getsource(original.load)
    for before,after in (
      ('audit_v5144_special_repeat_{move}_p{side}_kitana','audit_v5307_current_air_square_shadow_{move}_p{side}_sub_zero'),
      ('audit_v5145_special_repeat_{move}_p{side}_kitana_observed','audit_v5308_current_air_square_shadow_{move}_p{side}_sub_zero_observed')):
        load=replace_once(load,before,after)
    scope=dict(original.load.__globals__)
    exec(compile(load,__file__+'::entire_original_actual_capture_load','exec'),scope)
    scoped_load=scope['load']
    check=replace_once(inspect.getsource(original.check),'ids={side:identity,3-side:4}',
      'ids={side:identity,3-side:8}')
    scope=dict(original.check.__globals__,human=human)
    exec(compile(check,__file__+'::entire_original_body_and_shadow_SubZero','exec'),scope)
    scoped_check=scope['check']
    main=replace_once(inspect.getsource(original.main),
      'audit_v5148_special_shadow_{args.move}_p{args.side}_checked',
      'audit_v5314_current_air_square_shadow_{args.move}_p{args.side}_sub_zero_checked')
    # Reconstruct exclusively from the unchanged independently hashed compiled
    # ROM lane inventory, never from observed sprite/shadow comparison targets.
    def reconstruct(pins):
        for p in (Path(__file__),Path(original.__file__),Path(physical.__file__),
          Path(current.__file__),ROOT/'audit_v5312_current_air_square_subzero_repeat_checked/report.json',
          ROOT/'audit_v5148_special_shadow_square_p1_checked/report.json',
          ROOT/'audit_v5124_special_repeat_checked/report.json',Path(original.human.__file__)):
            pins[str(p.resolve())]=sha(p)
        old=ROOT/'diagnostic_v4992_native_subzero_legs';new=ROOT/current.NAME
        rel='input_sources/mame-mkp/src/mame/midway/midtunit.cpp'
        oldtext=(old/rel).read_text();newtext=(new/rel).read_text()
        def graphics(t):
            return t.split('ROM_START( mk2ks )',1)[1].split('ROM_END',1)[0].split(
              'ROM_REGION( 0x2000000, "gfxrom", ROMREGION_ERASE00 )',1)[1]
        need(graphics(oldtext)==graphics(newtext),'Entire actual compiled graphics lane declaration unchanged')
        pins[str((new/rel).resolve())]=sha(new/rel)
        return original.reconstruct(pins)
    scope=dict(original.main.__globals__,__file__=__file__,native=current,human=human,
      load=scoped_load,check=scoped_check,reconstruct=reconstruct)
    exec(compile(main,__file__+'::entire_original_native_shadow_gate_and_11_real_faults','exec'),scope)
    return scope['main']
def main():
    baseline=json.loads((ROOT/'audit_v5148_special_shadow_square_p1_checked/report.json').read_text())
    need(baseline['passed']and baseline['case']['entryBodyPublicationProven']and
      all(sha(p)==baseline['inputHashes'][str(p.resolve())]for p in (
        Path(original.__file__),ROOT/'tools/verify_move_phase_shadow_v5089.py')),
      'Full original accepted body/shadow/physical semantic sources unchanged')
    stockphysical=ROOT/'audit_v5124_special_repeat_checked/report.json'
    qualified=json.loads(stockphysical.read_text())
    need(qualified['passed']and sha(original.human.__file__)==qualified['inputHashes'][str(Path(original.human.__file__).resolve())],
      'Entire original actually qualified airborne-contact physical source unchanged')
    prior=json.loads((ROOT/'audit_v5312_current_air_square_subzero_repeat_checked/report.json').read_text())
    need(prior['passed']and prior['currentTrueSubZeroBothRolesVerified']and
      all(sha(p)==h for p,h in prior['inputHashes'].items()),
      'Entire current true Sub-Zero role/floor/physical/recovery and actual-fault matrix accepted')
    bindings()()
if __name__=='__main__':main()
