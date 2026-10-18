"""Read native split pose geometry and synchronization, without donor pixels."""
import json
import re
from pathlib import Path
from ingestion_contract import number
from inventory_character_tables import source_tables
from build_inflation_assets import sha

PORT=Path(__file__).resolve().parent
SRC=PORT.parent/'baseline/mk2-rebuild-main/srcp'


def extract():
    source=(SRC/'MKDEATH.ASM').read_text()
    tables=source_tables(source)
    headers={}
    for label,values in re.findall(r'(?m)^(\w+):\s*\n\s*\.word\s+([^\r\n]+)',(SRC/'MKSPLIT.TBL').read_text()):
        values=[number(v) for v in values.split(';',1)[0].split(',')]
        if len(values)==4:headers[label]=values
    sequences={}
    for actor,label in (('liu','a_lk_split'),('female_ninja','a_fn_split')):
        script=[v for row in tables[label]['rows'] for v in row['values']]
        assert len(script)==12 and [i for i,v in enumerate(script) if v=='0']==[3,11]
        poses=[]
        for phase,group in enumerate(v for v in script if v!='0'):
            components=[v for row in tables[group]['rows'] for v in row['values']]
            assert components[-1]=='0'
            pieces=[headers[v] for v in components[:-1]]
            left=min(-x for w,h,x,y in pieces)
            top=min(-y for w,h,x,y in pieces)
            right=max(w-x for w,h,x,y in pieces)
            bottom=max(h-y for w,h,x,y in pieces)
            poses.append(dict(phase=phase,group=group,part='together' if phase<3 else 'peel',
                headers=pieces,unionBounds=[left,top,right,bottom],
                width=right-left,height=bottom-top,xOffset=-left,yOffset=-top))
        sequences[actor]=poses
    reaction=source.split('\nr_split_in_2\n',1)[1].split('\nsplit_in_2_tab\n',1)[0]
    assert re.search(r'mmfm\s+sp,a8,a9\s*\n\s*move\s+a9,a11',reaction)
    assert re.search(r'movk\s+6,a0\s*\n\s*jsrp\s+double_mframew',reaction)
    return dict(format='MK2KS-VERTICAL-SPLIT-CONTRACT-1',sequences=sequences,
        initialPoseHold=64,remainingTogetherFrameDelay=5,togetherToPeelHold=16,peelFrameDelay=6,
        togetherPoseCount=3,peelPoseCount=7,twoZeroTerminators=True,
        secondaryObjectCreatedFromStance=True,secondaryPeelPointerReplacedByRestoredPrimaryPointer=True,
        originalUsesSamePeelScriptOnBothObjects=True,secondaryObjectFlipped=True,
        ownStanceReplacementRequiredByThisContract=False,
        asymmetricOwnHalvesMayUseSeparateSynchronizedScripts=True,
        geometryOnly=True,donorPixelsCopied=False,runtimeAcceptance=False,
        sourceSHA256={name:sha((SRC/name).read_bytes()) for name in ('MKDEATH.ASM','MKSPLIT.TBL')})


if __name__=='__main__':
    report=extract()
    (PORT/'SPLIT_NATIVE_CONTRACT.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k not in ('sequences','sourceSHA256')},indent=2))
