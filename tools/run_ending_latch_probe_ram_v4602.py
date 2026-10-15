"""Actual failed ending-switch register/VRAM/palette/RGB diagnosis, RAM only.

Never accept a chosen matching buffer as a renderer proof. Both current and
preceding actual requested starts are reported as diagnostic comparisons only.
No game code/control changes, new build, media file or whole-video acceptance.
"""
import inspect,json,re,subprocess,traceback
from pathlib import Path
import numpy as np
import run_kintaro_pressure_guard_long_campaign_v4439 as original
import qualify_ending_latch_probe_source_v4600 as source
import current_tomb_ram_model_v3642 as model
ROOT,need,sha=original.ROOT,original.need,original.sha
def comparison(rgb,raw,palettes,start,control,tap):
    address=start if control&0x400 else start^0xfffc;row=(address>>4)&511
    column=((((address&0x7c)<<4)|(tap&0x3fff))*2)&511
    need(row+254<=512 and column+400<=512 and start&3==0,'Actual native nonwrapped register rectangle')
    words=np.frombuffer(raw,dtype='<u2').reshape(512,512)[row:row+254,column:column+400]&0x7fff
    colors=np.frombuffer(palettes,dtype='<u4');expected=np.stack([(colors[words]>>n)&255 for n in(16,8,0)],axis=2).astype(np.uint8)
    mismatch=np.any(rgb!=expected,axis=2);where=np.argwhere(mismatch)
    return dict(start=start,row=row,column=column,mismatchedPixels=int(mismatch.sum()),
      expectedRGBSHA256=model.digest(expected.tobytes()),actualRGBSHA256=model.digest(rgb.tobytes()),
      firstMismatch=where[0].tolist()if len(where)else None)
def collector():
    text=inspect.getsource(original.capture)
    changes=[
      ("need(fighter=='sonya','Actual unfinished Sonya P2 context only')","need(fighter=='kano','Only actual previously failed Kano P2 ending switch')"),
      ('audit_v4438_kintaro_pressure_guard_long_source_preflight/report.json','audit_v4601_ending_latch_probe_source_checked/report.json'),
      ("audit_v4440_{fighter}_kintaro_pressure_guard_long_p2_campaign","audit_v4603_{fighter}_ending_latch_probe_ram"),
      ("MK2KS_CAMPAIGN_STRATEGY='guard_punish'","MK2KS_CAMPAIGN_STRATEGY='zoning'"),
      ('headers=[];images={};stream=hashlib.sha256();byte_count=0;guest_sha=None',
       'headers=[];images={};stream=hashlib.sha256();byte_count=0;guest_sha=None\n    transport=model.Transport();probe_raw={};probe_rgb={};probe_records=[];last_before=None'),
      ("if line.startswith('MK2_CAMPAIGN_GUEST_RAM '):",'''if line.startswith(('MK2_TOMB_RAM_BUFFER ','MK2_TOMB_RAM_PIXELS ')):
                    row=dict(re.findall(r'(\\w+)=([^\\s]+)',line));encoded=next(process.stdout).strip()
                    if line.startswith('MK2_TOMB_RAM_BUFFER '):
                        raw=transport.decode(row,encoded);probe_raw[row['file']]=raw
                        log.write('MK2_ENDING_PROBE_BUFFER_DIGEST '+line.split(' ',1)[1].strip()+' sha256='+model.digest(raw)+'\\n')
                    else:
                        need(row['bytes']=='406400'and row['width']=='400'and row['height']=='254'and row['encoding']=='u32le_numeric_hex'and len(encoded)==812800,'Whole actual native snapshot RGB32 in RAM')
                        words=np.frombuffer(bytes.fromhex(encoded),dtype='>u4').reshape(254,400)
                        pixels=np.stack([(words>>n)&255 for n in(16,8,0)],axis=2).astype(np.uint8);probe_rgb[row['file']]=pixels
                        log.write('MK2_ENDING_PROBE_RGB_DIGEST '+line.split(' ',1)[1].strip()+' sha256='+model.digest(pixels.tobytes())+'\\n')
                elif line.startswith('MK2_CAMPAIGN_GUEST_RAM '):'''),
      ("need('hex='not in line,'Never persist encoded raster')",'''need('hex='not in line,'Never persist encoded raster')
                    if line.startswith('MK2_ENDING_PROBE_START_WRITE '):
                        r=dict(re.findall(r'(\\w+)=([^\\s]+)',line));last_before=int(r['before'],16)
                    if line.startswith('MK2_ENDING_PROBE_SAMPLE '):
                        r=dict(re.findall(r'(\\w+)=([^\\s]+)',line));frame=int(r['frame'])
                        pixels=probe_rgb.pop(f'display_{frame}.png');raw=probe_raw.pop(f'display_vram_{frame}.bin');palettes=probe_raw.pop(f'display_palette_{frame}.bin')
                        current=comparison(pixels,raw,palettes,int(r['start'],16),int(r['control'],16),int(r['tap'],16))
                        before=comparison(pixels,raw,palettes,last_before,int(r['control'],16),int(r['tap'],16))if last_before is not None else None
                        probe_records.append(dict(native=r,currentRequestedStart=current,precedingActualRequestedStart=before,diagnosticOnly=True,rendererAccepted=False))
                        print(f'ending latch age={r["age"]} requested={r["start"]} DPYADR={r["dpyadr"]} VCOUNT={r["vcount"]} mismatch={current["mismatchedPixels"]}',flush=True)'''),
      ('nativeFrameStreamSHA256=stream.hexdigest().upper(),passed=False',
       'nativeFrameStreamSHA256=stream.hexdigest().upper(),actualEndingLatchProbeFields=len(probe_records),passed=False'),
      ('return folder,headers,images',"(folder/'ending_latch_probe_records.json').write_text(json.dumps(probe_records,indent=2)+'\\n')\n    return folder,headers,images,probe_records")]
    for before,after in changes:
        need(text.count(before)==1,'Only declared whole4439 cold controls and read-only diagnostic RAM sink addition: '+before);text=text.replace(before,after,1)
    namespace=dict(vars(original),__file__=__file__,source=source,LUA=source.LUA,model=model,comparison=comparison)
    exec(compile(text,__file__+'::whole4439_failed_switch_probe_only','exec'),namespace)
    return namespace['capture']
def main():
    out=ROOT/'audit_v4604_kano_ending_latch_probe_observed';need(not out.exists(),'Fresh immutable diagnosis')
    try:
        folder,headers,images,records=collector()('kano')
        need([int(r['native']['age'])for r in records]==list(range(1100,1141)),'Every actual failed-switch diagnostic field')
        report=dict(passed=True,capture=str(folder),actualDiagnosticFields=len(records),
          actualCauseRequiresSourceAndTimingQualification=True,fullVideoAcceptance=False,fullPortAcceptance=False)
    except Exception as error:report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
    out.mkdir();need(subprocess.run(['compact.exe','/C','/I','/Q','/S:'+str(out)],capture_output=True).returncode==0,'Compressed before writes')
    (out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2),flush=True)
    raise SystemExit(0 if report['passed']else 1)
if __name__=='__main__':main()
