"""Exact full original hardware/page gates adapted only to actual current P1 scope."""
import ast,hashlib,inspect,json
from pathlib import Path
import verify_current_p1_native_ending_hardware_v5272 as hardware
import verify_current_p1_ending_pages_v5268 as pages
import verify_current_p1_ending_pages_v5253 as oldpages
import current_payload_metadata_context_v5229 as current
ROOT,need,sha=current.ROOT,current.need,current.sha
OUT=ROOT/'audit_v5275_current_p1_complete_ending_gate_source_checked'
def main():
    need(not OUT.exists(),'Fresh immutable full ending verification-source proof')
    current.expected()
    prepath=ROOT/'audit_v5267_p1_ending_deferred_source_checked/report.json'
    pre=json.loads(prepath.read_text())
    need(pre['passed']and pre['sourceOnly']and all(sha(p)==h for p,h in pre['inputHashes'].items()),
      'Actual before-boot full P1 observer/model/unchanged-controller and alias gate intact')
    priorpath=ROOT/'audit_v4758_kano_complete_native_ending_pixels_and_hardware_checked/report.json'
    prior=json.loads(priorpath.read_text())
    need(prior['passed']and prior['fullEndingVRAMRGBPixelsAccepted']and
      prior['metadataNeverSubstitutedForPixels']and not prior['dummyVRAMUsed']and
      len(prior['actualMetadataFaultsRejected'])==27 and len(prior['actualTerminalFaultsRejected'])==8 and
      len(prior['actualNativePixelBitFaultsRejected'])==2,
      'Whole prior actual native RAM pixels/hardware ledger and all real faults retained')
    original=hardware.original
    for module in (original,original.previous,original.diagnostic,original.model):
        p=str(Path(module.__file__).resolve())
        need(p in prior['inputHashes']and sha(p)==prior['inputHashes'][p],
          'Exact accepted whole original hardware function/model source '+p)
    old=Path(oldpages.__file__).read_text();new=Path(pages.__file__).read_text()
    need(new.replace('audit_v5264_','audit_v5250_').replace('audit_v5269_','audit_v5254_')==old,
      'Every original photo/font/text-shadow/background/actual RGB fault gate retained; only fresh actual paths')
    counts={}
    for fighter in ('kano','sonya'):
        fn=hardware.verifier(fighter)
        need(fn.__globals__['contract']is hardware.contract and
          fn.__globals__['terminal_boundary']is hardware.terminal_boundary and
          fn.__globals__['guest_provider']is current and
          fn.__globals__['model']is hardware.hardware_model,
          'Actual compiled full checker binds true physical P1 parser/native cycle/guest and separate mandatory pixel proof')
        counts[fighter]=len(fn.__code__.co_code)
    need(hardware.hardware_model.parse is hardware.p1.parse and
      hardware.hardware_model.previous.previous.validate_context is hardware.p1.validate_context and
      hardware.Ledger.__bases__==(hardware.p1.Scanline,),
      'Every actual ledger record and complete unchanged scanline machine binds original P1 admission')
    pins=dict(pre['inputHashes'])
    for p in [prepath,priorpath,Path(__file__).resolve(),Path(hardware.__file__),Path(pages.__file__),Path(oldpages.__file__),
      ROOT/'tools/qualify_p1_ending_deferred_source_v5262.py',
      ROOT/'tools/run_p1_ending_deferred_pixels_v5261.py',
      ROOT/'tools/verify_current_p1_native_ending_hardware_v5270.py']:
        if p.suffix=='.py':ast.parse(p.read_text(),filename=str(p))
        pins[str(p.resolve())]=sha(p)
    need(all(sha(p)==h for p,h in pins.items()),'Full original/failure/fresh source chain byte-exact')
    report=dict(passed=True,sourceOnly=True,physicalSlot=1,fullOriginalHardwareLedgerAndPagePredicatesRetained=True,
      compiledWholeHardwareVerifierBytes=counts,all27MetadataAnd8TerminalFaultsRetained=True,
      separateWholeNativeRAMVRAMRGBBitFaultProofMandatory=True,noDummyVRAM=True,
      priorFailedPreflightsPreserved=[
        dict(source='tools/qualify_p1_ending_deferred_source_v5262.py',issue='One source mutation anchor omitted assert(); no native launch'),
        dict(source='tools/verify_current_p1_native_ending_hardware_v5270.py',issue='Preflight expected six log opens; complete actual original has four; no native checker run')],
      actualCurrentP1CompletePixelsHardwarePagesAccepted=False,fullPortAcceptance=False,inputHashes=pins,newBuilds=0,rawMediaWritten=0)
    OUT.mkdir();(OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items()if k!='inputHashes'},indent=2),flush=True)
if __name__=='__main__':main()
