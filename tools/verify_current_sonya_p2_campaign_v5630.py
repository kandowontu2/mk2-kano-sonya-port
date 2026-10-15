"""Whole current Sonya P2 campaign plus complete supplemental physical replays.

Retain all5213 selection/schedule/morph/health/continue/boss/ending semantics,
all18actual native/RAM faults, mirror/range/Kitana/Jax/SubZero input replays.
Only slot provenance changes; Jax instruction/Carry callback gate also required.
"""
import inspect,json,re,traceback
from pathlib import Path
from types import SimpleNamespace
import current_payload_metadata_context_v5229 as current
import run_current_sonya_p2_campaign_v5628 as capture
import verify_extended_sonya_p1_whole_campaign_v5213 as original
import verify_current_kano_p2_campaign_v5623 as kano
ROOT,need,sha=current.ROOT,current.need,current.sha
OUT=ROOT/'audit_v5631_current_sonya_p2_campaign_checked'

def matched(folder,pins):
 source=inspect.getsource(kano.matched)
 changes=[("meta['fighter']=='kano'","meta['fighter']=='sonya'"),
  ("meta['identity']==17","meta['identity']==18"),
  ('boundary=capture.boundary.source_boundary()','boundary=capture.source_boundary()'),
  ("boundary['physicalInputsExactlyUnchanged']","boundary['originalPhysicalPolicyUnchanged']"),
  ("MK2KS_TEST_FIGHTER='kano'","MK2KS_TEST_FIGHTER='sonya'"),
  ("MK2KS_CAMPAIGN_STRATEGY='zoning',MK2KS_BOSS_PHYSICAL_POLICY='shao_knife_retreat'",
   "MK2KS_CAMPAIGN_STRATEGY='guard_punish',MK2KS_BOSS_PHYSICAL_POLICY='shao_ring_retreat'"),
  ("command[command.index('-str')+1]=='6000'","command[command.index('-str')+1]=='18100'")]
 for before,after in changes:
  need(source.count(before)==1,'Whole current provenance adaptation '+before)
  source=source.replace(before,after,1)
 scope=dict(vars(kano),__file__=__file__,current=current,capture=capture)
 exec(compile(source,__file__+'::entire_current_provenance','exec'),scope)
 scope['matched'](folder,pins)
 text=original.read_log(folder)
 rows=re.findall(r'^MK2_CAMPAIGN_P2_SOURCE path=(\S+) bytes=(\d+) slot=2 writes=0 assistance=none$',text,re.M)
 wanted=set(capture.original.CONTROLLERS)-{'mk2ks_mileena_campaign_trace_v3848.lua'}
 need(len(rows)==len(wanted)and {r[0]for r in rows}==wanted and all(int(r[1])>0 for r in rows),
  'All seven actually loaded native P2 transitive source declarations, no omitted overlay')

def p2_factory(function,module):
 source=inspect.getsource(function)
 for before,after in [("\"f['human_slot'] == '1'\"","\"f['human_slot'] == '2'\""),
                      ("\"r['slot'] == '1'\"","\"r['slot'] == '2'\"")]:
  need(source.count(before)==1,'Whole original physical replay slot boundary '+before)
  source=source.replace(before,after,1)
 source=source.replace('Actual true Sonya P1 identity','Actual true Sonya P2 identity')
 scope=dict(vars(module),__file__=__file__)
 exec(compile(source,__file__+'::whole_P2_'+module.__name__,'exec'),scope)
 return scope[function.__name__]

