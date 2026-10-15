"""Original command at the actual ROM's verified128..176 separation gate."""
import code
import inspect
import json
from pathlib import Path
import capture_native_secondary_kano_reference as reference

ROOT = reference.ROOT
reference.OUT = ROOT / 'audit_native_secondary_kano_source_distance'
reference.LUA = ROOT / 'mk3_native_secondary_kano_source_distance.lua'


def transformed():
    baseline = (ROOT/'mk3_native_secondary_kano_reference.lua').read_text()
    wrapper = reference.LUA.read_text()
    replacements = [
        ("local raw,w,h=machine.screens[':screen']:pixels()",
         "local screen=machine.screens[':screen'];local raw=screen:pixels();local w,h=screen.width,screen.height"),
        ('if gap>45 then press(forward)', 'if gap>65 then press(forward)'),
        ("if gap>20 then press(forward)else command=frame;geometry('COMMAND_SPACING')end",
         "if gap<144 then press(x<y and 'left' or 'right')elseif gap>152 then press(forward)else command=frame;geometry('COMMAND_SPACING')end"),
        ('local ca=frame-command', "local ca=frame-command\n   for _,at in ipairs({4,14,24,34,44,70})do if ca==at then pending[#pending+1]='command_age_'..ca end end"),
        ('0xff991f70,0xffa5ef10', '0xff991f70,0xff992ee0,0xff993160,0xff9931f0,0xff993760,0xff992090,0xffa5ef10'),
    ]
    for old, new in replacements:
        reference.need(baseline.count(old) == 1 and old in wrapper and
                       (new in wrapper or new.replace('\n', '\\n') in wrapper),
                       'Only exact physical spacing and passive raster/code observations')
        baseline = baseline.replace(old, new)
    reference.need('original_source_distance' in wrapper, 'Exact transformed Lua chunk identity')
    return baseline


def run():
    input_report = ROOT/'audit_native_kano_secondary_input/report.json'
    record = json.loads(input_report.read_text())
    reference.need(record['passed'] and record['sourceInputAccepted'] and
                   not record['runtimeAccepted'] and
                   all(reference.sha(p) == h for p, h in record['inputHashes'].items()),
                   'Actual original source input/distance map and all frozen dependencies match')
    prior = ROOT/'audit_native_secondary_kano_guarded_command/report.json'
    record = json.loads(prior.read_text())
    reference.need(record['passed'] and record['nativeExit'] == 0 and not record['finisherAccepted'] and
                   all(reference.sha(p) == h for p, h in record['inputHashes'].items()),
                   'Guarded close-distance attempt is terminal and conserved, not promoted')
    transformed()
    source = inspect.getsource(reference.run)
    changes = [
        ('source=LUA.read_text()', 'source=transformed()'),
        ("ROOT/'audit_native_secondary_finisher_reference/report.json']",
         "ROOT/'audit_native_secondary_finisher_reference/report.json', ROOT/'mk3_native_secondary_kano_reference.lua', ROOT/'tools/capture_native_secondary_kano_reference.py', ROOT/'audit_native_secondary_kano_guarded_command/report.json', ROOT/'audit_native_kano_secondary_input/report.json']"),
    ]
    for old, new in changes:
        reference.need(source.count(old) == 1, 'Unique exact provenance/controller specialization')
        source = source.replace(old, new)
    scope = dict(vars(reference), transformed=transformed, __file__=__file__)
    exec(compile(source, __file__+'::original_source_distance', 'exec'), scope)
    return scope['run']()


if __name__ == '__main__':
    capture = run()
    code.interact(banner='Original source-distance reference terminal; actual raster buffers in RAM.',
                  local=dict(capture=capture))
