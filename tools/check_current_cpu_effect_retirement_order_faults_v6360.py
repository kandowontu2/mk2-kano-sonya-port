"""Real intra-field retirement-order counterexamples, no native replay."""
import gzip,json,subprocess,traceback
from pathlib import Path
import verify_current_cpu_effect_render_v6356 as original
ROOT,need=original.ROOT,original.need
sha=original.bridge.sha
OUT=ROOT/'audit_v6361_current_cpu_effect_retirement_order_faults'


def main():
 need(not OUT.exists(),'Immutable original-order counterexample proof')
 parent_path=ROOT/'audit_v6359_current_cpu_effect_render_checked/report.json'
 parent=json.loads(parent_path.read_text());need(parent['passed']and all(sha(p)==h for p,h in parent['inputHashes'].items()),'Complete current renderer/art/erase proof unchanged')
 case=ROOT/'audit_v6349_current_cpu_effect_render_ram'
 with gzip.open(case/'run.log.gz','rt',encoding='utf-8')as file:text=file.read()
 sources=set(parent['originalBladeDonorArt']['sources']);positive=original.order_contract(text,sources)
 lines=text.splitlines();retire=next(i for i,s in enumerate(lines)if s.startswith('MK2_BLADE_ALLOC_RETIRE ')and'frame=1909 'in s)
 last=positive['lastPublication']['lineIndex'];publication=lines[last]
 need(last<retire and 'frame=1909 'in publication,'Actual final blade publication precedes cleanup inside same field')
 moved=list(lines);moved.pop(last);moved.insert(retire,publication)
 duplicated=list(lines);duplicated.insert(retire+1,publication)
 wrong=list(lines);wrong[retire]=wrong[retire].replace('frame=1909 ','frame=1908 ',1)
 faults=[]
 for label,bad in [('final publication after retirement','\n'.join(moved)+'\n'),
                   ('duplicated stale final publication','\n'.join(duplicated)+'\n'),
                   ('false retirement field','\n'.join(wrong)+'\n')]:
  need(bad!=text,'Real observed-order counterexample, not noop')
  try:original.order_contract(bad,sources)
  except(ValueError,AssertionError,KeyError)as error:faults.append(dict(fault=label,rejectedBy=str(error)))
  else:raise ValueError('Accepted actual retirement-order fault '+label)
 need(original.order_contract(text,sources)==positive,'Original positive restored')
 pins=dict(parent['inputHashes'])
 for p in(parent_path,Path(__file__),Path(original.__file__)):pins[str(p.resolve())]=sha(p)
 result=dict(passed=True,parentFullSceneQualification=str(parent_path),positive=positive,
             actualOrderFaultsRejected=faults,inputHashes=pins,newNativeBoots=0,newBuilds=0,newRawMedia=0,
             noRelaxedSameFieldPublicationRule=True,fullPortAcceptance=False,goalStatus='active')
 OUT.mkdir();p=OUT/'report.json';p.write_text(json.dumps(result,indent=2)+'\n');h=sha(p)
 need(subprocess.run(['compact.exe','/C','/EXE:LZX','/F','/I','/Q',str(p)],capture_output=True).returncode==0 and sha(p)==h,'Exact report losslessly compressed')
 print(json.dumps(dict(passed=True,actualOrderFaultsRejected=len(faults),newNativeBoots=0)),flush=True)


if __name__=='__main__':
 try:main()
 except Exception as error:
  OUT.mkdir(exist_ok=True);(OUT/'failure.json').write_text(json.dumps(dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False),indent=2)+'\n');raise
