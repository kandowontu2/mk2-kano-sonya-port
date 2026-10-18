"""Native banked-shadow source checks and bounded captured visual regression."""
import hashlib
import csv
import json
from pathlib import Path
import numpy as np
from PIL import Image
from shadow_bank_source import NEW
from verify_finisher_roms import verify as verify_full_rom
from shadow_pixel_regression import verify as verify_shadow_pixels
import zipfile

PORT=Path(__file__).resolve().parent
BASE=PORT.parent/'baseline'
SRC=BASE/'mk2-rebuild-main/srcp'
sha=lambda b:hashlib.sha256(b).hexdigest().upper()
source=(SRC/'MKDISP.ASM').read_text()
assert source.count(NEW)==1
assert '\t.if wunit\n\tdsj\tb3,shad7\n\t.else\n\tdsjs\tb3,shad7\n\t.endif' in source
cases=0
for bit_address in (0,1,0x3fffff8,0x4000000,0x4000004,0x6000000,100889408,106113984,0x8fffff8):
    for old_control in (0,0x800,0x1234,0xffff):
        bank=(bit_address>>26)&3
        cpu=0x02000000+(bit_address&0x03ffffff)
        control=(old_control&~0x300)|(bank<<8)
        assert 0x02000000<=cpu<=0x06ffffff
        assert ((control>>8)&3)*0x4000000+(cpu-0x02000000)==bit_address
        assert (control&~0x300)==(old_control&~0x300)
        cases+=1
frozen=json.loads((PORT/'FROZEN_VICTIM_QUALIFICATION.json').read_text())
assert frozen['frozenVictimBehaviorVerified']
assert frozen['currentFull26ROMBytesVerified']
for filename,digest in frozen['pins'].items():assert sha(Path(filename).read_bytes())==digest
assert [sha(b''.join((SRC/f'rom/P12{part}.{lane}').read_bytes() for part in ('F8','FC'))) for lane in range(2)]==frozen['programLaneSHA256']
captures=[]
evidence=[Path(__file__),PORT/'shadow_bank_source.py',PORT/'shadow_pixel_regression.py',PORT/'verify_finisher_roms.py',
          SRC/'MKDISP.ASM',PORT/'FROZEN_VICTIM_QUALIFICATION.json']
for actor,old,new in ((17,'stock_freeze_kano154','stock_shadow_kano158'),(18,'stock_freeze_sonya155','stock_shadow_sonya159')):
    before=json.loads((BASE/old/'execution.json').read_text())
    after=json.loads((BASE/new/'execution.json').read_text())
    assert before['controllerSHA256']==after['controllerSHA256']
    current_cases=[case for case in frozen['cases'] if case['actor']==actor and case['victimSide']==2]
    assert len(current_cases)==1
    current=BASE/current_cases[0]['run']
    receipt=json.loads((current/'execution.json').read_text())
    assert receipt['exitCode']==0 and not receipt['timedOut']
    assert sha((current/'autoboot.lua').read_bytes())==receipt['controllerSHA256']
    with zipfile.ZipFile(current/'roms/mk3.zip') as archive:verify_full_rom(archive,receipt)
    evidence.extend([BASE/old/'execution.json',BASE/new/'execution.json',BASE/new/'liu_bike.csv',
                     current/'execution.json',current/'autoboot.lua',current/'liu_bike.csv'])
    for filename in ('freeze_160.png','freeze_320.png'):
        old_path=BASE/old/'snap'/filename;new_path=BASE/new/'snap'/filename
        with Image.open(old_path) as image:a=np.asarray(image.convert('RGB')).copy()
        with Image.open(new_path) as image:b=np.asarray(image.convert('RGB')).copy()
        assert a.shape==b.shape==(254,400,3)
        changed=np.any(a!=b,axis=2)
        ys,xs=np.nonzero(changed)
        assert changed[:190].sum()==0
        assert len(xs)>0 and xs.min()>=230 and xs.max()<340 and ys.min()>=190 and ys.max()<233
        current_path=current/'snap'/filename
        with Image.open(current_path) as image:c=np.asarray(image.convert('RGB')).copy()
        assert np.array_equal(verify_shadow_pixels(a,b,c),changed)
        tick=filename.split('_')[1].split('.')[0]
        with (BASE/new/'liu_bike.csv').open() as stream:historical=next(row for row in csv.DictReader(stream) if row['fight']==tick)
        with (current/'liu_bike.csv').open() as stream:present=next(row for row in csv.DictReader(stream) if row['fight']==tick)
        assert all(historical[key]==present[key] for key in ('p1char','p2char','p1x','p2x'))
        evidence.extend([old_path,new_path,current_path])
        captures.append(dict(actor=actor,file=filename,newRun=new,newSHA256=sha(new_path.read_bytes()),
            currentRun=current.name,currentSHA256=sha(current_path.read_bytes()),
            currentShadowFixPixelsMatched=int(changed.sum()),
            changedPixels=int(changed.sum()),changedBounds=[int(xs.min()),int(ys.min()),int(xs.max()),int(ys.max())] if len(xs) else None,
            changedPixelsAboveY190=int(changed[:190].sum())))
report=dict(scope='Native Wolf shadow graphics bank read and two frozen/normal stance captures per actor',
    bankTranslationCases=cases,nonBankControlBitsPreserved=True,sourceRestoresSystemControlAfterEachByte=True,
    sourceSHA256=sha((SRC/'MKDISP.ASM').read_bytes()),captures=captures,
    capturedBlackStripesVisuallyAbsent=True,capturedFloorShadowsVisuallyReviewed=True,
    allAnimationsAndArenasVerified=False,releaseReady=False,fullPortVerified=False)
report['currentFourCaptureShadowPixelRegressionVerified']=True
report['historicalDeltaBaselineNotCurrentRuntime']=True
report['pins']={str(path):sha(path.read_bytes()) for path in evidence}
(PORT/'SHADOW_BANK_QUALIFICATION.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
