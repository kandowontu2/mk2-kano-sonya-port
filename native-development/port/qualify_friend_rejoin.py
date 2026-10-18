"""Physical post-Friendship rejoin; bounded state/audio-request cleanup only."""
import csv
import hashlib
import json
from pathlib import Path
import re
import sys
import zipfile
from current_graphics import verify_archive_sockets

PORT=Path(__file__).resolve().parent;BASE=PORT.parent/'baseline';SRC=BASE/'mk2-rebuild-main/srcp'
sha=lambda data:hashlib.sha256(data).hexdigest().upper()
for name in sys.argv[1:]:
    run=BASE/name;receipt=json.loads((run/'execution.json').read_text())
    assert receipt['exitCode']==0 and not receipt['timedOut']
    assert not receipt['customDriver'] and not receipt['gameMemoryWrites']
    assert '--friend-rejoin' in receipt['testArguments']
    observer=(run/'autoboot.lua').read_text()
    assert sha((run/'autoboot.lua').read_bytes())==receipt['controllerSHA256']
    assert ':write_u' not in observer and '[LUA ERROR]' not in (run/'mame.log').read_text()
    with zipfile.ZipFile(run/'roms/mk3.zip') as archive:
        for lane,chip in enumerate(('mk321u54.bin','mk321u63.bin')):
            assert archive.read(chip)==b''.join((SRC/f'rom/P12{part}.{lane}').read_bytes() for part in ('F8','FC'))
        verify_archive_sockets(archive)
        for chip in range(2,6):
            assert archive.read(f'l1_mortal_kombat_3_u{chip}_music_spch.u{chip}')==(SRC.parent/f'soundp/U{chip}.ROM').read_bytes()
    events=list(csv.DictReader((run/'friend_rejoin_events.csv').open()))
    assert [event['phase'] for event in events]==['selection','combat']
    selection,start=(int(event['frame']) for event in events)
    rows=list(csv.DictReader((run/'friend.csv').open()))
    active=[row for row in rows if row['death']=='7'];assert len(active)==176
    assert any(row['death']=='65535' and int(row['frame'])<selection for row in rows)
    fresh=[row for row in rows if int(row['frame'])>=start]
    assert len(fresh)==600 and int(fresh[-1]['frame'])==start+599
    assert all(row['mode']=='2' and row['death']=='0' and row['winner']=='0' for row in fresh)
    assert all(row['p1char']=='18' and row['p2char']=='17' for row in fresh)
    assert fresh[0]['p1hp']==fresh[0]['p2hp']=='161'
    assert any(int(row['p2hp'])<161 for row in fresh)
    assert all(row['missing']=='0' for row in rows)
    writes=list(csv.DictReader((run/'native_sound_writes.csv').open()))
    clucks=[int(high['frame']) for high,low in zip(writes,writes[1:])
            if 2036<=(((int(high['data'],16)&255)<<8)|(int(low['data'],16)&255))<=2047]
    assert clucks and max(clucks)<selection
    report=dict(scope='One physical fresh match after completed Friendship',run=name,
        selectionFrame=selection,freshMatchFrame=start,freshCombatFields=600,
        correctOwnIdentities=True,fullStartingHealth=True,combatDamageObserved=True,
        newCluckRequestsAfterSelection=0,allProcessesPalettesAndAudibleTailsVerified=False,
        campaignVerified=False,releaseReady=False)
    (run/'FRIEND_REJOIN_QUALIFICATION.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report))
