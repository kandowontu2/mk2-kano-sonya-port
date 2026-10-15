"""Consume the actual completed P2 capture with its one native shutdown seed.

All raw VRAM/RGB comparisons already ran inside the source-qualified live
collector; actual per-field records, RGB/transport digests and bit faults
are mandatory. No raw data is fabricated/replayed and no new boot occurs.
The single unrendered notifier seed is checked by the original full native
terminal/hardware ledger; it is never accepted as pixels or silently ignored.
"""
import argparse,gzip,json,re,traceback
from pathlib import Path
from types import SimpleNamespace
import run_current_p2_ending_pixels_complete_v5719 as capture
import verify_complete_native_ending_pixels_hardware_v4757 as original_hardware
import ending_raster_cpu_cycle_model_v4740 as model
import current_payload_metadata_context_v5229 as current
import qualify_ending_display_latch_source_v4647 as window
hardware=SimpleNamespace(**dict(vars(original_hardware),p1=model,current=current,window=window))
ROOT,need,sha=hardware.ROOT,hardware.need,hardware.sha
def run(fighter):
    folder=ROOT/f'audit_v5720_{fighter}_current_p2_ending_pixels'
    terminalpath=folder/'ending_live_model_terminal.json'
    live=json.loads(terminalpath.read_text());meta=json.loads((folder/'result.json').read_text())
    need(meta['passed']and meta['nativeExit']==0 and not meta['endingModelErrors']and
      len(meta['endingNativePixelFaults'])==2 and live['completedNativeCapture']and
      not live['actualModelErrors']and live['actualRemainingRGBTargets']==0 and
      live['actualBases']==1 and live['actualActorOwnerClassifications']==live['actualQueues']==live['actualPaletteClassifications']==0 and
      live['actualPixelFaultsRejected']==meta['endingNativePixelFaults'],
      'Actual complete native/model/pixel terminal; all errors fatal, full RAM runtime exports required')
    baseline=ROOT/('audit_v5622_current_kano_p2_campaign' if fighter=='kano'else 'audit_v5689_verified_subzero_sonya_p2_campaign')
    prepath=capture.source.OUT/'report.json';pre=json.loads(prepath.read_text())
    need(pre['passed']and pre['sourceOnly']and all(sha(p)==h for p,h in pre['inputHashes'].items())and
      all(sha(p)==h for p,h in meta['inputHashes'].items()),
      'Actual complete live RAM/model/physical-controller/current-game source pins unchanged')
    guest=json.loads((folder/'guest_memory_proof.json').read_text())
    need(guest['sha256']==hardware.current.GUEST_SHA and guest['everyActualByteComparedInRAM']and
      guest['captureSourceSHA256']==sha(capture.__file__)and guest['transportSourceSHA256']==sha(ROOT/capture.source.LUA),
      'Actual full independently expected guest and executed collector/observer')
    with gzip.open(folder/'run.log.gz','rt')as reader:raw=reader.read()
    with gzip.open(baseline/'run.log.gz','rt')as reader:prior=reader.read()
    native=lambda t:[l for l in t.splitlines()if not l.startswith(('MK2_NAT_CAMPAIGN_FLOOR_',
      'MK2_NAT_CAMPAIGN_SHADOW_','MK2_NAT_CAMPAIGN_ENDING_DISPLAY_','MK2_ENDING_RAM_','Average speed: '))]
    need(native(raw)==native(prior),'Every actual original cold guest/selection/ladder/combat/boss/own-ending/RGB event exact')
    records=json.loads((folder/'ending_continuous_records.json').read_text())
    visible=json.loads((folder/'ending_visible_digests.json').read_text())
    buffers=json.loads((folder/'ending_buffer_digests.json').read_text())
    lo,hi=hardware.window.renderer_window(raw,fighter);ids=(13,17 if fighter=='kano'else 18)
    need([r['frame']for r in records]==list(range(lo,hi+1))and
      len(records)==len(visible)==meta['observedEndingRGBFields']==meta['exactContinuousEndingFields']and
      all(r['exactVRAMWords']==262144 and r['exactRGBPixels']==101600 and r['actualRasterClocks']>=2 for r in records),
      'Every actual completed full source-timed native VRAM/RGB field; retained per-field exports mandatory')
    # Each successful Model.snapshot consumes its actual RGB target with pop().
    # Requiring a complete one-to-one exported transport/log/snapshot/record
    # binding proves the actual runtime RGB queue has no orphan target.
    def tagged(prefix):return [dict(re.findall(r'(\w+)=([^\s]+)',l))for l in raw.splitlines()if l.startswith(prefix+' ')]
    snaps=tagged('MK2_NAT_CAMPAIGN_FLOOR_SNAP')
    rgbrows=tagged('MK2_ENDING_RAM_RGB_DIGEST')
    need(len(snaps)==len(rgbrows)==len(records)and
      [dict(file=s['file'],rgbSHA256=r['rgbSHA256'])for s,r in zip(snaps,records)]==visible and
      [dict(file=r['file'],rgbSHA256=r['sha256'])for r in rgbrows]==visible and
      [int(s['frame'])for s in snaps]==[r['frame']for r in records],
      'All actual RGB targets consumed exactly once by the complete unchanged runtime Model.snapshot')
    bufferrows=tagged('MK2_ENDING_RAM_BUFFER_DIGEST')
    need(len(bufferrows)==len(buffers)and all(a['file']==b['file']and
      a['rawSHA256']==b['sha256']and a['bytes']==int(b['bytes'])for a,b in zip(buffers,bufferrows)),
      'Every actual RAM decoder export binds exact native transport digest')
    prefixes=lambda tag:tagged('MK2_NAT_CAMPAIGN_'+tag)
    begin,ko,attract=map(prefixes,('ENDING_DISPLAY_BEGIN','ENDING_DISPLAY_KO','ENDING_DISPLAY_ATTRACT'))
    need(len(begin)==len(ko)==len(attract)==1 and begin[0]['frame']==str(lo)and
      begin[0]['identity']==str(ids[1])and begin[0]['winner']=='2'and
      int(begin[0]['final_ko'])==int(ko[0]['frame'])<lo and ko[0]['pc']=='FF836700'and
      int(attract[0]['frame'])==hi-299,
      'Same own P2 native boss collision/winner/retired-actor ending and300realattract fields')
    need(len(prefixes('FLOOR_BASE'))==1 and not prefixes('FLOOR_QUEUE')and
      not prefixes('FLOOR_QUEUE_DISPATCH')and not prefixes('FLOOR_OWNER'),
      'One actual base only; no native actor/owned-palette/floor classifier admission')
    lines=raw.splitlines();last=max(i for i,l in enumerate(lines)if l.startswith('MK2_NAT_CAMPAIGN_FLOOR_SNAP '))
    tail_events=[hardware.p1.parse(l)for l in lines[last+1:]if hardware.p1.parse(l)and
      hardware.p1.parse(l)[0]in hardware.p1.Model.OPERATIONS]
    need(len(tail_events)==1 and tail_events[0][0]=='FLOOR_RASTER_CLOCK'and
      tail_events[0][1]['reason']=='field'and tail_events[0][1]['frame']==hi+1,
      'Exactly one original unrendered stop-notifier seed, no leftover CPU/DMA/shift/IO or pixel operations')
    need(live['actualCompletedFieldRecords']==len(records)and
      live['actualRemainingEvents']==[[tag,row]for tag,row in tail_events],
      'Actual runtime exports agree with independently parsed terminal operation tail')
    positive=hardware.contract(lines,ids,hi+1)
    need([r['frame']for r in positive['records']]==[r['frame']for r in records]and
      all(r['actualRasterClocks']==c['clocks']and r['actualDisplayIOStoresAtSnapshot']==c['ioStoresAtSnapshot']
      for r,c in zip(records,positive['records'])),
      'Every actual completed source-timed pixel record agrees independently with complete native hardware ledger')
    tail=[l for l in lines if (
      l.startswith('MK2_NAT_CAMPAIGN_FLOOR_RASTER_CLOCK ')and
      (('reason=finish 'in l and f'frame={hi} 'in l)or f'frame={hi+1} 'in l))or(
      l.startswith(('MK2_NAT_CAMPAIGN_FLOOR_SNAP ','MK2_NAT_CAMPAIGN_RESULT ','MK2_NAT_CAMPAIGN_FLOOR_RESULT '))and
      (f'frame={hi} 'in l or f'frame={hi+1} 'in l))]
    boundary=hardware.terminal_boundary(tail,ids,lo,hi,len(records))
    need(positive['unrenderedTerminalSeed']==boundary['actualTerminalClock']==tail_events[0][1]and
      sum(r['actualRasterClocks']for r in records)+1==positive['clocks'],
      'Every actual clock accounts for completed pixels or the one original native unrendered stop seed')
    pins=dict(meta['inputHashes'])
    for p in [Path(__file__).resolve(),Path(original_hardware.__file__),Path(model.__file__),terminalpath,prepath,
      baseline/'run.log.gz',*folder.rglob('*')]:
        if p.is_file():pins[str(p.resolve())]=sha(p)
    need(all(sha(p)==h for p,h in pins.items()),'All real failed/corrected terminal and full actual per-field evidence byte-exact')
    return dict(passed=True,fighter=fighter,physicalSlot=2,candidate=hardware.current.NAME,
      executableSHA256=hardware.current.EXE_SHA,capture=str(folder),
      actualColdNativeCampaignExactlyUnchanged=True,endingStart=lo,endingAttract=hi-299,
      lastCompletedRendererField=hi,actualAttractRendererFields=300,
      exactConsecutiveNativeVideoFields=len(records),exactRGBPixels=len(records)*101600,
      exactVRAMWords=len(records)*262144,actualNativePixelFaultsRejected=meta['endingNativePixelFaults'],
      actualSourceTimedRasterClocks=sum(r['actualRasterClocks']for r in records),
      actualDisplayIOStores=records[-1]['actualDisplayIOStoresAtSnapshot'],oneInitialBaseOnly=True,
      comparisonTargetsNeverReanchor=True,actualNativeUnrenderedTerminalBoundary=boundary,
      everyActualRetainedPerFieldRAMRecordRequired=True,missingOrAlteredPixelRecordNeverAccepted=True,
      noNewNativeBoot=True,actualLiveModelTerminalExportRequired=str(terminalpath),
      actualCurrentP2EndingAttractNativeRendererVideoAccepted=True,
      independentStockTransitionChoreographyAccepted=False,completeArtAudioCinematicContextAcceptance=False,
      fullPortAcceptance=False,inputHashes=pins,rawMediaGuestAudioFilesWritten=0,newBuilds=0,publicPlayableChanged=False)
def main(fighter):
    out=ROOT/f'audit_v5722_{fighter}_current_p2_ending_terminal_pixels_checked'
    need(not out.exists(),'Fresh immutable actual terminal result')
    try:report=run(fighter)
    except Exception as error:report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
    out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items()if k!='inputHashes'},indent=2),flush=True)
    raise SystemExit(0 if report['passed']else 1)
if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--fighter',required=True,choices=('kano','sonya'))
    main(parser.parse_args().fighter)
