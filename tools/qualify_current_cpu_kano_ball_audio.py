"""Natural CPU-owned launch progression/EOF; no heard-mix acceptance."""
import copy,json,wave
import check_campaign_stage_chronology as chronology
import verify_native_source_sync as sync
sync.verify()
folder=sync.ROOT/'audit_current_cpu_kano_ball_audio_runtime'
out=sync.ROOT/'audit_current_cpu_kano_ball_audio_checked'
assert not out.exists()
terminal=json.loads((folder/'terminal.json').read_text(encoding='utf-8-sig'))
assert terminal['exitCode']==0 and terminal['limitReason'] is None
assert not (folder/'stderr.log').read_text().strip()
rows=chronology.load(folder/'run.log')
old=chronology.load(sync.ROOT/'audit_bounded_compact_kano_campaign_p1_runtime/run.log')
excluded={'CPU_BALL_CUE','CPU_BALL_OWNER','CPU_BALL_CHANNEL','HOST_BOUND','RESULT','INPUT_DIGEST_FINAL'}
for tag in set(rows)|set(old):
    if tag in excluded:continue
    assert [r for r in rows.get(tag,[]) if int(r['frame'])<4000]==[r for r in old.get(tag,[]) if int(r['frame'])<4000],tag
clip=sync.BUILD/'samples/mk2ks/kano_ball_launch.wav'
with wave.open(str(clip)) as wav:length=wav.getnframes()
assert length==55465
def gate(records):
    cues=records['CPU_BALL_CUE'];assert len(cues)==1
    cue=cues[0];assert cue['id']=='17' and cue['action']=='523' and cue['cue']=='6B03'
    owners=records['CPU_BALL_OWNER'];channels=records['CPU_BALL_CHANNEL']
    for owner in owners:
        assert owner['guest_id']=='17' and owner['guest_actor']==cue['actor'] and owner['guest_main']==cue['main']
        if owner['actor']!='00000000':
            assert owner['actor']==cue['actor'] and owner['main']==cue['main'] and owner['id']=='17'
    active=[r for r in channels if r['channel']=='12' and int(r['age'])<=3]
    assert len(active)==4 and all(int(r['length'])==length and r['paused']==r['loop']=='0' for r in active)
    assert all(int(r['sample']) in (16,4294967295) for r in active)
    assert all(float(b['pos'])>float(a['pos']) for a,b in zip(active,active[1:]))
    eof=next(r for r in owners if r['actor']=='00000000')
    at=next(r for r in channels if r['age']==eof['age'] and r['channel']=='12')
    assert float(at['pos'])>=length and eof['guest_hp']==cue['health']
    assert eof['main']=='00000000' and eof['id']=='0' and eof['stored_health']=='0'
    assert all(r['length']=='0' for r in channels if r['channel']=='13')
    return dict(cue=cue,earlySamples=active,eof=eof,eofChannel=at)
proof=gate(rows)
bad=copy.deepcopy(rows);bad['CPU_BALL_OWNER'][0]['actor']='01000000'
try:gate(bad)
except AssertionError:pass
else:raise AssertionError('Wrong CPU audio owner accepted')
out.mkdir();report=dict(naturalCpuBallVoicePassed=True,priorPhysicalInputsUnchanged=True,
    proof=proof,coldSourceBookkeepingMinusOneNotSilentPlayback=True,wrongOwnerRejected=True,
    clipSHA256=sync.sha(clip),logSHA256=sync.sha(folder/'run.log'),terminal=terminal,
    heardMixAccepted=False,allCpuAudioContextsAccepted=False,fullPortAccepted=False)
(out/'report.json').write_text(json.dumps(report,indent=2))
print(json.dumps(dict(passed=True,cpuCue=proof['cue']['frame'],eofAge=proof['eof']['age'],sampleLength=length)))
