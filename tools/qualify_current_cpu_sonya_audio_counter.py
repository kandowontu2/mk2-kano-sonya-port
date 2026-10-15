"""Record failed contact attempt explicitly; cannot pass damage interruption."""
import json
import check_campaign_stage_chronology as chronology
import verify_native_source_sync as sync
sync.verify()
folder=sync.ROOT/'audit_current_cpu_sonya_audio_counter_runtime'
out=sync.ROOT/'audit_current_cpu_sonya_audio_counter_checked'
assert not out.exists()
terminal=json.loads((folder/'terminal.json').read_text(encoding='utf-8-sig'))
assert terminal['exitCode']==0 and terminal['limitReason'] is None
assert not (folder/'stderr.log').read_text().strip()
rows=chronology.load(folder/'run.log')
old=chronology.load(sync.ROOT/'audit_current_cpu_sonya_bicycle_audio_runtime/run.log')
for tag in set(rows)|set(old):
    if tag=='CPU_AUDIO_COUNTER_INPUT':continue
    assert [r for r in rows.get(tag,[]) if int(r['frame'])<1690]==[r for r in old.get(tag,[]) if int(r['frame'])<1690],tag
inputs=rows['CPU_AUDIO_COUNTER_INPUT'];assert [int(r['age']) for r in inputs]==list(range(60))
assert all(r['down']=='1' and int(r['block'])==int(int(r['age'])<12) and int(r['hp'])==int(12<=int(r['age'])<24 and int(r['age'])%6<3) for r in inputs)
owners=rows['CPU_BICYCLE_OWNER'];eof=next(r for r in owners if r['actor']=='00000000')
assert eof['age']=='76' and all(r['guest_hp']=='161' for r in owners)
hits=[r for r in rows['HEALTH'] if r['slot']=='1' and 1689<=int(r['frame'])<=1765 and r['pc']=='FF836700' and int(r['after'])<int(r['before'])<=161]
assert not hits
uppers=[r for r in rows['LIVE'] if r['actions'].split(',')[0]=='263' and 1690<=int(r['frame'])<1750]
assert uppers and all(r['human']=='18:18' for r in uppers)
out.mkdir();report=dict(finiteObservationPassed=True,damageInterruptionProven=False,
    attemptedCounterOutcome='Native uppercut activated but no CPU damage before both voice clips reached EOF.',
    physicalCounterFields=60,firstObservedUppercut=uppers[0],cpuVoiceEOF=eof,
    damageContacts=hits,terminal=terminal,logSHA256=sync.sha(folder/'run.log'),fullPortAccepted=False)
(out/'report.json').write_text(json.dumps(report,indent=2));print(json.dumps(dict(observationPassed=True,damageInterruptionProven=False,uppercut=uppers[0]['frame'],eof=eof['frame'])))
