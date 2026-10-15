"""Four actually earned rare Tomb mirror drops, not full-stage/port acceptance.

Reuse terminal native captures. Preserve the entire original renderer, native
earned/branch/motion contracts, actual counterexamples and audio exclusions.
"""
import json, subprocess
from pathlib import Path
import run_remaining_random_drop_mirror_render_ram_v4465 as remaining
ROOT, need, sha = remaining.ROOT, remaining.need, remaining.sha
OUT = ROOT / 'audit_v4469_both_characters_both_slots_unpressed_random_mirror_tomb_render'
CONTEXTS = (('kano',1,10), ('sonya',1,4), ('kano',2,2), ('sonya',2,11))

def main():
    need(not OUT.exists(), 'Fresh immutable aggregate proof, never rerun completed native scenes')
    pins = {}
    def pin(path, wanted=None):
        path = Path(path).resolve(); key = str(path); actual = sha(path)
        need((wanted is None or actual == wanted) and (key not in pins or pins[key] == actual),
             'Exact consistent executed sources and terminal evidence')
        pins[key] = actual
    pin(__file__)
    query = "Get-CimInstance Win32_Process -Filter \"Name='python.exe' OR Name='mkport_candidate.exe'\" | Where-Object { $_.CommandLine -match 'run_remaining_random_drop_mirror_render_ram_v4465.py|audit_v4466_' } | Select-Object ProcessId,Name,CommandLine | ConvertTo-Json -Compress"
    live = subprocess.run(['powershell.exe','-NoProfile','-Command',query],capture_output=True,text=True)
    need(live.returncode == 0 and not live.stdout.strip(), 'All actual native render jobs terminal')
    guest = remaining.runtime.audio.old.expected()
    cases = []
    for fighter,side,delay in CONTEXTS:
        if (fighter,side) == ('kano',1):
            folder,output = remaining.runtime.CASE,remaining.runtime.OUT
            accepted = 'current3836KanoP1RandomDropMirrorNativeTombWholeRenderPaletteShadowEraseAccepted'
        else:
            folder,output = remaining.paths(fighter,side)
            accepted = 'current3836RandomDropMirrorNativeTombWholeRenderPaletteShadowEraseAccepted'
        path = output / 'report.json'; report = json.loads(path.read_text()); pin(path)
        proofpath = ROOT / f'audit_v4459_tomb_mirror_random_drop_checked/{fighter}_p{side}_delay{delay:02d}/report.json'
        proof = json.loads(proofpath.read_text()); pin(proofpath)
        identity = 17 if fighter == 'kano' else 18
        need(report['passed'] and report[accepted] and report['candidate'] == remaining.runtime.NAME and
             report['fighter'] == proof['fighter'] == fighter and report['side'] == proof['side'] == side and
             report['truePhysicalIDs'] == [identity,identity] and proof['passed'] and
             proof['physicalCommandDelay'] == delay and proof['nativeRandomDropStateAndOriginal801CleanupAccepted'],
             'Actual selected character, physical slot and qualified rare command timing')
        for value in (report,proof):
            for p,h in value['inputHashes'].items(): pin(p,h)
        scene = report['nativeScene']; branch = report['nativeBranch']
        need(branch == proof['nativeBranch'] and branch['nativeDrop'] and
             scene['nativeDrop'] and scene['nativeInputState'] == branch['earnedContract'] and
             scene['nativeMotion'] == branch['nativeMotion']['phase'] and
             scene['actualNativeRandomValue'] == branch['actualNativeRandomValue'] < 50 and
             branch['nativeMotion']['phase']['checkedConsecutiveCallbacks'] == 269 and
             branch['earnedContract']['consecutive_fields'] == 801,
             'Complete original earned native rare branch and full269 motion, not held/pressed substitution')
        need(len(proof['actualOriginalFullEarnedFaultsRejected']) == 12 and
             len(proof['actualOriginalBranchPCActorMainIOFaultsRejected']) == 4 and
             len(proof['actual269PhaseFaultsRejected']) == 4 and
             {r['kind'] for r in report['actualPixelFaultsRejected']} == {'VRAM target bit','visible RGB bit'},
             'All original actual negative earned/branch/phase/whole-render controls retained')
        log = (folder / 'run.log').read_text()
        need(remaining.runtime.branches.branch(log,guest,fighter,side) == branch and
             len(remaining.runtime.native.actual_faults(log,fighter,side,guest)) == 12 and
             len(remaining.runtime.branches.faults(log,guest,fighter,side)) == 4,
             'Recheck actual native branch, earned and task/PC/IO counterexamples on frozen full-scene capture')
        terminal = json.loads((folder / 'result.json').read_text())
        need(terminal['captureCompleted'] and terminal['exit_code'] == 0 and not terminal['modelErrors'] and
             terminal['modelExactFields'] == terminal['observedRGBFields'] == report['sampledFrames'] and
             terminal['guest_writes'] == 0 and terminal['assistance'] == 'none' and not terminal['cheats_enabled'],
             'Actual terminal full source-model run, no assistance or omitted failed scenes')
        need(report['sampledFrames'] == scene['retired'] - scene['origin'] + 30 > 500 and
             report['exactRGBPixels'] == report['sampledFrames'] * 400 * 254 and
             report['oneInitialBaseOnly'] and report['laterTargetsNeverUsedAsAnchors'] and
             report['nativeMirrorPaletteSelectors'] == {'1':[False],'2':[True]} and
             report['nativeShiftLoads'] == report['nativeShiftFills'] > 0 and
             report['fullPhysicalPaletteChecks'] > report['sampledFrames'] and scene['nativeShadowCopies'] > 0 and
             all(int(scene['ownedBodyDispatches'][str(s)]) > 100 for s in (1,2)),
             'Whole retirement+30 scene, exact source palette/body/ground/native shadow/erase model')
        need(report['sourcePreflight']['observerSHA256'] == remaining.runtime.controls() and
             report['sourcePreflight']['modelSHA256'] == remaining.runtime.model.MODEL_SOURCE_SHA256 and
             report['rawImageAudioVRAMROMCopiesWritten'] == 0 and not report['publicPlayableOrReleaseChanged'] and
             not report['fullPortAcceptance'] and not report['completeStageVictimAudioAccepted'] and
             not report['allMirrorBranchesAndSlotsAccepted'], 'Original renderer and explicit full-scope exclusions')
        if (fighter,side) != ('kano',1):
            _,digest = remaining.runner(fighter,side,delay)
            need(digest == report['entire4460RendererAdaptationSHA256'], 'Exact entire executed role-only renderer adaptation')
        cases.append(dict(fighter=fighter,side=side,physicalCommandDelay=delay,report=str(path),
                          stateReport=str(proofpath),capture=str(folder),frames=report['sampledFrames'],
                          nativeBranch=branch,nativeScene=scene,nativeMirrorPaletteSelectors=report['nativeMirrorPaletteSelectors']))
    need({(r['fighter'],r['side']) for r in cases} == {('kano',1),('sonya',1),('kano',2),('sonya',2)},
         'Both real character identities in both physical slots')
    need(all(sha(p) == h for p,h in pins.items()), 'Every actual original/aggregate evidence byte unchanged')
    return dict(passed=True,candidate=remaining.runtime.NAME,cases=cases,inputHashes=pins,
                priorCompletedNativeScenesNotRerun=True,actualTrueMirrorRenderContexts=4,
                actualWholeVisibleFields=sum(r['frames'] for r in cases),
                actualExactVisibleRGBPixels=sum(r['frames'] for r in cases)*400*254,
                actualRenderCounterexamplesRejected=8,
                current3836BothCharactersBothSlotsUnpressedRareMirrorTombWholeRenderPaletteShadowEraseAccepted=True,
                broaderPitTombVictimsAccepted=False,completeStageVictimAudioAccepted=False,
                publicPlayableOrReleaseChanged=False,rawImageAudioVRAMROMCopiesWritten=0,
                fullPortAcceptance=False,scope=__doc__)

if __name__ == '__main__':
    report = main()
    OUT.mkdir()
    need(subprocess.run(['compact.exe','/C','/I','/Q','/S:'+str(OUT)],capture_output=True).returncode == 0,
         'Aggregate text compressed before write')
    (OUT / 'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k not in ('inputHashes','cases')},indent=2),flush=True)
