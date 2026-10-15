"""Physical Mileena Ring/back-jump spacing only; original full campaign retained."""
import hashlib,json,re,subprocess
from pathlib import Path
import qualify_mirror_guard_zoning_source_v4192 as original
ROOT,need,sha=original.ROOT,original.need,original.sha
OUT=ROOT/'audit_v4262_mileena_ring_spacing_source_preflight'
LUA='mk2ks_mileena_ring_spacing_campaign_ram_v4259.lua'

def source_boundary():
    base=original.source_boundary()
    base['previousMirrorPolicySingleDispatchEdit']=base.pop('singleDispatchEdit')
    base['previousMirrorPolicyOriginalOtherRosterZoningRestored']=base.pop('originalOtherRosterZoningRestored')
    old=(ROOT/'mk2ks_mirror_guard_zoning_campaign_ram_v4186.lua').read_text()
    wrapper=(ROOT/LUA).read_text()
    first=wrapper.index("   elseif strategy=='guard_punish' and other.roster==5 then\n")
    last=wrapper.index("   elseif strategy=='guard_punish' and other.roster==18 then\n",first)
    block=wrapper[first:last];rest=wrapper[:first]+wrapper[last:]
    edits={
      'local gp_action_taps={}")':'local gp_action_taps={}\\nlocal rs_last,rs_ring,rs_dir,rs_jumpdir=nil,nil,nil,nil\\nlocal rs_jump=-1000\\nlocal rs_taps={}")',
      '::guard_punish_inputs_and_RAM_sinks':'::mileena_ring_spacing_inputs_and_RAM_sinks',
      "assert(limit==5900,'Finite host-only observation; no victory supplied')":"assert(limit==1500,'Finite host-only observation; no victory supplied')",
    }
    for before,after in edits.items():
        need(old.count(before)==1,'Unique declared physical state/label/host limit change');old=old.replace(before,after)
    need(old==rest,'Entire original selection/mirror/other opponents/boss/ending/attract preserved')
    need(not re.search(r':write_|\.value\s*=(?!=)|load_?state|set_pc|set_state|return\s+data',block),'No guest/register/AI/health/RNG/difficulty override')
    need('other.action=='not in block,'No assumption that action303 or507 is safe')
    for part in ("frame-rs_ring<64","age>=2 and age<5","age>=7 and age<10","age>=8 and age<12",
                 "press('Low Punch')","age>=15","elseif gap<150 then","frame-rs_jump>=40",
                 "frame-rs_jump<4","frame-rs_jump<48","frame%6<3","press('High Kick')"):
        need(part in block,'Declared ordinary command/spacing edge '+part)
    need("{'ring',0xffffb400}" in (ROOT/'mk2ks_natural_campaign_shao_ring_retreat_v3485.lua').read_text(),
         'Original native Ring activation observer retained, no planned input credited')
    need("'RANGE_CPU_ACTION'" in block and "'RANGE_ACTION'" in block and
         'cpu.A8.value~=actor.actor' in block and 'cpu.A13.value~=actor.main' in block and
         'data&0xffff' in block and 'mask~=0xffff' in block,'Actual native action stores are read-only and owner-bound')
    expanded=(ROOT/'mk2ks_natural_campaign_shao_ring_retreat_v3485.lua').read_text()
    literal=r'"(?:[^"\\]|\\.)*"';pairs=re.findall(r'once\(('+literal+r'),\s*('+literal+r')\)',wrapper)
    need(len(pairs)==3,'Every original explicit prefix edit retained')
    for a,b in pairs:
        a,b=json.loads(a),json.loads(b);need(expanded.count(a)==1,'Unique controller prefix');expanded=expanded.replace(a,b,1)
    label=json.loads(re.search(r'local original=('+literal+')',wrapper)[1])
    replacement=re.search(r'local replacement=\[\[\n(.*?)\]\]',wrapper,re.S)[1]
    need(expanded.count(label)==1,'One physical dispatch block');expanded=expanded.replace(label,replacement,1)
    sink=json.loads(re.search(r'local guest_sink=('+literal+')',wrapper)[1])
    need(expanded.count(sink)==1,'One actual whole guest read');expanded=expanded.replace(sink,'_campaign_guest(raw)',1)
    need(expanded.count('screen:snapshot(')==6,'Every original RGB sink retained in RAM');expanded=expanded.replace('screen:snapshot(','_campaign_emit(')
    base.update(previousWrapperSHA256=base['wrapperSHA256'],previousExpandedControllerSHA256=base['expandedControllerSHA256'],
      wrapperSHA256=sha(ROOT/LUA),expandedControllerSHA256=hashlib.sha256(expanded.encode()).hexdigest().upper(),
      actualOnlyMileenaPhysicalPolicyChanged=True,mirrorGuardAlgorithmUnchanged=True,otherRosterOriginalZoningUnchanged=True,
      originalBossOwnEndingAndAttractCodeUnchanged=True,hostOnlyObservationSeconds=1500,
      runtimeSyntaxProven=False,actualMoveAttemptsNeverAssumedActivations=True,
      campaignClearAccepted=False,gameSourceOrPlayableChanges=0,fullPortAcceptance=False)
    return base

if __name__=='__main__':
    need(not OUT.exists(),'Fresh immutable source preflight');r=source_boundary()
    paths=(Path(__file__),Path(original.__file__),ROOT/LUA,ROOT/'tools/run_mileena_ring_spacing_campaign_v4260.py',
      ROOT/'mk2ks_mirror_guard_zoning_campaign_ram_v4186.lua',ROOT/'mk2ks_natural_campaign_shao_ring_retreat_v3485.lua',
      ROOT/'audit_v4256_mileena_native_throw_interruptions_checked/report.json')
    r.update(passed=True,inputHashes={str(p.resolve()):sha(p) for p in paths},scope=__doc__)
    OUT.mkdir();need(subprocess.run(['compact.exe','/C','/I','/Q','/S:'+str(OUT)],capture_output=True).returncode==0,'Compress before writing')
    (OUT/'report.json').write_text(json.dumps(r,indent=2)+'\n')
    print(json.dumps({k:v for k,v in r.items() if k!='inputHashes'},indent=2),flush=True)
