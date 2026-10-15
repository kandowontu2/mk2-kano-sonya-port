"""Successor: bicycle is four three-field pulses, not five.

Preserve the executed predecessor; all native-state and fault checks unchanged.
"""
from pathlib import Path
import verify_native_source_sync as sync

predecessor=Path(__file__).with_name('qualify_bounded_interrupted_reactivation.py')
source=predecessor.read_text()
old="expected_count={'bicycle':15,'square':9,'ball':84}[move]"
assert source.count(old)==1
source=source.replace(old,"expected_count={'bicycle':12,'square':9,'ball':84}[move]")
source=source.replace('checkerSHA256=sync.sha(Path(__file__))','checkerSHA256=sync.sha(Path(__file__)),predecessorSHA256=sync.sha(predecessor)')
exec(compile(source,str(Path(__file__)), 'exec'))
