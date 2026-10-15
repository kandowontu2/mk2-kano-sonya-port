param([ValidateSet(1,2)][int]$Side)
$ErrorActionPreference='Stop'
$taskRoot=Split-Path $PSScriptRoot -Parent
$taskPython='C:\Users\kando\AppData\Local\Programs\Python\Python314\python.exe'
Push-Location $taskRoot
try{
 $moves=if($Side -eq 1){@('choke','bicycle','blade','ring','knife','square','ball')}else{@('leg','choke','bicycle','blade','ring','knife','square','ball')}
 foreach($move in $moves){
  $case="audit_v1800_human_${move}_p${Side}_render"
  & "$PSScriptRoot/run_human_special_full_render_v1795.ps1" -CaseName $case -Move $move -Side $Side
  $result=Get-Content -LiteralPath "$case/result.json" -Raw | ConvertFrom-Json
  if($result.exit_code -ne 0){throw "Terminal capture failed: $case"}
  & $taskPython "$PSScriptRoot/verify_human_special_full_render_v1797.py" $case --output "${case}_checked"
  if($LASTEXITCODE -ne 0){throw "Native render check failed: $case"}
  & $taskPython "$PSScriptRoot/inspect_continuous_move_erase_v1798.py" $case --output "${case}_continuity_checked"
  if($LASTEXITCODE -ne 0){throw "Native continuity check failed: $case"}
  Write-Output "Accepted consecutive native body/shadow/erase: $move P$Side"
 }
 $case="audit_v1800_human_square_air_p${Side}_render"
 & "$PSScriptRoot/run_human_special_full_render_v1795.ps1" -CaseName $case -Move square -Side $Side -Air
 $result=Get-Content -LiteralPath "$case/result.json" -Raw | ConvertFrom-Json
 if($result.exit_code -ne 0){throw "Terminal capture failed: $case"}
 & $taskPython "$PSScriptRoot/verify_human_special_full_render_v1797.py" $case --output "${case}_checked"
 if($LASTEXITCODE -ne 0){throw "Native render check failed: $case"}
 & $taskPython "$PSScriptRoot/inspect_continuous_move_erase_v1798.py" $case --output "${case}_continuity_checked"
 if($LASTEXITCODE -ne 0){throw "Native continuity check failed: $case"}
 Write-Output "Accepted consecutive native body/shadow/erase: airborne square P$Side"
}finally{Pop-Location}
