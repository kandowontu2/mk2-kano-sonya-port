"""Change physical Reptile approach only; retain native cold campaign."""
import verify_native_source_sync as sync
sync.verify()
base=sync.ROOT/'audit_current_sonya_reptile_crouch_counter_preparation'
out=sync.ROOT/'audit_current_sonya_reptile_reactive_preparation';assert not out.exists()
source=(base/'campaign.lua').read_text()
assert source.count("other.roster==9 and 'uppercut'")==1
source=source.replace("other.roster==9 and 'uppercut'","other.roster==9 and 'reactive'")
source=source.replace('frame>=12000','frame>=20000').replace('maximum_fields=12000','maximum_fields=20000')
out.mkdir();lua=out/'campaign.lua';lua.write_text(source)
runner=(base/'run.ps1').read_text().replace(base.name+'/campaign.lua',out.name+'/campaign.lua').replace(sync.sha(base/'campaign.lua'),sync.sha(lua))
runner=runner.replace('audit_current_sonya_reptile_crouch_counter_runtime','audit_current_sonya_reptile_reactive_runtime').replace("'-str','400'","'-str','700'")
(out/'run.ps1').write_text(runner)
print('Prepared20k physical reactive jumpkick route against Reptile only; unchanged Baraka, no media/assistance')
