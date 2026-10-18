"""Compare preparation output entirely in memory; never overwrite live sources."""
import difflib
import hashlib
import json
import re
from pathlib import Path
import prepare_game_candidate as prepare

PORT=Path(__file__).resolve().parent
generated=prepare.main(audit=True)
normalize=lambda b:b.replace(b'\r\n',b'\n')
sha=lambda b:hashlib.sha256(b).hexdigest().upper()
def structural_signature(data):
    """Triage only: not a substitute for assembly/link byte comparison."""
    declarations=set();body=[]
    for line in normalize(data).decode('latin-1').replace('\x1a','').splitlines():
        if line.lstrip().startswith(('*',';')):
            continue
        quote=None;clean=[]
        for char in line:
            if char in ('"',"'"):
                if quote==char:quote=None
                elif quote is None:quote=char
            if char==';' and quote is None:break
            clean.append(char)
        text=''.join(clean).strip()
        if not text:continue
        declaration=re.fullmatch(r'\.(ref|def)\s+(.+)',text,re.I)
        if declaration:
            declarations.update((declaration[1].lower(),name.strip()) for name in declaration[2].split(','))
            continue
        tokens=re.findall(r'"[^"\n]*"|\'[^\'\n]*\'|[A-Za-z0-9_.$]+|[^\s]',text)
        # Keep literal data values ordered but permit adjacent data rows to
        # wrap differently. Symbol spelling and expression tokens stay exact.
        directive=re.fullmatch(r'\.(word|long|byte)\s+([^"\']+)',text,re.I)
        if directive:
            for value in directive[2].split(','):
                body.append((directive[1].lower(),tuple(re.findall(r'[A-Za-z0-9_.$]+|[^\s]',value))))
        else:
            body.append(tuple(tokens))
    return sorted(declarations),body
matched=[];different=[];missing=[]
for name,data in sorted(generated.items()):
    target=prepare.DEST/name
    if not target.exists():
        missing.append(name);continue
    current=target.read_bytes()
    if normalize(current)==normalize(data):
        matched.append(name)
    else:
        diff=''.join(difflib.unified_diff(normalize(current).decode('latin-1').splitlines(True),
            normalize(data).decode('latin-1').splitlines(True),fromfile='current/'+name,tofile='regenerated/'+name))
        different.append(dict(file=name,currentSHA256=sha(current),regeneratedSHA256=sha(data),
            structuralTokensMatch=structural_signature(current)==structural_signature(data),diff=diff))
report=dict(scope='In-memory native source preparation closure, not compiled clean-build proof',
    generatedFiles=len(generated),matchedFiles=matched,differentFiles=different,missingFiles=missing,
    sourcePreparationReproducesCurrent=not different and not missing,
    structuralDifferences=[item['file'] for item in different if not item['structuralTokensMatch']],
    liveSourcesChanged=False,temporarySourceTreesCreated=False,cleanRebuildVerified=False,releaseReady=False)
(PORT/'SOURCE_REPRODUCTION_AUDIT.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(dict(generatedFiles=len(generated),matched=len(matched),
    different=[item['file'] for item in different],missing=missing,
    structuralDifferences=report['structuralDifferences'],
    sourcePreparationReproducesCurrent=report['sourcePreparationReproducesCurrent']),indent=2))
