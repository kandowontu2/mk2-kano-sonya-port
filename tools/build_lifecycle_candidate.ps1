$ErrorActionPreference='Stop'
$portRoot=Split-Path $PSScriptRoot -Parent
$repo=Join-Path $portRoot 'mame-mkp'
$out=Join-Path $portRoot 'diagnostic_v44_lifecycle_candidate'
$recovery=Join-Path $portRoot 'diagnostic_v43_leg_candidate\mkport_v42.exe'
$installed=Join-Path $repo 'mkport.exe'
$expectedInstalled='413855890FCE3BECAC9B24E11699FAD1CE465ACCBE4B27A93F2DD5819D13A891'
foreach ($path in @($recovery,$installed)) {
    if ((Get-FileHash -LiteralPath $path).Hash -ne $expectedInstalled) {throw "Installed/recovery build changed: $path"}
}
if (Test-Path -LiteralPath $out) {throw 'Refusing to overwrite a candidate or its evidence'}
$live=@(Get-CimInstance Win32_Process | Where-Object {$_.ExecutablePath -eq $installed})
if ($live.Count) {throw 'Installed emulator is running'}
New-Item -ItemType Directory -Path $out | Out-Null
$savedPath=$env:PATH
Push-Location $repo
try {
    $env:PATH='C:\Program Files\Git\usr\bin;C:\Users\kando\AppData\Local\Programs\Python\Python314;C:\Strawberry\c\bin;'+$env:PATH
    & gmake.exe SUBTARGET=mkport PYTHON_EXECUTABLE=C:/Users/kando/AppData/Local/Programs/Python/Python314/python.exe MINGW64=C:/Strawberry/c PTR64=1 -j4 2>&1 |
        Out-File -LiteralPath "$out\build.log" -Encoding utf8
    if ($LASTEXITCODE -ne 0) {throw "Candidate build failed: $LASTEXITCODE"}
    Copy-Item -LiteralPath $installed -Destination "$out\mkport_lifecycle.exe"
    [ordered]@{
        change='Destroy retained autoboot Lua result before the Lua engine during shutdown'
        executable_sha256=(Get-FileHash -LiteralPath "$out\mkport_lifecycle.exe").Hash
        frontend_sha256=(Get-FileHash -LiteralPath "$repo\src\frontend\mame\mame.cpp").Hash
        gameplay_source_sha256=(Get-FileHash -LiteralPath "$repo\src\mame\midway\midtunit_m.cpp").Hash
        payload_sha256=(Get-FileHash -LiteralPath "$portRoot\diagnostic_v44_blade_candidate\roms\mk2ks\mk2ks.mdata").Hash
    } | ConvertTo-Json | Out-File -LiteralPath "$out\build-info.json" -Encoding utf8
} finally {
    Copy-Item -LiteralPath $recovery -Destination $installed -Force
    $env:PATH=$savedPath
    Pop-Location
    if ((Get-FileHash -LiteralPath $installed).Hash -ne $expectedInstalled) {throw 'Installed executable restoration failed'}
}
Get-Content -LiteralPath "$out\build-info.json"
