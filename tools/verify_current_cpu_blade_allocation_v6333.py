"""Full original pool/attach/phase/retire/reuse proof for current CPU blade.

Adapt old fourteen-fixture gate only to the one naturally chosen current CPU
blade and existing full physical blade/knife contract. No address, descriptor,
pool-link, instruction, cadence, owner or post-retirement concession.
This is effect object lifetime, not full effect pixels/audio/port acceptance.
"""
import ast,datetime,gzip,inspect,json,subprocess,traceback
from pathlib import Path
import current_payload_metadata_context_v5229 as current
import verify_blade_allocation_v2911 as old
import capture_current_cpu_blade_knife_shadow_v6313 as phase_source
import verify_current_kano_cpu_blade_knife_v6304 as phase
import verify_current_existing_cpu_leg_choices_v6274 as faults
ROOT,need,sha=current.ROOT,current.need,current.sha
CASE=ROOT/'audit_v6332_current_cpu_blade_allocation_ram'
OUT=ROOT/'audit_v6334_current_cpu_blade_allocation_checked'
PARENT=ROOT/'audit_v6328_current_cpu_blade_knife_body_shadow_checked/report.json'


def phase_gate():
 # Reuse exact executed6313 full6310 motion/HP/state/native choice gate.
 source=inspect.getsource(phase_source.capture)
 start=source.index(' import ast\n');stop=source.index(' namespace.update(',start)
 namespace=dict(phase_source.__dict__,__file__=__file__)
 exec(compile('def prepare():\n'+source[start:stop]+' return scope[\'gate\']\n',__file__+'::whole_qualified_phase_gate','exec'),namespace)
 return namespace['prepare']()


def allocation_gate():
 source=inspect.getsource(old.verify_log)
 start=source.index("    if kind == 'interrupt':");stop=source.index('    for tag in ',start)
 source=source[:start]+"    original = full_phase(log, guest)\n    native_fields = phase.model.knife.rows(log, 'FIELD')\n"+source[stop:]
 before="(2 if kind == 'interrupt' else 8)"
 need(source.count(before)==1,'Only actual one-creation scenario cardinality changes')
 source=source.replace(before,'1',1)
 scope=dict(old.verify_log.__globals__,phase=phase,full_phase=phase_gate())
 exec(compile(source,__file__+'::entire_original_allocation_lifetime_gate_current_CPU_context','exec'),scope)
 return lambda text,guest:scope['verify_log'](text,guest,'cpu',2,'kano')


