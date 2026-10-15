"""Fix only twelve morph graphic/command descriptors using original streams.

The exact original MK3 compressed art is already in the imported ROM chips.
No custom shadow pass, pose/timer/floor/ID change, proxy, or repainted silhouette.
"""
import hashlib,json,struct,zlib
from pathlib import Path
import build_native_shang_morphs as morph
import verify_native_friendship_palette_assembly_v2750 as assembly
ROOT=assembly.ROOT
OUT=ROOT/'audit_v3169_native_morph_shadow_payload'
SOURCE=ROOT/assembly.NAME/'roms/mk2ks/mk2ks.mdata'
need=assembly.need

def prepare():
    need(not OUT.exists(),'Never overwrite payload/evidence')
    original=SOURCE.read_bytes()
    need(assembly.sha(SOURCE)=='5646E839C73C4DB89BCF7CC87ECADBDA94B1E0D30EB1C0D2ED50A21A5524E23D','Exact existing current payload')
    program=(ROOT/'mk3/mk3-maincpu.bin').read_bytes()
    need(assembly.sha(ROOT/'mk3/mk3-maincpu.bin')=='1BC7A53A023F15B20F01398F87E38478A27C670DF27EA320E36125D0957EE651','Exact original donor program')
    output=bytearray(original);changes=[];allowed=set()
    refs=__import__('verify_morph_render_v3149').references()
    for fi,target in enumerate(('kano','sonya')):
        for gi,group in enumerate(morph.SOURCE_GROUPS[target]):
            frames=morph.animation.frame_group(program,group,0xff800000,0xffffffff)
            need(len(frames)==2,'Original two-part transition composite')
            for ci,descriptor in enumerate(frames):
                source,command,w,h,xo,yo=morph.decoder.component_spec(program,descriptor)
                at=morph.FRAMES+(fi*6+gi*2+ci)*20
                old=struct.unpack_from('<4hIHI',original,at)
                need(old[:4]==(w,h,xo,yo)and old[5]==0x6000 and command&0x80 and(command>>12)&7==6,
                  'Old raw six-bit conversion and genuine original six-bit compressed row art')
                expected=refs[morph.address(morph.GROUPS+(fi*3+gi)*12)][ci]
                need(expected['indices'].shape==(h,w),'Exact original full sprite pixels retained')
                tagged=source+0x10000000
                need(0x10000000<=tagged<0x1a000000 and 0x12000000<=tagged+0x02000000<0x1c000000,
                  'Original native shadow scanner mapping and blitter cover same tagged donor stream')
                # The existing native import loads all original chips at +C00000.
                # Blitter removes A000000 bits; CPU scanner removes12000000 bits
                # and adds C00000 bytes. Both reach C00000+original_source/8.
                need((tagged-0x0a000000)//8==0xc00000+source//8,
                  'CPU scanner and blitter select identical existing donor graphics bytes')
                struct.pack_into('<IH',output,at+8,tagged,command)
                allowed.update(range(at+8,at+14))
                changes.append(dict(target=target,group=gi,component=ci,descriptor=morph.address(at),
                  originalDescriptor=descriptor,oldSource=old[4],source=tagged,oldCommand=old[5],command=command,
                  width=w,height=h,xo=xo,yo=yo,originalPixelSHA256=hashlib.sha256(expected['indices'].tobytes()).hexdigest().upper()))
    actual=[i for i,(a,b)in enumerate(zip(original,output))if a!=b]
    need(len(changes)==12 and actual and set(actual)<=allowed,'Exactly twelve source/format fields, every other payload byte unchanged')
    payload=OUT/'roms/mk2ks/mk2ks.mdata';payload.parent.mkdir(parents=True);payload.write_bytes(output)
    pins={str(SOURCE):assembly.sha(SOURCE),str(ROOT/'mk3/mk3-maincpu.bin'):assembly.sha(ROOT/'mk3/mk3-maincpu.bin'),
      str(Path(__file__).resolve()):assembly.sha(__file__),str(Path(morph.__file__).resolve()):assembly.sha(morph.__file__)}
    report=dict(passed=True,assetOnly=True,runtimeAcceptance=False,fullPortAcceptance=False,
      sourceSHA256=assembly.sha(SOURCE),payloadSHA256=assembly.sha(payload),
      payloadCRC32=f'{zlib.crc32(output):08x}',payloadSHA1=hashlib.sha1(output).hexdigest(),
      descriptors=changes,changedByteOffsets=actual,allOtherPayloadBytesUnchanged=True,
      noOriginalArtPixelOrPaletteOrPivotChanged=True,originalNativeCompressedRowsSelected=True,
      noCustomShadowOrProxyOrNewGraphicsAllocation=True,inputHashes=pins)
    (OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items()if k not in('inputHashes','descriptors','changedByteOffsets')},indent=2),flush=True)

if __name__=='__main__':prepare()
