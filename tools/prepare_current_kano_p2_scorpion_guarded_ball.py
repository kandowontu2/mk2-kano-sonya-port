"""Reuse verified guarded LK84/release ball tactic against real CPU Scorpion."""
import verify_native_source_sync as sync
sync.verify()
base=sync.ROOT/'audit_current_kano_p2_scorpion_choke_preparation'
out=sync.ROOT/'audit_current_kano_p2_scorpion_guarded_ball_preparation'
assert not out.exists()
source=(base/'campaign.lua').read_text()
start=source.index("    local forward=human.x<other.x and 'Right' or 'Left'",source.index("elseif fighter=='kano' and side==2 and other.roster==3 then"))
end=source.index('   elseif (leg_tactic',start)
branch="""    local height=human.floor-human.y
    local stance=human.action==0 or human.action==771 or human.action==772 or human.action==770 or human.action==1792 or human.action==1793
    local ready=height<=8 and human.flags&0x1c==0 and stance
    if not sb_last or frame-sb_last~=1 then sb_start=nil;sb_release=-1000 end
    sb_last=frame
    if sb_start then
     local age=frame-sb_start
     if age<84 or not ready then press('Low Kick');press('Down');press('Block')
     else sb_start=nil;sb_release=frame end
    elseif ready and frame-sb_release>=60 then
     sb_start=frame;press('Low Kick');press('Down');press('Block')
    elseif human.action~=523 and frame-sb_release>=12 then press('Down');press('Block')end
"""
source=source[:start]+branch+source[end:]
assert ':write_' not in source and ':snapshot(' not in source
out.mkdir();lua=out/'campaign.lua';lua.write_text(source)
runner=(base/'run.ps1').read_text().replace(base.name+'/campaign.lua',out.name+'/campaign.lua').replace(sync.sha(base/'campaign.lua'),sync.sha(lua)).replace('audit_current_kano_p2_scorpion_choke_runtime','audit_current_kano_p2_scorpion_guarded_ball_runtime')
(out/'run.ps1').write_text(runner)
print('Physical guardedLK84/native523release;32000fields/90sec/320MiB/10MiB/no media')
