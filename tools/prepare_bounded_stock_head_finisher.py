"""Real earned stock head finisher, remove legacy screenshot recorder."""
import json
import verify_native_source_sync as sync

def main():
    root=sync.ROOT;sync.verify()
    source=root/'mk2ks_stock_fatality_v1077.lua'
    lua=source.read_text()
    begin='emu.register_frame_done(function()\n if action_start and frame-action_start<=600'
    assert lua.count(begin)==1
    start=lua.index(begin);end=lua.index('emu.register_stop(function()',start)
    assert 'screen:snapshot' in lua[start:end]
    lua=lua[:start]+lua[end:]
    lua=r'''
for _,key in ipairs({'MK2KS_DIAGNOSTIC_CPU_ID','MK2KS_DIAGNOSTIC_LADDER_INDEX','MK2KS_DIAGNOSTIC_CPU_HEALTH','MK2KS_DIAGNOSTIC_P1_REGEN','MK2KS_DIAGNOSTIC_ALL_STAGES'})do
 assert(not os.getenv(key),'No forced finisher assistance')
end
'''+lua+r'''
emu.register_frame(function()
 if action_start and wrap and frame-wrap>=120 then
  log('BOUNDED_TERMINAL','reason=native_common_completion_followthrough raw_media=none')
  manager.machine:exit()
 elseif frame>=5800 then
  log('BOUNDED_FAILED','reason=earned_finisher_timeout raw_media=none')
  manager.machine:exit()
 end
end)
'''
    for banned in (':write_', ':snapshot(', ':pixels(', 'snapshot_pixels','io.open('):
        assert banned not in lua,banned
    old=root/'audit_bounded_native_pain_voice_preparation'
    out=root/'audit_bounded_stock_head_finisher_preparation';assert not out.exists()
    out.mkdir();target=out/'prepared_observer.lua';target.write_text(lua)
    for fighter in ('sonya','kano'):
        runner=(old/f'run_{fighter}.ps1').read_text().replace(old.name,out.name)
        runner=runner.replace(sync.sha(old/'prepared_observer.lua'),sync.sha(target))
        runner=runner.replace(f'audit_bounded_{fighter}_native_pain_voice_runtime',
                              f'audit_bounded_{fighter}_stock_head_finisher_runtime')
        needle="$env:MK2KS_HUMAN_SPECIAL_VICTIM='kitana'"
        assert runner.count(needle)==1
        runner=runner.replace(needle,needle+f"\n$env:MK2KS_TEST_FIGHTER='{fighter}'\n$env:MK2KS_CAMPAIGN_SIDE='1'\n$env:MK2KS_STOCK_KILLER='baraka'\n$env:MK2KS_STOCK_COMMAND='bbbb_hp'\n$env:MK2KS_STOCK_GAP='64'")
        (out/f'run_{fighter}.ps1').write_text(runner)
    (out/'report.json').write_text(json.dumps(dict(prepared=True,acceptance=False,
        originalDriverSha256=sync.sha(source),observerSha256=sync.sha(target),rawMedia='none')))

if __name__=='__main__':main()
