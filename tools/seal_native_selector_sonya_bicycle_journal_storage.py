"""Seal full finite Bicycle proofs; exact audit-only LZX and unchanged releases.

Retain actual rejected sources/results, complete independent source hashes,
original terminal native handle, and the full original goal requirements.
No media/build copies, gameplay mutation, native restart, or broad acceptance.
"""
import json
import subprocess
from pathlib import Path
import qualify_native_selector_sonya_bicycle_complete_journal as lifecycle
import seal_native_selector_knife_snapshot_storage as storage
import read_live_shang_drain_frames as census

ROOT,need,sha=lifecycle.ROOT,lifecycle.need,lifecycle.sha
OUT=ROOT/'audit_native_selector_sonya_bicycle_journal_storage_checked.json'


def execute():
    need(not OUT.exists(),'Fresh immutable complete Bicycle storage receipt')
    parent=lifecycle.OUT/'report.json';proof=json.loads(parent.read_text())
    operand_path=lifecycle.operands.OUT/'report.json';operands=json.loads(operand_path.read_text())
    capture=lifecycle.capture;held=capture.NATIVE_HANDLES[capture.KEY]
    host=next(r for r in census.census_hosts()if r['ProcessId']==38752)
    need(host['ParentProcessId']==40316 and host['createdUnix']==1791734919.6266766 and
         host['CommandLine']=='"'+host['ExecutablePath']+'" -B tools/capture_native_selector_special_shadow.py',
         'Exact original live host retained, not a replacement process')
    need(held['process'].poll()==proof['nativeExit']==0 and held['identity']==proof['actualNativeIdentity']==
         operands['actualNativeIdentity'] and not capture.base.choices.current.prior.identity.census(),
         'Same exact native42616 terminal handle and fresh empty native census')
    need(proof['passed'] and proof['finiteBicycleLifecycleAccepted'] and operands['passed'] and
         proof['wholeCurrentBicycleLifecycle']['sourceOperandHorizontalJournal']==
         operands['wholeCurrentBicycleHorizontalOperands'],
         'Cached exact pure parser preserves every original positive operand/replay result')
    need(len(proof['effectiveLifecycleFaultsRejected'])==10 and
         len(operands['effectiveOperandFaultsRejected'])==14 and
         len(operands['effectiveBoundarySourceFaultsRejected'])==7,
         'All31 effective lifecycle, full-operand and exact gateway source faults rejected')
    pins=dict(proof['inputHashes'])
    for p in (Path(__file__),parent,operand_path):
        key=str(p.resolve());h=sha(p);need(key not in pins or pins[key]==h,'No immutable evidence/source replaced');pins[key]=h
    need(all(sha(p)==h for p,h in pins.items()),'Every whole original source/native/evidence input pin intact')
    files=set()
    for folder in ('audit_native_selector_sonya_horizontal_operands_ram',
                   'audit_native_selector_sonya_horizontal_operands_capture_checked',
                   'audit_native_selector_sonya_horizontal_operands_checked',
                   'audit_native_selector_sonya_horizontal_operands_bound_checked',
                   'audit_native_selector_sonya_horizontal_operands_gateway_checked',
                   'audit_native_selector_sonya_bicycle_complete_journal_checked'):
        at=(ROOT/folder).resolve();need(at.is_relative_to(ROOT.resolve())and at.is_dir(),'Exact new audit subtree')
        files.update(p.resolve()for p in at.rglob('*')if p.is_file())
    for name in ('mk2ks_native_selector_sonya_horizontal_operands.lua',
                 'tools/capture_native_selector_sonya_horizontal_operands.py',
                 'tools/qualify_native_selector_sonya_horizontal_operands.py',
                 'tools/qualify_native_selector_sonya_horizontal_operands_bound.py',
                 'tools/qualify_native_selector_sonya_horizontal_operands_gateway.py',
                 'tools/qualify_native_selector_sonya_bicycle_complete_journal.py',
                 'tools/seal_native_selector_sonya_bicycle_journal_storage.py'):
        files.add((ROOT/name).resolve())
    before={p:dict(sha256=sha(p),logicalBytes=p.stat().st_size,storedBefore=storage.stored(p))for p in files}
    for p in sorted(files):
        need(p.is_relative_to(ROOT.resolve()) and p.suffix.lower() not in ('.exe','.zip','.wav','.png','.bin'),
             'Exact source/audit/config/digest only; original raw media untouched')
        call=subprocess.run(['compact.exe','/C','/EXE:LZX','/F','/I','/Q',str(p)],capture_output=True)
        need(call.returncode==0,'Exact individual audit force-LZX succeeded')
    entries=[]
    for p,old in before.items():
        need(sha(p)==old['sha256'],'Whole bytes unchanged after exact LZX')
        entries.append(dict(path=str(p),**old,storedAfter=storage.stored(p)))
    need(all(sha(p)==h for p,h in pins.items()),'Every full source/evidence pin freshly rehashed after compression')
    source_sync=storage.source.verify()
    need(source_sync['passed'],'Whole canonical compiled source and unchanged public/private endpoints')
    endpoints={str(p):sha(p)for p in storage.source.FIXED}
    need(all(endpoints[str(p)]==h for p,h in storage.source.FIXED.items()),'Public old CMD/ZIP and current EXE/payload/build unchanged')
    value=dict(passed=True,goalStatus='active',actualNativeIdentity=held['identity'],nativeExit=0,
        actualHostIdentity=host,cachedPureParserWholeOperandResultIdentical=True,
        finiteBicycleLifecycleReportSHA256=sha(parent),completeOperandReportSHA256=sha(operand_path),
        effectiveFaultsRejected=31,files=entries,inputHashes=pins,fullInputPins=len(pins),inputMismatches=0,
        logicalBytes=sum(r['logicalBytes']for r in entries),storedBefore=sum(r['storedBefore']for r in entries),
        storedAfter=sum(r['storedAfter']for r in entries),unchangedEndpoints=endpoints,
        requirements=proof['requirements'],remainingGroups=proof['remainingGroups'],
        wholeSourceSyncPassed=True,newNativeGames=0,newBuilds=0,newROMCopies=0,newRawMediaFiles=0,
        newZIPs=0,deletions=0,allArenaCPUContextsAccepted=False,fullPortAcceptance=False)
    OUT.write_text(json.dumps(value,indent=2)+'\n')
    digest=sha(OUT)
    call=subprocess.run(['compact.exe','/C','/EXE:LZX','/F','/I','/Q',str(OUT)],capture_output=True)
    need(call.returncode==0 and sha(OUT)==digest,'Entire final storage receipt compressed without changing bytes')
    return value
