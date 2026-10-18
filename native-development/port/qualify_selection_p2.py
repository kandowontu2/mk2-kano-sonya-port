"""Finite P2 native cursor pixels using an unobscured original Liu control."""
import csv
import json
from pathlib import Path
import sys
from PIL import Image
from qualify_selection_ui import PORT,BASE,digest,masks
from refresh_special_regression import verify_case

RED={(123,0,0),(255,0,0)}

def main(names):
    assert len(names)==2 and len(set(names))==2
    controls=set();data=[]
    evidence=[Path(__file__),PORT/'qualify_selection_ui.py',PORT/'qualify_initial_specials.py',
              PORT/'verify_finisher_roms.py',PORT/'refresh_special_regression.py']
    for name in names:
        assert Path(name).name==name and '/' not in name and '\\' not in name
        run=BASE/name;receipt=json.loads((run/'execution.json').read_text());args=receipt['testArguments']
        assert '--selection-ui-observe' in args and '--special' in args
        actor=17 if '--mirror' in args else 18
        assert ('--square' in args)==(actor==18)
        verify_case(name,args)
        with (run/'selection_ui.csv').open() as stream:rows=list(csv.DictReader(stream))
        expected=[n for n in range(3000,4501) if (n<=3950 and n%4==0) or (n>3950 and n%10==0)]
        assert [int(row['frame']) for row in rows]==expected
        samples=[];colors=[]
        for row in rows:
            path=run/'snap'/f"selection_ui_{int(row['frame']):05d}.png"
            with Image.open(path) as picture:
                assert picture.size==(400,254)
                image=picture.convert('RGB')
                if row['mode']=='4' and row['p2selected']=='1':
                    pair=masks(image,110,RED,64)
                    if pair[0] and pair[1]:controls.add(pair)
                if row['mode']=='4' and row['p2selected']==str(actor):
                    center=50 if actor==17 else 350
                    samples.append(masks(image,center,RED,64))
                    colors.append(image.getpixel((center-30,21)))
            evidence.append(path)
        combat=[row for row in rows if row['mode']=='2']
        assert combat and all(row['p2selected']==row['p2char']==str(actor) for row in combat)
        data.append((name,actor,samples,colors))
        evidence.extend(run/item for item in ('execution.json','autoboot.lua','selection_ui.csv','qualification.json'))
    assert controls and all(len(pair[0])==61 for pair in controls)
    cases=[]
    for name,actor,samples,colors in data:
        matches=sum(pair in controls for pair in samples)
        assert matches>=4 and RED<=set(colors)
        valid=[color for color in colors if color in RED]
        transitions=sum(a!=b for a,b in zip(valid,valid[1:]))
        assert transitions>=4
        cases.append(dict(run=name,actor=actor,physicalPlayer=2,highlightSamples=len(samples),
            matchingOriginalLiuBorderAndCenteredNumber=matches,numberMaskPixels=61,
            sampledDimBrightTransitions=transitions,firstCombatOwnIdentityVerified=True))
    assert {case['actor'] for case in cases}=={17,18}
    report=dict(scope='Finite P2 red cursor/number/identity versus unobscured original Liu control',cases=cases,
        originalCageControlOccludedByPlayer1NotUsed=True,
        originalReptileJoinFrameNotACursorReference=True,allNavigationEdgesOrTransitionsVerified=False,
        fullPortVerified=False,pins={str(path):digest(path) for path in evidence})
    (PORT/'SELECTION_P2_2219_QUALIFICATION.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({key:value for key,value in report.items() if key!='pins'},indent=2))

if __name__=='__main__':main(sys.argv[1:])
