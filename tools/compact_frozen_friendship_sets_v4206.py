"""Lossless bounded frozen-evidence compaction; no deletions or native media copies.

Retained original captures remain at their original paths with identical logical
bytes. No active native experiment, public executable, build or source is targeted.
"""
import concurrent.futures,json,re,subprocess,time
from pathlib import Path
import compact_current_tomb_logs_v3654 as storage
import run_mirror_guard_zoning_campaign_ram_v4187 as current

ROOT,need,sha=current.ROOT,current.need,current.sha
OUT=ROOT/'audit_v4207_frozen_friendship_set_compaction'
NAMES=('audit_v2756_native_kano_friendship_palette_p2','audit_v2731_current_kano_friendship_palette_lifecycle_p2',
 'audit_v2718_current_sonya_friendship_lifecycle_p2','audit_v2760_native_sonya_friendship_palette_p2',
 'audit_v2718_current_kano_friendship_lifecycle_p2','audit_v2756_native_kano_friendship_palette_p1',
 'audit_v2731_current_kano_friendship_palette_lifecycle_p1','audit_v2760_native_sonya_friendship_palette_p1',
 'audit_v2704_current_sonya_friendship_full_render_p1','audit_v2704_current_kano_friendship_full_render_p1')

def safe(p):
    p=Path(p).resolve();need(p.is_file() and p.parent.name in NAMES and p.parent.parent==ROOT.resolve(),'Only exact frozen direct evidence file')
    for a in (p,*p.parents):
        if a==ROOT.resolve():break
        need(not a.lstat().st_file_attributes&0x400,'No reparse file/ancestor')
    return p

def batch(rows):
    prepared=[]
    for row in rows:
        p=safe(row['path']);stat=p.stat()
        need(stat.st_nlink==1 and stat.st_size==row['logicalBytes'] and stat.st_mtime_ns==row['mtimeNS'] and storage.allocated(p)==row['allocatedBefore'],'Exact immutable inventory still current before compaction')
        prepared.append((p,row,sha(p)))
    result=subprocess.run(['compact.exe','/C','/F','/EXE:LZX','/I','/Q',*[str(p) for p,_,_ in prepared]],capture_output=True)
    need(result.returncode==0,'Native compression batch completed')
    answer=[]
    for p,row,digest in prepared:
        after=storage.allocated(p);stat=p.stat()
        need(sha(p)==digest and stat.st_size==row['logicalBytes'] and stat.st_mtime_ns==row['mtimeNS'] and after<=row['allocatedBefore'],'Every original byte, size and timestamp unchanged, no allocated growth')
        answer.append(dict(row,sha256=digest,allocatedAfter=after,reclaimed=row['allocatedBefore']-after))
    return answer

