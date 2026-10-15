"""Genuine Mileena regressions for the untouched original palette override."""
import json
import re
from pathlib import Path
import verify_native_arm_palette_v1074 as owned

ROOT=owned.ROOT;OUT=ROOT/'audit_v1079_arm_palette_stock_checked'
CASES=tuple(f'audit_v1078_jax_mileena_p{s}_stock_palette' for s in (1,2))

def verify():
 errors=[];pins={};summaries={};guest,_,_=owned.reconstruct()
 info=json.loads((ROOT/owned.CANDIDATE/'build-info.json').read_text(encoding='utf-8-sig'))
 def need(ok,label):
  if not ok:errors.append(label)
 # The only physical-driver change admits genuine native Mileena selection.
 old=(ROOT/'mk2ks_stock_fatality_v1021.lua').read_text()
 new=(ROOT/'mk2ks_stock_fatality_v1077.lua').read_text()
 need(new.replace('kitana=4,mileena=5','kitana=4')==old,'Original physical input algorithm unchanged')
 for filename in ('mk2ks_stock_fatality_v1077.lua','mk2ks_stock_fatality_display_v1077.lua','mk2ks_arm_palette_stock_trace_v1078.lua'):
  text=(ROOT/filename).read_text()
  need(not re.search(r'\bp:write_|\.value\s*=(?!=)|load_state|loadstate',text),'Read-only genuine stock observer '+filename)
 for case in CASES:
  folder=ROOT/case;result=json.loads((folder/'result.json').read_text(encoding='utf-8-sig'))
  side=result['victim_slot'];text=(folder/'run.log').read_text(encoding='utf-8-sig')
  need(result['exit_code']==0 and result['candidate']==owned.CANDIDATE and result['executable_sha256']==info['executable_sha256'] and result['payload_sha256']==info['payload_sha256'],'Exact stock build '+case)
  need(result['assistance']=='none' and not result['cheats_enabled'] and result['player']=='mileena' and result['killer']=='jax' and result['command']=='bbbb_lp' and result['target_gap']==96 and result['seconds']==95,'Genuine unassisted stock case '+case)
  for filename,wanted in result['input_hashes'].items():need(owned.digest(Path(filename))==wanted,'Changed stock input '+filename);pins[filename]=wanted
  need(not re.search(r'\[LUA ERROR\]|fatal error|access violation',text,re.I),'No stock runtime error '+case)
  rows=owned.prior.rows(text,'MK2_STOCK_HEAD_V921');items=lambda tag:[r for t,r in rows if t==tag]
  actions,wraps,stops=items('ACTION'),items('WRAP'),items('RESULT')
  need(len(actions)==len(wraps)==len(stops)==1,'One original stock action/completion '+case)
  if len(actions)!=1:continue
  action=actions[0];start=int(action['frame'])
  live=items('FIRST_LIVE');need(len(live)==1 and live[0]['ids']=='11,5' and live[0]['victim']==action['victim_actor'],'Genuine stock fighter selection '+case)
  health=161;killed=0;chain=True;damage=0
  for row in items('HEALTH'):
   if row['pc']!='FF836700' or int(row['frame'])>start:continue
   before,after=int(row['before']),int(row['after']);chain=chain and before==health and 0<=after<before<=161
   health=after;damage+=before-after
   if after==0:killed+=1;health=161
  need(chain and killed==2 and damage==322 and len(items('WIN'))==2,'Original collision health chain '+case)
  approach=items('APPROACH');pressed={(int(r['frame']),r['button']) for r in items('INPUT') if r['slot']==str(3-side)}
  need(len(approach)==1,'Actual stock spacing '+case)
  if approach:
   begin=int(approach[0]['frame']);need(92<=int(approach[0]['gap'])<=100 and start==begin+44 and all((begin+a,'Block') in pressed for a in (10,18,26,34)) and (begin+42,'Low_Punch') in pressed,'Physical BBBB LP '+case)
  compares=[r for r in items('COMPARE') if int(r['frame'])==start and 0xff879bd0<=int(r['table'],16)<=0xff879c10]
  need([r['actual'] for r in compares]==['1','2','2','2','2'] and all(r['actual']==r['wanted'] for r in compares),'Original stock button parser '+case)
  need(action['variant']=='2' and action['address']=='FF8BE240' and wraps[0]['age']=='147' and int(wraps[0]['frame'])==start+147 and stops[0]['frame']=='5198' and stops[0]['damage']=='322' and stops[0]['wins']=='2' and not items('CACHE_OVERWRITE') and any(r['mode']=='3' and int(r['frame'])>start+147 for r in items('MODE')),'Original stock completion/continue '+case)
  traces=owned.prior.rows(text,'MK2_ARM_PALETTE_V1073')
  entries=[r for t,r in traces if t=='ENTRY'];fallback=[r for t,r in traces if t=='STOCK_FALLBACK']
  props={r['prop'] for r in entries};applied=[r for t,r in traces if t=='ORIGINAL_APPLY' and r['prop'] in props]
  need(len(entries)==len(fallback)==len(applied)==2 and not any(t=='OWNED_APPLY' for t,_ in traces),'Only original stock path for both props '+case)
  for row in fallback:
   before=next((r for r in entries if r['prop']==row['prop']),None)
   need(before is not None and row['preserved']=='1' and all(row[k]==before[k] for k in ('sp','st','a1','a2','a7','prop','main','victim','id','flags')),'Stock registers/status/stack preserved '+case)
   need(row['id']=='5' and row['victim']==action['victim_actor'] and row['main']==action['main'] and row['prop_id']=='0' and row['a7']=='FF90DD00','Actual original Mileena override '+case)
  for row in applied:
   before=next(r for r in entries if r['prop']==row['prop'])
   need(row['palette']=='FF90DD00' and row['a7']=='FF90DD00' and row['pc']=='FF8410A0' and int(row['sp'],16)==int(before['sp'],16)-32,'Original native palette applier call '+case)
  need((folder/'guest_maincpu.bin').read_bytes()==guest,'Independent whole guest '+case)
  for filename in ('run.log','result.json','guest_maincpu.bin'):pins[str(folder/filename)]=owned.digest(folder/filename)
  summaries[case]={'stockVictimID':5,'nativeWrapAge':147,'nativeProps':2,'originalMileenaPalette':'FF90DD00','genuineCollisionDamage':damage,'registersStatusStackPreserved':True}
 return {'passed':not errors,'errors':sorted(set(errors)),'cases':summaries,'inputHashes':pins,
  'scope':'two genuine normal Dead Pool Mileena Jax arm-rip stock-palette regressions',
  'mileenaOriginalOverrideAccepted':not errors,'naturalAlternateSelectionAccepted':False,'allStockFatalitiesAccepted':False,'fullPortAccepted':False}

if __name__=='__main__':
 if OUT.exists():raise ValueError('Preserve verification evidence')
 report=verify();OUT.mkdir();(OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps({k:v for k,v in report.items() if k not in ('cases','inputHashes')},indent=2))
 raise SystemExit(0 if report['passed'] else 1)
