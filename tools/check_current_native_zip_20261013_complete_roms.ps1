$ErrorActionPreference='Stop'
$taskScript=Get-Content -LiteralPath (Join-Path $PSScriptRoot 'check_current_native_zip_20261013.ps1') -Raw
$taskScript=$taskScript.Replace("'release_current_native_playtest_20261013'","'release_current_native_playtest_20261013_complete_roms'")
$taskScript=$taskScript.Replace('MK2_Kano_Sonya_CURRENT_NATIVE_PLAYTEST_20261013.zip','MK2_Kano_Sonya_CURRENT_NATIVE_PLAYTEST_20261013_complete_roms.zip')
$taskScript=$taskScript.Replace('9481CF6938EF23CBBA58101C3E0118B137E3005C7A04E9CB0E95B4E3362B8842','EDAC17A71DC7353ABC35C32D914E8248DB7804DCA6F9AA3A24B9B25EDF2797B7')
$taskScript=$taskScript.Replace('audit_current_native_zip_portable_check_20261013','audit_current_native_zip_portable_check_20261013_complete_roms')
Invoke-Expression $taskScript
