"""Actual native drawing-pass execution; not desired floor geometry acceptance.

Independent indexed-VRAM reconstruction is anchored BEFORE each pass, never
at its tested flip. Actual display registers bind its output to every PNG
pixel. Earlier inter-pass erasure, P1/other arenas and stock-style geometry
remain explicitly outside this contract.
"""
import argparse
import json
import re
from pathlib import Path
import inspect_natural_arena_floor_v602_v3 as model
from verify_native_floor_display_v602 import replay
from verify_native_pit_mirrors_v602 import check_capture
from verify_native_pit_scene_v602_v4 import ROOT, rows, need, number, hexnum


def verify_contract(groups, proof, fighter):
    need(fighter in('kano','sonya'),'Actual declared imported fighter')
    events=sorted([(r['event'],kind,r)for kind in('FLOOR_PRE_FRAME','FLOOR_DMA','FLOOR_CPU','FLOOR_FLIP')for r in groups[kind]])
    need(len({e[0]for e in events})==len(events),'Unique actual native event ordering')
    pres=groups['FLOOR_PRE_FRAME']
    dmas=groups['FLOOR_DMA']
    need(len(pres)==137 and {r['frame']for r in pres}==set(range(1898,2035)),'Complete bounded original drawing passes')
    for pre in pres:
        first=next(r for r in dmas if r['frame']==pre['frame'])
        need(pre['phase']=='before_first_frame_dma'and pre['event']+1==first['event'],
             'Pre-pass state immediately precedes the first actual command, not the tested flip')
    commands=groups['FLOOR_COMMAND']
    need(len(commands)==len(dmas)and all(r['after']&0x8000 for r in commands),'Every actually triggered DMA accounted')
    for command,dma in zip(commands,dmas):
        need(command['frame']==dma['frame']and command['after']==dma['command']and
             command['at']==0x01A80010 and command['mask']==0xffff and
             command['after']==((command['before']&~command['mask'])|(command['value']&command['mask'])),
             'Actual native trigger and full register merge')
    latches={r['event']:r for r in groups['FLOOR_LATCH']if r['snapshot']==r['flip_frame']}
    need(len(proof['records'])==proof['frames']==15 and len(latches)==15,'Every retained actual display sample')
    need([r['frame']for r in proof['records']]==list(range(1912,2025,8)),'Fixed actual samples, no best-frame search')
    for record in proof['records']:
        latch=latches[record['event']]
        need(latch['snapshot']==record['frame']and record['arena']==0,'Actual P2 Dead Pool sample')
        need(record['vram_mismatches']==record['displayed_mismatches']==record['shadow_mismatches']==0,
             'Every reconstructed VRAM word, displayed pixel and silhouette agrees exactly')
        need(record['display_pixels']==101600 and record['shadow_pixels']>0,'Exact displayed buffer and visible imported floor silhouette')
        need(all(record['body'][slot]['pixels']>0 and record['body'][slot]['mismatches']==0 for slot in(1,2)),
             'Both actual bodies present and every visible body pixel agrees')
        need(record['body'][1]['id']==3 and record['body'][2]['id']==(17 if fighter=='kano'else 18),
             'Own-ID imported fighter against original Baraka, no proxy')
    return dict(passed=True,fighter=fighter,human_slot=2,arena=0,frames=15,
        indexed_vram_words=15*512*512,display_pixels=15*400*254,
        shadow_pixels=sum(r['shadow_pixels']for r in proof['records']),
        imported_body_pixels=sum(r['body'][2]['pixels']for r in proof['records']),
        native_body_pixels=sum(r['body'][1]['pixels']for r in proof['records']),
        records=proof['records'],fullPortAcceptance=False,floorAcceptance=False,
        interpass_erasure_proven=False,desired_grounding_proven=False,
        scope='Exact original drawing-pass DMA/foreground/imported body and projected-shadow execution from actual PRE-pass VRAM through actual native display flip. Not inter-pass erasure, desired native-style geometry/grounding, other arenas/P1 or full-game acceptance.')


def verify(folder,fighter,reference):
    folder=check_capture(folder,fighter,2)
    reference=check_capture(reference,fighter,2)
    log=(folder/'run.log').read_text(encoding='utf-8-sig')
    result=rows(log,'RESULT')
    need(len(result)==1,'One genuine terminal')
    result=result[0]
    need(number(result,'schema')==20 and number(result,'frame')==3556 and
         number(result,'reset')==number(result,'ending')==-1 and number(result,'floor_snaps')==15,
         'Exact input-only terminal, no reset/ending claim')
    replay(log,(reference/'run.log').read_text(encoding='utf-8-sig'),3556)
    observer=(folder/'input_sources/mk2ks_natural_campaign_probe_v20.lua').read_text()
    need(not re.search(r'write_u\d+|:write_|load_?state|\.value\s*=(?!=)|dofile\(',observer),'No observer guest-state writes')
    groups,*_=model.data(folder)
    proof=model.inspect(folder)
    return verify_contract(groups,proof,fighter)


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('folder',type=Path);parser.add_argument('fighter',choices=('kano','sonya'))
    parser.add_argument('reference',type=Path);args=parser.parse_args()
    print(json.dumps(verify(args.folder,args.fighter,args.reference),indent=2))
