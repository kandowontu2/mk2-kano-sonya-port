"""Native crouch-loop-gated physical leg chord vs stage11 SubZero only."""
import verify_native_source_sync as sync
sync.verify()
base=sync.ROOT/'audit_current_sonya_p1_subzero_defense_priority_preparation'
out=sync.ROOT/'audit_current_sonya_p1_subzero_settled_leg_preparation'
assert not out.exists()
source=(base/'campaign.lua').read_text()
source='local sl_taps,sl_loop,sl_main,sl_down,sl_pulse,sl_last={},nil,nil,nil,nil,nil\n'+source
marker="   elseif fighter=='sonya' and side==1 and (other.roster==8"
assert source.count(marker)==1
branch='''   elseif fighter=='sonya' and side==1 and other.roster==8 and stage==11 then
    if not sl_taps[human.main]then
     local observed_main=human.main
     sl_taps[observed_main]=p:install_write_tap(observed_main+0x1f0,observed_main+0x1ff,'passive settled Sonya crouch loop',function(at,data,mask)
      if at~=observed_main+0x1f0 or mask~=0xffff or data&0xffff~=770 or cpu.PC.value~=0xff82fa80 then return end
      local h=sample(side)
      if h and h.main==observed_main and h.id==18 and h.owner==h.actor then sl_loop=frame;sl_main=observed_main end
     end)
     taps[#taps+1]=sl_taps[observed_main]
    end
    if not sl_last or frame-sl_last>1 then sl_down=nil;sl_pulse=nil end
    sl_last=frame
    local grounded=human.y==human.floor
    local ready=grounded and human.flags&0x1c==0 and human.body&0x0c==0 and(human.action==0 or human.action==771 or human.action==770 or human.action==772 or human.action==1792 or human.action==1793)
    if sl_pulse and frame-sl_pulse<8 then
     press('Down');if frame-sl_pulse<4 then press('Low Punch');press('Block')end
    elseif not ready or other.flags&0x10~=0 or other.floor-other.y>8 then
     sl_down=nil;press('Down');press('Block')
    elseif gap>100 then
     sl_down=nil;press(human.x<other.x and'Right'or'Left')
    else
     sl_down=sl_down or frame;press('Down')
     if human.action==770 and sl_loop and sl_main==human.main and sl_loop>=sl_down and frame-sl_loop<=2 and(not sl_pulse or frame-sl_pulse>=64)then
      sl_pulse=frame;press('Low Punch');press('Block')
      log('SONYA_SETTLED_LEG_PLAN',string.format('actor=%08X main=%08X id=18 action=770 gap=%d loop=%d health=%d,%d',human.actor,human.main,gap,sl_loop,human.hp,other.hp))
     end
    end
'''
source=source.replace(marker,branch+marker)
assert ':write_' not in source and ':snapshot(' not in source
out.mkdir();lua=out/'campaign.lua';lua.write_text(source)
runner=(base/'run.ps1').read_text().replace(base.name+'/campaign.lua',out.name+'/campaign.lua').replace(sync.sha(base/'campaign.lua'),sync.sha(lua)).replace('audit_current_sonya_p1_subzero_defense_priority_runtime','audit_current_sonya_p1_subzero_settled_leg_runtime')
(out/'run.ps1').write_text(runner)
print('Stage11actualcrouchloop/physicalleggrab;180sec/320MiB/10MiB/no media')