def jax_callbacks(text,guest):
 module=original.supplemental.jax
 source=inspect.getsource(module.callbacks)
 need(source.count("r['human_slot']=='1'")==1,'Whole native Jax callback slot guard')
 source=source.replace("r['human_slot']=='1'","r['human_slot']=='2'",1).replace('P1 Sonya/Jax','P2 Sonya/Jax')
 scope=dict(vars(module),__file__=__file__)
 exec(compile(source,__file__+'::whole_Jax_callbacks_P2','exec'),scope)
 gate=scope['callbacks'];positive=gate(text,guest)
 line=next(s for s in text.splitlines()if s.startswith('MK2_JAX_GROUND_NATIVE ')and ' kind=ground_result 'in s)
 row=dict(re.findall(r'(\w+)=([^\s]+)',line));faults=[]
 for key,value in [('pc','FFF00000'),('a8','01000000'),('opcode','0000'),('carry',str(1-int(row['carry']))),('human_slot','1')]:
  damaged=re.sub(r'\b'+key+r'=[^\s]+',key+'='+value,line,count=1)
  need(damaged!=line,'Actual nonvacuous native Jax callback fault')
  try:gate(text.replace(line,damaged,1),guest)
  except ValueError as error:faults.append(dict(key=key,rejectedBy=str(error)))
  else:raise ValueError('Actual native Jax callback fault admitted '+key)
 need(gate(text,guest)==positive,'Full native callback positive restored')
 return dict(positive=positive,actualNativeCallbackFaultsRejected=faults)

def whole_run():
 slot=SimpleNamespace(guard_replay=original.slot.sonya.physical.replay,
  range_replay=original.slot.sonya.spacing.replay)
 kitana=original.supplemental.kitana;jax=original.supplemental.jax;subzero=original.subzero
 supplemental=SimpleNamespace(
  kitana=SimpleNamespace(make_replay=p2_factory(kitana.make_replay,kitana)),
  jax=SimpleNamespace(make_replay=p2_factory(jax.make_replay,jax)))
 subzero_carrier=SimpleNamespace(make_replay=p2_factory(subzero.make_replay,subzero))
 scope=dict(vars(original),__file__=__file__,current=current,capture=capture,OUT=OUT,matched=matched,
  slot=slot,supplemental=supplemental,subzero=subzero_carrier,jax_callbacks=jax_callbacks)
 for function in [original.campaign_meta,original.ram_guest,original.ram_guest_checked,original.make_native,original.run]:
  source=inspect.getsource(function);changes=[]
  if function is original.campaign_meta:changes=[('human_slot=1,cpu_slot=2','human_slot=2,cpu_slot=1')]
  if function is original.run:
   changes=[("parse(text,1,'sonya')","parse(text,2,'sonya')"),
    ("'roster','18,1'","'roster','1,18'"),
    ('actualNaturalCurrentSonyaP1BossesOwnEndingAttractAccepted','actualNaturalCurrentSonyaP2BossesOwnEndingAttractAccepted'),
    ("guest=current.expected();proof=json.loads((capture.OUT/'guest_memory_proof.json').read_text())",
     "guest=current.expected();callbacks=jax_callbacks(text,guest);proof=json.loads((capture.OUT/'guest_memory_proof.json').read_text())"),
    ('actualFullMirrorGuardInputReplay=guard,','actualFullNativeJaxCallbacks=callbacks,actualFullMirrorGuardInputReplay=guard,')]
  for before,after in changes:
   need(source.count(before)==1,'Whole semantic/physical replay adaptation '+before)
   source=source.replace(before,after,1)
  exec(compile(source,__file__+'::entire_'+function.__name__,'exec'),scope)
 report=scope['run']()
 need(report['actualNaturalCurrentSonyaP2BossesOwnEndingAttractAccepted']and
  report['case']['unassisted_clear_proven']and len(report['actualNativeAndRAMProofFaultsRejected'])==18,
  'Full actual current P2 own bosses/ending/attract plus all18real faults; no deadline credited as clear')
 return report

if __name__=='__main__':
 need((capture.OUT/'result.json').is_file(),'Await actual terminal; never restart live capture')
 need(not OUT.exists(),'Fresh immutable full native campaign verdict')
 try:report=whole_run()
 except Exception as error:report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
 OUT.mkdir();(OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps({k:v for k,v in report.items()if k not in('inputHashes','case')},indent=2),flush=True)
 if report['passed']:
  print(json.dumps({k:v for k,v in report['case'].items()if k not in('inputHashes','uppercutAssignmentFrames')},indent=2),flush=True)
 raise SystemExit(0 if report['passed']else 1)
