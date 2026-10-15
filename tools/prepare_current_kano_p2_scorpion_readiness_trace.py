"""Read-only scalar controller gate trace, identical physical inputs."""
import verify_native_source_sync as sync
sync.verify()
base=sync.ROOT/'audit_current_kano_p2_scorpion_crouch_ready_preparation'
out=sync.ROOT/'audit_current_kano_p2_scorpion_readiness_trace_preparation'
assert not out.exists()
source=(base/'campaign.lua').read_text()
marker="    if gap>100 and height<=8 and other.flags&0x10==0 then sc_down=nil;press(forward)"
assert source.count(marker)==1
extra="""    if frame%12==0 then
     log('SCORPION_READY',string.format('ready=%d height=%d flags=%04X body=%04X action=%d gap=%d down_age=%d upper_age=%d native_counter=%d hardware=%04X health=%d,%d',ready and 1 or 0,height,human.flags,human.body,human.action,gap,sc_down and frame-sc_down or -1,frame-sc_upper,p:read_u16(human.main+0x220),p:read_u16(0x01600000),human.hp,other.hp))
    end
"""
source=source.replace(marker,extra+marker)
assert ':write_' not in source and ':snapshot(' not in source
out.mkdir();lua=out/'campaign.lua';lua.write_text(source)
runner=(base/'run.ps1').read_text().replace(base.name+'/campaign.lua',out.name+'/campaign.lua').replace(sync.sha(base/'campaign.lua'),sync.sha(lua)).replace('audit_current_kano_p2_scorpion_crouch_ready_runtime','audit_current_kano_p2_scorpion_readiness_trace_runtime')
(out/'run.ps1').write_text(runner)
print('Passive readiness scalar every12fields;32000fields/90sec/320MiB/10MiB/no media')
