"""UNEXECUTED two-line Jax8 guard change; native jump/leg and all other controls retained."""
import json
import verify_native_source_sync as sync
sync.verify();root=sync.ROOT
base=root/'audit_current_sonya_p2_jax_deferred_ground_taps_preparation'
out=root/'audit_current_sonya_p2_jax_standing_guard_preparation';assert not out.exists()
original=(base/'campaign.lua').read_text()
start=original.index("   elseif fighter=='sonya' and side==2 and other.roster==11 and stage==8 then")
end=original.index("   elseif fighter=='sonya' and side==2 and other.roster==17 and stage==7 then",start+1)
old=original[start:end]
first="    elseif other.flags&0x10~=0 then\n     press('Down');press('Block')"
second="    else press('Down');press('Block')end"
assert old.count(first)==old.count(second)==1
new=old.replace(first,"    elseif other.flags&0x10~=0 then\n     press('Block')").replace(second,"    else press('Block')end")
source=original[:start]+new+original[end:]
def gate(candidate):
    assert candidate.count(new)==1 and candidate.replace(new,old)==original
    assert "if age<7 then press('Down')end" in new and "if age>=3 and age<7 then press('Low Punch');press('Block')end" in new
    assert 'jgl_until=frame+40' in new and 'frame-jgl_jump>=4' in new
    assert ':write_' not in candidate and ':snapshot(' not in candidate
gate(source);faults=[]
for label,bad in [('changed leg Down chord',source.replace("if age<7 then press('Down')end","if age<6 then press('Down')end",1)),('changed jump guard40',source.replace('jgl_until=frame+40','jgl_until=frame+41',1)),('lost standing default guard',source.replace(new,new.replace("else press('Block')end","else press('Down');press('Block')end",1),1))]:
    try:gate(bad)
    except AssertionError:faults.append(label)
    else:raise AssertionError('Source mutation admitted')
out.mkdir();lua=out/'campaign.lua';lua.write_text(source)
runner=(base/'run.ps1').read_text().replace(base.name+'/campaign.lua',out.name+'/campaign.lua').replace(sync.sha(base/'campaign.lua'),sync.sha(lua)).replace('audit_current_sonya_p2_jax_deferred_ground_taps_runtime','audit_current_sonya_p2_jax_standing_guard_runtime')
(out/'run.ps1').write_text(runner)
report=dict(prepared=True,emulatorLaunched=False,runtimeAcceptance=False,fullPortAcceptance=False,
            solePhysicalChange='Two stage8-only non-leg guard/default lines remove Down; retain Block. Ground-pound jump priority, short leg chord, deferred native observers and other stages identical.',
            evidence='audit_current_jax_guard_jump_windows_checked/report.json',proposedConservedPrefix=101525,
            effectiveSourceFaultsRejected=faults,luaSHA256=sync.sha(lua),limits=dict(wallSeconds=180,memoryMiB=320,textMiB=10,media=False,guestWrites=False))
(out/'preparation.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
