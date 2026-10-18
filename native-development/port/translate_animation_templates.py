"""Translate native control source to independent, own-art animation scripts.

Preserves symbolic MKII control tokens and phase delimiters from the supplied
source. Only explicitly matched donor roles are emitted; uncovered dispatch
entries remain reported rather than silently aliasing another fighter.
"""
import re
import json
import hashlib
import zipfile
import argparse
from pathlib import Path
import import_character_art as art

HERE=art.HERE
SRC=HERE.parent/'baseline/mk2-rebuild-main/srcw'
OUT=HERE/'generated_templates_bound'
p=art.parser
def parse_source(path):
    blocks={}; aliases={}; current=None; labels=[]
    for number,row in enumerate(path.read_text().splitlines(),1):
        code=row.split(';',1)[0].rstrip()
        if not code.strip() or code.lstrip().startswith(('*','\x1a')): continue
        if code[0].isalpha() or code[0]=='_':
            m=re.match(r'([A-Za-z_]\w*):?\s*(.*)',code)
            if not m: raise ValueError((number,row))
            current=m[1]; labels.append(current); blocks[current]=[]; code=m[2]
        if not current or not code.strip(): continue
        m=re.match(r'\s*\.(long|word)\s+(.+)',code,re.I)
        if m: blocks[current].append((m[1].lower(),m[2].strip(),number))
        elif code.strip().lower()!='.end': raise ValueError(('Not typed animation data',number,code))
    for index,name in enumerate(labels[:-1]):
        if not blocks[name]: aliases[name]=labels[index+1]
    return blocks,aliases
def canonical(name,aliases):
    seen=set()
    while name in aliases:
        assert name not in seen; seen.add(name); name=aliases[name]
    return name
