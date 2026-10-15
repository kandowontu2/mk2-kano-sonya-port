"""Actual current palette ownership defect and bounded native teardown proof.
Guest palette instructions remain original, but the compiled CPU pre-fetch
hook rewrites a genuine donor bubble palette as if it were frame metadata.
The auxiliary object's ID zero selects stock palette row zero, which receives
the explicit bubble color upload and retains a reference into the next screen.
Do not call palette ownership/cleanup, full finishers or the port accepted.
"""
import json,re
from pathlib import Path
import inspect_current_friendship_palette_lifecycle_v2732 as diagnostic
life=diagnostic.life
ROOT=life.ROOT
need=life.need
OUT=ROOT/'audit_v2738_current_friendship_palette_router_checked'
def path_rows(path):
 rows=[]
 with path.open(encoding='utf-8-sig') as stream:
  for line in stream:
   m=re.match(r'MK2_PAL_PATH_(\w+) (.*)',line)
   if m:rows.append((m[1],dict(re.findall(r'(\w+)=([^\s]+)',m[2]))))
 return rows
def trace_check(rows,guest):
 begin=life.select(rows,'BEGIN');done=life.select(rows,'CONSTRUCT_RETURN')
 need(len(begin)==len(done)==1,'One actual native bubble palette-path invocation')
 step={life.pointer(r,'entry'):r for r in life.select(rows,'STEP') if life.pointer(r,'entry')!=0xff80cfd0}
 first,after=step[0xff80d3a0],step[0xff80d3c0]
 stock=int.from_bytes(guest[(0xfffec000-0xff800000)//8:(0xfffec000-0xff800000)//8+4],'little')
 need(life.pointer(first,'a0')==life.pointer(begin[0],'a0')==0xfecdf710 and life.pointer(after,'a0')==stock==0xffadbbd0,'Actual genuine palette redirected to stock auxiliary-ID-zero row at compiled hook')
 need(life.pointer(after,'a3')==life.pointer(first,'a3')+0x23 and all(first[key]==after[key] for key in ('frame','a1','a2','a4','a8','a13','sp','stack')),'Only original ADDI A3 plus compiled A0 rewrite between exact native instruction boundaries')
 a=(0xff80d3a0-0xff800000)//8
 need(guest[a:a+4]==bytes.fromhex('03 0b 23 00'),'Original instruction only adds 23h to A3, cannot change A0')
 need(life.pointer(step[0xff80d490],'a0')==stock and life.pointer(step[0xff80d570],'a0')==0x0404 and life.pointer(done[0],'a0')==0x01069c80,'Actual rewritten pointer stored and palette index returned to independent auxiliary task')
 return dict(beforeSource=0xfecdf710,afterSource=stock,originalInstruction='ADDI 23h,A3',compiledHookPC=0xff80d3c0,allocatedPaletteIndex=4,auxiliaryTask=0x01069c80)
def verify():
 pins=life.native.scene.launch.source_pins()
 def pin(path,wanted=None):
  path=str(path);actual=life.native.scene.launch.sha(path);need(wanted is None or actual==wanted,'Immutable actual palette-router dependency '+path);need(path not in pins or pins[path]==actual,'Consistent actual dependency '+path);pins[path]=actual
 frozen=ROOT/life.native.scene.current.NAME/'input_sources/mame-mkp/src/devices/cpu/tms34010/tms34010.cpp'
 pin(frozen,'87B5F2953B374D890CC97F041AA450D8E89DAC735C8299BF40F3E491E7E94AEF')
 cpu=frozen.read_text();condition='mk2ks_imported_descriptor && !mk2ks_native_morph_palette &&'
 need(cpu.count(condition)==2 and cpu.count('m_pc == 0xff80d3c0')==2 and cpu.count('m_regs[0].reg = int32_t(TMS34010_RDMEM_DWORD(table + TMS34010_RDMEM_WORD(mk2ks_object + 0x1f0) * 32));')==2,'Both real compiled execution/debug CPU paths contain same blanket donor-root palette rewrite')
 cpp=ROOT/life.native.scene.current.NAME/'input_sources/mame-mkp/src/mame/midway/midtunit_m.cpp';pin(cpp,'17B055BA1D8AC4F9EEAB157A408327F9B0D120B6C731598D4E6195E50C8E684F')
 need('leg_movi(0,0xfecdf720); leg_movi(2,16); leg_call(0xff80c6b0);' in cpp.read_text(),'Actual compiled port explicitly replaces sixteen pens in assigned child bank')
 guest,_,payload=life.native.scene.current.expected();offset=(0xfecdf710-0xfe800000)//8
 need(int.from_bytes(payload[offset:offset+2],'little')==16,'Actual entry root is a genuine 16-color palette header, not frame metadata')
 cases={};outcomes=[]
 for side in (1,2):
  folder=ROOT/f'audit_v2731_current_kano_friendship_palette_lifecycle_p{side}';path=ROOT/f'audit_v2733_current_kano_friendship_palette_lifecycle_p{side}_diagnostic/report.json';report=json.loads(path.read_text())
  need(report['passed'] and report['diagnosticCompleted'] and report['uninterruptedCompletePaletteTableReplayAccepted'] and report['actualNativeTaskReturnAndSpriteReclaimAccepted'] and report['actualReplayedTableStores']==328 and report['actualNativeReferenceIncrements']==227 and report['actualNativeReferenceReleases']==51 and not report['allocatorPaletteSourceIdentityAccepted'] and not report['actualNativeBubblePaletteReferenceReclaimed'] and report['actualPaletteIndex']==4 and report['actualAllocatorEntrySource']==0xfecdf710 and report['actualPaletteTableSource']==report['finalPaletteSource']==0xffadbbd0 and report['finalPaletteReferenceCount']==1 and not report['gameChanged'] and not report['fullPortAcceptance'],'Both actual palette diagnostics prove complete table replay and retain actual source/refcount failure')
  pin(path)
  for file,wanted in report['inputHashes'].items():pin(file,wanted)
  rows=diagnostic.parse(folder/'run.log');life_rows=life.parse(folder/'run.log');control=report['control'];allocated=life.check(life_rows,control,'kano',side)
  original=diagnostic.palette_check(rows,control,allocated,side);cleanup=diagnostic.lifecycle_check(life_rows,rows,control,allocated)
  need(original['actualCompletePaletteSnapshots']==report['actualCompletePaletteSnapshots'] and cleanup['actualNativeTaskReturnAndSpriteReclaimAccepted'],'Every actual palette/task/sprite control fully repeated')
  first_store=next(i for i,(tag,r) in enumerate(rows) if tag=='TABLE_STORE')
  first_state=next(i for i,(tag,r) in enumerate(rows) if tag=='STATE')
  ctor=next(i for i,(tag,r) in enumerate(rows) if tag=='CONSTRUCT')
  increment=next(i for i,(tag,r) in enumerate(rows) if tag=='TABLE_STORE' and life.pointer(r,'pc')==0xff80d550)
  changed_table=rows[first_state][1]['table'].split(',');fields=changed_table[4].split(':');fields[1]=f'{int(fields[1],16)^1:04X}';changed_table[4]=':'.join(fields)
  mutations=[('wrong_actual_store_before',first_store,'before',f'{life.pointer(rows[first_store][1],"before")^1:04X}','Each original palette store matches previous'),('missing_actual_table_store',first_store,'drop',None,'Each original palette store matches previous'),('wrong_actual_snapshot_reference',first_state,'table',','.join(changed_table),'Every actual complete palette snapshot'),('wrong_actual_constructor_index',ctor,'paletteIndex','0','Actual constructed palette bound'),('wrong_native_increment_source',increment,'pc','FF80CD90','Original native palette reset clears')]
  for name,idx,key,value,expected in mutations:
   changed=list(rows)
   if key=='drop':changed.pop(idx)
   else:r=dict(changed[idx][1]);r[key]=value;changed[idx]=(changed[idx][0],r)
   need(changed!=rows,'Non-vacuous actual palette counterexample')
   try:diagnostic.palette_check(changed,control,allocated,side)
   except ValueError as error:
    need(expected in str(error),'Specific actual palette invariant '+name+': '+str(error));outcomes.append(dict(side=side,name=name,rejectedBy=str(error)))
   else:raise ValueError('Corrupt actual palette ownership observations accepted '+name)
  for name,kind,key,value,expected in [('missing_actual_task_return','RETURN_TASK','drop',None,'Actual independently allocated task returned'),('wrong_native_task_return','RETURN_TASK','entry','FF80E250','Actual independently allocated task returned')]:
   changed=[]
   for tag,r in life_rows:
    if tag==kind:
     if key=='drop':continue
     r=dict(r);r[key]=value
    changed.append((tag,r))
   try:diagnostic.lifecycle_check(changed,rows,control,life.check(changed,control,'kano',side))
   except ValueError as error:
    need(expected in str(error),'Specific actual native task invariant '+name);outcomes.append(dict(side=side,name=name,rejectedBy=str(error)))
   else:raise ValueError('Corrupt actual native task return accepted '+name)
  need(diagnostic.palette_check(rows,control,life.check(life_rows,control,'kano',side),side)==original,'Final unmodified complete original palette control')
  cases[str(side)]=dict(actualPaletteReport=str(path),actualCompletePaletteSnapshots=report['actualCompletePaletteSnapshots'],actualNativeTaskReturnFrame=cleanup['actualTaskReturnFrame'],actualSpriteResetFrame=cleanup['actualSpritePoolResetFrame'],actualSpriteFreeMembershipFrame=cleanup['actualSpriteFreeMembershipFrame'],actualSpriteReuseFrame=cleanup['actualSpriteAllocatorReuseFrame'],actualNativeTaskReturnAndSpriteReclaimAccepted=True,paletteOwnershipAndReferenceCleanupAccepted=False,allocatorEntrySource=0xfecdf710,allocatedTableSource=0xffadbbd0,heldReferenceIntoNextScreen=1)
 trace=ROOT/'audit_v2736_current_kano_friendship_palette_path_p1';meta=json.loads((trace/'result.json').read_text(encoding='utf-8-sig'));before=json.loads((trace/'inputs_before.json').read_text(encoding='utf-8-sig'))
 need(meta['exit_code']==0 and meta['winner']=='kano' and meta['side']==1 and meta['assistance']=='none' and meta['guest_writes']==0 and not meta['cheats_enabled'] and before==meta['input_hashes'],'Actual terminal unchanged-build physical native instruction trace')
 for file,wanted in before.items():
  pin(file,wanted)
  if Path(file).suffix in ('.lua','.ps1','.json'):pin(trace/'input_sources'/Path(file).name,wanted)
 observer=(ROOT/'mk2ks_current_friendship_palette_path_v2734.lua').read_text();need(observer.count("dofile('mk2ks_current_friendship_extended_wins_v2688.lua')")==1 and not re.search(r':write_|set_value|clear_value|load_?state|\.value\s*=(?!=)',observer),'Instruction/stack observer read-only over existing genuine physical driver')
 old=(ROOT/'tools/run_current_friendship_palette_lifecycle_v2730.ps1').read_text();expected=old.replace('"$root/mk2ks_current_friendship_palette_lifecycle_v2729.lua"','"$root/mk2ks_current_friendship_palette_path_v2734.lua","$root/mk2ks_current_friendship_palette_lifecycle_v2729.lua"',1).replace('-autoboot_script "$root/mk2ks_current_friendship_palette_lifecycle_v2729.lua"','-autoboot_script "$root/mk2ks_current_friendship_palette_path_v2734.lua"')
 need(expected==(ROOT/'tools/run_current_friendship_palette_path_v2735.ps1').read_text(),'Exact physical launcher except smaller read-only instruction trace')
 records=path_rows(trace/'run.log');actual_path=trace_check(records,guest)
 filtered=lambda rs:[(tag,r) for tag,r in rs if not tag.startswith('SHADOW_')]
 baseline=ROOT/'audit_v2691_current_kano_friendship_shadow_p1/run.log';pin(baseline)
 need(filtered(life.native.scene.previous.parse(trace/'run.log'))==filtered(life.native.scene.previous.parse(baseline)),'Every original physical input/health/pose/WIN/cue/transition record unchanged in instruction trace')
 for name,entry,key,value,expected in [('no_host_palette_rewrite',0xff80d3c0,'a0','FECDF710','Actual genuine palette redirected'),('wrong_native_addi_result',0xff80d3c0,'a3','00000000','Only original ADDI'),('wrong_allocated_native_palette',0xff80d570,'a0','00000505','Actual rewritten pointer stored')]:
  changed=[]
  for tag,r in records:
   if tag=='STEP' and life.pointer(r,'entry')==entry:r=dict(r);r[key]=value
   changed.append((tag,r))
  need(changed!=records,'Non-vacuous real instruction trace corruption')
  try:trace_check(changed,guest)
  except ValueError as error:
   need(expected in str(error),'Specific real host-router invariant '+name);outcomes.append(dict(name=name,rejectedBy=str(error)))
  else:raise ValueError('Corrupt real instruction trace accepted '+name)
 for file in trace.rglob('*'):
  if file.is_file():pin(file)
 pin(Path(__file__).resolve());life.native.scene.launch.module_pins(pins)
 return dict(passed=True,cases=cases,actualCompiledPaletteRouterCause=actual_path,actualNativeTaskAndSpriteReclamationBothSlotsAccepted=True,actualPaletteReplaySnapshots=sum(c['actualCompletePaletteSnapshots'] for c in cases.values()),actualPaletteStoresReplayed=656,rejectedActualPaletteTaskAndRouterCounterexamples=len(outcomes),outcomes=outcomes,legitimatePaletteMisclassifiedByCompiledHostHookConfirmed=True,currentBubblePaletteOwnershipAndTeardownAccepted=False,nativePaletteOwnershipFixRequired=True,guestROMEqualityDoesNotProveUnmodifiedNativeExecution=True,executedSourcesCapturesAndReportsUnchanged=True,gameChanged=False,fullFinisherAcceptance=False,fullPortAcceptance=False,inputHashes=pins,scope=__doc__)
if __name__=='__main__':
 need(not OUT.exists(),'Immutable actual palette-router cause and teardown boundary')
 r=verify();OUT.mkdir();(OUT/'report.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps({k:v for k,v in r.items() if k not in ('inputHashes','outcomes')},indent=2),flush=True)
