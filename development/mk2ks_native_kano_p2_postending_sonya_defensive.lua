-- Ordinary defensive button policy for Subzero8 only. All native game state
-- and the earned tower/ending/fresh Sonya join remain unassisted.
local path='mk2ks_native_kano_p2_postending_sonya.lua'
local file=assert(io.open(path,'r'));local source=file:read('*a');file:close()
local before="one('-- Observe actual own special entries independently of intended button plans.',helper"
local at=assert(source:find(before,1,true))
assert(not source:find(before,at+#before,true),'One original physical controller expansion')
local policy=[=[
local old="if (leg_tactic or strategy=='lowkick'or strategy=='throw') and other.roster~=12 and other.roster~=13 then"
local new=[[
if strategy=='zoning' and other.roster==8 then
    local forward=human.x<other.x and'Right'or'Left'
    local height=human.floor-human.y
    local cpu_height=other.floor-other.y
    if gap>85 and (other.action==0x604 or other.action==0x10)then guard_until=frame+44 end
    if frame<guard_until and gap>65 then
     press('Down');press('Block')
    elseif close_start and frame-close_start<4 then
     press(forward);press('Low Punch')
    elseif height>8 then
     if gap<100 and frame%6<3 then press('High Kick')end
    elseif cpu_height>15 and gap<105 then
     press('Down')
     if frame-last_uppercut>=22 then press('High Punch');last_uppercut=frame
     else press('Block')end
    elseif gap>62 then
     close_start=nil;press(forward)
    elseif gap<42 and frame-last_close>=24 and human.flags&0x1c==0 and human.body&0x0c==0 then
     close_start=frame;last_close=frame;press(forward);press('Low Punch')
     log('DECISION','move=subzero_guarded_throw_attempt gap='..gap)
    elseif gap>=42 and frame-last_close>=24 and human.flags&0x1c==0 and human.body&0x0c==0 then
     last_close=frame;press('Down');press('Low Kick')
     log('DECISION','move=subzero_guarded_lowkick_attempt gap='..gap)
    else
     press('Down');press('Block')
    end
   elseif (leg_tactic or strategy=='lowkick'or strategy=='throw') and other.roster~=12 and other.roster~=13 then
]]
one(old,new)
]=]
source=source:sub(1,at-1)..policy..source:sub(at)
assert(load(source,'@'..path..'::ordinary_Subzero_defensive_buttons_only','t',_ENV))()
