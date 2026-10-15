"""Exact original saved-pass replay with native visibility observations; not acceptance."""
import argparse,bisect,json,re
from pathlib import Path
from collections import defaultdict
import verify_native_arena_geometry_v1583 as arena

campaign=arena.campaign;native=arena.native

def inspect(folder):
    pins={};campaign.matched(folder,pins)
    launch=json.loads((folder/'result.json').read_text(encoding='utf-8-sig'))
    assert launch['exit_code']==0 and launch['assistance']=='none'
    side=launch['human_slot'];fighter=launch['player'];log=folder/'run.log';original=campaign.digest(log)
    groups=defaultdict(list)
    keep={'FLOOR_PRE_FRAME','FLOOR_FLIP','FLOOR_LATCH','FLOOR_DISPLAY','FLOOR_SNAP','FLOOR_BEGIN','FLOOR_RESULT','FLOOR_GFX','FLOOR_OWNER'}
    hex_fields=native.raster.HEX|{'op','before0','before1','before','after','first_source','row'}
    str_fields=native.raster.STR|{'register'}
    def parse(line):
        row=dict(re.findall(r'(\w+)=([^\s]+)',line))
        for key,value in row.items():
            if key not in str_fields:row[key]=int(value,16 if key in hex_fields else 10)
        return row
    with log.open(encoding='utf-8-sig')as stream:
        for line in stream:
            match=re.match(r'^MK2_NAT_CAMPAIGN_(\w+) ',line)
            if match and match[1]in keep:
                campaign.drawing_scope(line,side,fighter);groups[match[1]].append(parse(line))
    pre={r['frame']:r for r in groups['FLOOR_PRE_FRAME']}
    latches=[r for r in groups['FLOOR_LATCH']if r['flip_frame']==r['snapshot']]
    windows=sorted((pre[r['snapshot']-1]['event'],r['event'])for r in latches)
    assert windows and all(a[1]<b[0]for a,b in zip(windows,windows[1:]))
    starts=[a for a,b in windows];selected=0;excluded=0
    queues=[];dispatches=[]
    selected_frames={r['snapshot']-1 for r in latches}
    with log.open(encoding='utf-8-sig')as stream:
        for line in stream:
            match=re.match(r'^MK2_NAT_CAMPAIGN_(FLOOR_CPU|FLOOR_DMA|FLOOR_QUEUE|FLOOR_QUEUE_DISPATCH) ',line)
            if not match:continue
            if match[1]in('FLOOR_QUEUE','FLOOR_QUEUE_DISPATCH'):
                frame=int(re.search(r'\bframe=(\d+)',line)[1])
                if frame in selected_frames:
                    campaign.drawing_scope(line,side,fighter)
                    (queues if match[1]=='FLOOR_QUEUE'else dispatches).append(parse(line))
                continue
            event=int(re.search(r'\bevent=(\d+)',line)[1]);i=bisect.bisect_right(starts,event)-1
            if i>=0 and event<=windows[i][1]:
                campaign.drawing_scope(line,side,fighter);groups[match[1]].append(parse(line));selected+=1
            else:excluded+=1
    buffers={r['key']:r for r in groups['FLOOR_GFX']};owners=defaultdict(list)
    for r in groups['FLOOR_OWNER']:owners[r['frame'],r['source'],r['slot']].append(r)
    def data(folder_arg):
        assert Path(folder_arg).resolve()==folder.resolve()
        return groups,buffers,None,None,owners
    # The original native inspector already restricts acceptance to these
    # exact anchored saved-pass intervals. Unsaved CPU/DMA rows are not a
    # floor/visibility acceptance here and remain untouched in the full log.
    native.raster.data=data
    report=native.raster.inspect(folder)
    failures=[]
    for r in report['records']:
        body=r['body'][side]
        if body['pixels']<=100 or body['mismatches'] or body.get('id')!={'kano':17,'sonya':18}[fighter]:
            failures.append(dict(frame=r['frame'],arena=r['arena'],file=r['file'],body=body,
                opponentBody=r['body'][3-side],wholeVRAMMismatches=r['vram_mismatches'],
                displayedMismatches=r['displayed_mismatches'],shadowMismatches=r['shadow_mismatches'],
                actualOwnQueues=[q for q in queues if q['frame']==r['frame']-1 and q['slot']==side],
                actualOwnDispatches=[q for q in dispatches if q['frame']==r['frame']-1 and q['slot']==side]))
    assert campaign.digest(log)==original
    pins[str(log.resolve())]=original
    pins[str((folder/'result.json').resolve())]=campaign.digest(folder/'result.json')
    for path in (Path(__file__),Path(native.raster.__file__),Path(arena.__file__)):
        pins[str(path.resolve())]=campaign.digest(path)
    return dict(diagnosticCompleted=True,fighter=fighter,humanSlot=side,exactSavedFrames=report['frames'],
        selectedSavedPassCPUAndDMAEvents=selected,unsavedPassEventsExcluded=excluded,
        savedPassIntervals=windows,visibilityFailures=failures,records=report['records'],
        fullPortAcceptance=False,inputHashes=pins)

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('folder',type=Path);parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args();assert not args.output.exists(),'Never overwrite evidence'
    report=inspect(args.folder);args.output.parent.mkdir(exist_ok=True);args.output.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(diagnosticCompleted=True,exactSavedFrames=report['exactSavedFrames'],
        visibilityFailures=[{k:v for k,v in r.items()if k not in('actualOwnQueues','actualOwnDispatches')}for r in report['visibilityFailures']]),indent=2),flush=True)
