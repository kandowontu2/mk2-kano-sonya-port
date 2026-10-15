"""Distinguish current regression from retained stage observer/render differences.

Same original earned-control driver, no palette/reset observer hooks in either
run. Existing1836/current3172 executables only, full RGB in RAM; retain digests
and bounded differing-color diagnostics, not pixel/image/VRAM/audio dumps.
"""
import concurrent.futures
import hashlib
import json
import os
import re
import subprocess
import traceback
from pathlib import Path

import numpy as np
from PIL import Image
import run_current_stage_palette_pixels_v3602 as stage

ROOT, need, sha = stage.ROOT, stage.need, stage.sha
OUT = ROOT / 'audit_v3612_stage_snapshot_forensic'
OBSERVER = ROOT / 'mk2ks_stage_snapshot_forensic_v3604.lua'


def compare(actual, expected):
    mask = np.any(actual != expected, axis=2)
    positions = np.argwhere(mask)
    if not len(positions): return dict(pixels=0)
    pairs = np.concatenate((expected[mask], actual[mask]), axis=1)
    colors, counts = np.unique(pairs, axis=0, return_counts=True)
    indices = np.argsort(counts)[::-1][:12]
    return dict(pixels=len(positions), bboxYX=[positions.min(axis=0).tolist(), positions.max(axis=0).tolist()],
                differingColorPairs=[dict(referenceRGB=colors[i,:3].tolist(), actualRGB=colors[i,3:].tolist(),
                                           pixels=int(counts[i])) for i in indices],
                firstPixels=[dict(y=int(y),x=int(x),referenceRGB=expected[y,x].tolist(), actualRGB=actual[y,x].tolist())
                             for y,x in positions[:8]])


