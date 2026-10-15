-- Preserve6567's unpaid/early-START rejection. Reuse the whole actual driver.
-- This original cabinet setup charges two credits; the screen opens later.
local f=assert(io.open('mk2ks_single_continue_v6567.lua','rb'))
local source=f:read('*a');f:close()
local before="local age=frame-continueAt;pulse('Coin',age,20,5);pulse('Start',age,80,5)"
local after="local age=frame-continueAt;pulse('Coin',age,20,5);pulse('Coin',age,270,5);pulse('Start',age,310,5)"
local first,last=assert(source:find(before,1,true))
assert(not source:find(before,last+1,true),'Only exact cabinet payment input window changes')
source=source:sub(1,first-1)..after..source:sub(last+1)
assert(load(source,'@mk2ks_single_continue_v6567.lua::original_two_credit_paid_input'))()
