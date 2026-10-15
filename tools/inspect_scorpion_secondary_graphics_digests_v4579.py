"""Read-only bounded observed-source comparison; no native art acceptance."""
import json,re,subprocess
from pathlib import Path
import scorpion_secondary_native_scene_model_v4559 as model
ROOT=Path(__file__).resolve().parent.parent
OUT=ROOT/'audit_v4580_scorpion_secondary_graphics_digest_inspected'

def main():
    model.need(not OUT.exists(),'Fresh source diagnosis')
    payload=ROOT/'diagnostic_v3836_native_mileena_rom_identity/roms/mk2ks/mk2ks.mdata'
    pins={};graphics=model.sources(payload.read_bytes(),pins)
    log=ROOT/'audit_v4576_scorpion_secondary_kano_p1_native_scene_ram/run.log'
    size=log.stat().st_size;total=0;bad=[]
    with log.open()as stream:
        while True:
            line=stream.readline()
            if not line or stream.tell()>size:break
            if not line.startswith('MK2_NAT_CAMPAIGN_FLOOR_GFX '):continue
            row=dict(re.findall(r'(\w+)=([^\s]+)',line));first,count=int(row['first']),int(row['bytes'])
            expected=model.digest(graphics[first:first+count]);total+=1
            if expected!=row['data_sha256']:bad.append(dict(row,expectedSHA256=expected))
    report=dict(passed=True,actualObservedGraphicsStreams=total,mismatches=bad,totalMismatches=len(bad),
      boundedActualLogBytes=size,wholeNativeSceneAcceptance=False,fullPortAcceptance=False,inputHashes=pins,
      payloadSHA256=model.digest(payload.read_bytes()))
    OUT.mkdir();model.need(subprocess.run(['compact.exe','/C','/I','/Q','/S:'+str(OUT)],capture_output=True).returncode==0,'Compressed before writes')
    (OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items()if k!='inputHashes'},indent=2),flush=True)

if __name__=='__main__':main()
