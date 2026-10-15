"""Actual unassisted native bubble palette ownership and reset, both slots.
Source-bound isolated candidate; every palette word/store replayed from one
baseline. Actual original task/sprite reclamation, native reference release
and unchanged physical scene chronology required. Not full-port acceptance.
"""
import argparse, copy, json, re, traceback
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import inspect_current_friendship_palette_lifecycle_v2732 as old
import verify_native_friendship_palette_assembly_v2750 as assembly

life=old.life
ROOT=assembly.ROOT
need=old.need
PALETTE=0xfffe2800

def palette_check(rows,control,allocated,side):
    # Reuse the exact complete-table replay, native store arithmetic and
    # independent constructor/task binding checks. The old defect diagnostic
    # intentionally allows source mismatch; this candidate must eliminate it.
    result=old.palette_check(rows,control,allocated,side)
    need(result['actualAllocatorEntrySource']==0xfecdf710 and result['actualPaletteTableSource']==PALETTE,
         'Typed native router owns genuine bubble palette instead of stock ID-zero row')
    need(result['actualConstructorReferenceCount']==1,'Exactly one original bubble palette reference')
    index=result['actualPaletteIndex'];cell=old.PAL_FIRST+index*old.PAL_STRIDE
    reset=control['actualPointerRetirement']
    entries=life.select(rows,'RELEASE_ENTRY')
    releases=[r for r in entries if life.number(r,'frame')==reset and
              life.pointer(r,'a8')==allocated['object'] and life.pointer(r,'a0')==result['actualEncodedPalette']]
    need(len(releases)==1,'Exactly one real original release call for actual bubble at native pool reset')
    drops=[r for r in life.select(rows,'TABLE_STORE') if life.pointer(r,'at')==cell+0x20 and
           life.number(r,'frame')==reset and life.pointer(r,'pc')==0xff80d710 and
           life.pointer(r,'before')==1 and life.pointer(r,'data')==0 and life.pointer(r,'a8')==allocated['object']]
    need(len(drops)==1 and result['actualNativeBubblePaletteReferenceReclaimed'],
         'Original reference decrement to zero at scene reset, never early or omitted')
    all_counts=[r for r in life.select(rows,'TABLE_STORE') if life.pointer(r,'at')==cell+0x20 and
                control['action']<life.number(r,'frame')<=reset]
    need(not any(life.pointer(r,'pc')==0xff80d710 and life.number(r,'frame')<reset for r in all_counts),
         'Owned palette remains allocated throughout live bubble drawing')
    for r in life.select(rows,'STATE'):
        if life.number(r,'frame')<reset and life.number(r,'frame')>=life.number(life.select(rows,'CONSTRUCT')[0],'frame'):
            words=old.words(r)
            need((words[index*4]|words[index*4+1]<<16)==PALETTE and words[index*4+2]==1,
                 'Every live native field retains exactly the bubble source and reference')
    stamps=[r for r in life.select(rows,'TABLE_STORE') if life.pointer(r,'at')==cell+0x30 and
            life.number(r,'frame')==reset and life.pointer(r,'pc')==0xff80d770]
    need(len(stamps)==1,'Original palette release writes native reuse-delay clock')
    result.update(ownedPaletteSourceAccepted=True,actualNativeReleaseFrame=reset,
                  actualNativeReleaseClockStore=stamps[0],noPrematurePaletteRelease=True)
    return result

def binding(folder):
    meta=json.loads((folder/'result.json').read_text(encoding='utf-8-sig'))
    before=json.loads((folder/'inputs_before.json').read_text(encoding='utf-8-sig'))
    build_path=ROOT/assembly.NAME/'build-info.json'
    build=json.loads(build_path.read_text(encoding='utf-8-sig'))
    need(meta['exit_code']==0 and meta['candidate']==build['name']==assembly.NAME and meta['winner']=='kano' and
         meta['side'] in (1,2) and meta['guest_writes']==0 and meta['assistance']=='none' and not meta['cheats_enabled'] and
         meta['command_case']=='positive' and meta['samples_enabled'] and meta['observation']==1600 and
         meta['requested_gap']==160 and before==meta['input_hashes'],'Actual terminal unassisted candidate capture')
    need(meta['executable_sha256']==build['executable_sha256'] and meta['payload_sha256']==build['payload_sha256'] and
         all(before.get(file)==wanted for file,wanted in build['input_hashes'].items()),'Exact executed compiled candidate and every recorded build input')
    pins=assembly.source_check()
    def pin(path,wanted=None):
        path=str(path);actual=assembly.sha(path)
        need(wanted is None or actual==wanted,'Immutable candidate dependency '+path)
        need(path not in pins or pins[path]==actual,'Consistent candidate dependency '+path)
        pins[path]=actual
    for file,wanted in before.items():
        pin(file,wanted)
        if Path(file).suffix in ('.lua','.ps1','.json'):pin(folder/'input_sources'/Path(file).name,wanted)
    pin(build_path);pin(ROOT/assembly.NAME/'mkport_candidate.exe',build['executable_sha256'])
    frozen=ROOT/assembly.NAME/'input_sources/mame-mkp/src'
    prior=ROOT/assembly.prior.NAME/'input_sources/mame-mkp/src'
    for file in frozen.rglob('*'):
        if file.is_file() and file.name!='midtunit_m.cpp':
            rel=file.relative_to(frozen)
            need(file.read_bytes()==(prior/rel).read_bytes(),'Every non-machine compiled source unchanged '+str(rel))
            pin(file);pin(prior/rel)
    need((frozen/'mame/midway/midtunit_m.cpp').read_bytes()==assembly.SOURCE.read_bytes(),
         'Exactly compiled reviewed native machine-source patch')
    old_runner=(ROOT/'tools/run_current_friendship_palette_lifecycle_v2730.ps1').read_text()
    need(old_runner.replace('diagnostic_v1836_ball_register_boundary',assembly.NAME)==
         (ROOT/'tools/run_native_friendship_palette_lifecycle_v2754.ps1').read_text(),
         'Entire physical runner unchanged except candidate path/name')
    guest,previous,payload,_,ranges=assembly.expected()
    need((folder/'guest_maincpu.bin').read_bytes()==guest and
         (ROOT/assembly.NAME/'roms/mk2ks/mk2ks.mdata').read_bytes()==payload,
         'Whole actual candidate guest and unchanged donor payload independently assembled')
    need(build['expected_guest_sha256']==__import__('hashlib').sha256(guest).hexdigest().upper(),
         'Compiled manifest agrees with independent whole guest reconstruction')
    log=(folder/'run.log').read_text(encoding='utf-8-sig')
    need(not re.search(r'LUA ERROR|fatal error|access violation|stack traceback|WRONG CHECKSUMS',log,re.I),
         'No native or observer runtime errors')
    return meta,guest,payload,pins,pin

