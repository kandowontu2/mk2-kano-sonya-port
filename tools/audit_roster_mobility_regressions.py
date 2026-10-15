"""Recheck all ordinary mobility contacts against the exact new roster build."""
import hashlib
import json
from pathlib import Path

import verify_current_mobility as mobility
import verify_native_shang_roster as morph

ROOT=Path(__file__).resolve().parents[1]
NAME='diagnostic_v336_native_cpu_turn_lookup'
OUT=ROOT/'audit_v341_native_roster_mobility_checked_inputs'


def run():
    if OUT.exists():raise SystemExit('Refusing to overwrite evidence')
    build_path=ROOT/NAME/'build-info.json'
    build=json.loads(build_path.read_text(encoding='utf-8-sig'))
    if build['executable_sha256']!=morph.EXE or build['payload_sha256']!=morph.PAYLOAD:
        raise SystemExit('Exact current roster candidate required')
    files={build_path,ROOT/NAME/'mkport_candidate.exe',ROOT/NAME/'roms/mk2ks/mk2ks.mdata',Path(__file__)}
    files.update(Path(p) for p in build['input_hashes'])
    # Freeze all verifier dependencies, not just the aggregate entry point.
    files.update((ROOT/'tools').glob('*.py'))
    cases=[]
    for target in ('kano','sonya'):
        for side in (1,2):
            for scenario in ('hit','block','miss'):
                folder=ROOT/f'audit_v340_current_mobility_p{side}_{target}_{scenario}'
                files.update(p for p in folder.rglob('*') if p.is_file())
                proof=mobility.verify(folder,target,side,scenario,NAME,morph.EXE,morph.PAYLOAD)
                if not proof['passed']:raise SystemExit(json.dumps(proof))
                cases.append(dict(case=folder.name,proof=proof))
    hashes={str(p):hashlib.sha256(p.read_bytes()).hexdigest().upper() for p in sorted(files)}
    for file,expected in build['input_hashes'].items():
        if hashes[file]!=expected:raise SystemExit('Current build input changed: '+file)
    OUT.mkdir()
    (OUT/'input_hashes_before.json').write_text(json.dumps(hashes,indent=2)+'\n')
    for case in cases:(OUT/(case['case']+'.json')).write_text(json.dumps(case['proof'],indent=2)+'\n')
    for file,expected in hashes.items():
        if hashlib.sha256(Path(file).read_bytes()).hexdigest().upper()!=expected:
            raise SystemExit('Audit input changed: '+file)
    result=dict(passed=True,candidate=NAME,executable_sha256=morph.EXE,payload_sha256=morph.PAYLOAD,
                cases=len(cases),joined_fields=sum(c['proof']['joined']['joined_fields'] for c in cases),
                checked_inputs=len(hashes),memory_assistance='none',whole_character_integration_complete=False,
                scope='twelve_cold_native_CPU_starts_real_joins_full_mobility_hit_block_miss_followup_after_roster_change_not_endings_all_CPU_moves_pixels_audio_or_full_goal')
    (OUT/'result.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__=='__main__':run()
