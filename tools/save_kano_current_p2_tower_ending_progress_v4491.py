"""Record actual current KanoP2 tower/pages while keeping full objective open."""
import ctypes,json,re,subprocess
from pathlib import Path
import verify_kano_current_p2_whole_campaign_v4487 as campaign
ROOT,need,sha=campaign.ROOT,campaign.need,campaign.sha
PARENT=ROOT/'audit_v4471_unpressed_random_mirror_full_scope_checkpoint/checkpoint.json'
OUT=ROOT/'audit_v4492_kano_current_p2_tower_ending_full_scope_checkpoint'

def main():
    need(not OUT.exists(),'Fresh immutable full-scope checkpoint')
    state=json.loads(PARENT.read_text());remaining=list(state['remaining']);pins=dict(state['inputHashes'])
    need(all(sha(p)==h for p,h in pins.items()),'Every inherited full-goal requirement/evidence unchanged')
    def pin(path,wanted=None):
        path=Path(path).resolve();key=str(path);actual=sha(path)
        need((wanted is None or actual==wanted) and (key not in pins or pins[key]==actual),
             'Exact actual compiled/public/source/proof bytes')
        pins[key]=actual
    pin(PARENT);pin(__file__)
    proofpath=campaign.OUT/'report.json';proof=json.loads(proofpath.read_text());pin(proofpath)
    case=proof['case']
    need(proof['passed'] and proof['current3836KanoP2NaturalTowerOwnEndingAttractAccepted'] and
         proof['originalComplete3747AlgorithmRetained'] and case['passed'] and case['unassisted_clear_proven'] and
         case['player']=='kano' and case['human_slot']==2 and case['actualWholeCampaignGrammarRetained'] and
         case['originalPhysicalKanoInputsExactlyUnchanged'] and not case['actualFiniteHostDeadlineReached'] and
         len(case['actualRowCounterexamplesRejected'])==12 and len(case['actualRAMGuestFaultsRejected'])==8,
         'Whole original actual native cold tower clear and original actual campaign/RAM counterexamples')
    pagepath=ROOT/'audit_v4490_kano_current_p2_native_ending_pages_checked/report.json'
    pages=json.loads(pagepath.read_text());pin(pagepath)
    need(pages['passed'] and pages['actualNaturalKanoP2EndingEarlyLatePhotoTextShadowCommonBackgroundAccepted'] and
         pages['physicalSlot']==2 and pages['identity']==17 and pages['actualFullRGBPixelsCompared']==406400 and
         len(pages['actualRAMRecordFaultsRejected'])==8 and
         not pages['allTransitionFramesCinematicsAudioHiddenBackgroundOrExtraBlackPensAccepted'] and
         not pages['fullPortAcceptance'], 'Four actual native pages with all original art/shadow/background gates and exclusions')
    for result in (case,pages):
        for p,h in result['inputHashes'].items():pin(p,h)
    text=(campaign.FOLDER/'run.log').read_text()
    def rows(tag):
        return [dict(re.findall(r'(\w+)=([^\s]+)',line)) for line in text.splitlines()
                if line.startswith('MK2_NAT_CAMPAIGN_'+tag+' ')]
    losses=rows('LOSS');wins=rows('WIN');stages=rows('STAGE')
    start,end=rows('ENDING_START'),rows('ENDING_COMPLETED')
    need(len(start)==len(end)==1,'Exactly one actual own ending and return-to-attract')
    kintaro_start=int(next(r for r in stages if r['stage']=='15')['frame'])
    shao_start=int(next(r for r in stages if r['stage']=='16')['frame'])
    last_kintaro_loss=max([int(r['frame']) for r in losses if r['stage']=='15']+[kintaro_start])
    kintaro=[r for r in wins if r['stage']=='15' and last_kintaro_loss<int(r['frame'])<shao_start and r['slot']=='2']
    need(len(kintaro)==2 and all(r['id']=='17' and r['entry']=='FFFEFA20' and r['pc']=='FF8296B0' and
         r['health'].split(',')[0]=='0' and int(r['health'].split(',')[1])>0 for r in kintaro),
         'Actual final Kintaro match has two owned true17 wins after last native loss, never CPU106/CPU winner credit')
    last_shao_loss=max([int(r['frame']) for r in losses if r['stage']=='16']+[shao_start])
    shao=[r for r in wins if r['stage']=='16' and last_shao_loss<int(r['frame'])<int(start[0]['frame']) and r['slot']=='2']
    ko=[r for r in rows('HEALTH') if r['slot']=='1' and r['after']=='0' and
        last_shao_loss<int(r['frame'])<int(start[0]['frame'])]
    need(len(shao)==len(ko)==2 and all(r['pc']=='FF836700' and r['at']=='010602F0' and int(r['before'])>0 for r in ko) and
         all(r['id']=='17' and r['entry']=='FFFEFA20' and r['pc']=='FF8296B0' for r in shao),
         'Both actual original collision Shao KOs and owned native winner-table reads in final selection')
    need(start[0]['winner']=='2' and start[0]['roster']=='17' and start[0]['health'].split(',')[0]=='0' and
         int(start[0]['health'].split(',')[1])>0 and start[0]['actors']=='00000000,00000000' and
         end[0]['mode']=='11' and end[0]['pictures']=='1,1' and end[0]['texts']=='3,3' and
         int(end[0]['age'])==int(end[0]['frame'])-int(start[0]['frame'])>1200,
         'Actual boss actor retirement, true own two-page ending and natural return to attract')
    query="Get-CimInstance Win32_Process -Filter \"Name='python.exe' OR Name='mkport_candidate.exe'\" | Where-Object { $_.CommandLine -match 'run_kano_current_p2_campaign_ram_v4484.py|verify_kano_current_p2_whole_campaign_v4487.py|verify_kano_current_p2_native_ending_pages_v4489.py|audit_v4485_' } | Select-Object ProcessId,Name,CommandLine | ConvertTo-Json -Compress"
    live=subprocess.run(['powershell.exe','-NoProfile','-Command',query],capture_output=True,text=True)
    need(live.returncode==0 and not live.stdout.strip(),'All actual native/whole/page jobs terminal')
    alloc=ctypes.windll.kernel32.GetCompressedFileSizeW
    alloc.argtypes=[ctypes.c_wchar_p,ctypes.POINTER(ctypes.c_uint32)];alloc.restype=ctypes.c_uint32
    files=[p for folder in (campaign.FOLDER,campaign.capture.OUT,campaign.OUT,pagepath.parent,campaign.boundary.OUT)
           for p in folder.rglob('*') if p.is_file()];allocated=0
    for p in files:
        pin(p);hi=ctypes.c_uint32();lo=alloc(str(p),ctypes.byref(hi));need(lo!=0xffffffff,'Exact current evidence allocation')
        allocated+=(hi.value<<32)|lo
    next_action=('Current3836 KanoP2 now has an actual cold natural tower clear with ordinary paid continues: '
      'two own Kintaro wins in final match, two original collision Shao KOs/own winner reads, true17 own ending '
      'and native attract return. Original3747 full campaign/schedule/selection/morph/native moves/health/'
      'KO/paid-continue/boss physical replay/ending grammar, twelve actual row faults and eight RAM guest '
      'faults retained. Four actual early/late own pages have full RGB equality to pinned original-source '
      'qualified natural P1 pages, preserving photo/story font/black shadow/common background/fault gates. '
      'This is not all transition frames, hidden background/extra black pens, cinematics or ending/audio '
      'acceptance. Do not rerun this accepted KanoP2 cold tower, accepted SonyaP2 tower or completed '
      'held/pressed/unpressed rare four-context Tomb mirror scenes. Next close remaining native ending '
      'transition/audio/current-build contexts or broader Pit/Tomb stock-victim/branch/audio/full move '
      'phase/ground/shadow/CPU/repeat/KO/overlap coverage, then other finishers/morphs/secrets/cinematics '
      'and combined final selection/ladder/names/audio/dependency-aware cleanup/refreshed release. '
      'All five original groups retained. Public1836 unchanged playtest; no new ROM/EXE/raw media or '
      'deletion, no previous cleanup saving recounted. Rejected4473 preflight preserved; corrected4482 '
      'binds the actually executed3744 historical launcher, without changing physical controller bytes.')
    state.update(previousCheckpoint=str(PARENT),inputHashes=pins,
      inputHashInheritance=dict(schema=1,parentCheckpoint=str(PARENT),parentCheckpointSHA256=sha(PARENT),
        mergeRule='Every original full-goal group/evidence/exclusion retained; actual current KanoP2 full tower/scoped native pages added.'),
      previousGoalTurnClassification=state['thisGoalTurnClassification'],
      thisGoalTurnClassification='progress: unchanged original Kano physical inputs on current3836 earn natural P2 tower/own ending/attract; complete original native campaign and actual counterexamples pass; four own native early/late ending pages verified against original-source models.',
      current3836KanoP2NaturalFullCampaignClearAccepted=True,current3836KanoP2OwnEndingAttractAccepted=True,
      current3836KanoP2FullShaoClearAccepted=True,current3836KanoP2NativeEndingPagesAccepted=True,
      current3836KanoP2WholeTowerReport=str(proofpath),current3836KanoP2NativeEndingPageReport=str(pagepath),
      currentKanoP2PageScopeLabelCorrection='Frozen4490 scope docstring inherits original4448 SonyaP2 label; actual identity17/roster17/table rows/current RGB hashes and explicit acceptance fields prove KanoP2. Source4489 performs declared role/reference substitutions only; historical label is not identity authority.',
      current3836KanoP2ActualFinalKintaroOwnWins=kintaro,current3836KanoP2ActualFinalShaoKOs=ko,
      current3836KanoP2NativeEndingStart=start[0],current3836KanoP2NativeEndingCompleted=end[0],
      current3836KanoP2FullEndingTransitionsCinematicsAndAudioAccepted=False,
      currentTurnDiagnosticLogicalBytes=sum(p.stat().st_size for p in files),currentTurnDiagnosticAllocatedBytes=allocated,
      currentTurnNewBuilds=0,currentTurnRawAudioRasterVRAMROMCopies=0,currentTurnDeletedFiles=0,currentTurnReclaimedAllocatedBytes=0,
      cleanupAccounting='Compressed source/text/digests only; native guest/RGB RAM-only. No deletion or historical cleanup saving counted again.',
      gameSourceAndPlayableBytesChangedThisTurn=False,publicLauncherChangedThisTurn=False,publicReleaseZIPChangedThisTurn=False,
      nextAction=next_action,nextImplementationAction=next_action,goalStatus='active',fullPortAcceptance=False,finishedRelease=False)
    need(state['remaining']==remaining and len(remaining)==5,'Original full scope and all five groups intact')
    need(all(sha(p)==h for p,h in pins.items()),'Every inherited/current/public byte unchanged')
    OUT.mkdir();need(subprocess.run(['compact.exe','/C','/I','/Q','/S:'+str(OUT)],capture_output=True).returncode==0,
                    'Checkpoint compressed before writes')
    (OUT/'checkpoint.json').write_text(json.dumps(state,indent=2)+'\n')
    print(json.dumps(dict(checkpoint=str(OUT/'checkpoint.json'),inputPins=len(pins),currentKanoP2NaturalTowerAccepted=True,
        nativeEndingPagesAccepted=True,currentEvidenceAllocatedBytes=allocated,originalRemainingGroups=5,fullPortAcceptance=False),indent=2),flush=True)

if __name__=='__main__':main()
