"""Prepare physical ready-gated Ring; no new PNGs or guest writes."""
import json,difflib
import verify_native_source_sync as sync
sync.verify();root=sync.ROOT;base=root/'audit_current_combined_sonya_smoke_preparation'
out=root/'audit_current_sonya_adaptive_ring_smoke_preparation';assert not out.exists()
old=(base/'campaign.lua').read_text();s=old
s=s.replace('local frame,selections,losses,wins,live_fields=0,0,0,0,0','local frame,selections,losses,wins,live_fields=0,0,0,0,0\nlocal smoke_plan,smoke_forward,smoke_entry,smoke_recovered=nil,nil,nil,nil')
needle='body=p:read_u16(a+0x160),bank=p:read_u16(a+0x140),action=p:read_u16(m+0x1f0)'
assert s.count(needle)==1
s=s.replace(needle,needle+',vy=p:read_u32(a+0x60),vx=p:read_u32(a+0x40),gravity=p:read_u32(a+0x20),trail=p:read_u32(m+0x190)')
needle=" log('SPECIAL',string.format('move=%s entry=%08X"
assert s.count(needle)==1;s=s.replace(needle," if move_name=='ring'and smoke_plan then smoke_entry=smoke_entry or frame end\n"+needle)
start=s.index('  if winner==0 and human.hp>0 and other.hp>0 then');end=s.index(' if first_live and stage==16',start)
policy="""  if winner==0 and human.hp>0 and other.hp>0 then
   local age=frame-first_live;local gap=math.abs(human.x-other.x)
   local back=human.x<other.x and'Left'or'Right'
   local clean=human.y==human.floor and human.vy==0 and human.vx==0 and human.gravity==0 and human.trail==0 and human.flags&0x1c==0 and human.body&0x0c==0 and(human.action==0 or human.action==771)
   local quiet=(other.action==0 or other.action==771)and other.flags&0x18==0
   if not smoke_plan then
    if age>60 and clean and quiet and gap>=150 then
     smoke_plan=frame;smoke_forward=human.x<other.x and'Right'or'Left'
     log('RING_READY_PLAN',string.format('forward=%s actor=%08X main=%08X owner=%08X id=%d roster=%d action=%d flags=%04X body=%04X y=%d floor=%d vy=%08X vx=%08X gravity=%08X trail=%08X cpu_action=%d cpu_flags=%04X gap=%d',smoke_forward,human.actor,human.main,human.owner,human.id,human.roster,human.action,human.flags,human.body,human.y,human.floor,human.vy,human.vx,human.gravity,human.trail,other.action,other.flags,gap))
    elseif age<60 then press('Block')
    elseif gap<150 then if age%4<3 then press('Up');press(back)end
    elseif not quiet then press('Block')end
   end
   if smoke_plan then
    local t=frame-smoke_plan
    if t>=0 and t<3 then press('Down')end
    if t>=5 and t<8 then press(smoke_forward)end
    if t>=6 and t<9 then press('Low Punch')end
    if smoke_entry and not smoke_recovered and frame>smoke_entry+12 and clean then
     smoke_recovered=frame;log('RING_RECOVERED',string.format('actor=%08X main=%08X owner=%08X id=%d action=%d y=%d floor=%d flags=%04X body=%04X',human.actor,human.main,human.owner,human.id,human.action,human.y,human.floor,human.flags,human.body))
    end
    if smoke_recovered then press('Block')end
    if t>400 then log('RING_ATTEMPT_END','entry='..(smoke_entry or-1)..' recovered='..(smoke_recovered or-1));manager.machine:exit()end
   end
   if age>=1100 then log('RING_TARGET_UNOBSERVED','no_clean_plan='..(smoke_plan and 0 or 1));manager.machine:exit()end
  end
 end
"""
s=s[:start]+policy+s[end:]
s=s[:s.index('local combined_captured={}')]+"\nemu.register_frame_done(function()if smoke_recovered and frame-smoke_recovered>=120 then log('RING_FOLLOWUP_COMPLETE','recovered='..smoke_recovered);manager.machine:exit()end end)\n"
assert ':write_'not in s and ':snapshot('not in s
out.mkdir();lua=out/'campaign.lua';lua.write_text(s)
runner=(base/'run.ps1').read_text().replace(base.name+'/campaign.lua',out.name+'/campaign.lua').replace(sync.sha(base/'campaign.lua'),sync.sha(lua)).replace('audit_current_combined_sonya_smoke_runtime','audit_current_sonya_adaptive_ring_smoke_runtime')
runner=runner.replace("rawMedia='four bounded400x254PNGs only; no raw media'","rawMedia='none'")
(out/'run.ps1').write_text(runner)
(out/'source.json').write_text(json.dumps(dict(preparedNotRun=True,LuaSHA256=sync.sha(lua),physicalOnly=True,newPNGCount=0,guestWrites=False,readiness='Same true18human owner/roster; actualYfloor/VY/VX/gravity/trailzero, action0or771/flags1Cbody0Cclear; CPUactualidle+flags18clear/gap150',policy='InitialBlock60, physicalbackjump tospace ifclose, neutralrelease ifquietfar; one actualreadylockedDirectionD,F,LP; recovery requiresnativeentry thencleanready,120followupfields',limits='4000fields/90sec320MiB10MiB/no media',scope='Targeted activation/recovery; noforcedCPUball requirement; allnativeportwords notADSPreceipt/heardmix',sourceDiff=''.join(difflib.unified_diff(old.splitlines(True),s.splitlines(True)))),indent=2))
manual=root/'audit_current_combined_sonya_smoke_manual_review'
assert not manual.exists();manual.mkdir()
(manual/'report.json').write_text(json.dumps(dict(rootReviewedAllFour=True,selection='properSonyaP1highlight/number/pose',ladder='actualSonyaicon andallselectorartcleared',fightAndCleanup='true18/17alive nativecontact,no selectoroverlays',ringActivationAccepted=False,newAudioLifetimeAccepted=False,scope='Finite actualfourPNGUI/identity/contactmanualreview only.',parentReportSHA256=sync.sha(root/'audit_current_combined_sonya_smoke_checked/report.json')),indent=2))
print(out,sync.sha(lua))
