"""Latest selector build: real Shang form special and native timed return.

Whole previous physical controller/terminal-first RAM audio transport retained.
Add full HIGH/OWNED/reservedGFX startup windows and retain the exact Popen.
No forced identity, timer, HP, AI, RNG, register, position or saved state.
"""
import inspect
import json
import sys
from pathlib import Path
from types import SimpleNamespace
import capture_morph_startup_return as original
import qualify_native_selector_sonya_walkin_winner_pcm as checkpoint

ROOT, need, sha = original.ROOT, original.need, original.sha
LUA = ROOT/'mk2ks_native_selector_morph_startup_return.lua'
PREFIX = 'audit_native_selector_morph_startup_return'
PARENT = checkpoint.OUT/'report.json'
CASES = {}
SCOPE = None


def prepare(state):
    parent = json.loads(PARENT.read_text())
    need(parent['passed'] and not original.original.identity.census() and
         all(sha(p) == h for p, h in parent['inputHashes'].items()),
         'Latest overlap checkpoint and whole current immutable build/source inventory')
    build = state['build']
    current = SimpleNamespace(ROOT=ROOT, NAME='diagnostic_native_selector_layers_long',
        EXE_SHA=build['executable_sha256'], PAYLOAD_SHA=build['payload_sha256'],
        GUEST_SHA=build['expected_guest_sha256'], __file__=__file__,
        expected=lambda: state['guest'], expected_gfx=lambda: state['gfx'])
    need(sha(ROOT/current.NAME/'mkport_candidate.exe') == current.EXE_SHA and
         sha(ROOT/current.NAME/'roms/mk2ks/mk2ks.mdata') == current.PAYLOAD_SHA,
         'Actual current private candidate, not obsolete morph build')
    source = original.source
    def replace(before, after):
        nonlocal source
        need(source.count(before) == 1, 'Exact whole original capture adaptation: '+before)
        source = source.replace(before, after, 1)
    replace("audit_morph_startup_return_{move}_p{side}_delay{delay}",
            PREFIX+"_{move}_p{side}_delay{delay}")
    replace(' LAST_CAPTURE=carrier',
            " carrier['coldBuffers']={k:bytearray() for k in WINDOWS}\n LAST_CAPTURE=carrier")
    replace("errors='replace')", "errors='replace',creationflags=subprocess.CREATE_NO_WINDOW)")
    replace('  observed=None', "  carrier['process']=job\n  observed=None")
    replace("str(folder)in observed['CommandLine']", "observed['CommandLine']==subprocess.list2cmdline(command)")
    replace("      if tag=='MK2_BBAUDIO_PCM':",
            "      if tag=='MK2_DRAIN_STARTUP':\n"
            "       kind=head['kind'];need(kind in WINDOWS and int(head['offset'])==len(carrier['coldBuffers'][kind]) and head['writes']=='0' and head['assistance']=='none' and int(head['start'],16)==(0x1fb0000 if kind=='graphics' else 0),'Complete ordered read-only native startup window')\n"
            "       carrier['coldBuffers'][kind].extend(raw);need(len(carrier['coldBuffers'][kind])<=len(WINDOWS[kind]),'No duplicate or overflow native startup bytes')\n"
            "       need(bytes(carrier['coldBuffers'][kind])==WINDOWS[kind][:len(carrier['coldBuffers'][kind])],'Every actual native initialized byte equals independent current source')\n"
            "      elif tag=='MK2_BBAUDIO_PCM':")
    replace("  need(all(sha(p)==h for p,h in pins.items()),'Every actually executed input unchanged')",
            "  need(all(bytes(carrier['coldBuffers'][k])==v for k,v in WINDOWS.items()) and carrier['text'].count('MK2_DRAIN_STARTUP_COMPLETE writes=0 assistance=none')==1,'Every full native HIGH/OWNED/reservedGFX startup window proved in THIS morph game')\n"
            "  need(all(sha(p)==h for p,h in pins.items()),'Every actually executed input unchanged')")
    replace(" pins=dict(json.loads((build/'build-info.json').read_text(encoding='utf-8-sig'))['input_hashes'])",
            " pins=dict(PARENT_PINS)\n compiled=json.loads((build/'build-info.json').read_text(encoding='utf-8-sig'))['input_hashes']\n for p,h in compiled.items():need(p not in pins or pins[p]==h,'No current compiled input replaced');pins[p]=h")
    replace(' folder.mkdir()',
            " for module in tuple(sys.modules.values()):\n"
            "  name=getattr(module,'__file__',None)\n"
            "  if name and Path(name).resolve().is_relative_to(ROOT) and Path(name).is_file():\n"
            "   p=str(Path(name).resolve());h=sha(p);need(p not in pins or pins[p]==h,'Every executed local source immutable');pins[p]=h\n"
            " for p in (PARENT,LUA,ROOT/'mk2ks_native_shang_drain_startup.lua',ROOT/'mk2ks_morph_startup_return.lua'):\n"
            "  p=str(p.resolve());h=sha(p);need(p not in pins or pins[p]==h,'Actual loaded observer immutable');pins[p]=h\n"
            " need(all(sha(p)==h for p,h in pins.items()),'Whole actual morph source/build inventory before dispatch')\n"
            ' folder.mkdir()')
    scope = dict(original.scope, __file__=__file__, current=current, LUA=LUA,
        WINDOWS=state['WINDOWS'], PARENT=PARENT, PARENT_PINS=parent['inputHashes'], sys=sys,
        LAST_CAPTURE=None)
    exec(compile(source, __file__+'::whole_original_morph_capture_current_selector_windows', 'exec'), scope)
    return scope


def execute(state, move='ball', side=1, preflight=False):
    global SCOPE
    need(move in ('ball','square') and side in (1,2), 'Only actual known morph physical routes')
    scope = prepare(state)
    need(scope['LAST_CAPTURE'] is None, 'No new native child in source-only preflight')
    if preflight:
        return dict(passed=True, sourceOnly=True, move=move, side=side,
            originalPhysicalInputsUnchanged=True, fullNativeWindowsStillRequired=True,
            newNativeGames=0, fullPortAcceptance=False)
    SCOPE = scope
    try:
        result = scope['run'](move, side, 1)
    finally:
        if scope['LAST_CAPTURE'] is not None:
            CASES[move, side] = scope['LAST_CAPTURE']
    return result
