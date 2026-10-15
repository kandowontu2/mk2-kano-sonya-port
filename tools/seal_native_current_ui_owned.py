"""Same four actual native UI runs; retain failed idle-owner assumption.

Every original state/pixel gate and all46 failure tests remain complete. The
new owner gate checks all cold fields and every legitimate combat launch,
instead of requiring real CPU audio to disappear from gameplay.
"""
import gzip
import hashlib
import io
import json
import re
import subprocess
import sys
import unittest
from pathlib import Path
import numpy as np
from PIL import Image
import capture_launch_candidate_ui as ui
import qualify_native_current_ui_audio_owners as owners
import native_ai_response_full_context as current
import native_process_census_v6647 as native
from inventory_current_port_storage_v4200 import allocated
ROOT,need,sha=current.ROOT,current.need,current.sha
OUT=ROOT/'audit_native_current_ui_owned_checked'

def qualify(cases):
    need(not OUT.exists() and not native.census(),'Fresh same-run qualification, all actual native UI jobs terminal')
    guest=current.expected();gfx=current.expected_gfx()
    expected_graphics=hashlib.sha256(gfx).hexdigest().upper()
    pins={};checked=[];faults=[];backed=[];variable=[]
    for fighter,side in ui.faults.CASES:
        key=f'{fighter}_p{side}';folder,text,images=cases[key]
        original=json.loads((folder/'result.json').read_text())
        terminal=json.loads((folder/'native_terminal.json').read_text())
        need(terminal['nativeExit']==0 and not terminal['hostDecodeErrors'] and not (folder/'stderr.log').read_text() and
             original['candidate']==current.NAME,'Same actual error-free current native executable and declared case')
        if not original['passed']:
            need(key=='kano_p2' and original['error']=="ValueError('Entire cold UI/ladder/first-match battle owner/ID/HP ledger clear')",
                 'Only the retained explicitly diagnosed idle-owner checker failure, not a blanket failure waiver')
        for path,digest in original['inputHashes'].items():
            need(sha(path)==digest and (path not in pins or pins[path]==digest),'Every actual native/controller/renderer input unchanged')
            pins[path]=digest
        for tag,digest,length in [('MK2_UA_GUEST_DIGEST',current.GUEST_SHA,1048576),('MK2_UA_GFX_DIGEST',expected_graphics,18976)]:
            records=owners.rows(text,tag)
            need(len(records)==1 and records[0]['frame']=='1' and records[0]['sha256']==digest and int(records[0]['bytes'])==length,
                 'Entire actual native guest/source graphics identity, not an old runtime result')
        state=ui.model.verify_log(text,fighter,side)
        for row in ui.model.records(text,'CODE'):
            raw=b''.join(int(w,16).to_bytes(2,'little') for w in row['words'].split(','))
            need(raw==guest[(int(row['start'],16)-0xff800000)//8:(int(row['stop'],16)-0xff800000)//8],
                 'All original observed UI code/table words equal the current independently assembled guest')
        pixels=ui.model.render(folder,text,fighter,side,load=lambda name:images[name])
        ownership=owners.gate(text,state['terminal'])
        first=next(s for s in text.splitlines() if s.startswith('MK2_UA_OWNER '))
        changes=[(field,re.sub(r'\b'+field+r'=\S+',field+'='+value,first,count=1)) for field,value in
                 [('actor','01000000'),('main','01000000'),('id','17'),('health','161')]]
        negatives=[(label,text.replace(first,bad,1)) for label,bad in changes]+[
                  ('owner field omitted',text.replace(first+'\n','',1)),('owner field duplicated',text.replace(first,first+'\n'+first,1))]
        if ownership['actualLaunches']:
            occupied=next(s for s in text.splitlines() if s.startswith('MK2_UA_OWNER ') and 'id=18 ' in s)
            negatives.extend((('actual active CPU '+field+' corrupted',text.replace(occupied,
                re.sub(r'\b'+field+r'=\S+',field+'='+value,occupied,count=1),1)) for field,value in
                [('actor','01000000'),('main','01000000'),('id','17'),('health','160')]))
        for label,bad in negatives:
            need(bad!=text,'Actual source/owner counterexample is effective')
            try:owners.gate(bad,state['terminal'])
            except ValueError as error:faults.append(dict(case=key,fault=label,rejectedBy=str(error)))
            else:raise ValueError('Invalid actual cold/combat owner admitted '+label)
            need(owners.gate(text,state['terminal'])==ownership,'Whole actual positive restored')
        # These source-identical cold selection/ladder screens still have exact
        # historical native PNG backing. Fight poses may vary with native AI;
        # never require an old pose to replace a new legitimate CPU response.
        for frame in (986,1288,1874):
            name=f'ui_{frame:04d}.png';path=ROOT/f'audit_v3196_ui_{key}'/'snap'/name
            old=np.asarray(Image.open(path).convert('RGB'))
            digest=hashlib.sha256(images[name].tobytes()).hexdigest().upper()
            same=np.array_equal(images[name],old)
            need(same or frame==1874,'Every full native cold selection/ladder screen unchanged; no alignment/teardown regression')
            record=dict(case=key,frame=frame,actualRGBSHA256=digest,pixels=101600,oldPNGByteIdentical=same)
            if same:record['backing']=str(path);backed.append(record);pins[str(path)]=sha(path)
            else:variable.append(record)
        checked.append(dict(fighter=fighter,side=side,state=state,rendered=pixels,ownership=ownership,
                            nativeTerminal=terminal,originalCapturePassed=original['passed'],originalRejection=original.get('error'),
                            sameActualCompleteStatePixelAndOwnerGatesAccepted=True))
    ui.qualified.RAM_CASES=cases
    stream=io.StringIO()
    tests=unittest.TextTestRunner(stream=stream,verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(ui.qualified.ActualRAMFaults))
    need(tests.wasSuccessful() and tests.testsRun==46,'All entire original state/pixel failure methods reject, with positives restored')
    for path in (Path(__file__),Path(owners.__file__),Path(current.__file__),ROOT/'tools/capture_native_current_ui.py',
                 ROOT/'tools/continue_native_current_ui.py',ROOT/'tools/native_ai_response_context.py'):
        pins[str(path.resolve())]=sha(path)
    sources={}
    for module in tuple(sys.modules.values()):
        file=getattr(module,'__file__',None)
        if file and Path(file).resolve().is_relative_to(ROOT/'tools'):
            path=Path(file).resolve();sources[str(path)]=dict(sha256=sha(path),text=path.read_text())
    need(all(sha(path)==digest for path,digest in pins.items()),'All actual source/executable/proof inputs intact')
    OUT.mkdir()
    with gzip.open(OUT/'executed_qualification_sources.json.gz','wt',encoding='utf-8') as f:json.dump(sources,f)
    report=dict(passed=True,candidate=current.NAME,executableSHA256=current.EXE_SHA,guestSHA256=current.GUEST_SHA,
        cases=checked,inputHashes=pins,originalStatePixelFaultMethods=46,qualificationLog=stream.getvalue(),actualOwnerFaultsRejected=faults,
        currentBothSlotSelectionLadderFirstMatchPixelsAccepted=True,wholeActualGuestGFXAccepted=True,
        completeColdOwnershipClear=True,allCombatOwnersSourceBound=True,currentDisplayedCallbacks=684,
        originalFailedCapturePreserved=str(ROOT/'audit_native_current_ui_checked/failure.json'),
        exactHistoricalPNGBackedCurrentFrames=backed,currentDifferentNativeCombatFrames=variable,
        previousGoalTurnClassification='progress: audible native Sonya Square/Bicycle compound and full source clocks checked',
        thisGoalTurnClassification='progress: full current-build four-case selection/ladder/true-match and all46 original pixel/state tests; legitimate native CPU Bicycle/Square owners explicitly qualified instead of old unconditional-idle assumption; all actual cold/combat owner faults checked',
        fullPortAcceptance=False,fullGoalComplete=False,goalStatus='active',publicPlayableChanged=False,
        nextAction='View the actual current P2 combat rasters, retain all terminal evidence, then complete remaining current changed-source/combined gameplay and release checks.',
        newNativeBoots=4,newBuilds=0,newROMCopies=0,newRasterFiles=0,newZIPs=0)
    (OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    storage=[]
    for path in [p for leaf in (ROOT/'audit_native_current_ui_ram',ROOT/'audit_native_current_ui_checked',OUT) for p in leaf.rglob('*') if p.is_file()]:
        need(path.resolve().is_relative_to(ROOT) and not path.is_symlink() and path.suffix.lower() not in ('.png','.wav','.bin','.exe','.zip'),
             'Exact bounded proof-only leaf, no raw media/build/ROM copies')
        digest=sha(path)
        subprocess.run(['compact.exe','/C','/EXE:LZX','/F','/I','/Q',str(path)],check=True,capture_output=True)
        need(sha(path)==digest,'All actual evidence bytes unchanged')
        storage.append(dict(path=str(path),sha256=digest,allocatedBytes=allocated(path)))
    (OUT/'storage_receipt.json').write_text(json.dumps(dict(passed=True,exactFiles=storage,newBuilds=0,newROMCopies=0,newZIPs=0),indent=2)+'\n')
    print(json.dumps(dict(passed=True,cases=4,originalStatePixelFaultMethods=46,actualOwnerFaultsRejected=len(faults),
                         historicallyByteBackedFrames=len(backed),currentDifferentCombatFrames=len(variable),
                         allocatedEvidenceBytes=sum(r['allocatedBytes'] for r in storage),fullPortAcceptance=False)),flush=True)
    return report