def verify(folder):
    meta,guest,payload,pins,pin=binding(folder);side=meta['side']
    native_rows=life.native.scene.previous.parse(folder/'run.log')
    image=life.native.graphics.graphics(pins)
    control=life.native.inventory(native_rows,'kano',side,guest,image)
    prior_log=ROOT/f'audit_v2731_current_kano_friendship_palette_lifecycle_p{side}/run.log'
    pin(prior_log)
    physical=lambda rows:[(tag,r) for tag,r in rows if not tag.startswith('SHADOW_')]
    need(physical(native_rows)==physical(life.native.scene.previous.parse(prior_log)),
         'All real input/health/pose/child/WIN/audio-cue and next-screen records unchanged')
    rows=old.parse(folder/'run.log');life_rows=life.parse(folder/'run.log')
    allocated=life.check(life_rows,control,'kano',side)
    result=palette_check(rows,control,allocated,side)
    cleanup=old.lifecycle_check(life_rows,rows,control,allocated)
    outcomes=[]
    ctor=next(i for i,(tag,r) in enumerate(rows) if tag=='CONSTRUCT_TABLE')
    release=next(i for i,(tag,r) in enumerate(rows) if tag=='RELEASE_ENTRY' and life.number(r,'frame')==control['actualPointerRetirement'] and life.pointer(r,'a8')==allocated['object'])
    decrement=next(i for i,(tag,r) in enumerate(rows) if tag=='TABLE_STORE' and life.number(r,'frame')==control['actualPointerRetirement'] and life.pointer(r,'pc')==0xff80d710 and life.pointer(r,'a8')==allocated['object'])
    index=result['actualPaletteIndex'];wrong=rows[ctor][1]['table'].split(',');parts=wrong[index].split(':');parts[0]='FFADBBD0';wrong[index]=':'.join(parts)
    for name,at,key,value,label in (
        ('stock_proxy_palette_record',ctor,'table',','.join(wrong),'Every actual complete palette snapshot'),
        ('missing_native_palette_release',release,None,None,'Exactly one real original release call'),
        ('missing_actual_reference_decrement',decrement,None,None,('Every actual complete palette snapshot','Each original palette store matches previous')),
        ('wrong_original_release_route',decrement,'pc','FF80CD90','Actual zero reference comes from observed original reset call'),
        ('wrong_original_release_arithmetic',decrement,'data','FFFF','Original palette release decrements')):
        changed=list(rows)
        if key is None:changed.pop(at)
        else:changed[at]=(changed[at][0],dict(changed[at][1],**{key:value}))
        need(changed!=rows,'Non-vacuous actual candidate corruption')
        try:palette_check(changed,control,allocated,side)
        except ValueError as error:
            labels=(label,) if isinstance(label,str) else label
            need(any(wanted in str(error) for wanted in labels),'Specific actual invariant '+name+': '+str(error))
            outcomes.append(dict(name=name,rejectedBy=str(error)))
        else:raise ValueError('Corrupted actual native palette accepted '+name)
    need(palette_check(rows,control,allocated,side)==result,'Final untouched complete candidate palette control')
    files=[file for file in folder.rglob('*') if file.is_file()]
    with ThreadPoolExecutor(max_workers=4) as pool:
        for file,actual in zip(files,pool.map(assembly.sha,files)):
            need(str(file) not in pins or pins[str(file)]==actual,'Consistent final actual capture pin')
            pins[str(file)]=actual
    pin(__file__);life.native.scene.launch.module_pins(pins)
    return dict(passed=True,candidate=assembly.NAME,fighter='kano',side=side,control=control,**result,**cleanup,
                wholeActualGuestAndPayloadReconstructed=True,physicalInputsAndNativeSceneChronologyUnchanged=True,
                actualPaletteOwnershipAndNativeReferenceCleanupAccepted=True,rejectedSpecificCounterexamples=outcomes,
                gameChanged=True,fullFinisherAcceptance=False,fullPortAcceptance=False,inputHashes=pins,scope=__doc__)

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('folder',type=Path);parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args();need(not args.output.exists(),'Never overwrite actual candidate evidence')
    try:report=verify(args.folder)
    except Exception as error:report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
    args.output.mkdir();(args.output/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({key:value for key,value in report.items() if key!='inputHashes'},indent=2),flush=True)
    raise SystemExit(0 if report['passed'] else 1)
