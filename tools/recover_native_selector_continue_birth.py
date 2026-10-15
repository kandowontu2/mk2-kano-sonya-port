"""Recover only the original completed P2 run's rounded CIM birth rejection.

Actual retained kernel handle supplies exact PID/birth/exit/path. The saved
LIVE census supplies parent/full command. Run all original positive/fault
gates on unchanged original RAM; never replay a game or overwrite its failure.
"""
import ctypes as c,json,subprocess,sys
from ctypes import wintypes as w
from pathlib import Path
import native_process_census_v6647 as kernel
import read_live_shang_drain_frames as hosts
import capture_native_kano_laser_cross_continue as prior

ROOT,need,sha=prior.ROOT,prior.need,prior.sha


def recover(state,cases,handles,expected):
    key='kano_p2_to_sonya';folder,text,images,old=cases[key];held=handles[key];job=held['process']
    out=ROOT/'audit_native_selector_continue_kano_p2_to_sonya_kernel_birth_recovery'
    need(not out.exists()and job.poll()==0 and job.pid==42416 and not kernel.census(),'Same original native terminal, no game replay/other native game')
    host=next(p for p in hosts.census_hosts()if p['ProcessId']==40856)
    need(host['ParentProcessId']==39948 and host['createdUnix']==1791732779.396103 and
         host['CommandLine']=='"'+sys.executable+'" -B tools/capture_native_selector_continue.py','Exact original host kernel identity')
    started=json.loads((folder/'process.json').read_text());live=json.loads((folder/'live_census.json').read_text())
    terminal=json.loads((folder/'native_terminal.json').read_text())
    reason="ValueError('Actual exact native executable child, birth time and isolated full command')"
    need(terminal['exitCode']==0 and terminal['observationErrors']==[reason]and terminal['nativePID']is None and
         old['passed']is False and old['nativeIdentity']is None and old['nativeExit']==0 and
         old['actualGuestGFXProofs']==expected and not(folder/'stderr.log').read_text()and
         started['nativeProducerPID']==job.pid and started['command']==held['command']and
         all(sha(p)==h for p,h in old['inputHashes'].items()),'Only original exact birth-boundary rejection; all five complete native byte proofs and frozen inputs intact')
    times=[w.FILETIME()for _ in range(4)]
    need(kernel.k.GetProcessTimes(job._handle,*(c.byref(t)for t in times)),'Read original retained native kernel handle times')
    to_unix=lambda t:((t.dwHighDateTime<<32)|t.dwLowDateTime)/10**7-11644473600
    born,ended=to_unix(times[0]),to_unix(times[1])
    get_pid=kernel.k.GetProcessId;get_pid.argtypes=[w.HANDLE];get_pid.restype=w.DWORD
    need(get_pid(job._handle)==job.pid and born>=started['startedUnix']and ended>born,'Actual exact original PID/creation/exit kernel handle, not rounded text or replacement')
    path=c.create_unicode_buffer(32768);length=w.DWORD(len(path))
    need(kernel.k.QueryFullProcessImageNameW(job._handle,0,path,c.byref(length)), 'Actual original retained native image path after termination')
    matches=[p for p in live if p['ProcessId']==job.pid and p['ParentProcessId']==40856 and
        p['ExecutablePath']==path.value and p['CommandLine']==subprocess.list2cmdline(held['command'])and
        0<=born-p['createdUnix']<0.001 and 0<started['startedUnix']-p['createdUnix']<0.001]
    need(len(matches)==1,'Saved exact live parent/path/command; ONLY millisecond CIM truncation crossed the launch-time lower bound')
    actual=dict(matches[0],createdUnix=born)
    recovery=dict(passed=True,originalNativeKernelIdentity=actual,actualKernelExitUnix=ended,nativeExit=0,
        actualOriginalHostIdentity=host,originalCIMBornUnix=matches[0]['createdUnix'],actualLaunchLowerBound=started['startedUnix'],
        originalRoundedBirthRejectionPreserved=True,originalCapturePassedFalsePreserved=True,
        originalCaptureSHA256=sha(folder/'report.json'),originalTerminalSHA256=sha(folder/'native_terminal.json'),
        newNativeBoots=0,newROMCopies=0,newRawMedia=0,fullPortAcceptance=False)
    out.mkdir();(out/'identity_recovery.json').write_text(json.dumps(recovery,indent=2)+'\n')
    normalized_terminal=dict(terminal,nativePID=job.pid,observationErrors=[],
        originalObservationErrors=terminal['observationErrors'],actualKernelIdentityRecoveryAccepted=True,
        originalTerminalSHA256=sha(folder/'native_terminal.json'))
    (out/'native_terminal.json').write_text(json.dumps(normalized_terminal,indent=2)+'\n')
    # Exact original six actual-state fault trials, without capture/IO/replay.
    source=prior.original.source
    first=source.index('  result=gate(text,fighter,side,target);')
    last=source.index('\n except Exception as e:r.update',first)
    body=source[first:last]
    need(body.count('except(ValueError,AssertionError,KeyError)as e:')==1,'One exact original six-fault exception boundary')
    body=body.replace('except(ValueError,AssertionError,KeyError)as e:','except(ValueError,AssertionError)as e:',1)
    validate='def validate_original(text,images,r,out,fighter,side,target,pins):\n'+''.join('    '+line[2:]+'\n'for line in body.splitlines())+'    return r\n'
    scope=dict(state['capture'].__globals__)
    exec(compile(validate,__file__+'::unchanged_original_capture_positive_and_six_state_faults','exec'),scope)
    recovered=dict(old,nativeIdentity=actual,inputHashes=dict(old['inputHashes']),
        originalRejectedCapturePreserved=True,originalRejectedCaptureSHA256=sha(folder/'report.json'),
        actualKernelIdentityRecoverySHA256=sha(out/'identity_recovery.json'))
    for p in (Path(__file__),ROOT/'tools/qualify_native_selector_continue_extra_windows.py',out/'identity_recovery.json',
        folder/'report.json',folder/'process.json',folder/'live_census.json',folder/'native_terminal.json',folder/'run.log.gz'):
        recovered['inputHashes'][str(p.resolve())]=sha(p)
    scope['validate_original'](text,images,recovered,out,'kano',2,'sonya',recovered['inputHashes'])
    need(recovered['passed']and len(recovered['actualFaultsRejected'])==6 and old['passed']is False,
         'All original positive gates and six actual faults restored, original rejected report remains FALSE')
    (out/'report.json').write_text(json.dumps(recovered,indent=2)+'\n')
    held['recoveredIdentity']=actual
    qualified=state['qualify'](out,text,images,recovered,'kano',2,'sonya')
    pixels=state['pixel_check'](out,text,images,'kano',2,'sonya')
    controls=state['control_check'](out,text,'kano',2,'sonya')
    state['COMPLETED'].append(key)
    print(json.dumps(dict(passed=True,key=key,actualKernelBorn=born,originalNativeReplayed=False,
        originalCaptureStillPassedFalse=True,originalStateRasterFaults=len(qualified['actualFaultsRejected']),
        actualControlFaults=len(controls['actualControlFaultsRejected']),additionalPixelFaults=len(pixels['additionalActualImageFaultsRejected']),
        fullPortAcceptance=False)),flush=True)
    return dict(folder=out,text=text,images=images,report=recovered,qualified=qualified,pixels=pixels,controls=controls)
