"""Current-source helper/table candidates; never infer exhaustive reachability."""
import hashlib
import json
from pathlib import Path
import re
from inventory_character_tables import source_tables,HELPERS,instruction_code

PORT=Path(__file__).resolve().parent
SRC=PORT.parent/'baseline/mk2-rebuild-main/srcp'
definitions={};references=[];source_hashes={}
for path in sorted(SRC.glob('*.ASM')):
    text=path.read_text();source_hashes[path.name]=hashlib.sha256(path.read_bytes()).hexdigest().upper()
    for label,table in source_tables(text).items():
        definitions.setdefault(label,[]).append(dict(file=path.name,**table))
    recent=[]
    for line,row in enumerate(text.splitlines(),1):
        code=instruction_code(row)
        recent.append((line,code));recent=recent[-15:]
        match=re.match(r'(?:calla|callr|jauc)\s+(\w+)',code)
        if not match or match[1] not in HELPERS:continue
        loads=[]
        for number,instruction in recent[:-1]:
            loaded=re.match(r'movi\s+([a-z_]\w*)\s*,\s*a0\b',instruction)
            if loaded:loads.append((number,loaded[1]))
        references.append(dict(file=path.name,line=line,helper=match[1],
            strideBits=16 if match[1].endswith('_word') else 32,
            candidate=loads[-1][1] if loads else None,
            candidateLoadLine=loads[-1][0] if loads else None))
short=[];covered=[];unresolved=[]
for reference in references:
    label=reference['candidate'];tables=definitions.get(label,[])
    if len(tables)!=1:
        unresolved.append(reference);continue
    table=tables[0]
    bits=sum({'word':16,'long':32,'byte':8}[row['type']]*len(row['values']) for row in table['rows'])
    record=dict(**reference,tableFile=table['file'],tableLine=table['line'],typedBits=bits,
        capacityAtCandidateStride=bits//reference['strideBits'],conditional=table['conditional'],
        requiresManualDataflowAndReachabilityReview=True)
    (covered if bits>=19*reference['strideBits'] else short).append(record)
report=dict(scope='Nearest named A0 helper loads in current source, candidate audit only',
    sourceSHA256=source_hashes,helperCalls=len(references),shortCandidates=short,
    capacityCoveredCandidates=covered,unresolvedReferences=unresolved,
    arbitraryIndexedLoadsCovered=False,exhaustiveSafetyVerified=False,
    rowsAutomaticallyExtended=False,gameCodeChanged=False,releaseReady=False)
(PORT/'CURRENT_CHARACTER_TABLE_AUDIT.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(dict(helperCalls=len(references),shortCandidates=short,
    capacityCoveredCandidates=len(covered),unresolvedReferences=len(unresolved),exhaustiveSafetyVerified=False),indent=2))
