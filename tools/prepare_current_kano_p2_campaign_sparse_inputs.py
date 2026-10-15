"""Same physical controller with redundant INPUT log suppression; no state edits."""
import json
import verify_native_source_sync as sync
sync.verify()
base=sync.ROOT/'audit_current_kano_p2_kitana_campaign_43000_preparation'
out=sync.ROOT/'audit_current_kano_p2_campaign_sparse_inputs_preparation'
assert not out.exists()
original=(base/'campaign.lua').read_text()
marker='local function log(tag,value)\n'
skip=" if tag=='INPUT' and frame>=1690 then return end\n"
assert original.count(marker)==1 and original.count('frame>=43000')==1
source=original.replace(marker,marker+skip).replace('frame>=43000','frame>=60000').replace('maximum_fields=43000','maximum_fields=60000')
assert source.replace(skip,'').replace('frame>=60000','frame>=43000').replace('maximum_fields=60000','maximum_fields=43000')==original
assert ':write_' not in source and ':snapshot(' not in source
out.mkdir();lua=out/'campaign.lua';lua.write_text(source)
runner=(base/'run.ps1').read_text().replace(base.name+'/campaign.lua',out.name+'/campaign.lua').replace(sync.sha(base/'campaign.lua'),sync.sha(lua)).replace('audit_current_kano_p2_kitana_campaign_43000_runtime','audit_current_kano_p2_campaign_sparse_inputs_runtime').replace("'-str','950'","'-str','1250'")
(out/'run.ps1').write_text(runner)
(out/'preparation.json').write_text(json.dumps(dict(controllerNormalizedExactlyUnchanged=True,priorLuaSHA256=sync.sha(base/'campaign.lua'),newLuaSHA256=sync.sha(lua),onlyChanges=['INPUT log suppression after1690','host field bound43000to60000'],fullCampaignAccepted=False),indent=2))
print('Identical physical controller; INPUT-log-only suppression;60000field target/90sec/320MiB/10MiB/no media')
