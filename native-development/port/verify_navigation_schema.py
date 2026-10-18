"""Check the explicit selector graph and geometry; not runtime integration."""
import hashlib
import json
import re
from pathlib import Path
HERE=Path(__file__).resolve().parent
def main():
    source=HERE/'asm/KSNAV.ASM'
    arrays={}; current=None
    for row in source.read_text().splitlines():
        code=row.split(';',1)[0].strip()
        if re.fullmatch(r'ks_\w+',code):current=code;arrays[current]=[]
        elif code.startswith('.word '):arrays[current]+=[int(x.strip(),0) for x in code[6:].split(',')]
    ids=arrays['ks_menu_ids'];inverse=arrays['ks_id_menu'];coords=arrays['ks_selection_xy']
    assert len(ids)==14 and len(set(ids))==14 and set(ids)==set(range(12))|{17,18}
    assert len(inverse)==19 and len(coords)==38
    xy=list(zip(coords[::2],coords[1::2]));assert len({xy[i] for i in ids})==14
    assert all(inverse[identity]==index for index,identity in enumerate(ids))
    assert all(inverse[i]==-1 for i in range(12,17))
    cases=[]
    for direction in ('up','down','left','right'):
        mapping=arrays[f'ks_{direction}_change'];sans=arrays[f'ks_{direction}_sans']
        assert len(mapping)==19 and sans[0]==len(sans)-1
        assert set(sans[1:])=={i for i,dest in enumerate(mapping) if i==dest}
        for identity in ids:
            dest=mapping[identity];assert dest in ids
            dx=xy[dest][0]-xy[identity][0];dy=xy[dest][1]-xy[identity][1]
            cases.append(dict(direction=direction,currentID=identity,nextID=dest,dx=dx,dy=dy,allowed=dest!=identity))
    assert arrays['ks_right_change'][9]==18 and arrays['ks_left_change'][18]==9
    assert arrays['ks_right_change'][17]==1 and arrays['ks_left_change'][1]==17
    assert next(c for c in cases if c['direction']=='down' and c['currentID']==17)['dx']==60
    assert next(c for c in cases if c['direction']=='down' and c['currentID']==18)['dx']==-60
    report=dict(passedStaticSchema=True,sourceSHA256=hashlib.sha256(source.read_bytes()).hexdigest().upper(),
        selectableCharacters=14,directionalCases=56,nativeHelperRuntimeVerified=False,
        selectorIntegrationVerified=False,onePressReptileSonyaAdjacency=True,
        absoluteCoordinateDeltaRequired=True,cases=cases)
    (HERE/'NAVIGATION_SCHEMA.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k!='cases'},indent=2))
if __name__=='__main__':main()
