"""Partial-terminal qualification using actual stage-frame intervals."""
from pathlib import Path

if __name__ == '__main__':
    original = Path(__file__).with_name('qualify_current_sonya_p2_lao_throw_campaign.py')
    code = original.read_text()
    changes = {
        "    assert len(rows['HOST_BOUND'])==1 and rows['HOST_BOUND'][0]['maximum_fields']=='20000'":
        "    assert not rows.get('HOST_BOUND')",
        "    assert attempts and all(r['stage']=='1' for r in attempts)":
        "    assert attempts and stages==[0,1]\n    assert all(int(r['frame'])>=int(rows['STAGE'][1]['frame']) for r in attempts)",
    }
    for old, new in changes.items():
        assert code.count(old) == 1
        code = code.replace(old, new)
    exec(compile(code, str(original)+' [partial frame successor]', 'exec'),
         {'__name__': '__main__', '__file__': str(original)})
