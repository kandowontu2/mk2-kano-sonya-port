-- CONTROLLED ALTERNATE DIAGNOSTIC ONLY, NEVER NATURAL SELECTION ACCEPTANCE.
-- Original real coin/select/combat/native command driver is unchanged.
-- One explicit victim flag-6 write exercises the existing alternate branch.
dofile('mk2ks_stock_fatality_display_v1046.lua')
local p=manager.machine.devices[':maincpu'].spaces.program
local side=assert(tonumber(os.getenv('MK2KS_CAMPAIGN_SIDE')))
local identity=assert(({kano=17,sonya=18})[os.getenv('MK2KS_TEST_FIGHTER')])
local frame,applied=0,0
emu.register_frame(function()
 frame=frame+1
 if applied~=0 or p:read_u16(0x01061b00)~=3 then return end
 local actor=p:read_u32(side==1 and 0x01060220 or 0x01060df0)
 if actor<0x01000000 or actor>=0x01100000 or p:read_u16(actor+0x1f0)~=identity then return end
 local flags=p:read_u16(actor+0x160)
 assert(flags&0x40==0,'Expected normal before controlled flag')
 p:write_u16(actor+0x160,flags|0x40)
 applied=applied+1
 print(string.format('MK2_ARM_ALT_V1063_ASSIST frame=%d actor=%08X id=%d side=%d old=%04X new=%04X writes=1 assistance=controlled_alt_flag natural_selection_verified=false',
  frame,actor,identity,side,flags,flags|0x40))
end)
emu.register_stop(function()
 print(string.format('MK2_ARM_ALT_V1063_RESULT frame=%d applied=%d writes=%d assistance=controlled_alt_flag natural_selection_verified=false',frame,applied,applied))
end)
