"""Exact-file source/choice audit compression, no raw media/build duplication."""
import json
import subprocess
from pathlib import Path
import seal_native_selector_knife_snapshot_storage as storage
import qualify_native_selector_sonya_startup_choices_bound as checked

ROOT,need,sha=storage.ROOT,storage.need,storage.sha
OUT=ROOT/'audit_native_selector_sonya_startup_choice_storage_checked.json'


def execute():
    need(not OUT.exists(),'Fresh immutable actual Sonya choice/storage inventory')
    path=checked.OUT/'report.json';report=json.loads(path.read_text())
    need(report['passed']and report['actualCurrentSourceNativeSonyaChoiceStreamAccepted']and
         len(report['effectiveSourceChoiceFaultsRejected'])==12 and
         report['actualNativeIdentity']['ProcessId']==32120 and
         report['actualNativeIdentity']['ParentProcessId']==38752 and
         report['actualNativeIdentity']['createdUnix']==1791766996.6480942 and report['nativeExit']==0,
         'Actual same original new terminal Sonya AI and complete twelve fault proof')
    files=set()
    for name in ('audit_native_selector_sonya_startup_choices_ram',
                 'audit_native_selector_sonya_startup_choices_capture_checked',
                 'audit_native_selector_sonya_startup_choices_checked',
                 'audit_native_selector_sonya_startup_choices_bound_checked'):
        folder=(ROOT/name).resolve();need(folder.is_dir()and folder.is_relative_to(ROOT.resolve()),'Exact new audit subtree')
        files.update(p.resolve()for p in folder.rglob('*')if p.is_file())
    for name in ('tools/capture_native_selector_sonya_startup_choices.py',
                 'tools/qualify_native_selector_sonya_startup_choices.py',
                 'tools/qualify_native_selector_sonya_startup_choices_bound.py',
                 'tools/seal_native_selector_sonya_startup_choice_storage.py',
                 'mk2ks_native_selector_sonya_startup_choices.lua'):
        files.add((ROOT/name).resolve())
    before={p:dict(sha256=sha(p),logicalBytes=p.stat().st_size,storedBefore=storage.stored(p))for p in files}
    for p in sorted(files):
        need(p.is_relative_to(ROOT.resolve())and p.suffix.lower()not in ('.exe','.zip','.wav','.png','.bin'),
             'Only exact source/audit/config/digest files, not builds or original media')
        call=subprocess.run(['compact.exe','/C','/EXE:LZX','/F','/I','/Q',str(p)],capture_output=True)
        need(call.returncode==0,'Exact source/audit file force-LZX succeeded')
    entries=[]
    for p,old in before.items():
        need(sha(p)==old['sha256'],'Every whole compressed source/evidence byte unchanged')
        entries.append(dict(path=str(p),**old,storedAfter=storage.stored(p)))
    pins=report['inputHashes'];need(all(sha(p)==h for p,h in pins.items()),'All full original current input pins rehashed after storage')
    endpoints={str(p):sha(p)for p in storage.source.FIXED}
    need(all(endpoints[str(p)]==h for p,h in storage.source.FIXED.items()),'Private candidate/public CMD/ZIP endpoints unchanged')
    value=dict(passed=True,goalStatus='active',files=entries,fullInputPins=len(pins),inputMismatches=0,
        logicalBytes=sum(r['logicalBytes']for r in entries),storedBefore=sum(r['storedBefore']for r in entries),
        storedAfter=sum(r['storedAfter']for r in entries),unchangedEndpoints=endpoints,
        actualSourceChoiceReportSHA256=sha(path),newBuilds=0,newROMCopies=0,newRawMediaFiles=0,newZIPs=0,
        deletions=0,allArenaCPUContextsAccepted=False,fullPortAcceptance=False)
    OUT.write_text(json.dumps(value,indent=2)+'\n')
    return value
