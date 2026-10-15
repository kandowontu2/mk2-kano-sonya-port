"""Current read-only, hardlink-aware storage inventory for the user's cleanup request."""
import ctypes
import json
import os
import shutil
import subprocess
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / 'audit_v4201_current_port_storage_inventory'
LIVE = ROOT / 'audit_v4188_sonya_mirror_guard_zoning_p2_campaign'
kernel = ctypes.WinDLL('kernel32', use_last_error=True)
size = kernel.GetCompressedFileSizeW
size.argtypes = (ctypes.c_wchar_p, ctypes.POINTER(ctypes.c_uint32))
size.restype = ctypes.c_uint32

def allocated(path):
    high = ctypes.c_uint32()
    ctypes.set_last_error(0)
    low = size(str(path), ctypes.byref(high))
    if low == 0xffffffff and ctypes.get_last_error():
        raise ctypes.WinError(ctypes.get_last_error())
    return (high.value << 32) | low

def main():
    if OUT.exists():
        raise ValueError('Never overwrite a cleanup inventory')
    groups, subgroups, seen, large, skipped = {}, {}, set(), [], []
    tick = time.monotonic()
    count = 0
    for base, dirs, files in os.walk(ROOT, followlinks=False):
        safe = []
        for name in dirs:
            path = Path(base) / name
            if path == LIVE:
                skipped.append(str(path) + ' (known live native capture; never select for cleanup)')
            elif path.lstat().st_file_attributes & 0x400:
                skipped.append(str(path))
            else:
                safe.append(name)
        dirs[:] = safe
        for name in files:
            path = Path(base) / name
            meta = path.lstat()
            if meta.st_file_attributes & 0x400:
                skipped.append(str(path))
                continue
            parts = path.relative_to(ROOT).parts
            top = parts[0] if len(parts) > 1 else '[root files]'
            sub = '/'.join(parts[:2]) if len(parts) > 2 else top
            row = groups.setdefault(top, dict(name=top, files=0, logicalBytes=0, allocatedBytes=0))
            child = subgroups.setdefault(sub, dict(name=sub, files=0, logicalBytes=0, allocatedBytes=0))
            for entry in (row, child):
                entry['files'] += 1
                entry['logicalBytes'] += meta.st_size
            key = (meta.st_dev, meta.st_ino)
            if key not in seen:
                seen.add(key)
                amount = allocated(path)
                for entry in (row, child):
                    entry['allocatedBytes'] += amount
                if amount >= 4 * 1024 * 1024:
                    large.append(dict(path=str(path), allocatedBytes=amount,
                                      logicalBytes=meta.st_size, links=meta.st_nlink))
            count += 1
            if time.monotonic() - tick > 20:
                print('Read-only inventory:', count, 'files', flush=True)
                tick = time.monotonic()
    result = dict(root=str(ROOT), readOnly=True, diskFreeBytes=shutil.disk_usage(ROOT).free,
                  uniqueAllocatedBytes=sum(r['allocatedBytes'] for r in groups.values()),
                  groups=sorted(groups.values(), key=lambda r:r['allocatedBytes'], reverse=True),
                  subgroups=sorted(subgroups.values(), key=lambda r:r['allocatedBytes'], reverse=True),
                  largestFiles=sorted(large, key=lambda r:r['allocatedBytes'], reverse=True),
                  skippedReparsePoints=skipped)
    OUT.mkdir()
    if subprocess.run(['compact.exe','/C','/I','/Q','/S:'+str(OUT)],capture_output=True).returncode:
        raise ValueError('Inventory compressed before writing')
    (OUT / 'inventory.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(dict(allocatedGiB=round(result['uniqueAllocatedBytes']/2**30, 2),
                         topGroups=result['groups'][:18], topSubgroups=result['subgroups'][:12],
                         largestFiles=result['largestFiles'][:15]), indent=2), flush=True)

if __name__ == '__main__':
    main()
