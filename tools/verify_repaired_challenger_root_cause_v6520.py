"""Actual four-slot challenger gate and exact failed Sonya KO/purge regression.

No native replay, previous failure relabeling, input retiming or public promotion.
Full native memory was compared by each capture; inspect its immutable proofs,
whole physical/health/actor chronology and passive native task-list evidence.
"""
import gzip,hashlib,json,re,struct,subprocess
from pathlib import Path
import native_projectile_identifiers_context_v6509 as candidate
import qualify_current_challenger_boundary_v6489 as original
ROOT,need,sha,rows=candidate.ROOT,candidate.need,candidate.sha,original.rows
OUT=ROOT/'audit_v6521_repaired_challenger_root_cause_checked'

def text(folder):
 with gzip.open(folder/'run.log.gz','rt',encoding='utf-8')as f:return f.read()

def selected(t,tag,last=None):
 return [l for l in t.splitlines() if l.startswith(tag+' ') and
         (last is None or int(dict(re.findall(r'(\w+)=([^\s]+)',l))['frame'])<=last)]

def regression(old,new):
 for tag in ('MK2_JR_INPUT','MK2_JR_HEALTH','MK2_CR_FIELD'):
  need(selected(old,tag,2155)==selected(new,tag,2155) and selected(new,tag,2155),
       'Every actual pre-purge physical/health/actor row unchanged '+tag)
 ko=[q for q in rows(new,'MK2_JR_HEALTH') if q['frame']=='2130' and q['slot']=='2']
 need(len(ko)==1 and ko[0]['before']=='21' and ko[0]['after']=='0' and ko[0]['pc']=='FF836700',
      'Same genuine CPU ring collision-earned KO, not a shortened or assisted route')
 before=[q for q in rows(new,'MK2_JC_TASK') if q['frame']=='2156' and q['entry']=='FF83F520']
 ring=next(q for q in before if q['task']=='01070490')
 need(ring['words'].split(',')[1]=='00030700' and any(q['task']=='0106DAF0' for q in before),
      'Actual ring now belongs to ordinary P1 projectile task family before original native purge')
 prior=[q for q in rows(old,'MK2_JC_TASK') if q['frame']=='2156' and q['entry']=='FF83F520']
 old_ring=next(q for q in prior if q['task']=='01070490')
 need(old_ring['words'].split(',')[1]=='0003B700','Preserved original protected bogus task identifier')
 need({q['task'] for q in prior}=={q['task'] for q in before},'Identical complete native pre-purge task membership')
 for a,b in zip(prior,before):
  need(a['task']==b['task'],'Exact native task order')
  aw=a['words'].split(',');bw=b['words'].split(',')
  if a['task']=='01070490':aw[1]=bw[1]
  need(aw==bw,'No unrelated pre-purge task-word delta')
 after=[q for q in rows(new,'MK2_JC_TASK') if q['frame']=='2159' and q['entry']=='FF83A4C0']
 need(after and not any(q['task'] in ('01070490','0106DAF0') for q in after),
      'Actual post-purge active task list contains neither ring nor linked polling task')
 bad={'FFA1D860','FFA1E7B0','FFA1E800'}
 need(any(q['at']=='FFA1D860' and q['frame']=='2158' for q in rows(old,'MK2_JC_ENTRY')),
      'Actual preserved original native missing-task assertion')
 need(not any(q['at'] in bad for tag in ('MK2_JA_ENTRY','MK2_JC_ENTRY') for q in rows(new,tag)),
      'No native assertion/error-loop entry in the complete repaired route')
 original.gate(new,'sonya',2)
 return dict(samePrePurgeInputsHealthActors=True,collisionKOFrame=2130,purgeFrame=2156,
             beforeRingTask='01070490',oldTaskID='B700',repairedTaskID='0700',
             postPurgeBothTasksAbsentAt=2159,nativeAssertionObservedBefore=True,nativeAssertionObservedAfter=False)

