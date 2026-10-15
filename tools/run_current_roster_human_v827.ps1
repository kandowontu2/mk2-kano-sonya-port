param([Parameter(Mandatory=$true)][ValidateRange(0,3)][int]$Group)
$ErrorActionPreference='Stop'
$root=Split-Path $PSScriptRoot -Parent
$victims=@('kung_lao','liu_kang','cage','baraka','kitana','mileena','shang_tsung','raiden','reptile','scorpion','jax','kano','sonya')
$moves=@('knife','ball','blade','choke','ring','square','bicycle','leg')
$index=0
# The 18 current Sub-Zero positive cases already accepted in v821 remain the
# control fixtures. Every other selectable victim is freshly exercised here.
foreach($move in $moves) {
    foreach($side in @(1,2)) {
        foreach($victim in $victims) {
            $variants=if($move -eq 'square'){@($false,$true)}else{@($false)}
            foreach($air in $variants) {
                $selected=($index % 4) -eq $Group
                $index++
                if(-not $selected){continue}
                $suffix=if($air){"${move}_air"}else{$move}
                $name="audit_v827_positive_${suffix}_p${side}_$victim"
                & "$PSScriptRoot/run_current_human_special_v820.ps1" -CaseName $name -Move $move -Side $side -Victim $victim -Air:$air
            }
        }
    }
}
if($index -ne 234){throw 'Complete wider-roster fixture inventory required'}
"Group $Group completed its assigned current roster captures. Independent verification is still required."
