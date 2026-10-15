param(
    [Parameter(Mandatory=$true)][string]$CaseName,
    [Parameter(Mandatory=$true)][string]$Executable,
    [Parameter(Mandatory=$true)][string]$PayloadRomDirectory,
    [Parameter(Mandatory=$true)][ValidateSet('kano','sonya')][string]$PlayerFighter,
    [Parameter(Mandatory=$true)][ValidateSet(17,18)][int]$OpponentId,
    [int]$LadderIndex=-1,
    [switch]$TraceVariety,
    [switch]$NaturalOnly,
    [ValidateSet('stock','projectile_zone','guard_uppercut','standing_hk')][string]$Strategy='stock',
    [ValidateRange(96,370)][int]$ConfirmAge=96,
    [ValidateRange(600,1500)][int]$BootFrame=600,
    [int]$Seconds=95
)
$ErrorActionPreference='Stop'
if(-not $NaturalOnly){throw 'This current-build runner permits natural input-only CPU cases only'}
if($CaseName -notmatch '^[a-zA-Z0-9_-]+$'){throw 'Use a simple evidence name.'}
if(-not $NaturalOnly -and ($PlayerFighter -eq 'kano' -and $OpponentId -ne 18 -or
   $PlayerFighter -eq 'sonya' -and $OpponentId -ne 17)){
    throw 'Choose the opposite added fighter as the CPU opponent.'
}
if($LadderIndex -lt -1 -or $LadderIndex -gt 16){throw 'Invalid ladder index.'}
if($NaturalOnly -and $LadderIndex -ne -1){throw 'Natural ladder runs cannot inject a stage'}
$root=Split-Path $PSScriptRoot -Parent
$Executable=(Resolve-Path -LiteralPath $Executable).Path
$PayloadRomDirectory=(Resolve-Path -LiteralPath $PayloadRomDirectory).Path
$payload=Join-Path $PayloadRomDirectory 'mk2ks\mk2ks.mdata'
$harness=Join-Path $root 'mk2ks_cpu_ladder_trace.lua'
if($NaturalOnly){$harness=Join-Path $root 'mk2ks_natural_cpu_moves_probe_v2.lua'}
$tracked=@($Executable,$payload,$harness,
    (Join-Path $root 'mk2ks_selector_exit_test.lua'),$PSCommandPath)
if($NaturalOnly){
    $candidateRoot=Split-Path $Executable -Parent
    $build=Get-Content "$candidateRoot/build-info.json" -Raw | ConvertFrom-Json
    foreach($item in $build.input_hashes.PSObject.Properties){if((Get-FileHash -LiteralPath $item.Name).Hash -ne $item.Value){throw "Candidate input changed: $($item.Name)"}}
    if((Get-FileHash -LiteralPath $Executable).Hash -ne $build.executable_sha256 -or (Get-FileHash -LiteralPath $payload).Hash -ne $build.payload_sha256){throw 'Candidate build changed'}
    $tracked+=@("$root/mk2ks_natural_cpu_moves_probe.lua","$root/mk2ks_cpu_ladder_trace.lua","$candidateRoot/build-info.json")
    $tracked+=@($build.input_hashes.PSObject.Properties.Name)
    $tracked+=@("$root/mk2ks_native_shang_morph.lua")
    $tracked+=@(Get-ChildItem -LiteralPath "$root/roms/mk2ks" -File | ForEach-Object {$_.FullName})
    $tracked+=@(Get-ChildItem -LiteralPath "$root/artwork" -File | ForEach-Object {$_.FullName})
}
$hashes=@{}
foreach($file in $tracked){$hashes[$file]=(Get-FileHash -LiteralPath $file).Hash}
$out=Join-Path $root $CaseName
if(Test-Path -LiteralPath $out){throw "Evidence exists: $out"}
New-Item -ItemType Directory -Path "$out/input_sources" | Out-Null
$hashes | ConvertTo-Json | Out-File "$out/input_hashes_before.json" -Encoding utf8
foreach($path in $tracked){if([IO.Path]::GetExtension($path) -in '.lua','.ps1','.json'){Copy-Item -LiteralPath $path -Destination "$out/input_sources"}}
$saved=@{}
Get-ChildItem Env: | Where-Object {$_.Name -match '^(MK2KS_|MK2_TRACE_|MK2_RANGE_|MK2_P2_)'} |
    ForEach-Object {$saved[$_.Name]=$_.Value}
