"""Preserve the integer-key serialization mismatch; same actual rasters only."""
import inspect
from pathlib import Path
import qualify_native_selector_held_visuals as original


def verify(ram):
    source=inspect.getsource(original.verify)
    changes=(("proof==ram['heldTimingReport']","proof==json.loads(json.dumps(ram['heldTimingReport']))"),
             ('Path(__file__),proof_path','Path(__file__),Path(original.__file__),proof_path'),
             ('report=dict(passed=True,','report=dict(passed=True,originalIntegerKeySerializationComparisonFailurePreserved=True,'))
    for before,after in changes:
        assert source.count(before)==1
        source=source.replace(before,after,1)
    scope=dict(vars(original),original=original,Path=Path,__file__=__file__)
    exec(compile(source,__file__+'::same_native_proof_json_key_normalization','exec'),scope)
    return scope['verify'](ram)
