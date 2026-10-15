"""UNEXECUTED trace-efficiency successor; every physical control byte retained."""
import json
import verify_native_source_sync as sync
sync.verify()
root=sync.ROOT;base=root/'audit_current_sonya_p2_jax_ground_jump_leg_preparation'
out=root/'audit_current_sonya_p2_jax_deferred_ground_taps_preparation';assert not out.exists()
original=(base/'campaign.lua').read_text()
start=original.index("for _,entry in ipairs({{0xff86dd90,'ground_entry'}")
end=original.index("for observed_slot,observed_hp in ipairs({0x010602f0,0x01060ec0})do",start)
block=original[start:end]
assert block.count("p:install_read_tap(address,address+15")==1 and block.count('human_jump')==3
wrapper='''local jax_native_taps_installed=false
local function install_owned_jax_native_taps()
'''+block+'''end
emu.register_frame(function()
 if jax_native_taps_installed or p:read_u16(0x01061b30)~=8 then return end
 local h,c=sample(2),sample(1)
 if not h or not c or h.id~=18 or h.roster~=18 or c.id~=11 or c.roster~=11 or h.owner~=h.actor or c.owner~=c.actor then return end
 jax_native_taps_installed=true;install_owned_jax_native_taps()
 log('JAX_NATIVE_TAPS_INSTALLED','stage=8 h_id=18 c_id=11 before_active_or_intro=true')
end)
'''
source=original[:start]+wrapper+original[end:]
def conservation(candidate):
    assert candidate.count(wrapper)==1
    assert candidate.replace(wrapper,block)==original
    assert "p:read_u16(0x01061b30)~=8" in wrapper and 'h.id~=18' in wrapper and 'c.id~=11' in wrapper
    assert 'h.owner~=h.actor or c.owner~=c.actor' in wrapper
    assert ':write_' not in candidate and ':snapshot(' not in candidate
conservation(source);faults=[]
for label,bad in [('changed physical ground-pound jump guard',source.replace('jgl_until=frame+40','jgl_until=frame+41',1)),
                  ('early wrong stage observer',source.replace(wrapper,wrapper.replace('~=8 then return end','~=7 then return end',1),1)),
                  ('lost deferred true CPU ownership',source.replace(wrapper,wrapper.replace('c.id~=11','c.id~=10',1),1))]:
    assert bad!=source
    try:conservation(bad)
    except AssertionError:faults.append(label)
    else:raise AssertionError('Source fault admitted')
out.mkdir();lua=out/'campaign.lua';lua.write_text(source)
runner=(base/'run.ps1').read_text().replace(base.name+'/campaign.lua',out.name+'/campaign.lua').replace(sync.sha(base/'campaign.lua'),sync.sha(lua)).replace('audit_current_sonya_p2_jax_ground_jump_leg_runtime','audit_current_sonya_p2_jax_deferred_ground_taps_runtime')
(out/'run.ps1').write_text(runner)
report=dict(prepared=True,emulatorLaunched=False,runtimeAcceptance=False,fullPortAcceptance=False,
            everyPhysicalControllerByteUnchanged=True,soleChange='Defer four passive ground/jump opcode-fetch taps until actual owned Jax11/Sonya18 actors exist at stage8; intro mode7 permitted so first ground entry can be retained.',
            baseline='audit_current_sonya_p2_jax_ground_jump_leg_runtime',baselinePrefixForNextCheck=101525,
            exactRemovedOriginalTapBlockSHA256=__import__('hashlib').sha256(block.encode()).hexdigest().upper(),
            effectiveSourceFaultsRejected=faults,luaSHA256=sync.sha(lua),
            originalSourceSHA256=sync.sha(base/'campaign.lua'),
            limits=dict(wallSeconds=180,memoryMiB=320,textMiB=10,media=False,guestWrites=False),
            caveat='Current third-round end sample alone does not prove an action20/flag10 guard stall. This is unexecuted observation-overhead optimization, not a demonstrated speedup or match clear. Future strict checks must exclude only newly added JAX_NATIVE_TAPS_INSTALLED tag and require native initial Carry skip retained.')
(out/'preparation.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
