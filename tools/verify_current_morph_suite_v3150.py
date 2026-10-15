"""Fresh candidate2753 real-input morphs; original full criteria unchanged.

Whole initialized guest independently reconstructed, all compiled inputs pinned.
This is not all morph branches, floor shadows/erase, arenas, audio or release.
"""
import inspect,json,hashlib,re
from pathlib import Path
import verify_native_friendship_palette_assembly_v2750 as assembly
import verify_human_shang as old_human
import verify_morph_render as old_render
import verify_human_shang_v3148 as human
import verify_morph_render_v3149 as render

ROOT=assembly.ROOT
OUT=ROOT/'audit_v3151_current_morph_suite_checked'
need=assembly.need

def unchanged_criteria():
    old=Path(old_human.__file__).read_text().replace(
      "CANDIDATE='diagnostic_v345_native_human_morph_binding'",
      "CANDIDATE='diagnostic_v2753_native_friendship_palette'").replace(
      "EXE='8E474E4B17759485BA54125CD06344FBA0AD89B5374DC34D0A8504DF167917EA'",
      "EXE='F7CE88667B33BA8AB7316F3C254B3B75A7A23ACA8C78524BB08B6E6055B90650'").replace(
      "PAYLOAD='82FE153FB56B46A6F9D42F493451AC3D59AD61713433714ACA7704E2881F8951'",
      "PAYLOAD='5646E839C73C4DB89BCF7CC87ECADBDA94B1E0D30EB1C0D2ED50A21A5524E23D'")
    need(old.strip()==Path(human.__file__).read_text().strip(),
      'Entire original human checker unchanged except explicit current matched build constants')
    old=Path(old_render.__file__).read_text().replace(
      'import verify_human_shang as human','import verify_human_shang_v3148 as human')
    need(old.strip()==Path(render.__file__).read_text().strip(),
      'Entire original art/DMA/palette/pivot/bitmap checker unchanged except explicit current provenance import')
    need(inspect.getsource(old_human.verify_log)==inspect.getsource(human.verify_log),
      'All original native command/store/restore/projectile/control criteria retained')
    need(inspect.getsource(old_render.verify_log)==inspect.getsource(render.verify_log),
      'All original full transition/handoff native drawing criteria retained')

