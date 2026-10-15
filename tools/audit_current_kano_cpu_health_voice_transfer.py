"""Compose finite runtime receipts with exact shared watcher source, no emulator."""
import json
import verify_native_source_sync as sync
sync.verify();R=sync.ROOT
out=R/'audit_current_kano_cpu_health_voice_transfer_checked';assert not out.exists()
paths=['audit_current_cpu_kano_ball_audio_checked/report.json','audit_current_cpu_sonya_voice_earlier_upper_checked/report.json','audit_current_battle_audio_hit_cleanup_checked/report.json']
d=[json.loads((R/p).read_text()) for p in paths]
assert d[0]['naturalCpuBallVoicePassed'] and d[1]['actualCpuActiveVoiceHealthInterruptionAccepted'] and d[2]['passed']
balls=[x for x in d[2]['cases'] if x['move']=='ball'];assert {x['side'] for x in balls}=={1,2}
source=R/'mame-mkp/src/mame/midway/midtunit_m.cpp';s=source.read_text()
start=s.index('TIMER_CALLBACK_MEMBER(midtunit_state::mk2ks_battle_audio_tick)')
block=s[start:s.index('\nvoid ',start)]
assert 'for (unsigned slot = 0; slot < 2; slot++)' in block
assert 'space.read_word(health[slot]) != m_mk2ks_battle_health[slot]' in block
assert 'mk2ks_battle_audio_stop(slot, "health_changed")' in block
assert 'states' not in block and 'state[slot]' not in block
stop=s[s.index('void midtunit_state::mk2ks_battle_audio_stop'):start]
assert 'stop(10 + slot * 2)' in stop and 'stop(11 + slot * 2)' in stop
out.mkdir();report=dict(sharedWatcherComponentTransferSupported=True,directCurrentCPU17ActiveHitRuntimeAccepted=False,
 sourceBasis='Watcher selects physical slot actor/Main/HP, savedid/mode; does not branch on CPUstate vs humanstate or character-specific health condition. Same stop channels10+slot*2/11+slot*2. CurrentCPU17 launch proves correct slot2 id17 marker/Main/channel12; currentCPU18 native activehit proves shared health-change branch; accepted humanKano ball activehit proof covers both physical slots.',
 currentCPU17Launch=d[0]['proof'],currentCPU18ActiveHit=d[1]['proof'],humanKanoBothSlotHitCleanup=balls,
 scope='Legitimate source-component transfer, not a newly observed CPU17 contact or full heard waveform. No distinct CPU17 health-stop branch found; do not invent a source defect from missing duplicate contact.',
 nextAction='Prefer uncovered gameplay/finisher/arena integration contexts. If directCPU17 contact required as extra runtime coverage, use a new finite physical counter; do not repeat unchanged baseline or make it a component acceptance prerequisite.',
 heardMixAccepted=False,allCPUContextsAccepted=False,fullPortAccepted=False,inputHashes={p:sync.sha(R/p) for p in paths},currentSourceSHA256=sync.sha(source),sharedWatcherSource=block)
(out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(dict(report=str(out/'report.json'),componentTransferSupported=True,directCPU17Hit=False)))
