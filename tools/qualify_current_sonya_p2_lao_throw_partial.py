"""Successor: a wall-capped run cannot emit its terminal HOST_BOUND row."""
from pathlib import Path

if __name__ == '__main__':
    original = Path(__file__).with_name('qualify_current_sonya_p2_lao_throw_campaign.py')
    code = original.read_text()
    failed = "    assert len(rows['HOST_BOUND'])==1 and rows['HOST_BOUND'][0]['maximum_fields']=='20000'"
    assert code.count(failed) == 1
    code = code.replace(failed, "    assert not rows.get('HOST_BOUND')")
    exec(compile(code, str(original)+' [partial-terminal successor]', 'exec'),
         {'__name__': '__main__', '__file__': str(original)})
