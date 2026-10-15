"""Pin eight finite current-executable special results without release promotion."""
import json
from pathlib import Path
import verify_native_source_sync as sync
names={
 'knife':'audit_bounded_current_knife_cycles_checked',
 'ring':'audit_bounded_current_ring_cycles_checked',
 'blade':'audit_bounded_current_blade_cycles_checked',
 'choke':'audit_bounded_current_choke_ticks_checked',
 'ball':'audit_bounded_current_ball_cycles_checked',
 'bicycle':'audit_bounded_current_bicycle_followup_damage_checked',
 'square':'audit_bounded_current_square_air_contact_checked',
 'leg':'audit_bounded_current_leg_cycles_checked'}
out=sync.ROOT/'audit_bounded_current_special_cycles_sealed';assert not out.exists()
results={};input_hashes={}
observer=sync.ROOT/'audit_bounded_current_special_cycles_preparation/cycles.lua'
observer_hash=sync.sha(observer)
for move,name in names.items():
    path=sync.ROOT/name/'report.json';report=json.loads(path.read_text())
    assert report['passed'] and report['fullGoalComplete'] is False
    assert set(report['results'])=={'P1','P2'}
    for side in (1,2):
        case=report['results'][f'P{side}']
        folder=sync.ROOT/(f'audit_bounded_current_square_air_cycles_p{side}_runtime' if move=='square' else f'audit_bounded_current_special_cycles_{move}_p{side}_runtime')
        assert sync.sha(folder/'run.log')==case['logSHA256']
        terminal=json.loads((folder/'terminal.json').read_text())
        assert terminal==case['terminal'] and terminal['observerSha256']==observer_hash
        assert terminal['exitCode']==0 and terminal['limitReason'] is None and terminal['rawMedia']=='none'
        assert terminal['peakWorkingSetBytes']<320*1024**2 and terminal['logBytes']<10*1024**2
        assert case['physicalCommands']==2 and case['settledIdle']
        input_hashes[str(folder/'run.log')]=case['logSHA256']
        input_hashes[str(folder/'terminal.json')]=sync.sha(folder/'terminal.json')
    input_hashes[str(path)]=sync.sha(path)
    results[move]=dict(results=report['results'],scope=report['scope'],reportSHA256=sync.sha(path))
report=dict(passedFiniteMechanics=True,physicalContexts=16,actualSpecialCycles=32,results=results,
    inputHashes=input_hashes,observerSHA256=observer_hash,sourceSync=sync.verify(),checkerSHA256=sync.sha(Path(__file__)),
    scope='Eight current-build specials, both physical slots, two activations each versus Kitana; square contact uses genuine opponent jumps. Native identity, collisions and normal follow-up/recovery. Not all moves, blocked/missed/CPU/mirror/arena/KO states, full raster, audio quality, campaign/endings or complete port.',
    publicBuildPromoted=False,fullGoalComplete=False)
out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(dict(passedFiniteMechanics=True,contexts=16,cycles=32,publicBuildPromoted=False)))
