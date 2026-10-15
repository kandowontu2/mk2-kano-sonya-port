"""Classify targeted raster differences, preserving unexplained sky pixels."""
import json,re
from pathlib import Path
from PIL import Image,ImageChops
import verify_native_source_sync as sync

def rows(folder):
    result={}
    for line in (folder/'run.log').read_text().splitlines():
        assert '[LUA ERROR]' not in line
        if line.startswith('MK2_UI_'):
            result.setdefault(line.split()[0][7:],[]).append(dict(re.findall(r'(\w+)=([^\s]+)',line)))
    return result

out=sync.ROOT/'audit_bounded_ladder_difference_review_checked';assert not out.exists()
proof_path=sync.ROOT/'audit_bounded_ladder_scanout_observed/report.json';proof=json.loads(proof_path.read_text());assert proof['passed']
cases={};images={}
for suffix in ('added','stock'):
    folder=sync.ROOT/f'audit_bounded_ladder_difference_sonya_p2_{suffix}_runtime'
    base=sync.ROOT/f'audit_bounded_ladder_scanout_sonya_p2_{suffix}_runtime'
    assert sync.sha(base/'run.log')==proof['results']['sonyaP2']['cases'][suffix]['logSHA256']
    t=json.loads((folder/'terminal.json').read_text());assert t['exitCode']==0 and t['limitReason'] is None
    assert rows(folder)==rows(base)
    files={age:folder/'snap'/f'difference_{age:03}.png' for age in (87,100,200,360)}
    images[suffix]={age:Image.open(path).convert('RGB') for age,path in files.items()}
    cases[suffix]=dict(terminal=t,logSHA256=sync.sha(folder/'run.log'),imageSHA256={str(age):sync.sha(path) for age,path in files.items()})
comparisons={}
for age in (87,100,200,360):
    a,b=images['added'][age],images['stock'][age];assert a.size==b.size==(400,254)
    diff=ImageChops.difference(a,b)
    assert diff.crop((0,24,80,241)).getbbox() is None
    right=diff.crop((320,24,400,241)).getbbox()
    if age in (200,360):assert right is None
    else:assert right is not None and right[2]<=6 and right[3]-right[1]<=9
    comparisons[str(age)]=dict(fullDifferenceBBox=diff.getbbox(),leftFormerCSSRegionBytewiseEqual=True,rightFormerCSSRegionDifferenceBBox=right,rightSkyDifferenceUnresolved=age in (87,100),ownLadderPortraitDifferenceVisuallyExpected=True)
report=dict(passed=True,cases=cases,comparisons=comparisons,sourceSync=sync.verify(),priorProofSHA256=sync.sha(proof_path),checkerSHA256=sync.sha(Path(__file__)),visualReview='Own moving ladder portrait and later own tower portrait differ as expected. No CSS poses/photos visible in the reviewed PNGs. Small upper-right sky discrepancy remains unclassified.',wholeSceneAcceptance=False,fullGoalComplete=False)
out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(dict(passed=True,targetedRasterPairs=4,smallSkyDifferencesUnresolved=True)))
