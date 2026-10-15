"""Extend qualified physical HK/ring timing to Baraka3 with passive HP context."""
import verify_native_source_sync as sync
sync.verify()
base=sync.ROOT/'audit_current_sonya_p2_reptile_hk_early_retreat_preparation'
out=sync.ROOT/'audit_current_sonya_p2_baraka_hk_ring_preparation'
assert not out.exists()
source=(base/'campaign.lua').read_text()
for old,new in [("(other.roster==8 or other.roster==2 or other.roster==0 or other.roster==9) then","(other.roster==8 or other.roster==2 or other.roster==0 or other.roster==9 or other.roster==3) then"),('(other.roster==2 or other.roster==0 or other.roster==9) and 100 or 90','(other.roster==2 or other.roster==0 or other.roster==9 or other.roster==3) and 100 or 90'),('(other.roster==9 and 6 or 10)','((other.roster==9 or other.roster==3) and 6 or 10)')]:
    assert source.count(old)==1,old
    source=source.replace(old,new)
start=source.index("for observed_slot,observed_hp in ipairs({0x010602f0,0x01060ec0})do\n")
end=source.index('\nend\n',start)+5
block=source[start:end].replace('~=1 then return end','~=6 then return end').replace('c.id~=8 or c.roster~=8','c.id~=3 or c.roster~=3').replace('ids=8,18','ids=3,18').replace('SONYA_SUBZERO_DAMAGE','SONYA_BARAKA_DAMAGE').replace('passive actual Sonya Subzero damage','passive actual Sonya Baraka damage')
assert 'SONYA_BARAKA_DAMAGE' in block
source=source[:end]+block+source[end:]
assert ':write_' not in source and ':snapshot(' not in source
out.mkdir();lua=out/'campaign.lua';lua.write_text(source)
runner=(base/'run.ps1').read_text().replace(base.name+'/campaign.lua',out.name+'/campaign.lua').replace(sync.sha(base/'campaign.lua'),sync.sha(lua)).replace('audit_current_sonya_p2_reptile_hk_early_retreat_runtime','audit_current_sonya_p2_baraka_hk_ring_runtime')
(out/'run.ps1').write_text(runner)
print('Baraka3 HK/ring+early retreat, actual HP tap;90sec/320MiB/10MiB/no media')
