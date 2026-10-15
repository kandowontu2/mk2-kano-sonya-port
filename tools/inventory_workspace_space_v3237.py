"""Read-only NTFS space inventory, with physical hardlinks counted once."""
import ctypes, json, os, shutil, time
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / 'audit_v3238_workspace_space_inventory'
kernel = ctypes.WinDLL('kernel32', use_last_error=True)
size = kernel.GetCompressedFileSizeW
size.argtypes = (ctypes.c_wchar_p, ctypes.POINTER(ctypes.c_uint32))
size.restype = ctypes.c_uint32
def allocated(path):
    high = ctypes.c_uint32(); ctypes.set_last_error(0)
    low = size(str(path), ctypes.byref(high))
    if low == 0xffffffff and ctypes.get_last_error():
        raise ctypes.WinError(ctypes.get_last_error())
    return (high.value << 32) | low
def main():
    if OUT.exists(): raise RuntimeError('Immutable inventory already exists')
    groups = {}; identities = {}; skipped = []; largest = []
    started = time.time()
    for base, dirs, files in os.walk(ROOT, followlinks=False):
        safe = []
        for name in dirs:
            path = Path(base) / name
            if path.stat(follow_symlinks=False).st_file_attributes & 0x400:
                skipped.append(str(path))
            else: safe.append(name)
        dirs[:] = safe
        for name in files:
            path = Path(base) / name
            meta = path.stat(follow_symlinks=False)
            if meta.st_file_attributes & 0x400:
                skipped.append(str(path)); continue
            rel = path.relative_to(ROOT); parts = rel.parts
            group = parts[0] if len(parts)>1 else '[root files]'
            row = groups.setdefault(group, dict(name=group,files=0,logicalBytes=0,uniqueAllocatedBytes=0))
            row['files'] += 1; row['logicalBytes'] += meta.st_size
            key = (meta.st_dev, meta.st_ino)
            if key not in identities:
                amount = allocated(path)
                identities[key] = dict(bytes=amount,links=meta.st_nlink,seen=1,first=str(path))
                row['uniqueAllocatedBytes'] += amount
                if amount >= 8*1024*1024:
                    largest.append(dict(path=str(path),allocatedBytes=amount,logicalBytes=meta.st_size,links=meta.st_nlink))
            else: identities[key]['seen'] += 1
        if time.time()-started>30:
            print('Scanned',sum(r['files'] for r in groups.values()),'files',flush=True); started=time.time()
    disk = shutil.disk_usage(ROOT)
    report = dict(readOnly=True,root=str(ROOT),diskFreeBytes=disk.free,
        groups=sorted(groups.values(),key=lambda r:r['uniqueAllocatedBytes'],reverse=True),
        largestFiles=sorted(largest,key=lambda r:r['allocatedBytes'],reverse=True),
        uniqueAllocatedBytes=sum(r['bytes'] for r in identities.values()),
        externallyLinkedIdentities=sum(r['seen']<r['links'] for r in identities.values()),
        skippedReparsePoints=skipped)
    OUT.mkdir(); (OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({**{k:v for k,v in report.items() if k not in ('groups','largestFiles')},
       'largestGroups':report['groups'][:25],'largestFiles':report['largestFiles'][:25]},indent=2))
if __name__=='__main__': main()
