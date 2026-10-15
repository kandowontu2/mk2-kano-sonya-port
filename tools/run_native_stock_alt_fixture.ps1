param(
    [Parameter(Mandatory=$true)][string]$CasePrefix,
    [Parameter(Mandatory=$true)][string]$Executable,
    [Parameter(Mandatory=$true)][string]$PayloadRomDirectory,
    [ValidateSet('kung_lao','liu_kang','cage','baraka','kitana','mileena','shang_tsung','raiden','sub_zero','reptile','scorpion','jax')]
    [string]$Victim='sub_zero',
    [ValidateSet(1,2)][int]$Side=1
)
$ErrorActionPreference='Stop'
$root=Split-Path $PSScriptRoot -Parent
if($CasePrefix -notmatch '^[a-zA-Z0-9_-]+$'){throw 'Use a simple evidence prefix'}
$Executable=(Resolve-Path -LiteralPath $Executable).Path
$PayloadRomDirectory=(Resolve-Path -LiteralPath $PayloadRomDirectory).Path
$out=Join-Path $root "${CasePrefix}_p${Side}_${Victim}"
if(Test-Path -LiteralPath $out){throw 'Refusing to overwrite diagnostic evidence'}
$expected=& python -c "import sys,json;sys.path.insert(0,sys.argv[1]);from verify_kano_victim_sync import VICTIMS;i,g=VICTIMS[sys.argv[2]];print(json.dumps({'id':i,'pose':format(g[-1],'08X')}))" $PSScriptRoot $Victim | ConvertFrom-Json
if($LASTEXITCODE -ne 0){throw 'Expectation lookup failed'}
$fixture=Join-Path $root 'mk2ks_native_stock_alt_fixture.lua'
$tracked=@($Executable,(Join-Path $PayloadRomDirectory 'mk2ks/mk2ks.mdata'),$PSCommandPath,$fixture,
    (Join-Path $root 'mk2ks_native_stock_body_test.lua'),(Join-Path $root 'mk2ks_kano_winner_hold_test.lua'),
    (Join-Path $root 'mk2ks_finish_state_trace.lua'),(Join-Path $root 'mk2ks_selector_exit_test.lua'),
    (Join-Path $PSScriptRoot 'verify_kano_victim_sync.py'),(Join-Path $PSScriptRoot 'verify_skeleton_sync.py'))
$hashes=@{}
foreach($path in $tracked){$hashes[$path]=(Get-FileHash -LiteralPath $path).Hash}
$saved=@{}
Get-ChildItem Env: | Where-Object {$_.Name -like 'MK2KS_*' -or $_.Name -like 'MK2_TRACE_*'} | ForEach-Object {$saved[$_.Name]=$_.Value}
New-Item -ItemType Directory -Path $out | Out-Null
Push-Location $root
try{
    Get-ChildItem Env: | Where-Object {$_.Name -like 'MK2KS_*' -or $_.Name -like 'MK2_TRACE_*'} | Remove-Item
    $env:MK2KS_TEST_FIGHTER=if($Side -eq 1){'kano'}else{$Victim}
    $env:MK2KS_P2_FIGHTER=if($Side -eq 1){$Victim}else{'kano'}
    $env:MK2KS_TEST_CONFIRM='hp'
    $env:MK2KS_TEST_CONFIRM_HOLD='8'
    $env:MK2KS_TWO_PLAYER='1'
    if($Side -eq 1){$env:MK2KS_TEST_ROUND_WIN='1'}else{$env:MK2KS_TEST_ROUND_LOSS='1'}
    $env:MK2KS_ASSERT_NATIVE_DISPLAY='1'
    $env:MK2KS_ASSERT_HUD_SHADOW='1'
    $env:MK2_TRACE_NATIVE_FINISH='kano'
    $env:MK2_TRACE_NATIVE_FINISH_SIDE="$Side"
    $env:MK2_TRACE_INPUT_ONLY_APPROACH='1'
    $env:MK2_TRACE_FINISH_ACTORS='1'
    $env:MK2_TRACE_SKELETON_OBJECT='1'
    $env:MK2_TRACE_FINISH_SOUND='1'
    $env:MK2_TRACE_VICTIM_PHASE_SNAPSHOTS='1'
    $env:MK2_TRACE_EXPECT_VICTIM_ID='{0:X4}' -f $expected.id
    $env:MK2_TRACE_EXPECT_VICTIM_HELD_POSE=$expected.pose
    & $Executable mk2ks -rompath "$PayloadRomDirectory;$root\roms" -artpath "$root\artwork" -skip_gameinfo -video none -sound none -nothrottle -str 110 -snapsize 400x300 -cfg_directory "$out\cfg" -nvram_directory "$out\nvram" -snapshot_directory "$out\snap" -autoboot_script $fixture 2>&1 | Out-File -LiteralPath "$out\run.log" -Encoding utf8
    $exitCode=$LASTEXITCODE
    foreach($path in $tracked){if((Get-FileHash -LiteralPath $path).Hash -ne $hashes[$path]){throw "Diagnostic input changed: $path"}}
    $log=Get-Content -LiteralPath "$out\run.log" -Raw
    & python (Join-Path $PSScriptRoot 'verify_kano_victim_sync.py') "$out\run.log" --side $Side --victim $Victim | Out-File -LiteralPath "$out\victim_sync.json" -Encoding utf8
    $sync=$LASTEXITCODE -eq 0
    $passed=$exitCode -eq 0 -and $sync -and
        $log -match 'MK2_NATIVE_STOCK_BODY_RESULT pass=true[^\r\n]*alternate=true ' -and
        $log.Contains('MK2_STOCK_ALT_FIXTURE_RESULT pass=true applied=1 errors=0 natural_selection_verified=false') -and
        $log.Contains('MK2_KANO_WINNER_HOLD_RESULT pass=true ') -and
        $log.Contains('MK2_KANO_VICTIM_HOLD_RESULT pass=true ') -and
        $log.Contains('MK2KS_EXIT_RESULT pass=true ') -and
        $log.Contains('MK2KS_STABILITY stalled_frames=0 trap_frames=0') -and
        $log.Contains('MK2KS_DISPLAY_RESULT pass=true ') -and
        $log.Contains('MK2KS_HUD_SHADOW_RESULT pass=true ') -and
        $log -notmatch '(?i)fatal error|exception at|access violation|\[LUA ERROR\]'
    [ordered]@{passed=$passed;side=$Side;victim=$Victim;assistance='alternate_palette_flag_once_and_round_health';natural_alternate_selection_verified=$false;victim_sync_validated=$sync;input_hashes=$hashes} | ConvertTo-Json -Depth 4 | Out-File -LiteralPath "$out\result.json" -Encoding utf8
    Write-Output "$out pass=$passed (controlled alternate flag, not natural selection)"
    if(-not $passed){throw 'Controlled alternate palette diagnostic failed'}
}finally{
    Pop-Location
    Get-ChildItem Env: | Where-Object {$_.Name -like 'MK2KS_*' -or $_.Name -like 'MK2_TRACE_*'} | Remove-Item
    foreach($key in $saved.Keys){Set-Item -LiteralPath "Env:$key" -Value $saved[$key]}
}
