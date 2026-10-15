"""Current Kano and stock Liu control, physical held Block vs ordinary Freeze.

No guest/HP/AI writes or emulation state loading. Keep real images in RAM.
"""
import code,gzip,inspect,json,os
from pathlib import Path
import native_ai_response_full_context as native
import native_process_census_v6647 as census
import run_normal_subzero_freeze_v5033 as original
ROOT,need,sha=native.ROOT,native.need,native.sha
LUA='mk2ks_native_block_freeze_diagnostic.lua'

def read_log(folder):
    with gzip.open(folder/'run.log.gz','rt',encoding='utf-8') as stream:return stream.read()

def capture_source():
    source=inspect.getsource(original.capture)
    changes=[
        ("audit_v5034_normal_subzero_{fighter}_p{side}","audit_native_block_freeze_setup_checked_{fighter}_p{side}"),
        ("controllers=[ROOT/LUA,ROOT/'mk2ks_stock_fatality_v1021.lua']",
         "controllers=[ROOT/LUA,ROOT/'mk2ks_normal_subzero_freeze_v5031.lua',ROOT/'mk2ks_stock_fatality_v1021.lua']"),
        ("'-samplepath',str(ROOT/'samples')","'-samplepath',str(build/'samples')+';'+str(ROOT/'samples')"),
        (' proof_guest=proof_gfx=None;scenes=[]',' proof_guest=proof_gfx=None;scenes=[];images=[]'),
        ("with(folder/'run.log').open('w',encoding='utf-8')as log:","with gzip.open(folder/'run.log.gz','wt',encoding='utf-8')as log:"),
        (" log=(folder/'run.log').read_text();err=(folder/'stderr.log').read_text()"," log=read_log(folder);err=(folder/'stderr.log').read_text()"),
        ("      print('MK2_NORMAL_FREEZE_PREVIEW_DATAURL data:image/png;base64,'+base64.b64encode(png.getvalue()).decode(),flush=True)",
         "      images.append(Image.frombytes('RGB',(400,254),raw,'raw','BGRX'))"),
        ("  (folder/'process.json').write_text(json.dumps(dict(pid=process.pid,command=command),indent=2)+'\\n')",
         "  identity=next((r for r in census.census() if r['ProcessId']==process.pid),None)\n"
         "  need(identity and identity['ParentProcessId']==os.getpid(),'Actual known native child creation/command identity')\n"
         "  (folder/'process.json').write_text(json.dumps(dict(pid=process.pid,command=command,actualWindowsIdentity=identity),indent=2)+'\\n')"),
        ('  native_exit=process.wait()',
         "  native_exit=process.wait()\n (folder/'native_terminal.json').write_text(json.dumps(dict(pid=process.pid,nativeExit=native_exit,actualWindowsIdentity=identity),indent=2)+'\\n')"),
        (' return meta',' return dict(meta=meta,images=images,text=log,guest=guest)'),
    ]
    for before,after in changes:
        need(source.count(before)==1,'Exact complete physical Freeze host adaptation: '+before)
        source=source.replace(before,after,1)
    return source

def run(fighter):
    need(not census.census(),'No live native test before fresh diagnostic')
    source=capture_source()
    scope=dict(vars(original),__file__=__file__,native=native,census=census,LUA=LUA,read_log=read_log,gzip=gzip)
    exec(compile(source,__file__+'::whole_original_freeze_host','exec'),scope)
    capture=scope['capture'](fighter,2)
    folder=ROOT/f'audit_native_block_freeze_setup_checked_{fighter}_p2'
    with gzip.open(folder/'executed_block_freeze_sources.json.gz','wt',encoding='utf-8') as stream:
        json.dump(dict(host=source,files={str(ROOT/p):(ROOT/p).read_text() for p in (LUA,'mk2ks_normal_subzero_freeze_v5031.lua','mk2ks_stock_fatality_v1021.lua')}),stream)
    return capture

if __name__=='__main__':
    captures={}
    for fighter in ('kano','liu_kang'):
        try:captures[fighter]=run(fighter)
        except Exception as error:
            folder=ROOT/f'audit_native_block_freeze_setup_checked_{fighter}_p2'
            if folder.exists():
                path=folder/'capture_failure.json';need(not path.exists(),'Original immutable failure')
                path.write_text(json.dumps(dict(passed=False,error=repr(error)),indent=2)+'\n')
            raise
    code.interact(banner='Same terminal native held-Block comparison, original images retained in RAM.',local=dict(captures=captures))
