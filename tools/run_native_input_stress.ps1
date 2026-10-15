param(
    [Parameter(Mandatory=$true)][string]$CasePrefix,
    [Parameter(Mandatory=$true)][string]$Executable,
    [Parameter(Mandatory=$true)][string]$PayloadRomDirectory,
    [int]$Seconds=180
)
$ErrorActionPreference='Stop'
$root=Split-Path $PSScriptRoot -Parent
if($CasePrefix -notmatch '^[a-zA-Z0-9_-]+$'){throw 'Use a simple evidence prefix.'}
$Executable=(Resolve-Path -LiteralPath $Executable).Path
$PayloadRomDirectory=(Resolve-Path -LiteralPath $PayloadRomDirectory).Path
$payload=Join-Path $PayloadRomDirectory 'mk2ks\mk2ks.mdata'
$harness=Join-Path $root 'mk2ks_native_input_stress.lua'
$base=Join-Path $root 'mk2ks_selector_exit_test.lua'
$tracked=@($Executable,$payload,$harness,$base,$PSCommandPath)
$hashes=@{}
foreach($path in $tracked){$hashes[$path]=(Get-FileHash -LiteralPath $path).Hash}
$saved=@{}
Get-ChildItem Env: | Where-Object Name -Like 'MK2KS_*' |
    ForEach-Object {$saved[$_.Name]=$_.Value}
$failures=@()
Push-Location $root
try {
    foreach($first in @('kano','sonya')){
        foreach($path in $tracked){
            if((Get-FileHash -LiteralPath $path).Hash -ne $hashes[$path]){throw "Input changed: $path"}
        }
        Get-ChildItem Env: | Where-Object Name -Like 'MK2KS_*' | Remove-Item
        $second=if($first -eq 'kano'){'sonya'}else{'kano'}
        $env:MK2KS_TEST_FIGHTER=$first
        $env:MK2KS_P2_FIGHTER=$second
        $env:MK2KS_TEST_CONFIRM='hp'
        $env:MK2KS_TEST_CONFIRM_HOLD='8'
        $env:MK2KS_TWO_PLAYER='1'
        $env:MK2KS_TEST_ROUND_WIN='0'
        $env:MK2KS_TEST_ROUND_LOSS='0'
        $env:MK2KS_ASSERT_NATIVE_DISPLAY='1'
        $env:MK2KS_ASSERT_HUD_SHADOW='1'
        $case="${CasePrefix}_p1_${first}"
        $out=Join-Path $root $case
        if(Test-Path -LiteralPath $out){throw "Refusing to overwrite evidence: $out"}
        New-Item -ItemType Directory -Path $out | Out-Null
        & $Executable mk2ks -rompath "$PayloadRomDirectory;$root\roms_v22_clean;$root\roms" `
            -artpath "$root\artwork" -skip_gameinfo -video none -sound none -nothrottle `
            -str $Seconds -snapsize 400x300 -cfg_directory "$out\cfg" `
            -nvram_directory "$out\nvram" -snapshot_directory "$out\snap" `
            -autoboot_script $harness 2>&1 | Out-File -LiteralPath "$out\run.log" -Encoding utf8
        $exitCode=$LASTEXITCODE
        foreach($path in $tracked){
            if((Get-FileHash -LiteralPath $path).Hash -ne $hashes[$path]){throw "Input changed: $path"}
        }
        $log=Get-Content -LiteralPath "$out\run.log" -Raw
        $summary=([regex]::Match($log,'MK2KS_INPUT_STRESS_RESULT[^\r\n]*')).Value
        $match=[regex]::Match($summary,
            'active=(\d+) ids=(\d+),(\d+) identity_errors=(\d+) xspan=(\d+),(\d+) action_changes=(\d+),(\d+) health_drops=(\d+),(\d+)')
        $expected1=if($first -eq 'kano'){17}else{18}
        $expected2=if($first -eq 'kano'){18}else{17}
        $p2WinPattern='MK2KS_NATIVE_WIN frame=\d+ winner=' + $expected2.ToString('X4') + ' '
        $p2WinCount=([regex]::Matches($log,$p2WinPattern)).Count
        $passed=$exitCode -eq 0 -and $match.Success -and
            [int]$match.Groups[1].Value -ge 1000 -and
            [int]$match.Groups[2].Value -eq $expected1 -and
            [int]$match.Groups[3].Value -eq $expected2 -and
            [int]$match.Groups[4].Value -eq 0 -and
            [int]$match.Groups[5].Value -ge 20 -and
            [int]$match.Groups[6].Value -ge 20 -and
            [int]$match.Groups[7].Value -ge 8 -and
            [int]$match.Groups[8].Value -ge 8 -and
            $p2WinCount -ge 2 -and
            $log.Contains('MK2KS_DISPLAY_RESULT pass=true ') -and
            $log.Contains('MK2KS_HUD_SHADOW_RESULT pass=true ') -and
            $log.Contains('MK2KS_STABILITY stalled_frames=0 trap_frames=0') -and
            $log.Contains('MK2KS_EXIT_RESULT pass=true ') -and
            $log -notmatch '(?i)fatal error|exception at|access violation|\[LUA ERROR\]'
        [ordered]@{case=$case;passed=$passed;fighter_p1=$first;fighter_p2=$second;
            assisted=$false;exit_code=$exitCode;seconds=$Seconds;p2_native_wins=$p2WinCount;summary=$summary;
            executable_sha256=$hashes[$Executable];payload_sha256=$hashes[$payload];
            harness_sha256=$hashes[$harness];base_harness_sha256=$hashes[$base]} |
            ConvertTo-Json | Out-File -LiteralPath "$out\result.json" -Encoding utf8
        Write-Output "$case pass=$passed $summary"
        if(-not $passed){$failures+=$case}
    }
} finally {
    Pop-Location
    Get-ChildItem Env: | Where-Object Name -Like 'MK2KS_*' | Remove-Item
    foreach($key in $saved.Keys){Set-Item -LiteralPath "Env:$key" -Value $saved[$key]}
}
if($failures.Count){throw "Native input stress failed: $($failures -join ', ')"}
