param(
    [Parameter(Mandatory=$true)][string]$Name,
    [Parameter(Mandatory=$true)][string]$PayloadRomDirectory
)
$ErrorActionPreference='Stop'
if ($Name -notmatch '^diagnostic_v[0-9]+_[a-z0-9_]+$') { throw 'Use a versioned candidate directory name' }
$portRoot=Split-Path $PSScriptRoot -Parent
$repo=Join-Path $portRoot 'mame-mkp'
$out=Join-Path $portRoot $Name
$recovery=Join-Path $portRoot 'diagnostic_v43_leg_candidate\mkport_v42.exe'
$installed=Join-Path $repo 'mkport.exe'
$expectedInstalled='413855890FCE3BECAC9B24E11699FAD1CE465ACCBE4B27A93F2DD5819D13A891'
foreach ($path in @($recovery,$installed)) {
    if ((Get-FileHash -LiteralPath $path).Hash -ne $expectedInstalled) { throw "Installed/recovery build changed: $path" }
}
if (Test-Path -LiteralPath $out) { throw 'Refusing to overwrite a candidate or its evidence' }
if (@(Get-CimInstance Win32_Process | Where-Object {$_.ExecutablePath -eq $installed}).Count) { throw 'Installed emulator is running' }
$payload=(Resolve-Path -LiteralPath "$PayloadRomDirectory\mk2ks\mk2ks.mdata").Path
$originalSource=Join-Path $portRoot 'audit_v1249_rom_metadata_source\midtunit.before.cpp'
$currentSource=Join-Path $repo 'src\mame\midway\midtunit.cpp'
$oldMetadata='CRC(10ab3463) SHA1(055fbffc9b7ea6f039a2816549e138ab55179379)'
$newMetadata='CRC(4a606b51) SHA1(36a54a06e295ea08f1ce9bda9bfbce6353731ca9)'
if((Get-FileHash -LiteralPath $originalSource).Hash -ne '07C1FA27AAA0B1C836E462BC6EC13D62DFF405FA2B7F1358D7BB34B51731DA85') {throw 'Original native driver source changed'}
if((Get-FileHash -LiteralPath $currentSource).Hash -ne '07C1FA27AAA0B1C836E462BC6EC13D62DFF405FA2B7F1358D7BB34B51731DA85') {throw 'Historical source must be intact before staging'}
if((Get-FileHash -LiteralPath "$repo/src/mame/midway/midtunit_m.cpp").Hash -ne 'EE48F2FBD72749354A44F3B6574D00EB5DD879EC368A73FBDD57540A4F351D34') {throw 'Historical machine source must be intact before staging'}
$stage=Join-Path $portRoot 'audit_v1834_ball_register_source'
$prior=Get-Content -LiteralPath "$portRoot/diagnostic_v1597_native_ground_throw/build-info.json" -Raw | ConvertFrom-Json
foreach($item in $prior.input_hashes.PSObject.Properties){if((Get-FileHash -LiteralPath $item.Name).Hash -ne $item.Value){throw "Prior compiled input changed: $($item.Name)"}}
if((Get-FileHash -LiteralPath "$repo/src/mame/midway/midtunit.h").Hash -ne '256577139683DE7226D3EC0966CAC9B44C9C01C96ED561D236112B2DBADC7644'){throw 'Historical header changed before staging'}
if((Get-FileHash -LiteralPath $payload).Hash -ne '5646E839C73C4DB89BCF7CC87ECADBDA94B1E0D30EB1C0D2ED50A21A5524E23D') {throw 'Exact corrected native headed-reaction payload required'}
$tracked=@($payload,"$stage/midtunit_m.cpp","$stage/midtunit.cpp","$stage/midtunit.h","$repo\src\mame\midway\midtunit_m.cpp","$repo\src\mame\midway\midtunit.cpp",
	"$repo\src\mame\midway\mk2ks_native_picture.h","$repo\src\mame\midway\midtunit_v.h",
    "$repo\src\mame\midway\midtunit_v.cpp","$repo\src\mame\midway\midtunit.h",
    "$repo\src\frontend\mame\mame.cpp",
    "$repo\src\devices\cpu\tms34010\tms34010.cpp","$repo\src\devices\cpu\tms34010\tms34010.h")
$tracked+=Get-ChildItem -LiteralPath (Join-Path $portRoot 'samples\mk2ks') -File -Filter '*.wav' |
    Sort-Object Name | Select-Object -ExpandProperty FullName
