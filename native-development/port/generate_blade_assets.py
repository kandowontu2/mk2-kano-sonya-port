"""Native blade body/control data plus single-object compressed trail records."""
import hashlib
import json
import re
import import_character_art as art

HERE=art.HERE

def main():
    out=HERE/'generated_blade'
    assert not out.exists()
    out.mkdir()
    imported=(HERE/'generated_packed/KANOART.ASM').read_text()
    frames=[0xffb182d0,0xffb18360,0xffb183d0,0xffb18440,0xffb184b0,
            0xffb18520,0xffb18590,0xffb18600,0xffb18670,0xffb186e0]
    body=[0xff82fc40+i*0x60 for i in range(10)]
    advances=[0,8,8,8,11,11,11,0,0,0]
    lines=['; Own blade scripts; compressed graphics already reside in native ROM sockets.',
           '        .include mainequ.asm','        .ref ks_blade_fx_step,ks_knife_palette']
    lines+=['        .ref ks_kano_pose_'+f'{a:08x}' for a in body]
    lines+=['        .def ks_blade_animation','        .data','ks_blade_animation']
    for i,(address,advance) in enumerate(zip(body,advances)):
        assert f'.def ks_kano_pose_{address:08x}\n' in imported
        if advance:lines+=['        .long ani_adjustx',f'        .word {advance}']
        lines += [f'        .long ani_calla,ks_blade_fx_step,ks_blade_fx_{i}',
                  f'        .long ks_kano_pose_{address:08x}']
        if i in (4,7,9):lines+=['        .long 0']
    records=[]
    for i,address in enumerate(frames):
        match=re.search(rf'^ks_kano_frame_{address:08x}\n((?:        \.(?:word|long) [^\n]+\n){{4}})',imported,re.M)
        assert match,address
        record=match[1].replace('ks_kano_primary_palette','ks_knife_palette')
        assert 'ks_knife_palette' in record
        lines += [f'ks_blade_fx_{i}',record.rstrip()]
        records.append(dict(sourceFrame=hex(address),record=record))
    source=('\n'.join(lines)+'\n').encode()
    (out/'KSBANI.ASM').write_bytes(source)
    (out/'BLADE_ASSETS.json').write_text(json.dumps(dict(
        sourceSHA256=hashlib.sha256(source).hexdigest().upper(),
        bodyPoses=[hex(a) for a in body],xAdvances=advances,
        phaseHolds=[2,4,4],middlePhaseExtraHold=8,
        records=records,graphicsReusedWithoutRuntimeConversion=True,
        runtimeVerified=False),indent=2)+'\n')
    print(out)
if __name__=='__main__':main()
