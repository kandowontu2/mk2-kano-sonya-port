"""Hold actual Down before HP; never infer upper activation from input intent."""
import verify_native_source_sync as sync
sync.verify()
base=sync.ROOT/'audit_current_kano_p2_scorpion_upper_preparation'
out=sync.ROOT/'audit_current_kano_p2_scorpion_crouch_ready_preparation'
assert not out.exists()
source=(base/'campaign.lua').read_text()
start=source.index("    local forward=human.x<other.x and 'Right' or 'Left'",source.index("elseif fighter=='kano' and side==2 and other.roster==3 then"))
end=source.index('   elseif (leg_tactic',start)
branch="""    local forward=human.x<other.x and 'Right' or 'Left'
    local height=human.floor-human.y
    if not sc_last or frame-sc_last~=1 then sc_upper=-1000;sc_down=nil end
    sc_last=frame
    local ready=height==0 and human.flags&0x0c==0 and human.body&0x0c==0 and
     (human.action==770 or human.action==771 or human.action==772)
    if gap>100 and height<=8 and other.flags&0x10==0 then sc_down=nil;press(forward)
    else
     sc_down=sc_down or frame;press('Down')
     if ready and gap<105 and frame-sc_down>=12 and frame-sc_upper>=28 then
      sc_upper=frame;press('High Punch')
     elseif not ready and frame-sc_upper>=4 then press('Block')end
    end
"""
source=source[:start]+branch+source[end:]
assert ':write_' not in source and ':snapshot(' not in source
out.mkdir();lua=out/'campaign.lua';lua.write_text(source)
runner=(base/'run.ps1').read_text().replace(base.name+'/campaign.lua',out.name+'/campaign.lua').replace(sync.sha(base/'campaign.lua'),sync.sha(lua)).replace('audit_current_kano_p2_scorpion_upper_runtime','audit_current_kano_p2_scorpion_crouch_ready_runtime')
(out/'run.ps1').write_text(runner)
print('Physical Down12fields/actual grounded stance beforeHP;32000fields/90sec/320MiB/10MiB/no media')
