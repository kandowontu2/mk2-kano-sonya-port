"""Original physical campaign policy, scalar output and finite host deadline."""
import json
import verify_native_source_sync as sync
sync.verify()
out=sync.ROOT/'audit_bounded_campaign_progress_preparation';assert not out.exists();out.mkdir()
original=sync.ROOT/'mk2ks_natural_campaign_shao_knife_retreat_v3510.lua'
source=original.read_text()
sink="  local raw=p:read_range(0xff800000,0xffffffff,8,8);assert(#raw==1048576)\n  local file=assert(io.open(assert(os.getenv('MK2KS_CAMPAIGN_OUT'))..'/guest_maincpu.bin','wb'));file:write(raw);file:close()"
assert source.count(sink)==1;source=source.replace(sink,"  log('NO_RAW_DUMP','guest_memory_read_and_file_sink_omitted=true')")
assert source.count('screen:snapshot(')==6
source="local function discard_snapshot(...)end\n"+source.replace('screen:snapshot(','discard_snapshot(')
marker='emu.register_frame(function()\n';assert source.count(marker)==1
source=source.replace(marker,marker+" if frame>=12000 then log('HOST_BOUND','maximum_fields=12000 full_campaign_acceptance=false');manager.machine:exit();return end\n")
lua=out/'campaign.lua';lua.write_text(source)
base=(sync.ROOT/'audit_bounded_css_cadence_preparation/run_sonya_p1.ps1').read_text()
for fighter in ('kano','sonya'):
 for side in (1,2):
  runner=base.replace('audit_bounded_css_cadence_sonya_p1_runtime',f'audit_bounded_campaign_progress_{fighter}_p{side}_runtime')
  runner=runner.replace('audit_bounded_css_cadence_preparation/css.lua',out.name+'/campaign.lua')
  runner=runner.replace('1BEF196499DF6DD0FF3AE066D3C9C5DA6AC8E8A330B37D56530AF3C8E0555FD0',sync.sha(lua))
  start=runner.index('$env:MK2KS_UI_FIGHTER=');end=runner.index('$taskArgs=',start)
  strategy='defensive_leg' if fighter=='sonya' else 'zoning'
  runner=runner[:start]+f"$env:MK2KS_TEST_FIGHTER='{fighter}'\n$env:MK2KS_CAMPAIGN_SIDE='{side}'\n$env:MK2KS_CAMPAIGN_STRATEGY='{strategy}'\n$env:MK2KS_TEST_BOOT_FRAME='600'\n"+runner[end:]
  runner=runner.replace("'-str','65'","'-str','300'")
  (out/f'run_{fighter}_p{side}.ps1').write_text(runner)
(out/'report.json').write_text(json.dumps(dict(prepared=True,originalPhysicalPolicySHA256=sync.sha(original),maximumFields=12000,rawMedia=False,forcedGameState=False)))
