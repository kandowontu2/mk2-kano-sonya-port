"""CPU5-only staged physical crouch/upper, native flags and owned contacts."""
import verify_native_source_sync as sync
sync.verify()
base=sync.ROOT/'audit_current_kano_p2_mileena_gap90_preparation'
out=sync.ROOT/'audit_current_kano_p2_mileena_crouch_upper_preparation'
assert not out.exists()
source=(base/'campaign.lua').read_text()
marker="   if fighter=='kano' and side==2 and (other.roster==18 or other.roster==8 or other.roster==2 or other.roster==5) then"
assert source.count(marker)==1
new="""   if fighter=='kano' and side==2 and other.roster==5 then
    local forward=human.x<other.x and 'Right' or 'Left'
    local height=human.floor-human.y
    if not mu_last or frame-mu_last~=1 then mu_down=nil;mu_upper=-1000 end
    mu_last=frame
    local ready=height==0 and human.flags&0x1c==0 and human.action==770
    if gap>70 and height<=8 and other.flags&0x10==0 then
     mu_down=nil;press(forward)
    else
     mu_down=mu_down or frame;press('Down')
     if ready and gap<75 and frame-mu_down>=12 and frame-mu_upper>=28 then
      mu_upper=frame;press('High Punch')
      log('MILEENA_UPPER_INPUT',string.format('gap=%d height=%d action=%d flags=%04X native_counter=%d health=%d,%d',gap,height,human.action,human.flags,p:read_u16(human.main+0x220),human.hp,other.hp))
     end
    end
   elseif fighter=='kano' and side==2 and (other.roster==18 or other.roster==8 or other.roster==2) then"""
source=source.replace(marker,new)
assert ':write_' not in source and ':snapshot(' not in source
out.mkdir();lua=out/'campaign.lua';lua.write_text(source)
runner=(base/'run.ps1').read_text().replace(base.name+'/campaign.lua',out.name+'/campaign.lua').replace(sync.sha(base/'campaign.lua'),sync.sha(lua)).replace('audit_current_kano_p2_mileena_gap90_runtime','audit_current_kano_p2_mileena_crouch_upper_runtime')
(out/'run.ps1').write_text(runner)
print('CPU5-only staged Down12/trueaction770/HP/gap75/retry28;90sec/320MiB/10MiB/no media')