$savedPath=$env:PATH
try {
Copy-Item -LiteralPath "$stage/midtunit_m.cpp" -Destination "$repo/src/mame/midway/midtunit_m.cpp" -Force
Copy-Item -LiteralPath "$stage/midtunit.cpp" -Destination $currentSource -Force
Copy-Item -LiteralPath "$stage/midtunit.h" -Destination "$repo/src/mame/midway/midtunit.h" -Force
$before=@{}
foreach ($path in $tracked) { $before[$path]=(Get-FileHash -LiteralPath $path).Hash }
New-Item -ItemType Directory -Path $out | Out-Null
New-Item -ItemType Directory -Path "$out/input_sources" | Out-Null
foreach ($path in $tracked) {
    if ([IO.Path]::GetExtension($path) -in '.cpp','.h') {
        $relative=[IO.Path]::GetRelativePath($portRoot,$path)
        $frozen=Join-Path "$out/input_sources" $relative
        New-Item -ItemType Directory -Path (Split-Path $frozen -Parent) -Force | Out-Null
        Copy-Item -LiteralPath $path -Destination $frozen
    }
}
$compiledInputs=@{}
foreach($path in $tracked){
    if([IO.Path]::GetExtension($path) -in '.cpp','.h'){
        $relative=[IO.Path]::GetRelativePath($portRoot,$path)
        $compiledInputs[(Join-Path "$out/input_sources" $relative)]=$before[$path]
    }else{$compiledInputs[$path]=$before[$path]}
}
$compiledInputs[$originalSource]=(Get-FileHash -LiteralPath $originalSource).Hash
$compiledInputs[$PSCommandPath]=(Get-FileHash -LiteralPath $PSCommandPath).Hash
Copy-Item -LiteralPath $PSCommandPath -Destination "$out/input_sources"
Push-Location $repo
try {
    $env:PATH='C:\Program Files\Git\usr\bin;C:\Users\kando\AppData\Local\Programs\Python\Python314;C:\Strawberry\c\bin;'+$env:PATH
    # MAME's version probe can print a harmless git-describe warning on stderr.
    # Judge the native build by its exit status, not PowerShell's stderr promotion.
    $ErrorActionPreference='Continue'
    & gmake.exe SUBTARGET=mkport PYTHON_EXECUTABLE=C:/Users/kando/AppData/Local/Programs/Python/Python314/python.exe MINGW64=C:/Strawberry/c PTR64=1 -j4 2>&1 |
        Out-File -LiteralPath "$out\build.log" -Encoding utf8
    $ErrorActionPreference='Stop'
    if ($LASTEXITCODE -ne 0) { throw "Candidate build failed: $LASTEXITCODE" }
    foreach ($path in $tracked) { if ((Get-FileHash -LiteralPath $path).Hash -ne $before[$path]) { throw "Build inputs changed: $path" } }
    Copy-Item -LiteralPath $installed -Destination "$out\mkport_candidate.exe"
    New-Item -ItemType Directory -Path "$out/roms/mk2ks" | Out-Null
    Copy-Item -LiteralPath $payload -Destination "$out/roms/mk2ks/mk2ks.mdata"
    [ordered]@{name=$Name;executable_sha256=(Get-FileHash -LiteralPath "$out\mkport_candidate.exe").Hash;
        payload_sha256=$before[$payload];input_hashes=$compiledInputs;canonical_source_hashes_at_compile=$before;
        assembly='Source rebuild: ball callback preserves original MKII maximum separation and all helper-clobbered caller registers during rebound; native throw router, true actor IDs, move timing/damage, payload and audio unchanged from v1597';
        metadata_only_source_rebuild=$false;game_data_changed=$true;prior_candidate='diagnostic_v1597_native_ground_throw'} | ConvertTo-Json -Depth 4 |
        Out-File -LiteralPath "$out\build-info.json" -Encoding utf8
} finally {
    $env:PATH=$savedPath
    Pop-Location
}
} finally {
    Copy-Item -LiteralPath $recovery -Destination $installed -Force
    Copy-Item -LiteralPath "$portRoot/diagnostic_v1411_native_grab_audio/input_sources/mame-mkp/src/mame/midway/midtunit.h" -Destination "$repo/src/mame/midway/midtunit.h" -Force
    if((Get-FileHash -LiteralPath "$repo/src/mame/midway/midtunit.h").Hash -ne '256577139683DE7226D3EC0966CAC9B44C9C01C96ED561D236112B2DBADC7644'){throw 'Historical header restoration failed'}
    Copy-Item -LiteralPath "$portRoot/audit_v1321_ring_close_source_transition/midtunit_m.before.cpp" -Destination "$repo/src/mame/midway/midtunit_m.cpp" -Force
    Copy-Item -LiteralPath "$portRoot/audit_v1321_ring_close_source_transition/midtunit.before.cpp" -Destination "$repo/src/mame/midway/midtunit.cpp" -Force
    if((Get-FileHash "$repo/src/mame/midway/midtunit_m.cpp").Hash -ne 'EE48F2FBD72749354A44F3B6574D00EB5DD879EC368A73FBDD57540A4F351D34' -or (Get-FileHash "$repo/src/mame/midway/midtunit.cpp").Hash -ne '07C1FA27AAA0B1C836E462BC6EC13D62DFF405FA2B7F1358D7BB34B51731DA85'){throw 'Historical source restoration failed'}
    $env:PATH=$savedPath
    if ((Get-FileHash -LiteralPath $installed).Hash -ne $expectedInstalled) { throw 'Installed executable restoration failed' }
}
Get-Content -LiteralPath "$out\build-info.json"
