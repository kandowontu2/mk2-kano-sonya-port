"""Hash individual stereo frames in the sole remaining sixteen-frame block."""
import json
import verify_native_source_sync as sync

def main():
    sync.verify()
    old=sync.ROOT/'audit_bounded_twohuman_hit_pcm_boundary_preparation'
    out=sync.ROOT/'audit_bounded_twohuman_pcm_boundary_frames_preparation';assert not out.exists()
    source=(old/'prepared_observer.lua').read_text()+r'''
emu.register_sound_update(function()
 if not command or emu.time()<25.459 or emu.time()>25.461 then return end
 local raw=manager.machine.sound:get_samples();assert(#raw==3840)
 for n=0,15 do
  log('PCM_STEREO_FRAME',string.format('seconds=%.12f stereo_frame=%d sha256=%s raw_media=none',emu.time(),n,pcm_sha256(raw:sub(n*4+1,n*4+4))))
 end
end)
'''
    out.mkdir();observer=out/'prepared_observer.lua';observer.write_text(source)
    for label in ('samples','nosamples'):
        runner=(old/f'run_{label}.ps1').read_text()
        for before,after in {old.name:out.name,
            f'audit_bounded_twohuman_hit_pcm_boundary_{label}_runtime':f'audit_bounded_twohuman_pcm_boundary_frames_{label}_runtime',
            sync.sha(old/'prepared_observer.lua'):sync.sha(observer)}.items():
            assert runner.count(before)==1;runner=runner.replace(before,after)
        (out/f'run_{label}.ps1').write_text(runner)
    (out/'report.json').write_text(json.dumps(dict(prepared=True,observerSHA256=sync.sha(observer),rawMedia=False)))

if __name__=='__main__':main()
