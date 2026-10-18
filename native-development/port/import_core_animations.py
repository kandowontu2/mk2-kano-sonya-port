"""Generate initial native MKII control scripts referencing own imported art.

Only explicitly translated roles are emitted. No missing animation silently
falls back to Liu Kang or to a stance. This is not a complete dispatch table.
"""
import import_character_art as art
import hashlib
import json
import zipfile
p=art.parser
HERE=art.HERE
def main():
    with zipfile.ZipFile(art.ROOT/'mk3.zip') as z:
        lo=z.read('mk321u54.bin'); hi=z.read('mk321u63.bin')
    source=bytearray(len(lo)+len(hi)); source[::2]=lo; source[1::2]=hi
    output=HERE/'generated_packed/KSANIM.ASM'
    assert not output.exists()
    lines=['; Typed native MKII animation control data, linked to own poses.',
           '; Incomplete dispatch coverage: see CORE_ANIMATIONS.json.',
           '        .include mainequ.asm','        .data']
    exported={}; refs=set()
    for fighter,root,special,block in [('kano',p.KANO_MAIN,p.KANO_SPECIAL,p.KANO_BLOCK),('sonya',p.SONYA_MAIN,p.SONYA_SPECIAL,p.SONYA_BLOCK)]:
        spans=p.sequence_spans(source,root,block,(root,special))
        for name,index,loop in [('stance',0,0),('walk_forward',1,0),('walk_backward',2,0),('crouch',4,None),('forward_flip',26,1),('backward_flip',27,1)]:
            poses=[address for _,address,_ in p.group_references(source,*spans[index],*block)]
            assert poses, (fighter,name)
            label=f'ks_{fighter}_{name}'
            lines += [f'        .def {label}',label]
            for address in poses:
                pose=f'ks_{fighter}_pose_{address:08x}'
                refs.add(pose); lines.append(f'        .long {pose}')
            lines += ['        .long 0' if loop is None else f'        .long ani_jump,{label}+{loop*32}']
            exported[label]=dict(nativeRole=name,donorMainIndex=index,poses=len(poses))
        at=p.stock_file(p.u32(source,p.stock_file(root)+22*4))
        poses=[p.u32(source,at+i*4) for i in range(3)]
        assert p.u32(source,at+12)==0 and all(p.frame_group(source,a,*block) for a in poses)
        label=f'ks_{fighter}_vertical_jump'
        lines += [f'        .def {label}',label]
        for index in (1,2,None,1,0,None):
            if index is None: lines.append('        .long 0')
            else:
                pose=f'ks_{fighter}_pose_{poses[index]:08x}'
                refs.add(pose); lines.append(f'        .long {pose}')
        exported[label]=dict(nativeRole='vertical_jump',donorMainIndex=22,phases=['middle,tucked','middle,first'])
    for pose in sorted(refs): lines.insert(3,f'        .ref {pose}')
    contents=('\n'.join(lines)+'\n').encode(); output.write_bytes(contents)
    report=dict(sourceSHA256=hashlib.sha256(contents).hexdigest().upper(),source='KSANIM.ASM',
                exported=exported,completeDispatchTable=False,missingAnimationFallback=False)
    (output.parent/'CORE_ANIMATIONS.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(exportedScripts=len(exported),poseReferences=len(refs),completeDispatchTable=False)))
if __name__=='__main__': main()
