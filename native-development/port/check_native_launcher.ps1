$ErrorActionPreference = 'Stop'
$nativeMame = [IO.Path]::GetFullPath((Join-Path $PSScriptRoot '..\..\..\mame0289\mame.exe'))
$nativeRoms = Join-Path $PSScriptRoot 'development_patches\roundtrip\roms\mk3.zip'
$expectedMame = 'AF6966108D9B52C22465C6D50F4E5D50CC371B50F2D27DC443935F287AAD37A3'
$expectedRoms = '454772BC6831B6B2F672E59F23FC5456ADCEB886CBC98FE1D8DEC4559EFD0C38'
foreach ($check in @(@($nativeMame, $expectedMame), @($nativeRoms, $expectedRoms))) {
    if (-not (Test-Path -LiteralPath $check[0] -PathType Leaf)) { throw "Missing native playtest input: $($check[0])" }
    $nativeStream = [IO.File]::OpenRead($check[0])
    $nativeHasher = [Security.Cryptography.SHA256]::Create()
    try { $actualHash = [BitConverter]::ToString($nativeHasher.ComputeHash($nativeStream)).Replace('-', '') }
    finally { $nativeStream.Dispose(); $nativeHasher.Dispose() }
    if ($actualHash -ne $check[1]) { throw "Changed native playtest input: $($check[0])" }
}
Write-Output 'Verified stock MAME and current native ROM-patch development archive. Final acceptance remains open.'
