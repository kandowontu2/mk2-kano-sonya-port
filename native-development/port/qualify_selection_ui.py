"""Finite native-control border/number pixel checks, not every UI transition."""
import csv
import hashlib
import json
from pathlib import Path
import subprocess
import sys
from PIL import Image

PORT=Path(__file__).resolve().parent
BASE=PORT.parent/'baseline'
FLAGS=(subprocess.CREATE_NO_WINDOW|subprocess.BELOW_NORMAL_PRIORITY_CLASS) if sys.platform=='win32' else 0
GREEN={(0,123,0),(0,255,0)}

def digest(path):
    value=hashlib.sha256()
    with path.open('rb') as stream:
        while chunk:=stream.read(65536):value.update(chunk)
    return value.hexdigest().upper()

def masks(image,center,colors=GREEN,glyph_y=33):
    glyph=image.crop((center-5,glyph_y,center+6,glyph_y+22))
    glyph_mask=tuple(i for i,color in enumerate(glyph.get_flattened_data()) if color in colors)
    rim=image.crop((center-32,19,center+33,100))
    border_mask=tuple(i for i,color in enumerate(rim.get_flattened_data()) if color in colors and
        (i%65<5 or i%65>=60 or i//65<5 or i//65>=76))
    return glyph_mask,border_mask

def main(names):
    assert len(names)==2 and len(set(names))==2
    cases=[];evidence=[Path(__file__),PORT/'audit_campaign_run.py',PORT/'campaign_budget.py',PORT/'diagnostics/selection_ui_observer.lua']
    for name in names:
        assert Path(name).name==name and '/' not in name and '\\' not in name
        result=subprocess.run([sys.executable,str(PORT/'audit_campaign_run.py'),name],
                              cwd=PORT,capture_output=True,text=True,creationflags=FLAGS)
        assert result.returncode==0,result.stderr[-2000:]
        run=BASE/name;receipt=json.loads((run/'execution.json').read_text())
        assert '--selection-ui-observe' in receipt['testArguments']
        audit=json.loads((run/'CAMPAIGN_AUDIT.json').read_text())
        actor=audit['actor'];assert actor in (17,18) and audit['currentFullROMVerified']
        with (run/'selection_ui.csv').open() as stream:rows=list(csv.DictReader(stream))
        expected=[n for n in range(3500,4501) if (n<=3950 and n%4==0) or (n>3950 and n%10==0)]
        assert [int(row['frame']) for row in rows]==expected
        reference=set();target=[];colors=[];previews=set()
        for row in rows:
            path=run/'snap'/f"selection_ui_{int(row['frame']):05d}.png"
            with Image.open(path) as picture:
                assert picture.size==(400,254)
                image=picture.convert('RGB')
                if row['mode']=='4' and row['p1selected']=='1':reference.add(masks(image,110))
                if row['mode']=='4' and row['p1selected']==str(actor):
                    center=50 if actor==17 else 350
                    target.append(masks(image,center))
                    colors.append(image.getpixel((center-30,21)))
                    previews.add(hashlib.sha256(image.crop((0,105,79,246)).tobytes()).hexdigest())
            evidence.append(path)
        reference={pair for pair in reference if pair[0] and pair[1]}
        assert reference and all(len(pair[0])==63 for pair in reference)
        matching=sum(pair in reference for pair in target)
        assert matching>=4 and GREEN<=set(colors)
        valid=[color for color in colors if color in GREEN]
        transitions=sum(a!=b for a,b in zip(valid,valid[1:]))
        assert transitions>=4 and len(previews)>=2
        combat=[row for row in rows if row['mode']=='2']
        assert combat and all(row['p1selected']==row['p1char']==str(actor) for row in combat)
        cases.append(dict(run=name,actor=actor,physicalPlayer=1,highlightSamples=len(target),
            samplesMatchingOriginalLiuBorderAndCenteredNumber=matching,numberMaskPixels=63,
            sampledDimBrightTransitions=transitions,previewRegionPixelVariants=len(previews),
            firstCombatOwnIdentityVerified=True,allFramesOrNavigationEdgesVerified=False))
        evidence.extend(run/item for item in ('execution.json','autoboot.lua','CAMPAIGN_AUDIT.json','selection_ui.csv'))
    assert {case['actor'] for case in cases}=={17,18}
    report=dict(scope='Finite P1 original-control border/number/blink samples and first-combat identity',
        cases=cases,ladderCleanupVisualReviewSeparate=True,allUITransitionsVerified=False,
        fullPortVerified=False,pins={str(path):digest(path) for path in evidence})
    (PORT/'SELECTION_UI_2219_QUALIFICATION.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({key:value for key,value in report.items() if key!='pins'},indent=2))

if __name__=='__main__':main(sys.argv[1:])
