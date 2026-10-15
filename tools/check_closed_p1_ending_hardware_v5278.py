"""Read-only independent P1 ledger diagnostic on the closed prior native run.

The real post-export failure and absent per-field pixel records stay failed.
This checks the exact prepared ledger against actual native metadata; it
does not replace mandatory full pixels, pages or the complete fault matrix.
"""
import gzip,io,json,re,traceback
from pathlib import Path
import verify_current_p1_native_ending_hardware_v5272 as hardware
ROOT,need,sha=hardware.ROOT,hardware.need,hardware.sha
OUT=ROOT/'audit_v5279_closed_current_p1_native_metadata_diagnostic'
def run():
    folder=ROOT/'audit_v5250_kano_current_p1_ending_pixels'
    fail=ROOT/'audit_v5250_kano_current_p1_ending_pixels_checked/report.json'
    old=json.loads(fail.read_text());meta=json.loads((folder/'result.json').read_text())
    need(not old['passed']and "'bool' object has no attribute 'records'"in old['error']and
      meta['nativeExit']==0 and meta['exactContinuousEndingFields']==3040 and not meta['endingModelErrors'],
      'Actual terminal native metadata, failed export preserved, no live-log acceptance')
    path=folder/'run.log.gz'
    with gzip.open(path,'rt')as reader:raw=reader.read()
    lo,hi=hardware.window.renderer_window(raw,'kano');ids=(17,13)
    positive=hardware.contract(io.StringIO(raw),ids,hi+1)
    need([r['frame']for r in positive['records']]==list(range(lo,hi+1))and
      len(positive['records'])==3040,
      'Every actual closed ending and300attract hardware field; no fabricated pixels')
    guest=hardware.current.expected();stockpath=ROOT/'mk2/mk2-maincpu.bin'
    callers=hardware.original.original_io_callers(positive['io'],guest,stockpath.read_bytes())
    lines=raw.splitlines();stop=next(i for i,l in enumerate(lines)if l.startswith('MK2_NAT_CAMPAIGN_FLOOR_SNAP '))
    first=lines[:stop+1];baseline=hardware.contract(first,ids);faults=[]
    seed=next(l for l in first if l.startswith('MK2_NAT_CAMPAIGN_FLOOR_RASTER_CLOCK ')and 'reason=begin 'in l)
    store=next(l for l in first if l.startswith('MK2_NAT_CAMPAIGN_FLOOR_RASTER_IO '))
    for line,key,value,label in [(seed,'human_slot','2','wrong physical native slot'),
      (store,'pc','FFF00000','arbitrary aligned original ROM is not executed IO store')]:
        changed,n=re.subn(r'\b'+key+r'=\S+',key+'='+value,line,count=1)
        need(n==1 and changed!=line,'Actual nonvacuous original record fault')
        try:
            mutated=hardware.contract([changed if l==line else l for l in first],ids)
            hardware.original.original_io_callers(mutated['io'],guest,stockpath.read_bytes())
        except (ValueError,KeyError)as error:faults.append(dict(kind=label,rejectedBy=str(error)))
        else:raise ValueError('Actual metadata diagnostic fault accepted '+label)
        need(hardware.contract(first,ids)==baseline,'Whole original actual first native field restored')
    pins={str(p.resolve()):sha(p)for p in (Path(__file__),Path(hardware.__file__),path,fail,folder/'result.json',stockpath)}
    need(all(sha(p)==h for p,h in pins.items()),'Closed real native evidence and complete checker source exact')
    return dict(passed=True,metadataOnly=True,actualClosedNativeExit=0,physicalSlot=1,identity=17,
      actualCompletedHardwareFields=len(positive['records']),actualNativeClockRecords=positive['clocks'],
      actualDisplayIOStores=len(positive['io']),actualOriginalTimedOperations=positive['operations'],
      sourceQualifiedExecutedIOCallers=callers,actualMetadataFaultsRejected=faults,
      actualPostExportFailurePreserved=True,missingPerFieldPixelsStillUnaccepted=True,
      fullCurrentP1PixelsHardwarePagesAccepted=False,metadataNeverSubstitutedForPixels=True,
      noDummyVRAM=True,newBuilds=0,rawMediaWritten=0,fullPortAcceptance=False,inputHashes=pins)
def main():
    need(not OUT.exists(),'Fresh immutable closed-native metadata diagnostic')
    try:report=run()
    except Exception as error:report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
    OUT.mkdir();(OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items()if k!='inputHashes'},indent=2),flush=True)
    raise SystemExit(0 if report['passed']else 1)
if __name__=='__main__':main()