def ids(expr): return re.findall(r'\b[A-Za-z_]\w*\b',expr)
def main():
    cli=argparse.ArgumentParser()
    cli.add_argument('--output',type=Path,default=OUT)
    args=cli.parse_args(); out=args.output.resolve()
    assert out.is_relative_to(HERE.resolve()) and not out.exists(), 'Use a fresh generation directory inside port'
    blocks,aliases=parse_source(SRC/'MKLK.ASM')
    frame_labels=set()
    for tbl in ('MKLK.TBL','MKLK2.TBL','MKLK3.TBL'):
        frame_labels.update(re.findall(r'^([A-Za-z_]\w*):', (SRC/tbl).read_text(),re.M))
    groups={name for name,rows in blocks.items() if any(x in frame_labels for _,expr,_ in rows for x in ids(expr))}
    roots={kind:[expr for directive,expr,_ in blocks[name] if directive=='long'] for kind,name in [('main','lk_anitab1'),('special','lk_anitab2')]}
    with zipfile.ZipFile(art.ROOT/'mk3.zip') as z:
        lo=z.read('mk321u54.bin'); hi=z.read('mk321u63.bin')
    data=bytearray(len(lo)+len(hi)); data[::2]=lo; data[1::2]=hi
    report=dict(nativeMainEntries=len(roots['main']),nativeSpecialEntries=len(roots['special']),
                sourceTemplateSHA256=hashlib.sha256((SRC/'MKLK.ASM').read_bytes()).hexdigest().upper(),fighters={})
    native_symbols={name for _,name in re.findall(r'\b([0-9a-fA-F]{8})\s+([A-Za-z_]\w*)',(SRC/'MK2NEW.MAP').read_text())}
    native_callbacks={'kick_sounds','sweep_sounds'}
    assert native_callbacks <= native_symbols
    out.mkdir()
    for fighter,main,special,block in [('kano',p.KANO_MAIN,p.KANO_SPECIAL,p.KANO_BLOCK),('sonya',p.SONYA_MAIN,p.SONYA_SPECIAL,p.SONYA_BLOCK)]:
        donor_roots={'main':main,'special':special}
        spans={kind:p.sequence_spans(data,root,block,(main,special)) for kind,root in donor_roots.items()}
        output=['; Generated from native control SOURCE, not executable opcode data.',
                '; Independent scripts, own poses, preserved native control tokens.',
                '        .include mainequ.asm','        .data']
        entries={}; missing=[]; refs=set(); definitions=set()
        # The explicitly researched mappings are authoritative for core moves.
        # Advanced victim/fatality roles require separate choreography, not guesses.
        roles=dict(p.STANDARD_ANIMATION_TRANSLATIONS)
        # Source MKLK's main 25h is a_shredded: the old prototype's
        # "short stumble" label is not an authoritative semantic mapping.
        roles.pop(37,None)
        roles[30]=(23,'ordinary forward/back jump kick')
        # Visual review of original MK3 main 35 proves it is the attacker's
        # throw, not the forward-fall role used in the old prototype's comment.
        roles[36]=(35,'body throw attacker, native grab/throw/getup phases')
        # Preserve MKII's actual per-attacker victim control/XY phases.
        # Where that attacker exists in MK3, select its original victim pose
        # family. Otherwise use the original generic front/back throw body
        # pose family; no character ID or control trajectory is substituted.
        roles.update({
            42:(47,'thrown by Kung Lao'),43:(51,'thrown by Liu Kang'),
            44:(38,'thrown by Johnny Cage, native trajectory/generic own throw poses'),
            45:(38,'thrown by Baraka, native trajectory/generic own throw poses'),
            46:(39,'thrown by Kitana, native trajectory/own female throw poses'),
            47:(39,'thrown by Mileena, native trajectory/own female throw poses'),
            48:(50,'thrown by Shang Tsung'),
            49:(38,'thrown by Raiden, native trajectory/generic own throw poses'),
            50:(42,'thrown by Sub-Zero'),51:(42,'thrown by Reptile, native trajectory/own ninja throw poses'),
            52:(52,'thrown by Scorpion, native trajectory/own ninja throw poses'),
            53:(40,'thrown by Jax'),
        })
        for index,(donor_index,role) in roles.items():
            root=canonical(roots['main'][index],aliases)
            if root not in blocks or root in groups:
                missing.append(dict(index=index,reason='not an ordinary native script',root=root)); continue
            rows=blocks[root]
            used=[]
            for _,expr,_ in rows:
                used += [canonical(x,aliases) for x in ids(expr) if canonical(x,aliases) in groups]
            used=p.ordered_unique(used)
            if not used:
                missing.append(dict(index=index,reason='no native composite poses',root=root)); continue
            donor_span=spans['main'].get(donor_index)
            if not donor_span:
                missing.append(dict(index=index,reason='missing explicit donor span',donor=donor_index)); continue
            poses=p.ordered_unique([a for _,a,_ in p.group_references(data,*donor_span,*block)])
            explicit=p.DONOR_SEQUENCE_GROUPS[fighter].get(('main',donor_index))
            if explicit: poses=list(explicit)
            if not poses:
                missing.append(dict(index=index,reason='missing own donor poses',donor=donor_index)); continue
            label=f'ks_{fighter}_main_{index:02x}'
            mapping={name:f'ks_{fighter}_pose_{p.map_by_position(poses,i,len(used)):08x}' for i,name in enumerate(used)}
            body=[]; unknown=set()
            for directive,expr,line in rows:
                def replace(m):
                    name=m[0]; resolved=canonical(name,aliases)
                    if resolved==root: return label
                    if resolved in mapping:
                        refs.add(mapping[resolved]); return mapping[resolved]
                    if name.startswith('ani_'): return name
                    if name in native_callbacks:
                        refs.add(name); return name
                    if resolved in blocks:
                        targets=[i for i,v in enumerate(roots['main']) if canonical(v,aliases)==resolved]
                        if targets:
                            target=f'ks_{fighter}_main_{targets[0]:02x}'
                            refs.add(target); return target
                    if name not in ('H','h'): unknown.add(name)
                    return name
                value=re.sub(r'\b[A-Za-z_]\w*\b',replace,expr)
                body.append(f'        .{directive} {value} ; native source line {line}')
            if unknown:
                missing.append(dict(index=index,reason='unresolved control dependency',names=sorted(unknown))); continue
            definitions.add(label)
            output += [f'        .def {label}',f'; Native main {index:02x}: {role}',label]+body
            entries[str(index)]=dict(label=label,nativeRole=role,sourceRoot=root,donorMainIndex=donor_index,
                                     nativePoses=len(used),donorPoses=len(poses))
        required={r for r in refs if '_main_' in r}
        unresolved=required-definitions
        for r in sorted(refs-definitions): output.insert(3,f'        .ref {r}')
        contents=('\n'.join(output)+'\n').encode()
        (out/f'{fighter.upper()}ANI.ASM').write_bytes(contents)
        report['fighters'][fighter]=dict(entries=entries,explicitMissing=missing,
            uncoveredMainIndices=sorted(set(range(len(roots['main'])))-{int(x) for x in entries}),
            unresolvedScriptDependencies=sorted(unresolved),
            sourceSHA256=hashlib.sha256(contents).hexdigest().upper(),complete=False)
    (out/'TRANSLATION.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(nativeMainEntries=report['nativeMainEntries'],fighters={k:dict(emitted=len(v['entries']),unresolved=v['unresolvedScriptDependencies'],missing=v['explicitMissing']) for k,v in report['fighters'].items()}),indent=2))
if __name__=='__main__': main()
