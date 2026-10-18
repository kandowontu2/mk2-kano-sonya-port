"""Qualify only the native own-art scene, never playable-character completion."""
import csv
import hashlib
import json
import re
from pathlib import Path
HERE=Path(__file__).resolve().parent
BASE=HERE.parent/'baseline'
RUN=BASE/'stock_wolf_own_art_qualified'
SRC=BASE/'mk2-rebuild-main/srcw'
ROOT=HERE.parents[1]
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest().upper()
def main():
    execution=json.loads((RUN/'execution.json').read_text())
    assert execution['exitCode']==0 and not execution['timedOut']
    assert execution['nativeArtDiagnostic'] and not execution['customDriver'] and not execution['gameMemoryWrites']
    assert sha(Path(execution['emulator']))==execution['emulatorSHA256']
    symbols={name:int(address,16) for address,name in re.findall(r'\b([0-9a-fA-F]{8})\s+([A-Za-z_]\w*)',(SRC/'ARTTEST.MAP').read_text())}
    rows=list(csv.DictReader((RUN/'art_objects.csv').open()))
    live=[r for r in rows if r['kid']=='17' and r['sid']=='18']
    assert len(live)>=95 and int(live[-1]['frame'])-int(live[0]['frame'])>=2800
    source=(HERE/'generated_packed/KSANIM.ASM').read_text()
    counts={}
    for fighter,field,count in [('kano','kshape',9),('sonya','sshape',8)]:
        label=f'ks_{fighter}_stance'
        body=source.split('\n'+label+'\n',1)[1].split('.long ani_jump',1)[0]
        labels=re.findall(r'\.long (ks_\w+_pose_[0-9a-f]+)',body)
        assert len(labels)==count
        expected={symbols[name] for name in labels}
        actual={int(row[field],16) for row in live}
        assert actual==expected,(fighter,actual,expected)
        counts[fighter]=dict(verifiedStancePoses=len(actual),nativeID=17 if fighter=='kano' else 18)
    assert all(row['kobj']!=row['sobj'] for row in live)
    pins={}
    for p in [RUN/'execution.json',RUN/'art_objects.csv',SRC/'ARTTEST.MAP',SRC/'ARTTEST.OUT',
              HERE/'diagnostics/KSART.ASM',HERE/'diagnostics/art_probe.lua',
              HERE/'generated_packed/ART_IMPORT.json',HERE/'generated_templates_bound/TRANSLATION.json']+list((RUN/'snap').glob('art_*.png')):
        pins[str(p.relative_to(ROOT))]=sha(p)
    result=dict(passed=True,scope='Native ID17/18 own-art stance diagnostic on stock MAME; not fighting or selection integration',
                liveSamples=len(live),firstLiveFrame=int(live[0]['frame']),lastLiveFrame=int(live[-1]['frame']),
                fighters=counts,emulatorSHA256=execution['emulatorSHA256'],
                inputOnlyHostController=True,customEmulator=False,playablePortVerified=False,
                knownProbeFailures=['initial missing boot acknowledgment input','DWORD read of byte-aligned GSPA BSS pointer','30-frame sampling aliases 5-tick pose cycles'],files=pins)
    (RUN/'qualification.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='files'},indent=2))
if __name__=='__main__': main()
