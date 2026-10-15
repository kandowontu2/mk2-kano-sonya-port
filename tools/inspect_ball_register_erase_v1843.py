"""Uninterrupted VRAM proof including original native shift-register transfers.

Only the first base is an anchor. Every subsequent pre-pass/flip is a target.
Shift data must come from a real preceding native VRAM load; FILL addresses
come from original B2/B3/B4/B7 and actual CPU conversion state, not screenshots.
This is a bounded rendering check, not universal game/art/audio acceptance.
"""
import argparse,hashlib,json,struct
from pathlib import Path
import numpy as np
import inspect_secondary_display_v1231 as raster
import verify_ball_register_source_v1837 as current
raster.HEX|={'world','camera','display','parent_main','native_actor_owner','victim','victim_main',
             'dest','native_offset','pitch','shape','status','raster_control','psize','convdp_io','clipLow','clipHigh'}
SOURCE_HASHES={
 '34010gfx.hxx':'060BEDA20F292AF57AB0048E62BC7D4A87788B01353BA6B36EFC2BAC4A80EC73',
 '34010ops.hxx':'772F372A89CBDA2D7F8E59E51540350F17EFF175B0006EEA1C69BB033D2EDB12'}

def need(ok,msg):
    if not ok:raise ValueError(msg)

def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest().upper()

def short(n):return (n&65535)-65536 if n&32768 else n&65535

