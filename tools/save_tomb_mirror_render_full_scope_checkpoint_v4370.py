"""Actual whole native mirror rendering progress; all five full-goal groups intact."""
import ctypes,hashlib,json,subprocess
from pathlib import Path
import run_tomb_mirror_render_ram_v4361 as runtime
ROOT,need,sha=runtime.ROOT,runtime.need,runtime.sha
PARENT=ROOT/'audit_v4356_tomb_mirror_full_scope_checkpoint/checkpoint.json'
OUT=ROOT/'audit_v4371_tomb_mirror_render_full_scope_checkpoint'

def main():
    need(not OUT.exists(),'Fresh immutable complete-scope checkpoint')
    state=json.loads(PARENT.read_text());remaining=list(state['remaining']);pins=dict(state['inputHashes'])
    need(all(sha(p)==h for p,h in pins.items()),'Every inherited actual evidence/source/playable byte unchanged')
    def pin(path,wanted=None):
        path=Path(path).resolve();h=sha(path);key=str(path)
        need(key not in pins or pins[key]==h,'Inherited/shared byte identity')
        need(wanted is None or wanted==h,'Exact source/report hash');pins[key]=h
    pin(PARENT);pin(__file__)
    matrixpath=ROOT/'audit_v4369_both_characters_both_slots_true_mirror_tomb_render/report.json'
    matrix=json.loads(matrixpath.read_text())
    need(matrix['passed']and matrix['actualTrueMirrorRenderContexts']==4 and
      matrix['actualWholeVisibleFields']==2148 and matrix['actualExactVisibleRGBPixels']==218236800,
      'All actual4true mirror roles,537whole fields each and every218236800visible RGB pixel exact')
    need(matrix['current3836BothCharactersBothPhysicalSlotsTrueMirrorTombWholeRenderPaletteShadowEraseAccepted']and
      matrix['priorKanoP1NotRerun']and not matrix['mirrorDropAndPressedControlBranchesAccepted']and
      not matrix['allStageVictimAudioAccepted']and not matrix['fullPortAcceptance'],
      'Only actually observed held scenes/render/ground/shadow/erase accepted; missing branch/audio/full-port scope retained')
    pin(matrixpath)
    for p,h in matrix['inputHashes'].items():pin(p,h)
    cases=[];pids=[];folders=[]
    for row in matrix['cases']:
        path=Path(row['report']);r=json.loads(path.read_text());pin(path)
        identity=17 if r['fighter']=='kano'else 18
        need(r['passed']and r['truePhysicalIDs']==[identity,identity]and r['sampledFrames']==537 and
          r['exactRGBPixels']==54559200 and len(r['actualPixelFaultsRejected'])==2 and
          r['oneInitialBaseOnly']and r['laterTargetsNeverUsedAsAnchors'],'Unrelaxed true mirror entire continuous model and actual RGB/VRAM bit faults')
        need(r['nativeMirrorPaletteSelectors']=={'1':[False],'2':[True]}and r['fullPhysicalPaletteChecks']>537 and
          r['nativeShiftLoads']==r['nativeShiftFills']>0 and r['nativeShiftTransfers']>60000,
          'Actual native normal/alternate colours, all palette checks, source-owned native shadows and original erase transfers')
        scene=r['nativeScene'];branch=r['nativeBranch']
        need(scene['nativeInputState']['consecutive_fields']==801 and scene['nativeInputState']['earned_matches']==2 and
          scene['nativeInputState']['passed']and scene['nativeShadowCopies']>0 and
          not scene['nativeDrop']and not branch['nativeDrop']and branch['passed'],
          'Original complete earned1731 input/action/retirement contract; original held motion, no fictional drop')
        folder=((ROOT/'audit_v4362_current_kano_p1_true_mirror_tomb_render_ram')if (r['fighter'],r['side'])==('kano',1)else
          ROOT/f"audit_v4367_{r['fighter']}_p{r['side']}_true_mirror_tomb_render_ram")
        meta=json.loads((folder/'result.json').read_text());process=json.loads((folder/'process.json').read_text())
        need(meta['exit_code']==0 and meta['observedRGBFields']==meta['modelExactFields']==537 and not meta['modelErrors']and
          meta['ramGuestSHA256']=='938D380B3E2CE8DF6A688E2DC64C576CC7A1E554AE341E7B42463129FA5CA821'and
          meta['guest_writes']==0 and meta['assistance']=='none'and meta['rawImageAudioVRAMROMCopiesWritten']==0,
          'Actual terminal unassisted initialized3836 native guest and all live targets verified in RAM')
        need(not list(folder.rglob('*.bin'))and not list(folder.rglob('*.png'))and not list(folder.rglob('*.wav')),
          'No native ROM/VRAM/raster/audio copies persisted')
        for p,h in r['inputHashes'].items():pin(p,h)
        for p in folder.rglob('*'):
            if p.is_file():pin(p)
        cases.append(dict(fighter=r['fighter'],side=r['side'],report=str(path),nativePID=process['pid'],
          sampledFrames=537,exactVisibleRGBPixels=54559200,nativeShadowCopies=scene['nativeShadowCopies'],
          nativeShiftTransfers=r['nativeShiftTransfers'],fullPhysicalPaletteChecks=r['fullPhysicalPaletteChecks'],
          actualNativeRandomValue=scene['actualNativeRandomValue'],nativeDrop=False,
          originalPhysicalControlsAndEarnedStateIdenticalTo4351MirrorReference=True,fullPortAcceptance=False))
        pids.append(process['pid']);folders.append(folder)
    need({(c['fighter'],c['side'])for c in cases}=={('kano',1),('kano',2),('sonya',1),('sonya',2)},'Actual distinct4mirror contexts, never labels as identity')
    for name in ('mk2ks_tomb_mirror_display_ram_v4359.lua','tools/tomb_mirror_render_model_v4360.py',
      'tools/run_tomb_mirror_render_ram_v4361.py','tools/run_remaining_tomb_mirror_render_ram_v4366.py',
      'mame-mkp/unidasm.exe','mame-mkp/src/mame/midway/midtunit.cpp','mk2/mk2-maincpu.bin'):
        pin(ROOT/name)
    q="Get-CimInstance Win32_Process -Filter \"Name='python.exe' OR Name='mkport_candidate.exe'\" | Where-Object { @("
    q+=','.join(map(str,pids))+ ") -contains $_.ProcessId -or $_.CommandLine -match 'run_tomb_mirror_render_ram_v4361.py|run_remaining_tomb_mirror_render_ram_v4366.py' } | Select-Object ProcessId,Name,CommandLine | ConvertTo-Json -Compress"
    checked=subprocess.run(['powershell.exe','-NoProfile','-Command',q],capture_output=True,text=True)
    need(checked.returncode==0 and not checked.stdout.strip(),'Actual native/collector jobs terminal, no stale-file assumption or elapsed-time restart')
    get=ctypes.windll.kernel32.GetCompressedFileSizeW;get.argtypes=[ctypes.c_wchar_p,ctypes.POINTER(ctypes.c_uint32)];get.restype=ctypes.c_uint32
    files=[p for folder in folders for p in folder.rglob('*')if p.is_file()];allocated=0
    for p in files:
        high=ctypes.c_uint32();low=get(str(p),ctypes.byref(high));need(low!=0xffffffff,'Actual diagnostic allocation read');allocated+=(high.value<<32)|low
    logical=sum(p.stat().st_size for p in files)
    original=(ROOT/'mk2/mk2-maincpu.bin').read_bytes();guest=runtime.audio.old.expected()
    lo,hi=(0xff8eb0d0-0xff800000)//8,(0xff8eb1d0-0xff800000)//8
    need(guest[lo:hi]==original[lo:hi],'Actual3836 exact original two-Down Tomb branch bytes')
    ports=(ROOT/'mame-mkp/src/mame/midway/midtunit.cpp').read_text()
    mk2ports=ports.split('static INPUT_PORTS_START( mk2 )',1)[1].split('INPUT_PORTS_END',1)[0]
    need('PORT_BIT( 0x0002, IP_ACTIVE_LOW, IPT_JOYSTICK_DOWN ) PORT_8WAY PORT_PLAYER(1)'in mk2ports and
      'PORT_BIT( 0x0200, IP_ACTIVE_LOW, IPT_JOYSTICK_DOWN ) PORT_8WAY PORT_PLAYER(2)'in mk2ports,
      'Actual original native P1/P2 Down input bits1/9, not guessed controller direction')
    next_action=('All four current3836 true Kano/Kano and Sonya/Sonya held Tomb mirror scenes now pass entire native '
      'CPU/FIFO/DMA/shift continuous one-base/VRAM/RGB model,537fields each through native actor retirement plus30, '
      'normalP1/alternateP2 source palettes, original native compressed floor shadows and erase; 2148visible fields/'
      '218236800RGBpixels exact, eight actual pixel/VRAM faults rejected. Actual same-role physical controls/earned '
      'health/native finish/branch/801cleanup records match4351audio/state references. Do not rerun these frozen held '
      'roles or claim other branches/arenas/audio. Next concrete missing branch: original Tomb victim routine '
      'FF8EB0D0 reads IN0, NOT A0, tests bits1 and9; both Down pressed jumps FF8EB1B0 directly, otherwise FF8EB150 '
      'uses native50/1000 RNG. Local unidasm and actual MK2 input definition confirm P1Down0x0002/P2Down0x0200. '
      'A normal physical both-Down hold after genuine stage activation can exercise actual mirror fall/late victim '
      'scream without forcing RNG/flags/stage/health/identity. Use fresh immutable driver/source/capture leaves, '
      'preserve complete original1731 earned gates and independently qualify the pressed source/IO/owned-task/'
      'phase branch rather than weakening the existing unpressed3643qualification. Existing4held mirror branches '
      'are not substitutes for drop or pressed controls. Unpressed natural RNG drops can also require distinct '
      'legitimate physical command timing, never prescribed RNG. Continue broader Pit/Tomb victims and whole native '
      'stage/victim audio. Original full move art/ground/shadows/erase across arenas/CPU/repeated/KO/overlap, other '
      'finishers/victims/morphs/secrets/cinematics, actual full Kintaro/Shao clears/own endings/attract, final combined '
      'selection/ladder/names/audio/dependency cleanup/refreshed release all remain unchanged requirements. '
      'Preferred4300campaign baseline remains,4320backward policy rejected, strict CPU/Main-reuse/throw gaps retained. '
      'Public1836 launcher/executable/ZIP and installed binary unchanged, not a finished release.')
    state.update(previousCheckpoint=str(PARENT),inputHashes=pins,
      inputHashInheritance=dict(schema=1,parentCheckpoint=str(PARENT),parentCheckpointSHA256=sha(PARENT),
        mergeRule='Every original full-goal requirement/exclusion and inherited logical byte retained; actual bounded mirror render evidence added.'),
      previousGoalTurnClassification=state['thisGoalTurnClassification'],
      thisGoalTurnClassification='progress: actual3836 true mirrors for both characters/both physical slots pass537whole visible frames each, original palettes/ground/source-owned shadows/erase/retirement,2148fields/218236800RGBpixels exact. Full original earned/FIFO/native-source/RGB fault gates retained; pressed/native-random drop branches and other original full-goal gaps not claimed.',
      current3836TrueMirrorTombRenderMatrixReport=str(matrixpath),current3836TrueMirrorTombRenderCases=cases,
      current3836TrueMirrorTombRasterFloorShadowEraseAccepted=True,
      current3836BothCharactersBothPhysicalSlotsHeldTrueMirrorTombWholeRenderPaletteShadowEraseAccepted=True,
      current3836TrueMirrorTombHeldVisibleFields=2148,current3836TrueMirrorTombHeldExactRGBPixels=218236800,
      current3836TrueMirrorTombFullStageVictimAudioAccepted=False,current3836TrueMirrorTombAllDropAndPressedBranchesAccepted=False,
      currentTombMirrorRenderExecHandles=dict(first=47742,remainingMatrix=27987),currentTombMirrorRenderNativePIDs=pids,
      currentTombMirrorOriginalObserverHumanSlotAnnotationNotUsedAsPhysicalIdentityAuthority=True,
      currentTombMirrorBothDownSourceDiscovery=dict(codeRange=['FF8EB0D0','FF8EB1D0'],
        originalCodeSHA256=hashlib.sha256(original[lo:hi]).hexdigest().upper(),
        inputBits={'P1Down':1,'P2Down':9},originalPressedBranchEntry='FF8EB1B0',unpressedRNGEntry='FF8EB150',
        actualNativePressedMirrorBranchExercised=False,pressedBranchStillRequiresActualNativeSourceIOActorMainPhaseQualification=True),
      currentTurnNativeDiagnosticLogicalBytes=logical,currentTurnNativeDiagnosticAllocatedBytes=allocated,
      currentTurnRawAudioRasterVRAMROMCopies=0,currentTurnDeletedFiles=0,currentTurnNewBuilds=0,currentTurnReclaimedAllocatedBytes=0,
      cleanupAccounting='Only compressed native text/source/digest reports created; no new media/ROM copies or deletion, and no prior reclamation savings counted again.',
      gameSourceAndPlayableBytesChangedThisTurn=False,publicLauncherChangedThisTurn=False,publicReleaseZIPChangedThisTurn=False,
      nextAction=next_action,nextImplementationAction=next_action,goalStatus='active',fullPortAcceptance=False,finishedRelease=False)
    need(state['remaining']==remaining and len(remaining)==5,'All five original full-goal requirement groups unchanged')
    need(all(sha(p)==h for p,h in pins.items()),'All actual inherited/new byte pins unchanged')
    OUT.mkdir();need(subprocess.run(['compact.exe','/C','/I','/Q','/S:'+str(OUT)],capture_output=True).returncode==0,'Checkpoint compressed before write')
    (OUT/'checkpoint.json').write_text(json.dumps(state,indent=2)+'\n')
    print(json.dumps(dict(checkpoint=str(OUT/'checkpoint.json'),inputPins=len(pins),trueMirrorRenderContexts=4,
      wholeVisibleFields=2148,exactVisibleRGBPixels=218236800,diagnosticLogicalBytes=logical,diagnosticAllocatedBytes=allocated,
      originalRemainingGroups=5,rawNativeMediaCopies=0,fullPortAcceptance=False),indent=2),flush=True)

if __name__=='__main__':main()
