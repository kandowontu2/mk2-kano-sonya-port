"""Bounded read-only allocation census; never infer deletion authority from size."""
import ctypes
import heapq
import json
import os
import time
from pathlib import Path

R = Path(__file__).resolve().parent.parent
out = R/'audit_cleanup_candidate_census_20261015'
assert not out.exists()
api = ctypes.WinDLL('kernel32', use_last_error=True).GetCompressedFileSizeW
api.argtypes = (ctypes.c_wchar_p, ctypes.POINTER(ctypes.c_uint32))
api.restype = ctypes.c_uint32
start = time.monotonic()
groups, largest, seen = {}, [], set()
count = 0
bounded = False
for base, dirs, files in os.walk(R, followlinks=False):
    dirs[:] = [d for d in dirs if not (Path(base)/d).lstat().st_file_attributes & 0x400]
    for name in files:
        p = Path(base)/name
        st = p.lstat()
        if st.st_file_attributes & 0x400: continue
        rel = p.relative_to(R)
        group = rel.parts[0] if len(rel.parts)>1 else '[root]'
        row = groups.setdefault(group, [0, 0, 0])
        row[0] += 1
        row[1] += st.st_size
        key = (st.st_dev, st.st_ino)
        if key not in seen:
            seen.add(key)
            high = ctypes.c_uint32()
            ctypes.set_last_error(0)
            low = api(str(p), ctypes.byref(high))
            if low == 0xffffffff and ctypes.get_last_error():
                raise ctypes.WinError(ctypes.get_last_error())
            allocated = (high.value << 32) | low
            row[2] += allocated
            item = (allocated, str(rel), st.st_size, st.st_nlink)
            if len(largest)<40: heapq.heappush(largest, item)
            elif item>largest[0]: heapq.heapreplace(largest, item)
        count += 1
        if count>=200000 or time.monotonic()-start>60:
            bounded=True
            break
    if bounded: break
report = dict(readOnly=True, complete=not bounded, elapsedSeconds=time.monotonic()-start,
              files=count, uniqueAllocatedBytes=sum(r[2] for r in groups.values()),
              logicalBytes=sum(r[1] for r in groups.values()),
              largest=[dict(allocatedBytes=a, path=p, logicalBytes=s, links=n)
                       for a,p,s,n in sorted(largest, reverse=True)],
              topGroups=[dict(path=p, files=r[0], logicalBytes=r[1], allocatedBytes=r[2])
                         for p,r in sorted(groups.items(),key=lambda x:x[1][2],reverse=True)[:30]],
              deletionPlan=False, deletedFiles=0,
              scope='Reparse points skipped; hardlink identity counted once. Allocation is API-reported compressed size, not guaranteed recoverable free disk bytes. All source/proof/live files preserved.')
out.mkdir()
(out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report))
