"""Add actual current Kano clear and Sonya native107/boss progress to full goal."""
import gzip,hashlib,json,re,subprocess
from pathlib import Path
import native_subzero_legs_context_v4993 as native
import run_extended_sonya_p1_campaign_v5207 as current
ROOT,need,sha=native.ROOT,native.need,native.sha
PARENT=ROOT/'audit_v5193_campaign_activation_progress/progress.json'
OUT=ROOT/'audit_v5210_current_campaign_progress'
PAIRS=[["mk2ks_kintaro_pressure_guard_long_campaign_ram_v4436.lua","mk2ks_sonya_extended_guard_base_ram_v5201.lua"],["mk2ks_sonya_p1_kitana_guard_ram_v4793.lua","mk2ks_sonya_extended_kitana_ram_v5202.lua"],["mk2ks_sonya_p1_jax_jump_guard_ram_v4807.lua","mk2ks_sonya_extended_jax_ram_v5203.lua"],["mk2ks_sonya_p1_subzero_guard_ram_v5159.lua","mk2ks_sonya_extended_subzero_ram_v5204.lua"],["mk2ks_sonya_p1_subzero_crouch_prime_ram_v5174.lua","mk2ks_sonya_extended_prime_ram_v5205.lua"],["mk2ks_sonya_p1_subzero_tested_prime_ram_v5185.lua","mk2ks_sonya_extended_tested_ram_v5206.lua"]]

