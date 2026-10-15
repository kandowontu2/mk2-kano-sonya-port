"""Fresh twenty-case regressions on the native split invariant-blood candidate.

Run the original scoped pixel/geometry proofs, independently reconstruct the
whole current ROM, and compare established native observations and actual
rendered artifacts. Historical source hashes resolve only to exact archived
source files; no old evidence or canonical source is rewritten.
"""
import hashlib,json,re
from pathlib import Path
from PIL import Image
import verify_native_arm_palette_v1074 as arms
import verify_native_split_blood_v1133 as split
import verify_jax_clap_positions_v1036 as jax
import verify_rolling_heads_v1014 as baraka
import verify_native_torso_art_v980 as cage
import verify_native_inflation_art_v989 as kitana
import verify_native_death_grounding_v990 as reptile

ROOT=arms.ROOT;CANDIDATE=split.CANDIDATE
OUT=ROOT/'audit_v1141_native_regressions_after_split_blood_checked'
DRIVER=ROOT/'mame-mkp/src/mame/midway/midtunit_m.cpp'
ARCHIVED_DRIVER=ROOT/'audit_v1017_owned_rolling_heads_checkpoint/input_sources/mame-mkp/src/mame/midway/midtunit_m.cpp'
GROUPS=(
 ('cage',1005,979,'owned_torso','MK2_STOCK_HEAD_V921','MK2_CAGE_TORSO_V979',185,cage),
 ('kitana',1006,987,'owned_inflation','MK2_STOCK_HEAD_V921','MK2_INFLATION_ART_V938',276,kitana),
 ('reptile',1008,988,'native_death_grounding','MK2_REPTILE_V879','MK2_DEATH_ART_V897',187,reptile))

def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest().upper()
def lines(text,prefix):return re.findall(r'^'+re.escape(prefix)+r'_.*$',text,re.M)
def cases(killer):return tuple(f'audit_v1136_{killer}_{name}_p{side}_split_blood_regression' for name in ('kano','sonya') for side in (1,2))

