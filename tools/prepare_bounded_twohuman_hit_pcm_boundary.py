"""Sixteen-stereo-frame hashes only around the three cutoff updates."""
import json
import verify_native_source_sync as sync

def main():
    sync.verify()
    old=sync.ROOT/'audit_bounded_twohuman_hit_pcm_preparation'
    out=sync.ROOT/'audit_bounded_twohuman_hit_pcm_boundary_preparation';assert not out.exists()
    source=(old/'prepared_observer.lua').read_text()+r'''
emu.register_sound_update(function()
 if not command or emu.time()<25.439 or emu.time()>25.481 then return end
 local raw=manager.machine.sound:get_samples();assert(#raw==3840)
 for offset=1,#raw,64 do
  local part=raw:sub(offset,offset+63)
  log('PCM_BOUNDARY',string.format('seconds=%.12f first_stereo_frame=%d frames=16 sha256=%s raw_media=none',emu.time(),(offset-1)//4,pcm_sha256(part)))
 end
end)
'''
    out.mkdir();observer=out/'prepared_observer.lua';observer.write_text(source)
    for label in ('samples','nosamples'):
        runner=(old/f'run_{label}.ps1').read_text()
        for before,after in {old.name:out.name,
            f'audit_bounded_twohuman_hit_pcm_{label}_runtime':f'audit_bounded_twohuman_hit_pcm_boundary_{label}_runtime',
            sync.sha(old/'prepared_observer.lua'):sync.sha(observer)}.items():
            assert runner.count(before)==1;runner=runner.replace(before,after)
        (out/f'run_{label}.ps1').write_text(runner)
    (out/'report.json').write_text(json.dumps(dict(prepared=True,observerSHA256=sync.sha(observer),rawMedia=False,blockStereoFrames=16)))

if __name__=='__main__':main()
