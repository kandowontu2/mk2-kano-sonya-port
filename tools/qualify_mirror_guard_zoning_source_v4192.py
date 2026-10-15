"""One controller dispatch change; all original game, bosses and ending code unchanged."""
import hashlib,json,re,subprocess
from pathlib import Path
import qualify_guard_uppercut_ready_source_v4148 as previous

ROOT,need,sha=previous.ROOT,previous.need,previous.sha
OUT=ROOT/'audit_v4193_mirror_guard_zoning_source_preflight'

def source_boundary():
    base=previous.source_boundary()
    old=(ROOT/'mk2ks_guard_uppercut_ready_campaign_ram_v4144.lua').read_text()
    before="   elseif strategy=='guard_punish' and (other.roster==5 or other.roster==10 or other.roster==18) then"
    after="   elseif strategy=='guard_punish' and other.roster==18 then"
    need(old.count(before)==1 and old.replace(before,after,1)==(ROOT/'mk2ks_mirror_guard_zoning_campaign_ram_v4186.lua').read_text(),'Exactly one physical controller dispatch edit; mirror input algorithm unchanged, other roster uses original zoning')
    wrapper=(ROOT/'mk2ks_mirror_guard_zoning_campaign_ram_v4186.lua').read_text()
    expanded=(ROOT/'mk2ks_natural_campaign_shao_ring_retreat_v3485.lua').read_text()
    literal=r'"(?:[^"\\]|\\.)*"'
    pairs=re.findall(r'once\(('+literal+r'),\s*('+literal+r')\)',wrapper)
    need(len(pairs)==3,'All original explicit controller edits')
    for a,b in pairs:
        a,b=json.loads(a),json.loads(b);need(expanded.count(a)==1,'Unique original controller transformation');expanded=expanded.replace(a,b,1)
    label=json.loads(re.search(r'local original=('+literal+')',wrapper)[1])
    block=re.search(r'local replacement=\[\[\n(.*?)\]\]',wrapper,re.S)[1]
    need(expanded.count(label)==1,'Unique actual mirror-only block');expanded=expanded.replace(label,block,1)
    sink=json.loads(re.search(r'local guest_sink=('+literal+')',wrapper)[1]);need(expanded.count(sink)==1,'Actual whole guest sink')
    expanded=expanded.replace(sink,'_campaign_guest(raw)',1);need(expanded.count('screen:snapshot(')==6,'Actual six native media sinks');expanded=expanded.replace('screen:snapshot(','_campaign_emit(')
    base['baselineWrapperSHA256']=base.pop('wrapperSHA256');base['baselineExpandedControllerSHA256']=base.pop('expandedControllerSHA256')
    base.update(wrapperSHA256=sha(ROOT/'mk2ks_mirror_guard_zoning_campaign_ram_v4186.lua'),expandedControllerSHA256=hashlib.sha256(expanded.encode()).hexdigest().upper())
    original=(ROOT/'mk2ks_natural_campaign_shao_ring_retreat_v3485.lua').read_text()
    need("if projectile_start and frame-projectile_start<64 then" in original and "elseif gap<80 then" in original and "elseif strategy=='zoning' then" in original,'Original physical projectile/back-jump policy retained, not new game/AI assistance')
    observed=json.loads((ROOT/'audit_v3852_mileena_fixed_sonya_campaign_observed/report.json').read_text())
    meta=json.loads((ROOT/'audit_v3851_mileena_fixed_sonya_p2_campaign/result.json').read_text())
    need(observed['passed'] and not observed['independentCampaignAcceptance'] and meta['exit_code']==0 and meta['boot_frame']==600 and meta['strategy']=='zoning' and meta['candidate']=='diagnostic_v3836_native_mileena_rom_identity' and observed['observations'][0]['stages']==list(range(13)),'Previous same3836 physical zoning observed stage12; this is not whole-campaign acceptance or predicted success')
    base.update(singleDispatchEdit=True,mirrorGuardPhysicalAlgorithmUnchanged=True,originalOtherRosterZoningRestored=True,originalBossAndOwnEndingControllerRetained=True,gameSourceOrPlayableChanges=0,fullPortAcceptance=False)
    return base

if __name__=='__main__':
    need(not OUT.exists(),'Fresh immutable preflight');report=source_boundary()
    paths=(Path(__file__),Path(previous.__file__),ROOT/'mk2ks_mirror_guard_zoning_campaign_ram_v4186.lua',ROOT/'tools/run_mirror_guard_zoning_campaign_ram_v4187.py',ROOT/'mk2ks_guard_uppercut_ready_campaign_ram_v4144.lua',ROOT/'mk2ks_natural_campaign_shao_ring_retreat_v3485.lua',ROOT/'mk2ks_mileena_campaign_ram_v3849.lua',ROOT/'mk2ks_guarded_campaign_finite_ram_v3766.lua',ROOT/'tools/run_mileena_fixed_sonya_campaign_v3850.py',ROOT/'audit_v3851_mileena_fixed_sonya_p2_campaign/result.json',ROOT/'audit_v3852_mileena_fixed_sonya_campaign_observed/report.json',ROOT/'audit_v4167_cpu_busy_attack_windows/report.json',ROOT/'audit_v4185_current_sonya_p2_block_release_uppercut_transition_checked/report.json')
    report.update(passed=True,inputHashes={str(p.resolve()):sha(p) for p in paths},campaignClearAccepted=False,runtimeSyntaxProven=False,scope=__doc__)
    OUT.mkdir();need(subprocess.run(['compact.exe','/C','/I','/Q','/S:'+str(OUT)],capture_output=True).returncode==0,'Compression before preflight writes')
    (OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k!='inputHashes'},indent=2),flush=True)
