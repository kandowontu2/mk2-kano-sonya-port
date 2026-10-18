"""Dedicated native Sonya bicycle scripts; no ordinary move-slot replacement."""
import hashlib
import json
import import_character_art as art

HERE=art.HERE

def main():
    out=HERE/'generated_bike'
    assert not out.exists()
    out.mkdir()
    intro=[0xff83ea40,0xff83ea80,0xff83eae0]
    cycle=[0xff83eb40,0xff83eb80,0xff83ebc0,0xff83ec00,0xff83ec40,
           0xff83ec80,0xff83ec40,0xff83ec00,0xff83ebc0,0xff83eb80]
    end=list(reversed(intro))
    imported=(HERE/'generated_packed/SONYAART.ASM').read_text()
    refs={f'ks_sonya_pose_{a:08x}' for a in intro+cycle+end}
    assert all('.def '+r+'\n' in imported for r in refs)
    lines=['; Own bicycle body scripts, original compressed art and native control tokens.',
           '        .include mainequ.asm','        .ref ks_bike_push']
    lines+=['        .ref '+r for r in sorted(refs)]
    lines+=['        .def ks_bike_intro,ks_bike_cycle,ks_bike_end','        .data','ks_bike_intro']
    for a in intro:
        lines+=['        .long ani_calla,ks_bike_push','        .long ani_adjustxy',
                '        .word 5,10',f'        .long ks_sonya_pose_{a:08x}']
    lines+=['        .long 0','ks_bike_cycle']
    lines += [f'        .long ks_sonya_pose_{a:08x}' for a in cycle]
    lines+=['        .long ani_jump,ks_bike_cycle','ks_bike_end']
    lines += [f'        .long ks_sonya_pose_{a:08x}' for a in end]
    lines+=['        .long 0']
    source=('\n'.join(lines)+'\n').encode()
    (out/'KSBIANI.ASM').write_bytes(source)
    report=dict(sourceSHA256=hashlib.sha256(source).hexdigest().upper(),
                intro=[hex(a) for a in intro],cycle=[hex(a) for a in cycle],end=[hex(a) for a in end],
                introAdjustments=[5,10],nativeActorID=18,runtimeVerified=False)
    (out/'BIKE_ASSETS.json').write_text(json.dumps(report,indent=2)+'\n')
    print(out)
if __name__=='__main__': main()