def copies_for_fill(d):
    need(d['at']==0xff817130 and d['pc']==0xff817140 and d['op']==0x0fe0 and d['mask']==65535,'Exact original FILL XY instruction')
    need(not d['status']&0x02000000 and d['control']&0x0800,'First native FILL execution in shift-register mode')
    need((d['raster_control']>>6)&3==0,'This bounded native clear has no window clipping')
    need(d['psize']in(1,2,4,8,16) and d['pixelshift']==d['psize'].bit_length()-1,'Native pixel size and conversion shift agree')
    need(d['convdp']==1<<((~d['convdp_io'])&31),'Native CONVDP lookup matches original CPU source')
    bpp=d['psize'];ppw=16//bpp
    dx,dy=short(d['shape']),short(d['shape']>>16)
    need((dx,dy)==(1,127),'Only the original one-column 127-row clear is certified')
    address=(short(d['dest']>>16)*d['convdp']+(short(d['dest'])<<d['pixelshift'])+d['native_offset'])&0xffffffff
    address&=~(bpp-1)
    left=(ppw-((address&15)//bpp))&(ppw-1)
    right=((address+dx*bpp)&15)//bpp
    full=dx-left-right
    if full<0:left,right,full=dx,0,0
    else:full//=ppw
    count=int(left!=0)+full+int(right!=0)
    result=[]
    for _ in range(dy):
        for word in range(count):
            # Each original word_write callback copies all 1024 shift words.
            bitaddress=(((address>>4)+word)<<4)&0xffffffff
            result.append(bitaddress>>3)
        address=(address+d['pitch'])&0xffffffff
    need(len(result)>0 and all(0<=i and i+1024<=512*512 for i in result),'Native shift callback destination range')
    return result

def inspect(folder):
    folder=Path(folder);pins={}
    manifest=json.loads((folder/'result.json').read_text(encoding='utf-8-sig'))
    before=json.loads((folder/'input_hashes_before.json').read_text(encoding='utf-8-sig'))
    need(manifest['exit_code']==0 and manifest['candidate']==current.NAME and manifest['assistance']=='none'and manifest['cheats_enabled']is False,'Unassisted terminal current capture')
    need(before==manifest['input_hashes'],'Executed input manifest matches')
    for p,h in before.items():need(sha(p)==h,'Changed executed source '+p);pins[p]=h
    for name,h in SOURCE_HASHES.items():
        path=current.ROOT/'mame-mkp/src/devices/cpu/tms34010'/name
        need(sha(path)==h and any(Path(p).resolve()==path.resolve() and value==h for p,value in before.items()),'Bound actual unchanged native transfer implementation '+name)
    guest,_,_=current.expected();need((folder/'guest_maincpu.bin').read_bytes()==guest,'All initialized current guest bytes match independent source reconstruction')
    groups,buffers,_,_,owners=raster.data(folder)
    replay=raster.Replay(folder,groups,buffers,owners)
    shift_data={r['ref']:(folder/r['file']).read_bytes()for r in groups['FLOOR_SHIFT_DATA']}
    need(len(shift_data)==len(groups['FLOOR_SHIFT_DATA'])and all(len(raw)==2048 for raw in shift_data.values()),'Unique complete native shift streams')
    events=sorted([(kind,row)for kind in('FLOOR_PRE_FRAME','FLOOR_DMA','FLOOR_CPU','FLOOR_FLIP','FLOOR_SHIFT_LOAD','FLOOR_SHIFT_FILL','FLOOR_SHIFT')for row in groups[kind]],key=lambda item:item[1]['event'])
    need(len({r['event']for _,r in events})==len(events),'Unique original event ordering')
    latches={r['event']:r for r in groups['FLOOR_LATCH']if r['flip_frame']==r['snapshot']}
    checked_pres=checked_flips=loads=fills=transfers=direct=0;shift=None;records=[]
    for kind,row in events:
        if replay.epoch!=row['epoch']:replay.begin(row['epoch'])
        if row['event']<=replay.last_event:
            need(kind=='FLOOR_FLIP'and row['event']==replay.last_event and row['event']not in latches,'Only the initial pre-base flip may precede the base')
            continue
        need(row['event']>replay.last_event,'Strict chronological operations')
        replay.last_event=row['event']
        if kind in('FLOOR_PRE_FRAME','FLOOR_FLIP'):
            if kind=='FLOOR_FLIP'and row['event']not in latches:continue
            target=row if kind=='FLOOR_PRE_FRAME'else latches[row['event']]
            actual=np.fromfile(folder/target['file'],dtype='<u2').reshape(512,512)
            mismatch=replay.words!=actual
            if mismatch.any():
                y,x=np.where(mismatch)
                return dict(passed=False,failureKind=kind,frame=row['frame'],event=row['event'],mismatchCount=int(mismatch.sum()),
                  firstDifferences=[dict(x=int(xx),y=int(yy),model=int(replay.words[yy,xx]),actual=int(actual[yy,xx]))for yy,xx in zip(y[:16],x[:16])],
                  exactPriorPreBuffers=checked_pres,exactPriorFlips=checked_flips,shiftLoads=loads,shiftFills=fills,shiftTransfers=transfers,
                  laterBuffersUsedAsAnchors=False,fullPortAcceptance=False)
            checked_pres+=kind=='FLOOR_PRE_FRAME';checked_flips+=kind=='FLOOR_FLIP'
            records.append(dict(kind=kind,frame=row['frame'],event=row['event'],exactWords=512*512))
        elif kind=='FLOOR_SHIFT_LOAD':
            need(row['at']==0xff817080 and row['pc']==0xff817090 and row['op']==0xfa52 and row['mask']==65535 and row['control']&0x0800,'Original PIXT *B2,B2 native source load')
            need(row['index']==row['address']>>3 and row['address']==0x1fe000,'Original source template address')
            actual=shift_data[row['ref']];expected=replay.words.ravel()[row['index']:row['index']+1024].astype('<u2').tobytes()
            need(actual==expected,'Shift stream equals prior continuously modeled native VRAM, not a later screenshot')
            shift=actual;loads+=1
        elif kind in('FLOOR_SHIFT_FILL','FLOOR_SHIFT'):
            need(shift is not None and shift_data[row['ref']]==shift,'Store uses its actual original preceding source load')
            if kind=='FLOOR_SHIFT_FILL':indices=copies_for_fill(row);fills+=1
            else:
                need(row['at']==0xff816380 and row['pc']==0xff816390 and row['op']==0xf800 and row['mask']==65535 and row['control']&0x0800,'Original PIXT A0,*A0 shift store')
                need(row['index']==row['address']>>3 and 0<=row['index']<=512*512-1024,'Direct original shift destination')
                indices=[row['index']];direct+=1
            values=np.frombuffer(shift,dtype='<u2')
            for index in indices:
                replay.words.ravel()[index:index+1024]=values
                replay.body.ravel()[index:index+1024]=0;replay.shadow.ravel()[index:index+1024]=False
            transfers+=len(indices)
        elif kind=='FLOOR_DMA':replay.dma(row)
        elif kind=='FLOOR_CPU':replay.cpu(row)
    need(checked_pres==len(groups['FLOOR_PRE_FRAME'])and checked_flips==len(latches)>0 and loads==fills>0,'Every target and observed original clear accounted')
    for path in folder.rglob('*'):
        if path.is_file():pins[str(path)]=sha(path)
    pins[str(Path(__file__))]=sha(__file__)
    return dict(passed=True,continuousExactPreBuffers=checked_pres,continuousExactFlips=checked_flips,shiftLoads=loads,shiftFills=fills,
                nativeShiftTransfers=transfers,directShiftStores=direct,oneInitialBaseOnly=True,laterBuffersUsedAsAnchors=False,
                guestWrites=False,records=records,inputHashes=pins,fullPortAcceptance=False,scope=__doc__)

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('folder',type=Path);parser.add_argument('--output',type=Path,required=True);args=parser.parse_args()
    need(not args.output.exists(),'Never overwrite evidence')
    try:report=inspect(args.folder)
    except Exception as error:report=dict(passed=False,error=repr(error),laterBuffersUsedAsAnchors=False,fullPortAcceptance=False)
    args.output.mkdir();(args.output/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items()if k not in('records','inputHashes')},indent=2),flush=True)
    raise SystemExit(0 if report['passed']else 1)
