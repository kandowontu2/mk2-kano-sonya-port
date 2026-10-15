"""Complete actual Square-miss phases on a candidate mirror and native control.

True initial two-slot snapshots and actual instruction-bound lock/HP stores fill
the startup observer gap without fabricating a FIELD. All original Square rise,
flight, drop, landing and individual ready checks retained. Candidate mirror's
seven clean callbacks precede its actual next Leg Grab, not a 31-field idle pass.
"""
import inspect,json,sys,traceback
from pathlib import Path
import verify_native_cpu_square_inventory_v2998 as inventory
import native_cpu_square_startup_contract_v3005 as phase
import current_sonya_cpu_square_contract_v2045 as original
import run_native_cpu_square_locks_dispatch_v3002 as dispatch

ROOT=inventory.ROOT
OUT=ROOT/'audit_v3009_native_cpu_square_locks_checked'
need=inventory.need

def original_phase_source():
    need(inspect.getsource(original.source)==inspect.getsource(phase.source),'Every original Square/RNG/fall/cleanup program invariant retained exactly')
    source=inspect.getsource(original.verify)
    replacements=[
      ('def verify(log,guest):','def verify(log,guest,player):'),
      ("assert sel['human']==cold['human']=='kano'and sel['human_id']==cold['human_id']==17",
       "human_id=P.HUMANS[player]\n assert sel['human']==cold['human']==player and sel['human_id']==cold['human_id']==human_id"),
      ("relevant=[r for r in own if r['frame']<=ready]",
       "relevant=[r for r in own if r['frame']<=ready]\n later=[r['frame']for r in own if r['frame']>ready and r['kind']in ('leg','ring','square','bicycle','knife','ball','choke')]\n tailEnd=min([ready+31,*later])\n entry_boundary(log,guest,player,start,ready)"),
      ('range(start,ready+32)','range(start+1,tailEnd+1)'),
      ('baseline=by[start]','baseline=by[start+1]'),
      ('(18,18,17,17,0,1,2,1)','(18,18,human_id,human_id,0,1,2,1)'),
      ("r['vfloor']==r['stage_floor']-134","r['vfloor']==r['stage_floor']-(135 if human_id==18 else 134)"),
      ("assert not [r for r in P.rows(log,'HEALTH')if start<=r['frame']<=ready+30]",
       "assert not [r for r in inventory.rows(log,'MK2_SQUARE_LOCK_HEALTH')if start<=r['frame']<=tailEnd]"),
      ("flags=[r for r in P.flag_rows(log)if start<=r['frame']<=ready]",
       "flags=[r for r in inventory.rows(log,'MK2_SQUARE_LOCK_FLAG')if start<=r['frame']<=ready]"),
      ('for at in range(ready+1,ready+32):','for at in range(ready+1,tailEnd+1):'),
      ('everyPostRegainCallback=True,lastScene=ready+30',
       'everyReachedPostRegainCallback=True,postRegainOrdinaryCallbacks=tailEnd-ready,\n  originalThirtyOneCallbackOrdinaryTailAccepted=tailEnd==ready+31,lastScene=tailEnd')]
    for before,after in replacements:
        need(before in source,'Explicit original native context adaptation exists '+before)
        source=source.replace(before,after)
    need(source.rstrip()==inspect.getsource(phase.verify).rstrip(),'All original native phase/physics/lock checks retained except declared actual-context API and separately labelled later branch')

