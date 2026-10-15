"""Extend the existing passive audio observer to the other earned slot routes."""
import verify_native_source_sync as sync
sync.verify()
pit=(sync.ROOT/'audit_current_native_pit_audio_preparation/stage.lua').read_text()
marker='local channel={}'
assert pit.count(marker)==1
observer=pit[pit.index(marker):]
base=sync.ROOT/'audit_current_stock_tomb_other_sides_preparation'
out=sync.ROOT/'audit_current_stock_tomb_other_sides_audio_preparation'
assert not out.exists()
out.mkdir()
for case in ('sonya_p1_kitana','kano_p2_subzero'):
    source=(base/(case+'.lua')).read_text()
    assert ':write_' not in source and 'snapshot(' not in source
    lua=out/(case+'.lua')
    lua.write_text(source+'\n'+observer)
    runner=(base/(case+'.ps1')).read_text()
    runner=runner.replace(base.name+'/'+case+'.lua',out.name+'/'+case+'.lua')
    runner=runner.replace(sync.sha(base/(case+'.lua')),sync.sha(lua))
    runner=runner.replace('audit_current_stock_tomb_'+case+'_runtime','audit_current_stock_tomb_other_sides_audio_'+case+'_runtime')
    (out/(case+'.ps1')).write_text(runner)
print('Prepared two bounded passive audio cases, no raw media')
