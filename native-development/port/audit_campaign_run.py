"""Read-only finite campaign evidence. A loss/partial ladder is never completion."""
import collections
import csv
import hashlib
import json
import re
from pathlib import Path
import sys
import zipfile
from current_graphics import verify_archive_sockets
from campaign_rounds import split_rounds,native_round_wins,completed_native_matches,sampled_action_tag_episodes,require_clean_runtime_log
from native_roster import verified_names,provenance as roster_provenance
from campaign_budget import budget

PORT=Path(__file__).resolve().parent
BASE=PORT.parent/'baseline'
BUILD=BASE/'mk2-rebuild-main/srcp'
ROOT=PORT.parents[1]
sha=lambda b:hashlib.sha256(b).hexdigest().upper()
for name in sys.argv[1:]:
    folder=BASE/name
    receipt=json.loads((folder/'execution.json').read_text())
    assert receipt['exitCode']==0 and not receipt['timedOut']
    assert not receipt['customDriver'] and not receipt['gameMemoryWrites']
    controller=(folder/'autoboot.lua').read_bytes()
    assert sha(controller)==receipt['controllerSHA256']
    observer=controller.decode()
    assert ':write_u' not in observer and not re.search(r'\.value\s*=(?!=)',observer)
    assert receipt['emulatorSHA256']=='AF6966108D9B52C22465C6D50F4E5D50CC371B50F2D27DC443935F287AAD37A3'
    assert receipt['controllerSHA256']==sha((folder/'autoboot.lua').read_bytes())
    observer=(folder/'autoboot.lua').read_text()
    assert ':write_u' not in observer and not re.search(r'\.value\s*=(?!=)',observer)
    with zipfile.ZipFile(folder/'roms/mk3.zip') as archive:
        for lane,chip in enumerate(('mk321u54.bin','mk321u63.bin')):
            assert archive.read(chip)==b''.join((BUILD/f'rom/P12{p}.{lane}').read_bytes() for p in ('F8','FC'))
        verify_archive_sockets(archive)
        sound_folder='soundp' if '--sound-candidate' in receipt['testArguments'] else 'soundw'
        for chip in range(2,6):
            assert archive.read(f'l1_mortal_kombat_3_u{chip}_music_spch.u{chip}')==(BUILD.parent/sound_folder/f'U{chip}.ROM').read_bytes()
        with zipfile.ZipFile(ROOT/'roms/mk2.zip') as original:
            for bank,(first,second) in enumerate(((14,19),(16,20),(17,22))):
                for lane,(letter,socket) in enumerate((('ug',first),('uj',first),('ug',second),('uj',second))):
                    chip=133-bank*4-lane
                    assert archive.read(f'l1_mortal_kombat_3_u{chip}_game_rom.u{chip}')==original.read(
                        f'l1_mortal_kombat_ii_game_rom_{letter}{socket}.{letter}{socket}')
    rows=list(csv.DictReader((folder/'campaign.csv').open()))
    declared_budget=budget(receipt['testArguments'])
    continue_limit=declared_budget['continueLimit']
    assert 0<int(rows[-1]['frame'])<=declared_budget['fieldLimit']
    max_attempt=max(int(row.get('attempt','0')) for row in rows)
    assert max_attempt<=continue_limit
    continue_events=[]
    if (folder/'campaign_continues.csv').exists():
        continue_events=list(csv.DictReader((folder/'campaign_continues.csv').open()))
        for attempt in range(1,max_attempt+1):
            events=[event for event in continue_events if int(event['attempt'])==attempt]
            assert events and events[0]['phase']=='buyin'
            assert len([event for event in events if event['phase']=='combat'])<=1
            for event in events:
                if event['phase']=='combat':assert event['map']==events[0]['map'], 'Continue restarted a different ladder position'
    target=18 if '--sonya' in receipt['testArguments'] else 17
    control=next((arg for arg in receipt['testArguments'] if arg.startswith('--campaign-stock=')),None)
    if control:
        target=int(control.split('=',1)[1]);assert target in range(12)
    fight=[r for r in rows if r['mode']=='2']
    assert fight and all(int(r['p1char'])==target and int(r['p1selected'])==target for r in fight)
    assert max(int(r['missing']) for r in rows)==0
    symbols={n:int(a,16) for a,n in re.findall(r'\b([0-9a-fA-F]{8})\s+([A-Za-z_]\w*)',(BUILD/'MK2P.MAP').read_text())}
    assert all(int(r['pc'],16)!=symbols['illegal_opcode']+0x50 for r in rows)
    require_clean_runtime_log((folder/'mame.log').read_text())
    episodes=collections.Counter()
    opponent_episodes=sampled_action_tag_episodes(fight)
    previous=None
    rounds=split_rounds(fight)
    for r in fight:
        action=int(r['p1action'])
        if previous is None or action!=int(previous['p1action']): episodes[f'{action:04x}']+=1
        previous=r
    defeated=[]
    winning_rounds=native_round_wins(rows,rounds)
    completed_matches=completed_native_matches(winning_rounds)
    for position in sorted({int(r['map']) for r in rows}):
        stage=[r for r in rounds if r['map']==position]
        # A final hit can cross mode2 -> result mode between two sampled rows.
        # Require native winner/counter and terminal health, not mode2 HP alone.
        advanced=any(int(r['map'])>position for r in rows)
        if advanced:
            matches=[item for item in completed_matches if item['map']==position]
            assert len(matches)==1, 'Advancement without one same-attempt native match win'
            match=matches[0]
            defeated.append(dict(map=position,opponent=stage[0]['opponent'],naturalWinningRounds=2,
                successfulAttempt=match['attempt'],nativeResults=match['nativeResults']))
    ending=folder/'campaign_end.txt'
    termination=dict(line.split('=',1) for line in ending.read_text().splitlines()) if ending.exists() else None
    roster=verified_names(include_nonselectable=True)
    for item in rounds+defeated+winning_rounds:
        item['opponentName']=roster.get(item['opponent'],'UNKNOWN ID '+str(item['opponent']))
    report=dict(scope='Observed finite single-player attempt, not completion proof',
        actor=target,originalCharacterControl=control is not None,frames=int(rows[-1]['frame']),rounds=rounds,
        maxMapPosition=max(int(r['map']) for r in rows),
        lastMode=int(rows[-1]['mode']),lastWinner=int(rows[-1]['winner']),
        actionEpisodes=dict(episodes),naturallyDefeatedOpponents=defeated,nativeWinningRounds=winning_rounds,
        sampledActionTagEpisodesByOpponent={roster.get(actor,str(actor)):dict(counts) for actor,counts in opponent_episodes.items()},
        sampledActionTagEpisodeLimit='Observed tag changes/round starts, not recognized commands, hit counts or complete move activations; native tags may persist after interruption.',
        termination=termination,missingMarkers=0,illegalOpcodeRecoveryObserved=False,currentFullROMVerified=True,
        observedContinueAttempts=max_attempt,continueEvents=continue_events,declaredTestBudget=declared_budget,
        nativePaidContinuesAccepted=sum(event['phase']=='combat' for event in continue_events),
        nativeRosterNames=roster,nativeRosterSource=roster_provenance(),
        fullCampaignVerified=False,fullPortVerified=False)
    (folder/'CAMPAIGN_AUDIT.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(test=name,**report)))
