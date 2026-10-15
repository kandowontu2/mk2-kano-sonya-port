"""Native display-buffer binding and real arena coverage, not floor acceptance.

Reads actual TMS flip/VRAM and palette captures. No best-field/page/position
search, image tolerance, assisted stage selection or state injection.
"""
import argparse
import json
import re
from pathlib import Path
import numpy as np
from PIL import Image
from verify_native_pit_scene_v602_v4 import ROOT,rows,need,number,hexnum
from verify_native_pit_mirrors_v602 import check_capture


def check_latch(image,raw,palette_raw,start,control,tap):
    need(image.shape==(254,400,3)and len(raw)==512*512*2 and len(palette_raw)==32768*4,'Exact native raster/VRAM/palette sizes')
    # Original tms340x0_device::get_display_params, followed by the T-unit
    # scanline_update. Initial row comes from the actual display-start write.
    address=start if control&0x400 else start^0xfffc
    row=(address>>4)&511
    column=(((address&0x7c)<<4)|(tap&0x3fff))*2
    column&=511
    need(row+254<=512 and column+400<=512 and start&3==0,'Nonwrapped observed native display rectangle')
    words=np.frombuffer(raw,dtype='<u2').reshape(512,512)[row:row+254,column:column+400]&0x7fff
    palette=np.frombuffer(palette_raw,dtype='<u4')
    colors=np.stack([(palette>>16)&255,(palette>>8)&255,palette&255],axis=1).astype(np.uint8)
    expected=colors[words]
    matches=int(np.count_nonzero(np.all(image==expected,axis=2)))
    need(matches==400*254,'Every screenshot pixel matches the actual newly displayed VRAM and palette')
    return dict(passed=True,row=row,column=column,pixels=matches)


def replay(log,reference,terminal):
    need(not re.search(r'\[LUA ERROR\]|fatal error|access violation|stack traceback|REENTRY',log,re.I),'No observer/emulator error')
    for tag in ('INPUT','HEALTH','FIGHT','STATE'):
        bounded=lambda text:[r for r in rows(text,tag)if number(r,'frame')<=terminal]
        need(bounded(log)==bounded(reference),'Exact actual input/health/fight/state replay: '+tag)


def verify_display(folder,reference):
    folder=check_capture(folder,'sonya',2);reference=check_capture(reference,'sonya',2)
    log=(folder/'run.log').read_text(encoding='utf-8-sig')
    result=rows(log,'RESULT');need(len(result)==1,'One complete display scout terminal')
    result=result[0]
    need(number(result,'schema')==15 and number(result,'frame')==3556 and
         number(result,'reset')==number(result,'ending')==-1 and number(result,'floor_snaps')==15,
         'Complete input-only display scout, not a tower or arena-clear claim')
    replay(log,(reference/'run.log').read_text(encoding='utf-8-sig'),number(result,'frame'))
    observer=(folder/'input_sources/mk2ks_natural_campaign_probe_v15.lua').read_text()
    need(not re.search(r'write_u\d+|:write_|load_?state|\.value\s*=(?!=)|dofile\(',observer),'No observer guest writes')
    snaps,displays,latches,flips=(rows(log,t)for t in ('FLOOR_SNAP','FLOOR_DISPLAY','FLOOR_LATCH','FLOOR_FLIP'))
    need(len(snaps)==len(displays)==15 and len(latches)==30,'Complete retained native display evidence')
    records=[]
    for snap,display in zip(snaps,displays):
        frame=number(snap,'frame')
        need(number(display,'frame')==frame and snap['phase']=='frame_done','Actual render callback association')
        matches=[r for r in latches if number(r,'snapshot')==number(r,'flip_frame')==frame]
        need(len(matches)==1,'One exact current native display-flip latch, not a chosen best buffer')
        latch=matches[0]
        need(tuple(hexnum(latch,k)for k in ('start','control','tap'))==tuple(hexnum(display,k)for k in ('start','control','tap')),
             'Latched and current actual display registers agree')
        events=[r for r in flips if number(r,'frame')==frame and hexnum(r,'value')==hexnum(latch,'start')]
        need(len(events)==1 and hexnum(events[0],'at')==0xC0000090 and hexnum(events[0],'mask')==0xFFFF and
             hexnum(events[0],'pc')==0xFF8168E0,'Actual original TMS display-start write')
        image=np.asarray(Image.open(folder/'snap'/snap['file']).convert('RGB'))
        proof=check_latch(image,(folder/latch['file']).read_bytes(),(folder/display['palette_file']).read_bytes(),
                          hexnum(latch,'start'),hexnum(latch,'control'),hexnum(latch,'tap'))
        records.append(dict(frame=frame,file=snap['file'],**proof))
    return dict(passed=True,display_latch_proven=True,frames=len(records),pixels=sum(r['pixels']for r in records),
                records=records,fullPortAcceptance=False,floorAcceptance=False,
                scope='Exact actual front-buffer/VRAM/palette binding in moving Sonya-P2 Dead Pool frames. Not desired shadow geometry, grounding, artistic or all-arena acceptance.')


def verify_coverage(folder,fighter,reference):
    folder=check_capture(folder,fighter,2);reference=check_capture(reference,fighter,2)
    log=(folder/'run.log').read_text(encoding='utf-8-sig')
    result=rows(log,'RESULT');need(len(result)==1,'One complete arena-coverage terminal')
    result=result[0]
    need(number(result,'schema')==14 and number(result,'frame')==49237 and number(result,'reset')==number(result,'ending')==-1,
         'Complete no-reset natural campaign, not a cleared tower')
    replay(log,(reference/'run.log').read_text(encoding='utf-8-sig'),number(result,'frame'))
    identity=17 if fighter=='kano'else 18
    begins=rows(log,'FLOOR_BEGIN');snaps=rows(log,'FLOOR_SNAP')
    need(len(begins)==number(result,'floor_epochs')and len(snaps)==number(result,'floor_snaps'),'All captured windows/snapshots accounted')
    need({number(r,'arena')for r in begins}=={number(r,'arena')for r in snaps}==set(range(9)),
         'Actual windows and rendered screenshots in all nine regular arenas')
    need(all(r['human']==f'{identity}:{identity}'and r['cpu']=='3:3'for r in begins),'True selected player and native Baraka CPU')
    need(all((folder/'snap'/r['file']).is_file()for r in snaps),'Each arena-window screenshot retained')
    fights=rows(log,'FIGHT')
    need([(r['frame'],r['selection'],r['human'],r['cpu'])for r in begins]==
         [(r['frame'],r['selection'],r['human'],r['cpu'])for r in fights],'Every window originates in a real own-ID fight')
    return dict(passed=True,fighter=fighter,human_slot=2,arenas=list(range(9)),epochs=len(begins),screenshots=len(snaps),
                terminal_frame=number(result,'frame'),unassisted_clear_proven=False,fullPortAcceptance=False,floorAcceptance=False,
                scope='Actual input-only nine-regular-arena coverage and unchanged entire native gameplay replay. Retained floor pixels still require independent front-buffer/foreground/geometry verification; not P1, secret arena or full tower acceptance.')


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('kind',choices=('display','coverage'));parser.add_argument('folder',type=Path)
    parser.add_argument('fighter',choices=('kano','sonya'));parser.add_argument('reference',type=Path);args=parser.parse_args()
    need(args.kind!='display'or args.fighter=='sonya','Declared actual display scout')
    proof=verify_display(args.folder,args.reference)if args.kind=='display'else verify_coverage(args.folder,args.fighter,args.reference)
    print(json.dumps(proof,indent=2))
