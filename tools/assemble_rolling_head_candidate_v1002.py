"""Package an asset-only candidate with its exact unchanged verified binary."""
import hashlib
import json
import shutil
from pathlib import Path
import build_rolling_head_order_v1001 as art

ROOT=art.ROOT
OUT=ROOT/'diagnostic_v1002_owned_rolling_head_order'


def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def main():
    if OUT.exists():raise ValueError('Never replace a candidate')
    source=ROOT/'diagnostic_v978_owned_torso_invariant_blood'
    info=json.loads((source/'build-info.json').read_text(encoding='utf-8-sig'))
    pins=info['input_hashes'].copy()
    for filename,wanted in pins.items():
        assert digest(Path(filename))==wanted,filename
    assert digest(source/'mkport_candidate.exe')==info['executable_sha256']
    assert digest(source/'roms/mk2ks/mk2ks.mdata')==info['payload_sha256']==art.SOURCE_SHA
    payload=ROOT/'audit_v1001_owned_rolling_head_encoding/roms/mk2ks/mk2ks.mdata'
    report=json.loads((payload.parents[2]/'report.json').read_text())
    assert digest(payload)==report['outputSHA256']
    for relative in ('tools/assemble_rolling_head_candidate_v1002.py','tools/build_rolling_head_order_v1001.py',
                     'tools/build_native_death_art_v900.py','tools/build_native_pit_fall_v2.py',
                     'tools/build_native_projectile_impacts.py','audit_v1001_owned_rolling_head_encoding/report.json',
                     'diagnostic_v978_owned_torso_invariant_blood/build-info.json'):
        pins[str(ROOT/relative)]=digest(ROOT/relative)
    for path in (ROOT/'art_native_rolling_heads_v998').iterdir():
        if path.is_file():pins[str(path)]=digest(path)
    pins[str(payload)]=digest(payload)
    (OUT/'roms/mk2ks').mkdir(parents=True)
    shutil.copy2(source/'mkport_candidate.exe',OUT/'mkport_candidate.exe')
    shutil.copy2(payload,OUT/'roms/mk2ks/mk2ks.mdata')
    data=dict(name=OUT.name,executable_sha256=digest(OUT/'mkport_candidate.exe'),
              payload_sha256=digest(payload),input_hashes=pins,
              executable_reused_from=source.name,
              reason='Asset-only payload changes; exact compiled C++ inputs and binary retained',
              fullPortAccepted=False)
    (OUT/'build-info.json').write_text(json.dumps(data,indent=2)+'\n')
    print(json.dumps({k:v for k,v in data.items() if k!='input_hashes'},indent=2))


if __name__=='__main__':main()