def capture(kind, guest, payload, old, refs):
    name = stage.NAME if kind == 'current' else 'diagnostic_v1836_ball_register_boundary'
    folder = ROOT / f'audit_v3611_{kind}_tomb_snapshot_forensic'
    need(not folder.exists(), 'Fresh forensic leaf, never restart/overwrite')
    candidate = ROOT / name
    build = json.loads((candidate / 'build-info.json').read_text(encoding='utf-8-sig'))
    files = {candidate / 'mkport_candidate.exe', candidate / 'roms/mk2ks/mk2ks.mdata', candidate / 'build-info.json',
             OBSERVER, *[ROOT / p for p in stage.LUA], Path(__file__).resolve(),
             stage.OLD_REPORT, stage.REFERENCE / 'run.log',
             ROOT / 'audit_v3598_current_kano_tomb_p1_palette_pixels/visible_frames.json',
             ROOT / 'audit_v3603_current_tomb_palette_pixels_checked/report.json',
             ROOT / 'mk2ks_native_stage_performer_v806.lua', ROOT / 'mk2ks_stage_branch_provenance_v1722.lua'}
    before = {str(p.resolve()): sha(p) for p in files}
    need(before[str(candidate / 'mkport_candidate.exe')] == build['executable_sha256'] and
         before[str(candidate / 'roms/mk2ks/mk2ks.mdata')] == build['payload_sha256'] and
         (candidate / 'roms/mk2ks/mk2ks.mdata').read_bytes() == payload, 'Existing matched forensic playable pair')
    folder.mkdir()
    result = subprocess.run(['compact.exe','/C','/I','/Q','/S:'+str(folder)],capture_output=True,text=True)
    need(result.returncode==0,'Lossless compressed small forensic leaf')
    (folder / 'input_hashes_before.json').write_text(json.dumps(before,indent=2)+'\n')
    env = {k:v for k,v in os.environ.items() if not re.match(r'^(MK2KS_|MK2_TRACE_|MK2_RANGE_|MK2_P2_)',k)}
    env.update(MK2KS_STAGE_SIDE='1',MK2KS_STAGE_WINNER='kano',MK2KS_STAGE_ARENA='1',MK2KS_STAGE_CASE='positive',
               MK2KS_STAGE_OUT=str(folder),MK2KS_STAGE_NO_HOOKS='1')
    cmd = [str(candidate/'mkport_candidate.exe'),'mk2ks','-rompath',str(candidate/'roms')+';'+str(ROOT/'roms'),
           '-samplepath',str(ROOT/'samples'),'-samples','-artpath',str(ROOT/'artwork'),'-skip_gameinfo','-nocheat',
           '-inipath',str(folder),'-video','none','-sound','none','-samplerate','48000','-noautoframeskip','-frameskip','0',
           '-nothrottle','-str','900','-snapsize','400x254','-cfg_directory',str(folder/'cfg'),'-nvram_directory',str(folder/'nvram'),
           '-snapshot_directory',str(folder/'snap'),'-autoboot_script',str(OBSERVER)]
    verified,diagnostics,errors=[],[],[]
    pins=dict(before)
    with (folder/'stderr.log').open('wb') as stderr, subprocess.Popen(cmd,cwd=ROOT,env=env,stdout=subprocess.PIPE,stderr=stderr) as process:
        print(f'{kind} forensic native PID={process.pid}; original physical controls, no hook observers',flush=True)
        with (folder/'run.log').open('w',encoding='utf-8') as log:
            for line in iter(process.stdout.readline,b''):
                if line.startswith(b'MK2_STAGE_TRANSFER_PIXELS '):
                    header=line.decode('ascii').strip();row=dict(re.findall(r'(\w+)=([^\s]+)',header))
                    encoded=process.stdout.readline().strip()
                    try:
                        need(len(verified)<537 and len(encoded)==812800 and int(row['frame'])==8174+len(verified),
                             'Complete native forensic RGB framing')
                        words=np.frombuffer(bytes.fromhex(encoded.decode('ascii')),dtype='>u4').reshape(254,400)
                        actual=np.stack([(words>>shift)&255 for shift in(16,8,0)],axis=2).astype(np.uint8)
                        path=stage.REFERENCE/'snap'/refs[len(verified)]['file'];wanted=old['inputHashes'][str(path)]
                        need(sha(path)==wanted,'Unchanged source-bound reference raster');pins[str(path)]=wanted
                        expected=np.asarray(Image.open(path).convert('RGB'))
                        difference=int(np.count_nonzero(np.any(actual!=expected,axis=2)))
                        frame=int(row['frame'])
                        if frame in (8174,8204,8217,8250,8493,8510,8680,8710):
                            diagnostics.append(dict(frame=frame,**compare(actual,expected)))
                        verified.append(dict(frame=frame,currentRGB_SHA256=hashlib.sha256(actual.tobytes()).hexdigest().upper(),
                            referenceRGB_SHA256=hashlib.sha256(expected.tobytes()).hexdigest().upper(),differingPixels=difference))
                        log.write(f'MK2_STAGE_FORENSIC_CHECKED frame={frame} differingPixels={difference}\n')
                    except Exception as error: errors.append(dict(header=header,error=repr(error)))
                else:
                    need(not re.search(b'^[A-F0-9]{1000}',line),'Raw RGB never written to forensic logs')
                    log.write(line.decode('utf-8',errors='strict'))
        code=process.wait()
    log=(folder/'run.log').read_text();stderr=(folder/'stderr.log').read_text()
    native_ok=code==0 and not errors and len(verified)==537 and (folder/'guest_maincpu.bin').read_bytes()==guest
    need(native_ok and not re.search(r'Lua error|LUA ERROR|stack traceback|Fatal error',log+stderr,re.I),
         'Native terminal and actual whole forensic guest, not fabricated RGB')
    baseline=(stage.REFERENCE/'run.log').read_text(encoding='utf-8-sig')
    actual_lines=stage.classic(log).splitlines()
    actual_lines=[line for line in actual_lines if not line.startswith('MK2_STAGE_FORENSIC_')]
    reference_lines=stage.classic(baseline).splitlines()
    need(len(actual_lines)==len(reference_lines),'All original physical/native record slots present')
    changed_records=[dict(index=i,reference=a,actual=b)for i,(a,b)in enumerate(zip(reference_lines,actual_lines))if a!=b]
    # These differences are diagnostic facts, not timing/position normalization
    # or acceptance of a weakened physical/visual oracle.
    provenance=lambda value:[line for line in value.splitlines()if line.startswith('MK2_STAGE_PROVENANCE_')]
    original_provenance=provenance(baseline);current_provenance=provenance(log)
    provenance_equal=current_provenance==original_provenance
    native=stage.native.check_log('\n'.join(actual_lines),'kano',1,1,'positive',certified_drop_log=stage.classic(baseline))
    for path,wanted in before.items(): need(sha(path)==wanted,'Actual forensic inputs unchanged')
    result=dict(captureCompleted=True,exit_code=code,candidate=name,kind=kind,frames=537,
                mismatchFrames=sum(r['differingPixels']>0 for r in verified),
                allPhysicalNativeProvenanceRecordsUnchanged=not changed_records and provenance_equal,
                physicalNativeRecordDifferences=changed_records,originalProvenanceExactlyRetained=provenance_equal,
                nativeInputStateGate=native,diagnosticFrames=diagnostics,
                paletteResetObserverHooksEnabled=False,rawImageAudioVRAMPlayableCopiesWritten=0,
                currentVisualAcceptance=False,fullPortAcceptance=False)
    (folder/'visible_frames.json').write_text(json.dumps(verified,indent=2)+'\n')
    (folder/'result.json').write_text(json.dumps(result,indent=2)+'\n')
    for file in folder.rglob('*'):
        if file.is_file():pins[str(file)]=sha(file)
    print(f'{kind}: terminal0, {result["mismatchFrames"]}/537 differ from heavy native reference',flush=True)
    return result,verified,pins


