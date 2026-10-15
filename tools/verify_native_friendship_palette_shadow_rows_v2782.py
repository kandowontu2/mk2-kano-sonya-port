"""Source-bound native shadow rows/black pen in four palette-candidate scenes.
Bind both-slot source-perfect drawing and uninterrupted erasure first. Check
all original signed row scans and actual native callback owners, not just
first/last rows. This is one arena/cross-character victim pair, not all-port
shadow, absolute grounding, audio or finisher acceptance.
"""
import json,struct,traceback
from pathlib import Path
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
import verify_native_friendship_palette_assembly_v2750 as assembly
import verify_current_friendship_shadow_rows_v2720 as rows
import inspect_native_friendship_palette_render_v2774 as render

ROOT=assembly.ROOT
OUT=ROOT/'audit_v2783_native_friendship_palette_shadow_rows_checked'
need=rows.need

def verify():
    guest,_,payload,*_=assembly.expected()
    pins=assembly.source_check();cases={}
    def pin(path,wanted=None):
        path=str(path)
        if path in pins:
            need(wanted is None or pins[path]==wanted,'Consistent candidate row dependency '+path);return
        actual=assembly.sha(path);need(wanted is None or actual==wanted,'Immutable candidate row dependency '+path);pins[path]=actual
    image=rows.native.graphics.graphics(pins)
    for fighter in ('kano','sonya'):
        for side in (1,2):
            folder=ROOT/(f'audit_v2756_native_kano_friendship_palette_p{side}' if fighter=='kano' else f'audit_v2760_native_sonya_friendship_palette_p{side}')
            report_path=ROOT/(f'audit_v2767_native_kano_friendship_palette_p{side}_render_diagnostic/report.json' if fighter=='kano' else f'audit_v2775_native_sonya_friendship_palette_p{side}_render_diagnostic/report.json')
            proof=json.loads(report_path.read_text());pin(report_path)
            need(proof['passed'] and proof['diagnosticCompleted'] and proof['wholeActualGuestAndPayloadReconstructed'] and
                 proof['allActualGraphicsBuffersROMBound'] and proof['actualConsecutiveScanouts']==1600 and
                 proof['diagnostics']['drawing']['passed'] and proof['diagnostics']['drawing']['frames']==1537,
                 'Actual newly built source-perfect four-scene drawing acceptance')
            for file,wanted in proof['inputHashes'].items():
                need(file not in pins or pins[file]==wanted,'Consistent exact render dependency '+file);pins[file]=wanted
            erasure=proof['diagnostics']['continuousErasure']
            if fighter=='kano':
                erase_path=ROOT/f'audit_v2780_native_kano_friendship_palette_p{side}_erase_diagnostic/report.json'
                erasure=json.loads(erase_path.read_text());pin(erase_path)
                for file,wanted in erasure['inputHashes'].items():
                    need(file not in pins or pins[file]==wanted,'Consistent exact erasure dependency '+file);pins[file]=wanted
            need(erasure['passed'] and erasure['oneInitialBaseOnly'] and not erasure['laterBuffersUsedAsAnchors'] and
                 erasure['continuousExactPreBuffers']==erasure['continuousExactFlips']==1537,
                 'Every actual inter-pass write and scene erasure independently exact')
            need((folder/'guest_maincpu.bin').read_bytes()==guest,'Whole actual candidate guest independently reconstructed')
            groups,*_=render.raster.data(folder)
            result=rows.rows_checked(groups,image,payload,guest,proof['control'],side)
            first=groups['SHADOW_COMPONENT'][0];event=first['event']
            dma_index=next(i for i,row in enumerate(groups['FLOOR_DMA']) if row['event']==event)
            outcomes=[]
            mutations=[('missing_actual_intermediate_copy','drop',None,'Every actual native shadow copy'),
                       ('wrong_intermediate_source','source',0,'Every actual intermediate source'),
                       ('wrong_intermediate_caller','pc',0xff801590,'Every actual native shadow copy'),
                       ('wrong_shadow_pen','color',14,'Every actual intermediate source'),
                       ('wrong_shadow_xy','y',(groups['FLOOR_DMA'][dma_index]['y']+1)&511,'Every actual intermediate source'),
                       ('wrong_original_cached_source','first_source',0,'All actual shadow cache words')]
            for name,field,value,expected in mutations:
                changed=defaultdict(list,{tag:list(records) for tag,records in groups.items()})
                changed['SHADOW_COMPONENT'][0]=dict(changed['SHADOW_COMPONENT'][0])
                changed['FLOOR_DMA'][dma_index]=dict(changed['FLOOR_DMA'][dma_index])
                if field=='drop':changed['SHADOW_COMPONENT'].pop(0)
                elif field=='first_source':changed['SHADOW_COMPONENT'][0][field]=value
                else:changed['FLOOR_DMA'][dma_index][field]=value
                need(changed!=groups,'Non-vacuous actual native row corruption')
                try:rows.rows_checked(changed,image,payload,guest,proof['control'],side)
                except ValueError as error:
                    need(expected in str(error),'Exact actual row invariant '+name)
                    outcomes.append(dict(name=name,rejectedBy=str(error)))
                else:raise ValueError('Corrupt actual native shadow accepted '+name)
            need(rows.rows_checked(groups,image,payload,guest,proof['control'],side)==result,
                 'Final untouched complete native row-sequence control')
            for display in groups['FLOOR_DISPLAY']:
                palette=(folder/display['palette_file']).read_bytes()
                need(struct.unpack_from('<H',palette,15*2)[0]&0x7fff==0,
                     'Actual native override pen fifteen remains black in every complete scanout palette')
            cases[f'{fighter}_p{side}']=dict(**result,sourcePerfectScanouts=1600,exactNativeDrawingPasses=1537,
                exactContinuousErasurePasses=1537,actualNativeBlackPalettePenConfirmed=True,
                rejectedSpecificCounterexamples=outcomes,absoluteShadowGeometryAccepted=False)
            print(f'{fighter}_p{side}: exact native rows, black pen and six actual corruptions checked',flush=True)
    pin(__file__);rows.native.scene.launch.module_pins(pins)
    print('Revalidating deduplicated actual candidate render/source graph:',len(pins),flush=True)
    with ThreadPoolExecutor(max_workers=4) as pool:
        for (path,wanted),actual in zip(pins.items(),pool.map(assembly.sha,pins)):
            need(wanted==actual,'Actual candidate row/source dependency changed '+path)
    return dict(passed=True,candidate=assembly.NAME,cases=cases,actualConsecutiveScanouts=6400,
                actualBoundPixels=6400*400*254,exactNativeDrawingAndContinuousErasurePasses=6148,
                rejectedActualShadowCounterexamples=24,sourceDerivedNativeShadowRowsAndBlackPenAccepted=True,
                gameChanged=True,allArenaGroundingAndShadowAcceptance=False,completeSceneRasterShadowAudioAccepted=False,
                fullFinisherAcceptance=False,fullPortAcceptance=False,inputHashes=pins,scope=__doc__)

if __name__=='__main__':
    need(not OUT.exists(),'Immutable actual palette candidate shadow proof')
    try:report=verify()
    except Exception as error:report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
    OUT.mkdir();(OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({key:value for key,value in report.items() if key not in ('inputHashes','cases')},indent=2),flush=True)
    raise SystemExit(0 if report['passed'] else 1)
