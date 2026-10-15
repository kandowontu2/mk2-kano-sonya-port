param(
    [Parameter(Mandatory=$true)][string]$CasePrefix,
    [Parameter(Mandatory=$true)][string]$Executable,
    [Parameter(Mandatory=$true)][string]$PayloadRomDirectory,
    [ValidateSet('kano','sonya')][string[]]$Fighters=@('kano','sonya')
)
$ErrorActionPreference='Stop'
$root=Split-Path $PSScriptRoot -Parent
if($CasePrefix -notmatch '^[a-zA-Z0-9_-]+$'){throw 'Use a simple evidence prefix'}
$Executable=(Resolve-Path -LiteralPath $Executable).Path
$PayloadRomDirectory=(Resolve-Path -LiteralPath $PayloadRomDirectory).Path
$romPath="$PayloadRomDirectory;$root\roms_v22_clean;$root\roms"
$harness=Join-Path $root 'mk2ks_attract_carryover_test.lua'
$saved=@{}
Get-ChildItem Env: | Where-Object Name -Like 'MK2KS_*' | ForEach-Object {$saved[$_.Name]=$_.Value}
Push-Location $root
try {
    foreach($fighter in $Fighters){
        Get-ChildItem Env: | Where-Object Name -Like 'MK2KS_*' | Remove-Item
        $env:MK2KS_TEST_FIGHTER=$fighter
        $env:MK2KS_P2_FIGHTER='stock'
        $env:MK2KS_TEST_CONFIRM='hp'
        $env:MK2KS_TEST_CONFIRM_HOLD='8'
        $env:MK2KS_TWO_PLAYER='0'
        $env:MK2KS_TEST_ROUND_WIN='1'
        $env:MK2KS_ALLOW_NATURAL_LOSS='1'
        $env:MK2KS_ASSERT_NATIVE_DISPLAY='1'
        $env:MK2KS_ASSERT_HUD_SHADOW='1'
        $case="${CasePrefix}_${fighter}"
        $out=Join-Path $root $case
        if(Test-Path -LiteralPath $out){throw "Evidence exists: $out"}
        New-Item -ItemType Directory -Path $out | Out-Null
        & $Executable mk2ks -rompath $romPath -artpath "$root\artwork" -skip_gameinfo `
            -video none -sound none -nothrottle -str 250 -snapsize 400x300 `
            -cfg_directory "$out\cfg" -nvram_directory "$out\nvram" -snapshot_directory "$out\snap" `
            -autoboot_script $harness 2>&1 | Out-File -LiteralPath "$out\run.log" -Encoding utf8
        if($LASTEXITCODE -ne 0){throw "$fighter attract capture emulator failed"}
        $log=Get-Content -LiteralPath "$out\run.log" -Raw
        $passed=$log -match 'MK2KS_ATTRACT_CARRYOVER_RESULT stock_combat=true captures=3' -and
            $log -match 'MK2KS_CAMPAIGN_GAME_OVER ' -and
            $log -match 'MK2KS_EXIT_RESULT pass=true ' -and
            $log -match 'MK2KS_STABILITY stalled_frames=0 trap_frames=0'
        [ordered]@{fighter=$fighter;passed=$passed;
            executable_sha256=(Get-FileHash $Executable).Hash;
            payload_sha256=(Get-FileHash (Join-Path $PayloadRomDirectory 'mk2ks\mk2ks.mdata')).Hash} |
            ConvertTo-Json | Out-File -LiteralPath "$out\result.json" -Encoding utf8
        Write-Output "$case pass=$passed"
        if(-not $passed){throw "$fighter attract carryover run failed assertions"}
    }
} finally {
    Pop-Location
    Get-ChildItem Env: | Where-Object Name -Like 'MK2KS_*' | Remove-Item
    foreach($key in $saved.Keys){Set-Item -LiteralPath "Env:$key" -Value $saved[$key]}
}
