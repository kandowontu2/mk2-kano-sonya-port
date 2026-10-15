"""Prepare only: restore proven default apex kicks, retain staged diagnostic observers."""
import json
import verify_native_source_sync as sync
sync.verify();root=sync.ROOT
base=root/'audit_current_sonya_p1_kintaro_deferred_observers_preparation'
default=root/'audit_current_sonya_p1_boss_light_preparation'
out=root/'audit_current_sonya_p1_default_kick_deferred_preparation'
proof=root/'audit_current_sonya_p1_default_kick_deferred_source_checked'
assert not out.exists() and not proof.exists()
source=(base/'campaign.lua').read_text();baseline=(default/'campaign.lua').read_text()
clamped="if kick_vy>=kick_vy_min and kick_vy<0x80000000 and (stage~=15 or(height<=60 and gap<=100)) and frame%6<3 then press('High Kick')end"
original="if kick_vy>=kick_vy_min and kick_vy<0x80000000 and frame%6<3 then press('High Kick')end"
assert source.count(clamped)==1 and baseline.count(original)==1
source=source.replace(clamped,original,1)
ending_head='local ending_taps_installed=false\nlocal function install_deferred_ending_taps()\n if ending_taps_installed then return end\n ending_taps_installed=true\n'
special_head='local special_taps_installed=false\nlocal function install_deferred_special_taps()\n if special_taps_installed then return end\n special_taps_installed=true\n'
ending=baseline[baseline.index('for page=0,1 do\n'):baseline.index('emu.register_frame_done(function()')]
special=baseline[baseline.index('for _,move in ipairs(own_moves)do\n'):baseline.index('for observed_slot,observed_hp in ipairs(')]
calls=' if stage==15 or stage==16 then install_deferred_special_taps()end\n if stage==16 then install_deferred_ending_taps()end\n'
def stage16(text):
 a=text.index('    if stage==16 then\n');b=text.index('    elseif quiet then',a)
 return a,b,text[a:b]
a,b,fixed_ring=stage16(source);c,d,old_ring=stage16(baseline)
assert "press(fighter=='sonya'and'Low Punch'or'High Punch')" in fixed_ring and "projectile_direction=fighter=='sonya'and forward or back" in fixed_ring
def gate(candidate):
 assert candidate.count(ending_head+ending+'end\n')==1 and candidate.count(special_head+special+'end\n')==1 and candidate.count(calls)==1
 restored=candidate.replace(ending_head+ending+'end\n',ending,1).replace(special_head+special+'end\n',special,1).replace(calls,'',1)
 x,y,ring=stage16(restored);assert ring==fixed_ring
 restored=restored[:x]+old_ring+restored[y:]
 assert restored==baseline
 assert candidate.count(original)==1 and clamped not in candidate
 assert ':write_' not in candidate and ':snapshot(' not in candidate
gate(source);faults=[]
for name,broken in (
 ('reintroduced_low_kick_clamp',source.replace(original,clamped,1)),
 ('physical_jump_direction_changed',source.replace('boss_jump_direction=forward;boss_walk_last_x=nil','boss_jump_direction=back;boss_walk_last_x=nil',1)),
 ('Sonya_ring_wrong_button',source.replace("press(fighter=='sonya'and'Low Punch'or'High Punch')","press('High Punch')",1)),
):
 assert broken!=source
 try:gate(broken)
 except AssertionError:faults.append(name)
 else:raise AssertionError('Conservation fault accepted')
out.mkdir();lua=out/'campaign.lua';lua.write_text(source)
runner=(base/'run.ps1').read_text().replace(base.name+'/campaign.lua',out.name+'/campaign.lua').replace(sync.sha(base/'campaign.lua'),sync.sha(lua)).replace('audit_current_sonya_p1_kintaro_deferred_observers_runtime','audit_current_sonya_p1_default_kick_deferred_runtime')
(out/'run.ps1').write_text(runner)
report=dict(preparedOnlyNotRun=True,defaultStage15PhysicalControllerExactlyConserved=True,
 wholeSourceExactlyRestoredToBossLightAfterDiagnosticUnwrapAndExplicitStage16RingRestoration=True,
 correctedStage16SonyaRingRetained=True,coldReadTaps=1,specialTapsDeferred15=4,endingTapsDeferred16=4,
 rejectedFaults=faults,preparedLuaSHA256=sync.sha(lua),defaultBaselineLuaSHA256=sync.sha(default/'campaign.lua'),
 runtimePrefixAcceptance=False,winningRouteAccepted=False,fullPortAccepted=False,
 futureGate='Exact retained preboss107553 and default111442 history, excludeonlyearlySPECIAL; same-paid two native boss rounds, never combine continued isolated wins')
proof.mkdir();(proof/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
