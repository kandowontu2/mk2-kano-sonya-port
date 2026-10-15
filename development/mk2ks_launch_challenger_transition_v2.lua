-- Correct only the generated observer's bracket delimiter; retain failed source.
local f=assert(io.open('mk2ks_launch_challenger_transition.lua','rb'));local s=f:read('a'):gsub('\r\n','\n');f:close()
local before=' taps[#taps+1]])';local a,b=assert(s:find(before,1,true));assert(not s:find(before,b+1,true))
s=s:sub(1,a-1)..' taps[#taps+1]\n]])'..s:sub(b+1)
assert(load(s,'@complete_launch_challenger_transition_correct_delimiter','t',_G))()
