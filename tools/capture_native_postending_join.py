"""Whole earned Kano P2 tower, followed by genuine coin/start Sonya P2 join.

The established physical campaign controller is unchanged until its original
300-field ending follow-through. Only a new ordinary-input phase is appended.
"""
import code
import gzip
import inspect
import json
import os
from pathlib import Path
import re
import time
import native_ai_response_full_context as native
import native_process_census_v6647 as census
import run_current_kano_p1_campaign_v5195 as original
import qualify_kano_current_p2_campaign_source_v4482 as boundary

ROOT, need, sha = native.ROOT, native.need, native.sha
OUT = ROOT/'audit_native_postending_kano_p2_sonya_join'
LUA = 'mk2ks_native_kano_p2_postending_sonya.lua'
CONTROLLERS = [LUA, *boundary.TRANSITIVE_LUA]


def metadata_clean(errors, proof):
    need(errors == '' and proof and proof['sha256'] == native.GUEST_SHA and proof['everyActualByteComparedInRAM'],
         'Current independent whole guest and completely empty native error stream')
    return dict(metadataMatchesPayload=True, nativeStderrEmpty=True, releaseMetadataCorrectionStillRequired=False)


def capture_source():
    source = inspect.getsource(original.capture)
    changes = [
        ("MK2KS_TEST_FIGHTER='kano',MK2KS_CAMPAIGN_SIDE='1'", "MK2KS_TEST_FIGHTER='kano',MK2KS_CAMPAIGN_SIDE='2'"),
        ("fighter='kano',physicalSlot=1,", "fighter='kano',physicalSlot=2,"),
        ('Current4992 Kano P1 campaign started', 'Current native Kano P2 post-ending join campaign started'),
        ("'-samplepath',str(ROOT/'samples')", "'-samplepath',str(candidate/'samples')+';'+str(ROOT/'samples')"),
        ("stdout=subprocess.PIPE,stderr=errors,text=True,encoding='utf-8',errors='strict')as process:",
         "stdout=subprocess.PIPE,stderr=errors,text=True,encoding='utf-8',errors='strict',creationflags=subprocess.CREATE_NO_WINDOW)as process:"),
        ("  (OUT/'process.json').write_text(",
         "  identity=next((r for r in census.census() if r['ProcessId']==process.pid),None)\n"
         "  need(identity and identity['ParentProcessId']==os.getpid() and identity['createdUnix']>=started-1,'Actual live native child creation identity')\n"
         "  (OUT/'native_identity.json').write_text(json.dumps(identity,indent=2)+'\\n')\n"
         "  (OUT/'process.json').write_text("),
        ("      name.startswith('ending_page') or name=='ending_return_to_attract.png')",
         "      name.startswith('ending_page') or name.startswith('postjoin_') or name=='ending_return_to_attract.png')"),
        ("      print('MK2_CURRENT_CAMPAIGN_PREVIEW_DATAURL data:image/png;base64,'+\n       base64.b64encode(preview.getvalue()).decode(),flush=True)",
         "      # Actual native PNG previews stay in the retained RAM host."),
        ("if re.match(r'^MK2_NAT_CAMPAIGN_(SELECT_ID|STAGE|LOSS|ENDING_START|ENDING_COMPLETED|RESULT) ',line)",
         "if re.match(r'^MK2_POSTENDING_(BEGIN|SELECT|SELECT_ID|MATCH|COMPLETE|FAILED) ',line) or re.match(r'^MK2_NAT_CAMPAIGN_(SELECT_ID|STAGE|LOSS|ENDING_START|ENDING_COMPLETED|RESULT) ',line)"),
        (' return result\n', ' return dict(result=result,images=images,text=chronology,guest=guest)\n'),
    ]
    for before, after in changes:
        need(source.count(before) == 1, 'Exact whole host adaptation: '+before)
        source = source.replace(before, after, 1)
    return source


def run():
    need(not OUT.exists() and not census.census(), 'One fresh actual native campaign, never restart a live one')
    physical = boundary.source_boundary()
    need(physical['passed'] and physical['physicalInputsExactlyUnchanged'], 'Whole previously qualified original physical Kano controller')
    text = (ROOT/LUA).read_text()
    need(not re.search(r':write_|write_[ui]\d+|load_?state|\.value\s*=(?!=)', text), 'Ordinary physical inputs and passive reads only')
    scope = dict(vars(original), __file__=__file__, native=native, census=census, OUT=OUT, LUA=LUA,
                 CONTROLLERS=CONTROLLERS, qualify_payload_metadata_warning=metadata_clean)
    source = capture_source()
    exec(compile(source, __file__+'::whole_current_campaign_host', 'exec'), scope)
    capture = scope['capture']()
    need(not census.census(), 'Original native child actually terminal')
    with gzip.open(OUT/'executed_postending_sources.json.gz', 'wt', encoding='utf-8') as stream:
        json.dump(dict(host=source, files={str(ROOT/name):(ROOT/name).read_text() for name in CONTROLLERS}), stream)
    return capture


if __name__ == '__main__':
    try:
        capture = run()
    except Exception as error:
        if OUT.exists():
            path=OUT/'postending_capture_failure.json'
            need(not path.exists(), 'Immutable actual capture failure')
            path.write_text(json.dumps(dict(passed=False,error=repr(error)),indent=2)+'\n')
        raise
    code.interact(banner='Same original terminal post-ending campaign: native images retained in RAM.', local=dict(capture=capture))
