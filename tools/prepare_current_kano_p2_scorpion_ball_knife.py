"""Physical low-health knife followup; retain guarded ball until CPUHP<=33."""
import verify_native_source_sync as sync
sync.verify()
base=sync.ROOT/'audit_current_kano_p2_scorpion_guarded_ball_preparation'
out=sync.ROOT/'audit_current_kano_p2_scorpion_ball_knife_preparation'
assert not out.exists()
source=(base/'campaign.lua').read_text()
marker='    if sb_start then\n'
assert source.count(marker)==1
extra="""    if sf_start and frame-sf_start<64 then
     local age=frame-sf_start
     if age>=2 and age<5 then press('Down')end
     if age>=7 and age<10 then press(sf_back)end
     if age>=8 and age<12 then press('High Punch')end
     if age>=15 then press('Down');press('Block')end
    elseif other.hp<=33 and ready then
     sf_start=frame;sf_back=human.x<other.x and 'Left' or 'Right';sb_start=nil
     log('SCORPION_LOW_KNIFE_PLAN',string.format('gap=%d health=%d,%d action=%d cpu_action=%d',gap,human.hp,other.hp,human.action,other.action))
    elseif sb_start then
"""
source=source.replace(marker,extra)
source=source.replace('then sb_start=nil;sb_release=-1000 end','then sb_start=nil;sb_release=-1000;sf_start=nil end')
assert ':write_' not in source and ':snapshot(' not in source
out.mkdir();lua=out/'campaign.lua';lua.write_text(source)
runner=(base/'run.ps1').read_text().replace(base.name+'/campaign.lua',out.name+'/campaign.lua').replace(sync.sha(base/'campaign.lua'),sync.sha(lua)).replace('audit_current_kano_p2_scorpion_guarded_ball_runtime','audit_current_kano_p2_scorpion_ball_knife_runtime')
(out/'run.ps1').write_text(runner)
print('Physical guardedball then CPUHP<=33 native knifecommand;32000fields/90sec/320MiB/10MiB/no media')
