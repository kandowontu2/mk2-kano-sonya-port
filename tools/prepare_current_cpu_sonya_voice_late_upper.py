"""Finite physical falling-CPU uppercut, no forced contact or audio writes."""
import json,difflib
import verify_native_source_sync as sync
sync.verify()
R=sync.ROOT
out=R/'audit_current_cpu_sonya_voice_late_upper_preparation';assert not out.exists()
base=R/'audit_current_cpu_sonya_bicycle_audio_preparation'
s=(base/'campaign.lua').read_text()
needle="   if (leg_tactic or strategy=='lowkick'or strategy=='throw') and other.roster~=12 and other.roster~=13 then"
assert s.count(needle)==1
policy="""   if frame-first_live<90 then
    local age=frame-first_live
    press('Down')
    if age<12 then press('Block')
    elseif age>=56 and age<62 then press('High Punch')end
    log('CPU_AUDIO_LATE_UPPER_INPUT',string.format('age=%d down=1 block=%d hp=%d',age,age<12 and 1 or 0,age>=56 and age<62 and 1 or 0))
   elseif (leg_tactic or strategy=='lowkick'or strategy=='throw') and other.roster~=12 and other.roster~=13 then"""
s=s.replace(needle,policy)
old=" if signature==audio_signature and age>3 and age~=20 and age~=60 and age~=120 then return end"
assert s.count(old)==1;s=s.replace(old,' -- Every field: distinguish active pre-hit voice from EOF and timed native retirement.')
assert ':write_' not in s and ':snapshot(' not in s
out.mkdir();lua=out/'campaign.lua';lua.write_text(s)
runner=(base/'run.ps1').read_text().replace(base.name+'/campaign.lua',out.name+'/campaign.lua').replace(sync.sha(base/'campaign.lua'),sync.sha(lua)).replace('audit_current_cpu_sonya_bicycle_audio_runtime','audit_current_cpu_sonya_voice_late_upper_runtime')
(out/'run.ps1').write_text(runner)
historical={}
for n in ['audit_v6373_current_cpu_blade_knife_audio_checked','audit_v6387_current_cpu_ring_audio_checked','audit_v6407_current_cpu_ring_mirror_audio_checked','audit_v6429_current_cpu_ring_miss_audio_checked','audit_v6447_current_cpu_compound_audio_checked','audit_v6462_current_cpu_ball_audio_checked','audit_v6671_kano_cpu_launch_audio_checked']:
 d=json.loads((R/n/'report.json').read_text());assert d['passed'];historical[n]={k:v for k,v in d.items() if isinstance(v,(str,int,bool)) and k not in ['thisGoalTurnClassification','previousGoalTurnClassification','preservedExecutedFailure','preservedFailedStartup']}
report=dict(preparedNotRun=True,LuaSHA256=sync.sha(lua),physicalOnly=True,observerEveryField120=True,
 rationale='Prior upper activation1711: CPUx544,y-22 versus human661,81 (gap117,height103) missed. CPU1745 x680,y10 (gap19,height71),1750x700,y73(gap39,height8); lateHP ages56..61 targets actual descending pass before cryEOF1765. New trajectory/contact not assumed.',
 previousCounterDamageInterruptionProven=False,currentChangedAdmission='v5219 battle handling hardcoded18/mode2; current adds17/6B03/action20B, demo1+introguard and actual savedid/mode. Channel/sample/start(false)/60Hz lifetime unchanged.',
 retainedHistoricalFiniteWaveformProofs=historical,retainedSoundClockEqualityReport='audit_current_historical_sonya_ending_scope_v2_checked/report.json',
 requirement='ActualCPUowned18 voice positive position below66523 before native slot1HP FF836700 reduction; sameactor/Main; storedowner cleared by health_changed beforeEOF; continuous native mode2 and both channels stop, not match loss/join substitution.',
 bounded='4000fields;90sec/320MiB/10MiB;no raw media',fullPortAccepted=False,
 sourceDiff=''.join(difflib.unified_diff((base/'campaign.lua').read_text().splitlines(True),s.splitlines(True))),baselineSHA256=sync.sha(base/'campaign.lua'))
(out/'source.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(dict(preparation=str(out),LuaSHA256=sync.sha(lua),preparedNotRun=True)))
