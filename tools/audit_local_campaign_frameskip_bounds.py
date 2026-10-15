"""Local option/setter constraints; no runtime performance or visual claim."""
import json
import verify_native_source_sync as sync
sync.verify()
root=sync.ROOT;out=root/'audit_local_campaign_frameskip_bounds_checked'
assert not out.exists()
paths={k:root/v for k,v in {'header':'mame-mkp/src/emu/video.h','video':'mame-mkp/src/emu/video.cpp','options':'mame-mkp/src/emu/emuopts.cpp','lua':'mame-mkp/src/frontend/mame/luaengine.cpp','runner':'audit_current_kano_p2_campaign_frontier_observer_preparation/run.ps1'}.items()}
s={k:p.read_text() for k,p in paths.items()}
def verify(d):
    assert 'constexpr int FRAMESKIP_LEVELS = 12;' in d['header']
    assert 'constexpr int MAX_FRAMESKIP = FRAMESKIP_LEVELS - 2;' in d['header']
    assert 'm_frameskip_level = std::min<int>(frameskip, MAX_FRAMESKIP);' in d['video']
    assert 'OPTION_FRAMESKIP ";fs(0-10)"' in d['options']
    assert 'video_type["frameskip"] = sol::property(&video_manager::frameskip, &video_manager::set_frameskip);' in d['lua']
    assert "'-frameskip','10'" in d['runner']
verify(s)
faults=[]
for label,key,old,new in [('wrong_maximum','header','FRAMESKIP_LEVELS - 2','FRAMESKIP_LEVELS - 1'),('removed_clamp','video','std::min<int>(frameskip, MAX_FRAMESKIP)','frameskip')]:
    bad=dict(s);bad[key]=bad[key].replace(old,new)
    try:verify(bad)
    except AssertionError:faults.append(label)
    else:raise AssertionError('Unsupported frameskip assumption accepted')
report=dict(passedLocalSourceChecks=True,normalMaximumFrameskip=10,currentRunnerFrameskip=10,normalSetterElevenWouldClampToTen=True,runtimeElevenTestNeeded=False,uiFastForwardIsSeparatePath=True,performanceImprovementProven=False,sourceSHA256={k:sync.sha(p) for k,p in paths.items()},rejectedFaults=faults,fullPortAccepted=False)
out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
