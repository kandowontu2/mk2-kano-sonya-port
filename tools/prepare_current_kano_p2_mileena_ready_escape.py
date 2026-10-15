"""Knife recovery backjump deferred to actual grounded ready state, CPU5 only."""
import verify_native_source_sync as sync
sync.verify()
base=sync.ROOT/'audit_current_kano_p2_mileena_knife_escape_preparation'
out=sync.ROOT/'audit_current_kano_p2_mileena_ready_escape_preparation'
assert not out.exists()
source=(base/'campaign.lua').read_text()
old="""     if age>=24 and age<28 then press('Up');press(mj_back)end
     if age>=28 then
      press(mj_back)
      if height>8 and gap<120 and frame%6<3 then press('High Kick')end
     end"""
new="""     if age>=24 then
      local ready=height<=8 and human.flags&0x1c==0 and (human.action==0 or human.action==771 or human.action==772 or human.action==770 or human.action==1792 or human.action==1793 or human.action==3)
      if not mj_escape and ready then
       mj_escape=frame
       log('MILEENA_READY_ESCAPE_INPUT',string.format('age=%d gap=%d action=%d flags=%04X health=%d,%d',age,gap,human.action,human.flags,human.hp,other.hp))
      end
      press(mj_back)
      if mj_escape and frame-mj_escape<4 then press('Up')end
      if height>8 and gap<120 and frame%6<3 then press('High Kick')end
     end"""
assert source.count(old)==1
source=source.replace(old,new)
assert source.count('mj_start=frame;mj_back=back')==1
source=source.replace('mj_start=frame;mj_back=back','mj_start=frame;mj_back=back;mj_escape=nil')
assert ':write_' not in source and ':snapshot(' not in source
out.mkdir();lua=out/'campaign.lua';lua.write_text(source)
runner=(base/'run.ps1').read_text().replace(base.name+'/campaign.lua',out.name+'/campaign.lua').replace(sync.sha(base/'campaign.lua'),sync.sha(lua)).replace('audit_current_kano_p2_mileena_knife_escape_runtime','audit_current_kano_p2_mileena_ready_escape_runtime')
(out/'run.ps1').write_text(runner)
print('CPU5-only knife escape actualready afterage24;90sec/320MiB/10MiB/no media')
