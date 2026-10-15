"""Current requirement/evidence audit, never a full-port acceptance substitute.

Inspect actual preserved report bodies and every direct input pin. A passing
historical result cannot transfer to a different current executable. Finite
coverage and explicit unaccepted branches remain distinct from completion.
"""
import datetime,hashlib,json,re,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parent.parent
OUT=ROOT/'audit_v6477_current_natural_integration_requirements'
BUILD='diagnostic_v5219_current_payload_rom_metadata'
EXE='A6BC32F526C78A5BD72ED1960EAE56AB40701D7FE881D70A93E031AEB87AB944'
PAYLOAD='A9A9DB228D4CF5FEA7E2A659AEF4D4407193FEE3D2F86E217F7F725D0D8E58D3'
SPECS={
 'selection':('Dedicated top-row portraits; zero highlight displacement; native blinking border/player number and animation; symmetric navigation without skipping Reptile',
              (5445,6266,6273)),
 'transition':('No persistent selector portrait/pose/hints through ladder or fights; dedicated ladder icons; actual match admission without softlocks',
               (5445,5698,5402)),
 'identity':('Official true Kano17/Sonya18 actors and underlying native state/AI/roster ownership, never a name-only Liu proxy, in both player slots',
             (6273,6266,5698,6473)),
 'names':('Correct MK2-style selection/ladder/lifebar/winner names, including the same native black name shadow',
          (5445,6273,5466)),
 'human_moves':('All eight complete native-feeling specials with normal activation, repeated use, hit/block/miss/rejection, separate cleanup and subsequent ordinary control',
                (5322,6266,6066,6074)),
 'cpu_moves':('Natural native CPU repertoire, move bodies/effects/state/health/ground/shadow/audio/recovery, including genuine contact and compound continuations',
              (5340,5371,6283,6359,6373,6382,6387,6392,6407,6417,6429,6436,6447,6455,6462,6473)),
 'ordinary_combat':('Native walking/jumping/ducking/guard/get-up/attacks, contact/chip/throws/airborne paired victims, mirrors and alternate palettes',
                    (6022,6036,6066,6074,6080,5402)),
 'ground_shadows':('Correct sole grounding and native floor shadows under both added fighters across complete ordinary/special/airborne/victim and arena phases',
                   (5445,5322,6022,6036,6066,6473,6455,6436,5938)),
 'audio':('Source-native impact/victim voices, launch sounds, announcers, priority/RNG, exact finite sample lifetime and no stale playback',
          (5466,5601,5747,5884,5974,6220,6228,6236,6259,6447,6462)),
 'finishers_victims':('Own finishers/Friendship/Babality and native stock finisher/paired/morph/palette/victim cleanup and cinematic teardown for both added actors',
                     (5459,5466,5507,5520,5531,5406,5415,5420,5426,6122,6133,6140,6152,6196,6211,6220,6228,6236,6252,6259)),
 'stage_finishers':('Native Pit/Tomb performer and victim/mirror/held/pressed/random-drop branches, original choreography, ground/shadow/audio and retirement',
                    (5884,5890,5915,5938,5974)),
 'campaign_cinematics':('Natural full ladders and both bosses; own complete endings and attract; normal join/reselect/continue and secret/cinematic routes',
                       (5698,5732,5747,5445,6273)),
 'cmd_release':('Runnable CMD opens the matching playable game; verified standalone ZIP at current state; final combined selection/ladder/names/gameplay/audio regression and finished release',
                (6241,6266,5990)),
 'storage':('Dependency-aware obsolete build/data cleanup; preserve user source and required reconstruction inputs; no redundant builds/ROM/raw media',
            (6475,6464,6457,6449)),
}
_hashes={}


def need(value,message):
 if not value:raise ValueError(message)


def sha(path):
 p=Path(path).resolve();key=str(p)
 if key not in _hashes:
  h=hashlib.sha256()
  with p.open('rb')as f:
   for chunk in iter(lambda:f.read(1024*1024),b''):h.update(chunk)
  _hashes[key]=h.hexdigest().upper()
 return _hashes[key]


def locate(version):
 folders=[p for p in ROOT.iterdir()if p.is_dir()and re.match(r'^audit_v'+str(version)+r'_',p.name)]
 need(len(folders)==1,'Unambiguous actual requirement evidence folder '+str(version))
 paths=[folders[0]/n for n in('report.json','progress.json')if(folders[0]/n).is_file()]
 need(len(paths)==1,'Unambiguous actual completed receipt '+str(version))
 return paths[0]


def facts(value):
 # Retain all top-level scalar acceptance/limit fields and compact scope facts.
 # Do not turn fullPortAcceptance=False into a missing narrow runtime result.
 return {k:v for k,v in value.items()if isinstance(v,(str,bool,int,float))or
         k in('next','nextAction','nextActions','remaining','scope','finiteVisualReview')}


