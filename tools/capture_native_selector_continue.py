"""Full four-route paid continues and ordinary controls on CURRENT selector.

Keep all original loss/payment/ownership/UI/raster/control/fault predicates.
Add whole actual HIGH1MiB/OWNED2MiB/reservedGFX64KiB verification in EACH game.
The legacy18976-byte UI-graphics slice remains explicitly limited, never full
gfxrom acceptance. Original native handles/media remain RAM-only.
"""
import code,inspect,json,traceback
from pathlib import Path
from types import SimpleNamespace
import capture_native_kano_laser_cross_continue as prior
import verify_native_selector_layers_startup as startup

ROOT,need,sha=prior.ROOT,prior.need,prior.sha
INIT=ROOT/'audit_native_selector_continue_initializer'
PREFIX='audit_native_selector_continue'
LUA=ROOT/'mk2ks_native_selector_continue.lua'
RAM_CASES={}
COMPLETED=[]
NATIVE_HANDLES={}
WINDOWS={}


def expectation():
    need(not INIT.exists()and not startup.initial.identity.census(),'Fresh independent models, no unknown original native game')
    build_path=ROOT/startup.NAME;meta_path=build_path/'build-info.json'
    build=json.loads(meta_path.read_text(encoding='utf-8-sig'));cold_path=startup.OUT/'report.json';cold=json.loads(cold_path.read_text())
    restored=json.loads((build_path/'restoration.json').read_text(encoding='utf-8-sig'))
    need(cold['passed']and cold['actualNativeInitializedWindowsAccepted']and
         sha(build_path/'mkport_candidate.exe')==build['executable_sha256']and
         sha(build_path/'roms/mk2ks/mk2ks.mdata')==build['payload_sha256']and
         restored['passed']and restored['native_build_exit']==0 and
         all(sha(p)==h for p,h in restored['restored_actual_preexisting_files'].items())and
         not(ROOT/'mame-mkp/build/mingw-gcc').exists(),'Exact private current build, original dirty files restored, compiler cache absent')
    pins={}
    for p,h in cold['inputHashes'].items():need(sha(p)==h,'All frozen current source/model/startup inputs');pins[p]=h
    INIT.mkdir();wanted=startup.expected(INIT);WINDOWS.update(wanted)
    need({k:startup.initial.digest(v)for k,v in wanted.items()}==cold['actualWindowHashes'],'Independent full current initialized models')
    gfx=prior.native_base.ui.graphics.expected_gfx()
    need(len(gfx)==18976 and startup.initial.digest(gfx)=='29F765CC8B72A446029A5BA9F46E6F98E77BEB5285BFEC89E0335D2BF3A19076',
         'Exactly the original independently decoded11944+7032 UI graphics bytes, not full32MiB gfxrom')
    for p in (Path(__file__),Path(prior.__file__),Path(startup.__file__),meta_path,cold_path,LUA,
        ROOT/'mk2ks_native_shang_drain_startup.lua',ROOT/'mk2ks_cross_continue_adaptive.lua',
        ROOT/'audit_native_selector_held_checked/report.json',ROOT/'audit_native_selector_navigation_checked/report.json'):
        pins[str(p.resolve())]=sha(p)
    for p in prior.adaptive.DEPENDENCIES:
        pins[str(p.resolve())]=sha(p)
        if p.suffix=='.lua':
            need(not prior.original.scope['re'].search(r':write_|write_[ui]\d+|\.value\s*=(?!=)|load_?state|plugin\.cheat',p.read_text()),
                 'Every original actually loaded physical controller/passive observer refuses game-state writes')
    report=dict(passed=True,sourceOnlyAccepted=True,wholeExpectedGuestSHA256=build['expected_guest_sha256'],
        limitedExpectedUIGFXSHA256=startup.initial.digest(gfx),limitedExpectedUIGFXBytes=18976,
        actualFullNativeWindowsStillRequiredInEveryCase=True,expectedWindowHashes=cold['actualWindowHashes'],
        inputHashes=pins,newBuilds=0,newROMCopies=0,newRawMedia=0,newZIPs=0,
        latestPlayableChanged=False,goalStatus='active',fullPortAcceptance=False)
    (INIT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    current=SimpleNamespace(ROOT=ROOT,NAME=startup.NAME,EXE_SHA=build['executable_sha256'],
        GUEST_SHA=build['expected_guest_sha256'],PAYLOAD_SHA=build['payload_sha256'],__file__=__file__,
        expected=lambda:wanted['high'],expected_gfx=lambda:gfx)
    return wanted['high'],gfx,build,current


def functions():
    collector=inspect.getsource(prior.collector)
    boundary='    scope=dict(original.scope,__file__=__file__,current=current,contract=contract,gate=contract.gate,'
    additions='''    extra=(
        ("started=time.time();native=None;errors=[];proofs={};images={};digests=[]",
         "started=time.time();native=None;errors=[];proofs={};images={};digests=[];cold_buffers={k:bytearray()for k in WINDOWS}"),
        ("  (out/'process.json').write_text", "  NATIVE_HANDLES[f'{fighter}_p{side}_to_{target}']=dict(process=process,command=command,folder=out)\\n  (out/'process.json').write_text"),
        ("native=matches[0]", "native=matches[0];need(native['CommandLine']==subprocess.list2cmdline(command),'Exact actual full current native command');NATIVE_HANDLES[f'{fighter}_p{side}_to_{target}']['identity']=native"),
        ("('MK2_SC_GUEST ','MK2_SC_GFX ','MK2_SC_RGB ')", "('MK2_SC_GUEST ','MK2_SC_GFX ','MK2_SC_RGB ','MK2_DRAIN_STARTUP ')"),
        ("      if tag.endswith(('GUEST','GFX')):",
         "      if tag=='MK2_DRAIN_STARTUP':\\n"
         "       kind=r['kind'];need(kind in cold_buffers and int(r['offset'])==len(cold_buffers[kind])and len(raw)==int(r['bytes'])and r['writes']=='0'and r['assistance']=='none'and int(r['start'],16)==(0x1fb0000 if kind=='graphics'else 0),'Every complete actual initialized chunk')\\n"
         "       cold_buffers[kind].extend(raw)\\n"
         "       need(len(cold_buffers[kind])<=len(WINDOWS[kind]),'No duplicate/overflow actual initialized bytes')\\n"
         "       if len(cold_buffers[kind])==len(WINDOWS[kind]):\\n"
         "        need(bytes(cold_buffers[kind])==WINDOWS[kind],'Entire actual current '+kind+' equals independent model in THIS continue game')\\n"
         "        proofs['cold_'+kind]=dict(bytes=len(cold_buffers[kind]),sha256=hashlib.sha256(cold_buffers[kind]).hexdigest().upper(),everyActualByteComparedInRAM=True)\\n"
         "      elif tag.endswith(('GUEST','GFX')):"),
        ("len(proofs)==2", "len(proofs)==5"),
        ("  need(not re.search(r'LUA ERROR|stack traceback|fatal error|access violation',text,re.I)",
         "  need(text.count('MK2_DRAIN_STARTUP_COMPLETE writes=0 assistance=none')==1,'Exactly one full current initialized-window completion')\\n  need(not re.search(r'LUA ERROR|stack traceback|fatal error|access violation',text,re.I)"),
        ("        newBuilds=0,newROMCopies=0,newRawMedia=0,newZIPs=0,canonicalCMDUsed=False,publicPlayableChanged=False,fullPortAcceptance=False)",
         "        newBuilds=0,newROMCopies=0,newRawMedia=0,newZIPs=0,canonicalCMDUsed=False,limitedUIGFXBytes=18976,fullGFXRegionAccepted=False,fullCurrentHIGHOWNEDReservedGFXAccepted=True,publicPlayableChanged=False,fullPortAcceptance=False)"))
    for before,after in extra:source=replace(source,before,after)
'''
    need(collector.count(boundary)==1,'One whole original native collector compilation boundary')
    collector=collector.replace(boundary,additions+boundary,1)
    before='DEPENDENCIES=contract.DEPENDENCIES,RAM_CASES=RAM_CASES)'
    collector=prior.replace(collector,before,'DEPENDENCIES=contract.DEPENDENCIES,RAM_CASES=RAM_CASES,WINDOWS=WINDOWS,NATIVE_HANDLES=NATIVE_HANDLES,LUA=LUA)')
    scope=dict(vars(prior),ROOT=ROOT,INIT=INIT,PREFIX=PREFIX,RAM_CASES=RAM_CASES,COMPLETED=COMPLETED,
        NATIVE_HANDLES=NATIVE_HANDLES,WINDOWS=WINDOWS,LUA=LUA,expectation=expectation,__file__=__file__)
    for name in ('contracts','qualification','next_case','run'):
        exec(compile(inspect.getsource(getattr(prior,name)),__file__+'::whole_original_'+name,'exec'),scope)
    exec(compile(collector,__file__+'::whole_original_collector_plus_full_current_windows','exec'),scope)
    return scope


if __name__=='__main__':
    state=None
    try:
        state=functions();state['run']('kano',1)
        for fighter,side in (('sonya',1),('kano',2),('sonya',2)):state['next_case'](fighter,side)
    except Exception as error:
        failure=ROOT/'audit_native_selector_continue_failure'
        need(not failure.exists(),'Preserve actual original current continue failure');failure.mkdir()
        (failure/'report.json').write_text(json.dumps(dict(passed=False,error=repr(error),traceback=traceback.format_exc(),
            inputHashes={str(Path(__file__).resolve()):sha(__file__)},fullPortAcceptance=False),indent=2)+'\n')
        print(json.dumps(dict(passed=False,error=repr(error),traceback=traceback.format_exc())),flush=True)
    code.interact(banner='Original current native continue handles and rasters retained; never timeout-reboot.',
        local=dict(cases=RAM_CASES,state=state,handles=NATIVE_HANDLES))
