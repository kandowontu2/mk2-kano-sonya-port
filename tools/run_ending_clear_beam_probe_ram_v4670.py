"""Actual58183 pixel counterexample: bounded end-VRAM versus live beam probe.

Same accepted cold physical campaign and initialized guest.21 actual fields,
whole RGB/VRAM/palette in RAM, CPU write timing compacted by exact beam/register
tuple. No matching-image search, raster-model acceptance or game mutation.
"""
import inspect,json,re,subprocess,traceback
from pathlib import Path
import run_ending_latch_probe_ram_v4605 as previous
import qualify_ending_clear_beam_source_v4671 as source
ROOT,need,sha=previous.ROOT,previous.need,previous.sha
model=previous.model

def comparison(rgb,raw,palettes,start,control,tap):
    result=previous.comparison(rgb,raw,palettes,start,control,tap)
    # A diagnostic difference is preserved, never converted into a pass.
    return result

def collector():
    text=inspect.getsource(previous.collector)
    for before,after in(
      ('audit_v4607_ending_latch_probe_source_checked/report.json','audit_v4672_ending_clear_beam_source_checked/report.json'),
      ('audit_v4608_{fighter}_ending_latch_probe_ram','audit_v4673_{fighter}_ending_clear_beam_probe_ram'),
      ("probe_records.append(dict(native=r,currentRequestedStart=current_comparison,precedingActualRequestedStart=before,diagnosticOnly=True,rendererAccepted=False))",
       "derived=(int(r['dpyadr'],16)+(int(r['vcount'])-int(r['veblnk'])+1)*(int(r['control'],16)&0x03fc))&0xffff\n                        hardware=comparison(pixels,raw,palettes,derived,int(r['control'],16),int(r['tap'],16))\n                        probe_records.append(dict(native=r,currentRequestedStart=current_comparison,precedingActualRequestedStart=before,hardwareDerivedStart=hardware,diagnosticOnly=True,rendererAccepted=False))")):
        need(text.count(before)==1,'Only exact bounded capture leaf/metadata diagnostic addition')
        text=text.replace(before,after)
    namespace=dict(vars(previous),__file__=__file__,source=source,comparison=comparison)
    exec(compile(text,__file__+'::whole4605_bounded_actual_clear_probe','exec'),namespace)
    return namespace['collector']()

def main():
    out=ROOT/'audit_v4674_kano_ending_clear_beam_probe_observed'
    need(not out.exists(),'Fresh immutable actual clear-beam diagnosis')
    try:
        folder,headers,images,records=collector()('kano')
        need([int(r['native']['age'])for r in records]==list(range(1877,1898)),'Every21 actual fields including failed58183')
        text=(folder/'run.log').read_text();baseline=(ROOT/'audit_v4485_kano_current_p2_campaign_ram/run.log').read_text()
        prefixes=('MK2_NAT_CAMPAIGN_','MK2_MILEENA_CAMPAIGN_','MK2_BOSS_KNIFE_','MK2_CAMPAIGN_GUEST_RAM_DIGEST ','MK2_CAMPAIGN_RAM_FRAME_DIGEST ')
        selected=lambda t:[l for l in t.splitlines()if l.startswith(prefixes)]
        need(selected(text)==selected(baseline),'Every original physical/health/native boss/ending/attract/guest/58RGB event unchanged')
        bucket=lambda tag:[dict(re.findall(r'(\w+)=([^\s]+)',l))for l in text.splitlines()if l.startswith('MK2_ENDING_PROBE_'+tag+' ')]
        buckets,totals=bucket('CPU_BUCKET'),bucket('CPU_TOTAL')
        need([int(r['age'])for r in totals]==list(range(1877,1898))and
             all(sum(int(b['count'])for b in buckets if b['frame']==r['frame'])==int(r['writes_observed'])for r in totals),
             'Complete actual CPU beam ledger for every field; aggregate counts exact')
        pins=json.loads((folder/'result.json').read_text())['input_hashes']
        for p in folder.rglob('*'):
            if p.is_file():pins[str(p)]=sha(p)
        p=ROOT/'audit_v4485_kano_current_p2_campaign_ram/run.log';pins[str(p)]=sha(p)
        need(all(sha(p)==h for p,h in pins.items()),'All executed/current native inputs unchanged')
        report=dict(passed=True,capture=str(folder),actualDiagnosticFields=21,records=records,actualCPUBuckets=buckets,actualCPUTotals=totals,
                    everyOriginalColdNativeEventAndRGBUnchanged=True,actualRasterCauseQualificationPending=True,
                    fullEndingRendererVideoAccepted=False,fullPortAcceptance=False,rawMediaFilesWritten=0,inputHashes=pins,scope=__doc__)
    except Exception as error:report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
    out.mkdir();need(subprocess.run(['compact.exe','/C','/I','/Q','/S:'+str(out)],capture_output=True).returncode==0,'Compressed before writes')
    (out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items()if k not in('inputHashes','records','actualCPUBuckets','actualCPUTotals')},indent=2),flush=True)
    raise SystemExit(0 if report['passed']else 1)

if __name__=='__main__':main()
