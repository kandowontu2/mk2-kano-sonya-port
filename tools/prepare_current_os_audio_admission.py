"""Prepare one default-auto audible OS admission case; DO NOT launch."""
import json
import verify_native_source_sync as sync
sync.verify();R=sync.ROOT
base=R/'audit_current_cpu_sonya_voice_earlier_upper_preparation';out=R/'audit_current_os_audio_admission_preparation';assert not out.exists()
s=(base/'campaign.lua').read_text();assert 'frame>=4000' in s;s=s.replace('frame>=4000','frame>=1850').replace('maximum_fields=4000','maximum_fields=1850')
assert ':write_' not in s and ':snapshot(' not in s
out.mkdir();lua=out/'campaign.lua';lua.write_text(s)
cs=R/'tools/ReadOnlyAudioSession.cs'
runner=(base/'run.ps1').read_text().replace(base.name+'/campaign.lua',out.name+'/campaign.lua').replace(sync.sha(base/'campaign.lua'),sync.sha(lua)).replace('audit_current_cpu_sonya_voice_earlier_upper_runtime','audit_current_os_audio_admission_runtime')
runner=runner.replace("'-sound','none'","'-sound','auto'").replace("'-nothrottle'","'-throttle'").replace("'-str','900'","'-str','40'")
runner=runner.replace('Elapsed.TotalSeconds -gt 90','Elapsed.TotalSeconds -gt 45')
runner=runner.replace("'-samples','-samplerate'","'-verbose','-samples','-samplerate'")
runner=runner.replace('$taskLog=Join-Path $taskCase',"Add-Type -Path (Join-Path $taskRoot 'tools/ReadOnlyAudioSession.cs')\n$taskLog=Join-Path $taskCase")
runner=runner.replace('$taskPeak=0L',"$taskPeak=0L\n$taskHostPeak=0L\n$taskHost=[Diagnostics.Process]::GetCurrentProcess()\n$taskAudioWriter=[IO.StreamWriter]::new((Join-Path $taskCase 'audio_sessions.jsonl'),$false)\n$taskAudioClock=-1.0")
needle=' $taskPeak=[Math]::Max($taskPeak,$taskProcess.WorkingSet64)'
assert runner.count(needle)==1
runner=runner.replace(needle,needle+"""
 $taskHost.Refresh();$taskHostPeak=[Math]::Max($taskHostPeak,$taskHost.WorkingSet64)
 if($taskHostPeak -gt 320MB){$taskLimitReason='host_memory_limit'}
 if($taskClock.Elapsed.TotalSeconds-$taskAudioClock -ge 0.5){
  $taskActual=Get-Process -Id $taskProcess.Id -ErrorAction SilentlyContinue
  if($taskActual -and $taskActual.StartTime -eq $taskBirth){
   $taskReadings=@([MK2OutputProbe.ReadOnly]::Snapshot([uint32]$taskProcess.Id))
   $taskAudioRow=[ordered]@{elapsedSeconds=$taskClock.Elapsed.TotalSeconds;pid=$taskProcess.Id;birth=$taskBirth.ToString('o');readings=$taskReadings;hostWorkingSetBytes=$taskHost.WorkingSet64}
   $taskAudioWriter.WriteLine(($taskAudioRow|ConvertTo-Json -Compress -Depth 5));$taskAudioWriter.Flush()
  }
  $taskAudioClock=$taskClock.Elapsed.TotalSeconds
 }
""")
runner=runner.replace('$taskProcess.WaitForExit()',"$taskAudioWriter.Dispose()\n$taskProcess.WaitForExit()")
runner=runner.replace("rawMedia='none'","hostPeakWorkingSetBytes=$taskHostPeak;rawMedia='none';osAudioSettingsModified=$false;soundProvider='auto';throttled=$true")
# Child creation is scoped in the runner only; preparation never calls it.
assert "'-sound','auto'" in runner and "'-throttle'" in runner and "'-nothrottle'" not in runner
assert all(token not in runner for token in ['.SetMute(','.SetMasterVolume(','.SetMasterVolumeLevelScalar(','SetDefaultEndpoint'])
(out/'run.ps1').write_text(runner)
sdk='C:/Program Files (x86)/Windows Kits/10/Include/10.0.22621.0/um/'
headers=['audiopolicy.h','mmdeviceapi.h','endpointvolume.h','audioclient.h']
report=dict(preparedNotRun=True,LuaSHA256=sync.sha(lua),COMSourceSHA256=sync.sha(cs),COMSource=str(cs),SDKHeaderHashes={h:sync.sha(__import__('pathlib').Path(sdk+h)) for h in headers},
 originalPhysicalController='Existing physical P2Sonya CPU18 ready-lateupper policy unchanged; only fieldceiling1850 replaces4000. Native own/CPUidentity and marker/HP observers retained.',
 sound='defaultauto,48000,real-throttle; noforcedbackend/volume/DIP. Freshconfig doesnotmutate publicsettings. AudibleOUTPUT probe NOT heardmix judgment.',
 reads='All active renderendpoint sessions, exactPID/birth, state/peak/sessionmutevolume/endpointmutevolume GETonly. Set methods are ABI placeholders never called. NoaudioPCMbuffers read/recorded.',
 externalState='Sessionorendpointmute/zero volume/disconnecteddevice are externalconditions; report honestly, neverunmute/changevolume/defaultdevice orlabelgamebug.',
 limits='1850fields/40emulatedseconds;45wallseconds;eachhost/child320MiB;10MiBtext;0PNGs/WAV/rawPCM',
 noAudibleLaunchYet=True,heardMixAccepted=False,fullPortAccepted=False)
(out/'source.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(dict(preparation=str(out),LuaSHA256=sync.sha(lua),COMSourceSHA256=sync.sha(cs),preparedNotRun=True)))
