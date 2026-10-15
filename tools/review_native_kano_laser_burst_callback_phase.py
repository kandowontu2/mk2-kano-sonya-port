"""Match each passive field to its actual emulator callback phase.

Original frame callback precedes the scheduled shake step at164+3n; its
instruction tap records that later step in the same frame. Native callback
records after that step. Compare exact instruction-tap cadence and each full
timeline at its own real phase, not a fabricated same-phase field reading.
Also preserve opaqueFF raster ABI and the original first observed age1.
All preceding failed reviews and all executed game inputs stay immutable.
"""
import inspect
from pathlib import Path
import review_native_kano_laser_burst as prior
import review_native_kano_laser_burst_raster_abi as raster

ROOT=prior.ROOT
OUT=ROOT/'audit_native_kano_laser_burst_callback_phase_review'


def main():
    prior.need('Every original burst-global field' in (prior.OUT/'failure.txt').read_text() and
        'Original complete18-step shake and final restoration' in (raster.OUT/'failure.txt').read_text(),
        'Both actual review-side failures conserved')
    scope=dict(vars(prior),OUT=OUT,__file__=__file__,uniform_digest=raster.uniform_digest)
    original=inspect.getsource(prior.original_contract)
    edits=[("list(range(241)), 'Every original burst-global field'",
            "list(range(1,241)), 'Every original field after instruction-tap activation'"),
        ('want=0xfff4 if age<218 and ((age-164)//3)%2==0 else 0',
         'want=0xfff4 if 165<=age<218 and ((age-165)//3)%2==0 else 0'),
        ("sourceBackgroundWord='0000')",
         "sourceBackgroundWord='0000',sourceFieldCallbackPhase='before same-frame scheduled shake step; instruction taps retain164+3n exact step ages')")]
    for old,new in edits:
        prior.need(original.count(old)==1,'Exact original callback-phase specialization')
        original=original.replace(old,new)
    exec(compile(original,__file__+'::source_actual_callback_phase','exec'),scope)
    source=inspect.getsource(prior.main)
    old="paths=[Path(__file__),Path(prior.__file__),stage_path,donor_path,old_failure,"
    new="paths=[Path(__file__),ROOT/'tools/review_native_kano_laser_burst.py',ROOT/'tools/review_native_kano_laser_burst_raster_abi.py',ROOT/'audit_native_kano_laser_burst_review/failure.txt',ROOT/'audit_native_kano_laser_burst_raster_abi_review/failure.txt',Path(prior.__file__),stage_path,donor_path,old_failure,"
    prior.need(source.count(old)==1,'Complete immutable review and runtime provenance')
    source=source.replace(old,new)
    exec(compile(source,__file__+'::same_strict_native_contracts','exec'),scope)
    scope['main']()


if __name__=='__main__':main()
