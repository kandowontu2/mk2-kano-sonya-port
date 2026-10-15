"""Decode original swallowing grammar and character references; no game edits.

Only three small source-reference atlases are saved for authoring missing art.
These are not emulator screenshots or runtime/art acceptance.
"""
import hashlib,json,struct,subprocess
from pathlib import Path
from PIL import Image,ImageDraw
import audit_animation_poses as poses
import audit_native_inflation_references_v931 as native
import build_mk2ks_mk3 as animation
import upgrade_ksui_previews as ui
ROOT=native.ROOT;OUT=ROOT/'art_reference_mileena_v3801'
def sha(data):return hashlib.sha256(data).hexdigest().upper()
def group(program,address):
    values=[]
    for index in range(6):
        pointer=struct.unpack_from('<I',program,native.off(address)+index*4)[0]
        if not pointer:return values
        if not 0xff800000<=pointer<0xfffff000:raise ValueError('Original descriptor range')
        values.append(pointer)
    raise ValueError('Original group terminator')
def main():
    if OUT.exists():raise ValueError('Fresh immutable source references')
    original=(ROOT/'mk2/mk2-maincpu.bin').read_bytes();donor=(ROOT/'mk3/mk3-maincpu.bin').read_bytes()
    assert sha(original)=='45B3285496DB555EFAF4A3608A4F59845DD47A82E4A0593607E0592F47B36F23'
    assert sha(donor)=='1BC7A53A023F15B20F01398F87E38478A27C670DF27EA320E36125D0957EE651'
    pins={str(ROOT/'mk2/mk2-maincpu.bin'):sha(original),str(ROOT/'mk3/mk3-maincpu.bin'):sha(donor)}
    gfx=bytearray(0xc00000)
    for base,pair in enumerate(((14,19),(16,20),(17,22))):
        for lane,(side,chip)in enumerate((('g',pair[0]),('j',pair[0]),('g',pair[1]),('j',pair[1]))):
            path=ROOT/'mk2'/f'l1_mortal_kombat_ii_game_rom_u{side}{chip}.u{side}{chip}'
            raw=path.read_bytes();assert len(raw)==0x100000;pins[str(path)]=sha(raw)
            gfx[base*0x400000+lane:base*0x400000+lane+len(raw)*4:4]=raw
    donor_gfx=ui.load_gfx(ROOT/'mk3')
    for _,chips in ui.GFX_BANKS:
        for chip in chips:
            path=ROOT/'mk3'/f'l1_mortal_kombat_3_u{chip}_game_rom.u{chip}';pins[str(path)]=sha(path.read_bytes())
    OUT.mkdir();assert subprocess.run(['compact.exe','/C','/I','/Q','/S:'+str(OUT)],capture_output=True).returncode==0
    report=dict(scope=__doc__,inputHashes=pins,stock={},ownReferences={},gameWrites=0,artAcceptance=False,fullPortAcceptance=False)
    for name,identity,expected_count in(('male',1,7),('female',4,8)):
        stream=struct.unpack_from('<I',original,native.off(0xff9e9140)+identity*4)[0]
        palette_address=struct.unpack_from('<I',original,native.off(0xff907910)+identity*4)[0]
        palette=native.palette(original,palette_address);records=[];words=[]
        for index in range(10):
            word=struct.unpack_from('<I',original,native.off(stream)+index*4)[0];words.append(word)
            if not word:break
            frames=group(original,word);specs=[ui.component_spec(original,f)for f in frames]
            bounds=[min(-s[4]for s in specs),min(-s[5]for s in specs),max(-s[4]+s[2]for s in specs),max(-s[5]+s[3]for s in specs)]
            image=poses.render_group(original,gfx,palette,frames)
            records.append(dict(index=index,group=f'{word:08X}',frames=[f'{f:08X}'for f in frames],specs=specs,bounds=bounds,size=list(image.size),rgbaSHA256=sha(image.tobytes()),image=image))
        assert len(records)==expected_count and words[-1]==0
        sheet=Image.new('RGBA',(1200,560),(32,32,38,255));draw=ImageDraw.Draw(sheet)
        for r in records:
            image=r.pop('image');x=r['index']%4*300;y=r['index']//4*280
            scaled=image.resize((image.width*2,image.height*2),Image.Resampling.NEAREST)
            sheet.alpha_composite(scaled,(x+(300-scaled.width)//2,y+34+(240-scaled.height)//2))
            draw.text((x+4,y+3),f"{name} phase {r['index']}: {r['size']}",fill='white')
            draw.text((x+4,y+17),f"native bounds {r['bounds']}",fill='white')
        path=OUT/f'stock-{name}-swallowing.png';sheet.save(path)
        report['stock'][name]=dict(identity=identity,stream=f'{stream:08X}',words=[f'{w:08X}'for w in words],palette=f'{palette_address:08X}',poses=records,atlas=str(path),atlasSHA256=sha(path.read_bytes()))
    sheet=Image.new('RGBA',(1200,500),(32,32,38,255));draw=ImageDraw.Draw(sheet)
    for row,(name,root,special,block)in enumerate((('kano',animation.KANO_MAIN,animation.KANO_SPECIAL,animation.KANO_BLOCK),('sonya',animation.SONYA_MAIN,animation.SONYA_SPECIAL,animation.SONYA_BLOCK))):
        spans=animation.sequence_spans(donor,root,block,(root,special));palette=ui.donor_palette(donor,name);records=[]
        for col,number in enumerate((0,16,37)):
            groups=list(dict((g,f)for _,g,f in animation.group_references(donor,*spans[number],*block)).items())
            address,frames=groups[0];image=poses.render_group(donor,donor_gfx,palette,frames)
            scaled=image.resize((image.width*2,image.height*2),Image.Resampling.NEAREST)
            sheet.alpha_composite(scaled,(col*400+(400-scaled.width)//2,row*250+35+(210-scaled.height)//2))
            draw.text((col*400+4,row*250+5),f'{name}: original animation {number}, {address:08X}',fill='white')
            records.append(dict(animation=number,group=f'{address:08X}',frames=[f'{f:08X}'for f in frames],size=list(image.size),rgbaSHA256=sha(image.tobytes())))
        report['ownReferences'][name]=records
    path=OUT/'kano-sonya-original-costumes.png';sheet.save(path);report['ownReferenceAtlas']=str(path);report['ownReferenceAtlasSHA256']=sha(path.read_bytes())
    (OUT/'reference.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(output=str(OUT),stockPhases={'male':7,'female':8},gameWrites=0,artAcceptance=False),indent=2))
if __name__=='__main__':main()
