"""Only extend normal physical controls to real roster10; preserve native morph rules."""
import hashlib,json,re,subprocess
from pathlib import Path
import qualify_mileena_jump_retry_source_v4281 as previous
ROOT,need,sha=previous.ROOT,previous.need,previous.sha
LUA='mk2ks_shang_jump_retry_campaign_ram_v4300.lua'
OUT=ROOT/'audit_v4302_shang_jump_retry_source_preflight'

def source_boundary():
    base=previous.source_boundary()
    old=(ROOT/previous.LUA).read_text()
    changes={
      "   elseif strategy=='guard_punish' and other.roster==5 then":
      "   elseif strategy=='guard_punish' and (other.roster==5 or other.roster==10) then",
      "       if not own or not target or not actor or own.id~=18 or own.roster~=18 or target.id~=5 or target.roster~=5 or":
      "       if not own or not target or not actor or own.id~=18 or own.roster~=18 or\n        (target.roster~=5 and target.roster~=10) or (target.roster==5 and target.id~=5) or",
      '::mileena_jump_retry_inputs_and_RAM_sinks':'::shang_jump_retry_inputs_and_RAM_sinks',
    }
    for a,b in changes.items():
        need(old.count(a)==1,'Unique controller dispatch/observer label boundary')
        old=old.replace(a,b,1)
    wrapper=(ROOT/LUA).read_text()
    need(wrapper==old,'Only physical dispatch and read-only observer coverage extended; every other byte preserved')
    expanded=(ROOT/'mk2ks_natural_campaign_shao_ring_retreat_v3485.lua').read_text()
    literal=r'"(?:[^"\\]|\\.)*"'
    pairs=re.findall(r'once\(('+literal+r'),\s*('+literal+r')\)',wrapper)
    need(len(pairs)==3,'All original prefix transformations retained')
    for a,b in pairs:
        a,b=json.loads(a),json.loads(b)
        need(expanded.count(a)==1,'Unique original source prefix')
        expanded=expanded.replace(a,b,1)
    original=json.loads(re.search(r'local original=('+literal+')',wrapper)[1])
    replacement=re.search(r'local replacement=\[\[\n(.*?)\]\]',wrapper,re.S)[1]
    need(expanded.count(original)==1,'Original non-boss dispatch boundary')
    need(not re.search(r':write_|\.value\s*=(?!=)|load_?state|set_pc|set_state|return\s+data',replacement),
         'No guest/AI/roster/morph/health/difficulty/RNG/position overrides')
    expanded=expanded.replace(original,replacement,1)
    sink=json.loads(re.search(r'local guest_sink=('+literal+')',wrapper)[1])
    need(expanded.count(sink)==1,'One whole RAM guest sink')
    expanded=expanded.replace(sink,'_campaign_guest(raw)',1)
    need(expanded.count('screen:snapshot(')==6,'All original raster sinks retained in RAM')
    expanded=expanded.replace('screen:snapshot(','_campaign_emit(')
    return dict(passed=True,wrapperSHA256=sha(ROOT/LUA),
      expandedControllerSHA256=hashlib.sha256(expanded.encode()).hexdigest().upper(),
      previousControllerSHA256=base['expandedControllerSHA256'],
      nativeMorphRulesUnchanged=True,originalSelectionMirrorOtherOpponentsBossesEndingsAttractUnchanged=True,
      actualMoveAttemptsNeverAssumedActivations=True,nativeObserverRoleReuseRuntimeProven=False,
      fullPortAcceptance=False)

if __name__=='__main__':
    need(not OUT.exists(),'Fresh source preflight before first boot')
    r=source_boundary()
    paths=(Path(__file__).resolve(),Path(previous.__file__).resolve(),ROOT/LUA,ROOT/previous.LUA,
      ROOT/'tools/run_shang_jump_retry_campaign_v4303.py')
    r['inputHashes']={str(p):sha(p) for p in paths}
    OUT.mkdir()
    need(subprocess.run(['compact.exe','/C','/I','/Q','/S:'+str(OUT)],capture_output=True).returncode==0,'Compress before writing')
    (OUT/'report.json').write_text(json.dumps(r,indent=2)+'\n')
    print(json.dumps({k:v for k,v in r.items() if k!='inputHashes'},indent=2),flush=True)