Push-Location $root
try {
    Get-ChildItem Env: | Where-Object {$_.Name -match '^(MK2KS_|MK2_TRACE_|MK2_RANGE_|MK2_P2_)'} | Remove-Item
    $env:MK2KS_TEST_FIGHTER=$PlayerFighter
    $env:MK2KS_TEST_CONFIRM='hp'
    $env:MK2KS_TEST_CONFIRM_HOLD='8'
    $env:MK2KS_TEST_CONFIRM_AT_AGE="$ConfirmAge"
    $env:MK2KS_TEST_BOOT_FRAME="$BootFrame"
    $env:MK2KS_TWO_PLAYER='0'
    $env:MK2KS_TEST_ROUND_WIN='1'
    $env:MK2KS_ALLOW_NATURAL_LOSS='1'
    if(-not $NaturalOnly){$env:MK2KS_DIAGNOSTIC_CPU_ID="$OpponentId"}
    $env:MK2KS_ROUND_WIN_STRATEGY=$Strategy
    if($LadderIndex -ge 0){$env:MK2KS_DIAGNOSTIC_LADDER_INDEX="$LadderIndex"}
    $env:MK2KS_TRACE_CPU_OWNED_SPECIALS='1'
    if($TraceVariety){$env:MK2KS_TRACE_AI_VARIETY='1'}
    $env:MK2KS_ASSERT_NATIVE_DISPLAY='1'
    $env:MK2KS_ASSERT_HUD_SHADOW='1'
    & $Executable mk2ks -rompath "$PayloadRomDirectory;$root\roms" `
        -artpath "$root\artwork" -skip_gameinfo -nocheat -inipath "$out" -video none -sound none -nothrottle `
        -str $Seconds -snapsize 400x300 -cfg_directory "$out\cfg" `
        -nvram_directory "$out\nvram" -snapshot_directory "$out\snap" `
        -autoboot_script $harness 2>&1 | Out-File -LiteralPath "$out\run.log" -Encoding utf8
    $exitCode=$LASTEXITCODE
    foreach($file in $tracked){
        if((Get-FileHash -LiteralPath $file).Hash -ne $hashes[$file]){throw "Input changed: $file"}
    }
    $log=Get-Content -LiteralPath "$out\run.log" -Raw
    $owned=[regex]::Match($log,'MK2KS_CPU_OWNED_SPECIAL_RESULT kano=(\d+) sonya=(\d+)')
    $count=if($owned.Success){[int]$owned.Groups[1+($OpponentId-17)].Value}else{0}
    $requested=if($NaturalOnly){'nil'}else{"$OpponentId"}
    $injection=[regex]::Match($log,"MK2KS_CPU_DIAGNOSTIC_RESULT requested=$requested injected=(true|false)")
    $firstSpecial=[regex]::Match($log,"MK2KS_CPU_OWNED_SPECIAL frame=(\d+) id=$OpponentId ")
    $firstInjection=[regex]::Match($log,'MK2KS_CPU_DIAGNOSTIC_WRITE frame=(\d+) ')
    $specialFrame=if($firstSpecial.Success){[int]$firstSpecial.Groups[1].Value}else{-1}
    $injectionFrame=if($firstInjection.Success){[int]$firstInjection.Groups[1].Value}else{-1}
    $naturalSpecial=$specialFrame -ge 0 -and ($injectionFrame -lt 0 -or $specialFrame -lt $injectionFrame)
    $nativeEntries=[regex]::Matches($log,"(?m)^MK2_NAT_CPU_ENTRY frame=\d+ serial=\d+ id=$OpponentId ").Count
    $activation=if($NaturalOnly){$nativeEntries -gt 0}else{$count -gt 0 -and $firstSpecial.Success}
    $variety=[regex]::Match($log,'MK2KS_CPU_VARIETY_RESULT knife=(\d+) ball=(\d+) blade=(\d+) ring=(\d+) square=(\d+) bicycle=(\d+)')
    $alternateGroup=if($OpponentId -eq 17){2}else{5}
    $thirdGroup=if($OpponentId -eq 17){3}else{6}
    $thirdCount=if($variety.Success){[int]$variety.Groups[$thirdGroup].Value}else{0}
    $alternateCount=if($variety.Success){[int]$variety.Groups[$alternateGroup].Value+$thirdCount}else{0}
    $passed=$exitCode -eq 0 -and $owned.Success -and $activation -and
        (-not $TraceVariety -or ($variety.Success -and $alternateCount -gt 0)) -and
        $injection.Success -and
        (-not $NaturalOnly -or ($nativeEntries -gt 0 -and $injection.Groups[1].Value -eq 'false' -and $log.Contains('MK2KS_CPU_DIAGNOSTIC_LADDER_RESULT requested=nil injected=false') -and $log -notmatch 'MK2KS_CPU_DIAGNOSTIC_WRITE|MK2KS_CPU_DIAGNOSTIC_LADDER_WRITE')) -and
        $log.Contains('MK2KS_EXIT_RESULT pass=true ') -and
        $log.Contains('MK2KS_STABILITY stalled_frames=0 trap_frames=0') -and
        $log.Contains('MK2KS_DISPLAY_RESULT pass=true ') -and
        $log.Contains('MK2KS_HUD_SHADOW_RESULT pass=true ') -and
        $log.Contains('MK2KS_CPU_DIAGNOSTIC_HEALTH_RESULT requested=nil all_stages=false writes=0') -and
        $log.Contains('MK2KS_CPU_DIAGNOSTIC_P1_REGEN_RESULT enabled=false writes=0') -and
        $log -notmatch '(?i)fatal error|exception at|access violation|\[LUA ERROR\]'
    [ordered]@{case=$CaseName;passed=$passed;player=$PlayerFighter;opponent_id=$OpponentId;
        ladder_index=$LadderIndex;special_entries=$count;first_special_frame=$specialFrame;
        trace_variety=$TraceVariety.IsPresent;alternate_entries=$alternateCount;third_entries=$thirdCount;
        first_injection_frame=$injectionFrame;natural_special=$naturalSpecial;
        natural_only=$NaturalOnly.IsPresent;native_move_entries=$nativeEntries;strategy=$Strategy;confirm_age=$ConfirmAge;boot_frame=$BootFrame;memory_assistance='none';cheats=$false;input_hashes=$hashes;
        scope='CPU_action_entry_and_natural_selection_when_requested_not_complete_move_or_whole_game_fidelity';
        complete_native_move_verification_pending=$true;
        diagnostic_injected=$injection.Groups[1].Value;
        exit_code=$exitCode;executable_sha256=$hashes[$Executable];payload_sha256=$hashes[$payload];
        harness_sha256=$hashes[$harness]} |
        ConvertTo-Json | Out-File -LiteralPath "$out\result.json" -Encoding utf8
    Write-Output "$CaseName pass=$passed owned_special_entries=$count natural_special=$naturalSpecial first_special=$specialFrame first_injection=$injectionFrame"
    if(-not $passed){throw "CPU-owned special check failed: $CaseName"}
} finally {
    Pop-Location
    Get-ChildItem Env: | Where-Object {$_.Name -match '^(MK2KS_|MK2_TRACE_|MK2_RANGE_|MK2_P2_)'} | Remove-Item
    foreach($key in $saved.Keys){Set-Item -LiteralPath "Env:$key" -Value $saved[$key]}
}
