param(
    [Parameter(Mandatory=$true)][string]$CasePrefix,
    [Parameter(Mandatory=$true)][string]$Executable,
    [Parameter(Mandatory=$true)][string]$PayloadRomDirectory,
    [ValidateSet('kano','sonya','liu_kang')][string[]]$Fighters=@('kano','sonya','liu_kang'),
    [switch]$LongHover
)
$ErrorActionPreference='Stop'
if($CasePrefix -notmatch '^[a-zA-Z0-9_-]+$'){throw 'Use a simple evidence prefix'}
$root=Split-Path $PSScriptRoot -Parent
$Executable=(Resolve-Path -LiteralPath $Executable).Path
$PayloadRomDirectory=(Resolve-Path -LiteralPath $PayloadRomDirectory).Path
$harness=Join-Path $root 'mk2ks_selector_exit_test.lua'
$saved=@{}
Get-ChildItem Env: | Where-Object Name -Like 'MK2KS_*' | ForEach-Object {$saved[$_.Name]=$_.Value}
Push-Location $root
try {
    foreach($fighter in $Fighters){
        Get-ChildItem Env: | Where-Object Name -Like 'MK2KS_*' | Remove-Item
        $env:MK2KS_TEST_FIGHTER=$fighter
        $env:MK2KS_P2_FIGHTER='stock'
        $env:MK2KS_TEST_CONFIRM='hp'
        $env:MK2KS_TWO_PLAYER='0'
        if($LongHover){
            $env:MK2KS_TRACE_CURSOR_LONG='1'
            $env:MK2KS_TEST_CONFIRM_AT_AGE='300'
        } else {
            $env:MK2KS_TRACE_CURSOR_BLINK='1'
        }
        $out=Join-Path $root "${CasePrefix}_${fighter}"
        if(Test-Path -LiteralPath $out){throw "Evidence exists: $out"}
        New-Item -ItemType Directory -Path $out | Out-Null
        & $Executable mk2ks -rompath "$PayloadRomDirectory;$root\roms_v22_clean;$root\roms" `
            -artpath "$root\artwork" -skip_gameinfo -video none -sound none -nothrottle `
            -str $(if($LongHover){42}else{28}) -snapsize 400x300 -cfg_directory "$out\cfg" `
            -nvram_directory "$out\nvram" -snapshot_directory "$out\snap" `
            -autoboot_script $harness 2>&1 | Out-File -LiteralPath "$out\run.log" -Encoding utf8
        if($LASTEXITCODE -ne 0){throw "Cursor probe exited $LASTEXITCODE for $fighter"}
        $log=Get-Content -LiteralPath "$out\run.log" -Raw
        $label=if($LongHover){'cursor_trace_long'}else{'cursor_trace'}
        $required=if($LongHover){24}else{8}
        if(@([regex]::Matches($log,"MK2KS_EXIT snapshot=\d+ label=$label(?:\s|$)")).Count -ne $required){
            throw "Cursor probe did not capture $required frames for $fighter"
        }
        if(-not $log.Contains('MK2KS_EXIT_RESULT pass=true ')){
            throw "Selection did not enter combat after hover for $fighter"
        }
        Write-Output "$fighter cursor frames captured"
    }
    if(@($Fighters).Count -eq 3){
        $checker=if($LongHover){'check_cursor_long.py'}else{'check_cursor_temporal.py'}
        & python (Join-Path $PSScriptRoot $checker) $CasePrefix --root $root
        if($LASTEXITCODE -ne 0){throw 'Cursor/preview temporal screen-space check failed'}
    }
} finally {
    Pop-Location
    Get-ChildItem Env: | Where-Object Name -Like 'MK2KS_*' | Remove-Item
    foreach($key in $saved.Keys){Set-Item -LiteralPath "Env:$key" -Value $saved[$key]}
}
