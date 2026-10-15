"""Physical approach, stock punch, and added-fighter counter-punch."""
import json
import verify_native_source_sync as sync

def main():
    root=sync.ROOT;sync.verify();old=root/'audit_bounded_aerial_all_query_preparation'
    lua=(old/'prepared_observer.lua').read_text()
    marker="  if age>=180 then log('IDLE_TERMINAL','fields=180 policy=physical_aerial_motion');manager.machine:exit();return end"
    assert lua.count(marker)==1
    lua=lua.replace(marker,"  if age>=240 then log('IDLE_TERMINAL','fields=240 policy=physical_contact_reaction');manager.machine:exit();return end",1)
    marker="  if age>=8 and age<12 then input(1,'Up')end\n  if age>=72 and age<76 then input(1,'Up');input(1,'Right')end"
    assert lua.count(marker)==1
    lua=lua.replace(marker,"  if age>=8 and age<104 and math.abs(a.x-b.x)>45 then input(1,a.x<b.x and 'Right' or 'Left')end\n  if age>=112 and age<116 then input(2,'High Punch')end\n  if age>=152 and age<156 then input(1,'High Punch')end",1)
    lua+=r'''
local contact_health_taps={}
for n,s in ipairs(slots)do
 contact_health_taps[#contact_health_taps+1]=p:install_write_tap(s.hp,s.hp+15,'actual physical contact health',function(at,data,mask)
  if not ready or at~=s.hp then return end
  log('CONTACT_HEALTH',string.format('slot=%d before=%d after=%d mask=%04X pc=%08X',n,p:read_u16(at),data&65535,mask,regs.PC.value))
 end)
end
emu.register_stop(function()assert(#contact_health_taps==2)end)
'''
    out=root/'audit_bounded_contact_reaction_preparation';out.mkdir(exist_ok=False)
    target=out/'prepared_observer.lua';target.write_text(lua)
    for fighter in ('sonya','kano'):
        runner=(old/f'run_{fighter}.ps1').read_text().replace(old.name,out.name)
        runner=runner.replace(sync.sha(old/'prepared_observer.lua'),sync.sha(target))
        runner=runner.replace(f'audit_bounded_{fighter}_aerial_all_query_runtime',f'audit_bounded_{fighter}_contact_reaction_runtime')
        (out/f'run_{fighter}.ps1').write_text(runner)
    (out/'report.json').write_text(json.dumps(dict(prepared=True,acceptance=False,observerSha=sync.sha(target),maximumReadyFields=240)))

if __name__=='__main__':main()
