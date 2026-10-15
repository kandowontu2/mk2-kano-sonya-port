param([Parameter(Mandatory=$true)][string]$CaseName,[ValidateSet('kano','sonya')][string]$Target,
    [ValidateSet('hit','block','duck')][string]$Scenario='hit',[switch]$Choreography)
$ErrorActionPreference='Stop'
$root=Split-Path $PSScriptRoot -Parent
if($CaseName -notmatch '^audit_v[0-9]+_[a-z0-9_]+$'){throw 'Use versioned evidence names'}
$out=Join-Path $root $CaseName
if(Test-Path -LiteralPath $out){throw 'Refusing to overwrite evidence'}
$exe=Join-Path $root 'mame-mkp/mkwport.exe'
$autoboot="$root/mk3_ring_close_reference_v1318.lua"
$tracked=@($exe,$autoboot,"$root/mk3_projectile_choreography_reference.lua","$root/mk3_knife_geometry_reference.lua",$PSCommandPath)
$hashes=[ordered]@{};foreach($path in $tracked){$hashes[$path]=(Get-FileHash -LiteralPath $path).Hash}
New-Item -ItemType Directory -Path "$out/input_sources" | Out-Null
foreach($path in $tracked){if([IO.Path]::GetExtension($path) -in '.lua','.ps1'){Copy-Item -LiteralPath $path -Destination "$out/input_sources"}}
$hashes | ConvertTo-Json | Out-File "$out/input_hashes_before.json" -Encoding utf8
$savedTarget=$env:MK3_PROJECTILE_TARGET;$savedScenario=$env:MK3_KNIFE_GUARD
Push-Location $root
try {
    $env:MK3_PROJECTILE_TARGET=$Target;$env:MK3_KNIFE_GUARD=$Scenario
    & $exe mk3 -rompath "$root/roms;$root" -skip_gameinfo -nocheat -inipath "$out" -video none -sound none -nothrottle -str 100 -snapsize 400x300 `
        -cfg_directory "$out/cfg" -nvram_directory "$out/nvram" -snapshot_directory "$out/snap" -autoboot_script $autoboot 2>&1 |
        Out-File "$out/run.log" -Encoding utf8
    $code=$LASTEXITCODE
    foreach($path in $tracked){if((Get-FileHash -LiteralPath $path).Hash -ne $hashes[$path]){throw "Input changed during reference: $path"}}
    [ordered]@{exit_code=$code;target=$Target;scenario=$Scenario;scope='original_MK3_read_only_reference';choreography=[bool]$Choreography;input_hashes=$hashes} |
        ConvertTo-Json -Depth 4 | Out-File "$out/result.json" -Encoding utf8
    "$CaseName terminal exit=$code"
} finally {Pop-Location;$env:MK3_PROJECTILE_TARGET=$savedTarget;$env:MK3_KNIFE_GUARD=$savedScenario}
