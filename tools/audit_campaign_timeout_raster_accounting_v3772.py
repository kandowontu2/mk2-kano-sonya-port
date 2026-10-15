"""Record the exposed MAME timeout PNGs without changing historical metadata."""
import json
from pathlib import Path
import run_native_sound_delivery_ram_v3682 as current
ROOT,need,sha=current.ROOT,current.need,current.sha
OUT=ROOT/'audit_v3773_campaign_timeout_raster_accounting'
LEAVES=('audit_v3745_guarded_kano_natural_p2_campaign','audit_v3745_guarded_sonya_natural_p2_campaign',
        'audit_v3751_guarded_sonya_zoning_p2_campaign','audit_v3756_guarded_sonya_throw_p2_campaign')

def main():
    need(not OUT.exists(),'Fresh immutable capture accounting')
    pins={str(Path(__file__).resolve()):sha(__file__)};cases=[]
    video=ROOT/'mame-mkp/src/emu/video.cpp';source=video.read_text()
    first=source.index('// if we\'re past the "time-to-execute" requested, signal an exit')
    last=source.index('machine().schedule_exit();',first)
    need('m_seconds_to_run'in source[first:last]and'// create a final screenshot'in source[first:last]and
      'save_snapshot(&screen, file)'in source[first:last],'Exact native MAME timeout screenshot implementation')
    pins[str(video)]=sha(video)
    for leaf in LEAVES:
        folder=ROOT/leaf;path=folder/'result.json';meta=json.loads(path.read_text())
        need(meta['exit_code']==0 and meta['candidate']==current.NAME,'Only actual terminal3680 cases')
        pins[str(path)]=sha(path);log=folder/'run.log';pins[str(log)]=sha(log)
        images=list(folder.rglob('*.png'));audio=list(folder.rglob('*.wav'))
        expected=0 if meta['player']=='kano'else 1
        need(len(images)==expected and not audio and all(p==folder/'snap/mk2ks/0000.png'for p in images),
          'Complete real output inventory, not the incorrect zero-raster metadata')
        for image in images:pins[str(image)]=sha(image)
        cases.append(dict(capture=leaf,recordedRasterFiles=meta['rawRasterFilesWritten'],actualAutomaticRasterFiles=len(images),
          incorrectZeroRasterCountRejected=bool(images),imageSHA256=[sha(p)for p in images],
          actualAutomaticRasterLogicalBytes=sum(p.stat().st_size for p in images),
          fullCampaignClearNotImplied=True,fullPortAcceptance=False))
    report=dict(passed=True,cases=cases,inputHashes=pins,nativeTimeoutAutomaticRasterFiles=3,
      historicalResultsChanged=False,automaticRasterFilesDeleted=False,captureMemoryOnlyContractAccepted=False,
      followupWrapper='mk2ks_guarded_campaign_finite_ram_v3766.lua',
      followupActualHostDeadlineExecutionNotYetVerified=True,fullPortAcceptance=False)
    OUT.mkdir();(OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items()if k not in('inputHashes','cases')},indent=2),flush=True)

if __name__=='__main__':main()
