"""Read-only reset-path coverage; deliberately not a runtime audio acceptance gate."""
import json
import re
import verify_native_source_sync as sync

sync.verify()
root = sync.ROOT/'mame-mkp/src'
samples = root/'devices/sound/samples.cpp'
driver = root/'mame/midway/midtunit.cpp'
machine = root/'mame/midway/midtunit_m.cpp'


def body(source, name):
    match = re.search(r'void samples_device::'+name+r'\([^)]*\)\s*\{([^}]*)\}', source)
    assert match, name
    return match[1]


def gate(source, configuration):
    assert 'stop_all();' in body(source, 'device_reset')
    all_channels = body(source, 'stop_all')
    assert 'channel < m_channels' in all_channels and 'stop(channel);' in all_channels
    stop = body(source, 'stop')
    assert 'chan.source = nullptr;' in stop and 'chan.source_num = -1;' in stop
    assert 'm_mk2ks_voices->set_channels(19);' in configuration


source = samples.read_text()
configuration = driver.read_text()
gate(source, configuration)
for old in ('stop_all();', 'stop(channel);', 'chan.source = nullptr;'):
    changed = source.replace(old, '/* removed by mutation */', 1)
    try:
        gate(changed, configuration)
    except AssertionError:
        pass
    else:
        raise AssertionError('Reset-path mutation accepted: '+old)
report = dict(sourceResetPathVerified=True, configuredChannels=list(range(19)),
              deviceResetCallsStopAll=True, everyChannelSourceCleared=True,
              sourceSHA256={str(p.relative_to(sync.ROOT)):sync.sha(p)
                            for p in (samples,driver,machine)},
              runtimeResetDuringActiveCueProven=False,
              sceneChangeCleanupProven=False, muteInterruptionProven=False,
              newEmulatorRuns=0, fullPortAccepted=False,
              scope='Current source call chain only. Does not prove compiled samples.cpp provenance or runtime interruption timing.')
out = sync.ROOT/'audit_current_samples_reset_source'
assert not out.exists()
out.mkdir()
(out/'report.json').write_text(json.dumps(report, indent=2))
print(json.dumps(report, indent=2))
