"""One actual native secret-route attempt; whole sources/RGB stay in RAM.

Only normal coins, selection, earned arena rotation, attacks, Down and Start.
Never inject a secret opponent or assist health/RNG. Drain the same process to
terminal even after an observer failure; a deadline is an unaccepted attempt.
"""
import argparse
import ast
import code
import gzip
import hashlib
import json
import os
import re
import subprocess
import time
from pathlib import Path
import kano_ball_launch_context_v6642 as current
import native_process_census_v6647 as native

ROOT, need, sha = current.ROOT, current.need, current.sha
LUA = ROOT/'mk2ks_natural_smoke_route.lua'
DRIVER = ROOT/'mk2ks_native_stage_performer_v806.lua'
GRAPHICS_PROBE = ROOT/'mk2ks_graphics_reset_probe.lua'


def preflight():
    source, script = DRIVER.read_text(), LUA.read_text()
    need(not re.search(r'write_[ui]\d+|:write_|\.value\s*=(?!=)|load_?state', script+source),
         'Both complete observers/controllers use only normal physical input and passive reads')
    literal = r"(?:'(?:[^'\\]|\\.)*'|\"(?:[^\"\\]|\\.)*\"|\[\[[\s\S]*?\]\])"
    replacements = re.findall(r'source=change\(source,('+literal+r'),\s*('+literal+r')\)', script)
    need(len(replacements) == script.count('source=change('), 'Every declared whole-driver adaptation parsed')
    decode = lambda s: s[2:-2] if s.startswith('[[') else ast.literal_eval(s)
    for before, after in replacements:
        before, after = decode(before), decode(after)
        need(source.count(before) == 1, 'Exact unique native driver adaptation '+before[:70])
        source = source.replace(before, after, 1)
    need(source.count('screen:snapshot(') == 2, 'Only two original screen snapshot sinks')
    stock = (ROOT/'mk2/mk2-maincpu.bin').read_bytes()
    guest = current.expected()
    for lo, hi in ((0xffa19fd0, 0xffa1a610), (0xffa1bda0, 0xffa1c5f0), (0xffa0ba10, 0xffa0baf0)):
        a, b = (lo-0xff800000)//8, (hi-0xff800000)//8
        need(guest[a:b] == stock[a:b], 'Whole untouched original secret trigger/cinematic/role construction code')
    return dict(passed=True, wholeDriverEdits=len(replacements), noGameStateAssistance=True,
                originalSecretTriggerArena=7, originalToastyClockWindow=64, input='Down + normal Start')


