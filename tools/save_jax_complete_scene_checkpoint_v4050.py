"""Finalize this bounded Jax scene proof; preserve the complete active objective."""
import json,subprocess
from pathlib import Path
import run_native_sound_delivery_ram_v3682 as current
ROOT,need,sha=current.ROOT,current.need,current.sha
PARENT=ROOT/'audit_v4047_jax_scene_ram_campaign_full_scope_checkpoint/checkpoint.json'
OUT=ROOT/'audit_v4051_jax_complete_scene_full_scope_checkpoint'

def main():
    need(not OUT.exists(),'Fresh immutable checkpoint')
    state=json.loads(PARENT.read_text());remaining=list(state['remaining']);pins={}
    need(state['goalStatus']=='active'and len(remaining)==5 and not state['fullPortAcceptance']and not state['finishedRelease'],'Full original objective remains incomplete')
    def pin(path,wanted=None):
        path=Path(path).resolve();key=str(path);digest=sha(path)
        need(wanted is None or digest==wanted,'Exact accepted evidence unchanged '+key)
        need(key not in pins or pins[key]==digest,'Consistent proof pin')
        need(key not in state['inputHashes']or state['inputHashes'][key]==digest,'Shared inherited bytes unchanged')
        pins[key]=digest
    pin(PARENT);reports={}
    for leaf in('audit_v4039_jax_clap_earned_checked','audit_v4041_jax_clap_native_fifo_checked','audit_v4049_jax_clap_scene_matrix_compression'):
        path=ROOT/leaf/'report.json';r=json.loads(path.read_text());need(r['passed']and not r['fullPortAcceptance'],'Bounded proof passed '+leaf);reports[leaf]=r;pin(path)
        for p,h in r['inputHashes'].items():pin(p,h)
    earned=reports['audit_v4039_jax_clap_earned_checked'];fifo=reports['audit_v4041_jax_clap_native_fifo_checked'];storage=reports['audit_v4049_jax_clap_scene_matrix_compression']
    need(earned['actualContexts']==4 and earned['actualStateFaultsRejected']==32 and earned['originalCompleteEarnedStateAlgorithmRetained']and earned['sourceBoundOriginalJaxTaskAccepted'],'Four actual original earned-state contexts and32 faults')
    need(fifo['actualContexts']==4 and fifo['actualRowFaultsRejected']==40 and not fifo['allArenaFloorShadowsAccepted'],'Four actual native FIFO/projection/floor/shadow contexts and40 faults, not all arenas')
    wanted={('kano',1):(10972,592),('kano',2):(10988,608),('sonya',1):(10986,606),('sonya',2):(10992,612)}
    for c in fifo['cases']:
        key=c['fighter'],c['side'];p=c['nativeFIFO'];total,owned=wanted[key]
        need(p['sourceBoundProjections']==2904 and p['floorShadowCopyCommands']==total and p['actualOwnedCompressedShadowRows']['copies']==owned and p['actualOwnedCompressedShadowRows']['rowStreamVerified'],'Every actual native component/camera/DMA and complete compressed shadow row stream')
    for p in(Path(__file__).resolve(),ROOT/'tools/compact_jax_clap_scene_matrix_v4048.py'):pin(p)
    missing=state['confirmedMissingThisTurnCapturePIDs']+[40096]
    q=subprocess.run(['powershell.exe','-NoProfile','-Command','Get-CimInstance Win32_Process | Where-Object { $_.ProcessId -in @('+','.join(map(str,missing))+') } | Select-Object -ExpandProperty ProcessId'],capture_output=True,text=True)
    need(q.returncode==0 and not q.stdout.strip(),'Exact native capture and original state verifier handles terminal/missing now')
    for relative,wanted in {
      'diagnostic_v1836_ball_register_boundary/mkport_candidate.exe':'34D427A8FB152E89F4B5FDA5CCE7A8BDB2CC3020CD66C42979B53ED1BA15263E',
      'diagnostic_v1836_ball_register_boundary/roms/mk2ks/mk2ks.mdata':'5646E839C73C4DB89BCF7CC87ECADBDA94B1E0D30EB1C0D2ED50A21A5524E23D',
      'release_v1863_current_playtest/MK2_Kano_Sonya_v1836_CURRENT_PLAYTEST.zip':'994AC5535CD65EA92B7BCD19E12EC6669F4527796CD0CA8C7CA28E708A6897EA',
      'mame-mkp/mkport.exe':'413855890FCE3BECAC9B24E11699FAD1CE465ACCBE4B27A93F2DD5819D13A891',
      'mame-mkp/src/mame/midway/midtunit_m.cpp':'EE48F2FBD72749354A44F3B6574D00EB5DD879EC368A73FBDD57540A4F351D34',
      'mame-mkp/src/mame/midway/midtunit.cpp':'07C1FA27AAA0B1C836E462BC6EC13D62DFF405FA2B7F1358D7BB34B51731DA85',
      'mame-mkp/src/mame/midway/midtunit.h':'256577139683DE7226D3EC0966CAC9B44C9C01C96ED561D236112B2DBADC7644'}.items():pin(ROOT/relative,wanted)
    pin(ROOT/state['currentCMD'])
    reclaimed=state['currentTurnReclaimedAllocatedBytes']+storage['reclaimedAllocatedBytes']
    state.update(inputHashes=pins,inputHashInheritance=dict(schema=1,parentCheckpoint=str(PARENT),parentCheckpointSHA256=sha(PARENT),mergeRule='Resolve parent recursively; preserve retired/deleted exclusions and agree on shared fresh pins; do not flatten.'),previousCheckpoint=str(PARENT),
      thisGoalTurnClassification=state['thisGoalTurnClassification']+' Same recorded52768 state qualifier reached terminal0; all four original Jax earned-state/health/hold-release/parser/true-ID position-row/188field completion contexts passed and32 actual faults rejected. Same native generic FIFO/cache/component/DMA/camera/floor/811 compressed-shadow proof passed all four contexts and40 actual faults.11616 source-bound projections,43938 actual native floor-shadow copy commands and2418 own compressed-row copies accepted. Four terminal scene leaves losslessly sealed; complete goal-turn allocated reclaim76623872bytes,0 deletions/0 new builds.',
      currentDevelopmentNativeJaxClapStateReport=str(ROOT/'audit_v4039_jax_clap_earned_checked/report.json'),
      currentDevelopmentNativeJaxClapFIFOReport=str(ROOT/'audit_v4041_jax_clap_native_fifo_checked/report.json'),
      currentDevelopmentNativeJaxClapQualified=dict(ownVictimContexts=4,exactRGBFields=2596,exactRGBPixels=263753600,originalStateFaultsRejected=32,actualFIFOProjectionFloorFaultsRejected=40,sourceBoundProjections=11616,nativeFloorShadowCopyCommands=43938,actualOwnCompressedShadowRowCopies=2418,allOwnShadowRowsVerified=True,allSevenHeadlessGroupsActuallyDrawn=True,scope='Normal costume Dead Pool only, original Jax head-clap. No original-stock full-waveform, all-finisher/audio/arena/alternate-costume/ending or full-port acceptance.'),
      pendingJaxClapQualification=None,currentTurnReclaimedAllocatedBytes=reclaimed,currentTurnDeletedFiles=0,currentTurnNewBuilds=0,confirmedMissingThisTurnCapturePIDs=missing,
      nextImplementationAction='All original Jax head-clap scene/state/FIFO/grounding/shadow tests are terminal and accepted in four normal Dead Pool contexts. Continue full native Jax victim/effect audio and remaining original finisher/victim/morph/secret/cinematic cases, including stock full-waveform controls where required. SonyaP2 zoning Start700 remains a failed-clear observation; next genuine physical control plan should respond to the actual failing Mileena encounter rather than repeat an identical boot/strategy or change health/AI/schedule. Full multi-arena move/ground/shadow/cleanup, genuine own endings, final combined UI/ladder/names/audio regression, dependency-aware obsolete-folder cleanup and refreshed ZIP remain required. Do not restart consumed capture/qualifier handles or promote development3836 based only on this scoped proof.',
      fullPortAcceptance=False,finishedRelease=False,goalStatus='active')
    need(state['remaining']==remaining and state['currentCandidate']=='diagnostic_v1836_ball_register_boundary','Full scope and public release retained')
    OUT.mkdir();need(subprocess.run(['compact.exe','/C','/I','/Q','/S:'+str(OUT)],capture_output=True).returncode==0,'Checkpoint compressed before writes')
    (OUT/'checkpoint.json').write_text(json.dumps(state,indent=2)+'\n')
    print(json.dumps(dict(checkpoint=str(OUT/'checkpoint.json'),freshPins=len(pins),originalJaxStateFaults=32,actualJaxFIFOFloorFaults=40,reclaimedAllocatedBytes=reclaimed,goalStatus='active',fullPortAcceptance=False)),flush=True)

if __name__=='__main__':main()
