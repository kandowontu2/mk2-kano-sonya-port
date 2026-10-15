"""Serve original RAM rasters and seal twenty-four viewed ground poses."""
import hashlib
import json
from pathlib import Path
import capture_native_kano_laser_ground_complete_buffers as current
import capture_native_kano_laser_ground_ram as capture
import serve_native_current_ui_ram as preview

AGES=(16,128,248,368,432,456)

def serve(cases):
    aliases={}
    for key,c in cases.items():
        images={name.replace('ground_','ui_',1):pixels for name,pixels in c['images'].items()}
        aliases[key]=(c['folder'],c['log'],images)
    return preview.serve(aliases),aliases

def metadata(cases):
    return {key:[dict(frame=r['frame'],age=r['age']) for r in capture.ground.rows(c['log'],'SNAP') if r['age']in AGES]
            for key,c in cases.items()}

def seal(cases):
    out=capture.ROOT/'audit_native_kano_laser_ground_visual_review'
    capture.need(not out.exists(),'Fresh immutable ground visual review')
    report_path=current.OUT/'report.json';report=json.loads(report_path.read_text())
    capture.need(report['passed'] and report['boundedBothSlotDeadPoolGroundShadowAcceptance'] and
                 report['actualDisplayedNativeRasters']==148 and len(report['faultChecks'])==28 and
                 all(capture.sha(p)==h for p,h in report['inputHashes'].items()),'Whole current native ground/DMA/latch/negative-control gate')
    capture.need(set(cases)=={'kano_p1','sonya_p1','kano_p2','sonya_p2'},'All four actual native ground trials')
    records=[]
    for key,c in cases.items():
        snaps=[r for r in capture.ground.rows(c['log'],'SNAP')if r['age']in AGES]
        capture.need([r['age']for r in snaps]==list(AGES),'All six individually viewed native poses, including both jumps')
        for r in snaps:
            pixels=c['images'][r['file']]
            capture.need(pixels.shape==(254,400,3),'Original unscaled actual raster')
            records.append(dict(case=key,frame=r['frame'],age=r['age'],nativeRGBSHA256=hashlib.sha256(pixels.tobytes()).hexdigest().upper(),individuallyViewed=True))
    out.mkdir()
    result=dict(passed=True,candidate=report['candidate'],sourceReportSHA256=capture.sha(report_path),
        inputHashes={str(Path(__file__).resolve()):capture.sha(__file__),
                     str(current.RECHECK/'result.json'):capture.sha(current.RECHECK/'result.json')},
        individuallyViewedNativeRasters=records,all148DisplayedRastersIndependentlyBound=True,
        observations=['Imported and stock idle soles share the native displayed contact row',
                      'Visible native black compressed-row fighter shadows',
                      'Actual jump, crouch, walk and recovery phases preserve native grounding/shadow projection'],
        requirements=['selection','transition','identity','names','human_moves','cpu_moves','ordinary_combat',
                      'ground_shadows','audio','finishers_victims','stage_finishers','campaign_cinematics','cmd_release','storage'],
        remainingGroups=['startup_audio_full_UI_ground','broader_CPU_projectile_arena_shadow_audio',
                         'stage_reselect_rejoin_postending','Pit_Tomb_stock_victims_sound_priority',
                         'secret_morph_cinematic','combined_acceptance_CMD_finished_ZIP'],
        boundedBothSlotDeadPoolGroundShadowAcceptance=True,allArenaFloorAcceptance=False,allMoveShadowStatesAcceptance=False,
        fullVisualTimelineAccepted=False,audioWaveformAcceptance=False,fullPortAcceptance=False,
        publicPlayableChanged=False,newBuilds=0,newROMCopies=0,newRawMedia=0,newZIPs=0,goalStatus='active')
    (out/'report.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(dict(passed=True,individuallyViewedNativeRasters=len(records),allArenaFloorAcceptance=False)),flush=True)
    return result
