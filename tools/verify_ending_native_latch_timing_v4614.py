"""Actual ending-switch cause: native VBLANK latch, never a pixel-based fallback.

Derive visible start from actual DPYADR and original DUDATE/scanline count
before considering RGB. This is a41-field hardware diagnosis, not whole
ending renderer, independent choreography, art/audio or full-port acceptance.
"""
import copy,json,re,subprocess
from pathlib import Path
import run_ending_latch_probe_ram_v4605 as capture
ROOT,need,sha=capture.ROOT,capture.need,capture.sha
CASE=ROOT/'audit_v4608_kano_ending_latch_probe_ram'
OUT=ROOT/'audit_v4615_ending_native_latch_timing_checked'
def derive(row):
    native=row['native'];hexnum=lambda k:int(native[k],16)
    vcount,blank,first=(int(native[k])for k in('vcount','vsblnk','veblnk'))
    control,start,address=hexnum('control'),hexnum('start'),hexnum('dpyadr')
    need(vcount==blank-1 and blank-first==254 and control&0x8000 and
      start&3==address&3==0 and control&0x03fc==16,
      'Actual end-of-visible native scanline, enabled DPYCTL and nonzoom DUDATE scope; no guessing a row')
    # Exactly inverse to original scanline_callback decrement, after254 lines.
    derived=(address+(vcount-first+1)*(control&0x03fc))&0xffff
    comparisons=[r for r in(row['currentRequestedStart'],row['precedingActualRequestedStart'])if r is not None and r['start']==derived]
    need(comparisons and all(r==comparisons[0]for r in comparisons),
      'Only the independently hardware-derived address, never choose a matching image or search buffers')
    observed=comparisons[0]
    need(observed['mismatchedPixels']==0 and observed['actualRGBSHA256']==observed['expectedRGBSHA256'],
      'Every actual visible pixel matches the independently derived native scanout')
    return dict(frame=int(native['frame']),age=int(native['age']),requestedStart=start,
      actualEndOfVisibleDPYADR=address,derivedLatchedVisibleStart=derived,wholeRGBSHA256=observed['actualRGBSHA256'])
def contract(records):
    need([int(r['native']['age'])for r in records]==list(range(1100,1141)),'All41 actual diagnostic fields, no missing failed field')
    derived=[derive(r)for r in records]
    delayed=[r for r in derived if r['requestedStart']!=r['derivedLatchedVisibleStart']]
    need(len(delayed)==1 and delayed[0]['frame']==57416 and delayed[0]['age']==1120 and
      delayed[0]['requestedStart']==0xfffc and delayed[0]['derivedLatchedVisibleStart']==0xeffc,
      'Exactly actual previously failed field: new DPYSTRT request with old native latched scanout')
    return derived
