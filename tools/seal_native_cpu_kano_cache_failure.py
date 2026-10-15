"""Freeze the actual corrupting run before any source or controller changes."""
import gzip,json,subprocess
from pathlib import Path
import native_ai_response_context as native
import native_process_census_v6647 as census
ROOT,need,sha=native.ROOT,native.need,native.sha
if __name__=='__main__':
    folder=ROOT/'audit_native_sonya_p1_postending_kano_anchors_checked'
    out=folder/'cache_failure_preserved.json'
    need(not out.exists() and not census.census(),'Actual native terminal; fresh preservation')
    terminal=json.loads((folder/'native_terminal.json').read_text())
    stop=json.loads((folder/'explicit_confirmed_cache_failure_stop.json').read_text())
    pins=json.loads((folder/'input_hashes_before.json').read_text())
    need(terminal['nativeExit']==stop['nativeExit']==0xffffffff and
         len(stop['actualGlobalOverrunEvents'])==146,'Actual confirmed corrupting run explicitly stopped')
    need(all(sha(p)==h for p,h in pins.items()),'All executed inputs unchanged before preservation')
    sources={p:dict(sha256=h,text=Path(p).read_text()) for p,h in pins.items()
             if Path(p).suffix.lower() in ('.py','.lua','.cpp','.h','.cmd')}
    archive=folder/'original_corrupting_executed_sources.json.gz'
    with gzip.open(archive,'wt',encoding='utf-8') as stream:json.dump(sources,stream)
    out.write_text(json.dumps(dict(passed=False,confirmedNativeGraphicsCorruption=True,
        nativeExit=terminal['nativeExit'],observedGlobalStores=146,originalInputHashes=pins,
        sourceArchiveSHA256=sha(archive),sourceArchiveEntries=len(sources),
        fullPortAcceptance=False,goalStatus='active'),indent=2)+'\n')
    for p in folder.iterdir():
        if p.is_file():subprocess.run(['compact.exe','/C','/EXE:LZX','/F','/I','/Q',str(p)],check=True,capture_output=True)
    print(json.dumps(dict(preserved=True,sources=len(sources),globalStores=146)))
