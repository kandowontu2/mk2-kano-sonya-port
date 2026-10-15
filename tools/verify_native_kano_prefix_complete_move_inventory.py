"""All actual owned entries:179 knives AND2 blade swipes, not181 knives.

Preserve both original failed assumptions. Retain the complete original
inventory, actor snapshot correction, native HP and full fault suite.
"""
import inspect
import json
from pathlib import Path
import verify_native_kano_prefix_owned_snapshot_windows as snapshot

ROOT,need,sha=snapshot.ROOT,snapshot.need,snapshot.sha
OUT=ROOT/'audit_native_kano_prefix_complete_move_inventory_checked'


def once(source,before,after):
    need(source.count(before)==1,'One whole original finite gate boundary')
    return source.replace(before,after)


def run():
    snapshot_failure=snapshot.OUT/'failure.json'
    failed=json.loads(snapshot_failure.read_text())
    need(not failed['passed'] and failed['error']=="ValueError('All181 actual native knife instruction entries belong to current true Kano actor/Main, not merely intended inputs')",
         'Actual snapshot-successor failure preserved, not relabelled as a passed game')
    factory=inspect.getsource(snapshot.run)
    factory=once(factory,"    return scope['run']()","    scope['wholeSnapshotFieldsSource']=source.replace(before,after)\n    return scope")
    outer=dict(vars(snapshot),__file__=__file__,OUT=OUT)
    exec(compile(factory,__file__+'::entire_original_owned_snapshot_factory','exec'),outer)
    scope=outer['run']()
    source=scope['wholeSnapshotFieldsSource']
    source=once(source,"    for q in rows['SPECIAL']:",
        "    need(sum(q['move']=='knife' for q in rows['SPECIAL'])==179 and sum(q['move']=='blade' for q in rows['SPECIAL'])==2, 'Entire actual179-knife/two-blade native move inventory retained')\n    for q in rows['SPECIAL']:")
    source=once(source,"        need(q['move']=='knife' and q['entry']=='FFFFB000' and q['at']=='FFFFB010' and q['pc']=='FFFFB020' and",
        "        expected={'knife':('FFFFB000','FFFFB010','FFFFB020'),'blade':('FFF8CC00','FFF8CC10','FFF8CC30')}[q['move']]\n        need((q['entry'],q['at'],q['pc'])==expected and")
    source=once(source,'All181 actual native knife instruction entries belong to current true Kano actor/Main, not merely intended inputs',
        'All181 actual knife/blade instruction entries belong to current true Kano actor/Main, not merely intended inputs')
    source=once(source,'nativeWinnerCalls=19,actualOwnedKnifeEntries=181,',
        'nativeWinnerCalls=19,actualOwnedNativeEntries=181,actualOwnedKnifeEntries=179,actualOwnedBladeEntries=2,')
    exec(compile(source,__file__+'::entire_original_fields_with_complete_actual_move_inventory','exec'),scope)
    run_source=inspect.getsource(snapshot.previous.run)
    run_source=once(run_source,'for p in (Path(__file__),Path(capture.__file__),Path(prepared.__file__),Path(reader.__file__),Path(native_health.__file__),',
        'for p in (snapshot_failure,Path(snapshot.__file__),failed_path,observer_path,Path(previous.__file__),Path(__file__),Path(capture.__file__),Path(prepared.__file__),Path(reader.__file__),Path(native_health.__file__),')
    scope.update(snapshot_failure=snapshot_failure,snapshot=snapshot)
    exec(compile(run_source,__file__+'::entire_original_Kano_progression_health_and_fault_gate','exec'),scope)
    return scope['run']()


if __name__=='__main__':
    try:run()
    except Exception as error:
        need(not OUT.exists(),'Preserve original actual complete-move inventory outcome')
        OUT.mkdir();(OUT/'failure.json').write_text(json.dumps(dict(passed=False,error=repr(error),fullPortAcceptance=False),indent=2)+'\n')
        raise
