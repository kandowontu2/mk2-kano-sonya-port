"""Current native grammar, invalid commands and three stock morph fallbacks.

All original per-field native/store/floor/restore/control criteria retained.
Not CPU random morph, every arena/finisher/audio/pixel or release acceptance.
"""
import hashlib,json,re
from pathlib import Path
import verify_native_friendship_palette_assembly_v2750 as assembly
import verify_human_shang_v3174 as human
import verify_morph_render_v3175 as render
import verify_native_morph_floor_projection_v3185 as floor
ROOT=assembly.ROOT;need=assembly.need
OUT=ROOT/'audit_v3192_current_morph_commands_checked'

def verify():
    need(not OUT.exists(),'Never overwrite evidence')
    floor.source_contract()
    dispatch=ROOT/'audit_v3189_current_morph_command_dispatch/report.json'
    job=json.loads(dispatch.read_text())
    expected=set()
    for side in(1,2):
        for target,profiles in(
          ('kano',('wrong_button','reversed','expired','extra_button','airborne')),
          ('sonya',('no_down','no_lp','no_block','extra_button','airborne','block2','block_first','lp_first'))):
            expected.update((target,side,profile)for profile in profiles)
        expected.update(('kano',side,profile)for profile in('stock_lp','stock_lk','stock_block'))
    need(job['passed']and job['captures']==32 and
      {(r['target'],r['side'],r['profile'])for r in job['cases'].values()}==expected and
      all(r['exitCode']==r['nativeExitCode']==0 for r in job['cases'].values()),
      'Exact independently specified32real human command cases all terminal')
    guest,old,payload,ends,ranges=assembly.expected()
    need(hashlib.sha256(guest).hexdigest().upper()=='65CE02355CD6B2830F4635FF1B8D55C1D0D22BA22E37ECF17B820DF26DA020E7',
      'Independently reconstructed whole current guest')
    pins=assembly.source_check();cases={}
    def pin(path,wanted=None):
        path=Path(path).resolve();actual=assembly.sha(path)
        need(wanted is None or actual==wanted,'Unchanged captured input '+str(path))
        need(str(path)not in pins or pins[str(path)]==actual,'Consistent immutable input')
        pins[str(path)]=actual
    info=json.loads((ROOT/human.CANDIDATE/'build-info.json').read_text(encoding='utf-8-sig'))
    need(assembly.sha(ROOT/human.CANDIDATE/'roms/mk2ks/mk2ks.mdata')==human.PAYLOAD and
      (ROOT/human.CANDIDATE/'roms/mk2ks/mk2ks.mdata').read_bytes()==
      (ROOT/'audit_v3169_native_morph_shadow_payload/roms/mk2ks/mk2ks.mdata').read_bytes(),
      'Entire corrected native payload independently reconstructed')
    positives=negatives=stock=0
    for target,side,profile in sorted(expected):
        folder=ROOT/f'audit_v3190_current_morph_{target}_p{side}_{profile}'
        meta=json.loads((folder/'result.json').read_text(encoding='utf-8-sig'))
        before=json.loads((folder/'input_hashes_before.json').read_text(encoding='utf-8-sig'))
        need((meta['exit_code'],meta['lua_errors'],meta['candidate'],meta['executable_sha256'],
          meta['payload_sha256'],meta['target'],meta['side'],meta['profile'])==
          (0,0,human.CANDIDATE,human.EXE,human.PAYLOAD,target,side,profile),
          'Exact actual matched case and native executable/payload')
        need(before==meta['input_hashes']and all(before.get(file)==value for file,value in info['input_hashes'].items()),
          'Every compiled dependency pinned before and after native execution')
        need((folder/'guest_maincpu.bin').read_bytes()==guest,'Whole actual initialized guest source-bound')
        for file,wanted in before.items():
            pin(file,wanted)
            if Path(file).suffix in('.lua','.ps1','.json'):pin(folder/'input_sources'/Path(file).relative_to(ROOT),wanted)
            if Path(file).suffix=='.lua':
                need(not re.search(r':write_|write_u\d+|\.value\s*=(?!=)|load_?state|:reset\(',Path(file).read_text()),
                  'No observer guest/register/identity/AI/health/RNG/reset assistance')
        log=(folder/'run.log').read_text(encoding='utf-8-sig')
        need(len(re.findall(r'^MK2_MORPH_GUEST frame=1 bytes=1048576 start=FF800000 stop=100000000 writes=0$',log,re.M))==1,
          'Actual full read-only initialized guest capture')
        proof=human.verify(folder,target,side,profile)
        need(proof['passed']and proof['gameplay_fields']==1001,
          'Entire unchanged original native lifecycle criterion '+str(proof['errors']))
        if profile in human.STOCK:stock+=1
        elif profile in human.POSITIVE:positives+=1
        else:negatives+=1
        cases[f'{target}_p{side}_{profile}']=dict(proof,wholeGuestSourceBound=True,
          allCompiledInputsUnchanged=True,normalPhysicalInputsOnly=True)
        for file in folder.rglob('*'):
            if file.is_file():pin(file)
    need((positives,negatives,stock)==(6,20,6),'Six Sonya chord variants,20 actual invalid/airborne rejections,six native stock morph fallbacks')
    for file,wanted in job['inputHashes'].items():pin(file,wanted)
    pin(dispatch);pin(Path(__file__))
    for module in(assembly,human,render,floor,floor.old_human,floor.old_render):pin(module.__file__)
    report=dict(passed=True,candidate=human.CANDIDATE,physicalCases=32,allGameplayFields=32032,
      SonyaChordVariantCases=positives,invalidAndAirborneRejectionCases=negatives,originalStockMorphFallbackCases=stock,
      originalWholeHumanNativeCriteriaUnchanged=True,allActualInitializedGuestsSourceBound=True,
      cases=cases,allCPUMorphsOrArenasAccepted=False,allPixelsFloorShadowsAndAudioAccepted=False,
      gameplayPayloadChanged=True,nativeGuestProgramChanged=False,fullPortAcceptance=False,inputHashes=pins)
    OUT.mkdir();(OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items()if k not in('cases','inputHashes')},indent=2),flush=True)

if __name__=='__main__':verify()
