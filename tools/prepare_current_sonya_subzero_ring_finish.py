"""Physical ranged follow-up only after naturally earned low CPU health."""
import verify_native_source_sync as sync
sync.verify()
base=sync.ROOT/'audit_current_sonya_subzero_range_long_preparation'
out=sync.ROOT/'audit_current_sonya_subzero_ring_finish_preparation'
assert not out.exists()
source=(base/'campaign.lua').read_text()
marker='   elseif leg_tactic and other.roster==8 then\n'
assert source.count(marker)==1
branch='''   elseif leg_tactic and other.roster==8 and other.hp<=41 then
    local forward=human.x<other.x and'Right'or'Left'
    local back=forward=='Right'and'Left'or'Right'
    local height=human.floor-human.y
    if not chip_last or frame-chip_last~=1 then chip_ring=nil;chip_escape=nil end
    chip_last=frame
    if chip_ring and frame-chip_ring<64 then
     local age=frame-chip_ring
     if age>=2 and age<5 then press('Down')end
     if age>=7 and age<10 then press(chip_forward)end
     if age>=8 and age<12 then press('Low Punch')end
     if age>=15 then press('Down');press('Block')end
    elseif height>8 then
     chip_ring=nil;press(back)
     if frame%6<3 then press('High Kick')end
    elseif gap<120 then
     chip_ring=nil;chip_escape=chip_escape or frame
     local age=(frame-chip_escape)%48
     press(back)
     if age>=8 and age<16 then press('Up')end
    elseif human.flags&0x1c==0 and (human.action==771 or human.action==770 or human.action==1793 or human.action==1792)then
     chip_escape=nil;chip_ring=frame;chip_forward=forward
     log('SUBZERO_RING_FINISH_ATTEMPT',string.format('gap=%d cpu_hp=%d human_hp=%d',gap,other.hp,human.hp))
    else
     press('Down');press('Block')
    end
'''
source=source.replace(marker,branch+marker)
source="local chip_last,chip_ring,chip_escape,chip_forward=nil,nil,nil,nil\n"+source
source+='''
taps[#taps+1]=p:install_read_tap(0xffffb400,0xffffb40f,'read-only low-health own ring',function()
 if cpu.PC.value~=0xffffb410 then return end
 local own,other=sample(side),sample(opponent)
 if own and other and other.roster==8 and cpu.A8.value==own.actor then
  log('SUBZERO_RING_ENTRY',string.format('actor=%08X main=%08X id=%d roster=%d cpu_hp=%d human_hp=%d gap=%d pc=%08X',own.actor,own.main,own.id,own.roster,other.hp,own.hp,math.abs(own.x-other.x),cpu.PC.value))
 end
end)
'''
out.mkdir();lua=out/'campaign.lua';lua.write_text(source)
runner=(base/'run.ps1').read_text().replace(base.name+'/campaign.lua',out.name+'/campaign.lua').replace(sync.sha(base/'campaign.lua'),sync.sha(lua))
runner=runner.replace('audit_current_sonya_subzero_range_long_runtime','audit_current_sonya_subzero_ring_finish_runtime')
(out/'run.ps1').write_text(runner)
print('Prepared18000field normal ring follow-up when actual SubZero HP<=41; no forcing/media')
