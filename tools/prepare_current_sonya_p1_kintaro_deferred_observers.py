"""Prepare only: defer diagnostic-only ROM read taps, preserve physical controller bytes."""
import json
import verify_native_source_sync as sync
sync.verify();root=sync.ROOT
base=root/'audit_current_sonya_p1_kintaro_low_airkick_preparation'
out=root/'audit_current_sonya_p1_kintaro_deferred_observers_preparation'
proof=root/'audit_current_sonya_p1_kintaro_deferred_observers_source_checked'
assert not out.exists() and not proof.exists()
original=(base/'campaign.lua').read_text()
end_start=original.index('for page=0,1 do\n')
end_end=original.index('emu.register_frame_done(function()',end_start)
ending=original[end_start:end_end]
special_start=original.index('for _,move in ipairs(own_moves)do\n')
special_end=original.index('for observed_slot,observed_hp in ipairs(',special_start)
special=original[special_start:special_end]
assert ending.count(':install_read_tap(')==2 and special.count(':install_read_tap(')==1
assert 'press(' not in ending+special and ':write_' not in ending+special
ending_head='local ending_taps_installed=false\nlocal function install_deferred_ending_taps()\n if ending_taps_installed then return end\n ending_taps_installed=true\n'
special_head='local special_taps_installed=false\nlocal function install_deferred_special_taps()\n if special_taps_installed then return end\n special_taps_installed=true\n'
source=original.replace(ending,ending_head+ending+'end\n',1).replace(special,special_head+special+'end\n',1)
marker=' local stage=p:read_u16(0x01061b30);local schedule=p:read_u32(0x01061b10)\n'
calls=' if stage==15 or stage==16 then install_deferred_special_taps()end\n if stage==16 then install_deferred_ending_taps()end\n'
assert source.count(marker)==1
source=source.replace(marker,marker+calls,1)
def gate(candidate):
 assert candidate.count(ending_head+ending+'end\n')==1 and candidate.count(special_head+special+'end\n')==1
 assert candidate.count(calls)==1
 restored=candidate.replace(ending_head+ending+'end\n',ending,1).replace(special_head+special+'end\n',special,1).replace(calls,'',1)
 assert restored==original
 assert ':write_' not in candidate and ':snapshot(' not in candidate
gate(source)
faults=[]
for name,broken in (
 ('physical_direction_changed',source.replace('boss_jump_direction=forward;boss_walk_last_x=nil','boss_jump_direction=back;boss_walk_last_x=nil',1)),
 ('ending_observer_reintroduced_cold',source.replace('emu.register_frame_done(function()','install_deferred_ending_taps()\nemu.register_frame_done(function()',1)),
 ('special_deferral_gate_removed',source.replace('if stage==15 or stage==16 then install_deferred_special_taps()end','install_deferred_special_taps()',1)),
):
 assert broken!=source
 try:gate(broken)
 except AssertionError:faults.append(name)
 else:raise AssertionError('Conservation fault accepted: '+name)
out.mkdir();lua=out/'campaign.lua';lua.write_text(source)
runner=(base/'run.ps1').read_text().replace(base.name+'/campaign.lua',out.name+'/campaign.lua').replace(sync.sha(base/'campaign.lua'),sync.sha(lua)).replace('audit_current_sonya_p1_kintaro_low_airkick_runtime','audit_current_sonya_p1_kintaro_deferred_observers_runtime')
(out/'run.ps1').write_text(runner)
report=dict(preparedOnlyNotRun=True,exactSourceConservationAfterUnwrapping=True,
 coldReadTapCountBefore=9,coldReadTapCountAfter=1,specialEntryTapsDeferredToStage15=4,endingTableTapsDeferredToStage16=4,
 coldWinnerTapPreserved=True,allNativeHealthAndPhysicalInputDigestCodeBytesPreserved=True,
 allControllerDependentCallbacksAndVariablesPreserved=True,rejectedFaults=faults,
 earlySpecialEntryObservationIntentionallyOmitted=True,
 speedupAccepted=False,runtimeEquivalenceAccepted=False,fullPortAccepted=False,
 baselineLuaSHA256=sync.sha(base/'campaign.lua'),preparedLuaSHA256=sync.sha(lua),
 scalarObserverSideEffects=dict(special=['log SPECIAL only'],ending=['picture_reads','text_reads','pending_pages']),
 futureRuntimeGate='Compare retained records excluding early SPECIAL through107553, exact physical input digests/FIGHT/WIN/LOSS/HEALTH; verify deferred observers install at stages15/16 before claiming their later coverage')
proof.mkdir();(proof/'report.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report))
