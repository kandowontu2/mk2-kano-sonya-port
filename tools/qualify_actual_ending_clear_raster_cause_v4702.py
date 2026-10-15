"""Qualify the actual single clear-field cause, not whole-ending video.

All raw pixel/VRAM comparisons were performed in RAM by the pinned fresh
native capture. This offline qualification checks its complete actual beam
ledger, hardware/source timing, independent84pixel arithmetic and real-row
counterexamples. No new native capture, image fabrication or game mutation.
"""
import copy,json,re,subprocess,traceback
from pathlib import Path
import qualify_ending_clear_projection_source_v4694 as source
import ending_clear_beam_projection_v4688 as projection
ROOT,need,sha=source.ROOT,source.need,source.sha
OUT=ROOT/'audit_v4703_actual_ending_clear_raster_cause_checked'

def run():
    need(not OUT.exists(),'Fresh immutable actual raster-cause qualification')
    paths=[ROOT/'audit_v4697_kano_ending_clear_projection_observed/report.json',
           ROOT/'audit_v4695_ending_clear_projection_source_checked/report.json',
           ROOT/'audit_v4684_kano_ending_clear_beam_probe_observed/report.json']
    actual,preflight,prior=[json.loads(p.read_text())for p in paths]
    need(actual['passed']and actual['actualFields']==21 and actual['everyOriginalColdEventAndRGBUnchanged']and
         actual['rawMediaFilesWritten']==0 and not actual['fullEndingRendererVideoAccepted'],
         'Actual fresh native full21field observation, full cold policy unchanged, no whole-ending shortcut')
    need(preflight['passed']and len(preflight['actualBeamLedgerFaultsRejected'])==5 and prior['passed'],
         'Executed whole source/partial-update gates and actual previous beam faults retained')
    source.source_boundary()
    capture=Path(actual['capture']);meta=json.loads((capture/'result.json').read_text())
    need(meta['exit_code']==0 and meta['nativeGuestBytesVerifiedInRAM']==1048576 and
         meta['actualNativeFrameCallbacks']==58 and meta['actualEndingLatchProbeFields']==21 and
         meta['ramGuestSHA256']=='938D380B3E2CE8DF6A688E2DC64C576CC7A1E554AE341E7B42463129FA5CA821'and
         meta['rawRasterFilesWritten']==meta['guestDumpFilesWritten']==meta['raw_audio_files_written']==0,
         'Actual complete terminal0 guest and original58RGB, raw media only in RAM')
    record=actual['actualClearProjection'];native=record['native'];beam=[]
    # Bound exact native tag/frame, never an event-index or address substring.
    with(capture/'run.log').open()as stream:
        for line in stream:
            if line.startswith('MK2_ENDING_PROBE_CPU_BUCKET frame=58183 '):
                beam.append(dict(re.findall(r'(\w+)=([^\s]+)',line)))
    projection.validate(native,beam)
    need(beam==[b for b in prior['actualCPUBuckets']if b['frame']=='58183'],
         'Fresh and preceding actual cold probes have identical entire260bucket CPU/beam ledger')
    p=record['actualBeamProjection'];end=record['currentRequestedStart']
    need(p['sourceNativeCPUWrites']==67658 and p['exactEndVRAMWords']==262144 and
         p['actualVisibleRows']==254 and p['mismatchedPixels']==0 and p['firstMismatch']is None and
         p['projectedRGBSHA256']==p['actualRGBSHA256']==end['actualRGBSHA256']and
         p['diagnosticOnePrecedingVRAMBaseOnly']and not p['fullEndingRendererVideoAccepted']and
         end['mismatchedPixels']==84 and end['firstMismatch']==[0,356],
         'Every actual end word and every actual source-timed pixel exact; original static84pixel counterexample preserved')
    # Derive the three still-visible tail lengths solely from actual CPU
    # stores preceding each original scanline partial update, not RGB search.
    counts={}
    for b in beam:
        if b['pc']=='FF80F550':counts[int(b['beam'])]=int(b['count'])
    clear=0;tails=[]
    for row in range(254):
        current=20+row;clear+=counts.get(current-1,0)*2
        old=max(0,min(400,row*512+56+400-clear))
        if old:tails.append(dict(row=row,firstColumn=400-old,pixels=old,clearedWordsBeforePartialUpdate=clear))
    need([(r['row'],r['firstColumn'],r['pixels'])for r in tails]==[(0,356,44),(1,372,28),(2,388,12)]and
         sum(r['pixels']for r in tails)==end['mismatchedPixels'],
         'All84 stale tail pixels independently explained by paired writes and original partial-update timing')
    faults=[]
    def reject(label,n=native,b=beam):
        try:projection.validate(n,b)
        except ValueError as error:faults.append(dict(kind=label,rejectedBy=str(error)))
        else:raise ValueError('Actual beam/native counterexample admitted '+label)
        projection.validate(native,beam)
    for key,value in(('frame','58184'),('age','1888'),('identity','18'),('side','1'),('writes','1'),
                      ('assistance','forced'),('origin','56297'),('start','EFFC'),('dpyadr','E01C'),
                      ('control','F000'),('tap','001D'),('vcount','272'),('vsblnk','275'),('veblnk','21')):
        bad=dict(native);bad[key]=value;reject('actual_context_'+key,n=bad)
    for key,value in(('beam','18'),('dpyadr','0000'),('mask','00FF'),('count','1'),('pc','FFF00000'),
                      ('value','3F00'),('first','001FE010'),('last','001FE000'),('identity','18')):
        bad=copy.deepcopy(beam);need(bad[0][key]!=value,'Non-vacuous actual bucket fault');bad[0][key]=value
        reject('actual_bucket_'+key,b=bad)
    reject('missing_actual_bucket',b=beam[1:]);reject('duplicated_actual_bucket',b=beam+[beam[0]])
    pins={}
    for proof in(actual,preflight,prior):
        for path,h in proof['inputHashes'].items():
            need(path not in pins or pins[path]==h,'Consistent actual native/source proof inputs');pins[path]=h
    for path in paths+[Path(__file__).resolve(),Path(projection.__file__).resolve(),Path(source.__file__).resolve()]:pins[str(path)]=sha(path)
    need(all(sha(path)==h for path,h in pins.items()),'Every actual native/source input unchanged')
    return dict(passed=True,inputHashes=pins,actualNativeExit=0,actualBeamBuckets=len(beam),
      actualNativeCPUWrites=67658,exactActualEndVRAMWords=262144,exactActualRGBPixels=254*400,
      independentSourceTimingTails=tails,actualBeamAndContextFaultsRejected=faults,
      singleFieldSourceTimingCauseAccepted=True,wholeEndingSingleInitialBaseAccepted=False,
      actualRawPixelBitFaultsQualified=False,fullEndingRendererVideoAccepted=False,fullPortAcceptance=False,
      newBuilds=0,rawMediaFilesWritten=0,scope=__doc__)

if __name__=='__main__':
    try:report=run()
    except Exception as error:report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
    OUT.mkdir();need(subprocess.run(['compact.exe','/C','/I','/Q','/S:'+str(OUT)],capture_output=True).returncode==0,'Compressed before writes')
    (OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items()if k not in('inputHashes','actualBeamAndContextFaultsRejected')},indent=2),flush=True)
    raise SystemExit(0 if report['passed']else 1)
