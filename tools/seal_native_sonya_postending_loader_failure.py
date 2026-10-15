"""Preserve exact failed test-loader inputs before correcting the anchor."""
import gzip,json,subprocess
from pathlib import Path
import native_ai_response_context as native
import native_process_census_v6647 as census
ROOT,need,sha=native.ROOT,native.need,native.sha
if __name__=='__main__':
    folder=ROOT/'audit_native_sonya_p1_postending_kano'
    out=folder/'loader_failure_preserved.json'
    need(not out.exists() and not census.census(),'Actual failed child terminal before any editing/retry')
    terminal=json.loads((folder/'native_terminal.json').read_text())
    pins=json.loads((folder/'input_hashes_before.json').read_text())
    error=(folder/'stderr.log').read_text()
    need(terminal['nativeExit']==3 and 'One exact verified source boundary' in error and
         not (folder/'guest_memory_proof.json').exists(),'Actual pre-frame script-loader failure, no game/guest success')
    need(all(sha(p)==h for p,h in pins.items()),'Every original failed run input still unchanged before correction')
    sources={p:dict(sha256=h,text=Path(p).read_text()) for p,h in pins.items() if Path(p).suffix in ('.py','.lua')}
    with gzip.open(folder/'original_failed_executed_sources.json.gz','wt',encoding='utf-8') as stream:json.dump(sources,stream)
    for p in folder.iterdir():
        if p.is_file():subprocess.run(['compact.exe','/C','/EXE:LZX','/F','/I','/Q',str(p)],check=True,capture_output=True)
    out.write_text(json.dumps(dict(passed=False,failedLoaderPreserved=True,nativeExit=3,
        nativeGuestAccepted=False,gameBugClaim=False,fullPortAcceptance=False,goalStatus='active',
        reason='New test wrapper expected read(a), while the immutable guard base uses read(*a).',
        originalInputHashes=pins,actualNativeIdentity=terminal['identity']),indent=2)+'\n')
    print(json.dumps(dict(preserved=True,nativeExit=3,nativeGuestAccepted=False)))