def verify():
 errors=[];pins={};summaries={};historical_sources=[]
 def need(ok,label):
  if not ok:errors.append(label)
 def inputs(result,historical=False):
  for filename,wanted in result['input_hashes'].items():
   path=Path(filename)
   if historical and path==DRIVER and digest(path)!=wanted:
    need(digest(ARCHIVED_DRIVER)==wanted,'Exact historical compiled source '+filename)
    pins[str(ARCHIVED_DRIVER)]=wanted
    historical_sources.append({'canonical':filename,'historicalSource':str(ARCHIVED_DRIVER),'SHA256':wanted})
   else:
    need(path.is_file() and digest(path)==wanted,'Changed input '+filename);pins[filename]=wanted
 current_guest,split_graphics,split_assets,current_split_payload=split.reconstruct()
 old_guest,old_assets=jax.expected_guest()
 info=json.loads((ROOT/CANDIDATE/'build-info.json').read_text(encoding='utf-8-sig'))
 current_payload=(ROOT/CANDIDATE/'roms/mk2ks/mk2ks.mdata').read_bytes()
 need(digest(ROOT/CANDIDATE/'mkport_candidate.exe')==info['executable_sha256'],'Current compiled executable')
 need(digest(ROOT/CANDIDATE/'roms/mk2ks/mk2ks.mdata')==info['payload_sha256'],'Current compiled payload')
 for filename,wanted in info['input_hashes'].items():need(digest(Path(filename))==wanted,'Build input '+filename);pins[filename]=wanted
 saved_jax=(jax.CANDIDATE,jax.CASES,jax.expected_guest)
 saved_baraka=(baraka.CANDIDATE,baraka.EXE,baraka.PAYLOAD,baraka.CASES,baraka.verify_payload)
 try:
  # The original tests still execute all physical/native/palette/pixel checks.
  # Only their expected candidate identity and independently reconstructed ROM
  # are supplied for the independently reconstructed current native data.
  jax.CANDIDATE=CANDIDATE;jax.CASES=cases('jax')
  jax.expected_guest=lambda:(current_guest,old_assets)
  baraka.CANDIDATE=CANDIDATE;baraka.EXE=info['executable_sha256'];baraka.PAYLOAD=info['payload_sha256']
  baraka.CASES=cases('baraka')
  def expected(payload=None):
   assert payload is None or payload==current_payload
   return current_guest,old_assets
  baraka.verify_payload=expected
  jax_report=jax.verify();need(jax_report['passed'],'Fresh Jax head-clap proof')
  errors.extend(jax_report['errors']);pins.update(jax_report['inputHashes'])
  for case,data in jax_report['cases'].items():summaries[case]={'killer':'jax',**data}
  baraka_report=baraka.verify();need(baraka_report['passed'],'Fresh Baraka head/body proof')
  errors.extend(baraka_report['errors']);pins.update(baraka_report['inputHashes'])
  for case,data in baraka_report['cases'].items():summaries[case]={'killer':'baraka',**data}
 finally:
  jax.CANDIDATE,jax.CASES,jax.expected_guest=saved_jax
  baraka.CANDIDATE,baraka.EXE,baraka.PAYLOAD,baraka.CASES,baraka.verify_payload=saved_baraka
 for killer,old_version,baseline_version,baseline_suffix,driver,observer,wrap_age,module in GROUPS:
  # Re-execute golden physical/art proofs. Canonical source changes are NOT
  # ignored: independently resolve every golden result hash below, including
  # its exact archived driver rather than requiring obsolete bytes live.
  golden=module.verify(check_files=False)
  need(golden['passed'],'Fresh frozen '+killer+' physical/art proof')
  errors.extend(golden['errors'])
  for name in ('kano','sonya'):
   for side in (1,2):
    baseline_name=f'audit_v{baseline_version}_{killer+"_" if killer!="reptile" else ""}{name}_p{side}_{baseline_suffix}'
    baseline=ROOT/baseline_name
    inputs(json.loads((baseline/'result.json').read_text(encoding='utf-8-sig')),True)
    current_name=f'audit_v1136_{killer}_{name}_p{side}_split_blood_regression';current=ROOT/current_name
    result=json.loads((current/'result.json').read_text(encoding='utf-8-sig'))
    need(result['candidate']==CANDIDATE and result['executable_sha256']==info['executable_sha256'] and result['payload_sha256']==info['payload_sha256'],'Exact current build '+current_name)
    need(result['exit_code']==0 and result['player']==name and result['victim_slot']==side and result['winner_slot']==3-side and result['seconds']==95 and result['assistance']=='none' and result['cheats_enabled'] is False,'Cold unassisted physical case '+current_name)
    inputs(result)
    text=(current/'run.log').read_text(encoding='utf-8-sig');old=(baseline/'run.log').read_text(encoding='utf-8-sig')
    need(not re.search(r'\[LUA ERROR\]|fatal error|access violation|exception at',text,re.I),'No runtime errors '+current_name)
    for prefix in (driver,observer):
     before,after=lines(old,prefix),lines(text,prefix)
     need(bool(before) and after==before,'All native physical/art observations unchanged '+current_name+' '+prefix)
    need((current/'guest_maincpu.bin').read_bytes()==current_guest,'Exact whole current ROM '+current_name)
    blobs={p.name:p for p in current.glob('*.bin') if p.name!='guest_maincpu.bin'}
    old_blobs={p.name:p for p in baseline.glob('*.bin') if p.name!='guest_maincpu.bin'}
    need(blobs.keys()==old_blobs.keys(),'Same actual native graphics/palette evidence '+current_name)
    for filename,path in blobs.items():
     need(filename in old_blobs and path.read_bytes()==old_blobs[filename].read_bytes(),'Actual native graphics/palette unchanged '+current_name+' '+filename)
     pins[str(path)]=digest(path)
    pictures={str(p.relative_to(current/'snap')):p for p in (current/'snap').rglob('*.png')}
    old_pictures={str(p.relative_to(baseline/'snap')):p for p in (baseline/'snap').rglob('*.png')}
    need(pictures.keys()==old_pictures.keys(),'All actual presented snapshot names '+current_name)
    identical=0
    for filename,path in pictures.items():
     equal=filename in old_pictures and Image.open(path).size==(400,254) and path.read_bytes()==old_pictures[filename].read_bytes()
     need(equal,'Actual presented PNG unchanged '+current_name+' '+filename);identical+=int(equal);pins[str(path)]=digest(path)
    for filename in ('run.log','result.json','guest_maincpu.bin'):pins[str(current/filename)]=digest(current/filename)
    summaries[current_name]={'killer':killer,'previousVerifiedCase':baseline_name,
       'nativeWrapAge':wrap_age,'actualPNGs':len(pictures),'actualIdenticalPNGs':identical,
       'actualGraphicsAndPaletteDumps':len(blobs),'allNativeObservationLinesIdentical':all(lines(text,p)==lines(old,p) for p in (driver,observer))}
 need(len(summaries)==20,'Five established native actions, both true victims and physical slots')
 return {'passed':not errors,'errors':sorted(set(errors)),'cases':summaries,'inputHashes':pins,
   'resolvedHistoricalCompiledSources':list({r['SHA256']:r for r in historical_sources}.values()),
   'scope':'20 current real-input normal Dead Pool cases: Jax clap, Baraka, Cage torso, Kitana inflation, Reptile head removal',
   'currentEstablishedVictimRegressionsAfterSplitBloodAccepted':not errors,'alternateCostumesAccepted':False,
   'allStockFatalitiesAccepted':False,'allArenasAccepted':False,'fullPortAccepted':False}

if __name__=='__main__':
 if OUT.exists():raise ValueError('Never replace verification evidence')
 report=verify();OUT.mkdir();(OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps({k:v for k,v in report.items() if k not in ('cases','inputHashes','resolvedHistoricalCompiledSources')},indent=2))
 raise SystemExit(0 if report['passed'] else 1)
