"""Original four standard UI predicates plus actual confirmed native layering."""
import json,re
from pathlib import Path
import capture_native_selector_layers_ui_ram as capture
import qualify_native_anchor_ui_cases as previous
import native_process_census_v6647 as census

ROOT=capture.ROOT
OUT=ROOT/'audit_native_selector_layers_ui_checked'
need,sha,digest=capture.original.need,capture.original.sha,capture.original.digest
BASE_CASES=previous.CASES

def verify(ram):
    need(not OUT.exists() and not census.census(),'Fresh finite original terminal UI proof')
    expected={c+'_confirm96'for c in BASE_CASES}|{c+'_confirm370'for c in BASE_CASES[:2]}
    need(set(ram['cases'])==expected,'All four standard and both delayed native cases')
    pins=dict(ram['pins']);accepted={};delayed={};faults=[];layering={};cleanup={}
    for case in sorted(expected):
        held=ram['cases'][case];folder=capture.OUT/case
        disk=json.loads((folder/'report.json').read_text())
        need(held['process'].poll()==0 and disk==held['report'] and disk['nativeExit']==0 and
             disk['actualNativeIdentity']==held['identity'] and not(folder/'stderr.log').read_text(),
             'Same actual native handle terminal and untouched captured metadata')
        need(disk['actualInitializedWindowHashes']=={k:digest(v)for k,v in ram['wanted'].items()},'All full actual initialized windows in THIS game')
        is_delayed=case.endswith('370');rows=previous.assess(disk['nativeControllerResults'],is_delayed)
        (delayed if is_delayed else accepted)[case]=rows
        if not is_delayed:
            for tag,key in [('MK2KS_EXIT_RESULT','identity_errors'),('MK2KS_EXIT_RESULT','leaks'),
                            ('MK2KS_EXIT_RESULT','name_errors'),('MK2KS_HUD_SHADOW_RESULT','errors'),
                            ('MK2KS_SELECTION_RESULT','p2_identity_errors'),('MK2KS_NATIVE_RESULT','roster_errors'),
                            ('MK2KS_STABILITY','stalled_frames'),('MK2KS_STABILITY','trap_frames')]:
                changed=[]
                for line in disk['nativeControllerResults']:
                    if line.startswith(tag+' '):
                        line,count=re.subn(r'\b'+key+r'=0\b',key+'=1',line);need(count==1,'Unique original field mutation')
                    changed.append(line)
                try:previous.assess(changed)
                except ValueError as error:faults.append(dict(case=case,tag=tag,field=key,rejectedBy=str(error)))
                else:raise ValueError('Actual altered native UI failure accepted')
        frames=held['images'];need(len(frames)==len(disk['actualNativeRasters']) and 40<=len(frames)<=80,'Every actual native raster retained')
        for frame,record in zip(frames,disk['actualNativeRasters']):
            need(frame['header']==record['header'] and digest(frame['raw'])==frame['SHA256']==record['SHA256'] and
                 frame['image'].tobytes()==capture.original.Image.frombytes('RGB',(400,254),frame['raw'],'raw','BGRX').tobytes(),
                 'Whole original native BGRX and exact RGB decoding')
        depth={};completed={}
        for line in held['text']:
            if line.startswith('MK2_ANCHOR_UI_DEPTH '):
                row=previous.fields(line);depth.setdefault(int(row['seq']),[]).append(row)
            elif line.startswith('MK2_ANCHOR_UI_DEPTH_COMPLETE '):
                row=previous.fields(line);index=int(row['seq'])
                need(index not in completed and row['writes']=='0'and row['assistance']=='none','One explicit complete native list receipt per snapshot')
                completed[index]=row;depth.setdefault(index,[])
        need(set(depth)==set(completed)==set(range(len(frames))) and
             all(int(completed[i]['count'])==len(depth[i]) and completed[i]['frame']==frames[i]['header']['frame']for i in depth),
             'Every main render list complete, including explicit empty transition lists')
        exit_frame=int(rows['MK2KS_EXIT_RESULT']['exit']);clean=[];number_observations=0
        for index,frame in enumerate(frames):
            objects=depth[index];need(all(r['writes']=='0'and r['assistance']=='none'for r in objects),'Passive native render-list observation only')
            photos=[r for r in objects if r['descriptor']in('FFFF2800','FFFF2900')]
            if int(frame['header']['frame'])>=exit_frame:
                need(not photos,'Native added CSS photos absent from actual ladder/match/finish/win render lists')
                clean.append(dict(header=frame['header'],SHA256=frame['SHA256']))
            elif frame['header']['label']!='css_initial':
                need(len(photos)==2 and all(r['z']=='00000051'for r in photos),'Both own native photos at actual depth51h throughout CSS')
                numbers=[r for r in objects if r['descriptor']in('FFC09B30','FFC09BA0')]
                need(all(r['z']=='00000052'for r in numbers),'Every existing native player marker above both own photos and bodies; confirmed markers may retire normally')
                number_observations+=len(numbers)
                for p in photos:
                    need(all(int(body['order'])<int(p['order'])for body in objects if body['id']in('0011','0012')),'Actual sorted owned photos rendered after the owned previews')
        need(len(clean)>=8 and number_observations>0,'Multiple actual post-CSS transition/ladder/gameplay lists and real native player markers inspected')
        cleanup[case]=clean
        if is_delayed:
            left=20 if case.startswith('kano')else 320
            baseline=frames[0]['image']
            points=[(x,y)for y in range(26,91)for x in range(left+6,left+56)if not(left+20<=x<=left+45 and 29<=y<=86)]
            reference=bytes(c for xy in points for c in baseline.getpixel(xy))
            samples=[(i,f)for i,f in enumerate(frames)if f['header']['label']in('highlight','highlight_blink','cursor_trace_long') and int(f['header']['frame'])<exit_frame]
            need(len(samples)>=24,'All three observed pre/postconfirmation native blink windows retained')
            for index,frame in samples:
                need(bytes(c for xy in points for c in frame['image'].getpixel(xy))==reference,'No confirmed preview overlays or shifts ANY protected own portrait pixel')
            layering[case]=dict(actualProtectedPhotoPixels=len(points),actualFrames=[dict(index=i,header=f['header'],SHA256=f['SHA256'])for i,f in samples])
        for p in (folder/'report.json',folder/'process.json',folder/'run.log.gz'):pins[str(p.resolve())]=sha(p)
    need(len(accepted)==4 and len(delayed)==2 and len(faults)==32 and len(layering)==2,'All finite standard/confirmed gates and32 mutations')
    for p in (Path(__file__),Path(capture.__file__),Path(previous.__file__),ROOT/'audit_native_selector_layers_startup/report.json'):pins[str(p.resolve())]=sha(p)
    need(all(sha(p)==h for p,h in pins.items()) and not census.census(),'Every frozen input intact; all original native games terminal')
    report=dict(passed=True,finiteFourOriginalNativeUIControllerGatesAccepted=True,
        finiteConfirmedPhotoPixelOcclusionAndNativeNumberLayeringAccepted=True,actualStandardResults=accepted,
        actualDelayedTimingFailuresPreserved=delayed,actualFaultsRejected=faults,actualConfirmedPortraitPixels=layering,
        actualNativePhotoTeardownObservations=cleanup,nativePhotoObjectsAbsentAcrossObservedTransitionLadderMatchFinishWin=True,
        originalNativeRastersAwaitHumanReview=True,completeLadderRasterCleanupAccepted=False,
        fullNavigationGraphAccepted=False,fullGroundShadowMatrixAccepted=False,allMovesAccepted=False,audioAccepted=False,
        finishersAccepted=False,fullTowerAccepted=False,fullPortAcceptance=False,inputHashes=pins,
        newBuilds=0,newROMCopies=0,newRawMedia=0,newZIPs=0,publicPlayableChanged=False,goalStatus='active')
    OUT.mkdir();(OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    ram['finiteLayerUIReport']=report
    print(json.dumps(dict(passed=True,standardCases=4,confirmedCases=2,actualFaultsRejected=32,fullPortAcceptance=False)),flush=True)
    return report
