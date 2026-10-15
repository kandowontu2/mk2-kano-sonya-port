"""Decode exact original shatter-body composite and native own costumes.

Small source-reference atlas, not new gameplay artwork/runtime acceptance.
"""
import hashlib, json, struct, subprocess
from pathlib import Path
from PIL import Image, ImageDraw
import audit_animation_poses as poses
import audit_native_inflation_references_v931 as native
import upgrade_ksui_previews as ui

ROOT=native.ROOT
OUT=ROOT/'art_reference_subzero_shatter_v4861'

def sha(data): return hashlib.sha256(data).hexdigest().upper()
def need(condition,message):
    if not condition: raise ValueError(message)

def main():
    need(not OUT.exists(),'Fresh small source-reference leaf')
    program_path=ROOT/'mk2/mk2-maincpu.bin'; program=program_path.read_bytes()
    need(sha(program)=='45B3285496DB555EFAF4A3608A4F59845DD47A82E4A0593607E0592F47B36F23','Original native program')
    pins={str(program_path):sha(program),str(Path(__file__).resolve()):sha(Path(__file__).read_bytes())}
    graphics=bytearray(0xc00000)
    for bank,pair in enumerate(((14,19),(16,20),(17,22))):
        for lane,(side,chip) in enumerate((('g',pair[0]),('j',pair[0]),('g',pair[1]),('j',pair[1]))):
            path=ROOT/'mk2'/f'l1_mortal_kombat_ii_game_rom_u{side}{chip}.u{side}{chip}'
            raw=path.read_bytes(); need(len(raw)==0x100000,'Original graphics chip')
            pins[str(path)]=sha(raw); graphics[bank*0x400000+lane:bank*0x400000+lane+len(raw)*4:4]=raw
    rows=[]; atlas=Image.new('RGBA',(900,440),(28,28,34,255)); draw=ImageDraw.Draw(atlas)
    for col,(name,identity) in enumerate((('stock female',4),('stock male',11),('stock Liu Kang',0))):
        group=struct.unpack_from('<I',program,native.off(0xff8c2890)+identity*4)[0]
        descriptors=[]
        for index in range(8):
            pointer=struct.unpack_from('<I',program,native.off(group)+index*4)[0]
            if pointer==0: break
            need(0xff800000<=pointer<0xfffff000,'Original shatter descriptor')
            descriptors.append(pointer)
        need(len(descriptors)==3 and pointer==0,'Actual native three-component zero-terminated shatter body')
        palette_address=struct.unpack_from('<I',program,native.off(0xff907910)+identity*4)[0]
        palette=native.palette(program,palette_address)
        image=poses.render_group(program,graphics,palette,descriptors)
        specs=[ui.component_spec(program,p) for p in descriptors]
        doubled=image.resize((image.width*2,image.height*2),Image.Resampling.NEAREST)
        need(doubled.width<=290 and doubled.height<=350,'Bounded reference image')
        atlas.alpha_composite(doubled,(col*300+(300-doubled.width)//2,55+(340-doubled.height)//2))
        draw.text((col*300+5,8),f'{name} original frozen/shatter body',fill='white')
        draw.text((col*300+5,25),f'group {group:08X} / size {image.size}',fill='white')
        rows.append(dict(identity=identity,group=f'{group:08X}',descriptors=[f'{p:08X}' for p in descriptors],
                         specs=specs,size=list(image.size),rgbaSHA256=sha(image.tobytes())))
    own=ROOT/'art_reference_mileena_v3801/kano-sonya-original-costumes.png'
    pins[str(own)]=sha(own.read_bytes())
    OUT.mkdir(); need(subprocess.run(['compact.exe','/C','/I','/Q','/S:'+str(OUT)],capture_output=True).returncode==0,'Compressed before reference output')
    output=OUT/'original-shatter-bodies.png'; atlas.save(output)
    report=dict(scope=__doc__,stock=rows,ownCostumeReference=str(own),ownCostumeReferenceSHA256=pins[str(own)],
                atlas=str(output),atlasSHA256=sha(output.read_bytes()),inputHashes=pins,
                gameWrites=0,artAcceptance=False,fullPortAcceptance=False)
    (OUT/'reference.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items()if k!='inputHashes'},indent=2),flush=True)

if __name__=='__main__': main()
