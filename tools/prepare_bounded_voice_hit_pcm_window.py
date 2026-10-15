"""Short-window mixed PCM scalar hashes on the existing real hit replay."""
import json
import verify_native_source_sync as sync

def main():
    sync.verify()
    old=sync.ROOT/'audit_bounded_native_voice_channels_preparation'
    out=sync.ROOT/'audit_bounded_voice_hit_pcm_window_preparation';assert not out.exists()
    source=(old/'prepared_observer.lua').read_text()+(sync.ROOT/'tools/bounded_pcm_sha256.lua').read_text()+r'''
local hit_pcm_count=0
emu.register_sound_update(function()
 if selection_frame<2500 or selection_frame>2700 then return end
 local raw=manager.machine.sound:get_samples();assert(#raw>0 and #raw%4==0)
 local energy,peak=0,0
 for offset=1,#raw,2 do
  local value=string.unpack('<i2',raw,offset)
  energy=energy+value*value;peak=math.max(peak,math.abs(value))
 end
 hit_pcm_count=hit_pcm_count+1
 print(string.format('MK2_HIT_PCM frame=%d seconds=%.12f bytes=%d sha256=%s energy=%d peak=%d writes=0 raw_media=none',selection_frame,emu.time(),#raw,pcm_sha256(raw),energy,peak))
end)
emu.register_stop(function()print(string.format('MK2_HIT_PCM_STOP updates=%d writes=0 raw_media=none',hit_pcm_count))end)
'''
    assert ':write_' not in source and ':snapshot(' not in source
    out.mkdir();observer=out/'prepared_observer.lua';observer.write_text(source)
    runner=(sync.ROOT/'tools/run_bounded_native_uppercut_probe.ps1').read_text()
    for before,after in {
        'audit_bounded_native_uppercut_runtime':'audit_bounded_voice_hit_pcm_window_runtime',
        'audit_bounded_native_uppercut_owners_bound_preparation':out.name,
        '92F2EBD73A57733ED7638FE90D78F57B10CD238742BB6F02C49BE0123323DE94':sync.sha(observer),
        '$taskRoot=Split-Path $PSScriptRoot -Parent':f'$taskRoot="{sync.ROOT}"',
    }.items():
        assert runner.count(before)==1;runner=runner.replace(before,after)
    runner="$env:MK2KS_TEST_BOOT_FRAME='608'\n$env:MK2KS_CPU_PAIR_CONFIRM_AGE='264'\n"+runner
    (out/'run.ps1').write_text(runner)
    (out/'report.json').write_text(json.dumps(dict(prepared=True,observerSHA256=sync.sha(observer),rawMedia=False,acceptance=False)))

if __name__=='__main__':main()