def main():
 need(not OUT.exists(),'Fresh immutable additive full-goal progress')
 parent=json.loads(PARENT.read_text())
 sonya_path=ROOT/'audit_v5198_tested_prime_terminal_checked/report.json'
 kano_path=ROOT/'audit_v5200_current_kano_p1_whole_campaign_checked/report.json'
 sonya=json.loads(sonya_path.read_text());kano=json.loads(kano_path.read_text())
 need(sonya['passed']and sonya['nativeExit']==0 and
  sonya['actualWholeBoundedNativeCampaign']['actualStages']==list(range(13))+[14,15]and
  sonya['actualWholeSubZeroPhysicalReplay']['actualCompleteGuardFields']==102444 and
  sonya['actualWholeSubZeroPhysicalReplay']['actualNativeHumanUppercut107Stores']==35 and
  sonya['actualWholeSubZeroPhysicalReplay']['actualNativeLegActivations']==240 and
  sonya['actualWholeBoundedNativeCampaign']['actualOriginalMorphRestoreRows']==8 and
  not sonya['actualNaturalTowerClearAccepted'],'Whole actual bounded Sonya native progression/107/morphs, not bosses or ending')
 need(kano['passed']and kano['actualNaturalCurrentKanoP1BossesOwnEndingAttractAccepted']and
  kano['case']['unassisted_clear_proven']and kano['case']['stages_reached']==list(range(13))+[14,15,16]and
  kano['case']['observedBossFields']==32607 and kano['actualAttractFollowThroughFields']==300 and
  kano['actualNativeCacheGlobalStores']==0 and len(kano['actualNativeAndRAMProofFaultsRejected'])==18,
  'Entire original current Kano native/boss physical-input/own ending/300attract and actual fault grammar')
 deltas=[]
 for i,(old,new)in enumerate(PAIRS):
  before=(ROOT/old).read_text();after=(ROOT/new).read_text()
  restored=after
  for lower_old,lower_new in PAIRS[:i]:restored=restored.replace(lower_new,lower_old)
  if i==0:
   need(restored.count("assert(limit==18000,'Finite host-only observation; no victory supplied')")==1,
    'One finite observation deadline change')
   restored=restored.replace("assert(limit==18000,","assert(limit==5900,",1)
  need(restored==before,'Entire actual physical-controller chain byte-exact after only path/deadline restoration')
  deltas.append(dict(previous=old,current=new,previousSHA256=sha(ROOT/old),currentSHA256=sha(ROOT/new),
   onlyChanges='host observer5900to18000'if i==0 else'transitive source path only'))
 previous_host=(ROOT/'tools/run_tested_prime_sonya_campaign_v5186.py').read_text()
 actual_host=Path(current.__file__).read_text()
 restored=actual_host
 for old,new in PAIRS:restored=restored.replace(new,old)
 restored=restored.replace('audit_v5208_extended_sonya_p1_campaign','audit_v5187_tested_prime_sonya_p1_campaign')
 restored=restored.replace("MK2KS_CAMPAIGN_OBSERVER_LIMIT='18000'","MK2KS_CAMPAIGN_OBSERVER_LIMIT='5900'")
 restored=restored.replace("'-str','18100'","'-str','6000'")
 need(restored==previous_host,'Entire host unchanged except source routing/capture path/finite observer deadline')
 process=json.loads((current.OUT/'process.json').read_text())
 command='Get-CimInstance Win32_Process -Filter "Name=\'mkport_candidate.exe\' OR Name=\'python.exe\'" | Where-Object {$_.ProcessId -in '+str(process['pid'])+','+str(process['hostPID'])+'} | Select-Object ProcessId,ParentProcessId,CommandLine | ConvertTo-Json -Compress'
 census=subprocess.run(['powershell.exe','-NoProfile','-Command',command],capture_output=True,text=True)
 need(census.returncode==0,'Fresh authoritative exact native/collector census')
 live=json.loads(census.stdout)if census.stdout.strip()else[]
 if isinstance(live,dict):live=[live]
 terminal_path=current.OUT/'result.json';terminal=json.loads(terminal_path.read_text())if terminal_path.exists()else None
 if terminal is None:
  need(any(r['ProcessId']==process['pid']and str(current.OUT)in r['CommandLine']for r in live)and
   any(r['ProcessId']==process['hostPID']and 'run_extended_sonya_p1_campaign_v5207.py'in r['CommandLine']for r in live),
   'Pending only with both actual currently live exact commands')
 proof=json.loads((current.OUT/'guest_memory_proof.json').read_text())
 need(proof['everyActualByteComparedInRAM']and proof['sha256']==native.GUEST_SHA and
  proof['captureSourceSHA256']==sha(current.__file__)and proof['transportSourceSHA256']==sha(ROOT/current.LUA),
  'Actual new cold current initialized guest RAM proof')
 pins={}
 for report in(sonya,kano):
  for p,h in report['inputHashes'].items():
   need(p not in pins or pins[p]==h,'Consistent actual compiled/control/evidence byte pins');pins[p]=h
 for p,h in json.loads((current.OUT/'input_hashes_before.json').read_text()).items():
  need(p not in pins or pins[p]==h,'Consistent new actual inputs');pins[p]=h
 for p in[PARENT,sonya_path,kano_path,Path(__file__),current.OUT/'process.json',current.OUT/'guest_memory_proof.json']:
  pins[str(p.resolve())]=sha(p)
 for old,new in PAIRS:
  for name in(old,new):pins[str((ROOT/name).resolve())]=sha(ROOT/name)
 need(all(sha(p)==h for p,h in pins.items()),'Every existing successful/failing source/proof byte retained')
 remaining=parent['remaining'];need(len(remaining)==5,'All five full original unfinished groups preserved verbatim')
 report=dict(schema=1,parentAdditiveJournal=str(PARENT),goalStatus='active',remaining=remaining,
  mergeRule='Read with5193and every preceding full-goal journal. Requirements/evidence/exclusions persist; current Kano natural clear completes only the verified KanoP1 portion, not Sonya/P2/ending pixels/audio/all-art/port/release.',
  previousGoalTurnClassification='no progress: brief acknowledgement only; revalidated native state before action',
  thisGoalTurnClassification='progress: consumed actual5187native0terminal; complete source-bound native stage0..12,14,15/Sonya ownership/wins/specials/morphs and102444Sub fields independently checked, including35original HUMAN107 and240legs. New current Kano P1 run cleared actual native Kintaro/ShaoKahn, own two-page ending and300attract fields; whole unchanged original campaign/boss-button/source/health/winner/continue/morph/ending grammar and18actual faults accepted. Longer Sonya observation cold run started only after previous terminal; all physical policies byte-identical, only finite host deadline extends.',
  currentSonyaTerminal=dict(report=str(sonya_path),execSession=3931,execTerminalConsumed=True,nativeExit=0,
   frames=322771,actualStages=list(range(13))+[14,15],actualOwnRoundWins=41,nativeSpecials=934,
   nativeSubZeroLegs=240,nativeHumanUppercuts107=35,originalShangMorphRestoreRows=8,cacheGlobalStores=0,
   actualNaturalTowerClearAccepted=False),
  currentKanoClear=dict(report=str(kano_path),execSession=96735,execTerminalConsumed=True,nativeExit=0,
   frames=85094,actualStages=list(range(13))+[14,15,16],actualOwnRoundWins=33,
   bossPhysicalFields=32607,bossOwnRoundWins=5,actualBossNativeUppercuts=56,
   endingStart=82054,endingCompleted=84794,endingPictureReads=[1,1],endingTextReads=[3,3],
   returnToAttractFields=300,cacheGlobalStores=0,actualNaturalKanoP1BossesOwnEndingAttractAccepted=True,
   fullEndingPixelsAccepted=False,completeCampaignAudioAccepted=False),
  longerSonyaObservation=dict(execSession=44535,nativePID=process['pid'],collectorPID=process['hostPID'],
   actualLiveProcesses=live,nativeTerminal=terminal is not None,terminalReport=str(terminal_path)if terminal else None,
   hostObserverSeconds=18000,actualPhysicalPoliciesByteIdentical=True,actualSourceRestorationProof=deltas,
   growingLogNotPinnedAsTerminal=terminal is None,compressedTraceBytes=(current.OUT/'run.log.gz').stat().st_size,
   fullGuestRAMProof=proof,actualNaturalTowerClearAccepted=False),
  inputHashes=pins,knownCandidateMetadataReleaseDefect=sonya['exactCompiledMetadataWarning'],
  dirtyLiveDeclarationInspected=dict(path=str(ROOT/'mame-mkp/src/mame/midway/midtunit.cpp'),
   SHA256='07C1FA27AAA0B1C836E462BC6EC13D62DFF405FA2B7F1358D7BB34B51731DA85',
   note='Dirty live declaration differs from compiled4992; neither touched. Correct CRC/SHA1 against final actually packaged payload in next production build. No warning waiver in final release.'),
  publicPlayableChanged=False,newBuilds=0,newlyDeletedFiles=0,rawGuestMediaAudioFilesWritten=0,
  fullPortAcceptance=False,finishedRelease=False,
  nextAction='Poll same44535and actual141820/142152while live; consume actual terminal, do not restart because timeout or loss. Verify complete current extended Sonya campaign with unchanged native/boss/controller grammar and actual RAM provenance. Existing5198Sonya bounded only,5200KanoP1clear verified. Continue broader Pit/Tomb/victims/finishers/morphs/secrets/cinematics/full move-phase/grounding/shadows/all arenas/CPU KO overlap/audio/combined selection ladder names regression/dependency-aware cleanup/refreshed release. Correct final payload ROM declaration metadata before production. No proxies or native health/AI/RNG/state assistance.',
  storage='New test text losslessly gzip-streamed. Six tiny Lua controller copies, no native binaries/ROM/full build trees/raw guest/RGB/PCM. Previous reclamation not recounted.')
 OUT.mkdir();(OUT/'progress.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps(dict(journal=str(OUT/'progress.json'),goalStatus='active',currentKanoP1NaturalClearAccepted=True,
  currentSonyaReachedKintaro=True,actualSonyaHuman107Stores=35,longerSonyaObservation=report['longerSonyaObservation'],
  fullPortAcceptance=False),indent=2),flush=True)

if __name__=='__main__':main()