def main():
    need(not OUT.exists(),'Fresh immutable compaction leaf')
    proof=ROOT/'audit_v4205_frozen_friendship_storage_sample/report.json'
    sample=json.loads(proof.read_text());need(sample['passed'] and sample['reclaimedAllocatedBytes']==41115648 and sample['deletedFiles']==0,'Actual successful bounded storage sample, counted separately once')
    for p,h in sample['inputHashes'].items():need(sha(p)==h,'Original sample bytes unchanged')
    literals=' -or '.join("$_.CommandLine -like '*"+name+"*'" for name in NAMES)
    q=subprocess.run(['powershell.exe','-NoProfile','-Command','Get-CimInstance Win32_Process -Filter "Name=\'mkport_candidate.exe\' OR Name=\'mkport.exe\' OR Name=\'mame.exe\' OR Name=\'hbmame.exe\'" | Where-Object { '+literals+' } | Select-Object ProcessId,Name | ConvertTo-Json -Compress'],capture_output=True,text=True)
    need(q.returncode==0 and not q.stdout.strip(),'No actual native process owns any selected frozen capture; excludes query process itself')
    pins={str(Path(__file__).resolve()):sha(__file__),str(Path(storage.__file__).resolve()):sha(storage.__file__),str(proof):sha(proof)}
    keep=(ROOT/'diagnostic_v1836_ball_register_boundary/mkport_candidate.exe',ROOT/current.NAME/'mkport_candidate.exe',ROOT/current.NAME/'roms/mk2ks/mk2ks.mdata',ROOT/'mame-mkp/mkport.exe',ROOT/'release_v1863_current_playtest/MK2_Kano_Sonya_v1836_CURRENT_PLAYTEST.zip',ROOT/'mame-mkp/src/mame/midway/midtunit_m.cpp',ROOT/'PLAY_CURRENT_V1836_CHECKED.cmd')
    pins.update({str(p.resolve()):sha(p) for p in keep})
    rows=[];skipped=0
    for name in NAMES:
        folder=ROOT/name;meta=folder/'result.json'
        need(folder.is_dir() and not folder.is_symlink() and json.loads(meta.read_text(encoding='utf-8-sig'))['exit_code']==0,'Exact original native capture terminal0')
        pins[str(meta.resolve())]=sha(meta)
        for p in folder.iterdir():
            if not p.is_file() or not (p.name=='run.log' or re.fullmatch(r'display_[a-z0-9_]+\.bin',p.name)):continue
            p=safe(p);stat=p.stat();before=storage.allocated(p)
            if stat.st_nlink!=1 or stat.st_size<131072 or before<=stat.st_size*.27:
                skipped+=1;continue
            rows.append(dict(path=str(p),logicalBytes=stat.st_size,allocatedBefore=before,mtimeNS=stat.st_mtime_ns))
    need(rows,'Non-vacuous still-reclaimable exact evidence files')
    OUT.mkdir();need(subprocess.run(['compact.exe','/C','/I','/Q','/S:'+str(OUT)],capture_output=True).returncode==0,'Ledger compressed before writes')
    (OUT/'plan.json').write_text(json.dumps(dict(names=NAMES,targets=rows,inputHashes=pins,skippedAlreadyCompactOrHardlinked=skipped,deletedFiles=0),indent=2)+'\n')
    print(f'Frozen evidence compaction: {len(rows)} exact files; active captures/builds excluded',flush=True)
    batches=[rows[i:i+48] for i in range(0,len(rows),48)];done=0;reclaimed=0;errors=[];tick=time.monotonic()
    with (OUT/'files.jsonl').open('x') as ledger,concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
        futures={pool.submit(batch,part):part for part in batches}
        for future in concurrent.futures.as_completed(futures):
            try:
                verified=future.result()
                for row in verified:ledger.write(json.dumps(row)+'\n')
                done+=len(verified);reclaimed+=sum(row['reclaimed'] for row in verified);ledger.flush()
            except Exception as error:
                errors.append(dict(paths=[r['path'] for r in futures[future]],error=repr(error)))
                ledger.write(json.dumps(dict(batchError=errors[-1]))+'\n');ledger.flush()
            if time.monotonic()-tick>=20:
                print(f'Verified {done} files; reclaimed {reclaimed/2**20:.1f} MiB; errors={len(errors)}',flush=True);tick=time.monotonic()
    need(all(sha(p)==h for p,h in pins.items()),'Protected playable/source/sample and original native result metadata unchanged')
    report=dict(passed=not errors,exactFilesSelected=len(rows),exactFilesVerified=done,errors=errors,inputHashes=pins,
      reclaimedAllocatedBytes=reclaimed,deletedFiles=0,newNativeMediaCopies=0,activeCapturesExcluded=True,originalPathsBytesSizesTimestampsPreserved=True,
      previousSampleReclamationNotCountedAgain=True,scope=__doc__,fullPortAcceptance=False,
      recovery='Native NTFS lossless compression. Original files are readable without manual decompression; compact /U /EXE reverses it.')
    (OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k!='inputHashes'},indent=2),flush=True)
    raise SystemExit(0 if report['passed'] else 1)

if __name__=='__main__':main()