def verify():
    original_phase_source();pins={};cases={}
    runner=(ROOT/'tools/run_native_cpu_square_locks_v3001.ps1').read_text()
    expected=(ROOT/'tools/run_native_cpu_square_display_v2994.ps1').read_text().replace(
      '"$root/mk2ks_native_cpu_square_boundary_v2993.lua","$root/mk2/mk2-maincpu.bin"',
      '"$root/mk2ks_native_cpu_square_boundary_v2993.lua","$root/mk2ks_native_cpu_square_locks_v3000.lua","$root/mk2/mk2-maincpu.bin"').replace(
      '-autoboot_script "$root/mk2ks_native_cpu_square_boundary_v2993.lua"','-autoboot_script "$root/mk2ks_native_cpu_square_locks_v3000.lua"')
    need(runner.rstrip()==expected.rstrip(),'Entire original normal-input run unchanged except startup read-only observer')
    for build,player,approach,policy in dispatch.CASES:
        folder=ROOT/dispatch.name((build,player,approach,policy))
        log,guest,case=inventory.capture(folder,build,player,approach,policy,pins)
        native=inventory.boundary(log,guest,player)
        result=phase.verify(log,guest,player)
        prior=ROOT/inventory.dispatch.name((build,player,approach,policy))
        oldlog=(prior/'run.log').read_text(encoding='utf-8-sig')
        prefixes=('MK2_CPU_PAIR_','MK2_CPU_ROUND_','MK2_CPU_OVERLAP_','MK2_CPU_CHOICE_','MK2_SQUARE_NATIVE_','MK2_P2CPU_')
        actual=[line for line in log.splitlines()if line.startswith(prefixes)]
        old=[line for line in oldlog.splitlines()if line.startswith(prefixes)]
        need(actual==old and case['health']['allModePhysicalFields']==3602 and case['stateLedger']['liveFields']>0,'All actual original physical/CPU/RNG/health/state events identical with entry taps added')
        need((folder/'guest_maincpu.bin').read_bytes()==(prior/'guest_maincpu.bin').read_bytes(),'Actual whole guest unchanged by observer')
        case.update(case=folder.name,build=build,player=player,squareBoundaries=native,phase=result,
                    originalPhysicalAndNativeEventsUnchanged=True,actualOriginalEvents=len(actual),
                    moveMissPhaseAccepted=True,allCPUOrArtAudioAccepted=False)
        cases[build+'_'+player]=case
        pins[str((prior/'run.log').resolve())]=inventory.assembly.sha(prior/'run.log')
        pins[str((prior/'guest_maincpu.bin').resolve())]=inventory.assembly.sha(prior/'guest_maincpu.bin')
        print(folder.name+': actual source-bound initial locks and complete 54-field Square miss phases passed',flush=True)
    need(cases['new_sonya']['phase']['postRegainOrdinaryCallbacks']==7 and not cases['new_sonya']['phase']['originalThirtyOneCallbackOrdinaryTailAccepted']and
         cases['old_kano']['phase']['postRegainOrdinaryCallbacks']==31 and cases['old_kano']['phase']['originalThirtyOneCallbackOrdinaryTailAccepted'],
         'Candidate next native Leg Grab retained, not substituted for original control 31-callback ordinary tail')
    for module in tuple(sys.modules.values()):
        file=getattr(module,'__file__',None)
        if file and Path(file).resolve().is_relative_to(ROOT/'tools')and Path(file).suffix=='.py':pins[str(Path(file).resolve())]=inventory.assembly.sha(file)
    for leaf in ('audit_v2999_native_cpu_square_inventory_checked','audit_v3003_native_cpu_square_locks_dispatch'):
        path=ROOT/leaf/'report.json';pins[str(path.resolve())]=inventory.assembly.sha(path)
    for file,wanted in pins.items():need(inventory.assembly.sha(file)==wanted,'Immutable complete native input/capture dependency '+file)
    return dict(passed=True,cases=cases,actualPhysicalFixtures=2,actualInitialEntryStoresCaptured=True,
      fullOriginalSquareMissPhaseChecksRetained=True,sourceBoundNativeCollisionReturns=52,
      candidateMirrorIdleTailSubstituted=False,allCPUOrHitOrArtAudioAccepted=False,
      gameChanged=False,fullPortAcceptance=False,inputHashes=pins,scope=__doc__)

if __name__=='__main__':
    need(not OUT.exists(),'Immutable actual Square initial-lock/phase proof')
    try:report=verify()
    except Exception as error:report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
    OUT.mkdir();(OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items()if k not in('cases','inputHashes')},indent=2),flush=True)
    raise SystemExit(0 if report['passed']else 1)
