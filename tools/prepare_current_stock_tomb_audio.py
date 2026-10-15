"""Sparse existing native sound-word/channel0 observer; no PCM or images."""
import verify_native_source_sync as sync
sync.verify()
pit=(sync.ROOT/'audit_current_native_pit_audio_preparation/stage.lua').read_text()
marker='local channel={}';assert pit.count(marker)==1
observer=pit[pit.index(marker):].replace('native Pit sound words','native stock-victim Tomb sound words')
out=sync.ROOT/'audit_current_stock_tomb_audio_preparation'
assert not out.exists();out.mkdir()
for case in ('kunglao','jax_sonya_p2'):
    base=sync.ROOT/('audit_current_native_tomb_stock_'+case+'_preparation')
    source=(base/'stage.lua').read_text()+'\n'+observer
    lua=out/(case+'.lua');lua.write_text(source)
    runner=(base/'run.ps1').read_text().replace(base.name+'/stage.lua',out.name+'/'+case+'.lua').replace(sync.sha(base/'stage.lua'),sync.sha(lua)).replace('audit_current_native_tomb_stock_'+case+'_runtime','audit_current_stock_tomb_audio_'+case+'_runtime')
    (out/(case+'.ps1')).write_text(runner)
print('Prepared2boundedstockTomb passive channel0 audio traces,no PCM/images')
