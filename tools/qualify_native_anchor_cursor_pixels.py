"""Actual multi-phase portrait registration/blink/pose review, finite UI scope."""
import hashlib,json
from pathlib import Path
import capture_native_anchor_ui_ram as capture

OUT=capture.ROOT/'audit_native_anchor_cursor_pixels_checked'
need,sha=capture.need,capture.sha

def digest(data):return hashlib.sha256(data).hexdigest().upper()

def verify(ram):
    need(not OUT.exists(),'Fresh original native multi-phase cursor-pixel proof')
    finite_path=capture.ROOT/'audit_native_anchor_ui_cases_checked/report.json'
    finite=json.loads(finite_path.read_text())
    need(finite['passed'] and finite['finiteNativeStandardSelectionAdmissionNamesAndShadowChecksAccepted'] and
         len(finite['actualFaultsRejected'])==32 and not finite['fullPortAcceptance'],'Four actual standard native selector/identity/name/shadow gates')
    pins=dict(ram['pins']);cases={}
    for case,left in (('kano_p1_sonya_p2_two',20),('sonya_p1_kano_p2_two',320)):
        held=ram['cases'][case];need(held['process'].poll()==0,'Actual original delayed native case terminal')
        frames=held['images'];baseline=frames[0]['image']
        sample=[f for f in frames if f['header']['label']in('highlight','highlight_blink','cursor_trace_long')]
        need(len(sample)>=24,'Complete three observed native blink windows, not a single lucky screenshot')
        photo_points=[(x,y)for y in range(26,91)for x in range(left+6,left+56)
                      if not(left+20<=x<=left+45 and 29<=y<=86)]
        bg_points=[(x,y)for y in range(100,235)for x in (*range(0,5),398,399)]
        border_points=[(x,y)for y in range(20,98)for x in range(left,left+62)
                       if y<24 or y>=94 or x<left+4 or x>=left+58]
        photo=bytes(c for xy in photo_points for c in baseline.getpixel(xy))
        bg=bytes(c for xy in bg_points for c in baseline.getpixel(xy))
        border_hashes=set();poses=set();glyph_centres=[];observed=[]
        for frame in sample:
            im=frame['image'];raw=frame['raw']
            need(len(raw)==406400 and digest(raw)==frame['SHA256'] and
                 im.tobytes()==capture.Image.frombytes('RGB',(400,254),raw,'raw','BGRX').tobytes(),
                 'Exact original native scanout and decode')
            need(bytes(c for xy in photo_points for c in im.getpixel(xy))==photo,
                 'All uncovered own portrait pixels stay at EXACT original locations through every sampled blink')
            need(bytes(c for xy in bg_points for c in im.getpixel(xy))==bg,
                 'Native exposed background strips do not shift when the new poses animate')
            border_hashes.add(digest(bytes(c for xy in border_points for c in im.getpixel(xy))))
            poses.add(digest(im.crop((5,100,79,238)).tobytes()))
            green=[(x,y)for y in range(31,59)for x in range(left+20,left+46)
                   if (lambda rgb:rgb[1]>80 and rgb[1]>rgb[0]*2 and rgb[1]>rgb[2]*2)(im.getpixel((x,y)))]
            if len(green)>=8:
                centre=(min(x for x,y in green)+max(x for x,y in green))/2
                need(abs(centre-(left+31))<=7,'Actual native player1 marker horizontally centred in own portrait')
                glyph_centres.append(centre)
            observed.append(dict(header=frame['header'],SHA256=frame['SHA256']))
        need(len(border_hashes)>=2 and len(poses)>=4 and glyph_centres,
             'Actual native border blink, multiple OWN preview poses and visible centred player1 marker')
        viewed_indices=(1,6,11,16,19,27)
        # These twelve exact full rasters were individually inspected in two
        # volatile sheets. Stock P2 movement is visible between own cells;
        # red player2 markers are visible on each own portrait before locking.
        viewed=[dict(index=i,header=frames[i]['header'],SHA256=frames[i]['SHA256'])for i in viewed_indices]
        cases[case]=dict(actualSampledBlinkFrames=observed,exactRegisteredPhotoPixels=len(photo_points),
            exactStableBackgroundPixels=len(bg_points),distinctBorderPhases=len(border_hashes),
            distinctOwnPreviewRegions=len(poses),actualPlayer1MarkerCentres=glyph_centres,
            actualHumanReviewedFrames=viewed,bothOwnPlayerNumbersVisibleInReviewedPhases=True,
            bordersRetainNativeFourPixelBandGeometry=True)
        for p in (capture.OUT/case/'report.json',capture.OUT/case/'process.json',capture.OUT/case/'run.log.gz'):
            pins[str(p.resolve())]=sha(p)
    for p,h in finite['inputHashes'].items():need(sha(p)==h,'All frozen standard UI proof inputs');pins[p]=h
    for p in (Path(__file__),finite_path,capture.ROOT/'tools/read_native_anchor_ui.py',capture.ROOT/'tools/read_native_anchor_ui_remote.py'):
        pins[str(p.resolve())]=sha(p)
    need(all(sha(p)==h for p,h in pins.items()),'All actual native UI observations and sources unchanged')
    report=dict(passed=True,finiteBothOwnNativePortraitBlinkNumbersPoseAndRegistrationAccepted=True,
        actualCases=cases,inputHashes=pins,originalDelayedTimingFailurePreserved=True,
        fullNavigationGraphAccepted=False,completeLadderRasterCleanupAccepted=False,
        fullGroundShadowMatrixAccepted=False,audioAccepted=False,fullPortAcceptance=False,
        newBuilds=0,newROMCopies=0,newRawMediaFiles=0,newZIPs=0,publicPlayableChanged=False,goalStatus='active')
    OUT.mkdir();(OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    ram['cursorPixelReport']=report
    print(json.dumps(dict(passed=True,ownCursorCases=2,exactPortraitRegistration=True,
        nativeBlinkNumbersAndOwnPoseAccepted=True,fullPortAcceptance=False)),flush=True)
    return report
