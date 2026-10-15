param(
    [Parameter(Mandatory=$true)][string[]]$CasePrefixes,
    [string[]]$Victims=@('kung_lao','liu_kang','cage','baraka','kitana','mileena',
        'shang_tsung','raiden','sub_zero','reptile','scorpion','jax','kano','sonya')
)
$ErrorActionPreference='Stop'
$root=Split-Path $PSScriptRoot -Parent
foreach($prefix in $CasePrefixes){
    if($prefix -notmatch '^[a-zA-Z0-9_-]+$'){throw "Invalid case prefix: $prefix"}
}
$checked=0
$referenceExe=''
$referencePayload=''
foreach($victim in $Victims){
    $pair=@{}
    foreach($side in 1,2){
        foreach($prefix in $CasePrefixes){
            $file=Join-Path $root "${prefix}_${victim}_p${side}\result.json"
            if(Test-Path -LiteralPath $file){
                if($pair.ContainsKey($side)){throw "Duplicate $victim P$side result"}
                $pair[$side]=Get-Content -LiteralPath $file -Raw | ConvertFrom-Json
            }
        }
        if(-not $pair.ContainsKey($side)){throw "Missing $victim P$side result"}
        if(-not $pair[$side].passed){throw "Failed $victim P$side air throw"}
        if($pair[$side].side -ne $side -or $pair[$side].victim -ne $victim){
            throw "Mismatched $victim P$side result identity"
        }
        if(-not $referenceExe){$referenceExe=$pair[$side].executable_sha256}
        if(-not $referencePayload){$referencePayload=$pair[$side].payload_sha256}
        if($pair[$side].executable_sha256 -ne $referenceExe -or
            $pair[$side].payload_sha256 -ne $referencePayload){
            throw "Build hash mismatch in $victim P$side result"
        }
    }
    if($pair[1].separation -ne $pair[2].separation){
        throw "Air-throw mirror mismatch for $victim`: P1=$($pair[1].separation), P2=$($pair[2].separation)"
    }
    $checked++
    Write-Output "$victim mirror separation=$($pair[1].separation)"
}
Write-Output "Mirror symmetry passed: $checked victims, $($checked*2) throws."
Write-Output "Executable SHA256: $referenceExe"
Write-Output "Payload SHA256: $referencePayload"
