"""Exact v680 build/launch provenance; explicit preserved v635 comparison."""
import json
from pathlib import Path
from verify_ko_round_floor_shadows import need, digest

ROOT=Path(__file__).resolve().parents[1]
NAME='diagnostic_v680_native_pit_initial_cache'
EXE='AD98FE42383F776BBD49BA4298EFD1F9F021FD2988C6B0A3956EE64316B44E82'
PAYLOAD='1367D5A0D42C661CF555F42231A20A650C28E107AB9C80BD821C0BEA7EB4D5EF'

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
        if Path(path).suffix in ('.lua','.ps1','.json'):
            need(digest(folder/'input_sources'/Path(path).name)==sha,'Frozen launch input changed: '+path)
        inputs[path]=sha
    for file in (folder/'run.log',folder/'result.json',folder/'input_hashes_before.json',
                 ROOT/NAME/'build-info.json'):
        inputs[str(file)]=digest(file)

def matched_reference(folder,inputs):
    """Historical inputs must match; only the intentionally edited driver
    resolves to its byte-exact pre-edit copy, never to a broad fallback."""
    result=json.loads((folder/'result.json').read_text(encoding='utf-8-sig'))
    old_name='diagnostic_v635_native_shadow_rows'
    old_exe='4CC606CFF6FC5747139948424DC38C9D9C932D6F41D45C372CCDB52B5C5C1F90'
    build=json.loads((ROOT/old_name/'build-info.json').read_text(encoding='utf-8-sig'))
    manifest=json.loads((folder/'input_hashes_before.json').read_text(encoding='utf-8-sig'))
    need(result['exit_code']==0 and result['candidate']==build['name']==old_name and
         result['executable_sha256']==build['executable_sha256']==old_exe and
         result['payload_sha256']==build['payload_sha256']==PAYLOAD and
         result['assistance']=='none' and manifest==result['input_hashes'], 'Exact terminal historical comparison')
    need(all(manifest.get(path)==sha for path,sha in build['input_hashes'].items()),'Historical build inventory complete')
    driver=ROOT/'mame-mkp/src/mame/midway/midtunit_m.cpp'
    preserved=ROOT/'audit_v680_pre_pit_initial_cache/sources/midtunit_m.cpp'
    for name,sha in manifest.items():
        path=Path(name)
        actual=preserved if path==driver else path
        if path==driver:
            need(sha=='2133D3D46E3DAFA3F44D0741962997595ADF4EB141A2EAB887EB7675A369707E',
                 'Only exact known pre-edit driver can resolve to preserved source')
        need(digest(actual)==sha,'Historical comparison input changed: '+name)
        if path.suffix in ('.lua','.ps1','.json'):
            need(digest(folder/'input_sources'/path.name)==sha,'Historical frozen launch source changed')
        inputs[str(actual)]=sha
    for path,sha in ((ROOT/old_name/'mkport_candidate.exe',old_exe),(ROOT/old_name/'roms/mk2ks/mk2ks.mdata',PAYLOAD)):
        need(digest(path)==sha,'Historical comparison binary changed');inputs[str(path)]=sha
    for path in (folder/'run.log',folder/'result.json',folder/'input_hashes_before.json',ROOT/old_name/'build-info.json'):
        inputs[str(path)]=digest(path)
