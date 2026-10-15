"""Retain earned Sonya opener; physical freeze guard/crouch HP against SubZero."""
import verify_native_source_sync as sync
sync.verify()
base=sync.ROOT/'audit_current_kano_p2_sonya_standing_counter_preparation'
out=sync.ROOT/'audit_current_kano_p2_subzero_crouch_counter_preparation'
assert not out.exists()
source=(base/'campaign.lua').read_text()
needle="   elseif (leg_tactic or strategy=='lowkick'or strategy=='throw') and other.roster~=12 and other.roster~=13 then"
assert source.count(needle)==1
branch="""   elseif fighter=='kano' and side==2 and other.roster==8 then
    local forward=human.x<other.x and 'Right' or 'Left'
    local height=human.floor-human.y
    if not kz_last or frame-kz_last~=1 then kz_start=nil;kz_guard=-1000 end
    kz_last=frame
    if other.action==0x604 or other.action==0x10 then kz_guard=frame+40 end
    if height>8 then kz_start=nil;press('Block')
    elseif frame<kz_guard and gap>90 then kz_start=nil;press('Down');press('Block')
    elseif gap<95 then
     kz_start=kz_start or frame;local age=(frame-kz_start)%32
     press('Down')
     if age<10 or age>=26 then press('Block')end
     if age>=13 and age<26 and age%6<3 then press('High Punch')end
     if age==13 then log('KANO_P2_SUBZERO_COUNTER',string.format('gap=%d action=%d cpu_action=%d flags=%04X health=%d,%d',gap,human.action,other.action,human.flags,human.hp,other.hp))end
    else kz_start=nil;press(forward)end
   elseif (leg_tactic or strategy=='lowkick'or strategy=='throw') and other.roster~=12 and other.roster~=13 then"""
source='local kz_last,kz_start,kz_guard=nil,nil,-1000\n'+source.replace(needle,branch)
needle="   log('HEALTH',string.format("
assert source.count(needle)==1
extra="""   if cpu.PC.value==0xff836700 and p:read_u16(0x01061b30)==1 then
    local a,b=sample(1),sample(2);local before,after=p:read_u16(at),data&0xffff
    if a and b and a.id==8 and b.id==17 and after<before and before<=161 then
     log('KANO_P2_SUBZERO_DAMAGE',string.format('victim_slot=%d before=%d after=%d a8=%08X a13=%08X p1_actor=%08X p1_main=%08X p2_actor=%08X p2_main=%08X ids=%d,%d actions=%d,%d',n,before,after,cpu.A8.value,cpu.A13.value,a.actor,a.main,b.actor,b.main,a.id,b.id,a.action,b.action))
    end
   end
"""
source=source.replace(needle,extra+needle)
assert ':write_' not in source and ':snapshot(' not in source
out.mkdir();lua=out/'campaign.lua';lua.write_text(source)
runner=(base/'run.ps1').read_text().replace(base.name+'/campaign.lua',out.name+'/campaign.lua').replace(sync.sha(base/'campaign.lua'),sync.sha(lua)).replace('audit_current_kano_p2_sonya_standing_counter_runtime','audit_current_kano_p2_subzero_crouch_counter_runtime')
(out/'run.ps1').write_text(runner)
print('Prepared20000fields; retained Sonya clear; physical SubZero freeze/crouch counter')
