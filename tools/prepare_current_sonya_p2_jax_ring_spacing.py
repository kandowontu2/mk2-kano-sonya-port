"""UNEXECUTED successor: historical physical ring/backjump policy at current Jax8."""
import json
import verify_native_source_sync as sync
sync.verify()
base=sync.ROOT/'audit_current_sonya_p2_kano_short_leg_preparation'
out=sync.ROOT/'audit_current_sonya_p2_jax_ring_spacing_preparation'
assert not out.exists()
source=(base/'campaign.lua').read_text()
marker="   elseif fighter=='sonya' and side==2 and other.roster==17 and stage==7 then"
assert source.count(marker)==1
branch="""   elseif fighter=='sonya' and side==2 and other.roster==11 and stage==8 then
    if not jrs_last or frame-jrs_last~=1 then jrs_ring=nil;jrs_dir=nil;jrs_jump=-1000;jrs_jumpdir=nil end
    jrs_last=frame
    local forward=human.x<other.x and'Right'or'Left'
    local back=forward=='Right'and'Left'or'Right'
    if jrs_ring and frame-jrs_ring<64 and(frame-jrs_ring<12 or gap>=150)then
     local age=frame-jrs_ring
     if age>=2 and age<5 then press('Down')end
     if age>=7 and age<10 then press(jrs_dir)end
     if age>=8 and age<12 then press('Low Punch')end
     if age>=15 then press('Down');press('Block')end
    elseif human.floor-human.y>8 then
     if jrs_jumpdir and frame-jrs_jump<48 then press(jrs_jumpdir)end
     if frame%6<3 then press('High Kick')end
    elseif gap<150 then
     jrs_ring=nil
     if frame-jrs_jump>=4 then
      jrs_jump=frame;jrs_jumpdir=back
      log('SONYA_JAX_JUMP_PLAN',string.format('stage=%d id=18 gap=%d action=%d health=%d,%d',stage,gap,human.action,human.hp,other.hp))
     end
     if frame-jrs_jump<3 then press('Up');press(jrs_jumpdir)
     else press(jrs_jumpdir)end
    else
     jrs_ring=frame;jrs_dir=forward
     log('SONYA_JAX_RING_PLAN',string.format('stage=%d actor=%08X main=%08X id=18 gap=%d action=%d health=%d,%d',stage,human.actor,human.main,gap,human.action,human.hp,other.hp))
    end
"""
source='local jrs_last,jrs_ring,jrs_dir,jrs_jumpdir=nil,nil,nil,nil\nlocal jrs_jump=-1000\n'+source.replace(marker,branch+marker)
source+='''
for observed_slot,observed_hp in ipairs({0x010602f0,0x01060ec0})do
 taps[#taps+1]=p:install_write_tap(observed_hp,observed_hp+15,'passive actual Sonya Jax damage',function(at,data,mask)
  if at~=observed_hp or mask~=0xffff or p:read_u16(0x01061b30)~=8 or p:read_u16(0x010601d0)~=2 then return end
  local before,after=p:read_u16(at),data&0xffff
  if after>=before or before>161 then return end
  local h,c=sample(2),sample(1)
  if not h or not c or h.id~=18 or h.roster~=18 or c.id~=11 or c.roster~=11 or h.owner~=h.actor or c.owner~=c.actor then return end
  log('SONYA_JAX_DAMAGE',string.format('victim_slot=%d before=%d after=%d pc=%08X ids=11,18 human_action=%d cpu_action=%d gap=%d height=%d cpu_height=%d',observed_slot,before,after,cpu.PC.value,h.action,c.action,math.abs(h.x-c.x),h.floor-h.y,c.floor-c.y))
 end)
end
'''
assert ':write_' not in source and ':snapshot(' not in source
out.mkdir();lua=out/'campaign.lua';lua.write_text(source)
runner=(base/'run.ps1').read_text().replace(base.name+'/campaign.lua',out.name+'/campaign.lua').replace(sync.sha(base/'campaign.lua'),sync.sha(lua)).replace('audit_current_sonya_p2_kano_short_leg_runtime','audit_current_sonya_p2_jax_ring_spacing_runtime')
(out/'run.ps1').write_text(runner)
report=dict(prepared=True,emulatorLaunched=False,runtimeAcceptance=False,fullPortAcceptance=False,
            historicalFinitePolicy='audit_v5661_sonya_p2_jax_ring_probe_checked/report.json',
            currentEvidence='audit_current_sonya_p2_kano_short_leg_runtime/run.log',
            proposedConservedPrefix=101525,changes='Stage8 trueCPUJax11 only: ring D2..5/F7..10/LP8..12, guard15..64 while gap150+, backjump3on/1off below150, actual airborne HK3on/3off; passive HP context.',
            limits=dict(wallSeconds=180,memoryMiB=320,textMiB=10,media=False,guestWrites=False),
            luaSHA256=sync.sha(lua))
(out/'preparation.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report))
