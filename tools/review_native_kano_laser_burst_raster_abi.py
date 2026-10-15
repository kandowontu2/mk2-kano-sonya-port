"""Correct only review-side raster ABI and original first-field boundary.

The actual RAM rasters have opaqueFF in their fourth byte, not zero.
Original start is detected inside an instruction tap after its frame callback,
so its passive global timeline begins at1. Native observer records0 as well.
Preserve the failed review, its frozen source, and all runtime evidence.
"""
import hashlib
import inspect
from pathlib import Path
import review_native_kano_laser_burst as prior

ROOT=prior.ROOT
OUT=ROOT/'audit_native_kano_laser_burst_raster_abi_review'


def uniform_digest(bgr):
    return hashlib.sha256(bytes((*bgr,255))*400*254).hexdigest().upper()


def main():
    failed=prior.OUT/'failure.txt'
    prior.need('Every original burst-global field' in failed.read_text(),
               'Actual previous review-side field-origin failure conserved')
    scope=dict(vars(prior),OUT=OUT,__file__=__file__,uniform_digest=uniform_digest)
    original=inspect.getsource(prior.original_contract)
    old="list(range(241)), 'Every original burst-global field'"
    prior.need(original.count(old)==1,'Exact original callback-origin boundary')
    original=original.replace(old,"list(range(1,241)), 'Every original burst-global field after instruction-tap activation'")
    exec(compile(original,__file__+'::actual_original_callback_origin','exec'),scope)
    source=inspect.getsource(prior.main)
    old="paths=[Path(__file__),Path(prior.__file__),stage_path,donor_path,old_failure,"
    new="paths=[Path(__file__),ROOT/'tools/review_native_kano_laser_burst.py',ROOT/'audit_native_kano_laser_burst_review/failure.txt',Path(prior.__file__),stage_path,donor_path,old_failure,"
    prior.need(source.count(old)==1,'Both failed checkers and actual runtime/source provenance')
    source=source.replace(old,new)
    exec(compile(source,__file__+'::strict_same_runtime_contracts','exec'),scope)
    scope['main']()


if __name__=='__main__':main()
