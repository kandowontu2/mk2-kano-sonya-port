"""Whole independent hardware ledger bound to actual current native P1 pixels.

Every original operation, source-cycle, instruction, per-field RAM agreement,
27 actual metadata faults and eight terminal faults remain. No dummy VRAM,
post-exit pixels, guest writes or campaign-policy changes.
"""
import argparse,gzip,inspect,json,subprocess,textwrap,traceback
from pathlib import Path
from types import SimpleNamespace
import verify_complete_native_ending_pixels_hardware_v4757 as original
import ending_raster_cpu_cycle_model_v4740 as p1
import current_payload_metadata_context_v5229 as current
import qualify_ending_display_latch_source_v4647 as window
ROOT,need,sha=current.ROOT,current.need,current.sha

# The identical qualified metadata-only adapter omits only indexed sampling.
# Pixel acceptance remains a separate mandatory actual whole RAM proof.
advance=textwrap.dedent(inspect.getsource(original.model.Scanline.advance))
for before,after in original.previous.changes:
    need(advance.count(before)==1,'Only original indexed sampling omitted')
    advance=advance.replace(before,after,1)
advance_scope=dict(p1.Scanline.advance.__globals__)
exec(compile(advance,__file__+'::whole_original_metadata_advance_P1','exec'),advance_scope)
class Ledger(p1.Scanline):
    advance=advance_scope['advance']
hardware_model=SimpleNamespace(**dict(vars(original.model),
    __file__=p1.__file__,parse=p1.parse,Scanline=p1.Scanline,
    previous=SimpleNamespace(previous=SimpleNamespace(validate_context=p1.validate_context))))
contract_scope=dict(vars(original.previous),model=hardware_model,Ledger=Ledger)
exec(compile(original.contract_source,__file__+'::entire_original_terminal_contract_P1','exec'),contract_scope)
contract=contract_scope['contract']
boundary_scope=dict(original.terminal_boundary.__globals__,model=hardware_model)
exec(compile(inspect.getsource(original.terminal_boundary),
    __file__+'::entire_original_terminal_boundary_P1','exec'),boundary_scope)
terminal_boundary=boundary_scope['terminal_boundary']

def verifier(fighter):
    source=inspect.getsource(original.run)
    start="""    capture=ROOT/f'audit_v4753_{fighter}_p2_ending_cpu_cycle_ram'"""
    end="""    ids=(13,17 if fighter=='kano'else 18);path=capture/'run.log';first=[];window=[]"""
    need(source.count(start)==source.count(end)==1,'Unique whole original proof admission')
    a=source.index(start);b=source.index(end)+len(end)
    source=source[:a]+"""    capture=ROOT/f'audit_v5720_{fighter}_current_p2_ending_pixels'
    oldreport=ROOT/f'audit_v5722_{fighter}_current_p2_ending_terminal_pixels_checked/report.json'
    pagepath=ROOT/f'audit_v5724_{fighter}_current_p2_original_ending_pages_checked/report.json'
    failed=json.loads(oldreport.read_text());meta=json.loads((capture/'result.json').read_text())
    pages=json.loads(pagepath.read_text())
    need(failed['passed']and meta['nativeExit']==0 and not meta['endingModelErrors']and
         len(meta['endingNativePixelFaults'])==len(failed['actualNativePixelFaultsRejected'])==2 and
         meta['exactContinuousEndingFields']==meta['observedEndingRGBFields']==failed['exactConsecutiveNativeVideoFields']and
         failed['actualCurrentP2EndingAttractNativeRendererVideoAccepted']and
         failed['oneInitialBaseOnly']and failed['comparisonTargetsNeverReanchor']and
         failed['actualColdNativeCampaignExactlyUnchanged']and
         failed['physicalSlot']==2 and failed['candidate']==current.NAME and failed['executableSHA256']==current.EXE_SHA and
         pages['passed']and pages['physicalSlot']==2 and pages['identity']==(17 if fighter=='kano'else 18)and
         pages['actualCurrentP2EndingEarlyLatePhotoTextShadowCommonBackgroundAccepted']and
         pages['actualFullRGBPixelsCompared']==406400,
         'Separate actual native terminal0/full RAM VRAM/RGB/cold-true-ID/source-page/bitfault proofs; metadata never replaces pixels')
    need(all(sha(p)==h for p,h in failed['inputHashes'].items())and
         all(sha(p)==h for p,h in pages['inputHashes'].items()),
         'Every actual whole native pixel and original photo/font/shadow/background input unchanged')
    for p,h in meta['inputHashes'].items():need(sha(p)==h,'All actual executed controls/observer/guest bytes unchanged')
    ids=(13,17 if fighter=='kano'else 18);path=capture/'run.log.gz';first=[];window=[]"""+source[b:]
    changes=[
      ("path.open()","gzip.open(path,'rt')"),
      ("previous.source.renderer_window","window_model.renderer_window"),
      ("failed['actualRasterClocks']","failed['actualSourceTimedRasterClocks']"),
      ("failed['actualOriginalDisplayIOStores']","failed['actualDisplayIOStores']"),
      ("('human_slot','1')","('human_slot','1')"),
      ("pins=dict(meta['input_hashes'])","pins=dict(meta['inputHashes'])"),
      ("physicalSlot=2,identity=ids[1]","physicalSlot=2,identity=ids[1]"),
      ("Path(guest_provider.__file__).resolve(),stockpath,oldreport,","Path(guest_provider.__file__).resolve(),stockpath,oldreport,pagepath,Path(original.__file__).resolve(),"),
      ("for p,h in failed['inputHashes'].items():","for p,h in {**failed['inputHashes'],**pages['inputHashes']}.items():")]
    expected_counts=[4,1,1,1,1,1,1,1,1]
    for (before,after),count in zip(changes,expected_counts):
        need(source.count(before)==count,'Exact whole original hardware proof adaptation '+before)
        source=source.replace(before,after)
    scope=dict(original.run.__globals__,__file__=__file__,ROOT=ROOT,need=need,sha=sha,
      current=current,model=hardware_model,guest_provider=current,gzip=gzip,
      contract=contract,terminal_boundary=terminal_boundary,window_model=window,
      original=original)
    exec(compile(source,__file__+'::entire_original_hardware_run_P1','exec'),scope)
    return scope['run']

def main(fighter):
    out=ROOT/f'audit_v5726_{fighter}_current_p2_complete_native_pixels_hardware_checked'
    need(not out.exists(),'Fresh immutable whole current P1 hardware proof')
    for path in (ROOT/f'audit_v5722_{fighter}_current_p2_ending_terminal_pixels_checked/report.json',
                 ROOT/f'audit_v5724_{fighter}_current_p2_original_ending_pages_checked/report.json'):
        need(path.exists(),'Await actual native terminal and independent complete page proof; no timeout acceptance')
    try:report=verifier(fighter)(fighter)
    except Exception as error:report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
    out.mkdir()
    need(subprocess.run(['compact.exe','/C','/I','/Q','/S:'+str(out)],capture_output=True).returncode==0,'Compress compact evidence before writes')
    (out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items()if k not in('inputHashes','actualMetadataFaultsRejected')},indent=2),flush=True)
    return 0 if report['passed']else 1

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--fighter',required=True,choices=('kano','sonya'))
    raise SystemExit(main(parser.parse_args().fighter))
