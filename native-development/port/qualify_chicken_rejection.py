"""Negative physical-input audio gate; not an exhaustive eligibility proof."""
import csv
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import zipfile
from current_sound import verify_latest_playlist

PORT=Path(__file__).resolve().parent;BASE=PORT.parent/'baseline';BUILD=BASE/'mk2-rebuild-main'
sha=lambda data:hashlib.sha256(data).hexdigest().upper()
verify_latest_playlist()
for name in sys.argv[1:]:
    folder=BASE/name;receipt=json.loads((folder/'execution.json').read_text())
    assert {'--friend','--punch-wins','--sound-candidate'}<=set(receipt['testArguments'])
    assert receipt['exitCode']==0 and not receipt['timedOut']
    assert not receipt['customDriver'] and not receipt['gameMemoryWrites']
    assert receipt['controllerSHA256']==sha((folder/'autoboot.lua').read_bytes())
    check=subprocess.run([sys.executable,str(PORT/'qualify_sonya_friend.py'),name],
                         capture_output=True,text=True,timeout=30,
                         creationflags=getattr(subprocess,'CREATE_NO_WINDOW',0))
    assert check.returncode==0,check.stdout+check.stderr
    behavior=json.loads(check.stdout)
    assert behavior['punchEligibilityRejected'] and behavior['nativeActionFields']==0
    with zipfile.ZipFile(folder/'roms/mk3.zip') as archive:
        for chip in range(2,6):
            assert archive.read(f'l1_mortal_kombat_3_u{chip}_music_spch.u{chip}')==(BUILD/f'soundp/U{chip}.ROM').read_bytes()
    writes=list(csv.DictReader((folder/'native_sound_writes.csv').open()))
    codes=[((int(high['data'],16)&255)<<8)|(int(low['data'],16)&255)
           for high,low in zip(writes,writes[1:])]
    assert not any(2036<=code<=2047 for code in codes)
    report=dict(scope='Finite punch-wins rejected Friendship and no cluck port requests',
        run=name,physicalSide=behavior['physicalActorSide'],naturalKnockouts=behavior['naturalKnockouts'],
        friendshipActivated=False,cluckRequests=0,positiveControlRequired=True,
        exhaustiveEligibilityProof=False,fullPortVerified=False,releaseReady=False)
    (folder/'CHICKEN_REJECTION.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report))
