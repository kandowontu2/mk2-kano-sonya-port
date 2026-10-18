"""Bounded historical-fix pixel mask compared with a current capture."""
import numpy as np

def verify(before,corrected,current):
    assert before.shape==corrected.shape==current.shape==(254,400,3)
    changed=np.any(before!=corrected,axis=2)
    ys,xs=np.nonzero(changed)
    assert len(xs)>0 and xs.min()>=230 and xs.max()<340 and ys.min()>=190 and ys.max()<233
    assert np.array_equal(current[changed],corrected[changed]),'Current shadow-fix pixels differ'
    return changed
