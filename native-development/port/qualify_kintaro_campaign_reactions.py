"""Sampled earned-campaign Kintaro slam body coverage, not full choreography."""
import csv
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys

PORT=Path(__file__).resolve().parent
BASE=PORT.parent/'baseline'
SRC=BASE/'mk2-rebuild-main/srcp'
FLAGS=(subprocess.CREATE_NO_WINDOW|subprocess.BELOW_NORMAL_PRIORITY_CLASS) if sys.platform=='win32' else 0

def digest(path):
    value=hashlib.sha256()
    with path.open('rb') as stream:
        while chunk:=stream.read(65536):value.update(chunk)
    return value.hexdigest().upper()

def check(script,*arguments):
    result=subprocess.run([sys.executable,str(PORT/script),*arguments],cwd=PORT,
                          capture_output=True,text=True,creationflags=FLAGS)
    assert result.returncode==0,result.stderr[-2000:]

def main(names):
    assert len(names)==2 and len(set(names))==2
    check('qualify_kintaro_reaction_source.py')
    source_proof=PORT/'generated_roster_roots/KINTARO_SOURCE_QUALIFICATION.json'
    symbols={name:int(address,16) for address,name in re.findall(r'\b([0-9a-fA-F]{8})\s+([A-Za-z_]\w*)',(SRC/'MK2P.MAP').read_text())}
    cases=[];evidence=[Path(__file__),PORT/'audit_campaign_run.py',PORT/'campaign_budget.py',
        PORT/'qualify_kintaro_reaction_source.py',source_proof,SRC/'MK2P.MAP',SRC/'KSREACT.ASM',SRC/'MKBOSS.ASM']
    for name in names:
        assert Path(name).name==name and '/' not in name and '\\' not in name
        check('audit_campaign_run.py',name)
        run=BASE/name
        audit=json.loads((run/'CAMPAIGN_AUDIT.json').read_text())
        actor=audit['actor'];assert actor in (17,18) and audit['currentFullROMVerified']
        label,poses=('kano',('ff8294a0','ff829940','ff8299a0')) if actor==17 else ('sonya',('ff836860','ff837060','ff8370c0'))
        expected={symbols[f'ks_{label}_pose_{pose}'] for pose in poses}
        own={address for symbol,address in symbols.items() if symbol.startswith(f'ks_{label}_pose_')}
        observed=set();fields=0;episodes=0;previous=None
        with (run/'campaign.csv').open() as stream:
            for row in csv.DictReader(stream):
                if row['mode']!='2' or row['p2char']!='12' or row['p2action']!='1287':continue
                assert row['p1char']==row['p1selected']==str(actor)
                assert row['p2selected']=='12' and row['missing']=='0'
                frame=int(row['frame']);context=(row['attempt'],row['map'],row['round'])
                if previous is None or previous[0]!=context or frame!=previous[1]+2:episodes+=1
                previous=(context,frame)
                shape=int(row['p1shape'],16);assert shape in own
                fields+=1;observed.add(shape)
        assert fields>0 and expected<=observed
        cases.append(dict(run=name,actor=actor,victimSide=1,sampledSlamFields=fields,
            sampledActionTagEpisodes=episodes,scriptPoseDescriptorsObserved=len(expected),
            allSampledBodiesOwn=True,allSixStepTimingAndCoordinatesVerified=False))
        evidence.extend(run/item for item in ('execution.json','autoboot.lua','CAMPAIGN_AUDIT.json','campaign.csv'))
    assert {case['actor'] for case in cases}=={17,18}
    report=dict(scope='Sampled physical-player1 victim bodies during native Kintaro507h campaign action',
        sourceAndLinkedScriptRequalified=True,cases=cases,bothVictimSidesVerified=False,
        fullChoreographyVisuallyAccepted=False,fullPortVerified=False,pins={str(path):digest(path) for path in evidence})
    (PORT/'generated_roster_roots/KINTARO_CAMPAIGN_REACTIONS.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({key:value for key,value in report.items() if key!='pins'},indent=2))

if __name__=='__main__':main(sys.argv[1:])
