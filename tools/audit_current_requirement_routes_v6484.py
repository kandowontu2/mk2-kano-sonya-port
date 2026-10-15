"""Resolve actual evidence schema routes and qualify four current continuations.

Never rewrite historical pins or count an evolving cleanup note as intact.
The manifest route proves artifact identity, not universal runtime coverage.
"""
import datetime,gzip,json,subprocess
from pathlib import Path
import audit_current_natural_integration_v6476 as inventory
import capture_current_continue_bound_v6482 as continuation
from inventory_current_port_storage_v4200 import allocated
ROOT,need,sha=inventory.ROOT,inventory.need,inventory.sha
OUT=ROOT/'audit_v6485_current_requirement_routes'

def main():
 need(not OUT.exists() and not continuation.prior.census(),'Fresh terminal-only audit; no native job remains live')
 priorpath=ROOT/'audit_v6477_current_natural_integration_requirements/report.json'
 prior=json.loads(priorpath.read_text());need(prior['passed'] and not prior['fullGoalComplete'],'Original whole-scope audit retained')
 pins={str(priorpath):sha(priorpath),str(Path(__file__)):sha(__file__)}
 anomalies=[];routes=[]
 manifest=ROOT/inventory.BUILD/'build-info.json';meta=json.loads(manifest.read_text(encoding='utf-8-sig'))
 need(sha(manifest)=='72F19E2E6CA566B6D4EF99C092831E8D988F97A037A32E8372B576519A18E526' and
      meta['executable_sha256']==inventory.EXE and meta['payload_sha256']==inventory.PAYLOAD,
      'Immutable current compiled executable/payload manifest')
 exe=ROOT/inventory.BUILD/'mkport_candidate.exe';payload=ROOT/inventory.BUILD/'roms/mk2ks/mk2ks.mdata'
 need(sha(exe)==inventory.EXE and sha(payload)==inventory.PAYLOAD,'Actual current playable bytes')
 for evidence in prior['evidence']:
  path=Path(evidence['path']);need(sha(path)==evidence['sha256'],'Original inspected receipt unchanged')
  report=json.loads(path.read_text(encoding='utf-8-sig'));direct={}
  for key in ('inputHashes','newInputHashes','sourceInputs'):
   direct.update(report.get(key,{}))
  for name,wanted in direct.items():
   actual=sha(name) if Path(name).is_file() else None
   if actual!=wanted:
    anomalies.append(dict(version=evidence['version'],path=name,expected=wanted,actual=actual,
                          classification='changed documentation, not an intact historical pin' if Path(name).resolve()==(ROOT/'WORKSPACE_CLEANUP_CURRENT.md').resolve() else 'unresolved input integrity failure'))
  direct_current=direct.get(str(exe))==inventory.EXE and direct.get(str(payload))==inventory.PAYLOAD
  manifest_current=direct.get(str(exe))==inventory.EXE and direct.get(str(manifest))==sha(manifest)
  routes.append(dict(version=evidence['version'],directPinMaps=list(k for k in ('inputHashes','newInputHashes','sourceInputs') if k in report),
                     directCurrentExecutablePayload=direct_current,currentArtifactManifestRoute=manifest_current,
                     flagPresent='passed' in report,reportedPassed=report.get('passed'),
                     runtimeScopeNotExpanded=True))
  pins[str(path)]=sha(path)
 need(len(anomalies)==2 and {a['version'] for a in anomalies}=={5884,5890} and
      all(a['classification'].startswith('changed documentation') for a in anomalies),
      'No missing or altered tested code/assets; preserve both cleanup-note mismatches explicitly')
 ending=next(r for r in routes if r['version']==5732)
 need(ending['directCurrentExecutablePayload'] and 'sourceInputs' in ending['directPinMaps'],
      'Actual full ending report uses sourceInputs, not a missing current identity')
 journalpath=inventory.locate(5322);journal=json.loads(journalpath.read_text());cases=journal['currentActualCases']
 need('passed' not in journal and len(cases)==18 and journal['actualPhysicalSpecialCycles']==36,
      'Additive journal is not a failed native test; independently inspect its complete children')
 move_children=[]
 for case in cases:
  path=Path(case['report']);report=json.loads(path.read_text())
  need(journal['newInputHashes'].get(str(path))==sha(path) and report['passed'] and
       report['candidate']==inventory.BUILD and report['executableSHA256']==inventory.EXE,
       'Each actual current independently qualified body/shadow child pinned by journal')
  pins[str(path)]=sha(path);move_children.append(dict(move=case['move'],slot=case['physicalSlot'],air=case['air'],report=str(path)))
 capture,gate=continuation.bindings();current_cases=[];files=[]
 for fighter in ('kano','sonya'):
  for side in (1,2):
   folder=ROOT/f'audit_v6483_current_continue_{fighter}_p{side}_ram'
   path=folder/'report.json';report=json.loads(path.read_text())
   need(report['passed'] and report['nativeExit']==0 and not report['observationErrors'] and
        report['candidate']==inventory.BUILD and report['executableSHA256']==inventory.EXE and
        report['payloadSHA256']==inventory.PAYLOAD and len(report['actualFaultsRejected'])==4,
        'Four complete current real cross-continue cases, not a first-slot substitute')
   need(all(sha(p)==h for p,h in report['inputHashes'].items()),'All actually executed inputs unchanged')
   with gzip.open(folder/'run.log.gz','rt',encoding='utf-8') as f:text=f.read()
   actual=gate(text,fighter,side);need(actual==report['actualCurrentContinuation'],'Whole current continuation gate reproduced')
   need(report['actualGuestGFXProofs']['guest']['sha256']=='5255F3D3870BF9E10999DF79BFD1E15AC892533F38BA1922E981060D2E84ED30' and
        report['actualGuestGFXProofs']['gfx']['bytes']==18976,'Full actual current guest and imported GFX in every cold boot')
   need(not any(p.suffix.lower() in ('.png','.wav','.bin','.pcm','.rgb','.exe','.mdata','.zip') for p in folder.rglob('*') if p.is_file()),
        'No raw media or redundant game/build copies')
   current_cases.append(actual)
   files.extend(p for p in folder.rglob('*') if p.is_file());pins[str(path)]=sha(path)
 failure=ROOT/'audit_v6480_current_continue_kano_p1_ram/report.json';failed=json.loads(failure.read_text())
 need(not failed['passed'] and failed['nativeExit']==0 and not failed['observationErrors'],
      'Preserve actual snapshot-binding runtime rejection, never relabel failed test passed')
 with gzip.open(failure.parent/'run.log.gz','rt',encoding='utf-8') as f:failed_rows=f.read().splitlines()
 with gzip.open(ROOT/'audit_v6483_current_continue_kano_p1_ram/run.log.gz','rt',encoding='utf-8') as f:corrected_rows=f.read().splitlines()
 unchanged_tags=('MK2_GROUND_INPUT ','MK2_GROUND_FIELD ','MK2_GROUND_HEALTH ','MK2_GROUND_MODE ','MK2_CR_FIELD ')
 need(all([l for l in failed_rows if l.startswith(tag)]==[l for l in corrected_rows if l.startswith(tag)] for tag in unchanged_tags),
      'Snapshot-hook correction leaves the whole physical/native/independent post-field chronology unchanged')
 files.extend(p for p in failure.parent.rglob('*') if p.is_file());pins[str(failure)]=sha(failure)
 paths=(ROOT/'mk2ks_current_continue_ram_v6478.lua',ROOT/'mk2ks_current_continue_bound_v6481.lua',
        ROOT/'tools/capture_current_continue_v6479.py',Path(continuation.__file__),Path(__file__))
 files.extend(paths);files=list(dict.fromkeys(p.resolve() for p in files))
 for p in (*paths,exe,payload,manifest,ROOT/'WORKSPACE_CLEANUP_CURRENT.md'):pins[str(p)]=sha(p)
 before=sum(allocated(p) for p in files)
 for path in files:
  digest=sha(path);need(subprocess.run(['compact.exe','/C','/EXE:LZX','/F','/I','/Q',str(path)],capture_output=True).returncode==0 and
                       inventory.hashlib.sha256(path.read_bytes()).hexdigest().upper()==digest,'Exact finite source/evidence compression')
 after=sum(allocated(p) for p in files)
 report=dict(passed=True,observedUTC=datetime.datetime.now(datetime.timezone.utc).isoformat(),candidate=inventory.BUILD,
             originalObjective=prior['objective'],originalRequirements=prior['requirements'],evidenceSchemaRoutes=routes,
             preservedHistoricalPinDrift=anomalies,unresolvedCodeAssetInputFailures=0,
             currentHumanMoveJournalChildren=move_children,currentPaidCrossContinuations=current_cases,
             newActualCurrentContinuationCases=4,collisionEarnedLosses=8,currentContinuedActorFields=sum(c['continuedActorFields'] for c in current_cases),
             actualRecordFaultsRejected=16,previousCaptureFailurePreserved=str(failure),
             originalFailedCapturePhysicalStateHealthAndModeRowsUnchanged=True,
             sourcePreflightRepairs=['missing Python prior binding repaired before native start; no game bytes changed'],
             exactTextFilesCompressed=len(files),logicalBytes=sum(p.stat().st_size for p in files),allocatedBytesBefore=before,allocatedBytes=after,
             remainingConcreteWork=['Current CPU/post-ending challenger join and single-player continue routes need current-build qualification, not old-build acceptance transfer',
                                    'Complete native Pit/Tomb stock-victim choreography and source sound-priority branch coverage',
                                    'Resolve cannonball donor launch-cue fidelity: current source has no startup cue; absence is not donor parity',
                                    'Complete remaining secret/morph/cinematic and integrated visual/audio regression, then finished matching release'],
             alreadyQualifiedNotUntouched=['Both-slot selection/ladder/real identities/name and floor shadows in recorded contexts',
                                           'Eight human and CPU move branches in their separately qualified finite contexts',
                                           'Four complete native campaigns, own ending pipelines and attract returns'],
             rawMediaFilesWritten=0,newBuilds=0,newROMCopies=0,newZIPs=0,currentPlayableChanged=False,fullPortAcceptance=False,fullGoalComplete=False,
             goalStatus='active',inputHashes=pins,previousGoalTurnClassification='no progress: acknowledgement only',
             thisGoalTurnClassification='progress: completed pending requirement audit, resolved schema-only apparent failures and preserved two documentation pin drifts; four cold current CMD paid cross-continuations qualified')
 OUT.mkdir();path=OUT/'report.json';path.write_text(json.dumps(report,indent=2)+'\n')
 digest=inventory.hashlib.sha256(path.read_bytes()).hexdigest().upper()
 need(subprocess.run(['compact.exe','/C','/EXE:LZX','/F','/I','/Q',str(path)],capture_output=True).returncode==0 and
      inventory.hashlib.sha256(path.read_bytes()).hexdigest().upper()==digest,'Complete route audit compressed without content loss')
 print(json.dumps({k:report[k] for k in ('passed','newActualCurrentContinuationCases','collisionEarnedLosses','currentContinuedActorFields','actualRecordFaultsRejected','unresolvedCodeAssetInputFailures','allocatedBytes','fullGoalComplete')}),flush=True)

if __name__=='__main__':main()
