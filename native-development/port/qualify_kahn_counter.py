"""Finite request-linked uppercut evidence; never a campaign-clear certificate."""
import csv
import hashlib
import json
from pathlib import Path
import re
import sys
import zipfile
from verify_finisher_roms import verify

PORT=Path(__file__).resolve().parent
BASE=PORT.parent/'baseline'
def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest().upper()

def profile(arguments):
    if '--campaign-kano-boss-guard' in arguments:
        assert '--sonya' not in arguments
        assert '--campaign-kano-human-prepare' in arguments and '--campaign-subzero-rfp-duck' in arguments
        return 17,True
    assert '--campaign-sonya-kahn-guard' in arguments and '--sonya' in arguments
    return 18,'--campaign-sonya-kahn-contact-ready' in arguments

def verify_request(row,contact_mode=False,contact_wake=None):
    assert row['chargeRoutine']=='1'
    if contact_mode:
        assert row['contactRecovery']=='1' and contact_wake is not None
        assert int(row['enemyWake'],16)==contact_wake
        assert int(row['distance'])<=105
    else:
        assert row['velocity']=='0' and int(row['distance'])<=140
    assert row['ownHeight']=='0' and int(row['ownFlags'])&0x1c==0
    assert 0<=int(row['bodyHeight'])<=96 and row['buttonTable']==row['duckTable']
    assert row['down']=='1' and row['block']=='0'

def request_window(index,frame):
    baseline=index.get(frame) or index.get(frame-1)
    assert baseline is not None
    context=(baseline['attempt'],baseline['round'])
    prior=baseline['p1action']
    entry=False
    cpu_drop=own_drop=0
    for delta in range(1,25):
        row=index.get(frame+delta)
        if row is None: continue
        if (row['attempt'],row['round'])!=context: break
        if delta<=8 and row['p1action']=='263' and prior!='263': entry=True
        prior=row['p1action']
        cpu_drop=max(cpu_drop,int(baseline['p2hp'])-int(row['p2hp']))
        own_drop=max(own_drop,int(baseline['p1hp'])-int(row['p1hp']))
    return dict(frame=frame,uppercutStateEntryWithin8=entry,
                opponentHealthDropWithin24=cpu_drop,ownHealthDropWithin24=own_drop)

def qualify(name):
    run=BASE/name
    receipt=json.loads((run/'execution.json').read_text())
    assert receipt['exitCode']==0 and not receipt['timedOut'], 'Incomplete runs are not qualified'
    assert not receipt['customDriver'] and not receipt['gameMemoryWrites']
    actor,contact_mode=profile(receipt['testArguments'])
    assert receipt['emulatorSHA256']=='AF6966108D9B52C22465C6D50F4E5D50CC371B50F2D27DC443935F287AAD37A3'
    observer=(run/'autoboot.lua').read_text()
    assert receipt['controllerSHA256']==sha(run/'autoboot.lua')
    assert ':write_u' not in observer and not re.search(r'\.value\s*=(?!=)',observer)
    assert '[LUA ERROR]' not in (run/'mame.log').read_text()
    with zipfile.ZipFile(run/'roms/mk3.zip') as archive: verify(archive,receipt)
    index={}
    with (run/'campaign.csv').open() as stream:
        for row in csv.DictReader(stream):
            assert int(row['missing'])==0
            if row['mode']=='2' and row['p2char']=='13':
                assert row['p1char']==row['p1selected']==str(actor) and row['p2selected']=='13'
                index[int(row['frame'])]=row
    with (run/'kahn_counter.csv').open() as stream:
        requests=[row for row in csv.DictReader(stream) if row['hp']=='1']
    assert index and requests
    contact_wake=None
    if contact_mode:
        src=BASE/'mk2-rebuild-main/srcp'
        symbols={n:int(a,16) for a,n in re.findall(r'\b([0-9a-fA-F]{8})\s+([A-Za-z_]\w*)',(src/'MK2P.MAP').read_text())}
        listing=(src/'MKBOSS.LST').read_text()
        def local(label):
            return int(re.search(r'^\s+\d+\s+([0-9a-fA-F]{8})\s+(?:[0-9a-fA-F]{4,8}\s+)?'+label+r'\b',listing,re.M)[1],16)
        origin=symbols['kahn_start']-local('kahn_start')
        sleeps=[int(m[1],16) for m in re.finditer(r'^\s+\d+\s+([0-9a-fA-F]{8})\s+sleep\s+020H\b',listing,re.M)
                if local('kahn_charge')<=int(m[1],16)<local('kahn_post_dont_walk')]
        assert len(sleeps)==1
        contact_wake=origin+sleeps[0]+0x50
    cases=[]
    for row in requests:
        verify_request(row,contact_mode,contact_wake)
        item=request_window(index,int(row['frame']))
        item['distance']=int(row['distance']);cases.append(item)
    pins=[run/name for name in ('execution.json','autoboot.lua','campaign.csv','kahn_counter.csv','mame.log')]
    pins.extend((Path(__file__).resolve(),PORT/'verify_finisher_roms.py'))
    if contact_mode: pins.extend(BASE/'mk2-rebuild-main/srcp'/name for name in ('MK2P.MAP','MKBOSS.LST','MKBOSS.ASM','MACROS.HDR'))
    report=dict(scope='Finite native Kahn counter requests, state entries and24-field health windows',
                actor=actor,physicalPlayer=1,
                current26ROMBytesVerified=True,requests=len(cases),contactRecoveryMode=contact_mode,
                uppercutStateEntriesWithin8=sum(c['uppercutStateEntryWithin8'] for c in cases),
                requestLinkedOpponentHealthDrops=sum(c['uppercutStateEntryWithin8'] and c['opponentHealthDropWithin24']>0 for c in cases),
                cases=cases,allHitsInterruptionsAudioQualified=False,
                campaignClearVerified=False,fullPortVerified=False,
                pins={str(path):sha(path) for path in pins})
    (run/'KAHN_COUNTER_QUALIFICATION.json').write_text(json.dumps(report,indent=2)+'\n')
    return {k:v for k,v in report.items() if k not in ('pins','cases')}

if __name__=='__main__':
    assert len(sys.argv)==2
    print(json.dumps(qualify(sys.argv[1]),indent=2))
