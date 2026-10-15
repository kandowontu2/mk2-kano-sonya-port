"""Exact current native P1 CPU/P2 human observer launch; no historical fallback."""
import json
import re
from pathlib import Path
from verify_native_candidate_v517 import ROOT, NAME, EXE, PAYLOAD, matched
from verify_cpu_air_runtime import need, n, h
from verify_cpu_air_gate import digest, ORIGINAL_SHA

SOURCE = 'B8542F4777E4F100EC4E86771AD70EC867522FE106DD51E6F164E408489722D3'

def matched_launch(folder, observer, runner):
    folder = Path(folder)
    launch = json.loads((folder/'result.json').read_text(encoding='utf-8-sig'))
    need((launch['cpu_slot'], launch['human_slot']) == (1, 2), 'Actual CPU/human slots')
    matched(folder, {})
    for filename, sha in launch['input_hashes'].items():
        path = Path(filename)
        if path.suffix in ('.lua', '.ps1', '.json'):
            need(digest(folder/'input_sources'/path.name) == sha, 'Exact frozen launch input')
    need(digest(ROOT/'mame-mkp/src/mame/midway/midtunit_m.cpp') == SOURCE, 'Exact current gameplay source')
    source = (folder/'input_sources'/observer).read_text()
    need(not re.search(r'write_u\d+|:write_|load_?state|\.value\s*=(?!=)', source), 'No guest-state assistance')
    need('-nocheat' in (folder/'input_sources'/runner).read_text(), 'Actual cheat-disabled launch')
    original = ROOT/'mk2/mk2-maincpu.bin'
    need(digest(original) == ORIGINAL_SHA, 'Exact original MKII program')
    return launch, (folder/'run.log').read_text(encoding='utf-8-sig'), original.read_bytes()
