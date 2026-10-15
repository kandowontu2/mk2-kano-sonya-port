"""Fresh cold21-field probe, independently reconstructing the actual84pixel clear."""
import inspect,json,re,subprocess,traceback
from pathlib import Path
import run_ending_latch_probe_ram_v4605 as previous
import ending_clear_beam_projection_v4688 as projection
import qualify_ending_clear_projection_source_v4689 as source
ROOT,need,sha=previous.ROOT,previous.need,previous.sha

def collector():
    text=inspect.getsource(previous.collector)
    changes=[
      ('audit_v4607_ending_latch_probe_source_checked/report.json','audit_v4690_ending_clear_projection_source_checked/report.json'),
      ('audit_v4608_{fighter}_ending_latch_probe_ram','audit_v4691_{fighter}_ending_clear_projection_ram'),
      ('probe_records=[];last_before=None','probe_records=[];last_before=None;prior_raw=None;cpu_buckets=[]'),
      ("if line.startswith('MK2_ENDING_PROBE_START_WRITE '):",
       "if line.startswith('MK2_ENDING_PROBE_CPU_BUCKET '):\n                        cpu_buckets.append(dict(re.findall(r'(\\\\w+)=([^\\\\s]+)',line)))\n                    if line.startswith('MK2_ENDING_PROBE_START_WRITE '):"),
      ("probe_records.append(dict(native=r,currentRequestedStart=current_comparison,precedingActualRequestedStart=before,diagnosticOnly=True,rendererAccepted=False))",
       "beam_projection=None\n                        if r['age']=='1887':\n                            need(prior_raw is not None,'Actual preceding complete native field required')\n                            beam_projection=projection.project(prior_raw,raw,palettes,pixels,r,[b for b in cpu_buckets if b['frame']==r['frame']])\n                        probe_records.append(dict(native=r,currentRequestedStart=current_comparison,precedingActualRequestedStart=before,actualBeamProjection=beam_projection,diagnosticOnly=True,rendererAccepted=False))\n                        prior_raw=raw")]
    for before,after in changes:
        need(text.count(before)==1,'Only exact full collector RAM projection and fresh-leaf adapter '+before[:65])
        text=text.replace(before,after)
    namespace=dict(vars(previous),__file__=__file__,source=source,projection=projection)
    exec(compile(text,__file__+'::whole4605_actual_clear_beam_projection','exec'),namespace)
    return namespace['collector']()

def main():
    out=ROOT/'audit_v4692_kano_ending_clear_projection_observed'
    need(not out.exists(),'Fresh immutable native beam projection')
    try:
        folder,headers,images,records=collector()('kano')
        need([int(r['native']['age'])for r in records]==list(range(1877,1898)),'Every21 actual diagnostic fields')
        modeled=[r for r in records if r['actualBeamProjection']is not None]
        need(len(modeled)==1 and modeled[0]['native']['frame']=='58183'and
             modeled[0]['actualBeamProjection']['mismatchedPixels']==0,'Exactly actual clear field fullRGB and endVRAM independently beam-projected')
        t=(folder/'run.log').read_text();baseline=(ROOT/'audit_v4485_kano_current_p2_campaign_ram/run.log').read_text()
        prefixes=('MK2_NAT_CAMPAIGN_','MK2_MILEENA_CAMPAIGN_','MK2_BOSS_KNIFE_','MK2_CAMPAIGN_GUEST_RAM_DIGEST ','MK2_CAMPAIGN_RAM_FRAME_DIGEST ')
        selected=lambda text:[l for l in text.splitlines()if l.startswith(prefixes)]
        need(selected(t)==selected(baseline),'Every original earned input/state/health/boss/ending/attract/guest/58RGB event unchanged')
        pins=json.loads((folder/'result.json').read_text())['input_hashes']
        for p in folder.rglob('*'):
            if p.is_file():pins[str(p)]=sha(p)
        p=ROOT/'audit_v4485_kano_current_p2_campaign_ram/run.log';pins[str(p)]=sha(p)
        need(all(sha(p)==h for p,h in pins.items()),'All actual native/current source bytes unchanged')
        report=dict(passed=True,capture=str(folder),actualFields=21,actualClearProjection=modeled[0],inputHashes=pins,
                    everyOriginalColdEventAndRGBUnchanged=True,actualRasterCauseFaultQualificationPending=True,
                    fullEndingRendererVideoAccepted=False,fullPortAcceptance=False,rawMediaFilesWritten=0,scope=__doc__)
    except Exception as error:report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
    out.mkdir();need(subprocess.run(['compact.exe','/C','/I','/Q','/S:'+str(out)],capture_output=True).returncode==0,'Compressed before writes')
    (out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items()if k!='inputHashes'},indent=2),flush=True)
    raise SystemExit(0 if report['passed']else 1)

if __name__=='__main__':main()
