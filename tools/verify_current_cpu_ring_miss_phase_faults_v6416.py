"""Actual current missed Ring lifecycle counterexamples, no replay/mutation.

Retain whole original match and compound contracts, and exercise the new
miss branch against copies of actual recorded fields, never guest state.
"""
import gzip,json,re,subprocess
from pathlib import Path
import current_cpu_ring_miss_phase_v6411 as phase
import capture_current_cpu_ring_miss_render_v6412 as capture

ROOT,need,sha=capture.ROOT,capture.need,capture.sha
OUT=ROOT/'audit_v6417_current_cpu_ring_miss_phase_checked'

def main():
 need(not OUT.exists() and not capture.original.previous.terminal.process_tools.census(),'Same naturally terminal capture; no replay')
 report=json.loads((capture.FOLDER/'result.json').read_text())
 terminal=json.loads((capture.FOLDER/'native_terminal.json').read_text())
 need(report['passed'] and terminal['exitCode']==0 and terminal['naturalTerminal'] and not terminal['observationErrors'] and
      report['wholeEarlierPhysicalTrajectoryIdentical'] and all(sha(p)==h for p,h in report['inputHashes'].items()),
      'Whole actual current executable/guest/physical/AI/health/source inputs unchanged')
 with gzip.open(capture.FOLDER/'run.log.gz','rt',encoding='utf-8')as file:text=file.read()
 guest=capture.original.previous.terminal.current.expected()
 positive=phase.full_phase(text,guest)
 need(positive==report['independentSemantics'],'Entire capture-admitted physical semantics restored independently')
 faults=[]
 def change(tag,key,value,where):
  line=next(s for s in text.splitlines()if s.startswith(tag+' ')and where in s)
  bad,n=re.subn(r'\b'+key+r'=\S+',key+'='+value,line,count=1)
  need(n==1 and bad!=line,'Nonvacuous actual native miss state fault');return text.replace(line,bad,1)
 trials=[
  ('native CPU proxy','MK2_CPU_OVERLAP_EVENT','id','1','kind=ring '),
  ('wrong parent owner','MK2_CPU_OVERLAP_EVENT','main_owner','00000000','kind=ring '),
  ('wrong child parent','MK2_CPU_OVERLAP_CHILD','shot_owner','00000000','entry=FFFC7000'),
  ('wrong child birth','MK2_CPU_OVERLAP_CHILD','frame','1893','entry=FFFC7000'),
  ('wrong flight group','MK2_CPU_OVERLAP_EVENT','a0','00000000','kind=group '),
  ('wrong group velocity','MK2_CPU_OVERLAP_EVENT','vx','00080000','kind=group '),
  ('wrong child position','MK2_CPU_OVERLAP_CHILD_FIELD','xraw','00000000','frame=1895'),
  ('invented impact action','MK2_CPU_OVERLAP_CHILD_FIELD','action','0500','frame=1895'),
  ('wrong child lifetime serial','MK2_CPU_OVERLAP_CHILD_FIELD','child_serial','2','frame=1895'),
  ('wrong retirement motion','MK2_CPU_OVERLAP_RETIRE','xraw','00000000','frame=1908'),
  ('wrong retirement routine','MK2_CPU_OVERLAP_RETIRE','pc','FF8B6831','frame=1908'),
  ('wrong parent held pose','MK2_CPU_PAIR_FIELD','pose','00000000','frame=1880'),
  ('retained parent lock','MK2_CPU_PAIR_FIELD','flags','00000010','frame=1930'),
 ]
 for label,tag,key,value,where in trials:
  bad=change(tag,key,value,where)
  try:phase.full_phase(bad,guest)
  except(ValueError,AssertionError,KeyError)as error:faults.append(dict(fault=label,rejectedBy=str(error)))
  else:raise ValueError('Actual native miss fault accepted '+label)
 line=next(s for s in text.splitlines()if s.startswith('MK2_CPU_OVERLAP_CHILD_FIELD '))
 for label,bad in [('omitted actual child callback',text.replace(line+'\n','',1)),
                   ('duplicated actual child callback',text.replace(line,line+'\n'+line,1))]:
  try:phase.full_phase(bad,guest)
  except(ValueError,AssertionError,KeyError)as error:faults.append(dict(fault=label,rejectedBy=str(error)))
  else:raise ValueError('Actual native miss callback fault accepted '+label)
 need(phase.full_phase(text,guest)==positive and len(faults)==15,'Entire original full positive restores after15 actual record faults')
 pins=dict(report['inputHashes'])
 for p in(capture.FOLDER/'result.json',capture.FOLDER/'native_terminal.json',capture.FOLDER/'run.log.gz',Path(__file__),Path(phase.__file__)):
  pins[str(p.resolve())]=sha(p)
 result=dict(passed=True,nativeTerminal=terminal,wholeNativePhysicalPhase=positive,actualMissPhaseFaultsRejected=faults,
             inputHashes=pins,goalStatus='active',newNativeBoots=0,newBuilds=0,newRawMedia=0,fullPortAcceptance=False)
 OUT.mkdir();path=OUT/'report.json';path.write_text(json.dumps(result,indent=2)+'\n');h=sha(path)
 need(subprocess.run(['compact.exe','/C','/EXE:LZX','/F','/I','/Q',str(path)],capture_output=True).returncode==0 and sha(path)==h,'Exact finite lifecycle proof losslessly compressed')
 print(json.dumps(dict(passed=True,actualMissPhaseFaults=len(faults),phase=positive['ring'])),flush=True)

if __name__=='__main__':main()
