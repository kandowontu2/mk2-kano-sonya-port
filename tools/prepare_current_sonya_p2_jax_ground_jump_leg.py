"""UNEXECUTED Jax8 successor: stock ground-pound jump priority then short leg."""
import ast
import json
import verify_native_source_sync as sync
sync.verify()
root=sync.ROOT;base=root/'audit_current_sonya_p2_kano_short_leg_preparation'
out=root/'audit_current_sonya_p2_jax_ground_jump_leg_preparation';assert not out.exists()
source=(base/'campaign.lua').read_text()
marker="   elseif fighter=='sonya' and side==2 and other.roster==17 and stage==7 then"
assert source.count(marker)==1
branch="""   elseif fighter=='sonya' and side==2 and other.roster==11 and stage==8 then
    if not jgl_last or frame-jgl_last~=1 then jgl_pulse=nil;jgl_until=-1000;jgl_jump=-1000 end
    jgl_last=frame
    local height=human.floor-human.y
    local ready=human.y==human.floor and(human.action==0 or human.action==771 or human.action==770 or human.action==772 or human.action==1792 or human.action==1793)
    local forward=human.x<other.x and'Right'or'Left'
    local back=forward=='Right'and'Left'or'Right'
    if other.action==311 then jgl_until=frame+40 end
    if frame<jgl_until and height<=8 then
     jgl_pulse=nil
     if frame-jgl_jump>=4 then
      jgl_jump=frame
      log('SONYA_JAX_POUND_JUMP_PLAN',string.format('stage=%d id=18 gap=%d action=%d cpu_action=%d until=%d health=%d,%d',stage,gap,human.action,other.action,jgl_until,human.hp,other.hp))
     end
     if frame-jgl_jump<3 then press('Up');press(back)end
    elseif height>8 then
     press(back)
    elseif jgl_pulse and frame-jgl_pulse<12 then
     local age=frame-jgl_pulse
     if age<7 then press('Down')end
     if age>=3 and age<7 then press('Low Punch');press('Block')end
    elseif other.flags&0x10~=0 then
     press('Down');press('Block')
    elseif ready and other.floor-other.y<=8 and gap<110 and(not jgl_pulse or frame-jgl_pulse>=48)then
     jgl_pulse=frame;press('Down')
     log('SONYA_JAX_SHORT_LEG_PLAN',string.format('stage=%d actor=%08X main=%08X id=18 action=%d gap=%d health=%d,%d',stage,human.actor,human.main,human.action,gap,human.hp,other.hp))
    elseif ready and gap>100 and other.floor-other.y<=8 then
     press(forward)
    else press('Down');press('Block')end
"""
source='local jgl_last,jgl_pulse=nil,nil\nlocal jgl_until,jgl_jump=-1000,-1000\n'+source.replace(marker,branch+marker)
source+='''
for _,entry in ipairs({{0xff86dd90,'ground_entry'},{0xff86e020,'ground_result'},{0xff86e070,'ground_damage'},{0xff831360,'human_jump'}})do
 local address,kind=entry[1],entry[2]
 taps[#taps+1]=p:install_read_tap(address,address+15,'passive Jax ground and Sonya jump',function(at,data,mask)
  if at~=address or cpu.PC.value~=address+16 or p:read_u16(0x010601d0)~=2 or p:read_u16(0x01061b30)~=8 then return end
  local h,c=sample(2),sample(1)
  if not h or not c or h.id~=18 or h.roster~=18 or c.id~=11 or c.roster~=11 or h.owner~=h.actor or c.owner~=c.actor or h.hp<=0 or c.hp<=0 then return end
  local owner,main=kind=='human_jump'and h.actor or c.actor,kind=='human_jump'and h.main or c.main
  if cpu.A8.value~=owner or cpu.A13.value~=main then return end
  log('JAX_GROUND_NATIVE',string.format('kind=%s entry=%08X at=%08X pc=%08X opcode=%04X mask=%04X stage=8 h_actor=%08X h_main=%08X h_owner=%08X c_actor=%08X c_main=%08X c_owner=%08X h_id=18 c_id=11 h_y=%d h_floor=%d h_vy=%08X c_y=%d c_floor=%d c_vy=%08X health=%d,%d carry=%d a8=%08X a13=%08X',kind,address,at,cpu.PC.value,data&0xffff,mask,h.actor,h.main,h.owner,c.actor,c.main,c.owner,h.y,h.floor,p:read_u32(h.actor+0x60),c.y,c.floor,p:read_u32(c.actor+0x60),h.hp,c.hp,(cpu.ST.value>>30)&1,cpu.A8.value,cpu.A13.value))
 end)
end
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
inspector=root/'tools/inspect_jax_137_ground_damage_source_v4805.py'
tree=ast.parse(inspector.read_text());checks=ast.literal_eval(next(n.value for n in tree.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='CHECKS' for t in n.targets)))
checks_lua=','.join('{0x%08x,%s}'%(address,','.join(str(w) for w in words)) for address,words in checks.items())
source+='''
local jax_loaded_code_checked=false
emu.register_frame_done(function()
 if jax_loaded_code_checked or p:read_u16(0x01061b30)~=8 or p:read_u16(0x010601d0)~=2 then return end
 local checks={CHECKS_LUA}
 local count=0
 for _,row in ipairs(checks)do for i=2,#row do assert(p:read_u16(row[1]+(i-2)*16)==row[i]);count=count+1 end end
 jax_loaded_code_checked=true;log('JAX_GROUND_CODE_CHECKED','stage=8 original_words='..count..' current_loaded=true')
end)
'''.replace('CHECKS_LUA',checks_lua)
assert ':write_' not in source and ':snapshot(' not in source
out.mkdir();lua=out/'campaign.lua';lua.write_text(source)
runner=(base/'run.ps1').read_text().replace(base.name+'/campaign.lua',out.name+'/campaign.lua').replace(sync.sha(base/'campaign.lua'),sync.sha(lua)).replace('audit_current_sonya_p2_kano_short_leg_runtime','audit_current_sonya_p2_jax_ground_jump_leg_runtime')
(out/'run.ps1').write_text(runner)
report=dict(prepared=True,emulatorLaunched=False,runtimeAcceptance=False,fullPortAcceptance=False,proposedConservedPrefix=101525,
            physicalPolicy='Actual CPU311 ground-pound extends40field jump guard; UpBack3on1off atfloor before any leg chord; actualairborne holdsBack; otherwise guardedshortleg Down7/LPBlock3..7 retry48 gap110. Stock ground-pound not Block guarded.',
            passiveObservations=['true native ground-entry/Carry-result/damage-path/jump PCs','owned HP contexts','loaded original29instruction sites'],
            limits=dict(wallSeconds=180,memoryMiB=320,textMiB=10,media=False,guestWrites=False),luaSHA256=sync.sha(lua))
(out/'preparation.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
