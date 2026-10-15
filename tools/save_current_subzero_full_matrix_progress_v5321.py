"""Additive whole-goal checkpoint for current complete Sub-Zero move matrix.

All eight human moves/both slots/36repeatedcycles include four real airborne
Square Wave contacts. Full original body/shadow/source/fault guards retained.
Neither this finite stage/victim matrix nor new stock-raw source qualification
closes broader arena/CPU/KO/overlap/audio/finisher/cinematic/release requirements.
"""
import ctypes,datetime,json,struct,subprocess
from collections import defaultdict
from pathlib import Path
from ctypes import wintypes
import current_payload_metadata_context_v5229 as current
import verify_current_air_square_repeat_v5309 as failed_air
import verify_current_subzero_special_shadow_v5302 as ground
import verify_special_repeat_v5115 as original
ROOT,need,sha=current.ROOT,current.need,current.sha
PARENT=ROOT/'audit_v5305_current_subzero_shadows_and_complete_sonya_ending_progress/progress.json'
OUT=ROOT/'audit_v5322_current_subzero_all_special_body_shadow_progress'
def main():
    need(not OUT.exists(),'Fresh immutable additive whole-goal progress')
    parent=json.loads(PARENT.read_text())
    need(parent['goalStatus']=='active'and len(parent['remaining'])==5 and
      all(sha(p)==h for p,h in parent['newInputHashes'].items()),
      'All five original groups, full P1 endings and previous actual shadow roles retained byte-exact')
    guest=current.expected();payload=(ROOT/current.NAME/'roms/mk2ks/mk2ks.mdata').read_bytes()
    pins={str(PARENT):sha(PARENT),str(Path(__file__).resolve()):sha(__file__)}
    physical=[]
    for name,key,cases,cycles,faults in (
      ('audit_v5320_current_subzero_full_repeat_matrix_checked','currentTrueSubZeroNativeVictimBothRolesAllEightMovesVerified',16,32,194),
      ('audit_v5312_current_air_square_subzero_repeat_checked','currentTrueSubZeroBothRolesVerified',2,4,26)):
        path=ROOT/name/'report.json';report=json.loads(path.read_text())
        need(report['passed']and report[key]and report['actualCases']==cases and
          report['actualVerifiedSpecialCycles']==cycles and len(report['actualSemanticFaultsRejected'])==faults and
          report['candidate']==current.NAME and report['executableSHA256']==current.EXE_SHA and
          all(sha(p)==h for p,h in report['inputHashes'].items())and not report['fullPortAcceptance'],
          'Every full original physical semantics and actual-fault matrix retained for current native roles')
        pins[str(path)]=sha(path);physical.append(report)
    evidence=[];cases=[];native_ids=[];raw_stock_poses=set()
    for move,side,air in [(m,s,False)for m in original.SPECS for s in (1,2)]+[('square',s,True)for s in (1,2)]:
        version=5314 if air else 5318 if move=='leg'else 5303
        stem='current_air_square_shadow'if air else 'current_stock_raw_reaction_shadow'if move=='leg'else 'current_special_shadow'
        path=ROOT/f'audit_v{version}_{stem}_{move}_p{side}_sub_zero_checked/report.json'
        report=json.loads(path.read_text());case=report['case']
        folder=ROOT/f'audit_v{5307 if air else 5300}_{"current_air_square_shadow"if air else"current_special_shadow"}_{move}_p{side}_sub_zero'
        observed=ROOT/f'audit_v{5308 if air else 5301}_{"current_air_square_shadow"if air else"current_special_shadow"}_{move}_p{side}_sub_zero_observed/report.json'
        runtime=json.loads(observed.read_text());process=json.loads((folder/'process.json').read_text())
        need(report['passed']and runtime['passed']and runtime['nativeExit']==0 and runtime['victim']=='sub_zero'and
          runtime['nativeStderrEmpty']and report['candidate']==current.NAME and report['executableSHA256']==current.EXE_SHA and
          case['entryBodyPublicationProven']and case['everyReadyBodyComponentSourceBound']and
          case['actualContiguousActorFields']==case['actualShadowEligibilityCalls']and
          case['actualNativeBodyCandidates']==case['actualOwnedShadowComponents']and
          case['unattributedOtherObjectShadowCopies']==0 and len(case['state']['cycles'])==2 and
          case['state']['trueIdentity']==original.SPECS[move][0]and
          len(report['actualSemanticFaultsRejected'])==(17 if move=='leg'else 11)and
          all(sha(p)==h for p,h in report['inputHashes'].items()),
          'Every ready field/native body/eligibility/complete shadow/ROM stream/fault/actual terminal accounted')
        if air:need(case['state']['actualSquareContactVerified']and all(c['victimDamage']==27 for c in case['state']['cycles']),
          'Four genuine27-damage contacts with both actors physically airborne')
        if move=='leg':
            need(case['originalStockRawReactionNativeScannerRowsSourceBound']and
              set(case['originalStockRawReactionStreams'])=={'0251F2DC_10_48_6000','0251F2DC_10_48_6010'},
              'Both original48-high raw reaction facings, every signed native scanner row independently compared')
            for line in (folder/'run.log').read_text().splitlines():
                if line.startswith('MK2_HPHASE_PROJECTION ')and 'graphic=0251F2DC 'in line:
                    import re
                    row=dict(re.findall(r'(\w+)=([^\s]+)',line));need(row['id']=='8','Raw reaction is original stock victim8, never an imported raw added fighter')
                    raw_stock_poses.add(int(row['pose'],16))
        g=json.loads((folder/'guest_memory_proof.json').read_text());gfx=json.loads((folder/'gfx_memory_proof.json').read_text())
        need(g['sha256']==current.GUEST_SHA and g['everyActualByteComparedInRAM']and
          gfx['bytes']==18976 and gfx['everyActualByteComparedInRAM'],
          'Every actual cold whole1MiB guest and appended GFX independently byte-exact in RAM')
        for p in (path,observed,*folder.rglob('*')):
            if p.is_file():pins[str(p.resolve())]=sha(p)
        new=air or move not in ('knife','ring')
        if new:evidence.extend(p for p in folder.rglob('*')if p.is_file())
        native_ids.append(process['pid'])
        cases.append(dict(move=move,physicalSlot=side,trueVictimID=8,air=air,newThisTurn=new,report=str(path),
          completeActorFields=case['actualContiguousActorFields'],
          fullOwnedBodyParts=case['actualNativeBodyCandidates'],nativeShadowCopies=case['actualSourceBoundShadowCopies'],
          ownAddedFighterShadowCopies=case['actualAddedFighterShadowCopies'],
          nativeFullRAMRGBFields=len(runtime['actualScenes']),actualShadowSemanticFaultsRejected=len(report['actualSemanticFaultsRejected'])))
    need(len(cases)==18 and sum(c['newThisTurn']for c in cases)==14 and
      sum(c['completeActorFields']for c in cases)==20512 and
      sum(c['nativeFullRAMRGBFields']for c in cases)==333,
      'Exactly18 actual current cases,14new cold boots,all20512actor fields/333RGB checkpoints accounted')
    # Raw reaction pose/group/picture descriptors are byte-identical original
    # MK2 ROM data, not patched/imported stand-ins or guessed stream metadata.
    stock=(ROOT/'mk2/mk2-maincpu.bin').read_bytes();raw_bindings=[]
    for pose in sorted(raw_stock_poses):
        off=(pose-0xff800000)//8;count=0
        need(0<=off<len(guest)-4,'Original raw reaction pose inside native ROM')
        while count<12:
            ptr=struct.unpack_from('<I',guest,off+count*4)[0]
            if not ptr:break
            data=(ptr-0xff800000)//8
            need(0<=data<len(guest)-14 and guest[data:data+14]==stock[data:data+14],
              'Every entire raw reaction component descriptor is original MK2, including native stock source/shape/flips')
            count+=1
        need(0<count<12 and guest[off:off+(count+1)*4]==stock[off:off+(count+1)*4],
          'Complete terminated raw reaction pose group exactly original MK2')
        raw_bindings.append(dict(nativePose=f'{pose:08X}',wholeOriginalParts=count))
    need(raw_bindings,'Actual original raw reaction descriptor provenance required')
    # Preserve/reproduce both real historical checker limitations without
    # interpreting unsupported data as success, hiding it, or changing game data.
    oldcheck,oldload,_=failed_air.bindings()
    try:oldcheck(oldload('square',1),guest,payload)
    except ValueError as error:
        need(str(error)=='Exact actual native pre-clip instruction/cache provenance','Exact failed old finite-view adapter')
        air_failure=str(error)
    else:raise ValueError('Original actual finite-view failure not reproduced')
    old=ground.bindings();scope=old.__globals__;model_gfx=scope['reconstruct'](pins)
    try:scope['check'](scope['load']('leg',1),guest,payload,model_gfx)
    except ValueError as error:
        need(str(error)=='Only exact original Kitana11x6 raw hand; no compressed or imported raw acceptance',
          'Exact original unsupported raw reaction guard remains immutable')
        raw_failure=str(error)
    else:raise ValueError('Original actual stock raw reaction failure not reproduced')
    qualified=ROOT/'audit_v5316_original_stock_raw_shadow_scanner_source_checked/report.json'
    proof=json.loads(qualified.read_text())
    need(proof['passed']and proof['sourceOnly']and proof['originalUnconditionalHeaderAndSignedWidthAdvanceQualified']and
      all(sha(p)==h for p,h in proof['inputHashes'].items()),
      'Actual native disassembly/whole original ROM/signed scanner qualifier unchanged')
    pins[str(qualified)]=sha(qualified)
    # Four explicitly named earlier source pins must exist; no vacuous filtered
    # legacy source qualification or reinterpretation of body-DMA raw decoding.
    prior_source=json.loads((ROOT/'audit_v2699_current_friendship_shadow_stock_comparison_checked/report.json').read_text())
    for rel in ('mame-mkp/unidasm.exe','mk2/mk2-maincpu.bin',
      'tools/verify_current_friendship_shadow_inventory_v2696.py','tools/compare_current_friendship_shadow_stock_v2698.py'):
        p=(ROOT/rel).resolve();need(str(p)in prior_source['inputHashes']and sha(p)==prior_source['inputHashes'][str(p)],
          'All four original signed scanner qualifier inputs explicitly present and byte-exact')
        pins[str(p)]=sha(p)
    files=('run_current_air_square_shadow_v5306.py','verify_current_air_square_repeat_v5309.py',
      'verify_current_air_square_repeat_v5311.py','verify_current_air_square_shadow_v5313.py',
      'native_stock_raw_shadow_scanner_v5315.py','verify_current_stock_raw_reaction_shadow_v5317.py',
      'verify_current_subzero_full_repeat_matrix_v5319.py')
    for name in files:p=ROOT/'tools'/name;pins[str(p)]=sha(p)
    command='@(Get-CimInstance Win32_Process | Where-Object { $_.ProcessId -in @('+','.join(map(str,native_ids))+') } | Select-Object ProcessId,Name,CommandLine) | ConvertTo-Json -Compress'
    census=subprocess.run(['powershell.exe','-NoProfile','-Command',command],capture_output=True,text=True)
    need(census.returncode==0,'Actual specific captured native process census')
    live=json.loads(census.stdout)if census.stdout.strip()else[]
    if isinstance(live,dict):live=[live]
    need(not any(p['Name']=='mkport_candidate.exe'and p.get('CommandLine')and
      ('audit_v5300_current_special_shadow_'in p['CommandLine']or'audit_v5307_current_air_square_shadow_'in p['CommandLine'])for p in live),
      'Every recorded native case actually terminal, never inferred from timeout or PID alone')
    kernel=ctypes.WinDLL('kernel32',use_last_error=True);allocated=kernel.GetCompressedFileSizeW
    allocated.argtypes=[wintypes.LPCWSTR,ctypes.POINTER(wintypes.DWORD)];allocated.restype=wintypes.DWORD
    disk=logical=0
    for p in set(evidence):
        hi=wintypes.DWORD();ctypes.set_last_error(0);lo=allocated(str(p),ctypes.byref(hi))
        need(lo!=0xffffffff or ctypes.get_last_error()==0,'Actual compressed trace allocation')
        disk+=lo+(hi.value<<32);logical+=p.stat().st_size
    need(all(sha(p)==h for p,h in pins.items()),'Final full actual native/counterexample/model/descriptor source evidence stable')
    report=dict(schema=1,observedUTC=datetime.datetime.now(datetime.timezone.utc).isoformat(),
      parentAdditiveJournal=str(PARENT),goalStatus='active',remaining=parent['remaining'],
      previousGoalTurnClassification='progress: current four actual projectile shadow roles plus complete native Sonya P1 ending/300attract pixels/pages/hardware accepted; full original scope intact',
      thisGoalTurnClassification='progress:14new cold physical current-candidate cases extend to all8moves/both human slots against real selected Sub-Zero8, plus both actual airborne-square contacts. Entire full physical matrix and220real faults accepted. Every ready-field full owned body and original native shadow projection/source/row/pen/cadence checked in all18contexts;210actual body/shadow faults rejected. Original Sub-Zero48-high raw reaction support derived from actual unchanged original ROM/disassembly unconditional signed header scanner, all its intermediate/tail rows and6additional real raw faults perrole checked; true stock pose/whole component descriptors equal original MK2. Both real failed checker sources preserved/reproduced. No game edits/proxies/forced state/timeout acceptance/raw media/new build or release promotion.',
      mergeRule='Additive finite Prison/Sub-Zero matrix only. Inherited old Kitana scope strings in historical checker reports are not actual victim selection. All five original unfinished groups remain verbatim.',
      currentActualCases=cases,newNativeColdBootsThisTurn=14,totalCurrentSubzeroColdBootCases=18,
      actualPhysicalSpecialCycles=36,actualContiguousActorFields=20512,actualFullRAMRGBFields=333,
      actualNativeSourceBoundShadowCopies=sum(c['nativeShadowCopies']for c in cases),
      actualAddedFighterSourceBoundShadowCopies=sum(c['ownAddedFighterShadowCopies']for c in cases),
      actualFullOwnedBodyParts=sum(c['fullOwnedBodyParts']for c in cases),
      actualBodyShadowFaultsRejected=sum(c['actualShadowSemanticFaultsRejected']for c in cases),
      actualFullPhysicalFaultsRejected=220,actualAirborneSquareContacts=4,
      rawOriginalReactionGroups=raw_bindings,
      preservedFailures=[dict(source=str(Path(failed_air.__file__)),error=air_failure,
        cause='Standalone physical gate was given full every-field publication data; fresh5311 uses the exact old finite sampled view while full5313 independently checks every unfiltered entry/body/shadow row.'),
        dict(source=str(Path(ground.__file__)),error=raw_failure,
        cause='Old Kitana11x6-only raw guard does not describe stock Sub-Zero10x48 reaction. Fresh5317 keeps imported streams compressed and admits only this exact stock raw reaction with independent original signed scanner and all actual DMA rows.')],
      rawMediaROMVRAMAudioFilesWritten=0,newBuilds=0,newDeletedFiles=0,publicPlayableChanged=False,
      refreshedReleaseZIP=False,fullPortAcceptance=False,allArenaCPUOrKOOverlapArtAudioAccepted=False,
      currentNewTraceLogicalBytes=logical,currentNewTraceAllocatedBytes=disk,
      cleanupAccounting='Only compact compressed logs/row proofs/JSON evidence for14new actual contexts; guest/GFX/RGB buffers remain RAM-only. Existing5219executable reused, no copied binary/payload/build tree. Prior reclaimed disk space not recounted.',
      newInputHashes=pins,
      nextAction='Move beyond Prison/Sub-Zero repeat matrix to naturally reached other arenas, real CPU/blocked/KO/overlap/victim/mirror contexts and full effect/voice audio; original stock18-high raw ice-hand shadow remains a distinct historical unqualified context (new whitelist only48-high reaction). Continue all Pit/Tomb branches and other finishers/morphs/secrets/cinematics/independent stock transition choreography, then final combined selection/ladder/names/audio and release regression. All original groups remain active; no completion/block claim.')
    need(report['actualBodyShadowFaultsRejected']==210,'All198original full-shadow faults plus12actual raw-specific faults')
    OUT.mkdir();need(subprocess.run(['compact.exe','/C','/I','/Q','/S:'+str(OUT)],capture_output=True).returncode==0,'Compress compact additive evidence')
    (OUT/'progress.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:report[k]for k in ('goalStatus','newNativeColdBootsThisTurn','actualPhysicalSpecialCycles',
      'actualContiguousActorFields','actualFullRAMRGBFields','actualNativeSourceBoundShadowCopies',
      'actualBodyShadowFaultsRejected','actualFullPhysicalFaultsRejected','currentNewTraceAllocatedBytes','fullPortAcceptance')},indent=2),flush=True)
if __name__=='__main__':main()
