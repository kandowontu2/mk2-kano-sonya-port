"""Manifest obsolete exploratory snapshot outputs; no deletion/imported collectors."""
import ctypes
import hashlib
import json
import time
from pathlib import Path

R=Path(__file__).resolve().parent.parent
out=R/'audit_obsolete_capture_target_review_20261015'
assert not out.exists()
def sha(p):
    with p.open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest().upper()
api=ctypes.WinDLL('kernel32',use_last_error=True).GetCompressedFileSizeW
api.argtypes=(ctypes.c_wchar_p,ctypes.POINTER(ctypes.c_uint32));api.restype=ctypes.c_uint32
targets=[];begin=time.monotonic();count=0
for folder in ('obj_dump2','native_kano_knife_clean_fast2','native_kano_knife_clean_fast',
               'native_kano_knife_scan_late_fast','native_kano_knife_scan'):
    path=R/folder/'snap'
    assert path.resolve().is_relative_to(R) and path.is_dir()
    leaves=[]
    for p in path.rglob('*'):
        assert not p.lstat().st_file_attributes & 0x400
        if not p.is_file():continue
        assert p.suffix.lower()=='.png',p
        st=p.lstat();assert st.st_nlink==1
        with p.open('rb') as f:assert f.read(8)==b'\x89PNG\r\n\x1a\n'
        high=ctypes.c_uint32();ctypes.set_last_error(0);low=api(str(p),ctypes.byref(high))
        if low==0xffffffff and ctypes.get_last_error():raise ctypes.WinError(ctypes.get_last_error())
        leaves.append(dict(path=str(p),bytes=st.st_size,allocatedBytes=(high.value<<32)|low,
                           SHA256=sha(p),mtimeNS=st.st_mtime_ns))
        count+=1;assert count<=6000 and time.monotonic()-begin<30
    assert leaves
    targets.append(dict(path=str(path),files=leaves,allocatedBytes=sum(x['allocatedBytes'] for x in leaves),
                        reason='Unreferenced legacy exploratory emulator snapshots, not native ROM/GFX or accepted proof captures. Parent final exact path/set/hash guard required before removal.'))
sourcepaths=[R/'tools'/n for n in ('build_mk2ks_mk3.py','build_native_projectile_choreography.py',
              'build_native_projectile_impacts.py','verify_projectile_render.py','check_knife_screen_alignment.py')]
report=dict(readOnly=True,deletedFiles=0,archiveCreated=False,targets=targets,
            totalFiles=count,allocatedCandidateBytes=sum(x['allocatedBytes'] for x in targets),
            sourceDependencyReview='Original projectile assets decode original MK3 program/GFX via build_mk2ks_mk3, build_native_projectile_impacts, build_native_projectile_choreography. verify_projectile_render.original_source explicitly reads mk3/mk3-maincpu.bin and original GFX, not these screenshots. Current build embeds pinned mdata and picture header. check_knife_screen_alignment only consumes caller-supplied native-command suite snapshots, not these old MK3 folders.',
            referenceReview='Scoped code LUA/PY/PS1/CPP/H plus workspace JSON/TXT/MD/CMD/BAT searches for these exact legacy folder names found storage inventory/census entries only, no source generator, execution or accepted proof input pins. Historical bookkeeping is not game dependency.',
            retained='All cfg/NVRAM, original Lua traces, original program/GFX, generated assets, current/historical accepted audit captures and source snapshots; only five exact /snap subtrees proposed.',
            inspectedSourceHashes={str(p):sha(p) for p in sourcepaths},elapsedSeconds=time.monotonic()-begin,
            fullPortAccepted=False)
out.mkdir();(out/'deletion_plan.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(dict(targets=[dict(path=x['path'],files=len(x['files']),allocatedBytes=x['allocatedBytes']) for x in targets],totalFiles=count,allocatedCandidateBytes=report['allocatedCandidateBytes'],elapsedSeconds=report['elapsedSeconds'])))
