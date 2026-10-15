"""Earn Portal normally, crouch uppercut, physical Down/Start on real Toasty."""
import verify_native_source_sync as sync
sync.verify()
base = sync.ROOT / 'audit_current_stock_pit_initialized_selector_preparation'
out = sync.ROOT / 'audit_current_sonya_natural_smoke_preparation'
assert not out.exists()
source = (base / 'sonya_p1_kitana.lua').read_text()
def change(old, new):
    global source
    assert source.count(old) == 1, old
    source = source.replace(old, new)
change('assert(target_arena==0 or target_arena==1 or target_arena==6)', 'assert(target_arena==7)')
change('local rematch_at,action_arena,last_state=nil,nil,nil', '''local rematch_at,action_arena,last_state=nil,nil,nil
local toast,accepted,secret,epoch,walkStart,walkX,jumpStart,punchStart,recovered=nil,nil,nil,nil,nil,nil,nil,nil,nil
local walked,jumped,punched=false,false,false
local function owned(a,identity,state)return a and a.id==identity and a.roster==identity and a.owner==a.actor and a.state==state end
local function ready(a)return a and a.y==a.floor and a.vy==0 and a.gravity==0 and a.flags&0x1c==0 and(a.action==0 or a.action==771)end''')
change('pose=p:read_u32(a+0x1d0),flags=p:read_u16(m+0x210)}', '''pose=p:read_u32(a+0x1d0),flags=p:read_u16(m+0x210),state=p:read_u16(s.state),
 floor=p:read_i16(m+0x200),action=p:read_u16(m+0x1f0),vx=p:read_u32(a+0x40),vy=p:read_u32(a+0x60),gravity=p:read_u32(a+0x20)}''')
change('frame>=36000', 'frame>=28000')
change('maximum_fields=36000', 'maximum_fields=28000')
change('if arena==target_arena then', 'if false and arena==target_arena then')
change('if not action and not command and window and frame-window>=720 and mode~=4 then',
       'if not accepted and not action and not command and window and frame-window>=720 and mode~=4 then')
change("else if frame%32<4 then press(side,'High Kick')end end", '''elseif arena==7 then
    press(side,'Down');if frame%48>=13 and frame%48<26 and frame%6<3 then press(side,'High Punch')end
   else if frame%32<4 then press(side,'High Kick')end end
   if arena==7 and toast and frame-toast<=48 then press(side,'Down');if(frame-toast)%8<4 then press(side,'Start')end end''')
change('if mode==2 and pending and h and v', 'if not accepted and mode==2 and pending and h and v')
change('if not action and not pending and h and v', 'if not accepted and not action and not pending and h and v')
change(' local h,v=sample(side),sample(3-side)\n if not accepted', ''' local h,v=sample(side),sample(3-side)
 if accepted then
  if mode~=2 then
   epoch=nil;walkStart=nil;walkX=nil;jumpStart=nil;punchStart=nil;recovered=nil;walked=false;jumped=false;punched=false
  elseif owned(h,id,1)and owned(v,14,0)and h.hp>0 and v.hp>0 then
   if not secret then secret=frame;log('SECRET_FIGHT','human='..h.id..' cpu='..v.id..' arena='..arena)end
   if not epoch then epoch=frame;log('SECRET_EPOCH','human_hp='..h.hp..' cpu_hp='..v.hp)end
   if not walked then
    if ready(h)then
     walkStart=walkStart or frame;walkX=walkX or h.x
     if math.abs(h.x-walkX)>=4 then walked=true;log('SECRET_WALK','start='..walkStart..' x='..h.x..' from='..walkX)
     else press(side,h.x<v.x and'Left'or'Right')end
    else walkStart=nil;walkX=nil;press(side,'Block')end
   elseif not jumped then
    if jumpStart and h.y<h.floor and h.action~=1283 then jumped=true;log('SECRET_JUMP','start='..jumpStart..' action='..h.action..' y='..h.y..' floor='..h.floor)
    elseif ready(h)then jumpStart=jumpStart or frame;press(side,'Up')end
   elseif not punched then
    if punchStart and h.action==257 then punched=true;log('SECRET_PUNCH','start='..punchStart)
    elseif ready(h)and not punchStart then punchStart=frame;press(side,'High Punch')
    elseif punchStart and frame-punchStart<4 then press(side,'High Punch')
    elseif punchStart and frame-punchStart>30 then punchStart=nil end
   elseif not recovered then
    if ready(h)then recovered=frame;log('SECRET_RECOVER','hp='..h.hp)end
   elseif frame-recovered>=180 then
    log('SECRET_COMPLETE','epoch='..epoch..' recovered='..recovered..' human='..h.id..' cpu='..v.id..' arena='..arena);manager.machine:exit()
   else press(side,'Block')end
  end
  if h and v then log('SECRET_FIELD',string.format('mode=%d arena=%d ids=%d,%d rosters=%d,%d states=%d,%d actors=%08X,%08X owners=%08X,%08X mains=%08X,%08X hp=%d,%d actions=%d,%d',
   mode,arena,h.id,v.id,h.roster,v.roster,h.state,v.state,h.actor,v.actor,h.owner,v.owner,h.main,v.main,h.hp,v.hp,h.action,v.action))end
 end
 if not accepted''')
source += '''
taps[#taps+1]=p:install_write_tap(0x01061cc0,0x01061ccf,'actual Toasty popup',function(at,data,mask)
 if mask==0xffff and cpu.PC.value==0xffa0baf0 and p:read_u16(0x01061ac0)==7 then
  toast=frame;log('SECRET_TOASTY',string.format('tick=%d pc=%08X',data&0xffff,cpu.PC.value))
 end
end)
taps[#taps+1]=p:install_write_tap(0x010601d0,0x010601df,'actual secret acceptance',function(at,data,mask)
 if mask==0xffff and data&0xffff==15 then
  accepted=frame;log('SECRET_ACCEPT',string.format('pc=%08X arena=%d task=%08X secretID=%d taskSide=%d in0=%08X tick=%d toastTick=%d',
   cpu.PC.value,p:read_u16(0x01061ac0),cpu.A13.value,p:read_u16(cpu.A13.value+0x120),p:read_u16(cpu.A13.value+0x100),p:read_u32(0x01600000),p:read_u16(0x0105d090),p:read_u16(0x01061cc0)))
 end
end)
for n=1,2 do
 taps[#taps+1]=p:install_write_tap(slots[n].hp,slots[n].hp+15,'secret native health',function(at,data,mask)
  if accepted and mask==0xffff then log('SECRET_HEALTH',string.format('slot=%d before=%d after=%d pc=%08X',n,p:read_u16(at),data&0xffff,cpu.PC.value))end
 end)
end
'''
assert ':write_' not in source and ':snapshot(' not in source and "read('a')" not in source
out.mkdir()
lua=out/'stage.lua';lua.write_text(source)
runner=(base/'sonya_p1_kitana.ps1').read_text().replace(
    base.name+'/sonya_p1_kitana.lua',out.name+'/stage.lua').replace(
    sync.sha(base/'sonya_p1_kitana.lua'),sync.sha(lua)).replace(
    'audit_current_stock_pit_initialized_selector_sonya_p1_kitana_runtime','audit_current_sonya_natural_smoke_runtime').replace(
    "$env:MK2KS_STAGE_ARENA='6'", "$env:MK2KS_STAGE_ARENA='7'")
(out/'run.ps1').write_text(runner)
print('Prepared natural SonyaP1/Kitana rotation to Portal;28000fields/90sec/320MiB;no media or forced RNG')
