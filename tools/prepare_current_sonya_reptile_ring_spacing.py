"""Reuse historical native physical ring/retreat spacing without dense sinks."""
import verify_native_source_sync as sync
sync.verify()
base=sync.ROOT/'audit_current_sonya_reptile_crouch_counter_long_preparation'
out=sync.ROOT/'audit_current_sonya_reptile_ring_spacing_preparation';assert not out.exists()
source=(base/'campaign.lua').read_text()
start=source.index("   elseif strategy=='uppercut' then\n")
end=source.index("   elseif strategy=='jumpkick' then\n",start)
source=source[:start]+'''   elseif strategy=='uppercut' then
    local forward=human.x<other.x and'Right'or'Left'
    local back=forward=='Right'and'Left'or'Right'
    if not rs_last or frame-rs_last~=1 then rs_ring=nil;rs_dir=nil;rs_jump=-1000;rs_jumpdir=nil end
    rs_last=frame
    if rs_ring and frame-rs_ring<64 and (frame-rs_ring<12 or gap>=150) then
     local age=frame-rs_ring
     if age>=2 and age<5 then press('Down')end
     if age>=7 and age<10 then press(rs_dir)end
     if age>=8 and age<12 then press('Low Punch')end
     if age>=15 then press('Down');press('Block')end
    elseif human.floor-human.y>8 then
     if rs_jumpdir and frame-rs_jump<48 then press(rs_jumpdir)end
     if frame%6<3 then press('High Kick')end
    elseif gap<150 then
     rs_ring=nil
     if frame-rs_jump>=4 then rs_jump=frame;rs_jumpdir=back end
     if frame-rs_jump<3 then press('Up');press(rs_jumpdir)
     else press(rs_jumpdir)end
    else
     rs_ring=frame;rs_dir=forward
     log('SPACING_RING_ATTEMPT','stage='..stage..' gap='..gap)
    end
'''+source[end:]
source=source.replace('local guard_until=-1000','local guard_until=-1000\nlocal rs_last,rs_ring,rs_dir,rs_jumpdir=nil,nil,nil,nil\nlocal rs_jump=-1000',1)
out.mkdir();lua=out/'campaign.lua';lua.write_text(source)
runner=(base/'run.ps1').read_text().replace(base.name+'/campaign.lua',out.name+'/campaign.lua').replace(sync.sha(base/'campaign.lua'),sync.sha(lua))
runner=runner.replace('audit_current_sonya_reptile_crouch_counter_long_runtime','audit_current_sonya_reptile_ring_spacing_runtime')
(out/'run.ps1').write_text(runner)
print('Prepared20k real D,F,LP and early retreat retry, Reptile only; native game unchanged/no media')
