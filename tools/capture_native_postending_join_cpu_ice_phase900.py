"""Same genuine earned campaign, only ordinary coin/start delayed 300 fields."""
import code,json,traceback
from pathlib import Path
import capture_native_postending_join as base

if __name__=='__main__':
    previous=json.loads((base.ROOT/'audit_native_postending_kano_p2_sonya_cpu_ice/bounded_controller_result.json').read_text())
    base.need(previous['failedCampaignPreserved'] and previous['nativeExit']==0 and
              not previous['postEndingJoinAccepted'],'Prior actual bounded attempt is terminal and remains unsuccessful')
    base.OUT=base.ROOT/'audit_native_postending_kano_p2_sonya_cpu_ice_phase900'
    base.LUA='mk2ks_native_kano_p2_postending_sonya_cpu_ice.lua'
    base.CONTROLLERS=[base.LUA,'mk2ks_native_kano_p2_postending_sonya_defensive.lua',*base.CONTROLLERS,
                      'tools/capture_native_postending_join_cpu_ice_phase900.py']
    source=base.capture_source()
    before="MK2KS_TEST_BOOT_FRAME='600'"
    base.need(source.count(before)==1,'One original physical cold-boot environment')
    source=source.replace(before,"MK2KS_TEST_BOOT_FRAME='900'",1)
    base.capture_source=lambda:source
    try:capture=base.run()
    except Exception as error:
        if base.OUT.exists():
            path=base.OUT/'phase900_capture_failure.json';base.need(not path.exists(),'Immutable actual phase failure')
            path.write_text(json.dumps(dict(passed=False,error=repr(error),traceback=traceback.format_exc()),indent=2)+'\n')
        raise
    code.interact(banner='Same terminal phase900 ordinary-input campaign; original ending and post-ending join remain required.',local=dict(capture=capture))
