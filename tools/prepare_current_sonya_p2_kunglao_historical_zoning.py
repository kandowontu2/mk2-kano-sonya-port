"""Extract physical inputs only from retained full-clear controller, no recorder."""
import json
import verify_native_source_sync as sync
sync.verify()
base=sync.ROOT/'audit_current_sonya_p2_kunglao_contact_trace_preparation'
old=sync.ROOT/'mk2ks_natural_campaign_shao_ring_retreat_v3485.lua'
out=sync.ROOT/'audit_current_sonya_p2_kunglao_historical_zoning_preparation'
assert not out.exists()
matrix=json.loads((sync.ROOT/'audit_v5698_current_campaign_four_case_matrix_checked/report.json').read_text())
pins={str(name).replace('\\','/').lower():digest for name,digest in matrix['inputHashes'].items()}
assert pins[str(old).replace('\\','/').lower()]==sync.sha(old)
prior=old.read_text()
start=prior.index("   elseif strategy=='zoning' then\n")
end=prior.index('   else\n    -- Read-only feedback:',start)
branch=prior[start:end]
branch=branch.replace("   elseif strategy=='zoning' then","   elseif fighter=='sonya' and side==2 and other.roster==0 then")
for name in ('projectile_start','projectile_direction','last_jump'):
    branch=branch.replace(name,'kz_'+name)
source=(base/'campaign.lua').read_text()
marker="   elseif fighter=='sonya' and side==2 and (other.roster==8 or other.roster==2 or other.roster==0) then"
assert source.count(marker)==1
source=source.replace(marker,branch+marker)
source='local kz_projectile_start,kz_projectile_direction=nil,nil\nlocal kz_last_jump=-1000\n'+source
assert ':write_' not in source and ':snapshot(' not in source
out.mkdir();lua=out/'campaign.lua';lua.write_text(source)
(out/'policy-provenance.json').write_text(json.dumps(dict(oldController=str(old),oldControllerSHA256=sync.sha(old),historicalClearIsCurrentAcceptance=False,extractedPhysicalBranchOnly=True),indent=2)+'\n')
runner=(base/'run.ps1').read_text().replace(base.name+'/campaign.lua',out.name+'/campaign.lua').replace(sync.sha(base/'campaign.lua'),sync.sha(lua)).replace('audit_current_sonya_p2_kunglao_contact_trace_runtime','audit_current_sonya_p2_kunglao_historical_zoning_runtime')
(out/'run.ps1').write_text(runner)
print('Historical physical zoning branch only/currentbuild;60k/90sec/320MiB/10MiB/no media')
