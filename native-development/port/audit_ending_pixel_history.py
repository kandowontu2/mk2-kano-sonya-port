"""Correct preview-based conclusions using actual decoded PNG bytes."""
import hashlib
import json
import re
from pathlib import Path
from PIL import Image

PORT=Path(__file__).resolve().parent
BASE=PORT.parent/'baseline'

def signature(path):
    with Image.open(path) as source:
        image=source.convert('RGB')
        assert image.size==(400,254)
        return hashlib.sha256(image.tobytes()).hexdigest().upper(),image.getbbox()

def audit():
    pins={};cases=[]
    def inspect(run,prefix,age):
        paths=[p for p in (BASE/run/'snap').glob(f'{prefix}_*_age{age:04d}.png')
               if re.fullmatch(re.escape(prefix)+r'_\d+_age'+f'{age:04d}'+r'\.png',p.name)]
        assert len(paths)==1,(run,prefix,age)
        path=paths[0];digest,bounds=signature(path)
        pins[str(path)]=hashlib.sha256(path.read_bytes()).hexdigest().upper()
        cases.append(dict(run=run,capture=path.name,pixelSHA256=digest,nonblackBounds=bounds))
        return digest,bounds
    for age in (1500,1740,2220,2580):
        assert inspect('stock_wolf_game783','ending',age)[1] is None
    first=inspect('stock_wolf_game786','ending_state',1734)[0]
    second=inspect('stock_wolf_game786','ending_state',2454)[0]
    assert first!=second
    for run in ('stock_wolf_game784','stock_wolf_game785','stock_wolf_game786','stock_wolf_game787'):
        for age in (1500,1620,1740,1860,1980,2100):
            digest,bounds=inspect(run,'ending',age)
            assert bounds is not None and digest==first
        for age in (2220,2340,2460,2580):
            digest,bounds=inspect(run,'ending',age)
            assert bounds is not None and digest==second
    #273B used live page flipping, yet its actual consecutive PNGs are stable.
    for age in range(1734,1746):assert inspect('stock_wolf_game785','ending_state',age)[0]==first
    for age in range(2454,2466):assert inspect('stock_wolf_game785','ending_state',age)[0]==second
    report=dict(scope='Named historical PNG files, not every rendered field',
                original034FBlackPagesConfirmed=True,
                restored273BObservedPagesPixelStable=True,
                laterPartialPreviewDiagnosisRetracted=True,
                nativeStaticPathRequiredToFixObservedFlicker=False,
                correctedConclusion='The observed partial previews did not reflect the actual PNG pixel data; no post-restore pixel disappearance is shown by these captures.',
                inspectedCaptures=len(cases),cases=cases,allEndingFieldsVerified=False,
                fullPortVerified=False,pins=pins)
    pins[str(Path(__file__))]=hashlib.sha256(Path(__file__).read_bytes()).hexdigest().upper()
    (PORT/'ENDING_PIXEL_HISTORY_AUDIT.json').write_text(json.dumps(report,indent=2)+'\n')
    return {k:v for k,v in report.items() if k not in ('pins','cases')}

if __name__=='__main__':print(json.dumps(audit(),indent=2))
