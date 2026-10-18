import unittest
import numpy as np
from chicken_shared_filter import fit_shared_filter

class SharedFilter(unittest.TestCase):
    def test_known_filter_and_validation_changes_cannot_change_fit(self):
        rng=np.random.default_rng(123)
        prediction=rng.normal(size=1024)
        observed=np.zeros(1024)
        coefficients=np.array([0,0,.1,.2,.4,.2,.1,0,0])
        for coefficient,offset in zip(coefficients,range(-4,5)):
            observed[4:-4]+=coefficient*prediction[4+offset:1020+offset]
        training=np.zeros(1024,dtype=bool);training[10:300]=True
        fitted,valid,proof=fit_shared_filter(observed,prediction,training)
        np.testing.assert_allclose(proof['coefficients'],coefficients,atol=1e-12)
        np.testing.assert_allclose(fitted[valid],observed[valid],atol=1e-12)
        changed=observed.copy();changed[~training]=rng.normal(size=(~training).sum())*1e6
        _,_,other=fit_shared_filter(changed,prediction,training)
        np.testing.assert_array_equal(proof['coefficients'],other['coefficients'])
        self.assertFalse(valid[:4].any() or valid[-4:].any())

    def test_rank_deficient_prefix_rejected(self):
        with self.assertRaises(AssertionError):fit_shared_filter(np.ones(128),np.ones(128),np.ones(128,dtype=bool))

if __name__=='__main__':unittest.main()
