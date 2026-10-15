"""Complete4401 pressed mirror renderer, remaining native character/slot cases.

Independent native jobs and RAM models; shared shadow inspector retains the
original3648 lock. No guest/palette/health/stage/position/RNG overrides. Frozen
KanoP1 result is reused, never rerun. Full-port and missing branch/audio gates
remain open even if all four observed pressed-mirror scenes pass.
"""
import concurrent.futures,hashlib,inspect,json,subprocess,traceback
from pathlib import Path
import run_pressed_mirror_render_ram_v4401 as runtime
ROOT,need,sha=runtime.ROOT,runtime.need,runtime.sha
OUT=ROOT/'audit_v4409_both_characters_both_slots_pressed_mirror_tomb_render'

def paths(fighter,side):
    need((fighter,side)in (('sonya',1),('kano',2),('sonya',2)),'Only remaining true native mirror roles')
    return (ROOT/f'audit_v4407_{fighter}_p{side}_pressed_mirror_tomb_render_ram',
      ROOT/f'audit_v4408_{fighter}_p{side}_pressed_mirror_tomb_render_checked')

def runner(fighter,side):
    source=inspect.getsource(runtime.run)
    identity=17 if fighter=='kano'else 18
    changes={"fighter,side,ids='kano',1,(17,17)":f"fighter,side,ids='{fighter}',{side},({identity},{identity})",
      'KanoP1 true mirror complete native scene RAM':f'{fighter.capitalize()}P{side} true mirror complete native scene RAM',
      'KanoP1 mirror ':f'{fighter.capitalize()}P{side} mirror ',
      'current3836KanoP1PressedMirrorNativeTombWholeRenderPaletteShadowEraseAccepted':'current3836PressedMirrorNativeTombWholeRenderPaletteShadowEraseAccepted'}
    for before,after in changes.items():
        need(source.count(before)==1,'Exact complete renderer identity/path-label adaptation: '+before)
        source=source.replace(before,after)
    folder,report=paths(fighter,side)
    scope=dict(runtime.__dict__);scope.update(__file__=__file__,CASE=folder,OUT=report)
    exec(compile(source,'<entire4361_native_mirror_render_'+fighter+'_p'+str(side)+'>','exec'),scope)
    return scope['run'],hashlib.sha256(source.encode()).hexdigest().upper()

def save_case(fighter,side):
    folder,output=paths(fighter,side);need(not folder.exists()and not output.exists(),'Never restart/overwrite an actual mirror scene')
    try:
        run,digest=runner(fighter,side);value=run();value['completeRendererAdaptationSHA256']=digest
    except Exception as error:value=dict(passed=False,fighter=fighter,side=side,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
    need(not output.exists(),'Fresh actual mirror result');output.mkdir()
    need(subprocess.run(['compact.exe','/C','/I','/Q','/S:'+str(output)],capture_output=True).returncode==0,'Compress report before write')
    file=output/'report.json';file.write_text(json.dumps(value,indent=2)+'\n')
    print(json.dumps(dict(fighter=fighter,side=side,passed=value['passed'],frames=value.get('sampledFrames'),error=value.get('error'))),flush=True)
    return value,file

def main():
    need(not OUT.exists(),'Fresh complete-scope mirror visual matrix')
    first=ROOT/'audit_v4403_kano_p1_pressed_mirror_tomb_render_checked/report.json'
    prior=json.loads(first.read_text());need(prior['passed']and prior['current3836KanoP1PressedMirrorNativeTombWholeRenderPaletteShadowEraseAccepted'],
      'Actual terminal current3836 KanoP1 full native mirror scene')
    pins=dict(prior['inputHashes']);pins[str(first)]=sha(first);pins[str(Path(__file__).resolve())]=sha(__file__)
    need(all(sha(path)==h for path,h in pins.items()),'All original frozen positive inputs/evidence unchanged')
    contexts=(('sonya',1),('kano',2),('sonya',2))
    need(all(not leaf.exists()for case in contexts for leaf in paths(*case)),'All new actual jobs fresh, no completed-case rerun')
    for case in contexts:runner(*case)
    with concurrent.futures.ThreadPoolExecutor(max_workers=3)as pool:
        futures=[pool.submit(save_case,*case)for case in contexts]
        results=[future.result()for future in futures]
    need(all(r['passed']for r,_ in results),'All remaining whole native mirror scenes passed without omitted/relaxed gates')
    cases=[dict(fighter=prior['fighter'],side=prior['side'],passed=True,report=str(first),
      frames=prior['sampledFrames'],nativeScene=prior['nativeScene'],nativeMirrorPaletteSelectors=prior['nativeMirrorPaletteSelectors'])]
    for report,path in results:
        need(report['current3836PressedMirrorNativeTombWholeRenderPaletteShadowEraseAccepted']and
          not report['allMirrorBranchesAndSlotsAccepted']and not report['fullPortAcceptance'],
          'Whole-scene bounded acceptance only, no imaginary mirror branches or full port')
        for p,h in report['inputHashes'].items():need(p not in pins or pins[p]==h,'All same immutable actual matrix inputs');pins[p]=h
        pins[str(path)]=sha(path)
        cases.append(dict(fighter=report['fighter'],side=report['side'],passed=True,report=str(path),
          frames=report['sampledFrames'],nativeScene=report['nativeScene'],nativeMirrorPaletteSelectors=report['nativeMirrorPaletteSelectors']))
    need({(r['fighter'],r['side'])for r in cases}=={('kano',1),('kano',2),('sonya',1),('sonya',2)},'Every true mirror character and physical slot')
    need(all(sha(path)==h for path,h in pins.items()),'Every actual source/report/log byte unchanged after terminal matrix')
    return dict(passed=True,candidate=runtime.NAME,cases=cases,inputHashes=pins,priorKanoP1NotRerun=True,
      actualTrueMirrorRenderContexts=4,actualWholeVisibleFields=sum(r['frames']for r in cases),
      actualExactVisibleRGBPixels=sum(r['frames']for r in cases)*400*254,
      current3836BothCharactersBothPhysicalSlotsPressedMirrorTombWholeRenderPaletteShadowEraseAccepted=True,
      mirrorDropAndPressedControlBranchesAccepted=True,allMirrorBranchesAccepted=False,allStageVictimAudioAccepted=False,
      publicPlayableOrReleaseChanged=False,rawImageAudioVRAMROMCopiesWritten=0,fullPortAcceptance=False,scope=__doc__)

if __name__=='__main__':
    try:report=main()
    except Exception as error:report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
    need(not OUT.exists(),'Never overwrite partial/complete native mirror visual matrix');OUT.mkdir()
    need(subprocess.run(['compact.exe','/C','/I','/Q','/S:'+str(OUT)],capture_output=True).returncode==0,'Matrix compressed before write')
    (OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items()if k not in('inputHashes','cases')},indent=2),flush=True)
    raise SystemExit(0 if report['passed']else 1)
