"""Record actual natural SonyaP2 tower/ending progress; full port goal stays open."""
import ctypes,json,subprocess
from pathlib import Path
import verify_sonya_p2_native_ending_pages_v4448 as pages
ROOT,need,sha=pages.ROOT,pages.need,pages.sha
PARENT=ROOT/'audit_v4445_kintaro_pressure_guard_full_scope_checkpoint/checkpoint.json'
OUT=ROOT/'audit_v4451_sonya_p2_native_tower_ending_full_scope_checkpoint'

def main():
    need(not OUT.exists(),'Fresh immutable full-scope checkpoint')
    state=json.loads(PARENT.read_text());remaining=list(state['remaining']);pins=dict(state['inputHashes'])
    need(all(sha(p)==h for p,h in pins.items()),'Every inherited original full-goal input byte unchanged')
    def pin(p,wanted=None):
        key=str(Path(p).resolve());h=sha(p)
        need((wanted is None or h==wanted) and (key not in pins or pins[key]==h),'Exact shared proof input')
        pins[key]=h
    pin(PARENT);pin(__file__)
    proof_path=pages.campaign.OUT/'report.json';proof=json.loads(proof_path.read_text());pin(proof_path)
    need(proof['passed'] and proof['case']['passed'] and proof['actualNaturalSonyaP2TowerClearAccepted'] and
         proof['case']['unassisted_clear_proven'] and proof['case']['actualWholeCampaignGrammarRetained'] and
         proof['case']['physicalCampaignExactlyUnchanged'] and proof['case']['hostObservationOnlyExtended'],
         'Complete independent native whole campaign and unchanged bounded-prefix grammar')
    page_path=pages.OUT/'report.json';page=json.loads(page_path.read_text());pin(page_path)
    need(page['passed'] and page['actualNaturalSonyaP2EndingEarlyLatePhotoTextShadowCommonBackgroundAccepted'] and
         page['actualFullRGBPixelsCompared']==406400 and not page['fullPortAcceptance'] and
         not page['allTransitionFramesCinematicsAudioHiddenBackgroundOrExtraBlackPensAccepted'],
         'Actual four early/late native pages accepted with original exclusions intact')
    for r in (proof['case'],page):
        for p,h in r['inputHashes'].items():pin(p,h)
    folder=pages.campaign.FOLDER;meta=json.loads((folder/'result.json').read_text())
    need(meta['exit_code']==0 and meta['player']=='sonya' and meta['human_slot']==2 and
         meta['assistance']=='none' and not meta['cheats_enabled'] and meta['actualNativeFrameCallbacks']==78 and
         meta['rawRasterFilesWritten']==meta['raw_audio_files_written']==meta['new_builds_or_rom_copies']==meta['guestDumpFilesWritten']==0,
         'Actual terminal natural capture, RAM-only media, no assistance/new builds')
    rows=pages.campaign.spacing.parse((folder/'run.log').read_text())
    start=next(r for r in rows if r['tag']=='ENDING_START')
    end=next(r for r in rows if r['tag']=='ENDING_COMPLETED')
    shao=next(r for r in rows if r['tag']=='STAGE' and r['stage']=='16')
    ko=[r for r in rows if r['tag']=='HEALTH' and r['slot']=='1' and r['after']=='0' and
        shao['frame']<r['frame']<start['frame']]
    need(len(ko)==2 and all(r['pc']=='FF836700' and int(r['before'])>0 and r['at']=='010602F0' for r in ko),
         'Both actual native Shao collision KOs, never only a stage marker or a planned Ring')
    need(start['winner']=='2' and start['roster']=='18' and start['health'].split(',')[0]=='0' and
         int(start['health'].split(',')[1])>0 and start['actors']=='00000000,00000000' and
         end['mode']=='11' and end['pictures']=='1,1' and end['texts']=='3,3' and
         end['frame']-start['frame']==int(end['age'])>1200,
         'Actual owned boss retirement, own two ending pages and native return to attract')
    cleanup_path=ROOT/'audit_v4447_generated_build_cache_compression/report.json'
    cleanup=json.loads(cleanup_path.read_text());pin(cleanup_path)
    need(cleanup['passed'] and cleanup['originalBytesAndMtimesPreserved'] and cleanup['deletedFiles']==0 and
         cleanup['sourceChanges']==0 and cleanup['newAllocatedBytesReclaimed']==
         cleanup['allocatedBytesBefore']-cleanup['allocatedBytesAfter']>0,
         'Exact newly reclaimed compiler-cache allocated bytes, no recycled historical saving')
    pin(ROOT/'tools/compress_generated_build_cache_v4446.py',cleanup['sourceSHA256'])
    for p,h in cleanup['publicInputHashes'].items():pin(p,h)
    query="Get-CimInstance Win32_Process -Filter \"Name='python.exe' OR Name='mkport_candidate.exe'\" | Where-Object { $_.CommandLine -match 'run_kintaro_pressure_guard_long_campaign_v4439.py|verify_kintaro_pressure_guard_long_whole_campaign_v4442.py|verify_sonya_p2_native_ending_pages_v4448.py|audit_v4440_' } | Select-Object ProcessId,Name,CommandLine | ConvertTo-Json -Compress"
    active=subprocess.run(['powershell.exe','-NoProfile','-Command',query],capture_output=True,text=True)
    need(active.returncode==0 and not active.stdout.strip(),'All relevant native capture/verification jobs terminal')
    alloc=ctypes.windll.kernel32.GetCompressedFileSizeW
    alloc.argtypes=[ctypes.c_wchar_p,ctypes.POINTER(ctypes.c_uint32)];alloc.restype=ctypes.c_uint32
    files=[p for p in folder.rglob('*') if p.is_file()];allocated=0
    for p in files:
        pin(p);hi=ctypes.c_uint32();lo=alloc(str(p),ctypes.byref(hi));need(lo!=0xffffffff,'Exact capture allocation')
        allocated+=(hi.value<<32)|lo
    for name in ('mk2ks_kintaro_pressure_guard_long_campaign_ram_v4436.lua',
                 'tools/qualify_kintaro_pressure_guard_long_source_v4437.py',
                 'tools/run_kintaro_pressure_guard_long_campaign_v4439.py',
                 'tools/verify_kintaro_pressure_guard_long_whole_campaign_v4442.py',
                 'tools/verify_sonya_p2_native_ending_pages_v4448.py',
                 'audit_v4438_kintaro_pressure_guard_long_source_preflight/report.json',
                 'audit_v4441_kintaro_pressure_guard_long_campaign_observed/report.json'):pin(ROOT/name)
    next_action=('Current3836 SonyaP2 now has a complete actual natural cold tower clear with normal paid '
      'continues: actual Kintaro match clear, two original collision ShaoKahn KOs, own native ending '
      'dispatch/pages and return-to-attract. Extended observation retained every bounded4428 native '
      'record before host deadline byte-for-byte; unchanged physical4424 policy and full original '
      'campaign/state/health/schedule/KO/IDs/morph/selection/ending/input counterexamples passed. Four '
      'actual early/late ending pages have complete RGB equality to pinned previously qualified natural '
      'P1 pages; original donor-photo/native story font/one-pixel black shadow/common stock background '
      'gates rechecked with exclusions retained. This is not complete transition-frame/cinematic/'
      'every-black-pen/native audio acceptance. Do not rerun this accepted cold tower or completed '
      'held/pressed Tomb mirrors. Next close the still missing native ending audio/transition and '
      'broader Pit/Tomb victim/branch/audio or full move-phase/ground/shadow/CPU/repeat/KO/overlap '
      'gates using read-only native RAM observers and original-source models. Inspect specific '
      'existing missing cases/dependencies first; do not infer all-character/current-build coverage '
      'from a SonyaP2 success or historical3680 KanoP2 proof. All five original scope groups remain '
      'intact, including other finishers/victims/morphs/secrets/cinematics and combined final '
      'selection/ladder/names/audio/dependency cleanup/refreshed release ZIP. Public1836 playtest '
      'and dirty MAME source remain unchanged, not a finished release. No new build/raw media/ROM '
      'copies were made. Generated compiler cache reclaimed498825626 new allocated bytes via '
      'lossless NTFS LZX after the previously observed linker became terminal; no files removed.')
    state.update(previousCheckpoint=str(PARENT),inputHashes=pins,
      inputHashInheritance=dict(schema=1,parentCheckpoint=str(PARENT),parentCheckpointSHA256=sha(PARENT),
        mergeRule='All inherited full-goal groups/evidence/strict exclusions retained; actual complete native SonyaP2 tower and scoped ending pages added.'),
      previousGoalTurnClassification=state['thisGoalTurnClassification'],
      thisGoalTurnClassification='progress: original bounded full-native verification completed; unchanged physical policy extended cold capture earns true SonyaP2 natural tower/own ending/attract and four source-qualified early/late pages; new allocated compiler cache saving verified.',
      current3836SonyaP2FullShaoClearAccepted=True,current3836SonyaP2OwnEndingAttractAccepted=True,
      current3836SonyaP2NaturalFullCampaignClearAccepted=True,currentDevelopmentSonyaP2FullTowerClearAccepted=True,
      current3836SonyaP2WholeTowerProof=str(proof_path),current3836SonyaP2WholeTowerCapture=str(folder),
      current3836SonyaP2NaturalEndingPageProof=str(page_path),current3836SonyaP2NaturalEndingPagesAccepted=True,
      current3836SonyaP2FullEndingTransitionsCinematicsAndAudioAccepted=False,
      current3836SonyaP2ActualNativeShaoKOs=ko,current3836SonyaP2NativeEndingStart=start,
      current3836SonyaP2NativeEndingCompleted=end,
      currentTurnDiagnosticLogicalBytes=sum(p.stat().st_size for p in files),currentTurnDiagnosticAllocatedBytes=allocated,
      currentTurnNewBuilds=0,currentTurnRawAudioRasterVRAMROMCopies=0,currentTurnDeletedFiles=0,
      currentTurnReclaimedAllocatedBytes=cleanup['newAllocatedBytesReclaimed'],currentTurnCleanupReport=str(cleanup_path),
      gameSourceAndPlayableBytesChangedThisTurn=False,publicLauncherChangedThisTurn=False,publicReleaseZIPChangedThisTurn=False,
      nextAction=next_action,nextImplementationAction=next_action,goalStatus='active',fullPortAcceptance=False,finishedRelease=False)
    need(state['remaining']==remaining and len(remaining)==5,'All five original goal requirement groups intact')
    need(all(sha(p)==h for p,h in pins.items()),'Every source/evidence/playable input unchanged before saving')
    OUT.mkdir();need(subprocess.run(['compact.exe','/C','/I','/Q','/S:'+str(OUT)],capture_output=True).returncode==0,
                    'Checkpoint compressed before writes')
    (OUT/'checkpoint.json').write_text(json.dumps(state,indent=2)+'\n')
    print(json.dumps(dict(checkpoint=str(OUT/'checkpoint.json'),inputPins=len(pins),
      naturalSonyaP2TowerOwnEndingAttractAccepted=True,nativeEarlyLateEndingPagesAccepted=True,
      newAllocatedBytesReclaimed=cleanup['newAllocatedBytesReclaimed'],fullPortAcceptance=False,
      originalRemainingGroups=5),indent=2),flush=True)

if __name__=='__main__':main()
