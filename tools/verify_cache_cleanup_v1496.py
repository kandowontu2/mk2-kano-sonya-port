"""Independently verify exact obsolete cache deletion and retained builds."""
import json,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'audit_v1496_old_compiler_cache_cleanup_checked'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest().upper()
def verify():
 folder=ROOT/'audit_v1495_old_compiler_cache_cleanup';before=json.loads((folder/'before.json').read_text(encoding='utf-8-sig'));after=json.loads((folder/'report.json').read_text(encoding='utf-8-sig'))
 assert after['passed'] and before['cacheFiles']==after['removedFiles'] and len(before['cacheFiles'])==8
 expected={ROOT/'mame-mkp/build/mingw-gcc/bin/x64/Release'/name for name in('mame_mkprobe','mame_mkwport')}
 assert {Path(p)for p in after['removedDirectories']}==expected and all(not p.exists()for p in expected)
 assert all(Path(p['path']).parent in expected and not Path(p['path']).exists()for p in before['cacheFiles'])
 for p,h in before['keptHashes'].items():assert sha(Path(p))==h
 for item in after['logs']:assert sha(Path(item['path']))==item['sha256'] and item['allocatedBefore']==item['allocatedAfter']
 # PowerShell Measure-Object on ordered dictionaries returned null. Sum the
 # captured individual file lengths, rather than treating null as zero.
 cache_bytes=sum(item['bytes']for item in before['cacheFiles']);assert cache_bytes==22678330
 pins={str(p.resolve()):sha(p)for p in(folder/'before.json',folder/'report.json',folder/'compaction.log',Path(__file__),ROOT/'tools/clean_obsolete_compiler_caches_v1495.ps1')}
 pins.update(before['keptHashes'])
 return dict(passed=True,removedDirectories=[str(p)for p in sorted(expected)],removedLogicalCacheBytes=cache_bytes,removedFiles=8,keptBuildsAndCurrentCMDUnchanged=True,logContentsUnchanged=True,logAdditionalAllocatedBytesReclaimed=0,logCompaction='Already NTFS compressed; command skipped them, no additional space reclaimed',recovery='The deleted compiler libraries regenerate from retained source. Playable executables and sources were not deleted.',allOldBuildFoldersDeleted=False,inputHashes=pins)
if __name__=='__main__':
 assert not OUT.exists();report=verify();OUT.mkdir();(OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:report[k]for k in('passed','removedLogicalCacheBytes','removedFiles','logAdditionalAllocatedBytesReclaimed')}),flush=True)
