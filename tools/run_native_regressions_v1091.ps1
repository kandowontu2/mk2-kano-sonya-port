param([Parameter(Mandatory=$true)][ValidateSet('kano','sonya')][string]$Player,
      [Parameter(Mandatory=$true)][ValidateSet(1,2)][int]$Side)
$ErrorActionPreference='Stop'
$root=Split-Path $PSScriptRoot -Parent
$candidate='diagnostic_v1071_native_detached_arm_costume'
Push-Location $root
try {
    $case="audit_v1091_jax_${Player}_p${Side}_palette_regression"
    & "$PSScriptRoot/run_stock_fatality_v1050.ps1" -CaseName $case -Player $Player -Side $Side -CandidateName $candidate -Killer jax -Command fff_lp_release -Gap 64
    if ((Get-Content -LiteralPath "$case/result.json" -Raw | ConvertFrom-Json).exit_code -ne 0) { throw "Nonzero terminal case $case" }
    $case="audit_v1091_baraka_${Player}_p${Side}_palette_regression"
    & "$PSScriptRoot/run_rolling_head_v1003.ps1" -CaseName $case -Player $Player -Side $Side -CandidateName $candidate -Killer baraka -Command bbbb_hp -Gap 64
    if ((Get-Content -LiteralPath "$case/result.json" -Raw | ConvertFrom-Json).exit_code -ne 0) { throw "Nonzero terminal case $case" }
    $case="audit_v1091_cage_${Player}_p${Side}_palette_regression"
    & "$PSScriptRoot/run_cage_torso_v979.ps1" -CaseName $case -Player $Player -Side $Side -CandidateName $candidate -Killer cage -Command ddff_lp -Gap 64
    if ((Get-Content -LiteralPath "$case/result.json" -Raw | ConvertFrom-Json).exit_code -ne 0) { throw "Nonzero terminal case $case" }
    $case="audit_v1091_kitana_${Player}_p${Side}_palette_regression"
    & "$PSScriptRoot/run_native_inflation_v939.ps1" -CaseName $case -Player $Player -Side $Side -CandidateName $candidate -Killer kitana -Command ffdf_lk_release -Gap 64
    if ((Get-Content -LiteralPath "$case/result.json" -Raw | ConvertFrom-Json).exit_code -ne 0) { throw "Nonzero terminal case $case" }
    $case="audit_v1091_reptile_${Player}_p${Side}_palette_regression"
    & "$PSScriptRoot/run_reptile_death_grounding_v904.ps1" -CaseName $case -Player $Player -Side $Side -CandidateName $candidate
    if ((Get-Content -LiteralPath "$case/result.json" -Raw | ConvertFrom-Json).exit_code -ne 0) { throw "Nonzero terminal case $case" }
    "Five native action replays terminal for $Player P$Side; independent verification pending"
} finally { Pop-Location }
