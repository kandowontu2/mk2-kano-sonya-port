"""Passive pre-handoff native throw checkpoint and loaded instruction words."""
import json,struct
import verify_native_source_sync as sync
sync.verify()
base=sync.ROOT/'audit_current_sonya_p2_baraka_hk_throw_onset_preparation'
out=sync.ROOT/'audit_current_sonya_p2_baraka_prethrow_trace_preparation'
assert not out.exists()
source=(base/'campaign.lua').read_text()
marker='-- Observe actual own special entries independently of intended button plans.'
assert source.count(marker)==1
extra="""taps[#taps+1]=p:install_read_tap(0xff8b6c60,0xff8b6c6f,'passive original throw before handoff',function(at)
 if at~=0xff8b6c60 or p:read_u16(0x01061b30)~=6 then return end
 local h,c=sample(2),sample(1)
 if not h or not c or h.id~=18 or h.roster~=18 or c.id~=3 or c.roster~=3 or cpu.A8.value~=c.actor or cpu.A13.value~=c.main or h.owner~=h.actor or c.owner~=c.actor then return end
 log('BARAKA_PRETHROW',string.format('pc=%08X a8=%08X a13=%08X cpu_actor=%08X cpu_main=%08X human_actor=%08X human_main=%08X gap=%d height=%d action=%d flags=%04X body=%04X hardware=%04X lowhardware=%04X kick_age=%d ring_age=%d health=%d,%d',cpu.PC.value,cpu.A8.value,cpu.A13.value,c.actor,c.main,h.actor,h.main,math.abs(h.x-c.x),h.floor-h.y,h.action,h.flags,h.body,p:read_u16(0x01600000),p:read_u16(0x01600020),sh_start and frame-sh_start or -1,sr_start and frame-sr_start or -1,h.hp,c.hp))
end)
"""
source=source.replace(marker,extra+marker)
addresses=[0xff8b6f30,0xff8b6f40,0xff8b6f50,0xff842850,0xff842860,0xff842870,0xff842880,0xff842890,0xff8428c0,0xff8428d0,0xff8428f0,0xff842900]
rom=sync.ROOT/'mk2/mk2-maincpu.bin'
with rom.open('rb') as stream:
    words=[]
    for address in addresses:
        stream.seek((address-0xff800000)//8);words.append(dict(address=f'{address:08X}',value=struct.unpack('<H',stream.read(2))[0]))
source+="\nemu.register_frame(function()\n if frame==300 then\n  for _,address in ipairs({"+','.join('0x'+r['address'] for r in words)+"})do log('THROW_HANDOFF_WORD',string.format('address=%08X value=%04X',address,p:read_u16(address)))end\n end\nend)\n"
assert ':write_' not in source and ':snapshot(' not in source
out.mkdir();lua=out/'campaign.lua';lua.write_text(source)
(out/'original-words.json').write_text(json.dumps(dict(originalROM_SHA256=sync.sha(rom),words=words),indent=2)+'\n')
runner=(base/'run.ps1').read_text().replace(base.name+'/campaign.lua',out.name+'/campaign.lua').replace(sync.sha(base/'campaign.lua'),sync.sha(lua)).replace('audit_current_sonya_p2_baraka_hk_throw_onset_runtime','audit_current_sonya_p2_baraka_prethrow_trace_runtime')
(out/'run.ps1').write_text(runner)
print('Unchanged controls/passive prethrow+12loaded words;70k ceiling/still90sec/320MiB/10MiB/no media')
