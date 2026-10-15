"""True first-live round-boundary Bicycle, no invented pre-entry live callback."""
import inspect,json,struct,sys,traceback
from pathlib import Path
import native_cpu_human_hold_capture_contract_v3111 as capture
import native_cpu_bicycle_round_boundary_contract_v3127 as phase
import native_cpu_bicycle_miss_contract_v3064 as old_phase
import verify_native_cpu_mobility_inventory_v3038 as choices
ROOT=capture.ROOT;OUT=ROOT/'audit_v3129_native_cpu_bicycle_round_boundary_checked';need=capture.need
def source():
    actual=inspect.getsource(phase.verify);original=inspect.getsource(old_phase.verify)
    before="    assert set(range(start,end+2))<=set(by)\n    baseline=by[start]\n    for at in range(start,end+2):"
    a=actual.index("    assert start not in by");b=actual.index("        r=by[at]",a)
    expected=original.replace(before,actual[a:b].rstrip()).replace(
      "flags=[r for r in state.original.flag_rows(log)if r['slot']==2 and start<=r['frame']<=end]",
      "flags=[r for r in native.rows(log,'MK2_MOBILITY_FLAG')if r['slot']==2 and start<=r['frame']<=end]")
    need(actual.rstrip()==expected.rstrip(),'Entire original Bicycle startup/seek/physics/ceiling/fall/landing/locks/HP retained; explicit source-bound boundary instead of imaginary prior live callback')
def verify():
    source();pins={}
    name='audit_v3110_native_cpu_human_hold_kano_guard_until_close_neutral_hold'
    log,guest,case=capture.capture(ROOT/name,'new','kano','guard_until_close','neutral_hold',pins)
    native=choices.native_choices(log,guest,'kano');need(len(native)==1 and native[0]['move']=='bicycle'and not native[0]['nativeContact'],'Actual one natural Bicycle miss')
    typed=phase.verify(log,guest);start,end=typed['start'],typed['ready']
    snapshots=capture.rows(log,'MK2_MOBILITY_ENTRY_STATE');flags=capture.rows(log,'MK2_MOBILITY_FLAG')
    by={r['frame']:r for r in capture.ledgers.pair.rows(log,'FIELD')}
    for snapshot in snapshots:
        side=snapshot['slot'];prefix=''if side==2 else 'v'
        for kind in('action','body','flags'):
            value=snapshot[kind]
            for row in flags:
                if row['frame']!=start or row['slot']!=side or row['kind']!=kind:continue
                need(row['before']==value and row['mask']==65535 and row['writes']==0 and row['assistance']=='none'and
                  (row['actor'],row['main'],row['owner'])==(snapshot['actor'],snapshot['main'],snapshot['actor'])and
                  row['at']==(snapshot['actor']+0x160 if kind=='body'else snapshot['main']+(0x1f0 if kind=='action'else 0x210))and
                  struct.unpack_from('<2H',guest,(row['pc']-32-0xff800000)//8)==(row['op0'],row['op1']),
                  'Every actual initial lock store source-bound, owned and chained from entry state')
                value=row['after']
            need(value==by[start+1][prefix+kind],'Actual entry chain equals first real live callback')
    actual=[r for r in flags if start<=r['frame']<=end]
    global_rows=[r for r in capture.ledgers.pair.flag_rows(log)if start<=r['frame']<=end]
    keys=('frame','slot','kind','at','before','after','pc','a8','a13','actor','main','id','state','op0','op1')
    need(len(global_rows)==len(actual)+1 and [tuple(r[k]for k in keys)for r in global_rows[1:]]==[tuple(r[k]for k in keys)for r in actual],
      'Entire independently bound initial-through-regain writer stream, plus exactly one original pre-entry AI clear')
    previous=global_rows[0]
    need((previous['frame'],previous['slot'],previous['kind'],previous['before'],previous['after'],previous['pc'],previous['op0'],previous['op1'])==
      (start,2,'flags',0,0,0xff9b3b40,0xb08d,0x210),'Only preceding stock no-op clear, independently covered by full whole-state ledger')
    need(typed['start']==2663 and typed['ready']==2724 and typed['fields']==61 and typed['fractionalLandingY']==40960,'Full native61-field boundary miss and fractional landing')
    case.update(case=name,phase=typed,actualNativeChoice=native[0],initialEntryChainAccepted=True,roundRevealBoundaryAccepted=True)
    for module in tuple(sys.modules.values()):
        file=getattr(module,'__file__',None)
        if file and Path(file).resolve().is_relative_to(ROOT/'tools')and Path(file).suffix=='.py':pins[str(Path(file).resolve())]=capture.assembly.sha(file)
    for file,wanted in pins.items():need(capture.assembly.sha(file)==wanted,'Immutable actual round-boundary source/capture '+file)
    return dict(passed=True,cases={'new_kano':case},actualCandidateBicycleMissAccepted=True,
      originalNativeMissPhysicsAndIndividualRecoveryRetained=True,actualRoundRevealToLiveBoundaryAccepted=True,
      actualInitialEntrySourceWriteChainsAccepted=True,missingInteriorFieldsPermitted=False,
      candidateBicycleHitOrBlockedAccepted=False,gameChanged=False,fullPortAcceptance=False,inputHashes=pins,scope=__doc__)
if __name__=='__main__':
    need(not OUT.exists(),'Immutable actual Bicycle round-boundary proof')
    try:value=verify()
    except Exception as error:value=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
    OUT.mkdir();(OUT/'report.json').write_text(json.dumps(value,indent=2)+'\n')
    print(json.dumps({k:v for k,v in value.items()if k not in('cases','inputHashes','scope')},indent=2),flush=True)
    raise SystemExit(0 if value['passed']else 1)
