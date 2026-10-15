"""Seal the twelve individually viewed current native UI rasters, no replay."""
import hashlib
import json
from pathlib import Path
import capture_native_kano_laser_audio as current

def seal(cases):
    root=current.ROOT
    out=root/'audit_native_kano_laser_ui_visual_review'
    current.need(not out.exists(),'Fresh immutable visual review')
    report_path=root/'audit_native_kano_laser_ui_checked/report.json'
    report=json.loads(report_path.read_text())
    current.need(report['passed'] and report['originalStatePixelFaultMethods']==46 and
                 report['currentBothSlotSelectionLadderFirstMatchPixelsAccepted'] and
                 report['candidate']==current.NAME,'Whole current four-case state/pixel gate')
    current.need(all(current.sha(p)==h for p,h in report['inputHashes'].items()),'Actual executed inputs and terminals unchanged')
    records=[]
    current.need(set(cases)=={'kano_p1','sonya_p1','kano_p2','sonya_p2'},'All four original native captures')
    for key,(folder,text,images) in cases.items():
        for frame,phase in ((986,'selection'),(1288,'ladder'),(1874,'first_match')):
            name=f'ui_{frame:04d}.png'
            pixels=images[name]
            current.need(pixels.shape==(254,400,3),'Actual unscaled original native raster')
            records.append(dict(case=key,frame=frame,phase=phase,
                nativeRGBSHA256=hashlib.sha256(pixels.tobytes()).hexdigest().upper(),
                individuallyViewed=True))
    out.mkdir()
    value=dict(passed=True,candidate=current.NAME,sourceReportSHA256=current.sha(report_path),
        sampledNativeRasters=records,allOriginalStatePixelFaultMethods=46,
        selectionAndLadderFirstMatchAcceptance=True,
        observations=['Dedicated top-row portraits, native colored border/player number and own preview poses',
                      'No persistent selection poses/avatars on battle plan; own ladder portrait retained naturally',
                      'Actual Kano/Sonya first-match identities and MK2-style lifebar names/shadows'],
        requirements=['selection','transition','identity','names','human_moves','cpu_moves','ordinary_combat',
                      'ground_shadows','audio','finishers_victims','stage_finishers','campaign_cinematics','cmd_release','storage'],
        remainingGroups=['startup_audio_full_UI_ground','broader_CPU_projectile_arena_shadow_audio',
                         'stage_reselect_rejoin_postending','Pit_Tomb_stock_victims_sound_priority',
                         'secret_morph_cinematic','combined_acceptance_CMD_finished_ZIP'],
        allFloorShadowStatesAccepted=False,fullVisualTimelineAccepted=False,fullLaddersAccepted=False,
        allCinematicsAccepted=False,fullPortAcceptance=False,publicPlayableChanged=False,
        newBuilds=0,newROMCopies=0,newRawMedia=0,newZIPs=0,goalStatus='active')
    (out/'report.json').write_text(json.dumps(value,indent=2)+'\n')
    print(json.dumps(dict(passed=True,individuallyViewedNativeRasters=len(records),fullPortAcceptance=False)),flush=True)
    return value