def run():
    need(not OUT.exists(),'Immutable diagnostic report')
    stage.controls()
    source=(ROOT/stage.LUA[2]).read_text()
    source=source.replace("tap(0xff80cf60,'actual palette hook entry',function(data)",
                          "if os.getenv('MK2KS_STAGE_NO_HOOKS')~='1' then\ntap(0xff80cf60,'actual palette hook entry',function(data)")
    source=source.replace("tap(0xff8bdfe0,'native earned Tomb begin',function()", "end\ntap(0xff8bdfe0,'native earned Tomb begin',function()")
    need(OBSERVER.read_text()==source,'Only read-only global hook exclusion switch added')
    current_guest,old_guest,current_payload,_,_=stage.inventory.current.expected_current()
    old_payload=(ROOT/'diagnostic_v1836_ball_register_boundary/roms/mk2ks/mk2ks.mdata').read_bytes()
    old=json.loads(stage.OLD_REPORT.read_text())
    need(sha(stage.OLD_REPORT)==json.loads(stage.LINEAGE.read_text())['inputHashes'][str(stage.OLD_REPORT)],'Reference lineage retained')
    refs=[dict(re.findall(r'(\w+)=([^\s]+)',line))for line in(stage.REFERENCE/'run.log').read_text(encoding='utf-8-sig').splitlines()
          if line.startswith('MK2_NAT_CAMPAIGN_FLOOR_SNAP ')]
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
        futures=[pool.submit(capture,kind,guest,payload,old,refs)for kind,guest,payload in
                 (('legacy',old_guest,old_payload),('current',current_guest,current_payload))]
        cases=[future.result()for future in futures]
    legacy,actual=cases
    old_current=json.loads((ROOT/'audit_v3598_current_kano_tomb_p1_palette_pixels/visible_frames.json').read_text())
    need([r['frame']for r in actual[1]]==[r['frame']for r in legacy[1]]==[r['frame']for r in old_current], 'All actual fields align without normalization')
    same_to_prior=sum(a['currentRGB_SHA256']==b['currentRGB_SHA256']for a,b in zip(actual[1],old_current))
    same_legacy_current=sum(a['currentRGB_SHA256']==b['currentRGB_SHA256']for a,b in zip(actual[1],legacy[1]))
    pins={}
    for _,_,values in cases:
        for file,wanted in values.items():
            need(file not in pins or pins[file]==wanted,'Consistent forensic actual inputs');pins[file]=wanted
    pins[str(stage.LINEAGE)]=sha(stage.LINEAGE)
    return dict(diagnosticCompleted=True,passed=True,cases=[item[0]for item in cases],
                actualCurrentFieldsEqualPriorHookObservedCapture=same_to_prior,
                actualLegacyFieldsEqualActualCurrent=same_legacy_current,
                currentHeaderGraphOrGuestPaletteChangeCauseProven=False,
                referenceHeavyObserverDifferencePresentInUnchangedLegacy=legacy[0]['mismatchFrames']>0,
                failed3605ComparisonAssumptionPreserved=True,
                oldFailedVerificationReport=str(ROOT/'audit_v3607_stage_snapshot_forensic/report.json'),
                newExecutableROMWAVPixelOrVRAMCopies=0,currentVisualAcceptance=False,
                fullPortAcceptance=False,inputHashes=pins,scope=__doc__)


if __name__=='__main__':
    try:report=run()
    except Exception as error:report=dict(passed=False,diagnosticCompleted=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
    need(not OUT.exists(),'Never overwrite diagnostic')
    OUT.mkdir();path=OUT/'report.json';path.write_text(json.dumps(report,indent=2)+'\n')
    before=sha(path);result=subprocess.run(['compact.exe','/C','/I','/Q',str(path)],capture_output=True,text=True)
    need(result.returncode==0 and sha(path)==before,'Lossless compact forensic report')
    print(json.dumps({k:v for k,v in report.items()if k not in('inputHashes','cases')},indent=2),flush=True)
    raise SystemExit(0 if report['passed']else 1)
