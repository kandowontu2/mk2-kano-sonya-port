"""Two CPU-owned voices progress independently, retain owner until both EOF."""
import copy,json,wave
import check_campaign_stage_chronology as chronology
import verify_native_source_sync as sync
sync.verify()
folder=sync.ROOT/'audit_current_cpu_sonya_bicycle_audio_runtime'
out=sync.ROOT/'audit_current_cpu_sonya_bicycle_audio_checked'
assert not out.exists()
terminal=json.loads((folder/'terminal.json').read_text(encoding='utf-8-sig'))
assert terminal['exitCode']==0 and terminal['limitReason'] is None
assert not (folder/'stderr.log').read_text().strip()
rows=chronology.load(folder/'run.log')
old=chronology.load(sync.ROOT/'audit_current_sonya_p2_native_start_runtime/run.log')
excluded={'CPU_BICYCLE_CUE','CPU_BICYCLE_OWNER','CPU_BICYCLE_CHANNEL','HOST_BOUND','RESULT','INPUT_DIGEST_FINAL'}
for tag in set(rows)|set(old):
    if tag in excluded:continue
    assert [r for r in rows.get(tag,[]) if int(r['frame'])<4000]==[r for r in old.get(tag,[]) if int(r['frame'])<4000],tag
clips={10:sync.ROOT/'samples/mk2ks/sonya_bicycle_launch.wav',11:sync.ROOT/'samples/mk2ks/sonya_bicycle_cry.wav'}
lengths={}
for channel,path in clips.items():
    with wave.open(str(path)) as wav:lengths[channel]=wav.getnframes()
assert lengths=={10:40720,11:66523}
def gate(records):
    cues=records['CPU_BICYCLE_CUE'];assert len(cues)==2 and [r['cue'] for r in cues]==['6B01','6B02']
    cue=cues[0]
    assert all(r['id']=='18' and r['action']=='516' and r['frame']==cue['frame'] and r['actor']==cue['actor'] and r['main']==cue['main'] for r in cues)
    owners=records['CPU_BICYCLE_OWNER'];channels=records['CPU_BICYCLE_CHANNEL']
    for owner in owners:
        assert owner['guest_id']=='18' and owner['guest_actor']==cue['actor'] and owner['guest_main']==cue['main']
        if owner['actor']!='00000000':assert owner['actor']==cue['actor'] and owner['main']==cue['main'] and owner['id']=='18'
    for n in (10,11):
        active=[r for r in channels if r['channel']==str(n) and int(r['age'])<=3]
        assert len(active)==4 and all(int(r['length'])==lengths[n] and r['paused']==r['loop']=='0' for r in active)
        assert all(float(b['pos'])>float(a['pos']) for a,b in zip(active,active[1:]))
    late=next(r for r in owners if r['age']=='60');assert late['actor']==cue['actor']
    first=next(r for r in channels if r['age']=='60' and r['channel']=='10')
    second=next(r for r in channels if r['age']=='60' and r['channel']=='11')
    assert float(first['pos'])==lengths[10] and 0<float(second['pos'])<lengths[11]
    eof=next(r for r in owners if r['actor']=='00000000')
    assert eof['main']=='00000000' and eof['id']=='0' and eof['stored_health']=='0' and eof['guest_hp']==cue['health']
    assert all(float(r['pos'])==lengths[int(r['channel'])] for r in channels if r['age']==eof['age'])
    return dict(cues=cues,ownerRetainedAfterFirstEOF=late,finalEOF=eof)
proof=gate(rows)
bad=copy.deepcopy(rows);next(r for r in bad['CPU_BICYCLE_CHANNEL'] if r['channel']=='11' and r['age']=='1')['pos']='0'
try:gate(bad)
except AssertionError:pass
else:raise AssertionError('Stopped second voice accepted')
out.mkdir();report=dict(naturalCpuBicycleVoicePassed=True,priorPhysicalInputsUnchanged=True,
    proof=proof,clipLengths=lengths,stoppedCryFaultRejected=True,
    terminal=terminal,logSHA256=sync.sha(folder/'run.log'),clipSHA256={n:sync.sha(path) for n,path in clips.items()},
    heardMixAccepted=False,allCpuAudioContextsAccepted=False,fullPortAccepted=False)
(out/'report.json').write_text(json.dumps(report,indent=2));print(json.dumps(dict(passed=True,launch=proof['cues'][0]['frame'],bothEOF=proof['finalEOF']['age'])))
