"""Read-only native selector table and full-priority rejection witness."""
import json
import verify_native_source_sync as sync

TAIL=r'''
local decline_taps={}
decline_taps[1]=p:install_read_tap(0xffa12530,0xffa1253f,'native general selector stock table',function(at)
 if not action_start or at~=0xffa12530 or cpu.PC.value~=at+16 then return end
 local cue=cpu.A0.value;assert(cue<254)
 print(string.format('MK2_ARM_SOUND_CALL frame=%d cue=%02X header=%04X packet=%04X a8=%08X a13=%08X writes=0 assistance=none',frame,cue,p:read_u16(0xffa0ef20+cue*32),p:read_u16(0xffa0ef20+cue*32+16),cpu.A8.value,cpu.A13.value))
end)
decline_taps[2]=p:install_read_tap(0xffa129d0,0xffa129df,'native full priority rejection',function(at)
 if not action_start or at~=0xffa129d0 or cpu.PC.value~=at+16 then return end
 print(string.format('MK2_ARM_SOUND_DECLINE frame=%d pc=%08X a0=%08X a1=%08X a3=%08X a4=%08X a8=%08X a13=%08X priority0=%d priority1=%d priority2=%d writes=0 assistance=none',frame,cpu.PC.value,cpu.A0.value,cpu.A1.value,cpu.A3.value,cpu.A4.value,cpu.A8.value,cpu.A13.value,p:read_u16(0x010b8100),p:read_u16(0x010b8140),p:read_u16(0x010b8180)))
end)
emu.register_stop(function()assert(#decline_taps==2)end)
'''

def main():
    sync.verify();old=sync.ROOT/'audit_bounded_jax_arms_voice_priority_preparation'
    out=sync.ROOT/'audit_bounded_sonya_p2_arm_priority_decline_preparation';assert not out.exists();out.mkdir()
    target=out/'prepared_observer.lua';target.write_text((old/'prepared_observer.lua').read_text()+TAIL)
    runner=(old/'run_sonya_p2.ps1').read_text().replace(old.name,out.name)
    runner=runner.replace(sync.sha(old/'prepared_observer.lua'),sync.sha(target))
    runner=runner.replace('audit_bounded_sonya_p2_jax_arms_voice_priority_runtime','audit_bounded_sonya_p2_arm_priority_decline_runtime')
    (out/'run.ps1').write_text(runner)
    (out/'report.json').write_text(json.dumps(dict(prepared=True,observerSha256=sync.sha(target),acceptance=False)))

if __name__=='__main__':main()
