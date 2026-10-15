"""Compact only input printing; controller/guest reads and deadlines unchanged."""
import verify_native_source_sync as sync
sync.verify()
old=sync.ROOT/'audit_bounded_kano_campaign_18000_preparation'
out=sync.ROOT/'audit_bounded_compact_kano_campaign_preparation'
assert not out.exists()
out.mkdir()
base=old/'campaign.lua'
source=base.read_text()
marker='local function log(tag,value)\n'
assert source.count(marker)==1
source=source.replace(marker,'''local input_digest,input_events=2166136261,0
local function log(tag,value)
 if tag=='INPUT' then
  local bytes=tostring(frame)..':'..(value or'')
  for index=1,#bytes do input_digest=((input_digest~bytes:byte(index))*16777619)&0xffffffff end
  input_events=input_events+1
  return
 end
''')
source+='''
emu.register_frame(function()
 if frame%300==0 then log('INPUT_DIGEST',string.format('events=%d fnv32=%08X',input_events,input_digest))end
end)
emu.register_stop(function()
 log('INPUT_DIGEST_FINAL',string.format('events=%d fnv32=%08X',input_events,input_digest))
end)
'''
lua=out/'campaign.lua'
lua.write_text(source)
runner=(old/'run_kano_p1.ps1').read_text()
runner=runner.replace(old.name+'/campaign.lua',out.name+'/campaign.lua').replace(sync.sha(base),sync.sha(lua))
runner=runner.replace('audit_bounded_kano_campaign_18000_p1_runtime','audit_bounded_compact_kano_campaign_p1_runtime')
(out/'run_kano_p1.ps1').write_text(runner)
print('Prepared compact logging only: unchanged18000field/90sec/320MiB limits')
