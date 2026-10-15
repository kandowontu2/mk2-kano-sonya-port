"""Full-scope checkpoint after owned victim data/native-state fix; goal active."""
import json,subprocess
from pathlib import Path
import run_native_sound_delivery_ram_v3682 as current
ROOT,need,sha=current.ROOT,current.need,current.sha
PARENT=ROOT/'audit_v3798_mileena_cache_full_scope_checkpoint/checkpoint.json'
OUT=ROOT/'audit_v3847_native_mileena_fix_full_scope_checkpoint'
def main():
    need(not OUT.exists(),'Immutable fresh full-scope checkpoint')
    state=json.loads(PARENT.read_text());remaining=list(state['remaining']);pins={}
    need(len(remaining)==5 and state['goalStatus']=='active'and not state['fullPortAcceptance']and not state['finishedRelease'],'Original full natural-character objective remains open')
    def pin(path,wanted=None):
        path=Path(path).resolve();key=str(path);digest=sha(path)
        need(wanted is None or digest==wanted,'Executed evidence unchanged '+key)
        need(key not in pins or pins[key]==digest,'Consistent fresh pin')
        need(key not in state['inputHashes']or state['inputHashes'][key]==digest,'Do not relabel inherited evidence')
        pins[key]=digest
    accepted_path=ROOT/'audit_v3843_mileena_identity_runtime_checked/report.json';accepted=json.loads(accepted_path.read_text());pin(accepted_path)
    need(accepted['passed']and accepted['actualContexts']==4 and accepted['actualRowFaultsRejected']==52 and accepted['wholeGuestAccepted']and accepted['nativeVictimStreamsAndCleanupAccepted'],'All true-ID native contexts independently qualified')
    need(not accepted['artPixelsShadowsOrAudioAccepted']and not accepted['fullCampaignStabilityAccepted']and not accepted['fullPortAcceptance'],'No pixel/audio/campaign/full-port promotion')
    for path,h in accepted['inputHashes'].items():pin(path,h)
    for name in ('audit_v3820_native_mileena_victim_data_checked','audit_v3834_native_mileena_rom_identity_checked','audit_v3845_mileena_candidate_compression'):
        report_path=ROOT/name/'report.json';report=json.loads(report_path.read_text());pin(report_path);need(report['passed'],'Source/data/loader/storage positive')
        for path,h in report['inputHashes'].items():pin(path,h)
    storage=json.loads((ROOT/'audit_v3845_mileena_candidate_compression/report.json').read_text())
    need(storage['deletedFiles']==0 and len(storage['captureChildrenMissing'])==8,'Lossless evidence and every capture stopped')
    leaves=('art_reference_mileena_v3801','art_native_mileena_v3810','asset_v3812_native_mileena_victims','source_v3814_native_mileena_victims','source_v3832_native_mileena_rom_identity','diagnostic_v3822_native_mileena_victims','diagnostic_v3836_native_mileena_rom_identity','audit_v3828_mileena_fixed_matrix_observed','audit_v3839_mileena_identity_matrix_observed')
    for leaf in leaves:
        for path in (ROOT/leaf).rglob('*'):
            if path.is_file():pin(path)
    for name in ('kano','sonya'):
        for side in (1,2):
            for prefix,suffix in (('audit_v3827','fixed'),('audit_v3838','rom_identity')):
                folder=ROOT/f'{prefix}_mileena_{name}_p{side}_{suffix}'
                need(not list(folder.rglob('*.png'))and not list(folder.rglob('*.wav')),'Actual runtime captures have no raster or PCM files')
                for path in folder.rglob('*'):
                    if path.is_file():pin(path)
    for file in ('tools/prepare_mileena_victim_references_v3800.py','tools/mileena_victim_art_prompts_v3802.json','tools/mileena_victim_sonya_prompt_v3805.json','tools/mileena_victim_selected_prompts_v3809.json','tools/build_native_mileena_victim_art_v3811.py','tools/verify_native_mileena_victim_data_v3815.py','tools/verify_native_mileena_victim_data_v3819.py','tools/build_native_mileena_victims_v3821.ps1','mk2ks_cache_provenance_mileena_fixed_v3823.lua','mk2ks_mileena_earned_fixed_v3824.lua','mk2ks_mileena_fixed_guest_v3825.lua','tools/run_mileena_fixed_matrix_v3826.py','tools/verify_mileena_fixed_runtime_v3829.py','tools/verify_native_mileena_rom_identity_v3833.py','tools/build_native_mileena_identity_v3835.ps1','tools/run_mileena_identity_matrix_v3837.py','tools/verify_mileena_identity_runtime_v3840.py','tools/verify_mileena_identity_runtime_v3842.py','tools/compact_mileena_candidate_evidence_v3844.py','tools/save_native_mileena_fix_checkpoint_v3846.py'):pin(ROOT/file)
    public={
      'diagnostic_v1836_ball_register_boundary/mkport_candidate.exe':'34D427A8FB152E89F4B5FDA5CCE7A8BDB2CC3020CD66C42979B53ED1BA15263E',
      'diagnostic_v1836_ball_register_boundary/roms/mk2ks/mk2ks.mdata':'5646E839C73C4DB89BCF7CC87ECADBDA94B1E0D30EB1C0D2ED50A21A5524E23D',
      'release_v1863_current_playtest/MK2_Kano_Sonya_v1836_CURRENT_PLAYTEST.zip':'994AC5535CD65EA92B7BCD19E12EC6669F4527796CD0CA8C7CA28E708A6897EA',
      'mame-mkp/mkport.exe':'413855890FCE3BECAC9B24E11699FAD1CE465ACCBE4B27A93F2DD5819D13A891',
      'mame-mkp/src/mame/midway/midtunit_m.cpp':'EE48F2FBD72749354A44F3B6574D00EB5DD879EC368A73FBDD57540A4F351D34',
      'mame-mkp/src/mame/midway/midtunit.cpp':'07C1FA27AAA0B1C836E462BC6EC13D62DFF405FA2B7F1358D7BB34B51731DA85',
      'mame-mkp/src/mame/midway/midtunit.h':'256577139683DE7226D3EC0966CAC9B44C9C01C96ED561D236112B2DBADC7644'}
    for path,h in public.items():pin(ROOT/path,h)
    pin(ROOT/state['currentCMD']);pin(PARENT)
    check=subprocess.run(['powershell.exe','-NoProfile','-Command','Get-CimInstance Win32_Process | Where-Object { $_.Name -match "mkport_candidate|gmake|cc1plus" } | Select-Object -ExpandProperty ProcessId'],capture_output=True,text=True)
    need(check.returncode==0 and not check.stdout.strip(),'No active candidate/compiler handles now')
    state['inputHashes']=pins
    state.update(inputHashInheritance=dict(schema=1,parentCheckpoint=str(PARENT),parentCheckpointSHA256=pins[str(PARENT)],mergeRule='Resolve parent recursively; preserve retired/deleted exclusions and agree on shared fresh pins; do not flatten.'),previousCheckpoint=str(PARENT),
      previousGoalTurnClassification='no progress: preceding acknowledgment-only response. Revalidated actual files and resumed the next safe implementation action.',
      thisGoalTurnClassification='progress: original swallowing grammar decoded, generated own-costume art with built-in image_gen, uniformly encoded15poses into free payload/graphics/program storage. Added source initialization loader extends only true17/18 native lookup rows; native copier/actions/cadence/IDs unchanged. Independent whole-source/payload proof rejects13data faults. Built3822 and reproduced native fixed path4contexts; original strict3829gate honestly rejected old ROM CRC warning. Corrected only actual payload CRC/SHA1 declaration, built3836, reran4earned physical contexts with correct ROM identity. First3840stategate revealed an unmodified pre-action lifebar FFFF init pair; exact original ROM routine and byte-identical old health prefix prove it, fresh3842permits only that exact same-field paired restoration before action and rejects52actual-row faults.3843wholeguest/native true-ID lookup/all15four-field poses/native disappearance/retirement/postmatch state accepted, NOT pixels/shadows/audio/campaign/fullport. Both builds and failed sources retained; compressed stopped logs/candidates, public1836 and installed/dirty working files unchanged. All five remaining groups stay open.',
      currentDevelopmentCandidate='diagnostic_v3836_native_mileena_rom_identity',
      currentDevelopmentExecutableSHA256='36B306F6A9241C1C977A7B0B1CFAC65884F4ED97963A60A1967138E000E7E982',
      currentDevelopmentPayloadSHA256='91F580279F1FC262E6CFE3CBC578FDCF7DC4AC3393B1055156D5FBEBC8998B24',
      currentDevelopmentGuestSHA256='938D380B3E2CE8DF6A688E2DC64C576CC7A1E554AE341E7B42463129FA5CA821',
      currentDevelopmentNativeMileenaVictimStateAccepted=True,currentDevelopmentNativeMileenaReport=str(accepted_path),currentDevelopmentActualNativeContexts=4,currentDevelopmentActualRowFaultsRejected=52,
      currentDevelopmentMileenaRasterArtShadowAudioAccepted=False,currentDevelopmentCampaignRegressionAccepted=False,currentDevelopmentWholePortRegressionAccepted=False,
      missingMileenaOwnedArtworkGeneratedWith='built-in image_gen, selected PNGs persisted in art_native_mileena_v3810; prompts tools/mileena_victim_selected_prompts_v3809.json',
      preservedCurrentTurnFailures={'3815':'incorrect native palette count64; actual native65 header includes transparent slot, independently corrected3819.', '3829':'Strict actual runtime gate rejects3822 WRONG CHECKSUMS. Correct ROM identity source3832/built3836; no suppression.', '3840':'Original pre-action round2 lifebar sentinel161->FFFF->4 rejected by generic all-fields health range. Exact original FF9DEC90..FF9DEF70 and old/current health-prefix equality justify only paired original initialization in3842. No collision/fatality/cache corruption exception.'},
      currentTurnReclaimedAllocatedBytes=storage['reclaimedAllocatedBytes'],currentTurnDeletedFiles=0,currentTurnNewBuilds=2,currentTurnActualCaptureRasterFiles=0,currentTurnActualCaptureAudioFiles=0,
      pendingNativeMileenaCapture=None,pendingNativeMileenaBuild=None,pendingNativeMileenaQualifier=None,
      nextImplementationAction='Verify actual3836 swallowing frames/position/native victim shadow/erase/audio in RAM in both slots; rerun unchanged long SonyaP2campaign past original223502Mileena cache failure and qualify whole native state. Then continue all five groups, not only this short fix.',
      fullPortAcceptance=False,finishedRelease=False,goalStatus='active')
    need(state['remaining']==remaining and state['currentCandidate']=='diagnostic_v1836_ball_register_boundary','Entire original scope/public launcher preserved')
    OUT.mkdir();need(subprocess.run(['compact.exe','/C','/I','/Q','/S:'+str(OUT)],capture_output=True).returncode==0,'Checkpoint compression')
    (OUT/'checkpoint.json').write_text(json.dumps(state,indent=2)+'\n');print(json.dumps(dict(checkpoint=str(OUT/'checkpoint.json'),freshPins=len(pins),goalStatus='active',nativeContextsAccepted=4,wholePortAccepted=False)))
if __name__=='__main__':main()
