"""Finite native UI gates: keep original delayed failures and whole scope open."""
import json,re
from pathlib import Path
import capture_native_anchor_ui_ram as base

OUT=base.ROOT/'audit_native_anchor_ui_cases_checked'
CASES=('kano_p1_sonya_p2_two','sonya_p1_kano_p2_two','kano_p1_stock_p2_ladder','sonya_p1_stock_p2_ladder')
need,sha=base.need,base.sha

def fields(line):return dict(re.findall(r'(\w+)=([^\s]+)',line))

def assess(lines,delayed=False):
    rows={line.split()[0]:fields(line)for line in lines}
    exit=rows['MK2KS_EXIT_RESULT'];shadow=rows['MK2KS_HUD_SHADOW_RESULT']
    selected=rows['MK2KS_SELECTION_RESULT'];native=rows['MK2KS_NATIVE_RESULT'];stable=rows['MK2KS_STABILITY']
    need(exit['fighter']in('kano','sonya') and exit['confirm']=='lp' and
         int(exit['combat'])>=1600 and int(exit['outside'])>300 and int(exit['name_checks'])>20 and
         all(exit[k]=='0'for k in ('leaks','identity_errors','name_errors')),
         'Actual admission/ordinary combat, own identity/name pixels and no portrait leakage')
    need(shadow['pass']=='true' and int(shadow['checks'])>=6 and shadow['errors']=='0' and
         selected['errors']=='0' and selected['p2_identity_errors']=='0' and int(selected['checks'])>400 and
         native['roster_errors']=='0' and int(native['hud_entries'])>=2 and
         stable['stalled_frames']==stable['trap_frames']=='0',
         'Actual native selection IDs, both HUDs, native black name shadows and advancing CPU')
    if selected['p2']=='stock':need(int(selected['ladder_entries'])>=1,'Own native ladder entry actually read')
    if delayed:
        need(exit['pass']=='false' and 400<=int(exit['exit'])-int(exit['css'])<500,
             'Preserve original failed timing limit on the deliberate370-frame confirmation; no relabeling')
    else:need(exit['pass']=='true' and 0<int(exit['exit'])-int(exit['css'])<400,'Original96-frame controller passes its unmodified full finite selector predicate')
    return rows

def verify(ram):
    need(not OUT.exists() and set(ram['cases'])==set(CASES),'Exact four original standard native cases')
    pins=dict(ram['pins']);accepted={};rejected=[];delayed_results={}
    for case in CASES:
        held=ram['cases'][case];folder=base.ROOT/'audit_native_anchor_ui_standard_ram'/case
        disk=json.loads((folder/'report.json').read_text())
        need(disk==held['report'] and held['process'].poll()==0 and disk['nativeExit']==0 and
             disk['actualNativeIdentity']==held['identity'] and not(folder/'stderr.log').read_text() and
             disk['actualInitializedWindowHashes']=={k:base.digest(v)for k,v in ram['wanted'].items()},
             'Same actual original terminal handle, source-bound windows and untouched captured report')
        need(not disk['visualSelectionAccepted'] and not disk['fullPortAcceptance'],'Transport metadata was not broader acceptance')
        rows=assess(disk['nativeControllerResults']);accepted[case]=rows
        for tag,key in [('MK2KS_EXIT_RESULT','identity_errors'),('MK2KS_EXIT_RESULT','leaks'),
                        ('MK2KS_EXIT_RESULT','name_errors'),('MK2KS_HUD_SHADOW_RESULT','errors'),
                        ('MK2KS_SELECTION_RESULT','p2_identity_errors'),('MK2KS_NATIVE_RESULT','roster_errors'),
                        ('MK2KS_STABILITY','stalled_frames'),('MK2KS_STABILITY','trap_frames')]:
            changed=[]
            for line in disk['nativeControllerResults']:
                if line.startswith(tag+' '):
                    line,count=re.subn(r'\b'+key+r'=0\b',key+'=1',line);need(count==1,'Unique actual native field mutation')
                changed.append(line)
            try:assess(changed)
            except ValueError as error:rejected.append(dict(case=case,tag=tag,field=key,rejectedBy=str(error)))
            else:raise ValueError('Altered actual native UI failure accepted')
        frames=held['images'];need(len(frames)==len(disk['actualNativeRasters'])and 40<=len(frames)<=80,'All actual bounded native frames held')
        for frame,record in zip(frames,disk['actualNativeRasters']):
            need(frame['header']==record['header'] and base.digest(frame['raw'])==frame['SHA256']==record['SHA256'] and
                 frame['image'].tobytes()==base.Image.frombytes('RGB',(400,254),frame['raw'],'raw','BGRX').tobytes(),
                 'Every exact original native raster and its RGB decoding match original captured receipt')
        delayed_folder=base.OUT/case
        delayed=json.loads((delayed_folder/'report.json').read_text())
        delayed_results[case]=assess(delayed['nativeControllerResults'],True)
        for p in (folder/'report.json',folder/'process.json',folder/'run.log.gz',delayed_folder/'report.json'):
            pins[str(p.resolve())]=sha(p)
    need(len(rejected)==32 and all(sha(p)==h for p,h in pins.items()),'All32 actual faults rejected and all inputs remain intact')
    pins[str(Path(__file__).resolve())]=sha(__file__)
    report=dict(passed=True,finiteNativeStandardSelectionAdmissionNamesAndShadowChecksAccepted=True,
        actualStandardCaseResults=accepted,deliberatelyDelayedOriginalTimingFailuresPreserved=delayed_results,
        actualFaultsRejected=rejected,inputHashes=pins,nativeRastersHeldForHumanMultiPhaseReview=True,
        multiPhaseVisualReceiptPending=True,completeLadderRasterCleanupAccepted=False,
        fullGroundShadowMatrixAccepted=False,allMovesAccepted=False,audioAccepted=False,
        finishersAccepted=False,fullTowerAccepted=False,fullPortAcceptance=False,newBuilds=0,newROMCopies=0,
        newRawMediaFiles=0,newZIPs=0,publicPlayableChanged=False,goalStatus='active')
    OUT.mkdir();(OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    ram['finiteUIReport']=report
    print(json.dumps(dict(passed=True,standardCases=4,actualFaultsRejected=32,fullPortAcceptance=False)),flush=True)
    return report
