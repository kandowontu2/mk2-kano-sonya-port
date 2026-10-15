"""Only physical Mileena inputs and read-only action/handler observations change."""
import hashlib,json,re,subprocess
from pathlib import Path
import qualify_mirror_guard_zoning_source_v4192 as previous
ROOT,need,sha=previous.ROOT,previous.need,previous.sha
OUT=ROOT/'audit_v4248_mileena_duck_pressure_source_preflight'

def source_boundary():
    base=previous.source_boundary()
    base['previousMirrorPolicySingleDispatchEdit']=base.pop('singleDispatchEdit')
    base['previousMirrorPolicyOriginalOtherRosterZoningRestored']=base.pop('originalOtherRosterZoningRestored')
    old=(ROOT/'mk2ks_mirror_guard_zoning_campaign_ram_v4186.lua').read_text()
    wrapper=(ROOT/'mk2ks_mileena_duck_pressure_campaign_ram_v4241.lua').read_text()
    first=wrapper.index("   elseif strategy=='guard_punish' and other.roster==5 then\n")
    last=wrapper.index("   elseif strategy=='guard_punish' and other.roster==18 then\n",first)
    block=wrapper[first:last];rest=wrapper[:first]+wrapper[last:]
    changes={
      'local gp_action_taps={}")':'local gp_action_taps={}\\nlocal du_last,du_down=nil,nil\\nlocal du_taps={}")',
      '::guard_punish_inputs_and_RAM_sinks':'::mileena_duck_pressure_inputs_and_RAM_sinks',
      "assert(limit==5900,'Finite host-only observation; no victory supplied')":"assert(limit==1500,'Finite host-only observation; no victory supplied')",
    }
    for before,after in changes.items():
        need(old.count(before)==1,'Unique physical-state/host-budget/trace-label edit');old=old.replace(before,after)
    need(old==rest,'Whole original selection/schedule/health/mirror guard/other-roster zoning/boss/ending/attract code preserved')
    need(not re.search(r':write_|\.value\s*=(?!=)|load_?state|set_pc|set_state|return\s+data',block),'No guest/register/state/load/health/AI/RNG/difficulty/cadence intervention')
    need("local age=(frame-du_down)%30"in block and "if age>=6 and age<9"in block and "press('High Punch')"in block and "press('Down')"in block and "press('Block')"not in block,'Ordinary Down preparation and3field HP6..8 edges; no rejected block-release shortcut')
    need('other.action=='not in block and 'cpu_action=%d'in block,'CPU action categories merely observed, not declared safe')
    need('p:install_write_tap(observed_main+0x1f0' in block and 'p:install_read_tap(0xff870dc0,0xff870dcf' in block and 'DUCK_ACTION'in block and 'DUCK_HANDLER'in block,'Both actual native main action stores and true HUMAN uppercut fetches observed')
    expanded=(ROOT/'mk2ks_natural_campaign_shao_ring_retreat_v3485.lua').read_text();literal=r'"(?:[^"\\]|\\.)*"'
    pairs=re.findall(r'once\(('+literal+r'),\s*('+literal+r')\)',wrapper);need(len(pairs)==3,'Three original explicit prefix edits')
    for a,b in pairs:
        a,b=json.loads(a),json.loads(b);need(expanded.count(a)==1,'Unique expanded native physical-controller boundary');expanded=expanded.replace(a,b,1)
    label=json.loads(re.search(r'local original=('+literal+')',wrapper)[1]);replacement=re.search(r'local replacement=\[\[\n(.*?)\]\]',wrapper,re.S)[1]
    need(expanded.count(label)==1,'Unique actual Mileena/mirror branch');expanded=expanded.replace(label,replacement,1)
    sink=json.loads(re.search(r'local guest_sink=('+literal+')',wrapper)[1]);need(expanded.count(sink)==1,'Actual original whole guest sink');expanded=expanded.replace(sink,'_campaign_guest(raw)',1)
    need(expanded.count('screen:snapshot(')==6,'All six native RGB sinks transported in RAM');expanded=expanded.replace('screen:snapshot(','_campaign_emit(')
    base.update(previousWrapperSHA256=base['wrapperSHA256'],previousExpandedControllerSHA256=base['expandedControllerSHA256'],
      wrapperSHA256=sha(ROOT/'mk2ks_mileena_duck_pressure_campaign_ram_v4241.lua'),expandedControllerSHA256=hashlib.sha256(expanded.encode()).hexdigest().upper(),
      actualOnlyMileenaPhysicalPolicyChanged=True,mirrorGuardAlgorithmUnchanged=True,otherRosterOriginalZoningUnchanged=True,
      originalBossOwnEndingAndAttractCodeUnchanged=True,hostOnlyObservationSeconds=1500,runtimeSyntaxProven=False,
      actualMoveAttemptsNeverAssumedActivations=True,campaignClearAccepted=False,gameSourceOrPlayableChanges=0,fullPortAcceptance=False)
    return base

if __name__=='__main__':
    need(not OUT.exists(),'Fresh immutable physical preflight');r=source_boundary()
    paths=(Path(__file__),Path(previous.__file__),ROOT/'mk2ks_mileena_duck_pressure_campaign_ram_v4241.lua',ROOT/'tools/run_mileena_duck_pressure_campaign_v4243.py',ROOT/'mk2ks_mirror_guard_zoning_campaign_ram_v4186.lua',ROOT/'mk2ks_natural_campaign_shao_ring_retreat_v3485.lua',ROOT/'audit_v4197_mirror_guard_zoning_whole_campaign_checked/report.json',ROOT/'audit_v4157_current_sonya_p2_clean_uppercut_checked/report.json',ROOT/'audit_v4167_cpu_busy_attack_windows/report.json')
    r.update(passed=True,inputHashes={str(p.resolve()):sha(p)for p in paths},scope=__doc__)
    OUT.mkdir();need(subprocess.run(['compact.exe','/C','/I','/Q','/S:'+str(OUT)],capture_output=True).returncode==0,'Preflight compressed before writes')
    (OUT/'report.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps({k:v for k,v in r.items()if k!='inputHashes'},indent=2),flush=True)
