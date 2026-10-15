"""Notrun: cold physical mirror, ordinary motion then release; naturalCPUlaser."""
import json,difflib
import verify_native_source_sync as sync
sync.verify();root=sync.ROOT;base=root/'audit_current_sonya_adaptive_ring_smoke_preparation'
out=root/'audit_current_cpu_laser_four_png_preparation';assert not out.exists()
old=(base/'campaign.lua').read_text();s=old
s=s.replace('local smoke_plan,smoke_forward,smoke_entry,smoke_recovered=nil,nil,nil,nil','local smoke_plan,smoke_forward,smoke_entry,smoke_recovered=nil,nil,nil,nil\nlocal visual_start,visual_winner,visual_motion=nil,nil,nil\nlocal visual_pending,visual_captured={},{}')
s=s.replace('if frame>=4000 then','if frame>=16000 then').replace('maximum_fields=4000','maximum_fields=16000')
start=s.index('  if winner==0 and human.hp>0 and other.hp>0 then');end=s.index(' if first_live and stage==16',start)
s=s[:start]+"""  if winner==0 and human.hp>0 and other.hp>0 and not visual_start then
   visual_motion=visual_motion or frame;local age=frame-visual_motion
   if age>=10 and age<20 then press('Right')end
   if age>=50 and age<54 then press('Up')end
   if age>=80 and age<84 then press('High Punch')end
   if age>=90 and age<180 then press('Block')end
  end
 else visual_motion=nil
 end
"""+s[end:]
s=s[:s.index('emu.register_frame_done(function()if smoke_recovered')]
s+="""
local function laser_pair()
 local k,h=sample(2),sample(1)
 return k and h and k.id==17 and k.roster==17 and k.state==0 and k.owner==k.actor and h.id==17 and h.roster==17 and h.state==1 and h.owner==h.actor,k,h
end
taps[#taps+1]=p:install_read_tap(0xffd85800,0xffd8580f,'actualnaturalCPUlaserentry',function(at)
 if at~=0xffd85800 or cpu.PC.value~=0xffd85810 or visual_start then return end
 local ok,k,h=laser_pair();if not ok or cpu.A8.value~=k.actor or cpu.A13.value~=k.main then return end
 assert(h.hp==0 and k.hp>0);visual_start=frame
 log('VISUAL_LASER_ENTRY',string.format('actor=%08X main=%08X owner=%08X victim=%08X victim_main=%08X id=%d victim_id=%d cpu_state=%d victim_state=%d hp=%d,%d pc=%08X',k.actor,k.main,k.owner,h.actor,h.main,k.id,h.id,k.state,h.state,k.hp,h.hp,cpu.PC.value))
end)
taps[#taps+1]=p:install_write_tap(0x01d01030,0x01d0103f,'naturalCPUlaserphasewords',function(at,data,mask)
 if not visual_start or at~=0x01d01030 or mask~=0xffff or data<0x6b40 or data>0x6b44 then return end
 local ok,k,h=laser_pair();if not ok or cpu.A8.value~=k.actor or cpu.A13.value~=k.main then return end
 log('VISUAL_LASER_PHASE',string.format('cue=%04X pc=%08X actor=%08X main=%08X victim=%08X victim_main=%08X palettes=%04X,%04X poses=%08X,%08X hp=%d,%d',data,cpu.PC.value,k.actor,k.main,h.actor,h.main,k.bank,h.bank,k.pose,h.pose,k.hp,h.hp))
 local label=({[0x6b40]='charge',[0x6b41]='beam',[0x6b43]='burst'})[data]
 if label and not visual_captured[label]then visual_pending[frame+4]=label end
end)
taps[#taps+1]=p:install_read_tap(0xffa14860,0xffa1486f,'actualCPUlaserwinner',function(at)
 if not visual_start or visual_winner or at~=0xffa14860 or cpu.PC.value~=0xffa14870 then return end
 local k=sample(2);if k and cpu.A8.value==k.actor and cpu.A13.value==k.main then visual_winner=frame;visual_pending[frame+60]='postscene';log('VISUAL_LASER_WINNER','main='..string.format('%08X',k.main))end
end)
emu.register_frame_done(function()
 if not visual_start then return end
 if(frame-visual_start)%10==0 or visual_pending[frame]then
  for n=1,2 do local a=sample(n);if a then log('VISUAL_LASER_ACTOR',string.format('slot=%d actor=%08X main=%08X owner=%08X id=%d roster=%d state=%d hp=%d pose=%08X palette=%04X x=%d y=%d floor=%d body=%04X trail=%08X',n,a.actor,a.main,a.owner,a.id,a.roster,a.state,a.hp,a.pose,a.bank,a.x,a.y,a.floor,a.body,a.trail))end end
 end
 local label=visual_pending[frame]
 if label and not visual_captured[label]then
  visual_captured[label]=true;local count=0;for _ in pairs(visual_captured)do count=count+1 end;assert(count<=4)
  log('VISUAL_LASER_CAPTURE','label='..label..' start='..visual_start..' mode='..p:read_u16(0x010601d0)..' actors='..string.format('%08X,%08X',p:read_u32(slots[1].actor),p:read_u32(slots[2].actor)))
  screen:snapshot(assert(os.getenv('MK2KS_LASER_PNG_DIR'))..'/'..label..'.png')
 end
 if visual_captured.postscene or frame-visual_start>=850 then log('VISUAL_LASER_COMPLETE','started='..visual_start..' winner='..(visual_winner or-1));manager.machine:exit()end
end)
"""
assert ':write_'not in s and s.count('screen:snapshot(')==1 and ':pixels('not in s
out.mkdir();lua=out/'campaign.lua';lua.write_text(s)
runner=(base/'run.ps1').read_text().replace(base.name+'/campaign.lua',out.name+'/campaign.lua').replace(sync.sha(base/'campaign.lua'),sync.sha(lua)).replace('audit_current_sonya_adaptive_ring_smoke_runtime','audit_current_cpu_laser_four_png_runtime').replace("$env:MK2KS_TEST_FIGHTER='sonya'","$env:MK2KS_TEST_FIGHTER='kano'").replace("$env:MK2KS_TEST_BOOT_FRAME='600'","$env:MK2KS_TEST_BOOT_FRAME='600'\n$env:MK2KS_LASER_PNG_DIR=$taskCase").replace('Elapsed.TotalSeconds -gt 90','Elapsed.TotalSeconds -gt 180').replace("rawMedia='none'","rawMedia='max4bounded400x254PNGs total256KiB; no rawbuffers'")
(out/'run.ps1').write_text(runner)
(out/'source.json').write_text(json.dumps(dict(preparedNotRun=True,LuaSHA256=sync.sha(lua),physicalOnly=True,forceCPU=False,inputs='ColdP1Kano nativeP2Kano mirror, normalpaidcontinues; Right10..19/Up50..53/HP80..83/Block90..179 thenreleased, resetmotionperactualvalidmatch. Nohumanfinishercommand.',retainedPhysicalTimingSource='mk2ks_native_kano_laser_cpu_motion.lua',media='max4PNG400254total256KiB charge/beam/burst/postscene',limits='16000fields180sec320MiB10MiB',phaseScope='ActualCPUlaserentryrequiresnativeP2state0true17/Mainowner/humanhp0; actual6B40/41/43sameownerphaseword+4fields drivesimages; postsceneactualnativewinner+60 candidate notactorretirementautomatically.',targetUnobservedIfNoNaturalCPULaser=True,fullPortAccepted=False),indent=2))
print(out,sync.sha(lua))
