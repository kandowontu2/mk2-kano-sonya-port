"""Release only the qualified original terminal coordinate campaign's RAM.

No native game stop/restart, source deletion or raw-media copies. The actual
dirty canonical files must already be restored by the newer layer build.
"""
import hashlib,json,os,sys
from pathlib import Path
import read_live_shang_drain_frames as identity
import verify_native_selector_layers_startup as current

ROOT=current.ROOT
OUT=ROOT/'audit_native_shang_anchor_terminal_ram_retirement'


def retire(ram):
    need,sha=current.initial.need,current.initial.sha
    need(not OUT.exists()and os.getpid()==3232 and os.getppid()==18840 and
         ram['process'].poll()==0 and not identity.identity.census(),'Exact retained host, original native game actually terminal, no other native game live')
    host=next(p for p in identity.census_hosts()if p['ProcessId']==os.getpid())
    need(host['createdUnix']==1791725456.1323967 and host['ParentProcessId']==18840 and
         Path(host['ExecutablePath']).resolve()==Path(sys.executable).resolve()and
         host['CommandLine']=='"'+sys.executable+'" -B tools/capture_native_shang_drain_anchors_campaign.py',
         'Exact original actual kernel host birth/path/parent/full command')
    build=ROOT/current.NAME
    restore_path=build/'restoration.json';cache_path=build/'cache_retirement.json'
    restored=json.loads(restore_path.read_text(encoding='utf-8-sig'));cache=json.loads(cache_path.read_text(encoding='utf-8-sig'))
    need(restored['passed']and restored['native_build_exit']==0 and cache['passed']and cache['nativeCompilerExit']==0 and
         cache['cacheAbsent']and not(ROOT/'mame-mkp/build/mingw-gcc').exists()and
         all(sha(p)==h for p,h in restored['restored_actual_preexisting_files'].items()),'Newer native compiler actually terminal, ALL original dirty files restored, generated cache absent')
    proof_path=ROOT/'audit_native_shang_anchor_terminal_checked/report.json';proof=json.loads(proof_path.read_text())
    need(proof==ram['terminalRecoveryReport']and proof['passed']and proof['finiteSonyaNormalShrinkingCrashAndOrdinaryRecoveryAccepted']and
         proof['sameOriginalNativeTerminal']and proof['nativeExit']==0 and proof['actualNativeIdentity']==ram['identity']and
         ram['identity']['ProcessId']==32016 and ram['identity']['ParentProcessId']==3232 and
         ram['identity']['createdUnix']==1791725473.170992 and not proof['fullPortAcceptance']and
         all(sha(p)==h for p,h in proof['inputHashes'].items()),'Actual complete terminal chronology/recovery evidence, all frozen inputs intact')
    captured=ram['capture'];text=captured['text'];images=len(captured['images'])
    need(len(text)==531553100 and images==45,'Exact original RAM ownership and qualified bounded rasters')
    hashed=hashlib.sha256()
    for first in range(0,len(text),1048576):hashed.update(text[first:first+1048576].encode())
    need(hashed.hexdigest().upper()==proof['wholeTerminalChronologySHA256'],'Entire original held chronology still equals already-qualified original terminal GZIP')
    report=dict(passed=True,qualifiedReceiptSHA256=sha(proof_path),originalNativeIdentity=ram['identity'],nativeExit=0,
        actualHostIdentity=host,releasedChronologyBytes=len(text),releasedRasterCount=images,RAMDictionaryCleared=True,
        normalHostExitRequired=True,actualNewerCompilerTerminalAndCanonicalRestorationVerified=True,
        inputHashes={str(p.resolve()):sha(p)for p in (Path(__file__),proof_path,restore_path,cache_path)},
        sourceAndEvidenceFilesDeleted=0,newNativeBoots=0,newROMCopies=0,newRawMedia=0,
        publicPlayableChanged=False,fullPortAcceptance=False,goalStatus='active')
    OUT.mkdir();ram.clear();(OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(passed=True,releasedChronologyBytes=len(text),releasedRasterCount=images,normalHostExitRequired=True)),flush=True)
    return report