def capture(folder,target,side,pins,guest,payload):
    def pin(path,wanted=None):
        path=Path(path).resolve();actual=assembly.sha(path)
        need(wanted is None or wanted==actual,'Unchanged captured input '+str(path))
        need(str(path)not in pins or pins[str(path)]==actual,'Consistent immutable source/evidence')
        pins[str(path)]=actual
    meta=json.loads((folder/'result.json').read_text(encoding='utf-8-sig'))
    before=json.loads((folder/'input_hashes_before.json').read_text(encoding='utf-8-sig'))
    info=json.loads((ROOT/human.CANDIDATE/'build-info.json').read_text(encoding='utf-8-sig'))
    need((meta['exit_code'],meta['lua_errors'],meta['candidate'],meta['executable_sha256'],
      meta['payload_sha256'],meta['target'],meta['side'],meta['profile'])==
      (0,0,human.CANDIDATE,human.EXE,human.PAYLOAD,target,side,'native'),
      'Actual terminal exact current candidate real-input case')
    need(before==meta['input_hashes'] and all(before.get(p)==v for p,v in info['input_hashes'].items()),
      'All compiled dependencies pinned both before and after execution')
    need((folder/'guest_maincpu.bin').read_bytes()==guest,
      'Whole actual initialized guest equals independent native source assembly')
    need((ROOT/human.CANDIDATE/'roms/mk2ks/mk2ks.mdata').read_bytes()==payload,
      'Whole actual payload equals independent native source assembly')
    for path,wanted in before.items():
        pin(path,wanted)
        source=Path(path)
        if source.suffix in('.lua','.ps1','.json'):
            pin(folder/'input_sources'/source.name,wanted)
        if source.suffix=='.lua':
            need(not re.search(r':write_|write_u\d+|\.value\s*=(?!=)|load_?state|:reset\(',source.read_text()),
              'No observer guest/register/AI/RNG/HP/state/reset assistance')
    log=(folder/'run.log').read_text(encoding='utf-8-sig')
    need(len(re.findall(r'^MK2_MORPH_GUEST frame=1 bytes=1048576 start=FF800000 stop=100000000 writes=0$',log,re.M))==1,
      'Single read-only whole initialized guest capture')
    need(not re.search(r'Fatal error|LUA ERROR|stack traceback|access violation',log,re.I),
      'No native emulator/observer failure')
    native=human.verify(folder,target,side,'native')
    drawing=render.verify(folder,target,side)
    need(native['passed'],'Full original native human morph acceptance '+str(native['errors']))
    need(drawing['passed'],'Full original native drawing acceptance '+str(drawing['errors']))
    need(native['gameplay_fields']==1001 and native['form_fields']>=512 and
      drawing['transition_fields']==24 and drawing['handoff_fields']==drawing['restored_handoff_fields']==8 and
      drawing['native_component_fields']==80 and len(drawing['visual'])==80 and
      all(v['score']==1.0 and v['visible']>0 and v['unoccluded']>0 for v in drawing['visual']),
      'Entire1001-field lifecycle, 24 transition holds,16 early native body handoffs,80 exact opaque component draws')
    for path in folder.rglob('*'):
        if path.is_file():pin(path)
    return dict(native=native,drawing=drawing,wholeActualGuestSourceBound=True,
      normalPhysicalButtonsOnly=True,allCompiledInputsUnchanged=True)

def verify():
    need(not OUT.exists(),'Never overwrite evidence')
    unchanged_criteria()
    pins=assembly.source_check()
    guest,old,payload,ends,ranges=assembly.expected()
    need(hashlib.sha256(guest).hexdigest().upper()=='65CE02355CD6B2830F4635FF1B8D55C1D0D22BA22E37ECF17B820DF26DA020E7',
      'Independent complete guest expected hash unchanged')
    cases={}
    for target in('kano','sonya'):
        for side in(1,2):
            folder=ROOT/f'audit_v3147_current_morph_{target}_p{side}'
            cases[f'{target}_p{side}']=capture(folder,target,side,pins,guest,payload)
    # Pin the original source decoders, original MK2/MK3 ROMs and every graphics bank.
    for folder in(ROOT/'mk2',ROOT/'mk3'):
        for path in folder.glob('*'):
            if path.is_file():pins[str(path.resolve())]=assembly.sha(path)
    for module in(assembly,assembly.prior,old_human,old_render,human,render,
      render.assets,render.animation,render.pixels,render.decoder,render.raster):
        path=Path(module.__file__);pins[str(path.resolve())]=assembly.sha(path)
    pins[str(Path(__file__).resolve())]=assembly.sha(__file__)
    report=dict(passed=True,candidate=human.CANDIDATE,cases=cases,
      originalHumanAndRenderCriteriaUnchanged=True,physicalCases=4,
      allGameplayFields=4004,actualTransitionFields=96,actualComponentFields=320,
      exactOriginalOpaqueComponentPixels=sum(v['visible'] for c in cases.values()for v in c['drawing']['visual']),
      ownNativeTimedRestorationAndPostRestoreControlsAccepted=True,
      originalDonorMorphArtAndFullNativeBodyPaletteHandoffsAccepted=True,
      allMorphBranchesAccepted=False,allFloorShadowsAndContinuousEraseAccepted=False,
      allArenasAudioAndFinishersAccepted=False,fullPortAcceptance=False,
      gameplaySourceOrPlayableBytesChanged=False,inputHashes=pins)
    OUT.mkdir();(OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items()if k not in('cases','inputHashes')},indent=2),flush=True)

if __name__=='__main__':verify()
