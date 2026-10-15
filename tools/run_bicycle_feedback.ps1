param(
    [Parameter(Mandatory=$true)][string]$CasePrefix,
    [Parameter(Mandatory=$true)][string]$Executable,
    [Parameter(Mandatory=$true)][string]$PayloadRomDirectory,
    [ValidateSet(1,2)][int[]]$Sides=@(1,2),
    [ValidateSet('kano','sonya','kung_lao','liu_kang','cage','baraka','kitana','mileena','shang_tsung','raiden','sub_zero','reptile','scorpion','jax')][string[]]$Victims=@('kano','sonya'),
    [ValidateSet('single','rounds','interrupt')][string[]]$Drivers=@('single'),
    [ValidateSet('near','air','held','block','duck','duck_block','far','reversed','expired','wrong_button','airborne','with_block')][string[]]$Modes=@('near')
)
$ErrorActionPreference='Stop'
$portRoot=Split-Path $PSScriptRoot -Parent
if ($CasePrefix -notmatch '^[a-zA-Z0-9_-]+$') {throw 'Use a simple evidence prefix'}
if ($Drivers -contains 'rounds' -and @($Victims | Where-Object {$_ -notin 'kano','sonya','kitana','sub_zero'}).Count) {throw 'Round driver supports Kano, Sonya, Kitana and Sub-Zero'}
if ($Drivers -contains 'interrupt' -and @($Victims | Where-Object {$_ -notin 'kano','sonya'}).Count) {throw 'Counter driver supports Kano and Sonya'}
$Executable=(Resolve-Path -LiteralPath $Executable).Path
$PayloadRomDirectory=(Resolve-Path -LiteralPath $PayloadRomDirectory).Path
$harness=Join-Path $portRoot 'mk2ks_bicycle_feedback_test.lua'
$romPath="$PayloadRomDirectory;$portRoot\roms_v22_clean;$portRoot\roms"
$tracked=@($Executable,(Join-Path $PayloadRomDirectory 'mk2ks\mk2ks.mdata'),$harness,$PSCommandPath)
foreach($script in 'mk2ks_selector_exit_test.lua','mk2ks_bicycle_test.lua','mk2ks_bicycle_lifecycle_test.lua','mk2ks_bicycle_interrupt_test.lua') {
    $tracked+=Join-Path $portRoot $script
}
$hashes=@{}
foreach($file in $tracked) {$hashes[$file]=(Get-FileHash -LiteralPath $file).Hash}
function Assert-Unchanged {
    foreach($file in $tracked) {if((Get-FileHash -LiteralPath $file).Hash -ne $hashes[$file]) {throw "Input changed: $file"}}
}
& $Executable mk2ks -rompath $romPath -verifyroms
if($LASTEXITCODE -ne 0) {throw 'Selected ROM audit failed'}
$saved=@{}
Get-ChildItem Env: | Where-Object Name -Like 'MK2KS_*' | ForEach-Object {$saved[$_.Name]=$_.Value}
$failed=@()
Push-Location $portRoot
try {
    foreach($driver in $Drivers) {
      $driverModes=if($driver -eq 'single') {$Modes} else {@('near')}
      foreach($side in $Sides) {foreach($victim in $Victims) {foreach($mode in $driverModes) {
        Assert-Unchanged
        Get-ChildItem Env: | Where-Object Name -Like 'MK2KS_*' | Remove-Item
        $env:MK2KS_TEST_FIGHTER=if($side -eq 1) {'sonya'} else {$victim}
        $env:MK2KS_P2_FIGHTER=if($side -eq 1) {$victim} else {'sonya'}
        $env:MK2KS_BICYCLE_SIDE="$side";$env:MK2KS_BICYCLE_MODE=$mode;$env:MK2KS_BICYCLE_FEEDBACK_DRIVER=$driver
        $env:MK2KS_TEST_CONFIRM='hp';$env:MK2KS_TEST_CONFIRM_HOLD='8';$env:MK2KS_TWO_PLAYER='1'
        $env:MK2KS_ASSERT_NATIVE_DISPLAY='1';$env:MK2KS_ASSERT_HUD_SHADOW='1'
        $env:MK2KS_PIN_FIGHTERS='0';$env:MK2KS_PROBE_NATIVE_ROSTER='0'
        $case="${CasePrefix}_${driver}_side${side}_${victim}_${mode}"
        $out=Join-Path $portRoot $case
        if(Test-Path -LiteralPath $out) {throw 'Refusing to overwrite evidence'}
        New-Item -ItemType Directory -Path $out | Out-Null
        $seconds=if($driver -eq 'rounds') {120} elseif($driver -eq 'interrupt') {65} else {60}
        & $Executable mk2ks -rompath $romPath -artpath "$portRoot\artwork" -skip_gameinfo -video none -sound none -nothrottle `
            -str $seconds -snapsize 400x300 -cfg_directory "$out\cfg" -nvram_directory "$out\nvram" -snapshot_directory "$out\snap" `
            -autoboot_script $harness 2>&1 | Out-File -LiteralPath "$out\run.log" -Encoding utf8
        $exitCode=$LASTEXITCODE
        Assert-Unchanged
        $log=Get-Content -LiteralPath "$out\run.log" -Raw
        $baseMarker=switch($driver) {single {'MK2KS_BICYCLE_RESULT pass=true '} rounds {'MK2KS_BICYCLE_LIFECYCLE_RESULT pass=true '} interrupt {'MK2KS_BICYCLE_INTERRUPT_RESULT pass=true '}}
        $passed=$exitCode -eq 0 -and $log -notmatch '(?i)fatal error|exception at|access violation|error in emu|\[LUA ERROR\]'
        foreach($marker in @($baseMarker,'MK2KS_BICYCLE_FEEDBACK_RESULT pass=true ','MK2KS_EXIT_RESULT pass=true ',
            'MK2KS_DISPLAY_RESULT pass=true ','MK2KS_HUD_SHADOW_RESULT pass=true ','MK2KS_STABILITY stalled_frames=0 trap_frames=0')) {
            $passed=$passed -and $log.Contains($marker)
        }
        [ordered]@{case=$case;passed=$passed;driver=$driver;side=$side;victim=$victim;mode=$mode;exit_code=$exitCode;
            executable_sha256=$hashes[$Executable];payload_sha256=$hashes[$tracked[1]];file_hashes=$hashes} |
            ConvertTo-Json -Depth 4 | Out-File -LiteralPath "$out\result.json" -Encoding utf8
        Write-Output "$case pass=$passed"
        if(-not $passed) {$failed+=$case}
      }}}
    }
} finally {
    Pop-Location
    Get-ChildItem Env: | Where-Object Name -Like 'MK2KS_*' | Remove-Item
    foreach($key in $saved.Keys) {Set-Item -LiteralPath "Env:$key" -Value $saved[$key]}
}
if($failed.Count) {throw "Failed bicycle feedback cases: $($failed -join ', ')"}
