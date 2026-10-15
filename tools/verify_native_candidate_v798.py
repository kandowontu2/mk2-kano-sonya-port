"""Exact current v786 build/launch provenance; no historical-source fallback."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NAME = 'diagnostic_v786_native_fighter_fade_exclusions'
EXE = '8DD83D7300BBC3872B1F829EA2A557CA968F5148464C3518AAB16B8559A76B55'
PAYLOAD = '7896C93822473376AD724BB5E747EDE88C198203786F3F9B928CD1D860BAE019'

def need(ok, message):
    if not ok:
        raise ValueError(message)

def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest().upper()

def matched(folder, inputs):
    result = json.loads((folder/'result.json').read_text(encoding='utf-8-sig'))
    build = json.loads((ROOT/NAME/'build-info.json').read_text(encoding='utf-8-sig'))
    need(result['exit_code'] == 0 and result['candidate'] == build['name'] == NAME
         and result['assistance'] == 'none' and result['cheats_enabled'] is False,
         'Terminal unassisted exact current candidate')
    need(result['executable_sha256'] == build['executable_sha256'] == EXE and
         result['payload_sha256'] == build['payload_sha256'] == PAYLOAD, 'Exact build identity')
    for path, value in ((ROOT/NAME/'mkport_candidate.exe', EXE),
                        (ROOT/NAME/'roms/mk2ks/mk2ks.mdata', PAYLOAD)):
        need(digest(path) == value, 'Actual candidate executable/payload')
        inputs[str(path)] = value
    manifest = json.loads((folder/'input_hashes_before.json').read_text(encoding='utf-8-sig'))
    need(manifest == result['input_hashes'], 'Before/after manifests agree')
    need(all(manifest.get(path) == value for path, value in build['input_hashes'].items()),
         'All actual build inputs present in launch inventory')
    for name, value in manifest.items():
        path = Path(name)
        need(digest(path) == value, 'Current launch input changed: ' + name)
        if path.suffix in ('.lua', '.ps1', '.json'):
            need(digest(folder/'input_sources'/path.name) == value, 'Frozen launch input changed: ' + name)
        inputs[name] = value
    for path in (folder/'run.log', folder/'result.json', folder/'input_hashes_before.json', ROOT/NAME/'build-info.json'):
        inputs[str(path)] = digest(path)
