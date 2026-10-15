"""Retry physical ignored jumps; original full campaign and repaired observers retained."""
import hashlib,json,re,subprocess
from pathlib import Path
import qualify_mileena_ring_spacing_source_v4261 as previous
import verify_mileena_observer_slot_reuse_source_v4276 as repair
ROOT,need,sha=previous.ROOT,previous.need,previous.sha
OUT=ROOT/'audit_v4282_mileena_jump_retry_source_preflight'
LUA='mk2ks_mileena_jump_retry_campaign_ram_v4280.lua'

def source_boundary():
    base=previous.source_boundary()
    old=(ROOT/'mk2ks_mileena_ring_spacing_campaign_ram_v4275.lua').read_text()
    repair.source_check(old)
    wrapper=(ROOT/LUA).read_text()
    changes={
      '    if rs_ring and frame-rs_ring<64 then':
      '    -- Preserve every D,F,LP edge, then permit an earlier physical retreat.\n    -- Failed Up attempts do not impose a40-field cooldown: retry3on/1off\n    -- while actually grounded; only native height admits the air-kick branch.\n    if rs_ring and frame-rs_ring<64 and (frame-rs_ring<12 or gap>=150) then',
      "     if frame-rs_jump>=40 then\n      reason='back_jump_attempt';rs_jump=frame;rs_jumpdir=back;press('Up');press(back)\n     elseif frame-rs_jump<4 then reason='back_jump_edge';press('Up');press(rs_jumpdir)\n     else reason='grounded_guard';press('Down');press('Block')end":
      "     if frame-rs_jump>=4 then rs_jump=frame;rs_jumpdir=back end\n     if frame-rs_jump<3 then reason='grounded_jump_retry_edge';press('Up');press(rs_jumpdir)\n     else reason='grounded_jump_retry_release';press(rs_jumpdir)end",
      '::mileena_ring_spacing_inputs_and_RAM_sinks':'::mileena_jump_retry_inputs_and_RAM_sinks',
    }
    for before,after in changes.items():
        need(old.count(before)==1,'Unique declared physical retry/retreat change');old=old.replace(before,after)
    need(old==wrapper,'Exact2physicalchanges andtrace label only; all selection/mirror/other opponent/boss/ending/attract and repaired observers unchanged')
    first=wrapper.index("   elseif strategy=='guard_punish' and other.roster==5 then\n")
    last=wrapper.index("   elseif strategy=='guard_punish' and other.roster==18 then\n",first)
    block=wrapper[first:last]
    need(not re.search(r':write_|\.value\s*=(?!=)|load_?state|set_pc|set_state|return\s+data',block),
         'No guest/state/AI/health/RNG/difficulty/position writes')
    need('other.action=='not in block and "elseif human.floor-human.y>8 then" in block and
         "frame-rs_ring<12 or gap>=150" in block and "frame-rs_jump>=4" in block and
         "frame-rs_jump<3" in block and "local observed_key=tostring(n)..':'..tostring(observed_main)" in block,
         'Actual-height air branch, complete Ring edges,3on1off retry, slot/Main observer binding')
    expanded=(ROOT/'mk2ks_natural_campaign_shao_ring_retreat_v3485.lua').read_text()
    literal=r'"(?:[^"\\]|\\.)*"';pairs=re.findall(r'once\(('+literal+r'),\s*('+literal+r')\)',wrapper)
    need(len(pairs)==3,'All original prefix transformations retained')
    for a,b in pairs:
        a,b=json.loads(a),json.loads(b);need(expanded.count(a)==1,'Unique prefix edit');expanded=expanded.replace(a,b,1)
    label=json.loads(re.search(r'local original=('+literal+')',wrapper)[1]);replacement=re.search(r'local replacement=\[\[\n(.*?)\]\]',wrapper,re.S)[1]
    need(expanded.count(label)==1,'One exact dispatch block');expanded=expanded.replace(label,replacement,1)
    sink=json.loads(re.search(r'local guest_sink=('+literal+')',wrapper)[1]);need(expanded.count(sink)==1,'Original whole guest sink')
    expanded=expanded.replace(sink,'_campaign_guest(raw)',1);need(expanded.count('screen:snapshot(')==6,'Every original RGB sink remains in RAM')
    expanded=expanded.replace('screen:snapshot(','_campaign_emit(')
    base.update(previousSpacingWrapperSHA256=base['wrapperSHA256'],previousSpacingExpandedControllerSHA256=base['expandedControllerSHA256'],
      wrapperSHA256=sha(ROOT/LUA),expandedControllerSHA256=hashlib.sha256(expanded.encode()).hexdigest().upper(),
      physicalCompleteRingCommandRetained=True,physicalGroundedJumpRetry3On1Off=True,
      physicalAttemptCooldownNotAssumedActualJump=True,observerKeyActualSlotAndMain=True,
      runtimeSyntaxProven=False,nativeObserverRepairRuntimeProven=False,
      actualMoveAttemptsNeverAssumedActivations=True,campaignClearAccepted=False,fullPortAcceptance=False)
    return base

if __name__=='__main__':
    need(not OUT.exists(),'Fresh immutable preflight');r=source_boundary()
    paths=(Path(__file__),Path(previous.__file__),Path(repair.__file__),ROOT/LUA,
      ROOT/'tools/run_mileena_jump_retry_campaign_v4283.py',ROOT/'mk2ks_mileena_ring_spacing_campaign_ram_v4275.lua',
      ROOT/'audit_v4277_mileena_observer_slot_reuse_source_checked/report.json',
      ROOT/'audit_v4274_mileena_ring_spacing_throw_windows_observed/report.json')
    r.update(passed=True,inputHashes={str(p.resolve()):sha(p) for p in paths},scope=__doc__)
    OUT.mkdir();need(subprocess.run(['compact.exe','/C','/I','/Q','/S:'+str(OUT)],capture_output=True).returncode==0,'Compress before writes')
    (OUT/'report.json').write_text(json.dumps(r,indent=2)+'\n')
    print(json.dumps({k:v for k,v in r.items() if k!='inputHashes'},indent=2),flush=True)
