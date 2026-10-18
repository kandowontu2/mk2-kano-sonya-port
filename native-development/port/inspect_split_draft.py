"""Identify transparent separated split components without modifying artwork."""
import json
import sys
from pathlib import Path
from PIL import Image
from build_inflation_assets import sha

PORT=Path(__file__).resolve().parent
SOURCE=PORT/'assets/split_draft/split-atlas.png'


def opaque_intervals(alpha,top,bottom):
    intervals=[]
    begin=None
    for x in range(alpha.width+1):
        opaque=x<alpha.width and alpha.crop((x,top,x+1,bottom)).getextrema()[1]>=128
        if opaque and begin is None:begin=x
        if not opaque and begin is not None:
            intervals.append((begin,x))
            begin=None
    return intervals


def inspect(source=SOURCE):
    rows=(0,315,548,810,1024)
    components=[]
    with Image.open(source) as atlas:
        assert atlas.mode=='RGBA' and atlas.size==(1536,1024)
        alpha=atlas.getchannel('A')
        assert alpha.getextrema()[0]==0
        for row in range(4):
            intervals=opaque_intervals(alpha,rows[row],rows[row+1])
            assert len(intervals)==(7 if row%2==0 else 10)
            phase_base=0 if row%2==0 else 5
            cursor=0
            for col in range(5):
                phase=phase_base+col
                count=1 if phase<3 else 2
                for side in range(count):
                    left,right=intervals[cursor]
                    cursor+=1
                    box=(left,rows[row],right,rows[row+1])
                    tile=alpha.crop(box).point(lambda a:255 if a>=128 else 0)
                    bounds=tile.getbbox()
                    assert bounds and bounds[1]>0 and bounds[3]<tile.height
                    assert left>0 and right<atlas.width
                    rectangle=[left+bounds[0],rows[row]+bounds[1],left+bounds[2],rows[row]+bounds[3]]
                    components.append(dict(actor='kano' if row<2 else 'sonya',phase=phase,
                        role='whole' if count==1 else ('viewer_left' if side==0 else 'viewer_right'),
                        sourceRectangle=rectangle,alpha128Pixels=tile.histogram()[255],
                        alpha128BoundsClearOfAtlasEdges=True))
            assert cursor==len(intervals)
    assert len(components)==34
    return dict(format='MK2KS-SPLIT-DRAFT-LAYOUT-1',file=source.name,
        SHA256=sha(source.read_bytes()),size=[1536,1024],rowBoundaries=rows,
        components=components,wholeComponents=6,halfComponents=28,
        backgroundHasTransparentAlpha=True,atlasPixelsChanged=False,
        costumeAsymmetryReviewRequired=True,nativeFacingAndOriginsVerified=False,
        pixelAcceptance=False,runtimeVerified=False,releaseReady=False)


if __name__=='__main__':
    repair=sys.argv[1:]==['--kano-continuity-repair']
    assert not sys.argv[1:] or repair
    report=inspect(SOURCE.parent/'split-atlas-v2.png' if repair else SOURCE)
    name='SPLIT_DRAFT_LAYOUT_V2.json' if repair else 'SPLIT_DRAFT_LAYOUT.json'
    (SOURCE.parent/name).write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k!='components'},indent=2))
