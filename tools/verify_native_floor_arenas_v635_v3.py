"""Strict matched inputs and bounded executed native replay results, not full port.

Detailed reports are reproducible with inspect_natural_arena_floor_v635_v4.py
and inspect_native_shadow_rows_v635.py. --replay recomputes those reports before
checking them; otherwise this checks the retained outputs and launch inputs.
"""
import argparse
import hashlib
import json
import re
from pathlib import Path
from verify_native_ui_flow_v635 import ROOT,NAME,EXE,PAYLOAD
from inspect_natural_arena_floor_v635_v4 import inspect as inspect_video
from inspect_native_shadow_rows_v635 import inspect as inspect_rows


def digest(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest().upper()
def need(condition,message):
    if not condition:raise ValueError(message)


def check_inputs(folder,fighter,seconds,side=2):
    result=json.loads((folder/'result.json').read_text(encoding='utf-8-sig'))
    before=json.loads((folder/'input_hashes_before.json').read_text(encoding='utf-8-sig'))
    need((result['exit_code'],result['candidate'],result['executable_sha256'],result['payload_sha256'],
          result['player'],result['human_slot'],result['seconds'],result['assistance'])==
         (0,NAME,EXE,PAYLOAD,fighter,side,seconds,'none'),'Exact terminal current native campaign')
    need(before==result['input_hashes'],'Exact before/after campaign inputs')
    for filename,sha in before.items():
        need(digest(filename)==sha,'Changed launch/build input: '+filename)
        if Path(filename).suffix in('.lua','.ps1','.json'):
            need(digest(folder/'input_sources'/Path(filename).name)==sha,'Changed frozen observer/build source')
    observer=(folder/'input_sources/mk2ks_natural_campaign_probe_v24.lua').read_text()
    need(not re.search(r'write_u\d+|:write_|load_?state|\.value\s*=(?!=)|dofile\(',observer),'Input-only cold campaigns')
    checked=dict(before)
    # Launch manifests pin inputs, not runtime outputs. Include the actual
    # logs, retained decoded reports, before/flip VRAM, palettes and PNGs too.
    for path in folder.rglob('*'):
        if path.is_file():checked[str(path)]=digest(path)
    return checked


def verify(replay=False):
    cases={};inputs={}
    for fighter,side in ((f,s)for s in(1,2)for f in('kano','sonya')):
        folder=ROOT/f'audit_v{646 if side==1 else 643}_native_floor_{fighter}_p{side}'
        inputs.update(check_inputs(folder,fighter,900,side))
        final=[];actual_arenas=set();timeline=[]
        with(folder/'run.log').open(encoding='utf-8-sig')as stream:
            for line in stream:
                need(not re.search(r'\[LUA ERROR\]|fatal error|access violation|stack traceback',line,re.I),'No runtime/observer error')
                if line.startswith('MK2_NAT_CAMPAIGN_'):
                    need('writes=0 assistance=none 'in line,'Every observation is input-only')
                if line.startswith('MK2_NAT_CAMPAIGN_RESULT '):final.append(line.strip())
                if line.startswith('MK2_NAT_CAMPAIGN_FLOOR_SNAP '):actual_arenas.add(int(re.search(r' arena=(\d+) ',line)[1]))
                if re.match(r'MK2_NAT_CAMPAIGN_(INPUT|HEALTH|FIGHT|STATE) ',line):timeline.append(line)
        need(len(final)==1 and'frame=49237 'in final[0]and'ending=-1 reset=-1 'in final[0],'Complete bounded genuine-loss/continue run, no reset')
        need(actual_arenas==set(range(9)),'All nine actual native arena IDs, not the ladder variable')
        video=inspect_video(folder)if replay else json.loads((folder/f'ordered-pass-v{4 if side==1 else 3}.json').read_text(encoding='utf-8-sig'))
        row=inspect_rows(folder)if replay else json.loads((folder/'row-stream.json').read_text(encoding='utf-8-sig'))
        need(video['frames']==({('kano',1):313,('sonya',1):296,('kano',2):330,('sonya',2):279}[fighter,side]),'Exact retained fixed sample count')
        need(all(r['vram_mismatches']==r['displayed_mismatches']==r['shadow_mismatches']==0 for r in video['records']),
             'Every retained actual VRAM word/display pixel/shadow pixel agrees exactly')
        need({r['arena']for r in video['records']}==actual_arenas,'Actual raster coverage equals native arena observations')
        need(row['rowStreamVerified']and not row['failures']and not row['oversized_rows'],'Every imported component/native row stream verified')
        cases[f'{fighter}_p{side}']=dict(terminal=final[0],actual_arenas=sorted(actual_arenas),samples=video['frames'],
            shadow_visible_samples=sum(r['shadow_pixels']>0 for r in video['records']),
            imported_body_pixels=sum(r['body'][side if side in r['body']else str(side)]['pixels']for r in video['records']),
            shadow_pixels=sum(r['shadow_pixels']for r in video['records']),
            components=row['components'],native_shadow_copies=row['checked_copies'],observed_imported_identities=row['identities'],
            observed_cpu_vram_writes=video['cpu_writes'])
        if side==1:
            identities=[tuple(pair)for pair in row['identities']]
            need((side,17 if fighter=='kano'else 18)in identities and(2,18)in identities,'Actual owned P1 plus imported CPU/mirror source, no proxy')
        if fighter=='kano'and side==2:
            compact=ROOT/'audit_v641_compact_native_floor_kano_p2'
            inputs.update(check_inputs(compact,'kano',65))
            prefix=lambda text:[r for r in text.splitlines()if re.match(r'MK2_NAT_CAMPAIGN_(INPUT|HEALTH|FIGHT|STATE) ',r)]
            old=ROOT/'audit_v636_native_shadow_kano_p2'
            for path in old.rglob('*'):
                if path.is_file():inputs[str(path)]=digest(path)
            need(prefix((compact/'run.log').read_text(encoding='utf-8-sig'))==prefix((old/'run.log').read_text(encoding='utf-8-sig')),
                 'Compact observed pre-pass capture preserves the entire genuine gameplay timeline')
            saved=json.loads((compact/'ordered-pass.json').read_text(encoding='utf-8-sig'))
            need(saved['frames']==15 and all(r['vram_mismatches']==r['displayed_mismatches']==0 for r in saved['records']),
                 'Compact pre-pass method retains exact original 15-sample pixel proof')
    for name in ('verify_native_floor_arenas_v635_v3.py','inspect_natural_arena_floor_v635_v4.py',
                 'inspect_native_shadow_rows_v635.py','inspect_natural_arena_floor_v602.py',
                 'verify_native_floor_display_v602.py','verify_native_ui_flow_v635.py'):
        path=ROOT/'tools'/name;inputs[str(path)]=digest(path)
    return dict(candidate=NAME,scope='Both slots/all regular arenas, actual P1 mirror/imported CPU paths; exact saved drawing pass through display flip. All runtime capture artifacts inventoried. Unsaved inter-pass erasure/CPU writes are outside this proof. Genuine losses/paid continues, not cleared towers',
                checks='fresh recomputation'if replay else'retained detailed runtime reconstructions and matched immutable inputs',
                cases=cases,checked_inputs=inputs,samples=sum(c['samples']for c in cases.values()),
                indexed_vram_words=sum(c['samples']for c in cases.values())*512*512,
                displayed_pixels=sum(c['samples']for c in cases.values())*400*254,
                nativeShadowArenaCheckpointPassed=True,fullPortAcceptance=False,floorAcceptance=False)


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--replay',action='store_true')
    parser.add_argument('--output',type=Path)
    args=parser.parse_args();encoded=json.dumps(verify(args.replay),indent=2)
    if args.output:args.output.write_text(encoded+'\n',encoding='utf-8')
    else:print(encoded)