def main():
    need(not OUT.exists(),'Fresh immutable source/actual hardware qualification')
    records=json.loads((CASE/'ending_latch_probe_records.json').read_text());positive=contract(records)
    meta=json.loads((CASE/'result.json').read_text());need(meta['exit_code']==0 and
      meta['ramGuestSHA256']=='938D380B3E2CE8DF6A688E2DC64C576CC7A1E554AE341E7B42463129FA5CA821'and
      meta['nativeGuestBytesVerifiedInRAM']==1048576 and meta['actualEndingLatchProbeFields']==41,
      'Actual terminal native0 full original current guest and bounded read-only hardware probe')
    log=(CASE/'run.log').read_text();baseline=(ROOT/'audit_v4485_kano_current_p2_campaign_ram/run.log').read_text()
    prefixes=('MK2_NAT_CAMPAIGN_','MK2_MILEENA_CAMPAIGN_','MK2_BOSS_KNIFE_','MK2_CAMPAIGN_GUEST_RAM_DIGEST ','MK2_CAMPAIGN_RAM_FRAME_DIGEST ')
    selected=lambda text:[line for line in text.splitlines()if line.startswith(prefixes)]
    need(selected(log)==selected(baseline),'Every original cold native input/state/health/boss/own-ending/attract/guest/RGB event unchanged')
    writes=[dict(re.findall(r'(\w+)=([^\s]+)',line))for line in log.splitlines()if line.startswith('MK2_ENDING_PROBE_START_WRITE ')and'age=1120 'in line]
    need(len(writes)==1 and writes[0]['pc']=='FF839FD0'and writes[0]['mask']=='FFFF'and
      writes[0]['before']==writes[0]['dpyadr']=='EFFC'and writes[0]['value']=='FFFC'and
      int(writes[0]['vcount'])==275>int(writes[0]['vsblnk'])==274,
      'Actual native DPYSTRT write after VBLANK already latched old EFFC; PC/data/mask/beam provenance exact')
    source=ROOT/'mame-mkp/src/devices/cpu/tms34010/tms34010.cpp';code=source.read_text()
    for token in ('if (vcount == vsblnk)','IOREG(REG_DPYADR) = IOREG(REG_DPYSTRT);',
      'if (vcount >= veblnk && vcount < vsblnk)',
      'dpyadr = ((dpyadr & 0xfffc) - (IOREG(REG_DPYCTL) & 0x03fc)) | (IOREG(REG_DPYSTRT) & 0x0003);',
      'uint16_t dpyadr = IOREG(REG_DPYADR);','params->rowaddr = dpyadr >> 4;'):
        need(token in code,'Original VBLANK/visible DUDATE/native scanout source operation retained: '+token)
    guest=capture.original.expected();rom=(ROOT/'mk2/mk2-maincpu.bin').read_bytes()
    a,b=(0xff839f20-0xff800000)//8,(0xff83a080-0xff800000)//8
    need(guest[a:b]==rom[a:b],'Actual delayed-switch CPU routine byte-exact to original MK2, not a port transition hook')
    faults=[]
    bad=copy.deepcopy(records);bad[20]['native']['dpyadr']='F01C'
    phase=copy.deepcopy(records);phase[20]['native']['vcount']='272'
    stride=copy.deepcopy(records);stride[20]['native']['control']='F020'
    for label,altered in [('wrong_actual_latched_DP YADR'.replace(' ',''),bad),('wrong_actual_scanline_phase',phase),
      ('wrong_actual_DUDATE',stride),('missing_actual_failed_field',records[:20]+records[21:])]:
        try:contract(altered)
        except ValueError as error:faults.append(dict(label=label,rejectedBy=str(error)))
        else:raise ValueError('Accepted actual hardware fault: '+label)
        need(contract(records)==positive,'Entire unchanged actual41-field positive restored after fault')
    pins=dict(meta['input_hashes']);pins[str(source)]=sha(source);pins[str(Path(__file__).resolve())]=sha(__file__)
    pins[str(ROOT/'audit_v4485_kano_current_p2_campaign_ram/run.log')]=sha(ROOT/'audit_v4485_kano_current_p2_campaign_ram/run.log')
    for p in CASE.rglob('*'):
        if p.is_file():pins[str(p)]=sha(p)
    need(all(sha(p)==h for p,h in pins.items()),'Every current source/capture/game/public input unchanged')
    report=dict(passed=True,actualNativeVBLANKLatchCauseEstablished=True,failedFrame=57416,
      actualDPYSTRTRequestAfterLatch=writes[0],hardwareDerivedVisibleFields=positive,actualHardwareFaultsRejected=faults,
      originalDelayedSwitchRoutineByteExact=True,originalColdNativeCampaignGuestRGBExactlyUnchanged=True,
      diagnosis='At VCOUNT275, after VSBLNK274 latched EFFC, original CPU writes requested FFFC. The displayed field still derives from old DPYADR; the following field derives from FFFC. Old verifier assumed immediate DPYSTRT display.',
      fullEndingRendererVideoAccepted=False,independentTransitionChoreographyArtAudioAccepted=False,
      fullPortAcceptance=False,inputHashes=pins,scope=__doc__)
    OUT.mkdir();need(subprocess.run(['compact.exe','/C','/I','/Q','/S:'+str(OUT)],capture_output=True).returncode==0,'Compressed before writes')
    (OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items()if k not in('inputHashes','hardwareDerivedVisibleFields')},indent=2),flush=True)
if __name__=='__main__':main()
