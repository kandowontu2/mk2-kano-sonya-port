"""Resolve old ROM leaves to exact retained bytes; preserve unmatched old payloads."""
import ctypes
import hashlib
import json
from pathlib import Path

R=Path(__file__).resolve().parent.parent
out=R/'audit_old_rom_tree_duplicate_review_20261015'
assert not out.exists()
folders=[R/n for n in ('roms_v19_clean','roms_v20_clean','roms_v21_clean','release_rom_stage')]
external=[R/n for n in ('roms/mk2ks','mk','mk2','mk3','roms_v22_clean/mk2ks',
                      'diagnostic_native_selector_layers_long/roms/mk2ks')]
api=ctypes.WinDLL('kernel32',use_last_error=True).GetCompressedFileSizeW
api.argtypes=(ctypes.c_wchar_p,ctypes.POINTER(ctypes.c_uint32));api.restype=ctypes.c_uint32
cache={}
def sha(p):
    if p not in cache:
        with p.open('rb') as f:cache[p]=hashlib.file_digest(f,'sha256').hexdigest().upper()
    return cache[p]
def alloc(p):
    hi=ctypes.c_uint32();ctypes.set_last_error(0);lo=api(str(p),ctypes.byref(hi))
    if lo==0xffffffff and ctypes.get_last_error():raise ctypes.WinError(ctypes.get_last_error())
    return (hi.value<<32)|lo
leaves=[]
for folder in folders:
    assert folder.is_dir() and folder.resolve().is_relative_to(R)
    for p in folder.rglob('*'):
        assert not p.lstat().st_file_attributes&0x400
        if p.is_file():leaves.append(p)
assert len(leaves)<=150
outside=[p for folder in external if folder.is_dir() for p in folder.iterdir() if p.is_file()]
groups={}
for p in leaves:groups.setdefault((p.stat().st_size,sha(p)),[]).append(p)
targets=[];retained=[]
for (size,digest),items in groups.items():
    names={p.name for p in items}
    match=next((p for p in outside if p.name in names and p.stat().st_size==size and sha(p)==digest),None)
    if match is None:
        match=items.pop(0)
        retained.append(dict(path=str(match),bytes=size,SHA256=digest,
                             reason='No matching external retained file found; keep one original historical payload/program/UI copy, not all copies.'))
    for p in items:
        st=p.lstat();assert st.st_nlink==1 and p!=match and sha(match)==digest
        targets.append(dict(path=str(p),bytes=size,mtimeNS=st.st_mtime_ns,SHA256=digest,
                            allocatedBytes=alloc(p),retainedIdenticalFile=str(match)))
assert not ({x['path'] for x in targets}&{x['retainedIdenticalFile'] for x in targets})
report=dict(readOnly=True,deletionsPerformed=0,targets=targets,retainedUnmatchedOriginals=retained,
            candidateFiles=len(targets),allocatedCandidateBytes=sum(x['allocatedBytes'] for x in targets),
            existingLeaves=len(leaves),folders=[str(p) for p in folders],
            referenceReview='Prior scoped code/Lua/CMD/proof JSON searches found these old folder names only in storage bookkeeping. No current launcher/build references. Exact retained-byte mapping is mandatory; do not delete unmatched originals or whole trees blindly.',
            safety='Final parent containment/non-reparse/exact file-set/size/SHA and retained source SHA checks required immediately before file-only removal. No source/runtime files or retained lookup endpoints selected.',
            fullPortAccepted=False)
out.mkdir();(out/'deletion_plan.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items() if k!='targets'}))
