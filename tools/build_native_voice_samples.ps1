param([string]$OutputDirectory='')
$ErrorActionPreference='Stop'
$root=Split-Path $PSScriptRoot -Parent
if (-not $OutputDirectory) {$OutputDirectory=Join-Path $root 'samples\mk2ks'}
$source=@(
    @{name='kano_select';id='236f';duration='1.15';fade='0.95'},
    @{name='sonya_select';id='2392';duration='1.15';fade='0.95'},
    @{name='kano_wins';id='2414';duration='2.00';fade='1.85'},
    @{name='sonya_wins';id='2439';duration='2.00';fade='1.85'}
)
New-Item -ItemType Directory -Force -Path $OutputDirectory | Out-Null
foreach($clip in $source) {
    $input=Join-Path $root "diagnostic_v153_sound_port_u8_$($clip.id)\isolated_loud.wav"
    if (-not (Test-Path -LiteralPath $input)) {throw "Missing verified isolated donor clip: $input"}
    $output=Join-Path $OutputDirectory "$($clip.name).wav"
    if (Test-Path -LiteralPath $output) {throw "Refusing to overwrite voice sample: $output"}
    & ffmpeg -hide_banner -loglevel error -ss 1.90 -t $clip.duration -i $input `
        -af "afade=t=in:st=0:d=0.08,afade=t=out:st=$($clip.fade):d=0.15" `
        -ar 16000 -ac 1 -c:a pcm_s16le $output
    if ($LASTEXITCODE -ne 0) {throw "Could not make voice sample: $output"}
    [pscustomobject]@{sample=$clip.name;command=$clip.id;bytes=(Get-Item -LiteralPath $output).Length;
        sha256=(Get-FileHash -LiteralPath $output).Hash}
}