def main():
 need(not OUT.exists(),'Fresh immutable actual regression qualifier')
 guest=candidate.expected();gfx=candidate.expected_gfx();base=candidate.old.expected()
 need(sum(a!=b for a,b in zip(base,guest))==158,'Independently predicted exact initialized delta')
 for table,count,origin in ((0xfd700,16,0xff8b5fc0),(0xfd750,12,0xff8b66a0)):
  need(guest[table:table+count*4]==base[candidate.repair.offset(origin):candidate.repair.offset(origin)+count*4],
       'Every stock packed identifier row preserved')
 pins={str(Path(__file__).resolve()):sha(__file__)};cases=[];faults=[]
 for fighter in ('kano','sonya'):
  for side in (1,2):
   folder=ROOT/f'audit_v6519_repaired_challenger_identity_{fighter}_p{side}_ram'
   r=json.loads((folder/'report.json').read_text());t=text(folder)
   need(r['passed'] and r['candidate']==candidate.NAME and r['nativeExit']==0 and not r['observationErrors'] and
        not (folder/'stderr.log').read_text().strip(),'Actual successful isolated candidate terminal')
   need(all(sha(p)==h for p,h in r['inputHashes'].items()),'Every actually executed input unchanged')
   identity=r['nativeIdentity'];process=json.loads((folder/'process.json').read_text())
   need(identity['ParentProcessId']==process['cmdPID'] and identity['createdUnix']>=process['startedUnix'] and
        Path(identity['ExecutablePath']).resolve()==(ROOT/candidate.NAME/'mkport_candidate.exe').resolve() and
        str(folder) in identity['CommandLine'] and '-nocheat' in identity['CommandLine'] and '-samples' in identity['CommandLine'],
        'Actual native child, exact executable/creation/arguments')
   for kind,expected in (('guest',guest),('gfx',gfx)):
    need(r['actualGuestGFXProofs'][kind]==dict(bytes=len(expected),sha256=hashlib.sha256(expected).hexdigest().upper()),
         'Complete independently compared initialized memory proof '+kind)
   good=original.gate(t,fighter,side);need(good==r['actualCurrentChallenger'],'Original entire gameplay gate agrees')
   for label,tag,key,value in [('wrong real ID','MK2_CR_FIELD','id','1'),('wrong Main owner','MK2_CR_FIELD','owner','00000000'),
                            ('false CPU role','MK2_JR_JOIN','otherState','1'),('false highlight','MK2_JR_HIGHLIGHT','roster','1'),
                            ('false ready','MK2_JR_RESULT','ready','-1'),('false terminal','MK2_JR_RESULT','terminal','1')]:
    line=next(l for l in t.splitlines() if l.startswith(tag+' ') and
              (tag!='MK2_CR_FIELD' or f'slot={side} ' in l and int(dict(re.findall(r'(\w+)=([^\s]+)',l))['frame'])>=good['events']['match']))
    bad=re.sub(r'\b'+key+r'=\S+',key+'='+value,line,count=1);need(line!=bad,'Effective actual-record fault')
    try:original.gate(t.replace(line,bad,1),fighter,side)
    except (ValueError,KeyError)as e:faults.append(dict(fighter=fighter,side=side,kind=label,rejectedBy=str(e)))
    else:raise ValueError('False actual gameplay evidence admitted '+label)
   for n in (1,2):
    line=next(l for l in t.splitlines() if l.startswith('MK2_CR_FIELD ') and f'slot={n} ' in l and
              f"frame={good['events']['terminal']-1} " in l)
    try:original.gate(t.replace(line+'\n','',1),fighter,side)
    except (ValueError,KeyError)as e:faults.append(dict(fighter=fighter,side=side,kind='missing final actual slot '+str(n),rejectedBy=str(e)))
    else:raise ValueError('Missing final actual native callback admitted')
   need(original.gate(t,fighter,side)==good,'Original positive restored after faults')
   cases.append(good);pins.update(r['inputHashes'])
   for p in folder.rglob('*'):
    if p.is_file():pins[str(p.resolve())]=sha(p)
 oldfolder=ROOT/'audit_v6501_current_challenger_cleanup_sonya_p2_ram'
 firstfolder=ROOT/'audit_v6511_repaired_challenger_sonya_p2_ram'
 newfolder=ROOT/'audit_v6519_repaired_challenger_identity_sonya_p2_ram'
 oldreport=json.loads((oldfolder/'report.json').read_text());first=json.loads((firstfolder/'report.json').read_text())
 newreport=json.loads((newfolder/'report.json').read_text());old=text(oldfolder);new=text(newfolder)
 need(not oldreport['passed'] and oldreport['nativeExit']==0 and not oldreport['observationErrors'],
      'Original runtime failure remains a failure, clean host observation')
 proof=regression(old,new)
 need(first['passed'] is False and first['nativeIdentity'] is None and first['nativeExit']==0 and
      first['observationErrors']==["ValueError('Exact live current executable child, full command and creation time')"],
      'Preserve first changed-build host identity failure; no invented cause or retrospective acceptance')
 firsttext=text(firstfolder)
 for tag in ('MK2_JR_INPUT','MK2_JR_HEALTH','MK2_CR_FIELD','MK2_JC_TASK','MK2_JC_ENTRY','MK2_JA_ENTRY'):
  need(selected(firsttext,tag)==selected(new,tag),'Whole first/second repaired gameplay chronology identical '+tag)
 need(first['actualRGBDigests']==newreport['actualRGBDigests'],'All27 repaired RGB digests identical across host-failed/passing run')
 need(oldreport['actualRGBDigests']==newreport['actualRGBDigests'][:2],
      'Original cold selection and first-match full-frame pixels unchanged, not full UI acceptance')
 rootfaults=[]
 for label,a,b in [('protected task survives','00030700','0003B700'),('wrong damage PC','pc=FF836700','pc=00000000'),
                   ('changed input','button=Block','button=Start')]:
  need(a in new,'Effective root-cause fault '+label)
  bad=new.replace(a,b,1)
  try:regression(old,bad)
  except (ValueError,KeyError,StopIteration)as e:rootfaults.append(dict(kind=label,rejectedBy=str(e)))
  else:raise ValueError('False root-cause evidence admitted '+label)
 need(regression(old,new)==proof,'Actual root-cause positive restored')
 for f in (oldfolder,firstfolder):
  report=json.loads((f/'report.json').read_text());need(all(sha(p)==h for p,h in report['inputHashes'].items()),'Every preserved failed input intact')
  pins.update(report['inputHashes'])
  for p in f.rglob('*'):
   if p.is_file():pins[str(p.resolve())]=sha(p)
 for p in (Path(candidate.__file__),Path(original.__file__),Path(original.executed.__file__)):
  pins[str(p.resolve())]=sha(p)
 report=dict(passed=True,candidate=candidate.NAME,executableSHA256=candidate.EXE_SHA,guestSHA256=candidate.GUEST_SHA,
             actualInitializedByteDelta=158,actualFourChallengerCases=cases,joinedActorFields=sum(c['joinedActorFields'] for c in cases),
             actualGameplayFaultsRejected=faults,actualRootCauseFaultsRejected=rootfaults,exactFailedRouteRepair=proof,
             preservedRuntimeFailure=str(oldfolder/'report.json'),preservedHostFailure=str(firstfolder/'report.json'),
             firstRepairedGameplayAndPixelsIdentical=True,originalColdSelectionFirstMatchPixelsIdentical=True,
             inputHashes=pins,newNativeBoots=0,newRawMedia=0,publicPlayableChanged=False,fullPortAcceptance=False,goalStatus='active')
 OUT.mkdir();p=OUT/'report.json';p.write_text(json.dumps(report,indent=2)+'\n');h=sha(p)
 need(subprocess.run(['compact.exe','/C','/EXE:LZX','/F','/I','/Q',str(p)],capture_output=True).returncode==0 and sha(p)==h,
      'Hash-preserving exact proof compression')
 print(json.dumps(dict(passed=True,cases=4,joinedActorFields=report['joinedActorFields'],gameplayFaults=len(faults),rootCauseFaults=len(rootfaults))),flush=True)

if __name__=='__main__':main()
