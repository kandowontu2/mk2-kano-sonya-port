"""Extract references using the original caller's ONE palette lookup per stream.

The executed failing predecessor is immutable. No image editing or game writes.
"""
import inspect
from pathlib import Path
import prepare_native_shang_drain_references as original


def main():
    source = inspect.getsource(original.main)
    before = 'palette_address = animation.u32(stock, animation.stock_file(parts[0]) + 14)'
    after = ('first_parts = animation.frame_group(stock, groups[0], 0xff800000, 0xffffffff)\n'
             '            assert first_parts\n'
             '            palette_address = animation.u32(stock, animation.stock_file(first_parts[0]) + 14)')
    assert source.count(before) == 1
    source = source.replace(before, after, 1)
    before = 'str(Path(__file__)): sha(Path(__file__).read_bytes())}'
    after = ('str(Path(__file__)): sha(Path(__file__).read_bytes()),\n'
             '            str(Path(original.__file__)): sha(Path(original.__file__).read_bytes())}')
    assert source.count(before) == 1
    source = source.replace(before, after, 1)
    source = source.replace('palette += [(0, 0, 0, 255)] * (256 - len(palette))',
                            'palette += [(0, 0, 0, 255)] * (256 - len(palette))')
    scope = dict(vars(original), original=original, __file__=__file__)
    exec(compile(source, __file__ + '::same_native_reference_with_first_phase_palette', 'exec'), scope)
    return scope['main']()


if __name__ == '__main__':
    main()
