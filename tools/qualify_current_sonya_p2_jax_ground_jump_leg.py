"""Retain strict chronology; additionally verify actual owned ground/jump callbacks."""
from pathlib import Path
code=Path(__file__).with_name('qualify_current_sonya_p2_jax_ring_spacing.py').read_text()
changes={
    'audit_current_sonya_p2_jax_ring_spacing':'audit_current_sonya_p2_jax_ground_jump_leg',
    'SONYA_JAX_RING_PLAN':'SONYA_JAX_SHORT_LEG_PLAN',
    'SONYA_JAX_JUMP_PLAN':'SONYA_JAX_POUND_JUMP_PLAN',
    "r['move']=='ring'":"r['move']=='leg'",
    "r['entry']=='FFFFB400' and r['pc']=='FFFFB420'":"r['entry']=='FFF80800' and r['pc']=='FFF80830'",
    'ringPlans':'legPlans',
    'ownedNativeRingEntries':'ownedNativeLegEntries',
    'One stage8 Jax11 physical ring/backjump successor':'One stage8 Jax11 physical ground-pound-jump/short-leg successor',
}
for old,new in changes.items():
    assert old in code,old
    code=code.replace(old,new)
code=code.replace("t!='SONYA_JAX_DAMAGE'", "t not in ('SONYA_JAX_DAMAGE','JAX_GROUND_NATIVE','JAX_GROUND_CODE_CHECKED')")
helper='''
def ground_gate(rows):
    native=[r for t,r in rows if t=='JAX_GROUND_NATIVE']
    addresses={'ground_entry':('FF86DD90','09C1'),'ground_result':('FF86E020','C80F'),
               'ground_damage':('FF86E070','09C0'),'human_jump':('FF831360','09C1')}
    # Jump opcode is separately loaded from original stock ROM, not guessed.
    stock=(sync.ROOT/'mk2/mk2-maincpu.bin').read_bytes()
    for r in native:
        entry,unused=addresses[r['kind']]
        expected=int.from_bytes(stock[(int(entry,16)-0xff800000)//8:(int(entry,16)-0xff800000)//8+2],'little')
        assert r['entry']==entry and int(r['at'],16)==int(entry,16) and int(r['pc'],16)==int(entry,16)+16
        assert int(r['opcode'],16)==expected
        assert r['h_id']=='18' and r['c_id']=='11' and r['h_actor']==r['h_owner'] and r['c_actor']==r['c_owner']
        role='h' if r['kind']=='human_jump' else 'c'
        assert r['a8']==r[role+'_actor'] and r['a13']==r[role+'_main']
        if r['kind']=='ground_result':
            not_grounded=int(r['h_vy'],16)!=0 or r['h_y']!=r['h_floor']
            assert int(r['carry'])==int(not_grounded)
    loaded=[r for t,r in rows if t=='JAX_GROUND_CODE_CHECKED']
    old=sync.ROOT/'tools/inspect_jax_137_ground_damage_source_v4805.py'
    tree=ast.parse(old.read_text())
    checks=ast.literal_eval(next(n.value for n in tree.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='CHECKS' for t in n.targets)))
    assert len(loaded)<=1
    if loaded:assert loaded[0]['current_loaded']=='true' and int(loaded[0]['original_words'])==sum(len(w) for w in checks.values())
    skips=[r for r in native if r['kind']=='ground_result' and r['carry']=='1']
    return dict(loadedOriginalSitesVerified=29 if loaded else 0,loadedOriginalWordsVerified=sum(len(w) for w in checks.values()) if loaded else 0,
                actualOwnedGroundEntries=sum(r['kind']=='ground_entry' for r in native),
                actualOwnedGroundResults=sum(r['kind']=='ground_result' for r in native),
                actualOwnedJumpEntries=sum(r['kind']=='human_jump' for r in native),
                actualNativeCarrySkips=len(skips),actualNativeDamagePathEntries=sum(r['kind']=='ground_damage' for r in native),
                sampleCarrySkips=skips[:8],nativeCallbackRecords=native,
                directCausalityScope='Actual ground-result Carry exactlymatches observed target VY/floor gate; Carry branches skip stock damage path. Does not classify every other HP event or prove all ground pounds evaded.')

'''
marker='def main():';assert code.count(marker)==1
code=code.replace(marker,helper+marker)
marker='report=dict(passed=True,';assert code.count(marker)==1
code=code.replace(marker,'''ground=ground_gate(rows)
    native=[r for t,r in rows if t=='JAX_GROUND_NATIVE']
    if native:
        for key,value in [('h_id','1'),('a13','00000000'),('opcode','0000')]:
            bad=copy.deepcopy(rows);next(r for t,r in bad if t=='JAX_GROUND_NATIVE')[key]=value
            try:ground_gate(bad)
            except AssertionError:faults.append(dict(kind='native ground/jump owner/code',key=key))
            else:raise AssertionError('Native callback mutation admitted')
        skip=next((r for r in native if r['kind']=='ground_result' and r['carry']=='1'),None)
        if skip:
            bad=copy.deepcopy(rows);next(r for t,r in bad if t=='JAX_GROUND_NATIVE' and r['frame']==skip['frame'] and r['kind']=='ground_result')['carry']='0'
            try:ground_gate(bad)
            except AssertionError:faults.append(dict(kind='lost actual Carry skip'))
            else:raise AssertionError('Lost Carry skip admitted')
    report=dict(passed=True,nativeGroundJumpProof=ground,''')
code=code.replace("'lastLoggedField','terminal')", "'lastLoggedField','terminal','nativeGroundJumpProof')")
# Avoid printing complete scalar callback ledger in the concise shell receipt.
code=code.replace("print(json.dumps({k:report[k]", "report_for_receipt=dict(report);report_for_receipt['nativeGroundJumpProof']={k:v for k,v in ground.items() if k not in ('nativeCallbackRecords','sampleCarrySkips')}\n    print(json.dumps({k:report_for_receipt[k]")
exec(compile(code,__file__,'exec'))
