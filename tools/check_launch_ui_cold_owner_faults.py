"""Entire actual cold-owner gate and changed-record negative controls."""
import inspect,json,re,subprocess
from pathlib import Path
import capture_launch_candidate_ui as host
ROOT,need,sha=host.ROOT,host.need,host.sha
OUT=ROOT/'audit_launch_candidate_ui_cold_owner_faults'

def gate(text,terminal):
 source=inspect.getsource(host.capture);first=source.index('  owner_rows=');last=source.index('  need(all(sha(',first)
 body='\n'.join(line[2:]for line in source[first:last].splitlines())
 code="def check(text,terminal):\n state={'terminal':terminal}\n"+'\n'.join(' '+line for line in body.splitlines())+"\n return len(owner_rows)\n"
 scope=dict(vars(host));exec(compile(code,__file__+'::entire_executed_cold_owner_gate','exec'),scope)
 return scope['check'](text,terminal)

def verify(cases):
 need(not OUT.exists(),'Fresh same-run owner fault qualification')
 proof_path=ROOT/'audit_launch_candidate_ui_checked/report.json';proof=json.loads(proof_path.read_text())
 need(proof['passed']and proof['allColdBattleOwnershipClear'],'Whole actual current fixture passed')
 pins=dict(proof['inputHashes']);pins[str(proof_path)]=sha(proof_path);faults=[];total=0
 for case in proof['cases']:
  key=f"{case['fighter']}_p{case['side']}";folder,text,_=cases[key];terminal=case['state']['terminal'];positive=gate(text,terminal);total+=positive
  line=next(s for s in text.splitlines()if s.startswith('MK2_UA_OWNER '))
  changes=[(name,re.sub(r'\b'+name+r'=\S+',name+'='+value,line,count=1))for name,value in(('actor','01000000'),('main','01000000'),('id','17'),('health','161'))]
  changed_texts=[(name,text.replace(line,changed,1))for name,changed in changes]+[('owner field omitted',text.replace(line+'\n','',1)),('duplicate owner field',text.replace(line,line+'\n'+line,1))]
  for label,bad in changed_texts:
   need(bad!=text,'Actual nonvacuous cold-owner record fault')
   try:gate(bad,terminal)
   except ValueError as error:faults.append(dict(case=key,fault=label,rejectedBy=str(error)))
   else:raise ValueError('Actual cold-owner counterexample admitted '+label)
   need(gate(text,terminal)==positive,'Entire positive restored')
 pins[str(Path(__file__).resolve())]=sha(__file__)
 need(all(sha(p)==h for p,h in pins.items()),'All actual source/evidence intact')
 report=dict(passed=True,completeColdBattleOwnerFields=total,actualOwnerFaultsRejected=faults,inputHashes=pins,
             newNativeBoots=0,newBuilds=0,newROMCopies=0,newZIPs=0,newRawMedia=0,fullPortAcceptance=False,goalStatus='active')
 OUT.mkdir();p=OUT/'report.json';p.write_text(json.dumps(report,indent=2)+'\n');h=sha(p)
 need(subprocess.run(['compact.exe','/C','/EXE:LZX','/F','/I','/Q',str(p)],capture_output=True).returncode==0 and sha(p)==h,'Lossless cold-owner proof')
 print(json.dumps(dict(passed=True,completeOwnerFields=total,actualOwnerFaultsRejected=len(faults))),flush=True)
 return report
