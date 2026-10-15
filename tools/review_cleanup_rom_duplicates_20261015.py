"""Exact candidate inventory only; no removals and no archive generation."""
import ctypes
import hashlib
import json
import zipfile
from pathlib import Path

R=Path(__file__).resolve().parent.parent
out=R/'audit_cleanup_rom_duplicate_review_20261015'
assert not out.exists()
def sha(p):
    with p.open('rb') as f: return hashlib.file_digest(f,'sha256').hexdigest().upper()
api=ctypes.WinDLL('kernel32',use_last_error=True).GetCompressedFileSizeW
api.argtypes=(ctypes.c_wchar_p,ctypes.POINTER(ctypes.c_uint32));api.restype=ctypes.c_uint32
current=R/'roms/mk2.zip'
digest=sha(current)
assert digest=='B9867A2D5F20D27A2E27FDC9799E44BE7FB6269948DBC1BE8EF53A8CB4C79EDD'
rows=[]
for folder in ('roms_v19_clean','roms_v20_clean','roms_v21_clean'):
    p=R/folder/'mk2.zip';st=p.lstat()
    assert p.resolve().is_relative_to(R) and st.st_nlink==1 and not st.st_file_attributes & 0x400
    assert sha(p)==digest
    high=ctypes.c_uint32();ctypes.set_last_error(0);low=api(str(p),ctypes.byref(high))
    if low==0xffffffff and ctypes.get_last_error(): raise ctypes.WinError(ctypes.get_last_error())
    rows.append(dict(path=str(p),logicalBytes=st.st_size,allocatedBytes=low+(high.value<<32),SHA256=digest,retainedIdenticalFile=str(current),safeExactDuplicateCandidate=True))
z=R/'release_current_native_playtest_20261013_complete_roms/MK2_Kano_Sonya_CURRENT_NATIVE_PLAYTEST_20261013_complete_roms.zip'
with zipfile.ZipFile(z) as f:
    names=f.namelist()
    guide=[n for n in names if n.endswith('MK2_KANO_SONYA_MOVES.txt')]
    documentation=[n for n in names if n.lower().endswith(('.txt','.md','.json'))]
report=dict(deletionPerformed=False,archiveCreated=False,exactDuplicateCandidates=rows,
            allocatedCandidateBytes=sum(x['allocatedBytes'] for x in rows),
            referenceReview='Scoped rg over current tools/CMD and workspace JSON/TXT/MD found these folder names only in historical storage inventories and the fresh census, not execution/proof pins. Parent should rerun final exact hash/path checks before deletion.',
            neverDeleteWholeFolders='Other mk2ks files inside old ROM folders have not been qualified.',
            oldCaptureBlocker='Knife/obj_dump capture folders have no literal reference found, but dynamic frame-source usage and original asset provenance not fully resolved; no capture deletion qualified.',
            currentZIP=str(z),currentZIPContainsMoveGuide=bool(guide),zipDocumentation= documentation,
            releaseGaps='Current ZIP is an explicitly unfinished playtest and predates external move guide and newest status. Do not claim final acceptance or rebuild solely to rename it.',
            fullPortAccepted=False)
out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
