"""Freeze the actual newline-literal provenance preflight failure."""
import gzip,json
from pathlib import Path
from capture_native_secondary_kano_reference import ROOT,census,need,sha

if __name__=='__main__':
    out=ROOT/'audit_native_secondary_guard_preflight_failure'
    need(not out.exists()and not census()and not (ROOT/'audit_native_secondary_kano_guarded_command').exists(),
         'Actual guard wrapper failed before any native job/output creation')
    paths=[ROOT/'tools/capture_native_secondary_kano_guarded_command.py',
           ROOT/'mk3_native_secondary_kano_guarded_command.lua',
           ROOT/'tools/capture_native_secondary_kano_command_checked.py',Path(__file__)]
    pins={str(p.resolve()):sha(p)for p in paths}
    out.mkdir()
    with gzip.open(out/'executed_preflight_sources.json.gz','wt',encoding='utf-8')as stream:
        json.dump({str(p.resolve()):dict(sha256=pins[str(p.resolve())],text=p.read_text())for p in paths},stream)
    (out/'report.json').write_text(json.dumps(dict(preserved=True,nativeStarted=False,
        actualError='ValueError: Only explicit raster ABI/combat and finish physical spacing replacements',
        cause='Exact new multiline insertion is escaped in the Lua string literal, not raw newlines in the wrapper file.',
        inputHashes=pins,gameSourceChanged=False,goalStatus='active'),indent=2)+'\n')
    print('Actual failed guard provenance preflight source conserved; no game started.')
