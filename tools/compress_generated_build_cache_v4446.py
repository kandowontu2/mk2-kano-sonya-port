"""Reclaim allocated space from generated compiler cache without deleting bytes."""
import ctypes,hashlib,json,os,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
TARGET=ROOT/'mame-mkp/build/mingw-gcc'
OUT=ROOT/'audit_v4447_generated_build_cache_compression'

def need(ok,message):
    if not ok:raise ValueError(message)

def sha(path):
    h=hashlib.sha256()
    with Path(path).open('rb') as f:
        for chunk in iter(lambda:f.read(1048576),b''):h.update(chunk)
    return h.hexdigest().upper()

allocated_api=ctypes.windll.kernel32.GetCompressedFileSizeW
allocated_api.argtypes=[ctypes.c_wchar_p,ctypes.POINTER(ctypes.c_uint32)]
allocated_api.restype=ctypes.c_uint32

def inventory():
    found={}
    for p in sorted(TARGET.rglob('*')):
        if not p.is_file():continue
        need(p.resolve().is_relative_to(TARGET.resolve()),'Exact generated-cache target boundary')
        s=p.stat();need(not s.st_file_attributes&0x400,'No file reparse targets')
        high=ctypes.c_uint32();low=allocated_api(str(p),ctypes.byref(high))
        need(low!=0xffffffff,'Exact NTFS allocated file size')
        found[str(p)]=dict(sha256=sha(p),bytes=s.st_size,mtimeNS=s.st_mtime_ns,
                          allocated=(high.value<<32)|low)
    return found

def main():
    need(not OUT.exists(),'Fresh immutable cleanup report')
    need(TARGET.resolve()==ROOT/'mame-mkp/build/mingw-gcc' and
         not TARGET.stat().st_file_attributes&0x400,'Exact non-reparse generated compiler cache')
    tracked=subprocess.run(['git','-C',str(ROOT/'mame-mkp'),'ls-files','--','build/mingw-gcc'],
                           capture_output=True,text=True,check=True)
    need(not tracked.stdout.strip(),'No tracked source files targeted')
    query="Get-CimInstance Win32_Process | Where-Object { $_.Name -match '^(make|mingw32-make|gcc|g\\+\\+|cc1plus|ld|ar|compact)\\.exe$' } | Select-Object ProcessId,Name,CommandLine | ConvertTo-Json -Compress"
    active=subprocess.run(['powershell.exe','-NoProfile','-Command',query],capture_output=True,text=True,check=True)
    need(not active.stdout.strip(),'No active compiler/linker/cache compression job')
    preserved=[ROOT/'mame-mkp/mkport.exe',
       ROOT/'diagnostic_v3836_native_mileena_rom_identity/mkport_candidate.exe',
       ROOT/'diagnostic_v1836_ball_register_boundary/mkport_candidate.exe',
       ROOT/'PLAY_CURRENT_V1836_CHECKED.cmd',
       ROOT/'release_v1863_current_playtest/MK2_Kano_Sonya_v1836_CURRENT_PLAYTEST.zip']
    public={str(p):sha(p) for p in preserved}
    status=subprocess.run(['git','-C',str(ROOT/'mame-mkp'),'status','--porcelain'],
                          capture_output=True,text=True,check=True).stdout
    before=inventory();need(before,'Real compiler cache files, no broad workspace target')
    paths=list(before)
    # Native filesystem compression only. No deletion, moves, archives or
    # alternate shell interpretation of resolved file paths.
    for i in range(0,len(paths),32):
        done=subprocess.run(['compact.exe','/C','/EXE:LZX','/F','/I','/Q',*paths[i:i+32]],
                            capture_output=True,text=True)
        need(done.returncode==0,'Every exact compiler-cache file compressed successfully')
    after=inventory();need(before.keys()==after.keys(),'No compiler-cache files created or deleted')
    for p,b in before.items():
        a=after[p]
        need(all(a[k]==b[k] for k in ('sha256','bytes','mtimeNS')),
             'Every original cache byte and modification time preserved')
    need(all(sha(p)==h for p,h in public.items()),'Installed binary, candidate and public release unchanged')
    need(subprocess.run(['git','-C',str(ROOT/'mame-mkp'),'status','--porcelain'],
          capture_output=True,text=True,check=True).stdout==status,'Existing dirty source worktree unchanged')
    old=sum(v['allocated'] for v in before.values());new=sum(v['allocated'] for v in after.values())
    report=dict(passed=True,target=str(TARGET),method='Native NTFS LZX compression, exact file paths',
      files=len(before),logicalBytes=sum(v['bytes'] for v in before.values()),
      allocatedBytesBefore=old,allocatedBytesAfter=new,newAllocatedBytesReclaimed=old-new,
      deletedFiles=0,newBuilds=0,sourceChanges=0,originalBytesAndMtimesPreserved=True,
      publicInputHashes=public,sourceSHA256=sha(__file__),cacheBefore=before,cacheAfter=after,
      fullPortAcceptance=False)
    OUT.mkdir()
    need(subprocess.run(['compact.exe','/C','/I','/Q','/S:'+str(OUT)],capture_output=True).returncode==0,
         'Compress new evidence before writes')
    (OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k not in ('cacheBefore','cacheAfter','publicInputHashes')},indent=2),flush=True)

if __name__=='__main__':main()
