"""Preserve actual Python setup SyntaxError before any emulator was spawned."""
import gzip,json
from pathlib import Path
import native_ai_response_context as current
import native_process_census_v6647 as census
ROOT,need,sha=current.ROOT,current.need,current.sha

if __name__=='__main__':
    out=ROOT/'audit_native_phase900_duplicate_keyword_failure'
    before=ROOT/'tools/capture_native_postending_join_cpu_ice_phase900_before_keyword_fix.py'
    need(not out.exists() and not census.census() and
         not (ROOT/'audit_native_postending_kano_p2_sonya_cpu_ice_phase900').exists(),
         'Actual setup failure before output creation/native launch; no live native is restarted')
    text=before.read_text()
    need("before=\"MK2KS_CAMPAIGN_SIDE='2'\"" in text and
         "before+\",MK2KS_TEST_BOOT_FRAME='900'\"" in text,'Exact preserved failed Python adaptation')
    out.mkdir()
    with gzip.open(out/'executed_outer_source.json.gz','wt',encoding='utf-8') as stream:
        json.dump(dict(path=str(before),sha256=sha(before),text=text),stream)
    (out/'report.json').write_text(json.dumps(dict(passed=False,nativeSpawned=False,pythonHostExit=1,
        error='SyntaxError: keyword argument repeated: MK2KS_TEST_BOOT_FRAME',
        cause='Original host already declared boot600; failed adapter inserted a duplicate boot keyword.',
        correctedAction='Replace the single existing boot600 keyword with boot900.',
        originalSourceSHA256=sha(before),correctedSourceSHA256=sha(ROOT/'tools/capture_native_postending_join_cpu_ice_phase900.py'),
        noGameResultAccepted=True,fullPortAcceptance=False),indent=2)+'\n')
    print(json.dumps(dict(preserved=True,nativeSpawned=False)),flush=True)
