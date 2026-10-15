"""Strict matched inputs and bounded executed native replay results, not full port.

Detailed reports are reproducible with inspect_natural_arena_floor_v635_v3.py
and inspect_native_shadow_rows_v635.py. --replay recomputes those reports before
checking them; otherwise this checks the retained outputs and launch inputs.
"""
import argparse
import hashlib
import json
import re
from pathlib import Path
from verify_native_ui_flow_v635 import ROOT,NAME,EXE,PAYLOAD
from inspect_natural_arena_floor_v635_v3 import inspect as inspect_video
from inspect_native_shadow_rows_v635 import inspect as inspect_rows


def digest(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest().upper()
def need(condition,message):
    if not condition:raise ValueError(message)


def check_inputs(folder,fighter,seconds):
    result=json.loads((folder/'result.json').read_text(encoding='utf-8-sig'))
    before=json.loads((folder/'input_hashes_before.json').read_text(encoding='utf-8-sig'))
    need((result['exit_code'],result['candidate'],result['executable_sha256'],result['payload_sha256'],
          result['player'],result['human_slot'],result['seconds'],result['assistance'])==
         (0,NAME,EXE,PAYLOAD,fighter,2,seconds,'none'),'Exact terminal current native campaign')
    need(before==result['input_hashes'],'Exact before/after campaign inputs')
    for filename,sha in before.items():
        need(digest(filename)==sha,'Changed launch/build input: '+filename)
        if Path(filename).suffix in('.lua','.ps1','.json'):
            need(digest(folder/'input_sources'/Path(filename).name)==sha,'Changed frozen observer/build source')
    observer=(folder/'input_sources/mk2ks_natural_campaign_probe_v24.lua').read_text()
    need(not re.search(r'write_u\d+|:write_|load_?state|\.value\s*=(?!=)|dofile\(',observer),'Input-only cold campaigns')
    return before


def verify(replay=False):
    cases={};inputs={}
    for fighter in('kano','sonya'):
        folder=ROOT/f'audit_v643_native_floor_{fighter}_p2'
        inputs.update(check_inputs(folder,fighter,900))
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
        video=inspect_video(folder)if replay else json.loads((folder/'ordered-pass-v3.json').read_text(encoding='utf-8-sig'))
        row=inspect_rows(folder)if replay else json.loads((folder/'row-stream.json').read_text(encoding='utf-8-sig'))
        need(video['frames']==(330 if fighter=='kano'else 279),'Exact retained fixed sample count')
        need(all(r['vram_mismatches']==r['displayed_mismatches']==r['shadow_mismatches']==0 for r in video['records']),
             'Every retained actual VRAM word/display pixel/shadow pixel agrees exactly')
        need({r['arena']for r in video['records']}==actual_arenas,'Actual raster coverage equals native arena observations')
        need(row['rowStreamVerified']and not row['failures']and not row['oversized_rows'],'Every imported component/native row stream verified')
        cases[fighter]=dict(terminal=final[0],actual_arenas=sorted(actual_arenas),samples=video['frames'],
            shadow_visible_samples=sum(r['shadow_pixels']>0 for r in video['records']),
            imported_body_pixels=sum(r['body']['2']['pixels']for r in video['records']),
            shadow_pixels=sum(r['shadow_pixels']for r in video['records']),
            components=row['components'],native_shadow_copies=row['checked_copies'])
        if fighter=='kano':
            compact=ROOT/'audit_v641_compact_native_floor_kano_p2'
            inputs.update(check_inputs(compact,'kano',65))
            prefix=lambda text:[r for r in text.splitlines()if re.match(r'MK2_NAT_CAMPAIGN_(INPUT|HEALTH|FIGHT|STATE) ',r)]
            old=ROOT/'audit_v636_native_shadow_kano_p2'
            need(prefix((compact/'run.log').read_text(encoding='utf-8-sig'))==prefix((old/'run.log').read_text(encoding='utf-8-sig')),
                 'Compact observed pre-pass capture preserves the entire genuine gameplay timeline')
            saved=json.loads((compact/'ordered-pass.json').read_text(encoding='utf-8-sig'))
            need(saved['frames']==15 and all(r['vram_mismatches']==r['displayed_mismatches']==0 for r in saved['records']),
                 'Compact pre-pass method retains exact original 15-sample pixel proof')
    return dict(candidate=NAME,scope='Executed fixed P2 all-regular-arena native drawing passes and shadow streams; genuine losses/paid continues, not cleared towers',
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
