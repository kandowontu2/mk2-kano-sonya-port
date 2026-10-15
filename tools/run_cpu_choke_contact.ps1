param(
    [Parameter(Mandatory=$true)][string]$CaseName,
    [Parameter(Mandatory=$true)][string]$Executable,
    [Parameter(Mandatory=$true)][string]$PayloadRomDirectory,
    [ValidateSet('kano','sonya')][string]$PlayerFighter='sonya',
    [ValidateRange(1,16)][int]$LadderIndex=7,
    [ValidateRange(30,300)][int]$Seconds=100,
    [switch]$Approach
)
$ErrorActionPreference='Stop'
if($CaseName -notmatch '^[a-zA-Z0-9_-]+$'){throw 'Use a simple evidence name.'}
$root=Split-Path $PSScriptRoot -Parent
$Executable=(Resolve-Path -LiteralPath $Executable).Path
$PayloadRomDirectory=(Resolve-Path -LiteralPath $PayloadRomDirectory).Path
$out=Join-Path $root $CaseName
if(Test-Path -LiteralPath $out){throw "Refusing to overwrite evidence: $out"}
$harness=Join-Path $root 'mk2ks_cpu_choke_contact_probe.lua'
$tracked=@($Executable,(Join-Path $PayloadRomDirectory 'mk2ks\mk2ks.mdata'),
    $harness,(Join-Path $root 'mk2ks_cpu_ladder_trace.lua'),
    (Join-Path $root 'mk2ks_selector_exit_test.lua'),$PSCommandPath)
$hashes=@{}
foreach($file in $tracked){$hashes[$file]=(Get-FileHash -LiteralPath $file).Hash}
& $Executable mk2ks -rompath "$PayloadRomDirectory;$root\roms" -verifyroms
if($LASTEXITCODE -ne 0){throw 'ROM verification failed.'}
New-Item -ItemType Directory -Path $out | Out-Null
$saved=@{}
Get-ChildItem Env: | Where-Object Name -Like 'MK2KS_*' | ForEach-Object {$saved[$_.Name]=$_.Value}
Push-Location $root
try {
    Get-ChildItem Env: | Where-Object Name -Like 'MK2KS_*' | Remove-Item
    $env:MK2KS_TEST_FIGHTER=$PlayerFighter
    $env:MK2KS_P2_FIGHTER='stock'
    $env:MK2KS_TEST_CONFIRM='hp'
    $env:MK2KS_TEST_CONFIRM_HOLD='8'
    $env:MK2KS_TWO_PLAYER='0'
    $env:MK2KS_ALLOW_NATURAL_LOSS='1'
    $env:MK2KS_DIAGNOSTIC_LADDER_INDEX="$LadderIndex"
    $env:MK2KS_TRACE_AI_VARIETY='1'
    if($Approach){$env:MK2KS_CPU_CHOKE_APPROACH='1'}
    $env:MK2KS_ASSERT_NATIVE_DISPLAY='1'
    $env:MK2KS_ASSERT_HUD_SHADOW='1'
    & $Executable mk2ks -rompath "$PayloadRomDirectory;$root\roms_v22_clean;$root\roms" `
        -artpath "$root\artwork" -skip_gameinfo -video none -sound none -nothrottle `
        -str $Seconds -snapsize 400x300 -cfg_directory "$out\cfg" `
        -nvram_directory "$out\nvram" -snapshot_directory "$out\snap" `
        -autoboot_script $harness 2>&1 | Out-File -LiteralPath "$out\run.log" -Encoding utf8
    $exitCode=$LASTEXITCODE
    foreach($file in $tracked){
        if((Get-FileHash -LiteralPath $file).Hash -ne $hashes[$file]){throw "Input changed: $file"}
    }
    $log=Get-Content -LiteralPath "$out\run.log" -Raw
    $summary=($log -split "`n" | Where-Object {$_ -match '^MK2KS_CPU_CHOKE_CONTACT_RESULT '}) | Select-Object -Last 1
    $passed=$exitCode -eq 0 -and
        $summary -match 'pass=true pulses=4 releases=1 damage=32 recovered=(true defeated=false|false defeated=true)' -and
        $log -match 'MK2KS_EXIT_RESULT pass=true ' -and
        $log -match 'MK2KS_STABILITY stalled_frames=0 trap_frames=0' -and
        $log -match 'MK2KS_DISPLAY_RESULT pass=true ' -and
        $log -match 'MK2KS_HUD_SHADOW_RESULT pass=true ' -and
        $log -match 'MK2KS_CPU_DIAGNOSTIC_RESULT requested=nil injected=false' -and
        $log -match "MK2KS_CPU_DIAGNOSTIC_LADDER_RESULT requested=$LadderIndex injected=true" -and
        $log -match 'MK2KS_CPU_DIAGNOSTIC_HEALTH_RESULT requested=nil all_stages=false writes=0' -and
        $log -match 'MK2KS_CPU_DIAGNOSTIC_P1_REGEN_RESULT enabled=false writes=0' -and
        $log -notmatch '(?i)fatal error|exception at|access violation|\[LUA ERROR\]'
    $outcomeSnapshot=if($summary -match 'recovered=true'){'cpu_choke_recovered.png'}else{'cpu_choke_defeated.png'}
    foreach($name in @('cpu_choke_paired.png',$outcomeSnapshot)){
        $passed=$passed -and (Test-Path -LiteralPath "$out\snap\$name" -PathType Leaf)
    }
    [ordered]@{case=$CaseName;passed=$passed;exit_code=$exitCode;player=$PlayerFighter;
        diagnostic_ladder_index=$LadderIndex;health_assistance=$false;walk_approach=$Approach.IsPresent;
        summary=$summary;input_hashes=$hashes} | ConvertTo-Json -Depth 4 |
        Out-File -LiteralPath "$out\result.json" -Encoding utf8
    Write-Output "$CaseName pass=$passed $summary"
    if(-not $passed){throw "CPU choke contact failed: $CaseName"}
} finally {
    Pop-Location
    Get-ChildItem Env: | Where-Object Name -Like 'MK2KS_*' | Remove-Item
    foreach($key in $saved.Keys){Set-Item -LiteralPath "Env:$key" -Value $saved[$key]}
}