def inspect_receipt(version):
 p=locate(version);value=json.loads(p.read_text(encoding='utf-8-sig'))
 pins={}
 for key in('inputHashes','newInputHashes'):
  for path,wanted in value.get(key,{}).items():
   resolved=str(Path(path).resolve())
   need(resolved not in pins or pins[resolved]==wanted,'Consistent explicit receipt pin maps '+str(version))
   pins[resolved]=wanted
 failures=[]
 for path,wanted in pins.items():
  if not Path(path).is_file():failures.append(dict(path=path,error='missing direct pinned input'))
  elif sha(path)!=wanted:failures.append(dict(path=path,error='changed direct pinned input',expected=wanted,actual=sha(path)))
 exe=ROOT/BUILD/'mkport_candidate.exe';data=ROOT/BUILD/'roms/mk2ks/mk2ks.mdata'
 current_bound=(pins.get(str(exe.resolve()))==EXE and pins.get(str(data.resolve()))==PAYLOAD)
 summaries=[]
 for key in('cases','case'):
  item=value.get(key)
  selected=item if isinstance(item,list)else[item]if isinstance(item,dict)else[]
  for row in selected:
   if isinstance(row,dict):summaries.append(facts(row))
 return dict(version=version,path=str(p),sha256=sha(p),reportedPassed=value.get('passed')is True,
             directPinnedInputs=len(pins),directPinsIntact=not failures,pinFailures=failures,
             explicitlyBindsCurrentExecutableAndPayload=current_bound,scopeAndAcceptanceFacts=facts(value),caseFacts=summaries)


def main():
 need(not OUT.exists(),'Fresh immutable actual requirement audit')
 need(sha(ROOT/BUILD/'mkport_candidate.exe')==EXE and sha(ROOT/BUILD/'roms/mk2ks/mk2ks.mdata')==PAYLOAD,
      'Authoritative current playable pair, not inferred from a historical label')
 query=subprocess.run(['powershell','-NoProfile','-Command',"Get-CimInstance Win32_Process -Filter \"Name = 'mkport_candidate.exe'\" | Select-Object ProcessId,Name | ConvertTo-Json -Compress"],capture_output=True,text=True)
 need(query.returncode==0 and not query.stdout.strip(),'Current native process census empty before read-only audit')
 versions=sorted({v for _,vs in SPECS.values()for v in vs});evidence={}
 for version in versions:
  evidence[version]=inspect_receipt(version)
  r=evidence[version]
  print(json.dumps(dict(version=version,passed=r['reportedPassed'],currentBound=r['explicitlyBindsCurrentExecutableAndPayload'],
                       directPins=r['directPinnedInputs'],pinFailures=len(r['pinFailures']))),flush=True)
 requirements=[]
 for key,(request,vs)in SPECS.items():
  records=[evidence[v]for v in vs]
  requirements.append(dict(key=key,originalRequirement=request,evidenceVersions=list(vs),
                           allListedReceiptsPassedAndPinned=all(r['reportedPassed']and r['directPinsIntact']for r in records),
                           allListedReceiptsExplicitlyCurrentBound=all(r['explicitlyBindsCurrentExecutableAndPayload']for r in records),
                           broadRequirementCompletion='unproven: inspect exact gates, recorded finite limits and missing routes; passing receipts are not automatically whole-scope acceptance'))
 release=ROOT/'release_v5986_current_playtest/MK2_Kano_Sonya_v5219_CURRENT_PLAYTEST.zip'
 pins={r['path']:r['sha256']for r in evidence.values()}
 for p in(Path(__file__),ROOT/BUILD/'mkport_candidate.exe',ROOT/BUILD/'roms/mk2ks/mk2ks.mdata',release):pins[str(p.resolve())]=sha(p)
 report=dict(passed=True,observedUTC=datetime.datetime.now(datetime.timezone.utc).isoformat(),candidate=BUILD,
             objective='Kano and Sonya appear as a natural part of the game in all aspects',requirements=requirements,
             evidence=list(evidence.values()),uniqueDirectPinnedFilesHashed=len(_hashes),inputHashes=pins,
             originalScopePreserved=True,fullPortAcceptance=False,fullGoalComplete=False,goalStatus='active',
             releaseStillCurrentPlaytest=True,newNativeBoots=0,newBuilds=0,newROMCopies=0,newRawMedia=0,newZIPs=0,
             previousGoalTurnClassification='progress: current CPU Bicycle full raster/body/shadow and independent release push qualified',
             thisGoalTurnClassification='progress: authoritative current requirement evidence and all direct pins inspected; no full-completion inference from green finite receipts')
 OUT.mkdir();p=OUT/'report.json';p.write_text(json.dumps(report,indent=2)+'\n');h=sha(p)
 need(subprocess.run(['compact.exe','/C','/EXE:LZX','/F','/I','/Q',str(p)],capture_output=True).returncode==0 and
      hashlib.sha256(p.read_bytes()).hexdigest().upper()==h,'Exact requirement inventory losslessly compressed')
 print(json.dumps(dict(passed=True,requirements=len(requirements),receipts=len(evidence),
                       directPinFailures=sum(len(r['pinFailures'])for r in evidence.values()),
                       explicitCurrentBindings=sum(r['explicitlyBindsCurrentExecutableAndPayload']for r in evidence.values()),
                       fullGoalComplete=False)),flush=True)


if __name__=='__main__':main()
