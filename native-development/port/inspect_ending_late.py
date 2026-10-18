"""Diagnose late capture cadence; never certify an unsampled framebuffer."""
import csv
import hashlib
import json
from pathlib import Path
import sys
from PIL import Image
from qualify_campaign_clear import qualify,BASE
from qualify_ending_capture import static_state

def pixel_hash(path):
    with Image.open(path) as image:
        assert image.size==(400,254)
        return hashlib.sha256(image.convert('RGB').tobytes()).hexdigest().upper()

def inspect(name,previous):
    qualify(name)
    run=BASE/name;old=BASE/previous
    assert (run/'campaign.csv').read_bytes()==(old/'campaign.csv').read_bytes(), 'Not an identical campaign replay'
    receipt=json.loads((run/'execution.json').read_text())
    prior=json.loads((old/'execution.json').read_text())
    assert receipt['replacementChips']==prior['replacementChips']
    assert receipt['testArguments']==prior['testArguments']
    assert prior['exitCode']==0 and not prior['timedOut']
    rows=list(csv.DictReader((run/'ending_state.csv').open()))
    late=[r for r in rows if 2574<=int(r['age'])<2586]
    static_state(late)
    samples=list(csv.DictReader((run/'ending_video_samples.csv').open()))
    assert [int(r['age']) for r in samples]==list(range(2520,2640))
    images=[run/'snap'/f"ending_late_{int(r['frame']):06d}_age{int(r['age']):04d}.png" for r in late]
    pixels=[pixel_hash(path) for path in images]
    second=next(r for r in rows if r['age']=='2460')
    second_path=run/'snap'/f"ending_state_{int(second['frame']):06d}_age2460.png"
    second_hash=pixel_hash(second_path)
    age2580=next(r for r in late if r['age']=='2580')
    old_capture=old/'snap'/f"ending_{int(age2580['frame']):06d}_age2580.png"
    new_capture=run/'snap'/f"ending_{int(age2580['frame']):06d}_age2580.png"
    report=dict(scope='Late consecutive capture versus sparse samples, identical current-ROM replay',
                run=name,previous=previous,completeCampaignTraceIdentical=True,
                lateConsecutiveFrames=12,latePixelVariants=len(set(pixels)),
                lateWindowMatchesEarlierSecondPage=all(value==second_hash for value in pixels),
                controlVariants=len({r['videoControl'] for r in samples}),
                sparseVRAMSampleVariants=len({r['vramSampleFNV'] for r in samples}),
                sparsePaletteSampleVariants=len({r['paletteSampleFNV'] for r in samples}),
                oldSparse2580PixelSHA256=pixel_hash(old_capture),
                newSparse2580PixelSHA256=pixel_hash(new_capture),
                allFramebufferPixelsVerified=False,wholeEndingVisuallyAccepted=False,
                fullPortVerified=False)
    pins=images+[second_path,old_capture,new_capture,run/'ending_video_samples.csv',
                 run/'ending_state.csv',run/'campaign.csv',old/'campaign.csv',
                 run/'execution.json',old/'execution.json',run/'autoboot.lua',Path(__file__)]
    report['pins']={str(p):hashlib.sha256(p.read_bytes()).hexdigest().upper() for p in pins}
    (run/'ENDING_LATE_DIAGNOSTIC.json').write_text(json.dumps(report,indent=2)+'\n')
    return {k:v for k,v in report.items() if k!='pins'}

if __name__=='__main__':print(json.dumps(inspect(*sys.argv[1:3]),indent=2))
