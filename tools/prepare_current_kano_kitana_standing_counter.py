"""Physical standing-HK recovery counter; unchanged earlier earned ladder."""
import verify_native_source_sync as sync
sync.verify()
base = sync.ROOT / 'audit_current_kano_kitana_close_guard_preparation'
out = sync.ROOT / 'audit_current_kano_kitana_standing_counter_preparation'
assert not out.exists()
source = (base / 'campaign.lua').read_text()
start = source.index('    if gap<105 and human.floor-human.y<=8 then')
end = source.index('    elseif ks_start and frame-ks_start<12 then', start)
branch = r'''    if gap<105 and human.floor-human.y<=8 then
     ks_start=nil
     local stance=human.action==0 or human.action==771 or human.action==772 or human.action==770 or human.action==1792 or human.action==1793
     local cpu_stance=other.action==0 or other.action==771 or other.action==772 or other.action==770
     if not kh_last or frame-kh_last~=1 then kh_start=nil;kh_retry=-1000 end
     kh_last=frame
     if kh_start and frame-kh_start<32 then
      local age=frame-kh_start
      if age>=6 and age<10 then press('High Kick')end
      if age>=10 then press('Down');press('Block')end
     elseif stance and human.flags&0x1c==0 and cpu_stance and other.floor-other.y<=8 and frame-kh_retry>=32 then
      kh_start=frame;kh_retry=frame
      log('KANO_KITANA_STANDING_COUNTER',string.format('gap=%d action=%d cpu_action=%d health=%d,%d',gap,human.action,other.action,human.hp,other.hp))
     else
      kh_start=nil;press('Down');press('Block')
     end
'''
source = 'local kh_last,kh_start,kh_retry=nil,nil,-1000\n' + source[:start] + branch + source[end:]
source += r'''
local kh_seen={}
emu.register_frame(function()
 if p:read_u16(0x01061b30)~=3 then return end
 local own=sample(side)
 if not own or own.id~=17 or own.roster~=17 or own.owner~=own.actor then return end
 if kh_seen.main~=own.main or kh_seen.action~=own.action then
  kh_seen.main=own.main;kh_seen.action=own.action
  log('KANO_STANDING_ACTION',string.format('actor=%08X main=%08X owner=%08X id=%d action=%d',own.actor,own.main,own.owner,own.id,own.action))
 end
end)
'''
assert ':write_' not in source and ':snapshot(' not in source
out.mkdir()
lua = out / 'campaign.lua'
lua.write_text(source)
runner = (base / 'run.ps1').read_text().replace(base.name + '/campaign.lua', out.name + '/campaign.lua').replace(sync.sha(base / 'campaign.lua'), sync.sha(lua)).replace('audit_current_kano_kitana_close_guard_runtime', 'audit_current_kano_kitana_standing_counter_runtime')
(out / 'run.ps1').write_text(runner)
print('Prepared physical standing counter:18000fields,no media,90sec/320MiB')
