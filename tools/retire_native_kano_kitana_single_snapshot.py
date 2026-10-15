"""Same protective stop conditions, one complete observed gzip snapshot.

The original stop preflight refused without terminating the game. Its code
is preserved. Avoid comparing loss counts from two separately growing reads;
retain all30+ failed attempts, rare earned rounds and five post-win losses.
"""
import inspect
import json
from pathlib import Path
from types import SimpleNamespace
import retire_native_kano_zoning_losing_kitana as previous

ROOT,need,sha=previous.ROOT,previous.need,previous.sha


def single_stats(lines,identity):
    source=inspect.getsource(previous.progress.inspect)
    first=source.index('    parse = lambda tag:')
    source="def actual_stats(lines,identity):\n    actual=next((q for q in census.census() if q['ProcessId']==identity['ProcessId']),None)\n    if actual!=identity:raise ValueError('Exact original native identity still live')\n"+source[first:]
    scope=dict(vars(previous.progress))
    exec(compile(source,__file__+'::whole_original_statistics_from_one_actual_snapshot','exec'),scope)
    return scope['actual_stats'](lines,identity)


def stop():
    source=inspect.getsource(previous.stop)
    before="    stats=progress.inspect(capture.OUT.name)\n    identity=json.loads((capture.OUT/'native_identity.json').read_text())\n    lines=reader.complete_lines(capture.OUT/'run.log.gz')"
    after="    identity=json.loads((capture.OUT/'native_identity.json').read_text())\n    lines=reader.complete_lines(capture.OUT/'run.log.gz')\n    stats=single_stats(lines,identity)"
    need(source.count(before)==1,'One entire original stop snapshot boundary')
    source=source.replace(before,after)
    before="str(Path(reader.__file__).resolve()):sha(reader.__file__)},"
    after="str(Path(reader.__file__).resolve()):sha(reader.__file__),str(Path(previous.__file__).resolve()):sha(previous.__file__)},"
    need(source.count(before)==1,'Frozen original refused-preflight source retained in stop input pins')
    scope=dict(vars(previous),__file__=__file__,single_stats=single_stats,previous=previous)
    exec(compile(source.replace(before,after),__file__+'::entire_original_safe_stop_with_single_snapshot','exec'),scope)
    return scope['stop']()


def prepare(ram):
    return previous.prepare(ram)


def retire():
    return previous.retire()


if __name__=='__main__':
    import sys
    {'stop':stop,'retire':retire}[sys.argv[1]]()
