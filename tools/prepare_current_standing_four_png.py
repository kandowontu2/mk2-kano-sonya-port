"""Prepare only: four physical idle matches; four PNGs <=256KiB total."""
import hashlib,json
from pathlib import Path
import verify_native_source_sync as sync

def main():
    sync.verify();root=sync.ROOT
    out=root/'audit_current_standing_four_png_v3_preparation'
    assert not out.exists();out.mkdir()
    source=(root/'audit_bounded_current_special_cycles_preparation/cycles.lua').read_text()
    # Reuse already inspected real-input ownership/sample/native-route routines only.
    lua="local identity=assert(tonumber(os.getenv('MK2KS_STANDING_ID')))\nlocal side=assert(tonumber(os.getenv('MK2KS_STANDING_SIDE')))\nassert((identity==17 or identity==18)and(side==1 or side==2))\nlocal spec={identity};local move='standing';local air=false\n"
    lua+=source[source.index("for _,key in ipairs({'MK2KS_DIAGNOSTIC_CPU_ID'"):source.index('local victim_name=')]
    lua+="local victim_name='kitana';local victim_id=4\nlocal expected=side==1 and {identity,4}or{4,identity}\n"
    lua+=source[source.index('local frame,css,live,ready'):source.index('for _,address in ipairs({spec[2]')]
    lua+=source[source.index('local function route(start,target)'):source.index('emu.register_frame_done(function()')]
    # Projection scalars bind the native camera/display transformation, not a floor rectangle.
    lua+="local capture=nil;local projection={}\n"
    lua+="""local tap=p:install_read_tap(0xff8042a0,0xff8042af,'standing actual projected body',function(at)
 if not capture or frame~=capture or at~=0xff8042a0 or regs.PC.value~=0xff8042b0 then return end
 for n=1,2 do local a=sample(n)
  if a and regs.A0.value==a.actor then projection[n]=(projection[n]or 0)+1
   log('PROJECTION',string.format('slot=%d actor=%08X pose=%08X source=%08X size=%08X xy=%08X display=%08X command=%08X pc=%08X',n,a.actor,a.pose,regs.A11.value,regs.A9.value,regs.A10.value,regs.A5.value,regs.A12.value,regs.PC.value))
  end
 end
end)
emu.register_frame_done(function()
 if capture~=frame then return end
 local a,b=sample(1),sample(2);assert(pair_live(a,b)and clean(a)and clean(b))
 assert(projection[1]and projection[2],'Missing same-frame native projection')
 part(1,a);part(2,b);log('CAPTURE','arena='..p:read_u16(0x01061ac0)..' width=400 height=254 cameraEvidence=native_display_and_xy')
 screen:snapshot(assert(os.getenv('MK2KS_STANDING_PNG')))
 log('COMPLETE','pngCount=1 rawBuffers=0');manager.machine:exit()
end)
emu.register_stop(function()tap:remove()end)
"""
    base=source[source.index('emu.register_frame(function()'):source.index(' if ready then\n  if not pair_live')]
    lua+=base+"\n if ready and not capture and clean(a)and clean(b)then settle=settle or frame;if frame-settle>=30 then capture=frame+1 end elseif not capture then settle=nil end\n if frame>6000 then log('FAILED','bounded_field_limit');manager.machine:exit()end\nend)\n"
    lua=lua.replace('and a.roster==a.id and b.roster==b.id','and a.hp>0 and b.hp>0 and a.roster==a.id and b.roster==b.id')
    (out/'standing.lua').write_text(lua)
    sha=sync.sha(out/'standing.lua').upper()
    runner=(root/'audit_bounded_current_special_cycles_preparation/run_leg_p1.ps1').read_text()
    runner=runner.replace("$taskCase=Join-Path $taskRoot 'audit_bounded_current_special_cycles_leg_p1_runtime'", "$taskCase=Join-Path $taskRoot ('audit_current_standing_'+$StandingId+'_p'+$StandingSide+'_runtime')")
    runner="param([ValidateSet(17,18)][int]$StandingId,[ValidateSet(1,2)][int]$StandingSide)\n"+runner
    runner=runner.replace('audit_bounded_current_special_cycles_preparation/cycles.lua','audit_current_standing_four_png_v3_preparation/standing.lua').replace('21C272F9D2DFCFFC7A1391D16E362D5EBF5863F3AC85E9B014926B7E2B155DE0',sha)
    first=runner.index("$env:MK2KS_HUMAN_SPECIAL_MOVE=");last=runner.index("$env:MK2KS_CPU_PAIR_APPROACH=",first)
    runner=runner[:first]+"$env:MK2KS_STANDING_ID=[string]$StandingId\n$env:MK2KS_STANDING_SIDE=[string]$StandingSide\n$env:MK2KS_STANDING_PNG=Join-Path $taskCase 'standing.png'\n"+runner[last:]
    runner=runner.replace("$env:MK2KS_CPU_PAIR_APPROACH='original'", "Remove-Item Env:MK2KS_CPU_PAIR_APPROACH -ErrorAction SilentlyContinue").replace("$env:MK2KS_CPU_CONTINUATION_POLICY='neutral_hold'", "Remove-Item Env:MK2KS_CPU_CONTINUATION_POLICY -ErrorAction SilentlyContinue")
    runner=runner.replace("$taskReport=[ordered]@{", "if(Test-Path -LiteralPath $env:MK2KS_STANDING_PNG){if((Get-Item -LiteralPath $env:MK2KS_STANDING_PNG).Length -gt 64KB){throw 'PNG exceeds per-case64KiB limit'}}\n$taskReport=[ordered]@{")
    runner=runner.replace("rawMedia='none'","rawMedia='one bounded400x254 PNG; no raw buffers'")
    (out/'run.ps1').write_text(runner)
    (out/'report.json').write_text(json.dumps(dict(prepared=True,executed=False,luaSHA256=sha,cases=[[17,1],[17,2],[18,1],[18,2]],pngCountLimit=4,pngTotalByteLimit=262144,perCasePngByteLimit=65536,physicalOnly=True,guestWrites=False,projectionSameFrame=True,opaqueSolesAccepted=False),indent=2))
    print(out,sha)

if __name__=='__main__':main()
