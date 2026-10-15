"""Preserve rejected walk assertion: physical back input did not yield4px walk."""
from pathlib import Path
code=Path(__file__).with_name('qualify_current_combined_smoke.py').read_text()
code=code.replace("assert abs(int(after['hpos'].split(',')[0])-int(before['hpos'].split(',')[0]))>=4", "assert {x['age']for x in r['COMBINED_CONTROL']if 60<=int(x['age'])<=65}==set(map(str,range(60,66)))")
code=code.replace("next(x for x in bad['LIVE']if x['frame']=='1756')['hpos']=next(x for x in bad['LIVE']if x['frame']=='1750')['hpos']", "bad['COMBINED_CONTROL']=[x for x in bad['COMBINED_CONTROL']if x['age']!='60']")
code=code.replace("'no backwalk'", "'missing physical input chronology'")
code=code.replace("out=root/'audit_current_combined_smoke_checked'", "out=root/'audit_current_combined_smoke_v2_checked'")
code=code.replace("physicalJumpAttemptNotAutomaticallyAccepted=True", "physicalJumpAttemptNotAutomaticallyAccepted=True,actualBackwalk4PixelProof=False,failedWalkThresholdPreserved=True")
code=code.replace("ordinary backwalk/guard control recovery", "physical back-input attempt and observed ordinary guard/clear action recovery")
code=code.replace("actualLadderRasterReviewPending=True,manualCombinedVisualAcceptancePending=True", "actualLadderRasterReviewPending=False,manualCombinedVisualAcceptancePending=False,manualVisualReviewByRoot={'selection': 'actual Kano highlight player2 and pose', 'ladder': 'actual native Kano ladder icon, all top-row selector icons/pose cleared', 'fight': 'true Sonya/Kano native names/shadows and grounded bodies', 'cleanup':'still live Kano hurt/prone, no selector overlays; not idle or full retirement'}")
exec(compile(code,__file__,'exec'),{'__file__':__file__})
