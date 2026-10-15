"""Reuse exact native-health census for the distinct recovery counter policy."""
from types import FunctionType
import check_bounded_native_counterkick_probe as prior
scope=dict(vars(prior),BASE=prior.prior.ROOT/'audit_bounded_native_recovery_counterkick_runtime',__file__=__file__)
main=FunctionType(prior.main.__code__,scope)
if __name__=='__main__':main()
