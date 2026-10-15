"""Transient mixed PCM hashes/levels, no raw output or retained waveform arrays."""
import json
import verify_native_source_sync as sync

TAIL=r'''
local split_pcm_updates,split_pcm_bytes=0,0
local split_sample_channels={}
emu.register_frame(function()
 if frame==1 then
  for item,index in pairs(manager.machine.devices[':mk2ksvoices'].items)do
   local channel,field=item:match('^(%x+)/chan%.(.+)$')
   if channel and field=='source_num' then split_sample_channels[tonumber(channel,16)]=emu.item(index)end
  end
  for n=0,13 do assert(split_sample_channels[n])end
 end
 if action_start and frame-action_start>=1 then
  local active=0
  for n=0,13 do if split_sample_channels[n]:read(0)~=0xffffffff then active=active|(1<<n)end end
  print(string.format('MK2_SPLIT_SAMPLE_MASK frame=%d age=%d active=%04X writes=0 assistance=none',frame,frame-action_start,active))
 end
end)
emu.register_sound_update(function()
 if not action_start then return end
 local raw=manager.machine.sound:get_samples();assert(#raw>0 and #raw%4==0)
 local energy,peak,nonzero=0,0,0
 for offset=1,#raw,2 do
  local value=string.unpack('<i2',raw,offset)
  energy=energy+value*value;peak=math.max(peak,math.abs(value));if value~=0 then nonzero=nonzero+1 end
 end
 split_pcm_updates=split_pcm_updates+1;split_pcm_bytes=split_pcm_bytes+#raw
 print(string.format('MK2_SPLIT_PCM_DIGEST frame=%d seconds=%.12f bytes=%d sha256=%s energy=%d peak=%d nonzero=%d writes=0 assistance=none',frame,emu.time(),#raw,pcm_sha256(raw),energy,peak,nonzero))
end)
emu.register_stop(function()
 print(string.format('MK2_SPLIT_PCM_STOP frame=%d updates=%d bytes=%d raw_media=none writes=0 assistance=none',frame,split_pcm_updates,split_pcm_bytes))
end)
'''

def main():
    sync.verify();old=sync.ROOT/'audit_bounded_kung_lao_split_dcs_delivery_preparation'
    out=sync.ROOT/'audit_bounded_kung_lao_split_pcm_digest_preparation';assert not out.exists()
    text=(old/'prepared_observer.lua').read_text()+(sync.ROOT/'tools/bounded_pcm_sha256.lua').read_text()+TAIL
    for banned in (':write_', ':snapshot(', ':pixels(', 'io.open('):assert banned not in text
    out.mkdir();target=out/'prepared_observer.lua';target.write_text(text)
    for side in (1,2):
        for fighter in ('sonya','kano'):
            for enabled in (True,False):
                label='samples' if enabled else 'nosamples'
                runner=(old/f'run_{fighter}_p{side}.ps1').read_text().replace(old.name,out.name)
                runner=runner.replace(sync.sha(old/'prepared_observer.lua'),sync.sha(target))
                runner=runner.replace('kung_lao_split_dcs_delivery_runtime',f'kung_lao_split_pcm_{label}_runtime')
                if not enabled:
                    before="'-samples'";assert runner.count(before)==1;runner=runner.replace(before,"'-nosamples'")
                (out/f'run_{fighter}_p{side}_{label}.ps1').write_text(runner)
    (out/'report.json').write_text(json.dumps(dict(prepared=True,observerSha256=sync.sha(target),rawMedia=False,acceptance=False)))

if __name__=='__main__':main()
