"""Not run: physical P1Sonya / scheduledKano; generic owned battle audio."""
import json,difflib
import verify_native_source_sync as sync
sync.verify();root=sync.ROOT;base=root/'audit_current_combined_smoke_v2_preparation'
out=root/'audit_current_combined_sonya_smoke_preparation';assert not out.exists()
old=(base/'campaign.lua').read_text();s=old
needle="elseif age>=85 and age<88 then press(backward);if age>=86 then press('High Punch')end"
assert s.count(needle)==1;s=s.replace(needle,"elseif age>=85 and age<88 then press(forward);if age>=86 then press('Low Punch')end")
start=s.index('local audio_items,audio_channels,audio_launch,audio_signature=')
end=s.index('local combined_captured={}',start)
audio="""local smoke_items,smoke_channels,smoke_launches={},{},{}
emu.register_frame(function()
 if frame~=1 then return end
 for name,index in pairs(manager.machine.devices[':'].items)do
  for _,field in ipairs({'actor','main','health','id','mode'})do
   if name:match('/m_mk2ks_battle_'..field..'$')then smoke_items[field]=emu.item(index)end
  end
 end
 for name,index in pairs(manager.machine.devices[':mk2ksvoices'].items)do
  local n,field=name:match('^(%x+)/chan%.(.+)$')
  if n and tonumber(n,16)>=10 and tonumber(n,16)<=13 then
   n=tonumber(n,16);smoke_channels[n]=smoke_channels[n]or{};smoke_channels[n][field]=emu.item(index)
  end
 end
 assert(smoke_items.actor and smoke_items.main and smoke_channels[10]and smoke_channels[13])
end)
taps[#taps+1]=p:install_write_tap(0x01d01030,0x01d0103f,'combined actual sound words',function(at,data,mask)
 if at~=0x01d01030 or mask~=0xffff then return end
 log('COMBINED_SOUND_WORD',string.format('word=%04X pc=%08X a8=%08X a13=%08X mode=%d',data&0xffff,cpu.PC.value,cpu.A8.value,cpu.A13.value,p:read_u16(0x010601d0)))
 if data<0x6b00 or data>0x6b03 then return end
 for n=1,2 do local a=sample(n)
  if a and(a.id==17 or a.id==18)and a.roster==a.id and a.owner==a.actor and a.hp>0 and cpu.A8.value==a.actor and cpu.A13.value==a.main then
   smoke_launches[n]={frame=frame,actor=a.actor,main=a.main,id=a.id}
   log('COMBINED_AUDIO_CUE',string.format('slot=%d cue=%04X pc=%08X actor=%08X main=%08X id=%d state=%d hp=%d action=%d',n,data,cpu.PC.value,a.actor,a.main,a.id,a.state,a.hp,a.action))
  end
 end
end)
emu.register_frame_done(function()
 for n,launch in pairs(smoke_launches)do if frame-launch.frame<=120 then
  local a=sample(n);local index=n-1
  log('COMBINED_AUDIO_OWNER',string.format('slot=%d launch=%d age=%d saved_actor=%08X saved_main=%08X saved_id=%d saved_mode=%d saved_hp=%d mode=%d guest_actor=%08X guest_main=%08X guest_id=%d roster=%d state=%d hp=%d',n,launch.frame,frame-launch.frame,smoke_items.actor:read(index),smoke_items.main:read(index),smoke_items.id:read(index),smoke_items.mode:read(index),smoke_items.health:read(index),p:read_u16(0x010601d0),a and a.actor or 0,a and a.main or 0,a and a.id or 0,a and a.roster or 0,a and a.state or -1,a and a.hp or 0))
  for channel=10+index*2,11+index*2 do local c=smoke_channels[channel]
   log('COMBINED_AUDIO_CHANNEL',string.format('slot=%d launch=%d age=%d channel=%d sample=%d length=%d pos=%.8f paused=%d loop=%d',n,launch.frame,frame-launch.frame,channel,c.source_num:read(0),c.source_len:read(0),string.unpack('<d',c.pos:read_block(0,8)),c.paused:read(0),c.loop:read(0)))
  end
 end end
end)
"""
s=s[:start]+audio+s[end:]
assert ':write_'not in s and s.count('screen:snapshot(')==1
out.mkdir();lua=out/'campaign.lua';lua.write_text(s)
runner=(base/'run.ps1').read_text().replace(base.name+'/campaign.lua',out.name+'/campaign.lua').replace(sync.sha(base/'campaign.lua'),sync.sha(lua)).replace('audit_current_combined_smoke_v2_runtime','audit_current_combined_sonya_smoke_runtime').replace("$env:MK2KS_TEST_FIGHTER='kano'","$env:MK2KS_TEST_FIGHTER='sonya'").replace("$env:MK2KS_CAMPAIGN_SIDE='2'","$env:MK2KS_CAMPAIGN_SIDE='1'")
assert "'-frameskip','0'" in runner and "'-snapsize','400x254'" in runner
(out/'run.ps1').write_text(runner)
(out/'source.json').write_text(json.dumps(dict(preparedNotRun=True,LuaSHA256=sync.sha(lua),physicalOnly=True,guestWrites=False,case='Cold physicalP1Sonya18 selects nativeCPU17 firststage',changes='Only RingD,F,LP insteadKnifeD,B,HP; P1Sonya runner; generic passive owned6B00..03/soundword observer bothslots',pngCountLimit=4,pngTotalByteLimit=262144,pngDimensions=[400,254],audioScope='Actualnativeport16bitwords, NOTADSPbyteconsumption or heardmix; actualbattleowner/length/pos/nonpaused sampled120fieldsaftereachownedcue. source_num sentinel notplayingpredicate; noassumedCPUballifnotobserved.',scope='One combined counterpart only; ladderphase pending actualpixelreview; attemptedwalk/jump notacceptedwithoutactivation.',sourceDiff=''.join(difflib.unified_diff(old.splitlines(True),s.splitlines(True)))),indent=2))
print(out,sync.sha(lua))
