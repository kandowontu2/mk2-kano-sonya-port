"""OS nonzero render admission, not a heard mix or hardware hearing claim."""
import copy,json,re
import check_campaign_stage_chronology as chronology
import verify_native_source_sync as sync
sync.verify();R=sync.ROOT
case=R/'audit_current_os_audio_admission_runtime';out=R/'audit_current_os_audio_admission_checked';assert not out.exists()
t=json.loads((case/'terminal.json').read_text(encoding='utf-8-sig'))
assert t['exitCode']==0 and t['limitReason'] is None and t['elapsedSeconds']<=45.5 and t['peakWorkingSetBytes']<=320*1024*1024 and t['hostPeakWorkingSetBytes']<=320*1024*1024
assert t['osAudioSettingsModified'] is False and t['soundProvider']=='auto' and t['throttled'] is True
text=(case/'run.log').read_text();error=(case/'stderr.log').read_text();assert not error.strip()
assert not re.search(r'failed to submit|Error creating|Error playing|Could not find XAudio2|LUA ERROR',text,re.I)
backend='directsound' if 'DirectSound: Primary buffer:' in text else 'xaudio2' if 'Sound: XAudio2 initialized.' in text else 'unidentified'
records=[json.loads(l) for l in (case/'audio_sessions.jsonl').read_text().splitlines()];assert len(records)<=120
native=chronology.load(case/'run.log');assert native['HOST_BOUND'][-1]['maximum_fields']=='1850'
assert any(x['human']=='18:18' and x['cpu']=='18:18' for x in native['FIGHT'])
def gate(rows):
 assert rows and backend!='unidentified'
 assert all(x['pid']==t['pid'] and x['birth']==t['birth'] for x in rows)
 eligible=[]
 for x in rows:
  for r in x['readings']:
   assert int(r['Pid'])==t['pid']
   if r.get('Error'):continue
   assert 0<=r['Peak']<=1 and 0<=r['SessionVolume']<=1 and 0<=r['EndpointVolume']<=1
   if r['State']==1 and r['Peak']>0 and not r['SessionMute'] and not r['EndpointMute'] and r['SessionVolume']>0 and r['EndpointVolume']>0:eligible.append(dict(elapsedSeconds=x['elapsedSeconds'],reading=r))
 assert eligible,'No nonzero unmuted exact-process active render-session observation'
 return eligible
try:proof=gate(records);passed=True;failure=None
except AssertionError as e:proof=[];passed=False;failure=str(e)
faults=[]
if passed:
 for kind in ['wrong_pid','zero_peak','inactive_session','session_muted','endpoint_muted']:
  b=copy.deepcopy(records)
  for x in b:
   if kind=='wrong_pid':x['pid']+=1
   for r in x['readings']:
    if kind=='zero_peak':r['Peak']=0
    elif kind=='inactive_session':r['State']=0
    elif kind=='session_muted':r['SessionMute']=True
    elif kind=='endpoint_muted':r['EndpointMute']=True
  try:gate(b)
  except AssertionError:faults.append(kind)
  else:raise AssertionError('Fault accepted:'+kind)
settings=[r for x in records for r in x['readings'] if not r.get('Error')]
out.mkdir();report=dict(finiteObservationCompleted=True,actualOSNonzeroRenderAdmissionAccepted=passed,failureReason=failure,actualBackend=backend,nonzeroUnmutedActiveReadings=len(proof),firstQualified=proof[0] if proof else None,lastQualified=proof[-1] if proof else None,effectiveFaultsRejected=faults,
 sessionOrEndpointExternalMuteObserved=any(r['SessionMute'] or r['EndpointMute'] for r in settings),externalZeroVolumeObserved=any(r['SessionVolume']==0 or r['EndpointVolume']==0 for r in settings),monitorErrors=[r['Error'] for x in records for r in x['readings'] if r.get('Error')],
 actualNativeFight=native['FIGHT'][0],actualNativeOwnedCPUCues=native.get('CPU_BICYCLE_CUE',[]),actualHostBackendLines=[l for l in text.splitlines() if 'Sound:' in l or 'DirectSound:' in l],
 terminal=t,logSHA256=sync.sha(case/'run.log'),sessionsSHA256=sync.sha(case/'audio_sessions.jsonl'),scope='One default-auto real-throttle current coldselection/fight. ActualexactPIDWindowsaudiosession active+nonzeropeak and existingmutevolumeREADONLY; noPCMrecording, settingschange or exactspeakerhardware/heardmix judgment.',heardMixAccepted=False,hardwareHearingAccepted=False,allAudioContextsAccepted=False,fullPortAccepted=False)
(out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
