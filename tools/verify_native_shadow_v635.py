"""Matched native-shadow executable/source/runtime/UI checkpoint, not full port."""
import argparse
import hashlib
import json
import re
from pathlib import Path
from inspect_native_shadow_rows_v635 import inspect as inspect_rows
from inspect_natural_arena_floor_v635 import inspect as inspect_video
from verify_native_ui_flow_v635 import ROOT, NAME, EXE, PAYLOAD, verify as verify_ui


def digest(path): return hashlib.sha256(Path(path).read_bytes()).hexdigest().upper()
def need(condition, message):
    if not condition: raise ValueError(message)


def check_capture(folder):
    result = json.loads((folder/'result.json').read_text(encoding='utf-8-sig'))
    before = json.loads((folder/'input_hashes_before.json').read_text(encoding='utf-8-sig'))
    need(result['input_hashes'] == before, 'Exact before/after input manifest')
    need((result['exit_code'],result['candidate'],result['executable_sha256'],result['payload_sha256'],result['assistance']) ==
         (0,NAME,EXE,PAYLOAD,'none'), 'Exact terminal native candidate capture')
    for filename, sha in before.items():
        need(digest(filename) == sha, 'Changed capture input: '+filename)
        if Path(filename).suffix in ('.lua','.ps1','.json'):
            need(digest(folder/'input_sources'/Path(filename).name) == sha, 'Changed frozen observer/build input')
    log = (folder/'run.log').read_text(encoding='utf-8-sig')
    need(not re.search(r'\[LUA ERROR\]|fatal error|access violation|stack traceback',log,re.I), 'No runtime/observer error')
    observer = next((folder/'input_sources').glob('mk2ks_natural_campaign_probe_v*.lua')).read_text()
    need(not re.search(r'write_u\d+|:write_|load_?state|\.value\s*=(?!=)|dofile\(', observer), 'Observer cannot supply guest state')
    for line in log.splitlines():
        if line.startswith('MK2_NAT_CAMPAIGN_'):
            need('writes=0 assistance=none ' in line, 'Every observed record is input-only')
    final = re.findall(r'^MK2_NAT_CAMPAIGN_RESULT .+$', log, re.M)
    need(len(final) == 1 and 'frame=3556 ' in final[0] and 'ending=-1 reset=-1 ' in final[0], 'Exact bounded cold-run terminal, no reset')
    return before,log


def verify():
    candidate = ROOT/NAME
    build = json.loads((candidate/'build-info.json').read_text(encoding='utf-8-sig'))
    need((build['name'],build['executable_sha256'],build['payload_sha256']) == (NAME,EXE,PAYLOAD), 'Exact native shadow build')
    need(digest(candidate/'mkport_candidate.exe') == EXE and digest(candidate/'roms/mk2ks/mk2ks.mdata') == PAYLOAD, 'Matched executable and payload')
    for filename,sha in build['input_hashes'].items(): need(digest(filename) == sha, 'Changed build input: '+filename)
    old = json.loads((ROOT/'diagnostic_v602_native_pit_position/build-info.json').read_text(encoding='utf-8-sig'))
    changed = {str(Path(p).name) for p,s in old['input_hashes'].items() if p in build['input_hashes'] and build['input_hashes'][p] != s}
    need(changed == {'midtunit.cpp','midtunit_v.cpp'}, 'Only original tracked video/map source changed; header newly tracked')
    need(old['payload_sha256'] == PAYLOAD, 'No gameplay payload change')
    archive = ROOT/'audit_v634_pre_native_shadow_sources'
    original_hashes = dict(zip(('midtunit.cpp','midtunit_v.cpp','midtunit_v.h'),(
        '72226681DF4EE21FA0250C25037F8E150386B954114DC58015F8110823082A3C',
        '1DB05087A5562DCC6C03241A744542168FF2D64FF0C5301FCAABB2F10E0E44EC',
        '8BA30B7AA635EA1FD68CF46697560E58BA7E3FC7A2C760C0881414836FBFD4D5')))
    for name,sha in original_hashes.items(): need(digest(archive/name) == sha, 'Exact pre-change source archive')
    runtime = {}
    inputs = dict(build['input_hashes'])
    for side in (1,2):
        for fighter in ('kano','sonya'):
            folder = ROOT/f'audit_v{639 if side == 1 else 636}_native_shadow_{"rows_" if side == 1 else ""}{fighter}_p{side}'
            manifest,log = check_capture(folder)
            inputs.update(manifest)
            row = inspect_rows(folder)
            need(row['rowStreamVerified'], 'Every independently decoded component row stream is native')
            video = inspect_video(folder)
            need(video['frames'] == (9 if side == 2 and fighter == 'sonya' else 15), 'Exact fixed screenshot window')
            need(all(r['vram_mismatches'] == r['displayed_mismatches'] == r['shadow_mismatches'] == 0 and r['shadow_pixels'] > 0
                     for r in video['records']), 'Every actual indexed VRAM word/display pixel/shadow matches independent replay')
            if side == 1:
                prior = (ROOT/f'audit_v638_native_shadow_{fighter}_p1/run.log').read_text(encoding='utf-8-sig')
                timeline = lambda value: [line for line in value.splitlines() if re.match(r'MK2_NAT_CAMPAIGN_(INPUT|HEALTH|FIGHT|STATE) ',line)]
                need(timeline(log) == timeline(prior), 'Expanded read-only component observation does not change gameplay chronology')
            runtime[f'{fighter}_p{side}'] = dict(row=row,video=video)
    ui = {}
    for side in (1,2):
        for fighter in ('kano','sonya'):
            folder = ROOT/f'audit_v{638 if side == 1 else 637}_native_shadow_ui_{fighter}_p{side}'
            ui[f'{fighter}_p{side}'] = verify_ui(folder,fighter,side)
    return dict(candidate=NAME, executable_sha256=EXE,payload_sha256=PAYLOAD,
                scope='Owned native compressed-row stepping, fixed Dead Pool drawing passes, both-slot CSS/ladder/first-match UI; not all-arena grounding or full gameplay',
                runtime=runtime,ui=ui, checked_build_inputs=inputs,
                shadow_copies=sum(c['row']['checked_copies'] for c in runtime.values()),
                shadow_components=sum(c['row']['components'] for c in runtime.values()),
                samples=sum(c['video']['frames'] for c in runtime.values()),
                nativeShadowRowCheckpointPassed=True,fullPortAcceptance=False,floorAcceptance=False)


if __name__ == '__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path)
    args=parser.parse_args()
    result=verify()
    encoded=json.dumps(result,indent=2)
    if args.output:
        args.output.write_text(encoded+'\n',encoding='utf-8')
    else: print(encoded)
