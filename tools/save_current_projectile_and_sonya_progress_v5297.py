"""Additive whole goal: native Sonya terminal, fresh capture, more real victim roles."""
import ast,datetime,json,subprocess
from pathlib import Path
import current_payload_metadata_context_v5229 as current
import verify_current_sonya_ring_repeat_v5291 as failed_floor
ROOT,need,sha=current.ROOT,current.need,current.sha
PARENT=ROOT/'audit_v5287_kano_complete_current_p1_ending_progress/progress.json'
OUT=ROOT/'audit_v5298_current_projectile_roles_and_sonya_ending_progress'
def main():
    need(not OUT.exists(),'Fresh immutable additive whole-goal progress')
    parent=json.loads(PARENT.read_text())
    need(len(parent['remaining'])==5 and all(sha(p)==h for p,h in parent['newInputHashes'].items()),
      'Every original group and complete Kano pixel/page/hardware evidence retained')
    pins={str(PARENT):sha(PARENT),str(Path(__file__).resolve()):sha(__file__)}
    oldfolder=ROOT/'audit_v5250_sonya_current_p1_ending_pixels'
    failpath=ROOT/'audit_v5250_sonya_current_p1_ending_pixels_checked/report.json'
    old=json.loads((oldfolder/'result.json').read_text());failed=json.loads(failpath.read_text())
    need(old['passed']and old['nativeExit']==0 and not old['endingModelErrors']and
      old['exactContinuousEndingFields']==old['observedEndingRGBFields']==3042 and
      len(old['endingNativePixelFaults'])==2 and not failed['passed']and
      "'bool' object has no attribute 'records'"in failed['error']and
      all(sha(p)==h for p,h in old['inputHashes'].items()),
      'Same87441 real native0/3042matches then actual exporter alias failure retained')
    need(not(oldfolder/'ending_continuous_records.json').exists(),'Missing original per-field export stays unaccepted')
    for p in (failpath,oldfolder/'result.json',oldfolder/'run.log.gz'):pins[str(p)]=sha(p)
    path=ROOT/'audit_v5296_current_sonya_ring_subzero_repeat_checked/report.json'
    # The retained suffix follows the original scope adapter's old leaf label;
    # actual report keys/cases explicitly include both Kano knife and Sonya ring.
    repeat=json.loads(path.read_text())
    need(repeat['passed']and repeat['candidate']==current.NAME and repeat['executableSHA256']==current.EXE_SHA and
      repeat['currentKanoKnifeAndSonyaRingBothSlotsAgainstSubZeroRepeatTwiceAndRecoverVerified']and
      repeat['actualCases']==4 and repeat['actualVerifiedSpecialCycles']==8 and
      repeat['actualContiguousPostFields']==3210 and repeat['actualFullRGBFields']==71 and
      len(repeat['actualSemanticFaultsRejected'])==50 and not repeat['fullArtAcceptance']and
      not repeat['fullAudioAcceptance']and not repeat['fullPortAcceptance']and
      all(sha(p)==h for p,h in repeat['inputHashes'].items()),
      'Every original real semantics/ownership/damage/controls/recovery/publication and50faults retained for additional actual native roles')
    pins[str(path)]=sha(path)
    # Reproduce only the exact prior native-floor assumption failure from the
    # same immutable actual rows; no positive checker is weakened or rewritten.
    checker,load,_=failed_floor.bindings()
    try:checker(load('ring',1),current.expected(),(ROOT/current.NAME/'roms/mk2ks/mk2ks.mdata').read_bytes())
    except ValueError as error:
        need(str(error)=='Independent own/stock floor anchor values','Exact retained failed original Kitana-specific floor assumption')
        floor_error=str(error)
    else:raise ValueError('Original real Sub-Zero floor failure not reproduced')
    census=subprocess.run(['powershell.exe','-NoProfile','-Command',
      'Get-CimInstance Win32_Process | Where-Object { $_.ProcessId -in @(105632,142492,142528,140956) } | Select-Object ProcessId,ParentProcessId,Name,CommandLine | ConvertTo-Json -Compress'],
      capture_output=True,text=True)
    need(census.returncode==0,'Fresh exact authoritative native/host census')
    live=json.loads(census.stdout)if census.stdout.strip()else[]
    if isinstance(live,dict):live=[live]
    need(not any(p['ProcessId']in(142528,140956)for p in live),'Original same87441 real terminal, not timeout/restart')
    folder=ROOT/'audit_v5264_sonya_current_p1_ending_pixels'
    terminal=ROOT/'audit_v5264_sonya_current_p1_ending_pixels_checked/report.json'
    proof=json.loads(terminal.read_text())if terminal.exists()else None
    hosts=[p for p in live if p['ProcessId']==105632 and 'run_p1_ending_deferred_pixels_v5266.py'in p['CommandLine']and '--fighter sonya'in p['CommandLine']]
    natives=[p for p in live if p['ProcessId']==142492 and p['ParentProcessId']==105632 and
      current.NAME in p['CommandLine']and str(folder)in p['CommandLine']and 'mk2ks_p1_ending_deferred_campaign_ram_v5260.lua'in p['CommandLine']]
    need(proof is not None or len(hosts)==len(natives)==1,'Pending only with actual same54808 fresh host/native confirmed live')
    guest=json.loads((folder/'guest_memory_proof.json').read_text())
    need(guest['sha256']==current.GUEST_SHA and guest['everyActualByteComparedInRAM'],
      'Fresh full1MiB independently expected guest exact before natural campaign')
    for name in ('process.json','guest_memory_proof.json','input_hashes_before.json'):
        pins[str(folder/name)]=sha(folder/name)
    if proof:pins[str(terminal)]=sha(terminal)
    files=['tools/run_current_repeated_specials_v5288.py','tools/verify_current_sonya_ring_repeat_v5291.py',
      'tools/verify_current_sonya_ring_repeat_v5293.py','tools/verify_current_projectile_repeat_v5295.py',
      'audit_v5294_current_sonya_ring_subzero_repeat_checked/report.json']
    for name in files:
        p=ROOT/name
        if p.suffix=='.py':ast.parse(p.read_text(),filename=str(p))
        pins[str(p)]=sha(p)
    need(all(sha(p)==h for p,h in pins.items()),'All original failed/current/native/semantic evidence bytes exact')
    report=dict(schema=1,observedUTC=datetime.datetime.now(datetime.timezone.utc).isoformat(),
      parentAdditiveJournal=str(PARENT),goalStatus='active',remaining=parent['remaining'],
      mergeRule='Additive only. Full original scope unchanged. Four new Prison/Sub-Zero projectile repeat roles do not replace all special/arena/CPU/KO/overlap/art/shadow/audio/finisher requirements.',
      previousGoalTurnClassification='progress: same2505 complete current Kano P1 ending/native3040pixels, pages and full hardware/all original faults verified; every original remaining group preserved',
      thisGoalTurnClassification='progress: same87441 Sonya real native0 ending/attract347965 and3042modelmatches/twoactualpixel faults completed, known post-exportbool collision retained and incomplete per-field proof unaccepted. Only after actual terminal launched source-qualified5266 fresh Sonya to preserve exports; exact1MiB guest verified and54808/105632/142492 live. Added actual cold current-candidate Kano knife/Sonya ring against real selected Sub-Zero in both human roles, eight physical activations/recoveries and ordinary follow-up. Full original semantic checker initially rejected Kitana floor83; original MK2 ROM tables independently derive Sub-Zero floor85 (native131 vs Kitana133 at original Prison216). Fresh source guard preserves entire table and all ownership/physics/commands/health/publication gates; allfourcases3210post-fields/71RAMRGBscenes/267bodyparts and50actualsemantic faults accepted.',
      originalSonyaNativeTerminal=dict(nativeExit=0,actualNativeStop=347965,endingStart=344923,attractStart=347665,
        exactObservedModelFields=3042,fullFinalPixelHardwareAcceptance=False,postExportAliasFailure=str(failpath)),
      currentSonyaFullCapture=dict(execSession=54808,hostPID=105632,nativePID=142492,
        exactCurrentlyLiveHost=hosts,exactCurrentlyLiveNative=natives,terminal=proof,growingLogNotPinned=True),
      newCurrentProjectileRoles=dict(report=str(path),actualCases=4,actualPhysicalCycles=8,
        completePostFields=3210,actualFullRAMRGBFields=71,sourceBoundPublishedBodyParts=267,
        actualSemanticFaultsRejected=50,fullArtShadowsAudioCPUOtherArenasOrKOAccepted=False),
      failedFloorCheck=dict(source='tools/verify_current_sonya_ring_repeat_v5291.py',reproducedError=floor_error,
        cause='Original Kitana-only83 floor guard; source-derived native Sub-Zero85, not a new character alignment defect'),
      newBuilds=0,newRawROMVRAMImageAudioFilesWritten=0,newDeletedFiles=0,
      publicPlayableChanged=False,refreshedReleaseZIP=False,fullPortAcceptance=False,newInputHashes=pins,
      nextAction='Poll same54808/105632/142492 while actually live; never timeout/loss restart. After actual terminal preserve its expected one-unrendered-stop-seed cleanup failure, run5280 --fighter sonya against full retained actual per-field exports, then5282 pages and5284 complete hardware/all27metadata/8terminal/2bit faults. Continue broader native special victim/phase/arena/CPU/KO/overlap art/shadow/audio contexts and other finishers. All five original groups remain verbatim.')
    OUT.mkdir();(OUT/'progress.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(journal=str(OUT/'progress.json'),goalStatus='active',newRealProjectileRoles=4,
      actualSpecialCycles=8,actualSemanticFaultsRejected=50,freshSonyaFullCaptureLive=bool(natives),
      originalSonyaNativeTerminal=0,fullPortAcceptance=False,newBuilds=0),indent=2),flush=True)
if __name__=='__main__':main()
