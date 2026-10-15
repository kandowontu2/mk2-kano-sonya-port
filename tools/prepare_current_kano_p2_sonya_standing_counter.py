"""Physical normal counter only against actual Sonya; subsequent zoning unchanged."""
import verify_native_source_sync as sync
sync.verify()
base=sync.ROOT/'audit_bounded_campaign_progress_core_preparation'
out=sync.ROOT/'audit_current_kano_p2_sonya_standing_counter_preparation'
assert not out.exists()
source=(base/'core.lua').read_text()
needle="   if (leg_tactic or strategy=='lowkick'or strategy=='throw') and other.roster~=12 and other.roster~=13 then"
assert source.count(needle)==1
branch="""   if fighter=='kano' and side==2 and other.roster==18 then
    local forward=human.x<other.x and 'Right' or 'Left'
    local height,cpu_height=human.floor-human.y,other.floor-other.y
    local stance=human.action==0 or human.action==771 or human.action==772
    local ready=height<=8 and human.flags&0x1c==0 and stance
    local safe=(other.action==0 or other.action==771 or other.action==772 or other.action==770) and other.flags&0x1c==0
    if not kp_last or frame-kp_last~=1 then kp_start=nil;kp_retry=-1000 end
    kp_last=frame
    if other.flags&0x10~=0 then kp_start=nil;press('Down');press('Block')
    elseif kp_start and frame-kp_start<32 then
     local age=frame-kp_start
     if age>=2 and age<6 then press('High Kick')end
     if age>=10 and (ready or not safe) then press('Down');press('Block')end
    elseif ready and safe and cpu_height<=8 and gap<105 and frame-kp_retry>=32 then
     kp_start=frame;kp_retry=frame
     log('KANO_P2_SONYA_COUNTER',string.format('gap=%d action=%d cpu_action=%d health=%d,%d',gap,human.action,other.action,human.hp,other.hp))
    elseif ready and safe and cpu_height<=8 and gap>=105 then kp_start=nil;press(forward)
    elseif not ready and safe then kp_start=nil
    else kp_start=nil;press('Down');press('Block')end
   elseif (leg_tactic or strategy=='lowkick'or strategy=='throw') and other.roster~=12 and other.roster~=13 then"""
source='local kp_last,kp_start,kp_retry=nil,nil,-1000\n'+source.replace(needle,branch)
source=source.replace('frame>=12000','frame>=20000').replace('maximum_fields=12000','maximum_fields=20000')
needle="   log('HEALTH',string.format("
assert source.count(needle)==1
extra="""   if cpu.PC.value==0xff836700 and p:read_u16(0x01061b30)==0 then
    local a,b=sample(1),sample(2);local before,after=p:read_u16(at),data&0xffff
    if a and b and a.id==18 and b.id==17 and after<before and before<=161 then
     log('KANO_P2_SONYA_DAMAGE',string.format('victim_slot=%d before=%d after=%d a8=%08X a13=%08X p1_actor=%08X p1_main=%08X p2_actor=%08X p2_main=%08X ids=%d,%d actions=%d,%d',n,before,after,cpu.A8.value,cpu.A13.value,a.actor,a.main,b.actor,b.main,a.id,b.id,a.action,b.action))
    end
   end
"""
source=source.replace(needle,extra+needle)
assert ':write_' not in source and ':snapshot(' not in source
out.mkdir();lua=out/'campaign.lua';lua.write_text(source)
runner=(base/'run_kano_p2.ps1').read_text().replace(base.name+'/core.lua',out.name+'/campaign.lua').replace(sync.sha(base/'core.lua'),sync.sha(lua)).replace('audit_bounded_campaign_progress_core_kano_p2_runtime','audit_current_kano_p2_sonya_standing_counter_runtime')
runner=runner.replace("'-str','300'","'-str','450'")
(out/'run.ps1').write_text(runner)
print('Prepared20000fields; KanoP2 physical counter only againstSonya; no media')