def run(fighter, side, attempt='portal_entry_correction', duration_seconds=920, graphics_probe=False, extra_pin_paths=()):
    need(bool(re.fullmatch(r'[a-z0-9_]+', attempt)), 'Safe explicit attempt label')
    need(isinstance(duration_seconds, int) and 920 <= duration_seconds <= 2400, 'Bounded explicit physical-policy duration')
    out = ROOT/f'audit_natural_smoke_route_{fighter}_p{side}_{attempt}'
    need(not out.exists() and not native.census(), 'One fresh native attempt; no replay or conflicting game')
    pre = preflight()
    script = GRAPHICS_PROBE if graphics_probe else LUA
    if graphics_probe:
        probe = GRAPHICS_PROBE.read_text()
        need(probe.count("dofile('mk2ks_natural_smoke_route.lua')") == 1 and
             not re.search(r'write_[ui]\d+|:write_|\.value\s*=(?!=)|load_?state', probe),
             'Whole extra decoder observer passive; same unchanged physical controller')
        pre['boundedPassiveGraphicsProbe'] = sha(GRAPHICS_PROBE)
    guest, gfx = current.expected(), current.prior.expected_gfx()
    build = ROOT/current.NAME
    pins = {str(p.resolve()): sha(p) for p in (Path(__file__), LUA, DRIVER, Path(current.__file__), Path(native.__file__),
            ROOT/'mk2/mk2-maincpu.bin', ROOT/'mame-mkp/unidasm.exe', build/'mkport_candidate.exe', build/'build-info.json',
            build/'roms/mk2ks/mk2ks.mdata', *extra_pin_paths)}
    if graphics_probe:
        pins[str(GRAPHICS_PROBE.resolve())] = sha(GRAPHICS_PROBE)
    out.mkdir()
    env = {k:v for k,v in os.environ.items() if not re.match(r'^(MK2KS_|MK2_TRACE_|MK2_RANGE_|MK2_P2_|MK2PORT_)', k)}
    env.update(MK2KS_STAGE_SIDE=str(side), MK2KS_STAGE_WINNER=fighter, MK2KS_STAGE_ARENA='7', MK2KS_STAGE_CASE='positive')
    env['MK2KS_SECRET_LIMIT'] = str(duration_seconds-20)
    command = [str(build/'mkport_candidate.exe'), 'mk2ks', '-rompath', str(build/'roms')+';'+str(ROOT/'roms'),
               '-samplepath', str(build/'samples')+';'+str(ROOT/'samples'), '-artpath', str(ROOT/'artwork'),
               '-samples', '-skip_gameinfo', '-nocheat', '-inipath', str(out), '-video', 'none', '-sound', 'none',
               '-noautoframeskip', '-frameskip', '0', '-nothrottle', '-snapsize', '400x254', '-str', str(duration_seconds),
               '-cfg_directory', str(out/'cfg'), '-nvram_directory', str(out/'nvram'),
               '-snapshot_directory', str(out/'snap'), '-autoboot_script', str(script)]
    capture = dict(folder=out, fighter=fighter, side=side, guest=guest, gfx=gfx, pins=pins, rgbFrames=[], text='',
                   guestCount=0, gfxCount=0, decodeErrors=[], preflight=pre)
    with (out/'stderr.log').open('w', encoding='utf-8') as err:
        started = time.time()
        job = subprocess.Popen(command, cwd=ROOT, env=env, stdout=subprocess.PIPE, stderr=err,
                               text=True, encoding='utf-8', errors='replace')
        observed = None
        for _ in range(100):
            observed = next((r for r in native.census() if r['ProcessId'] == job.pid), None)
            if observed or job.poll() is not None: break
            time.sleep(.02)
        need(observed and observed['ParentProcessId'] == os.getpid() and observed['createdUnix'] >= started-1 and
             Path(observed['ExecutablePath']).resolve() == (build/'mkport_candidate.exe').resolve() and str(out) in observed['CommandLine'],
             'Actual live native executable/PID/parent/creation/command before observing')
        (out/'process.json').write_text(json.dumps(dict(pid=job.pid, command=command, actualWindowsIdentity=observed), indent=2)+'\n')
        print(json.dumps(dict(nativePID=job.pid, fighter=fighter, side=side, preflight=pre)), flush=True)
        with gzip.open(out/'run.log.gz', 'wt', encoding='utf-8') as log:
            for line in job.stdout:
                try:
                    if ' hex=' in line:
                        tag = line.split()[0]
                        pairs = re.findall(r'(\w+)=([^\s]+)', line)
                        head = dict(pairs)
                        need(len(pairs) == len(head), 'Unique entire raw transport metadata')
                        raw = bytes.fromhex(head.pop('hex'))
                        need(len(raw) == int(head['bytes']), 'Whole original declared native buffer')
                        head['sha256'] = hashlib.sha256(raw).hexdigest().upper()
                        if tag == 'MK2_HPHASE_GUEST':
                            need(raw == guest, 'Whole independently reconstructed actual guest')
                            capture['guestCount'] += 1
                        elif tag == 'MK2_HPHASE_GFX':
                            need(raw == gfx, 'Entire actual imported source GFX')
                            capture['gfxCount'] += 1
                        elif tag == 'MK2_HPHASE_RGB':
                            need(head['width'] == '400' and head['height'] == '254' and len(raw) == 406400, 'Full actual screen transport')
                            capture['rgbFrames'].append(dict(header=head, pixels=raw))
                        else:
                            raise ValueError('Unexpected raw transport '+tag)
                        log.write(tag+'_DIGEST '+' '.join(k+'='+str(v) for k,v in head.items())+'\n')
                    else:
                        log.write(line)
                        if re.search(r'MK2_STAGE_(MATCH|WINDOW|TOASTY|SECRET_(ACCEPT|FIGHT|WALK|JUMP|PUNCH|RECOVER|RESULT)) |MK2_SECRET_DEADLINE', line):
                            print(line.strip(), flush=True)
                except Exception as error:
                    capture['decodeErrors'].append(dict(error=repr(error), tag=line.split()[0] if line.strip() else 'empty'))
            exitcode = job.wait()
    with gzip.open(out/'run.log.gz', 'rt', encoding='utf-8') as log: capture['text'] = log.read()
    terminal = dict(pid=job.pid, nativeExit=exitcode, actualWindowsIdentity=observed, hostDecodeErrors=capture['decodeErrors'])
    capture['terminal'] = terminal
    (out/'native_terminal.json').write_text(json.dumps(terminal, indent=2)+'\n')
    passed = (exitcode == 0 and not capture['decodeErrors'] and capture['guestCount'] == capture['gfxCount'] == 1 and
              not (out/'stderr.log').read_text() and not re.search(r'LUA ERROR|stack traceback|fatal error|access violation', capture['text'], re.I))
    need(not native.census(), 'Exact native job terminal; never an observation timeout')
    need(all(sha(p) == h for p,h in pins.items()), 'Every actually executed source/candidate/input unchanged')
    capture['report'] = dict(passed=passed, transportOnlyAccepted=passed, actualSecretRouteAccepted=False,
                             nativeTerminal=terminal, preflight=pre, inputHashes=pins, nativeRGBFrames=len(capture['rgbFrames']),
                             newBuilds=0, newROMCopies=0, newRawMedia=0, newZIPs=0, fullPortAcceptance=False)
    (out/'report.json').write_text(json.dumps(capture['report'], indent=2)+'\n')
    print(json.dumps(dict(transportPassed=passed, nativeExit=exitcode, nativeRGBFrames=len(capture['rgbFrames']))), flush=True)
    return capture


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--fighter', choices=('kano', 'sonya'), required=True)
    parser.add_argument('--side', choices=(1,2), type=int, required=True)
    parser.add_argument('--hold', action='store_true')
    parser.add_argument('--attempt', default='portal_entry_correction')
    parser.add_argument('--duration-seconds', type=int, default=920)
    parser.add_argument('--graphics-reset-probe', action='store_true')
    args = parser.parse_args()
    capture = run(args.fighter, args.side, args.attempt, args.duration_seconds, args.graphics_reset_probe)
    if args.hold:
        code.interact(banner='Same native secret-route terminal, original RGB retained in RAM.', local=dict(capture=capture))
