param([string]$CaseName='audit_v3269_current_native_cpu_square_hit')
$ErrorActionPreference='Stop'
$taskRoot=Split-Path $PSScriptRoot -Parent
$taskCandidate='diagnostic_v3172_native_morph_shadow'
$taskOut=Join-Path $taskRoot $CaseName
if($CaseName -notmatch '^audit_v[0-9]+_[a-z0-9_]+$' -or (Test-Path -LiteralPath $taskOut)){throw 'New immutable evidence leaf required'}
$taskBuildPath=Join-Path $taskRoot "$taskCandidate\build-info.json"
$taskBuild=Get-Content -LiteralPath $taskBuildPath -Raw | ConvertFrom-Json
$taskOriginal=Join-Path $taskRoot 'tools\run_native_cpu_square_locks_v3001.ps1'
$taskOriginalText=Get-Content -LiteralPath $taskOriginal -Raw
if($taskOriginalText -notmatch '-autoboot_script "\$root/mk2ks_native_cpu_square_locks_v3000.lua"'){throw 'Expected original observer chain'}
$taskSources=@($PSCommandPath,$taskOriginal,$taskBuildPath,
    "$taskRoot\$taskCandidate\mkport_candidate.exe","$taskRoot\$taskCandidate\roms\mk2ks\mk2ks.mdata",
    "$taskRoot\mk2ks_cpu_recovery_probe_v1438.lua","$taskRoot\mk2ks_physical_p2_cpu_continuation_v1997.lua",
    "$taskRoot\mk2ks_physical_p2_cpu_round_trace_v1998.lua","$taskRoot\mk2ks_physical_p2_cpu_overlap_trace_v1999.lua",
    "$taskRoot\mk2ks_physical_p2_cpu_choice_trace_v2035.lua","$taskRoot\mk2ks_native_cpu_square_boundary_v2993.lua",
    "$taskRoot\mk2ks_native_cpu_square_locks_v3000.lua","$taskRoot\mk2\mk2-maincpu.bin",
    "$taskRoot\mk2ks_physical_p2_cpu_square_trace_v2038.lua","$taskRoot\mk2ks_physical_p2_cpu_square_display_v2039.lua",
    "$taskRoot\mame-mkp\src\devices\cpu\tms34010\tms34010.cpp",
    "$taskRoot\mame-mkp\src\devices\cpu\tms34010\34010gfx.hxx","$taskRoot\mame-mkp\src\devices\cpu\tms34010\34010ops.hxx")
$taskSources+=@($taskBuild.input_hashes.PSObject.Properties.Name)
$taskSources+=@(Get-ChildItem -LiteralPath "$taskRoot\roms\mk2ks" -File | ForEach-Object FullName)
$taskSources+=@(Get-ChildItem -LiteralPath "$taskRoot\artwork" -File | ForEach-Object FullName)
$taskSources=@($taskSources | Select-Object -Unique)
foreach($taskPin in $taskBuild.input_hashes.PSObject.Properties){if((Get-FileHash -LiteralPath $taskPin.Name).Hash -ne $taskPin.Value){throw 'Compiled input changed'}}
if((Get-FileHash -LiteralPath "$taskRoot\$taskCandidate\mkport_candidate.exe").Hash -ne $taskBuild.executable_sha256 -or
   (Get-FileHash -LiteralPath "$taskRoot\$taskCandidate\roms\mk2ks\mk2ks.mdata").Hash -ne $taskBuild.payload_sha256){throw 'Matched current build required'}
