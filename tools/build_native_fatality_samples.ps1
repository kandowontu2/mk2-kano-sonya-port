param([string]$OutputDirectory='')
$ErrorActionPreference='Stop'
$root=Split-Path $PSScriptRoot -Parent
if (-not $OutputDirectory) {$OutputDirectory=Join-Path $root 'samples\mk2ks'}
$clips=@(
    @{name='sonya_kiss';source='audit_v216_mk3_isolated_orb_02d5';duration='1.40';fade='1.25';fade_duration='0.15'},
    @{name='kano_extract';source='audit_v216_mk3_isolated_extract_02c4';duration='0.85';fade='0.70';fade_duration='0.15'},
    @{name='sonya_burn_fire';source='audit_v218_mk3_isolated_burn_081c_full';duration='3.85';fade='3.65';fade_duration='0.20'},
    @{name='sonya_burn_victim';source='audit_v216_mk3_isolated_burn_27b7';duration='2.75';fade='2.55';fade_duration='0.20'}
)
New-Item -ItemType Directory -Force -Path $OutputDirectory | Out-Null
foreach($clip in $clips) {
    $input=Join-Path $root "$($clip.source)\isolated.wav"
    if (-not (Test-Path -LiteralPath $input)) {throw "Missing isolated donor recording: $input"}
    $output=Join-Path $OutputDirectory "$($clip.name).wav"
    if (Test-Path -LiteralPath $output) {throw "Refusing to overwrite sample: $output"}
    & ffmpeg -n -hide_banner -loglevel error -ss 21.90 -t $clip.duration -i $input `
        -af "volume=20dB,afade=t=in:st=0:d=0.05,afade=t=out:st=$($clip.fade):d=$($clip.fade_duration)" `
        -ar 16000 -ac 1 -c:a pcm_s16le $output
    if ($LASTEXITCODE -ne 0) {throw "Could not make sample: $output"}
    [pscustomobject]@{sample=$clip.name;bytes=(Get-Item -LiteralPath $output).Length;
        sha256=(Get-FileHash -LiteralPath $output).Hash}
}
