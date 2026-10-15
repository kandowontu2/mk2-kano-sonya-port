"""Compress exact new Ring audit sources/receipts only; verify full hashes.

No copies/builds/ROMs/raw media/ZIP/deletions. Retain original failures and
current exact compiled/public endpoints and all complete source input pins.
"""
import json
import subprocess
from pathlib import Path
import seal_native_selector_knife_snapshot_storage as prior
import seal_native_selector_cpu_rings_current_evidence as combined

ROOT,need,sha=prior.ROOT,prior.need,prior.sha
OUT=ROOT/'audit_native_selector_cpu_rings_storage_checked.json'


def execute():
    need(not OUT.exists(),'Fresh exact-file Ring storage receipt')
    files=set()
    for name in ('audit_native_selector_cpu_rings_snapshot_ram',
                 'audit_native_selector_cpu_rings_snapshot_capture_checked',
                 'audit_native_selector_cpu_rings_snapshot_transport_checked',
                 'audit_native_selector_cpu_rings_snapshot_renderer_checked',
                 'audit_native_selector_cpu_rings_snapshot_audio_checked',
                 'audit_native_selector_cpu_rings_snapshot_mechanics_checked',
                 'audit_native_selector_cpu_rings_snapshot_sealed',
                 'audit_native_selector_cpu_rings_native_branches_checked',
                 'audit_native_selector_cpu_rings_current_evidence_sealed'):
        folder=(ROOT/name).resolve();need(folder.is_relative_to(ROOT.resolve())and folder.is_dir(),'Exact existing new audit subtree')
        files.update(p.resolve()for p in folder.rglob('*')if p.is_file())
    for name in ('tools/capture_native_selector_cpu_rings_snapshot_ram.py',
                 'tools/qualify_native_selector_cpu_rings_snapshot_transport.py',
                 'tools/qualify_native_selector_cpu_rings_snapshot.py',
                 'tools/qualify_native_selector_cpu_rings_snapshot_audio.py',
                 'tools/qualify_native_selector_cpu_rings_snapshot_mechanics.py',
                 'tools/qualify_native_selector_cpu_rings_native_branches.py',
                 'tools/seal_native_selector_cpu_rings_snapshot.py',
                 'tools/seal_native_selector_cpu_rings_current_evidence.py',
                 'tools/seal_native_selector_cpu_rings_storage.py',
                 'tools/read_native_selector_cpu_rings_snapshot_frames.py',
                 'tools/read_native_selector_cpu_rings_snapshot_frames_remote.py',
                 'mk2ks_native_selector_cpu_rings_snapshot_ram.lua',
                 'audit_native_selector_cpu_ring_1_snapshot_actual_views.json',
                 'audit_native_selector_cpu_ring_2_snapshot_actual_views.json',
                 'audit_native_selector_cpu_ring_3_snapshot_actual_views.json'):
        files.add((ROOT/name).resolve())
    path=combined.OUT/'report.json';report=json.loads(path.read_text());need(report['passed'],'Finite combined evidence exists')
    before={p:dict(sha256=sha(p),logicalBytes=p.stat().st_size,storedBefore=prior.stored(p))for p in files}
    for p in sorted(files):
        need(p.is_relative_to(ROOT.resolve())and p.suffix.lower()not in ('.exe','.zip','.wav','.png','.bin'),
             'Exact source/config/audit/digest files only, never original media')
        result=subprocess.run(['compact.exe','/C','/EXE:LZX','/F','/I','/Q',str(p)],capture_output=True)
        need(result.returncode==0,'Exact file force-LZX succeeded')
    entries=[]
    for p,old in before.items():
        need(sha(p)==old['sha256'],'Whole compressed source/evidence byte hash unchanged')
        entries.append(dict(path=str(p),**old,storedAfter=prior.stored(p)))
    pins=report['inputHashes'];need(all(sha(p)==h for p,h in pins.items()),'All whole original input pins after compression')
    endpoints={str(p):sha(p)for p in prior.source.FIXED}
    need(all(endpoints[str(p)]==h for p,h in prior.source.FIXED.items()),'Private candidate/public CMD/older ZIP unchanged')
    value=dict(passed=True,goalStatus='active',files=entries,fullInputPins=len(pins),inputMismatches=0,
        logicalBytes=sum(r['logicalBytes']for r in entries),storedBefore=sum(r['storedBefore']for r in entries),
        storedAfter=sum(r['storedAfter']for r in entries),unchangedEndpoints=endpoints,
        finiteCombinedReportSHA256=sha(path),newBuilds=0,newROMCopies=0,newRawMediaFiles=0,newZIPs=0,
        deletions=0,fullPortAcceptance=False)
    OUT.write_text(json.dumps(value,indent=2)+'\n')
    return value
