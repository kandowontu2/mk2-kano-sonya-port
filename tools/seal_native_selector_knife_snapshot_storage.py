"""Exact new audit files only, force LZX and verify every whole byte hash.

No builds/ROM/raw media/ZIP copies/deletions; full source/evidence pins and
private/public endpoints checked after compression. Original RAM host retained.
"""
import ctypes
import json
import subprocess
from pathlib import Path
import verify_native_source_sync as source

ROOT,need,sha=source.ROOT,source.need,source.sha
OUT=ROOT/'audit_native_selector_knife_snapshot_storage_checked.json'


def stored(path):
    high=ctypes.c_uint32();function=ctypes.windll.kernel32.GetCompressedFileSizeW
    function.argtypes=(ctypes.c_wchar_p,ctypes.POINTER(ctypes.c_uint32));function.restype=ctypes.c_uint32
    low=function(str(path),ctypes.byref(high));need(low!=0xffffffff,'Actual exact Win32 stored file bytes')
    return (high.value<<32)|low


def execute():
    need(not OUT.exists(),'Fresh immutable storage/source receipt')
    files=set()
    for folder in (
        'audit_native_selector_walkin_knife_display_ram',
        'audit_native_selector_walkin_knife_display_capture_checked',
        'audit_native_selector_walkin_knife_display_renderer_checked',
        'audit_native_selector_walkin_knife_display_initialized_checked',
        'audit_native_selector_walkin_knife_display_face_rows_checked',
        'audit_native_selector_walkin_knife_vram_checked',
        'audit_native_selector_walkin_knife_snapshot_ram',
        'audit_native_selector_walkin_knife_snapshot_capture_checked',
        'audit_native_selector_walkin_knife_snapshot_renderer_checked',
        'audit_native_selector_walkin_knife_snapshot_sealed'):
        at=(ROOT/folder).resolve();need(at.is_relative_to(ROOT.resolve()) and at.is_dir(),'Exact audit subtree')
        files.update(p.resolve() for p in at.rglob('*') if p.is_file())
    for name in (
        'tools/capture_native_selector_walkin_knife_display_ram.py',
        'tools/qualify_native_selector_walkin_knife_display_ram.py',
        'tools/qualify_native_selector_walkin_knife_display_initialized.py',
        'tools/qualify_native_selector_walkin_knife_display_face_rows.py',
        'tools/qualify_native_selector_walkin_knife_vram.py',
        'tools/capture_native_selector_walkin_knife_snapshot_ram.py',
        'tools/qualify_native_selector_walkin_knife_snapshot.py',
        'tools/seal_native_selector_walkin_knife_snapshot.py',
        'tools/read_native_selector_knife_snapshot_frames.py',
        'tools/read_native_selector_knife_snapshot_frames_remote.py',
        'tools/seal_native_selector_knife_snapshot_storage.py',
        'mk2ks_native_selector_walkin_knife_display_ram.lua',
        'mk2ks_native_selector_walkin_knife_snapshot_ram.lua',
        'audit_native_selector_walkin_knife_existing_visuals.json',
        'audit_native_selector_walkin_knife_snapshot_actual_views.json'):
        files.add((ROOT/name).resolve())
    sealed=ROOT/'audit_native_selector_walkin_knife_snapshot_sealed/report.json'
    report=json.loads(sealed.read_text());need(report['passed'],'Full finite display proof exists')
    before={p:dict(sha256=sha(p),logicalBytes=p.stat().st_size,storedBefore=stored(p))for p in files}
    for p in sorted(files):
        need(p.is_relative_to(ROOT.resolve()) and p.suffix.lower() not in ('.exe','.zip','.wav','.png','.bin'),
             'Only exact small source/audit/config/digest trace files, never original media')
        call=subprocess.run(['compact.exe','/C','/EXE:LZX','/F','/I','/Q',str(p)],capture_output=True)
        need(call.returncode==0,'Exact file force-LZX succeeded')
    entries=[]
    for p,old in before.items():
        need(sha(p)==old['sha256'],'Whole bytes unchanged after LZX')
        entries.append(dict(path=str(p),**old,storedAfter=stored(p)))
    pins=report['inputHashes'];need(all(sha(p)==h for p,h in pins.items()),'All full original source/evidence pins after compression')
    endpoints={str(p):sha(p)for p in source.FIXED}
    need(all(endpoints[str(p)]==h for p,h in source.FIXED.items()),'Private current and public old CMD/ZIP endpoints unchanged')
    value=dict(passed=True,goalStatus='active',files=entries,fullInputPins=len(pins),inputMismatches=0,
        logicalBytes=sum(r['logicalBytes']for r in entries),storedBefore=sum(r['storedBefore']for r in entries),
        storedAfter=sum(r['storedAfter']for r in entries),unchangedEndpoints=endpoints,
        finiteRendererReportSHA256=sha(sealed),newBuilds=0,newROMCopies=0,newRawMediaFiles=0,newZIPs=0,
        deletions=0,fullPortAcceptance=False)
    OUT.write_text(json.dumps(value,indent=2)+'\n')
    return value


if __name__=='__main__':
    r=execute();print(json.dumps({k:v for k,v in r.items()if k not in ('files','unchangedEndpoints')},indent=2))
