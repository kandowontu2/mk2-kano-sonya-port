"""Fresh sole-emulator execution of preserved, previously unreached physical tactic."""
import verify_native_source_sync as sync
sync.verify()
base=sync.ROOT/'audit_current_sonya_p1_kintaro_close_retreat_preparation'
out=sync.ROOT/'audit_current_sonya_p1_kintaro_close_retreat_solo_preparation'
assert not out.exists()
assert sync.sha(base/'campaign.lua')=='7A18F13D78491B657FEFDA16BB3FE12D260DFBF77E77B7DEC775BBC8B7A7DC1D'
out.mkdir();lua=out/'campaign.lua';lua.write_bytes((base/'campaign.lua').read_bytes())
assert sync.sha(lua)==sync.sha(base/'campaign.lua')
runner=(base/'run.ps1').read_text().replace(base.name+'/campaign.lua',out.name+'/campaign.lua').replace('audit_current_sonya_p1_kintaro_close_retreat_runtime','audit_current_sonya_p1_kintaro_close_retreat_solo_runtime')
(out/'run.ps1').write_text(runner)
print('Same preserved Lua SHA; fresh sole-emulator case; previously unreached strategy, not failed-outcome repeat;180sec/320MiB/10MiB')
