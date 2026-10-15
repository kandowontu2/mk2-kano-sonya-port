"""Exact accepted laser-build/current secondary construction and audio transfer."""
import json,hashlib,copy
import verify_native_source_sync as sync
sync.verify();root=sync.ROOT;old=root/'diagnostic_native_kano_laser_audio';snapshot=old/'input_sources/mame-mkp/src/mame/midway'
current=root/'mame-mkp/src/mame/midway/midtunit_m.cpp';historical=snapshot/'midtunit_m.cpp'
a=current.read_text();b=historical.read_text();meta=json.loads((old/'build-info.json').read_text(encoding='utf-8-sig'))
assert meta['payload_sha256']==sync.sha(sync.BUILD/'roms/mk2ks/mk2ks.mdata')
def function(text,name):
    start=text.index('midtunit_state::'+name+'(');lo=text.rfind('\n',0,start)+1;opening=text.index('{',start);depth=1;end=opening+1
    while depth:depth+=(text[end]=='{')-(text[end]=='}');end+=1
    return text[lo:end]
start='// Typed native choreography for the missing eye laser and magenta orb.';end='void midtunit_state::init_mk2ks_native_selector()'
extract=lambda text:text[text.index(start):text.index(end,text.index(start))]
regions={'typed_secondary_visual_motion_victim_palette_emitters_button_action_cleanup':(extract(a),extract(b))}
for name in ['mk2ks_finish_audio_stop','mk2ks_finish_audio_start','mk2ks_finish_audio_frame','mk2ks_finish_audio_marker']:
    regions[name]=(function(a,name),function(b,name))
observed={};expected={};differences=[]
for name,(x,y)in regions.items():
    sha=hashlib.sha256(x.encode()).hexdigest();observed[name]=sha
    if x==y:expected[name]=sha
    else:differences.append(name)
backend=[]
for leaf in ['midtunit_v.cpp','midtunit_v.h']:
    now=root/'mame-mkp/src/mame/midway'/leaf;then=snapshot/leaf;assert now.read_bytes()==then.read_bytes();backend.append(dict(file=leaf,SHA256=sync.sha(now),wholeBytesExact=True))
def gate(check):assert check==expected
gate({k:observed[k]for k in expected});faults=[]
for name in expected:
    bad={k:observed[k]for k in expected};bad[name]='0'*64
    try:gate(bad)
    except AssertionError:faults.append(name)
    else:raise AssertionError('Changed dependency admitted')
reports=[]
for name in ['audit_native_kano_laser_cpu_motion_audio_review','audit_native_kano_laser_cpu_observed_audio_review']:
    p=root/name/'report.json';r=json.loads(p.read_text());assert r['passed'];reports.append(dict(report=str(p),SHA256=sync.sha(p),finiteAudioAccepted=r.get('finiteNativeLaserAudioAccepted',r.get('firstActualCPUWholeAudioAccepted')),runtimeCleanupAccepted=r.get('nativeSceneAudioCleanupAccepted',r.get('actualLaterTerminalAudioCleanupAccepted')),fullFinisherAccepted=r.get('fullFinisherAccepted'),wholeVisualRegressionAccepted=r.get('wholeNewVisualRegressionAccepted')))
out=root/'audit_current_secondary_laser_components_checked';assert not out.exists();out.mkdir()
report=dict(passed=True,exactNormalizedRegions={name:dict(equal=x==y,currentCharacters=len(x),historicalCharacters=len(y),currentSHA256=observed[name])for name,(x,y)in regions.items()},changedRegions=differences,wholeVideoDependencies=backend,payloadExact=True,retainedAcceptedNativeCPUAudioAndSceneCleanup=reports,effectiveDependencyFaultsRejected=faults,currentWholeSourceSHA256=sync.sha(current),historicalWholeSourceSHA256=sync.sha(historical),oldBuildInfoSHA256=sync.sha(old/'build-info.json'),finiteAudioComponentTransferAccepted=not differences,currentWholeSecondaryVisualFinisherAccepted=False,currentAllLoadedTypedRowsChecked=False,scope='Exact wholetyped secondaryvisual/motion/laser victim-palette/debris/button/action/cleanup construction and host4finish-audiofunctions compared, plus actualbackend/payloadsame. Accepted naturalCPU finitewholemix/nativecleanup retained, notreset. Historical fullFinisher andwholeNewVisualRegression werefalse; unchangedsource doesnot magically provide that missing authoredscene visual acceptance. No universalallinterrupt criterion, rawcollector, emulator or gameedit.',smallestRemainingVisualCheck='If required to close secondarycinematic visual acceptance: reuse accepted naturally earned CPUlaser physicalfixture oncurrentlong and inspect only nativecharge/beam/burst/postscene frames with≤4boundedPNGs; ownership/source/transport proofs retained. Requires explicitreview/mediaexception beforepreparationlaunch. Do notforceKanoAI or state and do notcollectwholeRAM/GFX/PCM.',fullPortAccepted=False)
(out/'report.json').write_text(json.dumps(report,indent=2));print(out);print('Changed:',differences)
