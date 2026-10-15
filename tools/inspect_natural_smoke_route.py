"""Compose exact Lua adaptations for inspection, without running a game."""
import ast
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LITERAL = r"(?:'(?:[^'\\]|\\.)*'|\"(?:[^\"\\]|\\.)*\"|\[\[[\s\S]*?\]\])"


def decode(s):
    return s[2:-2] if s.startswith('[[') else ast.literal_eval(s)


def adaptations(script, source):
    edits = re.findall(r'source=change\(source,('+LITERAL+r'),\s*('+LITERAL+r')\)', script)
    assert len(edits) == script.count('source=change(')
    for a, b in edits:
        a, b = decode(a), decode(b)
        assert source.count(a) == 1, a[:100]
        source = source.replace(a, b, 1)
    return source, len(edits)


def compose(script):
    source, count = adaptations(script, (ROOT/'mk2ks_native_stage_performer_v806.lua').read_text())
    assert source.count('screen:snapshot(') == 2
    source = source.replace('screen:snapshot(', '_secret_emit(')
    prefix = script.split('local prefix=[[', 1)[1].split(']]', 1)[0]
    return prefix+source, count


if __name__ == '__main__':
    source, count = compose((ROOT/'mk2ks_natural_smoke_route.lua').read_text())
    lines = source.splitlines()
    for n in range(115, 128):
        print(f'{n}: {lines[n-1]}')
    print('edits', count)
