"""Preserve executed checker; match the reused gate's actual failure type."""
from pathlib import Path

original = Path(__file__).with_name('qualify_bounded_current_morph_kos.py')
successor = original.with_name('qualify_bounded_current_morph_kos_fault_exception.py')
assert not successor.exists()
source = original.read_text()
before = '            except AssertionError:\n                pass\n'
after = ('            except ValueError as error:\n'
         "                assert str(error) == 'Every health change uses original collision/round initialization writer, no assistance'\n")
assert source.count(before) == 1
successor.write_text(source.replace(before, after))
print('Prepared exact ValueError fault check; unchanged gameplay gate')
