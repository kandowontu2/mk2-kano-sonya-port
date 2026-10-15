"""Exact Kintaro physical pressure guard/release, all native grammar retained."""
import hashlib,json,re,subprocess
from pathlib import Path
import qualify_shang_jump_retry_source_v4301 as previous
ROOT,need,sha=previous.ROOT,previous.need,previous.sha
LUA='mk2ks_kintaro_pressure_guard_campaign_ram_v4424.lua'
OUT=ROOT/'audit_v4426_kintaro_pressure_guard_source_preflight'
ADDED=r'''-- Physical Kintaro pressure defense only. Keep descending kicks/stomp HP.
-- Native block actions may attempt a jump after ordinary Block release;
-- no readiness label supplies an activation or writes any character state.
once("if can_crouch and frame-boss_walk_last_x>=12 and gap<jump_gap and cpu_height<20 and frame-boss_last_jump>=60 then",
 "if (can_crouch or(height==0 and human.flags&0x0c==0 and human.body&0x0c==0 and (human.action==0x700 or human.action==0x701))) and frame-boss_walk_last_x>=12 and gap<jump_gap and cpu_height<20 and frame-boss_last_jump>=60 then")
once("else press('Down')end\n    else\n     boss_walk_last_x=nil;press('Down');press('Block')\n    end\n   -- END actual-input boss clean-uppercut response v2332.",
 "else press('Down');press('Block')end\n    else\n     boss_walk_last_x=nil;press('Down');press('Block')\n    end\n   -- END actual-input boss clean-uppercut response v2332.")
'''

def source_boundary():
    base=previous.source_boundary();old=(ROOT/previous.LUA).read_text()
    need(old.count('once(original,replacement)\n')==1,'Unique existing non-boss controls boundary')
    old=old.replace('once(original,replacement)\n','once(original,replacement)\n'+ADDED)
    old=old.replace('::shang_jump_retry_inputs_and_RAM_sinks','::kintaro_pressure_guard_inputs_and_RAM_sinks')
    wrapper=(ROOT/LUA).read_text();need(wrapper==old,'Only two physical guard/release transforms and source label added')
    expanded=(ROOT/'mk2ks_natural_campaign_shao_ring_retreat_v3485.lua').read_text()
    literal=r'"(?:[^"\\]|\\.)*"'
    pairs=re.findall(r'once\(('+literal+r'),\s*('+literal+r')\)',wrapper)
    need(len(pairs)==5,'All three original prefix edits and two declared Kintaro guard/release edits')
    for a,b in pairs:
        a,b=json.loads(a),json.loads(b);need(expanded.count(a)==1,'Unique original transform')
        expanded=expanded.replace(a,b,1)
    original=json.loads(re.search(r'local original=('+literal+')',wrapper)[1])
    replacement=re.search(r'local replacement=\[\[\n(.*?)\]\]',wrapper,re.S)[1]
    need(expanded.count(original)==1,'Original non-boss branch unchanged')
    expanded=expanded.replace(original,replacement,1)
    sink=json.loads(re.search(r'local guest_sink=('+literal+')',wrapper)[1])
    need(expanded.count(sink)==1,'One original native RAM guest sink')
    expanded=expanded.replace(sink,'_campaign_guest(raw)',1)
    need(expanded.count('screen:snapshot(')==6,'All six native media callbacks in RAM')
    expanded=expanded.replace('screen:snapshot(','_campaign_emit(')
    need(not re.search(r':write_|\.value\s*=(?!=)|load_?state|set_pc|set_state|return\s+data',expanded),
         'No guest/identity/AI/health/difficulty/RNG/position overrides')
    return dict(passed=True,wrapperSHA256=sha(ROOT/LUA),
      expandedControllerSHA256=hashlib.sha256(expanded.encode()).hexdigest().upper(),
      priorExpandedControllerSHA256=base['expandedControllerSHA256'],
      physicalKintaroPressureGuardOnly=True,nativeObserversAndStompUppercutTimingRetained=True,
      originalForwardJumpAndDescendingKickRetained=True,
      ordinaryScorpion10AndMileena5PoliciesRetained=True,originalShaoEndingAttractRetained=True,
      actualMoveAttemptsNeverAssumedActivations=True,naturalTowerClearAccepted=False,fullPortAcceptance=False)

if __name__=='__main__':
    need(not OUT.exists(),'Fresh preflight before first native boot');r=source_boundary()
    paths=(Path(__file__).resolve(),Path(previous.__file__).resolve(),ROOT/LUA,ROOT/previous.LUA,
      ROOT/'tools/run_kintaro_pressure_guard_campaign_v4427.py',ROOT/'audit_v4423_sonya_kintaro_ground_damage/report.json')
    r['inputHashes']={str(p):sha(p) for p in paths}
    OUT.mkdir();need(subprocess.run(['compact.exe','/C','/I','/Q','/S:'+str(OUT)],capture_output=True).returncode==0,'Compress before writing')
    (OUT/'report.json').write_text(json.dumps(r,indent=2)+'\n')
    print(json.dumps({k:v for k,v in r.items() if k!='inputHashes'},indent=2),flush=True)
