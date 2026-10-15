"""Wait actual attract; normal two-coin Start/reselect/control test."""
import verify_native_source_sync as sync
sync.verify()
base=sync.ROOT/'audit_current_kano_earned_postending_join_preparation'
out=sync.ROOT/'audit_current_kano_postending_two_coin_join_preparation'
assert not out.exists()
source=(base/'campaign.lua').read_text();source='local pj_attract=nil\n'+source
start=source.index(' if ending_completed then\n  local age=frame-ending_completed')
end=source.index(' if not css and frame>700',start)
source=source[:start]+''' if ending_completed then
  if not pj_attract and mode==1 then pj_attract=frame;log('POST_ENDING_ATTRACT','mode=1')end
  if pj_attract then
   local age=frame-pj_attract
   if age>=20 and not pj_reset then
    pj_reset=true;css=nil;css_exit=nil;loss_at=nil
    log('POST_ENDING_PAID_START','coin_ages=20,50 start_age=100 target=17')
   end
   if age>=20 and age<24 or age>=50 and age<54 then press('Coin')end
   if age>=100 and age<104 then press('Start')end
  end
 end
'''+source[end:]
assert source.count('frame-ending_completed>=6000')==1
source=source.replace('frame-ending_completed>=6000','frame-ending_completed>=12000').replace("maximum_fields=6000","maximum_fields=12000")
assert ':write_' not in source and ':snapshot(' not in source
out.mkdir();lua=out/'campaign.lua';lua.write_text(source)
runner=(base/'run.ps1').read_text().replace(base.name+'/campaign.lua',out.name+'/campaign.lua').replace(sync.sha(base/'campaign.lua'),sync.sha(lua)).replace('audit_current_kano_earned_postending_join_runtime','audit_current_kano_postending_two_coin_join_runtime')
(out/'run.ps1').write_text(runner)
print('Actualattract+twoCoin/Start/reselect/controls;180sec/320MiB/10MiB/no media')
