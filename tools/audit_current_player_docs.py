"""Current launcher/doc correspondence; no game or release promotion."""
import json
import verify_native_source_sync as sync
sync.verify()
out=sync.ROOT/'audit_current_player_docs_checked'
assert not out.exists()
readme=(sync.ROOT/'PLAYTEST_README.txt').read_text()
moves=(sync.ROOT/'MK2_KANO_SONYA_MOVES.txt').read_text()
head=readme.split('HISTORICAL NOTES BELOW:',1)[0]
assert 'diagnostic_native_selector_layers_long' in head
assert 'PLAY_CURRENT_NATIVE_CHECKED.cmd' in head and 'PLAY_MK2_KANO_SONYA.cmd' in head
assert 'v635' not in head and 'PLAY_LATEST_TEST_BUILD.cmd' not in head
commands=["pulse(side,'Down',age,0,3)","move=='knife'and backward or forward",
          "(move=='knife'or move=='blade')and'High Punch'or'Low Punch'",
          "pulse(side,'Low Kick',age,0,84)",
          "pulse(side,backward,age,0,3);pulse(side,backward,age,6,3);pulse(side,'Down',age,12,3);pulse(side,'High Kick',age,13,3)",
          "pulse(side,'Down',age,0,7);pulse(side,'Low Punch',age,3,4);pulse(side,'Block',age,3,4)",
          "pulse(side,forward,age,0,3);pulse(side,backward,age,5,3);pulse(side,'High Punch',age,6,3)"]
controller=sync.ROOT/'audit_bounded_current_special_cycles_preparation/cycles.lua'
text=controller.read_text();assert all(c in text for c in commands)
sealed=sync.ROOT/'audit_bounded_current_special_cycles_sealed/report.json'
proof=json.loads(sealed.read_text())
assert proof['passedFiniteMechanics'] and proof['actualSpecialCycles']==32
assert set(proof['results'])=={'knife','ring','blade','choke','ball','bicycle','square','leg'}
assert 'airborne opponent' in moves and 'grounded-target tests did not deal damage' in moves
package=sync.ROOT/'release_current_native_playtest_20261013_complete_roms/MK2_Kano_Sonya_CURRENT_NATIVE_PLAYTEST_20261013_complete_roms.zip'
assert sync.sha(package)=='EDAC17A71DC7353ABC35C32D914E8248DB7804DCA6F9AA3A24B9B25EDF2797B7'
report=dict(passed=True,currentLauncherDocumented=True,historicalInstructionsSeparated=True,
            verifiedSpecialCommandsDocumented=8,packageUnchanged=True,newGameRuns=0,
            fullPortAccepted=False,longerRunApprovalPending=True,
            hashes={p.name:sync.sha(p) for p in [sync.ROOT/'PLAYTEST_README.txt',sync.ROOT/'MK2_KANO_SONYA_MOVES.txt',controller,sealed,package]})
out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
