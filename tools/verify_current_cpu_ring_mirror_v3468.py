"""Current3172 repeated CPU Ring state and first complete native Ring raster/erase.

Original capture/raster/health/state contracts remain exact; only immutable
snapshot addressing and current independently assembled build are adapted.
Not all CPU contexts/arenas/KO/audio or full-port acceptance.
"""
import inspect,json,sys,subprocess
from pathlib import Path
import verify_current_cpu_square_v3280 as current
import current_cpu_capture_contract_v3270 as snapshots
import verify_native_cpu_ring_render_v2983 as render
import verify_native_cpu_ring_erase_v2985 as erase

ROOT=current.ROOT;need=current.need;sha=current.assembly.sha
CASE=ROOT/'audit_v3467_current_cpu_ring_sonya'
OUT=ROOT/'audit_v3469_current_cpu_ring_mirror_checked'

def matched_adapter():
    source=inspect.getsource(render.matched)
    before="if Path(file).suffix in ('.lua','.ps1','.json'):pin(folder/'input_sources'/Path(file).name,wanted)"
    after="if Path(file).suffix in ('.lua','.ps1','.json'):pin_snapshot(folder,file,wanted,pin)"
    need(source.count(before)==1,'Exact single original snapshot-address adaptation')
    namespace=dict(vars(render));namespace['pin_snapshot']=snapshots.pin_snapshot
    exec(compile(source.replace(before,after),__file__+'::original_matched_snapshot_address_only','exec'),namespace)
    original=namespace['matched']
    def matched(folder,key,pins,guest,payload):
        meta=json.loads((folder/'result.json').read_text(encoding='utf-8-sig'))
        need(meta['snapshot_schema']==2 and meta['raw_audio_files_written']==0
             and meta['new_builds_or_rom_copies']==0,'Actual compressed hierarchy runner, no build/WAV copies')
        runner=(ROOT/'tools/run_current_cpu_ring_v3429.ps1').read_text()
        need('-nocheat' in runner and '-noautoframeskip -frameskip 0' in runner
             and '-wavwrite' not in runner and 'MK2KS_DIAGNOSTIC_CPU_ID' not in runner,
             'Ordinary physical controls only, no prescribed CPU/AI/HP/RNG')
        return original(folder,key,pins,guest,payload)
    return matched

def main():
    need(not OUT.exists(),'Immutable current Ring proof')
    expected=current.expected_current()
    candidate=ROOT/current.current.CANDIDATE
    need(sha(candidate/'mkport_candidate.exe')==current.current.EXE
         and (candidate/'roms/mk2ks/mk2ks.mdata').read_bytes()==expected[2],
         'Actual current matched playable pair and whole independently reconstructed payload')
    current.assembly.NAME=current.current.CANDIDATE
    current.assembly.expected=lambda:expected
    render.matched=matched_adapter()
    prior_path=ROOT/'audit_v2972_native_cpu_ring_checked/report.json'
    prior=json.loads(prior_path.read_text())
    need(prior['passed'],'Retained actual earlier CPU Ring trajectory, not current acceptance')
    scene=render.verify(CASE,'new_sonya',prior,expected[0],expected[2])
    need(scene['passed'] and scene['allRetainedScenesExact']
         and scene['originalPhysicalTrajectoryUnchanged'],'Full original Ring state/phase/art/palette/shadow/raster contracts')
    log=(CASE/'run.log').read_text(encoding='utf-8-sig')
    phases=render.phases.ring_contract.verify(log,expected[0],'sonya')
    health,rounds=render.phases.health_ledger(log,expected[0],'sonya')
    state=render.phases.state_ledgers(log,expected[0],'sonya',rounds)
    need(scene['state']['blocked'] and scene['state']['damage']==6 and scene['sampledFrames']==87,
         'Actual native mirror guard/6chip and full87scene window, never substituted Kano hit')
    erase.source_contract();erased=erase.inspect(CASE,expected[0],current.current.CANDIDATE)
    need(erased['passed'] and erased['oneInitialBaseOnly'] and not erased['laterBuffersUsedAsAnchors']
         and erased['continuousExactFlips']==scene['sampledFrames'],
         'Every native continuous erase/prebuffer/flip from one initial base')
    pins={str(prior_path.resolve()):sha(prior_path)}
    for table in (scene['inputHashes'],erased['inputHashes'],current.assembly.source_check()):
        for file,digest in table.items():
            key=str(Path(file).resolve());need(key not in pins or pins[key]==digest,'Consistent immutable relevant pin')
            pins[key]=digest
    for module in tuple(sys.modules.values()):
        file=getattr(module,'__file__',None)
        if file and Path(file).suffix=='.py' and Path(file).resolve().is_relative_to(ROOT/'tools'):
            pins[str(Path(file).resolve())]=sha(file)
    for file,digest in pins.items():need(sha(file)==digest,'Every source/capture/actual-runtime byte unchanged')
    value=dict(passed=True,candidate=current.current.CANDIDATE,case=str(CASE),human='sonya',
        independentWholeCurrentGuestAndPayloadAccepted=True,originalPhysicalAndNativeTrajectoryUnchanged=True,
        repeatedRingPhases=phases,wholeNativeHealth=health,wholeNativeStateLedger=state,
        sampledFrames=scene['sampledFrames'],exactScreenPixels=scene['exactScreenPixels'],
        nativeShadowCopies=scene['nativeShadowCopies'],sourceBoundProjections=scene['sourceBoundProjections'],
        continuousExactFlips=erased['continuousExactFlips'],oneInitialBaseOnly=True,
        firstCompleteRingPhaseArtShadowEraseAccepted=True,allRepeatedRingArtAccepted=False,
        allCPUContextsArenasKOOverlapAudioAccepted=False,specificCurrentCounterexamplesPending=True,
        gameOrPublicPlayableChanged=False,rawAudioFilesWritten=0,newBuildsOrROMCopies=0,
        fullPortAcceptance=False,scene=scene,erase=erased,inputHashes=pins)
    OUT.mkdir();path=OUT/'report.json';path.write_text(json.dumps(value,indent=2)+'\n');digest=sha(path)
    compressed=subprocess.run(['compact.exe','/C','/I','/Q',str(path)],capture_output=True,text=True)
    need(compressed.returncode==0 and sha(path)==digest,'Lossless report compression')
    print(json.dumps({k:v for k,v in value.items()if k not in ('scene','erase','inputHashes','repeatedRingPhases','wholeNativeHealth','wholeNativeStateLedger')},indent=2),flush=True)

if __name__=='__main__':main()
