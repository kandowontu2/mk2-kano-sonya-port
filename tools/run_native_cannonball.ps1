param(
    [Parameter(Mandatory=$true)][string]$CasePrefix,
    [string]$Executable = '',
    [string]$PayloadRomDirectory = '',
    [ValidateSet('kano','sonya')][string[]]$Fighters = @('kano','sonya'),
    [ValidateSet('hit','block','miss','short','boundary','minimum','held','airborne','recharge','wrong_button')]
    [string[]]$Cases = @('hit','block','miss','short','boundary','minimum','held','airborne','recharge','wrong_button'),
    [switch]$VictimAirTrace
)
$ErrorActionPreference = 'Stop'
$portRoot = Split-Path $PSScriptRoot -Parent
if ($CasePrefix -notmatch '^[a-zA-Z0-9_-]+$') { throw 'CasePrefix must be a simple directory prefix.' }
if ([bool]$Executable -ne [bool]$PayloadRomDirectory) { throw 'Supply both candidate executable and payload directory, or neither.' }
if (-not $Executable) { $Executable = "$portRoot\mame-mkp\mkport.exe" }
if (-not $PayloadRomDirectory) { $PayloadRomDirectory = "$portRoot\roms_v22_clean" }
$exePath = (Resolve-Path -LiteralPath $Executable).Path
$romRoot = (Resolve-Path -LiteralPath $PayloadRomDirectory).Path
$romPath = "$romRoot;$portRoot\roms_v22_clean;$portRoot\roms"
$payload = Join-Path $romRoot 'mk2ks\mk2ks.mdata'
$payloadHash = (Get-FileHash -LiteralPath $payload).Hash
& $exePath mk2ks -rompath $romPath -verifyroms
if ($LASTEXITCODE -ne 0) { throw 'Selected executable/payload failed ROM verification.' }
$env:MK2KS_TEST_CONFIRM = 'hp'
$env:MK2KS_TWO_PLAYER = '1'
$env:MK2KS_ASSERT_LIFECYCLE = '0'
$env:MK2KS_TEST_ROUND_WIN = '0'
$env:MK2KS_TEST_ROUND_LOSS = '0'
$env:MK2KS_TEST_PROJECTILES = '0'
$env:MK2KS_TEST_SQUARE = ''
$env:MK2KS_TEST_LEG = ''
$env:MK2KS_TRACE_LEG = '0'
$env:MK2KS_BALL_HOLD = ''
$env:MK2KS_TRACE_TABLES = '0'
$env:MK2KS_TRACE_REACTIONS = '0'
$env:MK2KS_TRACE_BALL = '0'
$env:MK2KS_BALL_VICTIM_AIR_TRACE = if ($VictimAirTrace) { '1' } else { '0' }
$env:MK2KS_ASSERT_NATIVE_DISPLAY = '1'
$env:MK2KS_ASSERT_HUD_SHADOW = '1'
$failures = @()
$buildHash = (Get-FileHash -LiteralPath $exePath -Algorithm SHA256).Hash
Push-Location "$portRoot\mame-mkp"
try {
    foreach ($fighter in $Fighters) {
        $env:MK2KS_TEST_FIGHTER = $fighter
        $env:MK2KS_P2_FIGHTER = if ($fighter -eq 'kano') { 'sonya' } else { 'kano' }
        foreach ($mode in $Cases) {
            if ((Get-FileHash -LiteralPath $exePath).Hash -ne $buildHash -or (Get-FileHash -LiteralPath $payload).Hash -ne $payloadHash) {
                throw 'Executable changed during the suite.'
            }
            $env:MK2KS_TEST_BALL = $mode
            $case = "${CasePrefix}_${fighter}_${mode}"
            $out = Join-Path $portRoot $case
            if (Test-Path -LiteralPath $out) { throw "Refusing to overwrite existing evidence: $out" }
            New-Item -ItemType Directory -Path $out | Out-Null
            & $exePath mk2ks -rompath $romPath -artpath '..\artwork' -skip_gameinfo `
                -video none -sound none -nothrottle -str 45 -snapsize 800x600 `
                -cfg_directory "$out\cfg" -nvram_directory "$out\nvram" -snapshot_directory "$out\snap" `
                -autoboot_script '..\mk2ks_selector_exit_test.lua' 2>&1 |
                Out-File -LiteralPath "$out\run.log" -Encoding utf8
            $exitCode = $LASTEXITCODE
            if ((Get-FileHash -LiteralPath $exePath).Hash -ne $buildHash -or (Get-FileHash -LiteralPath $payload).Hash -ne $payloadHash) {
                throw 'Executable changed during this case.'
            }
            $log = Get-Content -LiteralPath "$out\run.log" -Raw
            $passed = $exitCode -eq 0 -and $log -match 'MK2KS_BALL_RESULT pass=true ' -and
                $log -match 'MK2KS_EXIT_RESULT pass=true ' -and $log -match 'MK2KS_DISPLAY_RESULT pass=true ' -and
                $log -match 'MK2KS_HUD_SHADOW_RESULT pass=true ' -and
                $log -match 'MK2KS_STABILITY stalled_frames=0 trap_frames=0' -and
                $log -notmatch '(?i)fatal error|exception at|access violation|error in emu'
            [ordered]@{case=$case; passed=$passed; executable_sha256=$buildHash; payload_sha256=$payloadHash; exit_code=$exitCode} |
                ConvertTo-Json | Out-File -LiteralPath "$out\result.json" -Encoding utf8
            Write-Output "$case pass=$passed"
            if (-not $passed) { $failures += $case }
        }
    }
} finally { Pop-Location }
if ($failures.Count) { throw "Failed cannonball cases: $($failures -join ', ')" }
