"""Exact current build/launch provenance. No old-source fallback for v517."""
import json
from pathlib import Path
from verify_ko_round_floor_shadows import need, digest

ROOT=Path(__file__).resolve().parents[1]
NAME='diagnostic_v517_native_cannonball_velocity'
EXE='8E11915DC9DD1DE17616FD15034D6B9D7656091BDFA9B545942F73222942779E'
PAYLOAD='82FE153FB56B46A6F9D42F493451AC3D59AD61713433714ACA7704E2881F8951'

def matched(folder,inputs):
    result=json.loads((folder/'result.json').read_text(encoding='utf-8-sig'))
    build=json.loads((ROOT/NAME/'build-info.json').read_text(encoding='utf-8-sig'))
    need(result['exit_code']==0 and result['candidate']==build['name']==NAME and
         result['assistance']=='none','Terminal unassisted exact current candidate')
    need(result['executable_sha256']==build['executable_sha256']==EXE and
         result['payload_sha256']==build['payload_sha256']==PAYLOAD,'Exact build identity')
    for file,sha in ((ROOT/NAME/'mkport_candidate.exe',EXE),
                     (ROOT/NAME/'roms/mk2ks/mk2ks.mdata',PAYLOAD)):
        need(digest(file)==sha,'Actual candidate executable/payload');inputs[str(file)]=sha
    manifest=json.loads((folder/'input_hashes_before.json').read_text(encoding='utf-8-sig'))
    need(manifest==result['input_hashes'],'Before/after manifests agree')
    need(all(manifest.get(path)==sha for path,sha in build['input_hashes'].items()),
         'All actual build inputs present in launch inventory')
    for path,sha in manifest.items():
        need(digest(Path(path))==sha,'Current launch input changed: '+path)
        inputs[path]=sha
    for file in (folder/'run.log',folder/'result.json',folder/'input_hashes_before.json',
                 ROOT/NAME/'build-info.json'):
        inputs[str(file)]=digest(file)
