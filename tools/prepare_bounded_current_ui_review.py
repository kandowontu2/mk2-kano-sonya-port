"""Fresh physical CSS/ladder/fight review, at most eight PNGs per case."""
import json
import verify_native_source_sync as sync

sync.verify()
out=sync.ROOT/'audit_bounded_current_ui_review_preparation'
assert not out.exists();out.mkdir()
source=(sync.ROOT/'mk2ks_native_ui_flow_v2_probe.lua').read_text()
marker='local function snapshot(scene,age)\n'
assert source.count(marker)==1
source=source.replace(marker,"local captured=0\n"+marker+" if captured>=8 then return end\n if scene=='select' and not(age==66 or age==90 or age==108 or age==156 or age==228) then return end\n if scene=='transition' and not(age==2 or age==60) then return end\n if scene=='fight' and age>2 then return end\n captured=captured+1\n")
lua=out/'ui.lua';lua.write_text(source)
base=(sync.ROOT/'audit_bounded_interrupted_special_reactivation_preparation/run_square_p1.ps1').read_text()
for fighter in ('kano','sonya'):
    for side in (1,2):
        runner=base.replace('audit_bounded_interrupted_square_p1_reactivation_runtime',f'audit_bounded_current_ui_{fighter}_p{side}_runtime')
        runner=runner.replace('audit_bounded_interrupted_special_reactivation_preparation/square.lua',out.name+'/ui.lua')
        runner=runner.replace('9FB7CAE12E29C62DB432BEE543202C8E0D9F6F3D481A98A7CBB0950CE08C2EAC',sync.sha(lua))
        start=runner.index("$env:MK2KS_HUMAN_SPECIAL_MOVE=")
        end=runner.index('$taskArgs=',start)
        runner=runner[:start]+f"$env:MK2KS_UI_FIGHTER='{fighter}'\n$env:MK2KS_UI_SIDE='{side}'\n$env:MK2KS_UI_BOOT='604'\n"+runner[end:]
        runner=runner.replace("'-str','100'","'-str','65','-snapsize','400x254'")
        runner=runner.replace("rawMedia='none'","rawMedia='at most eight bounded PNGs; no video/audio recording'")
        (out/f'run_{fighter}_p{side}.ps1').write_text(runner)
(out/'report.json').write_text(json.dumps(dict(prepared=True,maximumPNGsPerCase=8,physicalInputsOnly=True,memoryLimitMiB=320,wallLimitSeconds=90,logLimitMiB=10)))
