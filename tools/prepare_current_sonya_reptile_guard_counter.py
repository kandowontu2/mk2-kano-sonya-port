"""Physical guarded counter preparation; passive native activation observer."""
import verify_native_source_sync as sync
sync.verify()
base=sync.ROOT/'audit_current_sonya_reptile_crouch_counter_long_preparation'
out=sync.ROOT/'audit_current_sonya_reptile_guard_counter_preparation';assert not out.exists()
source=(base/'campaign.lua').read_text()
start=source.index("   elseif strategy=='uppercut' then\n");end=source.index("   elseif strategy=='jumpkick' then\n",start)
source=source[:start]+'''   elseif strategy=='uppercut' then
    local forward=human.x<other.x and'Right'or'Left'
    if not gc_last or frame-gc_last~=1 then gc_start=nil;gc_retry=-1000 end
    gc_last=frame
    local height=human.floor-human.y
    local blocking=human.action==1792 or human.action==1793
    local ready=height<=8 and (blocking or human.action==771 or human.action==770 or human.action==772)
      and human.flags&0x1c==0 and (blocking or human.body&0x0c==0)
    local safe=other.action==0 or other.action==771 or other.action==770 or other.action==772 or other.action==263
      or (other.action>=1536 and other.action<=1551)
    if gc_start and frame-gc_start<12 then
     local age=frame-gc_start
     if age<9 then press('Down')end
     if age>=6 and age<9 then press('High Punch')end
    elseif height>8 then
     press('Block');if gap<100 and frame%6<3 then press('High Kick')end
    elseif ready and safe and gap<95 and frame-gc_retry>=32 then
     gc_start=frame;gc_retry=frame;press('Down')
     log('GUARDED_COUNTER_ATTEMPT',string.format('stage=%d gap=%d human_action=%d cpu_action=%d',stage,gap,human.action,other.action))
    elseif ready and safe and gap>85 and other.floor-other.y<=8 then
     gc_start=nil;press(forward)
    else
     gc_start=nil;press('Down');press('Block')
    end
'''+source[end:]
source=source.replace('local guard_until=-1000','local guard_until=-1000\nlocal gc_last,gc_start,gc_retry=nil,nil,-1000',1)
out.mkdir();lua=out/'campaign.lua';lua.write_text(source)
runner=(base/'run.ps1').read_text().replace(base.name+'/campaign.lua',out.name+'/campaign.lua').replace(sync.sha(base/'campaign.lua'),sync.sha(lua))
runner=runner.replace('audit_current_sonya_reptile_crouch_counter_long_runtime','audit_current_sonya_reptile_guard_counter_runtime')
(out/'run.ps1').write_text(runner)
print('Prepared20k physical guard/released-Block Down9 HP6..8; Reptile only/no media/normal caps')