New-Item -ItemType Directory -Path "$taskOut\input_sources" | Out-Null
& compact.exe /C /I /Q "/S:$taskOut" | Out-Null
if($LASTEXITCODE -ne 0){throw 'Capture compression could not be enabled'}
$taskHashes=@{};$taskSnapshots=@{}
foreach($taskFile in $taskSources){
    $taskResolved=(Resolve-Path -LiteralPath $taskFile).Path
    if(-not $taskResolved.StartsWith($taskRoot+'\',[StringComparison]::OrdinalIgnoreCase)){throw 'Expected workspace input only'}
    $taskHashes[$taskFile]=(Get-FileHash -LiteralPath $taskFile).Hash
    if([IO.Path]::GetExtension($taskFile) -in '.lua','.ps1','.json'){
        $taskRelative=$taskResolved.Substring($taskRoot.Length+1)
        $taskDestination=Join-Path "$taskOut\input_sources\tree" $taskRelative
        New-Item -ItemType Directory -Path (Split-Path $taskDestination -Parent) -Force | Out-Null
        Copy-Item -LiteralPath $taskFile -Destination $taskDestination
        if((Get-FileHash -LiteralPath $taskDestination).Hash -ne $taskHashes[$taskFile]){throw 'Exact original snapshot required'}
        $taskSnapshots[$taskFile]=$taskDestination
        # Legacy raster contracts read uniquely named Lua/PS1 files here.
        # JSON stays exclusively in its collision-free original hierarchy.
        if([IO.Path]::GetExtension($taskFile) -in '.lua','.ps1'){
            $taskAlias=Join-Path "$taskOut\input_sources" (Split-Path $taskFile -Leaf)
            if(Test-Path -LiteralPath $taskAlias){if((Get-FileHash -LiteralPath $taskAlias).Hash -ne $taskHashes[$taskFile]){throw 'Alias collision'}}
            else{Copy-Item -LiteralPath $taskFile -Destination $taskAlias}
        }
    }
}
$taskHashes | ConvertTo-Json | Out-File -LiteralPath "$taskOut\input_hashes_before.json" -Encoding utf8
$taskSnapshots | ConvertTo-Json | Out-File -LiteralPath "$taskOut\source_snapshot_paths.json" -Encoding utf8
$taskSaved=@{};Get-ChildItem Env: | Where-Object Name -match '^(MK2KS_|MK2_TRACE_|MK2_RANGE_|MK2_P2_)' | ForEach-Object {$taskSaved[$_.Name]=$_.Value}
Push-Location $taskRoot
try{
    Get-ChildItem Env: | Where-Object Name -match '^(MK2KS_|MK2_TRACE_|MK2_RANGE_|MK2_P2_)' | Remove-Item
    $env:MK2KS_TEST_FIGHTER='kano';$env:MK2KS_TEST_BOOT_FRAME='613';$env:MK2KS_TEST_CONFIRM='hp';$env:MK2KS_TEST_CONFIRM_HOLD='8';$env:MK2KS_TWO_PLAYER='0'
    $env:MK2KS_CPU_PAIR_APPROACH='guard_until_close';$env:MK2KS_CPU_CONTINUATION_POLICY='jump_guard';$env:MK2KS_CPU_PAIR_CONFIRM_AGE='264';$env:MK2KS_FLOOR_OUT=$taskOut
    & "$taskRoot\$taskCandidate\mkport_candidate.exe" mk2ks -rompath "$taskRoot\$taskCandidate\roms;$taskRoot\roms" -artpath "$taskRoot\artwork" -skip_gameinfo -nocheat -inipath "$taskOut" -video none -sound none -nothrottle -noautoframeskip -frameskip 0 -str 95 -snapsize 400x254 -cfg_directory "$taskOut\cfg" -nvram_directory "$taskOut\nvram" -snapshot_directory "$taskOut\snap" -autoboot_script "$taskRoot\mk2ks_native_cpu_square_locks_v3000.lua" 2>&1 | Out-File -LiteralPath "$taskOut\run.log" -Encoding utf8
    $taskExit=$LASTEXITCODE
    foreach($taskFile in $taskSources){if((Get-FileHash -LiteralPath $taskFile).Hash -ne $taskHashes[$taskFile]){throw 'Executed input changed'}}
    [ordered]@{exit_code=$taskExit;candidate=$taskCandidate;executable_sha256=$taskBuild.executable_sha256;payload_sha256=$taskBuild.payload_sha256;
        player='kano';boot_frame=613;confirm_age=264;approach='guard_until_close';policy='jump_guard';cpu_slot=2;human_slot=1;
        assistance='none';cheats_enabled=$false;passed=$false;input_hashes=$taskHashes;snapshot_schema=2;
        scope='Fresh current CPU Square capture; original physical inputs/native observer chain retained, independent verification pending'} |
        ConvertTo-Json -Depth 5 | Out-File -LiteralPath "$taskOut\result.json" -Encoding utf8
    Write-Output "$CaseName terminal exit=$taskExit; collision-free snapshots recorded"
}finally{
    Pop-Location
    Get-ChildItem Env: | Where-Object Name -match '^(MK2KS_|MK2_TRACE_|MK2_RANGE_|MK2_P2_)' | Remove-Item
    foreach($taskName in $taskSaved.Keys){Set-Item -LiteralPath "Env:$taskName" -Value $taskSaved[$taskName]}
}
