"""Finite static-page stability, separate from full visual/content acceptance."""
import csv
import hashlib
import json
from pathlib import Path
import sys
from PIL import Image
from qualify_campaign_clear import qualify,BASE

def static_state(rows):
    assert len(rows)==12
    assert [int(r['age']) for r in rows]==list(range(int(rows[0]['age']),int(rows[0]['age'])+12))
    assert all(r['displayon']=='1' and r['noflip']=='65535' and r['autoerase']=='0' for r in rows)
    assert all(r['objlst']==r['objlst2']=='00000000' for r in rows)
    assert len({(r['pageaddr'],r['scrntl'],r['scrnlr']) for r in rows})==1

def verify(name):
    clear=qualify(name)
    assert clear['nativeCampaignClearVerified']
    run=BASE/name
    receipt=json.loads((run/'execution.json').read_text())
    assert '--campaign-ending-state' in receipt['testArguments']
    rows=list(csv.DictReader((run/'ending_state.csv').open()))
    windows=[];pins={}
    for begin in (1734,2454):
        window=[r for r in rows if begin<=int(r['age'])<begin+12]
        static_state(window)
        pixels=[]
        for row in window:
            path=run/'snap'/f"ending_state_{int(row['frame']):06d}_age{int(row['age']):04d}.png"
            with Image.open(path) as image:
                assert image.size==(400,254)
                rgb=image.convert('RGB')
                assert rgb.getbbox() is not None, 'Black page is not a passing stable image'
                pixels.append(hashlib.sha256(rgb.tobytes()).hexdigest().upper())
            pins[str(path)]=hashlib.sha256(path.read_bytes()).hexdigest().upper()
        assert len(set(pixels))==1, 'Captured page changes within consecutive-field window'
        windows.append(dict(firstAge=begin,consecutiveFields=12,pixelSHA256=pixels[0]))
    assert windows[0]['pixelSHA256']!=windows[1]['pixelSHA256'], 'Two pages must be distinct'
    for path in (run/'ending_state.csv',run/'CAMPAIGN_CLEAR_QUALIFICATION.json',Path(__file__)):
        pins[str(path)]=hashlib.sha256(path.read_bytes()).hexdigest().upper()
    report=dict(scope='Two finite12-field earned-ending static-page windows',run=name,
                staticPageStateAndPixelStabilityVerified=True,twoDistinctNonblackPages=True,
                windows=windows,storyTextAndArtVisuallyAccepted=False,
                allEndingFieldsVerified=False,fullPortVerified=False,pins=pins)
    (run/'ENDING_CAPTURE_QUALIFICATION.json').write_text(json.dumps(report,indent=2)+'\n')
    return {k:v for k,v in report.items() if k!='pins'}

if __name__=='__main__':print(json.dumps(verify(sys.argv[1]),indent=2))
