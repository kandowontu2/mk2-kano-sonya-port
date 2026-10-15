$ErrorActionPreference='Stop'
$portRoot=Split-Path $PSScriptRoot -Parent
$candidate=Join-Path $portRoot 'diagnostic_v48_ground_alignment_candidate'
$build=Get-Content -LiteralPath (Join-Path $candidate 'build-info.json') -Raw | ConvertFrom-Json
$exe=Join-Path $candidate 'mkport_candidate.exe'
$payload=Join-Path $portRoot 'diagnostic_v46_bicycle_assets\roms\mk2ks\mk2ks.mdata'
if((Get-FileHash -LiteralPath $exe).Hash -ne $build.executable_sha256 -or
   (Get-FileHash -LiteralPath $payload).Hash -ne $build.payload_sha256){throw 'Candidate executable/payload changed'}
foreach($input in $build.input_hashes.PSObject.Properties){
    if((Get-FileHash -LiteralPath $input.Name).Hash -ne $input.Value){throw "Build input changed: $($input.Name)"}
}
$families=[ordered]@{
    ground=@('regression_v48_ground_verified_side*')
    core=@('regression_v48_ground_core_*')
    choke=@('regression_v48_ground_choke_*')
    leg=@('regression_v48_ground_leg_*')
    bicycle_contact=@('regression_v48_feedback_contacts_*')
    bicycle_rounds=@('regression_v48_feedback_rounds_*')
    bicycle_interrupt=@('regression_v48_feedback_interrupt_*')
}
$requiredCounts=@{ground=6;core=12;choke=4;leg=12;bicycle_contact=16;bicycle_rounds=8;bicycle_interrupt=4}
$evidence=@()
foreach($family in $families.Keys){
    $dirs=@(Get-ChildItem -LiteralPath $portRoot -Directory -Filter $families[$family][0])
    if($dirs.Count -ne $requiredCounts[$family]){throw "Missing $family runtime cases: $($dirs.Count)"}
    foreach($dir in $dirs){
        $resultPath=Join-Path $dir.FullName 'result.json'
        $logPath=Join-Path $dir.FullName 'run.log'
        $result=Get-Content -LiteralPath $resultPath -Raw | ConvertFrom-Json
        $log=Get-Content -LiteralPath $logPath -Raw
        if($result.case -ne $dir.Name -or -not $result.passed -or $result.exit_code -ne 0 -or
           $result.executable_sha256 -ne $build.executable_sha256 -or
           $result.payload_sha256 -ne $build.payload_sha256 -or
           $log -match '(?i)fatal error|exception at|access violation|error in emu|\[LUA ERROR\]'){
            throw "Invalid $family result: $($dir.Name)"
        }
        foreach($file in $result.file_hashes.PSObject.Properties){
            if((Get-FileHash -LiteralPath $file.Name).Hash -ne $file.Value){throw "Case input changed: $($file.Name)"}
        }
        $marker=switch($family){
            ground {'MK2KS_GROUND_RESULT pass=true '}
            core {if($dir.Name -match '_grid$'){'MK2KS_GRID_RESULT pass=true '}elseif($dir.Name -match '_navigation$'){'MK2KS_NAV_RESULT pass=true '}elseif($dir.Name -match '_basics_'){'MK2KS_BASIC_RESULT pass=true '}else{'MK2KS_EXIT_RESULT pass=true '}}
            choke {'MK2KS_CHOKE_RESULT pass=true '}
            leg {'MK2KS_LEG_RESULT pass=true '}
            bicycle_contact {'MK2KS_BICYCLE_FEEDBACK_RESULT pass=true '}
            bicycle_rounds {'MK2KS_BICYCLE_FEEDBACK_RESULT pass=true '}
            bicycle_interrupt {'MK2KS_BICYCLE_FEEDBACK_RESULT pass=true '}
        }
        $stability=if($family -eq 'core' -and $dir.Name -match '_(grid|navigation)$'){$true}
            elseif($family -eq 'core' -and $dir.Name -match '_basics_'){$log.Contains('stalled_frames=0 trap_frames=0')}
            else{$log.Contains('MK2KS_STABILITY stalled_frames=0 trap_frames=0')}
        if(-not $log.Contains($marker) -or -not $stability){
            throw "Missing gameplay/stability marker in $($dir.Name)"
        }
        $evidence+= [ordered]@{family=$family;case=$dir.Name;log_sha256=(Get-FileHash -LiteralPath $logPath).Hash;
            result_sha256=(Get-FileHash -LiteralPath $resultPath).Hash}
    }
}
$assetLog=Join-Path $candidate 'asset-tests-with-payload.log'
$assets=Get-Content -LiteralPath $assetLog -Raw
if($assets -notmatch 'Ran 45 tests' -or $assets -notmatch '(?m)^OK\s*$' -or $assets -match 'FAILED|skipped='){
    throw 'Complete asset suite not proven'
}
$launcher=Join-Path $candidate 'PLAY_CANDIDATE.cmd'
$launchResult=Get-Content -LiteralPath (Join-Path $portRoot 'regression_v48_candidate_cmd\result.json') -Raw | ConvertFrom-Json
$launchLog=Get-Content -LiteralPath (Join-Path $portRoot 'regression_v48_candidate_cmd\run.log') -Raw
$launcherAudit=Get-Content -LiteralPath (Join-Path $candidate 'launcher-audit.log') -Raw
if(-not $launchResult.passed -or $launchResult.exit_code -ne 0 -or
   $launchResult.candidate_sha256 -ne $build.executable_sha256 -or
   $launchResult.payload_sha256 -ne $build.payload_sha256 -or
   $launchResult.launcher_sha256 -ne (Get-FileHash -LiteralPath $launcher).Hash -or
   $launchResult.log_sha256 -ne (Get-FileHash -LiteralPath (Join-Path $portRoot 'regression_v48_candidate_cmd\run.log')).Hash -or
   -not $launchLog.Contains('MK2KS_EXIT_RESULT pass=true ') -or
   -not $launcherAudit.Contains('1 romsets found, 1 were OK.')){throw 'Candidate CMD launch not proven'}
if((Get-FileHash -LiteralPath (Join-Path $portRoot 'mame-mkp\mkport.exe')).Hash -ne
    '413855890FCE3BECAC9B24E11699FAD1CE465ACCBE4B27A93F2DD5819D13A891'){
    throw 'Installed executable changed'
}
$manifest=Join-Path $candidate 'verification.json'
if(Test-Path -LiteralPath $manifest){throw 'Refusing to overwrite a prior verification manifest'}
[ordered]@{candidate='v48 grounding and bicycle feedback';build=$build;runtime_cases=$evidence.Count+1;
    runtime_families=$requiredCounts;cases=$evidence;cmd_case='regression_v48_candidate_cmd';asset_tests=45;
    asset_log_sha256=(Get-FileHash -LiteralPath $assetLog).Hash;
    launcher_sha256=(Get-FileHash -LiteralPath $launcher).Hash;
    launcher_audit_sha256=(Get-FileHash -LiteralPath (Join-Path $candidate 'launcher-audit.log')).Hash;
    installed_executable_unchanged=$true;
    scope='Verified grounding, core roster, existing grab moves, bicycle impact/camera feedback, repeated rounds, interruption, and candidate CMD. The full port remains unfinished.'} |
    ConvertTo-Json -Depth 7 | Out-File -LiteralPath $manifest -Encoding utf8
Write-Output "Verified $($evidence.Count+1) current-candidate runtime cases and 45 asset tests."
