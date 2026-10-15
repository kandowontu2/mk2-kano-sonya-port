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
$audit=Join-Path $root 'mk2ks_missing_animation_probe.lua'
$stress=Join-Path $root 'mk2ks_native_input_stress.lua'
$base=Join-Path $root 'mk2ks_selector_exit_test.lua'
$tracked=@($Executable,$payload,$audit,$stress,$base,$PSCommandPath)
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
        $env:MK2KS_ASSERT_NATIVE_DISPLAY='1'
        $env:MK2KS_ASSERT_HUD_SHADOW='1'
        $env:MK2KS_ANIM_PROBE_BASE='mk2ks_native_input_stress.lua'
        $case="${CasePrefix}_p1_${first}"
        $out=Join-Path $root $case
        if(Test-Path -LiteralPath $out){throw "Refusing to overwrite evidence: $out"}
        New-Item -ItemType Directory -Path $out | Out-Null
        & $Executable mk2ks -rompath "$PayloadRomDirectory;$root\roms_v22_clean;$root\roms" `
            -artpath "$root\artwork" -skip_gameinfo -video none -sound none -nothrottle `
            -str $Seconds -snapsize 400x300 -cfg_directory "$out\cfg" `
            -nvram_directory "$out\nvram" -snapshot_directory "$out\snap" `
            -autoboot_script $audit 2>&1 | Out-File -LiteralPath "$out\run.log" -Encoding utf8
        $exitCode=$LASTEXITCODE
        foreach($path in $tracked){
            if((Get-FileHash -LiteralPath $path).Hash -ne $hashes[$path]){throw "Input changed: $path"}
        }
        $log=Get-Content -LiteralPath "$out\run.log" -Raw
        $mainEntries=[regex]::Matches($log,'MK2KS_ANIM_AUDIT_ENTRY key=\w+:main:\d+ reads=(\d+)')
        $mainReads=0
        foreach($entry in $mainEntries){$mainReads+=[int]$entry.Groups[1].Value}
        $stressResult=[regex]::Match($log,'MK2KS_INPUT_STRESS_RESULT[^\r\n]*').Value
        $activeMatch=[regex]::Match($stressResult,'active=(\d+)')
        $passed=$exitCode -eq 0 -and $mainEntries.Count -eq 7 -and $mainReads -eq 0 -and
            $activeMatch.Success -and [int]$activeMatch.Groups[1].Value -ge 1000 -and
            $stressResult.Contains('identity_errors=0') -and
            $log.Contains('MK2KS_EXIT_RESULT pass=true ') -and
            $log.Contains('MK2KS_DISPLAY_RESULT pass=true ') -and
            $log.Contains('MK2KS_HUD_SHADOW_RESULT pass=true ') -and
            $log.Contains('MK2KS_STABILITY stalled_frames=0 trap_frames=0') -and
            $log -notmatch '(?i)fatal error|exception at|access violation|\[LUA ERROR\]'
        [ordered]@{case=$case;passed=$passed;fighter_p1=$first;fighter_p2=$second;
            assisted=$false;seconds=$Seconds;exit_code=$exitCode;
            missing_main_cells_checked=$mainEntries.Count;missing_main_reads=$mainReads;
            input_stress_summary=$stressResult;
            executable_sha256=$hashes[$Executable];payload_sha256=$hashes[$payload];
            audit_sha256=$hashes[$audit];stress_sha256=$hashes[$stress];
            base_harness_sha256=$hashes[$base]} |
            ConvertTo-Json | Out-File -LiteralPath "$out\result.json" -Encoding utf8
        Write-Output "$case pass=$passed missing_main_reads=$mainReads $stressResult"
        if(-not $passed){$failures+=$case}
    }
} finally {
    Pop-Location
    Get-ChildItem Env: | Where-Object Name -Like 'MK2KS_*' | Remove-Item
    foreach($key in $saved.Keys){Set-Item -LiteralPath "Env:$key" -Value $saved[$key]}
}
if($failures.Count){throw "Missing-animation stress failed: $($failures -join ', ')"}
