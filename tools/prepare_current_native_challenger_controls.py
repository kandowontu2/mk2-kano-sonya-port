"""Natural added/stock CPU controls, physical join after first-live180 fields."""
import verify_native_source_sync as sync
sync.verify()
base=sync.ROOT/'audit_current_native_challenger_join_delay_preparation'
out=sync.ROOT/'audit_current_native_challenger_controls_preparation'
assert not out.exists()
source=(base/'campaign.lua').read_text()
start=source.index("taps[#taps+1]=p:install_write_tap(0x01d01030,0x01d0103f,'paid join actual CPU launch'")
end=source.index('emu.register_frame(function()',start)
source=source[:start]+source[end:]
needle=' join_coin:clear_value();join_button:clear_value()'
assert source.count(needle)==1
source=source.replace(needle,''' if not join_start and first_live and frame-first_live>=180 and p:read_u16(0x010601d0)==2 then
  local actual=sample(1)
  if actual and actual.state==0 and actual.owner==actual.actor then
   join_start=frame
   log('JOIN_TRIGGER',string.format('policy=after_live180 live_age=%d actor=%08X main=%08X id=%d roster=%d state=%d',frame-first_live,actual.actor,actual.main,actual.id,actual.roster,actual.state))
  end
 end
'''+needle)
source=source.replace('p2=%d credits=%d','p2=%d in1=%d')
out.mkdir();lua=out/'campaign.lua';lua.write_text(source)
runner=(base/'run.ps1').read_text().replace(base.name+'/campaign.lua',out.name+'/campaign.lua').replace(sync.sha(base/'campaign.lua'),sync.sha(lua))
for label,boot in [('added',600),('stock',700)]:
 text=runner.replace('audit_current_native_challenger_join_delay_runtime',f'audit_current_native_challenger_{label}_control_runtime')
 text=text.replace("MK2KS_TEST_BOOT_FRAME='600'",f"MK2KS_TEST_BOOT_FRAME='{boot}'")
 (out/f'run_{label}.ps1').write_text(text)
print('Prepared natural CPU controls after live180, genuine Coin1/Start1, actual state/no media')
