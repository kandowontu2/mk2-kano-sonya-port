"""Reuse passive winner channel observer on corrected earned stock Pit routes."""
import verify_native_source_sync as sync
sync.verify()
pit=(sync.ROOT/'audit_current_native_pit_audio_preparation/stage.lua').read_text()
marker='local channel={}'
assert pit.count(marker)==1
observer=pit[pit.index(marker):]
base=sync.ROOT/'audit_current_stock_pit_initialized_selector_preparation'
out=sync.ROOT/'audit_current_stock_pit_other_sides_audio_preparation'
assert not out.exists();out.mkdir()
for case in ('sonya_p1_kitana','kano_p2_subzero'):
    lua=out/(case+'.lua');lua.write_text((base/(case+'.lua')).read_text()+'\n'+observer)
    runner=(base/(case+'.ps1')).read_text().replace(base.name+'/'+case+'.lua',out.name+'/'+case+'.lua').replace(sync.sha(base/(case+'.lua')),sync.sha(lua)).replace('audit_current_stock_pit_initialized_selector_'+case+'_runtime','audit_current_stock_pit_other_sides_audio_'+case+'_runtime')
    (out/(case+'.ps1')).write_text(runner)
print('Prepared two passive Pit winner traces, run serially,no raw media')