def main():
 need(not OUT.exists(),'Fresh immutable qualification, no overwrite')
 report=json.loads((CASE/'result.json').read_text());terminal=json.loads((CASE/'native_terminal.json').read_text())
 need(report['passed'] and report['nativeExit']==terminal['exitCode']==0 and terminal['naturalTerminal'],
      'Same actual process naturally terminal before host qualification')
 need(not phase_source.terminal.process_tools.census(),'No live native job, no second replay')
 pins=dict(report['inputHashes']);need(all(sha(p)==h for p,h in pins.items()),'Actual executed inputs unchanged')
 baseline=ROOT/'audit_v2912_blade_allocation_checked/report.json';prior=json.loads(baseline.read_text())
 need(prior['passed'] and sha(old.__file__)==prior['inputHashes'][str(Path(old.__file__).resolve())],
      'Whole independently qualified original allocation/retirement model unchanged')
 with gzip.open(CASE/'run.log.gz','rt',encoding='utf-8')as file:text=file.read()
 guest=current.expected();gate=allocation_gate();positive=gate(text,guest)
 need(positive['contexts'][0]['start']==1871 and positive['contexts'][0]['nativeRetirement']==1909,
      'Actual expected naturally chosen blade, not a substitute action')
 mutate=lambda tag,key,value,where={}:faults.mutate_field(text,'MK2_BLADE_ALLOC_'+tag,key,value,
              lambda row:all(row.get(k)==str(v)for k,v in where.items()))
 contexts=old.rows(text,'CONTEXT_RESULT');ctx=contexts[0]
 pop=next(r for r in old.rows(text,'HEAD_STORE')if r['context']==1 and r['frame']==1871 and r['pc']==0xff809150 and r['at']==0x01060130)
 push=next(r for r in old.rows(text,'HEAD_STORE')if r['context']==1 and r['frame']==1909 and r['pc']==0xff8097d0 and r['at']==0x01060130)
 trials=[
  ('constructor_owner',mutate('CREATE','owner','01000000')),
  ('constructor_free_head',mutate('CREATE','freeHead','01000000')),
  ('pool_pop_register',mutate('HEAD_STORE','a2','01000000',{'sequence':pop['sequence']})),
  ('pool_pop_high_word',mutate('HEAD_STORE','data','0000',{'sequence':pop['sequence']+1})),
  ('pool_push_next',mutate('HEAD_STORE','targetNext','01000000',{'sequence':push['sequence']})),
  ('pool_push_high_word',mutate('HEAD_STORE','merged','01000000',{'sequence':push['sequence']+1})),
  ('attachment_wrong_object',mutate('TRAIL_STORE','a10','01000000',{'frame':1871})),
  ('attachment_wrong_opcode',mutate('TRAIL_STORE','op0','FFFF',{'frame':1871})),
  ('retirement_wrong_object',mutate('RETIRE','a0','01000000')),
  ('cleanup_wrong_owner',mutate('CLEANUP','a8','01000000')),
  ('effect_pose',mutate('FIELD','descriptor','FFF8F800',{'frame':1874})),
  ('effect_missing_active_list',mutate('FIELD','active','0',{'frame':1884})),
  ('effect_already_free',mutate('FIELD','free','1',{'frame':1884})),
  ('effect_wrong_parent_pose',mutate('FIELD','pose','00000000',{'frame':1886})),
  ('effect_bad_free_chain',mutate('FIELD','freeValid','0',{'frame':1890})),
  ('stale_trail_after_retirement',mutate('FIELD','trail',f"{ctx['object']:08X}",{'frame':1910})),
  ('unexplained_address_reuse',mutate('FIELD','active','1',{'frame':1911})),
  ('missing_retirement_field',text.replace(next(line+'\n'for line in text.splitlines()if line.startswith('MK2_BLADE_ALLOC_FIELD ')and'frame=1909 'in line),'',1)),
  ('missing_pool_store',text.replace(next(line+'\n'for line in text.splitlines()if line.startswith('MK2_BLADE_ALLOC_HEAD_STORE ')and f"sequence={push['sequence']+1} "in line),'',1)),
 ]
 rejected=[]
 for label,bad in trials:
  need(bad!=text,'Real observed record changed '+label)
  try:gate(bad,guest)
  except(AssertionError,ValueError,KeyError,IndexError)as error:rejected.append(dict(fault=label,rejectedBy=str(error)))
  else:raise ValueError('Actual allocation/retirement fault accepted: '+label)
 need(gate(text,guest)==positive,'Untouched positive restored after real-record fault matrix')
 parent=json.loads(PARENT.read_text());need(parent['passed'] and parent['goalStatus']=='active','Full goal and previous body/shadow qualification retained')
 for path in(PARENT,baseline,Path(__file__),Path(old.__file__),Path(phase_source.__file__),Path(phase.__file__),
             Path(faults.__file__),*(p for p in CASE.rglob('*')if p.is_file())):pins[str(path.resolve())]=sha(path)
 need(all(sha(p)==h for p,h in pins.items()),'Complete actual inputs/evidence/source unchanged')
 result=dict(passed=True,observedUTC=datetime.datetime.now(datetime.timezone.utc).isoformat(),candidate=current.NAME,
             goalStatus='active',parentAdditiveJournal=str(PARENT),remaining=parent['remaining'],case=positive,
             actualFaultsRejected=rejected,inputHashes=pins,scope=__doc__,newNativeBoots=1,newBuilds=0,newZIPs=0,newRawMedia=0,
             originalWholePhysicalTrajectoryUnchanged=report['originalWholePhysicalTrajectoryUnchanged'],
             fullEffectRasterAudioAcceptance=False,fullPortAcceptance=False,fullGoalComplete=False,
             previousGoalTurnClassification='progress: current body/shadows and stale latest launcher repaired',
             thisGoalTurnClassification='progress: current naturally chosen blade actual native pool/attachment/retirement lifetime, with actual-record faults',
             nextAction='Blade/knife effect raster/palettes/whole-screen erasure and audio; no replay solely for this accepted object lifetime')
 OUT.mkdir();path=OUT/'report.json';path.write_text(json.dumps(result,indent=2)+'\n');digest=sha(path)
 need(subprocess.run(['compact.exe','/C','/EXE:LZX','/F','/I','/Q',str(path)],capture_output=True).returncode==0 and sha(path)==digest,
      'Only lossless exactfile terminal report compression')
 print(json.dumps(dict(passed=True,contexts=positive['contexts'],headStores=positive['completeHeadStoreRows'],actualFaultsRejected=len(rejected),newBuilds=0)),flush=True)


if __name__=='__main__':
 try:main()
 except Exception as error:
  OUT.mkdir(exist_ok=True);(OUT/'failure.json').write_text(json.dumps(dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False),indent=2)+'\n');raise
