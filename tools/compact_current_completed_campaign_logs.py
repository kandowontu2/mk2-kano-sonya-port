"""Compress exact completed text logs in place; no archive/deletion/live targets."""
import ctypes,json,subprocess
from ctypes import wintypes
import verify_native_source_sync as sync
sync.verify()
root=sync.ROOT
out=root/'audit_current_completed_campaign_log_compression_20261014';assert not out.exists()
names=['sonya_p1_subzero_settled_leg','sonya_p1_subzero_guard_release_leg',
 'sonya_p1_subzero_short_leg','sonya_p1_liukang_short_leg','sonya_p1_boss_light',
 'sonya_p1_kintaro_close_retreat','sonya_p1_kintaro_close_retreat_solo',
 'sonya_p1_kintaro_attack_guard','sonya_p2_baraka_short_leg','sonya_p2_kano_short_leg',
 'sonya_p2_jax_ring_spacing','sonya_p2_jax_ground_jump_leg','kano_earned_ending_sound_events']
k=ctypes.WinDLL('kernel32',use_last_error=True)
k.GetCompressedFileSizeW.argtypes=[wintypes.LPCWSTR,ctypes.POINTER(wintypes.DWORD)]
k.GetCompressedFileSizeW.restype=wintypes.DWORD
k.OpenProcess.argtypes=[wintypes.DWORD,wintypes.BOOL,wintypes.DWORD];k.OpenProcess.restype=wintypes.HANDLE
k.GetExitCodeProcess.argtypes=[wintypes.HANDLE,ctypes.POINTER(wintypes.DWORD)]
k.CloseHandle.argtypes=[wintypes.HANDLE]
def allocated(path):
    high=wintypes.DWORD();ctypes.set_last_error(0)
    low=k.GetCompressedFileSizeW(str(path),ctypes.byref(high))
    if low==0xffffffff and ctypes.get_last_error():raise ctypes.WinError(ctypes.get_last_error())
    return (high.value<<32)|low
def live(pid):
    handle=k.OpenProcess(0x1000,False,pid)
    if not handle:return False
    try:
        code=wintypes.DWORD();assert k.GetExitCodeProcess(handle,ctypes.byref(code))
        return code.value==259
    finally:k.CloseHandle(handle)
rows=[];skipped=[]
for name in names:
    case=(root/('audit_current_'+name+'_runtime')).resolve()
    assert case.is_relative_to(root.resolve()) and not case.is_symlink()
    terminal=json.loads((case/'terminal.json').read_text(encoding='utf-8-sig'))
    assert terminal['exitCode'] in (0,-1) and terminal['limitReason'] in (None,'wall_limit')
    if live(terminal['pid']):skipped.append(str(case));continue
    path=case/'run.log';assert path.is_file() and not path.is_symlink()
    before=allocated(path);digest=sync.sha(path)
    completed=subprocess.run(['compact.exe','/C','/EXE:LZX','/F','/I','/Q',str(path)],capture_output=True,text=True)
    assert completed.returncode==0 and sync.sha(path)==digest
    rows.append(dict(path=str(path),logicalBytes=path.stat().st_size,sha256=digest,
        allocatedBefore=before,allocatedAfter=allocated(path)))
result=dict(files=rows,skippedPotentiallyLivePIDs=skipped,
    allocatedBytesBefore=sum(r['allocatedBefore'] for r in rows),
    allocatedBytesAfter=sum(r['allocatedAfter'] for r in rows),
    archiveCreated=False,deletedFiles=0,sourceOrBuildChanged=False,
    scope='Exact completed text logs only; content remains readable and checksum-identical. Allocation measured by GetCompressedFileSizeW, not logical file lengths.')
result['allocatedBytesReduced']=result['allocatedBytesBefore']-result['allocatedBytesAfter']
out.mkdir();(out/'report.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({key:value for key,value in result.items() if key!='files'}))
