"""Read-only source inventory before enabling IDs 17/18.

Candidate inventory, not a proof of exhaustive safety. Does not append guessed
rows or treat every byte/word as one character. Source locations and typed
table lengths remain visible for deliberate per-table integration.
"""
import json
import re
import zipfile
import hashlib
from pathlib import Path
import import_character_art as art
SRC=art.HERE.parent/'baseline/mk2-rebuild-main/srcw'
# These wrappers consume the same caller-supplied A0 character table.
# adjust_him_tbl selects the victim, not the attacker; both use 32-bit rows.
HELPERS={'get_char_word','get_char_long','get_his_char_word','get_his_char_long','ochar_jump','ochar_call',
         'adjust_him_tbl','ochar_do_or_rets'}

def instruction_code(row):
    """Respect GSPA column-zero labels without confusing indented operands."""
    code=row.split(';',1)[0].rstrip()
    if not code.strip() or code.lstrip().startswith(('*','\x1a')):
        return ''
    if re.match(r'^[A-Za-z_]\w*',code):
        code=re.sub(r'^[A-Za-z_]\w*:?\s*','',code,count=1)
    return code.strip().lower()
def source_tables(text):
    tables={}; current=None
    for n,row in enumerate(text.splitlines(),1):
        code=row.split(';',1)[0].rstrip()
        if not code.strip() or code.lstrip().startswith(('*','\x1a')): continue
        if re.match(r'^[A-Za-z_]\w*',code):
            m=re.match(r'^([A-Za-z_]\w*):?\s*(.*)',code)
            current=m[1];tables[current]=dict(line=n,rows=[],hasCode=False,conditional=False);code=m[2]
        if current and code.strip():
            m=re.match(r'\s*\.(word|long|byte)\s+(.+)',code,re.I)
            if m:tables[current]['rows'].append(dict(type=m[1].lower(),values=[x.strip() for x in m[2].split(',')],line=n))
            elif re.match(r'\s*\.(if|else|endif)',code,re.I): tables[current]['conditional']=True
            elif not code.lstrip().startswith('.'): tables[current]['hasCode']=True
    return {k:v for k,v in tables.items() if v['rows'] and not v['hasCode']}
def main():
    with zipfile.ZipFile('C:/Users/kando/Downloads/mk2-rebuild-main.zip') as z:
        names=[Path(n).name for n in z.namelist() if n.startswith('mk2-rebuild-main/src/') and n.count('/')==2 and n.upper().endswith('.ASM')]
    files={n:(SRC/n).read_text() for n in names}
    definitions={}; references=[]
    for name,text in files.items():
        for label,record in source_tables(text).items():
            record=dict(file=name,**record)
            record['typedBits']=sum({'word':16,'long':32,'byte':8}[r['type']]*len(r['values']) for r in record['rows'])
            definitions.setdefault(label,[]).append(record)
        recent=[]
        for line,row in enumerate(text.splitlines(),1):
            code=instruction_code(row)
            recent.append((line,code));recent=recent[-15:]
            match=re.match(r'(?:calla|callr|jauc)\s+(\w+)',code)
            if not match or match[1] not in HELPERS: continue
            candidates=[]
            for n,c in recent[:-1]:
                loaded=re.match(r'movi\s+([a-z_]\w*)\s*,\s*a0\b',c)
                if loaded:candidates.append((n,loaded[1]))
            references.append(dict(file=name,line=line,helper=match[1],
                nearestNamedA0Load=dict(line=candidates[-1][0],label=candidates[-1][1]) if candidates else None))
    wanted={r['nearestNamedA0Load']['label'] for r in references if r['nearestNamedA0Load']}
    wanted.update(['character_anitabs1','character_anitabs2','character_palettes_1','character_palettes_2',
                   'shadow_adjustments','stance_speeds','walk_forward_info','walk_backward_info'])
    indexed={label:definitions[label] for label in sorted(wanted) if label in definitions}
    result=dict(scope='Source candidates requiring individual interpretation, not an exhaustive safety proof',
        sourceFiles={name:hashlib.sha256((SRC/name).read_bytes()).hexdigest().upper() for name in sorted(files)},
        helperCalls=references,candidateTables=indexed,
        unresolvedNamedLoads=sorted(wanted-definitions.keys()),
        rowsAutomaticallyExtended=False,characterIDsSubstituted=False)
    output=art.HERE/'CHARACTER_TABLE_INVENTORY.json'
    output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(dict(helperCalls=len(references),candidateTables=len(indexed),
                         unresolvedNamedLoads=result['unresolvedNamedLoads']),indent=2))
if __name__=='__main__':main()
