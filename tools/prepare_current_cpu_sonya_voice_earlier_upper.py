"""Only shift physical HP seven fields earlier; no runtime launch."""
import json,difflib
import verify_native_source_sync as sync
sync.verify();R=sync.ROOT
base=R/'audit_current_cpu_sonya_voice_late_upper_preparation'
out=R/'audit_current_cpu_sonya_voice_earlier_upper_preparation';assert not out.exists()
old=(base/'campaign.lua').read_text();s=old
assert s.count('age>=56 and age<62')==2
s=s.replace('age>=56 and age<62','age>=49 and age<55')
assert s.replace('age>=49 and age<55','age>=56 and age<62')==old
assert ':write_' not in s and ':snapshot(' not in s
out.mkdir();lua=out/'campaign.lua';lua.write_text(s)
runner=(base/'run.ps1').read_text().replace(base.name+'/campaign.lua',out.name+'/campaign.lua').replace(sync.sha(base/'campaign.lua'),sync.sha(lua)).replace('audit_current_cpu_sonya_voice_late_upper_runtime','audit_current_cpu_sonya_voice_earlier_upper_runtime')
(out/'run.ps1').write_text(runner)
report=dict(preparedNotRun=True,LuaSHA256=sync.sha(lua),priorLuaSHA256=sync.sha(base/'campaign.lua'),onlyChange='Physical HP condition and matching diagnostic flag ages56..61→49..54; all other controller/observer/runner limits unchanged.',evidence='Late trial firstHP1746/age56→nativeupper2631752 (6fields). Human647/CPU710 gap63 missed. ProposedHP1739→expected1745 closer descending window; no trajectory/contact assumed.',sentinel='Do not gate source_num>=0: unchanged sample backend may retain -1 while actual source advances. Require owner/marker, positive advancing pos below length and cleanup beforeEOF.',scope='Actual CPU health-change interruption only; not heard mix, allCPU, wholeport.',sourceDiff=''.join(difflib.unified_diff(old.splitlines(True),s.splitlines(True))),fullPortAccepted=False)
(out/'source.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(dict(preparation=str(out),LuaSHA256=sync.sha(lua),preparedNotRun=True)))
