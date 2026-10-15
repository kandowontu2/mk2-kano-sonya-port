"""Unchanged full4460 native renderer for the three missing rare mirror roles."""
import argparse,hashlib,inspect,json,subprocess,traceback
from pathlib import Path
import run_tomb_mirror_random_drop_render_ram_v4460 as runtime
ROOT,need,sha=runtime.ROOT,runtime.need,runtime.sha

def paths(fighter,side):
    need((fighter,side) in (('sonya',1),('kano',2),('sonya',2)),
         'Only missing native roles; completed KanoP1 is never rerun')
    return (ROOT/f'audit_v4466_{fighter}_p{side}_random_drop_mirror_tomb_render_ram',
            ROOT/f'audit_v4467_{fighter}_p{side}_random_drop_mirror_tomb_render_checked')

def runner(fighter,side,delay):
    folder,output=paths(fighter,side)
    proof_path=ROOT/f'audit_v4459_tomb_mirror_random_drop_checked/{fighter}_p{side}_delay{delay:02d}/report.json'
    proof=json.loads(proof_path.read_text())
    need(proof['passed'] and proof['nativeRandomDropStateAndOriginal801CleanupAccepted'] and
         proof['fighter']==fighter and proof['side']==side and proof['physicalCommandDelay']==delay and
         proof['nativeBranch']['nativeDrop'] and all(sha(p)==h for p,h in proof['inputHashes'].items()),
         'Actual original whole earned/phase/source qualification before new native rendering')
    source=inspect.getsource(runtime.run);identity=17 if fighter=='kano' else 18
    changes=[("fighter,side,ids='kano',1,(17,17)",f"fighter,side,ids='{fighter}',{side},({identity},{identity})"),
       ('audit_v4459_tomb_mirror_random_drop_checked/kano_p1_delay10/report.json',str(proof_path.relative_to(ROOT)).replace('\\','/')),
       ("matrix['physicalCommandDelay']==10",f"matrix['physicalCommandDelay']=={delay}"),
       ("MK2KS_TOMB_COMMAND_DELAY='10'",f"MK2KS_TOMB_COMMAND_DELAY='{delay}'"),
       ('KanoP1 true mirror complete native scene RAM',f'{fighter.capitalize()}P{side} random-drop mirror complete native scene RAM'),
       ('KanoP1 mirror ',f'{fighter.capitalize()}P{side} random-drop mirror '),
       ('current3836KanoP1RandomDropMirrorNativeTombWholeRenderPaletteShadowEraseAccepted',
        'current3836RandomDropMirrorNativeTombWholeRenderPaletteShadowEraseAccepted')]
    for before,after in changes:
        need(source.count(before)==1,'Only declared character/physical slot/delay/reference/label adaptation: '+before)
        source=source.replace(before,after,1)
    scope=dict(runtime.__dict__);scope.update(__file__=__file__,CASE=folder,OUT=output)
    exec(compile(source,__file__+'::entire4460_missing_role_only','exec'),scope)
    return scope['run'],hashlib.sha256(source.encode()).hexdigest().upper()

def main():
    p=argparse.ArgumentParser();p.add_argument('--fighter',choices=('kano','sonya'),default='sonya')
    p.add_argument('--side',type=int,choices=(1,2),default=1);p.add_argument('--delay',type=int,default=4)
    a=p.parse_args();folder,output=paths(a.fighter,a.side)
    need(not folder.exists() and not output.exists(),'Every new actual native scene leaf unused')
    try:
        run,digest=runner(a.fighter,a.side,a.delay);report=run()
        report['entire4460RendererAdaptationSHA256']=digest
    except Exception as e:
        report=dict(passed=False,fighter=a.fighter,side=a.side,error=repr(e),traceback=traceback.format_exc(),fullPortAcceptance=False)
    need(not output.exists(),'Immutable current native result');output.mkdir()
    need(subprocess.run(['compact.exe','/C','/I','/Q','/S:'+str(output)],capture_output=True).returncode==0,
         'Compress new proof before writes')
    (output/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k not in ('inputHashes','nativeScene','nativeBranch')},indent=2),flush=True)
    raise SystemExit(0 if report['passed'] else 1)

if __name__=='__main__':main()
