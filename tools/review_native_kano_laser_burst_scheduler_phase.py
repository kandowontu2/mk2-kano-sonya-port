"""Final finite review using measured callback phase and opaque raster ABI.

Original frame reads precede instruction-tap flash/shake writes in that frame.
Native frame reads follow them. Exact helper-entry ages and rendered white
ages still match across games; complete global timelines use their measured
phases. No runtime input, source range, or cleanup gate is relaxed.
Every earlier executed/failed checker is retained and pinned.
"""
import inspect
from pathlib import Path
import review_native_kano_laser_burst as prior
import review_native_kano_laser_burst_raster_abi as raster

ROOT=prior.ROOT
OUT=ROOT/'audit_native_kano_laser_burst_scheduler_phase_review'


def main():
    failed=['audit_native_kano_laser_burst_review','audit_native_kano_laser_burst_raster_abi_review',
            'audit_native_kano_laser_burst_callback_phase_review']
    checks=['Every original burst-global field','Original complete18-step shake and final restoration',
            'Original background/palette restore timing']
    for folder,message in zip(failed,checks):
        prior.need(message in (ROOT/folder/'failure.txt').read_text(),'Actual prior checker failure conserved')
    scope=dict(vars(prior),OUT=OUT,__file__=__file__,uniform_digest=raster.uniform_digest)
    original=inspect.getsource(prior.original_contract)
    edits=[("list(range(241)), 'Every original burst-global field'",
            "list(range(1,241)), 'Every original field after instruction-tap activation'"),
        ('want=0xfff4 if age<218 and ((age-164)//3)%2==0 else 0',
         'want=0xfff4 if 165<=age<218 and ((age-165)//3)%2==0 else 0'),
        ('166<=age<172','167<=age<173'),
        ("sourceBackgroundWord='0000')",
         "sourceBackgroundWord='0000',sourceFieldCallbackPhase='before same-frame scheduled writes; flash fields167..172, quake field changes165+3n; instruction entry ages166/172 and164+3n unchanged')")]
    for old,new in edits:
        expected=2 if old=='166<=age<172' else 1
        prior.need(original.count(old)==expected,'Exact original measured callback boundary')
        original=original.replace(old,new)
    exec(compile(original,__file__+'::complete_original_pre_write_fields','exec'),scope)
    # Rebind this function to the measured fourth-byteFF whole-raster helper.
    # No predicates or native timing/lifecycle expectations are changed.
    exec(compile(inspect.getsource(prior.burst_contract),__file__+'::complete_native_post_write_fields','exec'),scope)
    source=inspect.getsource(prior.main)
    old="paths=[Path(__file__),Path(prior.__file__),stage_path,donor_path,old_failure,"
    extra=[ROOT/'tools'/leaf for leaf in ('review_native_kano_laser_burst.py',
        'review_native_kano_laser_burst_raster_abi.py','review_native_kano_laser_burst_callback_phase.py')]
    extra += [ROOT/folder/'failure.txt' for folder in failed]
    new='paths=[Path(__file__),'+','.join('ROOT/'+repr(str(p.relative_to(ROOT)).replace('\\','/')) for p in extra)+',Path(prior.__file__),stage_path,donor_path,old_failure,'
    prior.need(source.count(old)==1,'Complete failed reviewer, runtime, and source provenance')
    source=source.replace(old,new)
    exec(compile(source,__file__+'::same_strict_two_slot_review','exec'),scope)
    scope['main']()


if __name__=='__main__':main()
