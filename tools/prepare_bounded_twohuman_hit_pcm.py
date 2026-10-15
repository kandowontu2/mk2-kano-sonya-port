"""Transient mixed-update hashes, paired sample option controls."""
import json
import verify_native_source_sync as sync

def main():
    sync.verify()
    old=sync.ROOT/'audit_bounded_twohuman_hit_voice_state_preparation'
    out=sync.ROOT/'audit_bounded_twohuman_hit_pcm_preparation';assert not out.exists()
    source=(old/'prepared_observer.lua').read_text()+(sync.ROOT/'tools/bounded_pcm_sha256.lua').read_text()+r'''
local human_hit_updates=0
emu.register_sound_update(function()
 if not command or frame-command>160 then return end
 local raw=manager.machine.sound:get_samples();assert(#raw>0 and #raw%4==0)
 local energy,peak=0,0
 for at=1,#raw,2 do local value=string.unpack('<i2',raw,at);energy=energy+value*value;peak=math.max(peak,math.abs(value))end
 human_hit_updates=human_hit_updates+1
 log('PCM',string.format('seconds=%.12f bytes=%d sha256=%s energy=%d peak=%d raw_media=none',emu.time(),#raw,pcm_sha256(raw),energy,peak))
end)
emu.register_stop(function()log('PCM_STOP','updates='..human_hit_updates..' raw_media=none')end)
'''
    out.mkdir();observer=out/'prepared_observer.lua';observer.write_text(source)
    for label in ('samples','nosamples'):
        runner=(old/'run.ps1').read_text()
        for before,after in {old.name:out.name,
            'audit_bounded_twohuman_hit_voice_state_runtime':f'audit_bounded_twohuman_hit_pcm_{label}_runtime',
            sync.sha(old/'prepared_observer.lua'):sync.sha(observer)}.items():
            assert runner.count(before)==1;runner=runner.replace(before,after)
        if label=='nosamples':
            assert runner.count("'-samples'")==1;runner=runner.replace("'-samples'","'-nosamples'")
        (out/f'run_{label}.ps1').write_text(runner)
    (out/'report.json').write_text(json.dumps(dict(prepared=True,observerSHA256=sync.sha(observer),rawMedia=False)))

if __name__=='__main__':main()
