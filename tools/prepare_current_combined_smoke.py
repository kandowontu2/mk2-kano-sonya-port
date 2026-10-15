"""Prepare one physical P2Kano vs scheduled CPU18 combined smoke, not launch."""
import json,difflib
import verify_native_source_sync as sync
sync.verify();root=sync.ROOT
base=root/'audit_current_cpu_sonya_voice_earlier_upper_preparation'
out=root/'audit_current_combined_smoke_v2_preparation';assert not out.exists()
old=(base/'campaign.lua').read_text();s=old
begin=s.index('  if winner==0 and human.hp>0 and other.hp>0 then')
end=s.index(' if first_live and stage==16',begin)
s=s[:begin]+"""  if winner==0 and human.hp>0 and other.hp>0 then
   local age=frame-first_live
   local forward=human.x<other.x and 'Right'or'Left'
   local backward=forward=='Right'and'Left'or'Right'
   if age<60 then press('Block')
   elseif age>=60 and age<66 then press(backward)
   elseif age>=80 and age<83 then press('Down')
   elseif age>=85 and age<88 then press(backward);if age>=86 then press('High Punch')end
   elseif age>=190 and age<193 then press('Up')
   else press('Block')end
   log('COMBINED_CONTROL',string.format('age=%d action=%d gap=%d trueHuman=%d trueCPU=%d',age,human.action,math.abs(human.x-other.x),human.id,other.id))
  end
 end
"""+s[end:]
s+="""
local combined_captured={};local combined_total=0
emu.register_frame_done(function()
 local label=nil
 if css and frame-css==146 then label='selection'
 elseif css_exit and frame-css_exit==90 then label='ladder'
 elseif first_live and frame-first_live==5 then label='fight'
 elseif first_live and frame-first_live==350 then label='cleanup'end
 if label and not combined_captured[label]then
  combined_captured[label]=true;combined_total=combined_total+1;assert(combined_total<=4)
  log('COMBINED_CAPTURE','label='..label..' mode='..p:read_u16(0x010601d0)..' stage='..p:read_u16(0x01061b30)..' roster='..p:read_u16(slots[1].roster)..','..p:read_u16(slots[2].roster))
  screen:snapshot(assert(os.getenv('MK2KS_COMBINED_PNG_DIR'))..'/'..label..'.png')
 end
 if first_live and frame-first_live>=360 then log('COMBINED_COMPLETE','captures='..combined_total..' fullPortAcceptance=false');manager.machine:exit()end
end)
"""
assert ':write_'not in s and s.count('screen:snapshot(')==1
out.mkdir();lua=out/'campaign.lua';lua.write_text(s)
runner=(base/'run.ps1').read_text().replace(base.name+'/campaign.lua',out.name+'/campaign.lua').replace(sync.sha(base/'campaign.lua'),sync.sha(lua)).replace('audit_current_cpu_sonya_voice_earlier_upper_runtime','audit_current_combined_smoke_v2_runtime').replace("$env:MK2KS_TEST_FIGHTER='sonya'","$env:MK2KS_TEST_FIGHTER='kano'")
assert "'-frameskip','0'" in runner and "'-snapsize','400x254'" in runner
runner=runner.replace("$env:MK2KS_TEST_BOOT_FRAME='600'","$env:MK2KS_TEST_BOOT_FRAME='600'\n$env:MK2KS_COMBINED_PNG_DIR=$taskCase")
runner=runner.replace("$env:MK2KS_CAMPAIGN_STRATEGY='leg'","$env:MK2KS_CAMPAIGN_STRATEGY='uppercut'")
runner=runner.replace("$taskReport=[ordered]@{","$taskPNGs=@(Get-ChildItem -LiteralPath $taskCase -Filter '*.png'); if($taskPNGs.Count -gt 4 -or ($taskPNGs|Measure-Object -Property Length -Sum).Sum -gt 256KB){throw 'PNG budget exceeded'}\n$taskReport=[ordered]@{").replace("rawMedia='none'","rawMedia='four bounded400x254PNGs only; no raw media'")
(out/'run.ps1').write_text(runner)
(out/'source.json').write_text(json.dumps(dict(preparedNotRun=True,LuaSHA256=sync.sha(lua),physicalOnly=True,case='Cold real P2Kano17, original stage0 CPU18 via native CSS/ladder',fourPNG=['selection','ladder','fight','cleanup'],pngTotalByteLimit=262144,pngDimensions=[400,254],inputPolicy='60fields Block;6fields backwalk;one physical D,B,HP knife chord;ordinary Up;Blockfollowup',limits='4000fields/90sec/320MiB/10MiBtext',scope='Combined chronological UI/ladder/true17+18/fight/ownedknife/ordinarycontrol/passiveCPUvoice scalar lifetime; no heardmix/allmoves/allarenas/fullport acceptance.',sourceDiff=''.join(difflib.unified_diff(old.splitlines(True),s.splitlines(True)))),indent=2))
print(out,sync.sha(lua))
