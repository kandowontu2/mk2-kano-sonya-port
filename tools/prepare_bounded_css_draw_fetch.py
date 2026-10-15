"""Correct native prefetch address; retain zero-event predecessor evidence."""
import json
import verify_native_source_sync as sync
sync.verify()
old=sync.ROOT/'audit_bounded_css_draw_geometry_preparation'
out=sync.ROOT/'audit_bounded_css_draw_fetch_preparation';assert not out.exists();out.mkdir()
source=(old/'geometry.lua').read_text()
source=source.replace('install_read_tap(0xff804420,0xff80442f','install_read_tap(0xff804410,0xff80441f')
source=source.replace('at~=0xff804420','at~=0xff804410')
source=source.replace('age>=54 and age<=70 or age>=78 and age<=94 or age>=224 and age<=260','age==66 or age==90 or age==228')
source=source.replace('if id==17 or id==18 or id==1 or id==9 then','if true then')
lua=out/'fetch.lua';lua.write_text(source)
for side in (1,2):
 runner=(old/f'run_kano_p{side}.ps1').read_text()
 runner=runner.replace(old.name+'/geometry.lua',out.name+'/fetch.lua').replace(sync.sha(old/'geometry.lua'),sync.sha(lua))
 runner=runner.replace(f'audit_bounded_css_draw_geometry_kano_p{side}_runtime',f'audit_bounded_css_draw_fetch_kano_p{side}_runtime')
 (out/f'run_kano_p{side}.ps1').write_text(runner)
(out/'report.json').write_text(json.dumps(dict(prepared=True,nativeFetchAddress='FF804410',nativePC='FF804420',sampledAges=[66,90,228])))
