"""Convert split draft to editable own indexed components; not runtime acceptance."""
import json
import sys
from pathlib import Path
from PIL import Image
from generate_arm_rip_sources import palette, sha
from split_contract import extract

PORT=Path(__file__).resolve().parent
DRAFT=PORT/'assets/split_draft'
OUT=PORT/'assets/split'


def main():
    repair=sys.argv[1:]==['--kano-continuity-repair']
    assert not sys.argv[1:] or repair
    output=PORT/'assets/split_v2' if repair else OUT
    assert not output.exists(), 'Never overwrite reviewed native source art'
    layout_path=DRAFT/'SPLIT_DRAFT_LAYOUT.json'
    layout=json.loads(layout_path.read_text())
    atlas_path=DRAFT/layout['file']
    assert sha(atlas_path.read_bytes())==layout['SHA256']
    revised=None
    if repair:
        revised=json.loads((DRAFT/'SPLIT_DRAFT_LAYOUT_V2.json').read_text())
        assert sha((DRAFT/revised['file']).read_bytes())==revised['SHA256']
    geometry=extract()['sequences']
    frames=[]
    outputs={}
    preview=Image.new('RGB',(1000,680),(35,35,40))
    with Image.open(atlas_path) as atlas:
        assert atlas.mode=='RGBA'
        for actor_index,actor in enumerate(('kano','sonya')):
            ground=131 if actor=='kano' else 132
            refs=geometry['liu' if actor=='kano' else 'female_ninja']
            selected=[f for f in layout['components'] if f['actor']==actor]
            first=next(f for f in selected if f['phase']==0)
            first_box=first['sourceRectangle']
            scale=ground/(first_box[3]-first_box[1])
            ground_delta=ground-refs[0]['unionBounds'][3]
            colors,palette_hash=palette(actor)
            rgb=[((v>>10&31)*255//31,(v>>5&31)*255//31,(v&31)*255//31) for v in colors]
            nearest={}
            for frame in selected:
                phase,role=frame['phase'],frame['role']
                source_asset=atlas_path
                if repair and actor=='kano' and role!='whole':
                    frame=next(f for f in revised['components'] if f['actor']==actor and f['phase']==phase and f['role']==role)
                    source_asset=DRAFT/revised['file']
                    with Image.open(source_asset) as replacement:
                        crop=replacement.crop(frame['sourceRectangle'])
                else:
                    crop=atlas.crop(frame['sourceRectangle'])
                w,h=round(crop.width*scale),round(crop.height*scale)
                assert 0<w<=200 and 0<h<=170
                sample=crop.resize((w,h),Image.Resampling.LANCZOS)
                pixels=[]
                for r,g,b,a in sample.getdata():
                    if a<128:
                        pixels.append(0)
                        continue
                    key=(r,g,b)
                    if key not in nearest:
                        nearest[key]=min(range(1,64),key=lambda i:sum((key[c]-rgb[i][c])**2 for c in range(3)))
                    pixels.append(nearest[key])
                assert any(pixels)
                bottom=refs[phase]['unionBounds'][3]+ground_delta
                yo=h-bottom
                if role=='whole':
                    feet=[i%w for i in range(max(0,h-4)*w,h*w) if pixels[i]]
                    assert feet
                    xo=round((min(feet)+max(feet))/2)
                else:
                    # Canonical left-half inner edge follows native peel path.
                    # Native flip_multi will mirror the secondary object.
                    xo=w-refs[phase]['unionBounds'][2]
                reflected=role=='viewer_right'
                if reflected:
                    pixels=[v for y in range(h) for v in pixels[y*w:(y+1)*w][::-1]]
                filename=f'{actor}_{role}_{phase}.pgm'
                data=(f'P2\n# Own palette; zero transparent. Canonical native orientation.\n{w} {h}\n63\n'+
                      '\n'.join(' '.join(map(str,pixels[y*w:(y+1)*w])) for y in range(h))+'\n').encode('ascii')
                outputs[filename]=data
                rendered_pixels=pixels
                if reflected:
                    rendered_pixels=[v for y in range(h) for v in pixels[y*w:(y+1)*w][::-1]]
                rendered=Image.new('RGBA',(w,h))
                rendered.putdata([(*rgb[i],255) if i else (0,0,0,0) for i in rendered_pixels])
                row=actor_index*2+phase//5
                center=phase%5*200+100
                x=center+xo-w if reflected else center-xo
                y=row*170+145-ground-yo
                preview.paste(rendered,(x,y),rendered)
                frames.append(dict(**frame,file=filename,SHA256=sha(data),width=w,height=h,
                    xOffset=xo,yOffset=yo,ground=ground,sourceScale=scale,
                    paletteSourceSHA256=palette_hash,nativeSecondaryPixelsReflected=reflected,
                    sourceAsset=str(source_asset.relative_to(PORT)),sourceAssetSHA256=sha(source_asset.read_bytes()),
                    referenceGeometryOnly=refs[phase],nativeGroundAdaptation=ground_delta,
                    requiresCostumeAndRuntimeAlignmentReview=True))
    assert len(frames)==len(outputs)==34
    for actor in ('kano','sonya'):
        assert len([f for f in frames if f['actor']==actor and f['role']=='whole'])==3
        for role in ('viewer_left','viewer_right'):
            assert [f['phase'] for f in frames if f['actor']==actor and f['role']==role]==list(range(3,10))
    if repair:
        previous=json.loads((OUT/'SPLIT_SOURCES.json').read_text())
        preserved=[f for f in frames if f['actor']!='kano' or f['role']=='whole']
        assert len(preserved)==20
        for f in preserved:
            old=next(v for v in previous['frames'] if v['file']==f['file'])
            assert f['SHA256']==old['SHA256'],'Unrelated indexed pixels changed'
    output.mkdir()
    for filename,data in outputs.items():(output/filename).write_bytes(data)
    preview.save(output/'native-layout-preview.png')
    report=dict(format='MK2KS-SPLIT-INDEXED-SOURCES-1',frames=frames,
        draftLayoutSHA256=sha(layout_path.read_bytes()),atlasSHA256=sha(atlas_path.read_bytes()),
        transparentIndex=0,maximumIndex=63,originalCharacterPixelsCopied=False,
        dedicatedAsymmetricHalfSources=True,uniformScalePerActor=True,
        paletteConversionDone=True,costumeContinuityAccepted=False,
        nativeAlignmentAccepted=False,runtimeVerified=False,releaseReady=False)
    if repair:
        report.update(kanoHalfContinuityRevision=True,unchangedOtherFrames=20,
            priorSourceManifestSHA256=sha((OUT/'SPLIT_SOURCES.json').read_bytes()),
            revisedDraftLayoutSHA256=sha((DRAFT/'SPLIT_DRAFT_LAYOUT_V2.json').read_bytes()))
    (output/'SPLIT_SOURCES.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(frames=len(frames),nativeSecondaryFramesReflected=14,
                         runtimeVerified=False,costumeContinuityAccepted=False)))


if __name__=='__main__':main()
