"""Current native Sonya earned tower, followed by ordinary fresh Kano P1 join."""
import code,gzip,inspect,json,os,re
from pathlib import Path
import native_ai_response_full_context as native
import native_process_census_v6647 as census
import run_extended_sonya_p1_campaign_v5207 as original
from capture_native_postending_join import metadata_clean
ROOT,need,sha=native.ROOT,native.need,native.sha
OUT=ROOT/'audit_native_sonya_p1_postending_kano'
LUA='mk2ks_native_sonya_p1_postending_kano.lua'
CONTROLLERS=[LUA,'mk2ks_native_kano_p2_postending_sonya.lua',*original.CONTROLLERS]

def capture_source():
    source=inspect.getsource(original.capture)
    changes=[
        ("'-samplepath',str(ROOT/'samples')","'-samplepath',str(candidate/'samples')+';'+str(ROOT/'samples')"),
        ("stdout=subprocess.PIPE,stderr=errors,text=True,encoding='utf-8',errors='strict')as process:",
         "stdout=subprocess.PIPE,stderr=errors,text=True,encoding='utf-8',errors='strict',creationflags=subprocess.CREATE_NO_WINDOW)as process:"),
        ("  (OUT/'process.json').write_text(",
         "  identity=next((r for r in census.census() if r['ProcessId']==process.pid),None)\n"
         "  need(identity and identity['ParentProcessId']==os.getpid() and identity['createdUnix']>=started-1,'Actual known native child creation identity')\n"
         "  (OUT/'native_identity.json').write_text(json.dumps(identity,indent=2)+'\\n')\n"
         "  (OUT/'process.json').write_text("),
        ('  code=process.wait()',
         "  code=process.wait()\n (OUT/'native_terminal.json').write_text(json.dumps(dict(nativeExit=code,identity=identity),indent=2)+'\\n')"),
        ("      name.startswith('ending_page') or name=='ending_return_to_attract.png')",
         "      name.startswith('ending_page') or name.startswith('postjoin_') or name=='ending_return_to_attract.png')"),
        ("      print('MK2_CURRENT_CAMPAIGN_PREVIEW_DATAURL data:image/png;base64,'+\n       base64.b64encode(preview.getvalue()).decode(),flush=True)",
         '      # Original native pixels retained in RAM, never printed as base64.'),
        ("if re.match(r'^MK2_NAT_CAMPAIGN_(SELECT_ID|STAGE|LOSS|ENDING_START|ENDING_COMPLETED|RESULT) ',line)",
         "if re.match(r'^MK2_POSTENDING_(BEGIN|SELECT|SELECT_ID|MATCH|COMPLETE|FAILED) ',line) or re.match(r'^MK2_NAT_CAMPAIGN_(SELECT_ID|STAGE|LOSS|ENDING_START|ENDING_COMPLETED|RESULT) ',line)"),
        (' return result\n',' return dict(result=result,images=images,text=chronology,guest=guest)\n'),
    ]
    for before,after in changes:
        need(source.count(before)==1,'Exact whole qualified Sonya host adaptation: '+before)
        source=source.replace(before,after,1)
    compile(source,__file__+'::whole_original_Sonya_host','exec')
    return source

def run():
    need(not OUT.exists() and not census.census(),'One new cold native process, never restart a live run')
    previous=ROOT/'audit_v5214_extended_sonya_p1_whole_campaign_checked/report.json'
    accepted=json.loads(previous.read_text())
    need(accepted['passed'] and accepted['case']['unassisted_clear_proven'] and
         accepted['case']['player']=='sonya' and accepted['case']['human_slot']==1,
         'Actual previous complete tested-prime/Kitana/Jax/Subzero Sonya controller')
    before=accepted['case'].get('inputHashes',accepted.get('inputHashes',{}))
    for name in original.CONTROLLERS:
        path=ROOT/name
        need(before.get(str(path))==sha(path),'Every previously qualified whole physical controller unchanged: '+name)
    need(all(not re.search(r':write_|write_[ui]\d+|load_?state|\.value\s*=(?!=)',(ROOT/name).read_text())
             for name in CONTROLLERS),'Only ordinary buttons and read-only source/taps; no game assistance')
    source=capture_source()
    scope=dict(vars(original),__file__=__file__,native=native,census=census,OUT=OUT,LUA=LUA,
               CONTROLLERS=CONTROLLERS,qualify_payload_metadata_warning=metadata_clean)
    exec(compile(source,__file__+'::whole_original_Sonya_host','exec'),scope)
    capture=scope['capture']()
    with gzip.open(OUT/'executed_sonya_postending_sources.json.gz','wt',encoding='utf-8') as stream:
        json.dump(dict(host=source,files={str(ROOT/p):(ROOT/p).read_text() for p in CONTROLLERS}),stream)
    return capture

if __name__=='__main__':
    try:capture=run()
    except Exception as error:
        if OUT.exists():
            failure=OUT/'capture_failure.json';need(not failure.exists(),'Original actual failure preserved')
            failure.write_text(json.dumps(dict(passed=False,error=repr(error)),indent=2)+'\n')
        raise
    code.interact(banner='Same native terminal Sonya ending/fresh Kano join; no gameplay acceptance until independently checked.',local=dict(capture=capture))
