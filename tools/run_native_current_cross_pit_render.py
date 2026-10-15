"""Current repaired guest: complete original native cross-Pit scene in RAM.

Historical audio captures are frozen physical-input references ONLY, not
current audio acceptance. All original live raster/movie/phase-ground and
independently measured stock shadow-schedule predicates remain mandatory.
"""
import argparse
import code
import inspect
import json
import traceback
from pathlib import Path
import run_current_cross_pit_render_ram_v5905 as previous
import current_pit_shadow_schedule_bindings_v5932 as contract
import prepare_native_cross_tomb_19_audio_manifest_checked as prepared
import native_process_census_v6647 as census
import native_ram_raster_review as review

ROOT, need, sha = prepared.ROOT, prepared.need, prepared.sha
RAM = {}
HISTORICAL = ROOT / 'audit_v5899_current_cross_pit_winner_mix_checked/report.json'


def paths(fighter, side):
    need(fighter in ('kano', 'sonya') and side in (1, 2), 'Exact true character and physical slot')
    leaf = f'audit_native_current_cross_pit_{fighter}_p{side}_render'
    return ROOT / (leaf + '_ram'), ROOT / (leaf + '_checked')


def initialize(fighter, side):
    need(not census.census(), 'Never replace an existing native campaign')
    source = prepared.functions()['source_guard']()
    historical = json.loads(HISTORICAL.read_text())
    need(historical['passed'] and len(historical['cases']) == 4,
         'Original complete physical Pit reference remains available, not current sound acceptance')
    pins = dict(historical['inputHashes'])
    pins[str(HISTORICAL)] = sha(HISTORICAL)
    for winner in ('kano', 'sonya'):
        for slot in (1, 2):
            path = ROOT / f'audit_v5936_current_{winner}_p{slot}_pit_stock_shadow_scene_checked/report.json'
            proof = json.loads(path.read_text())
            need(proof['passed'] and proof['wholeNativePitShadowPolicyAccepted'] and
                 len(proof['nativeScene']['actualMovieFaultsRejected']) == 31 and
                 len(proof['nativeScene']['actualNativePhaseGroundFaultsRejected']) == 6 and
                 len(proof['nativeScene']['actualNativePitShadowPolicy']['actualShadowPolicyFaultsRejected']) == 5,
                 'Whole original phase-floor and independently proven stock Pit shadow contract retained')
            for name, digest in proof['inputHashes'].items():
                need(name not in pins or pins[name] == digest, 'Consistent historical source pins')
                pins[name] = digest
            pins[str(path)] = sha(path)
    need(all(sha(path) == digest for path, digest in pins.items()), 'All historical positive/failure/source inputs frozen')
    repaired = prepared.original.repaired
    leaf = f'audit_native_current_cross_pit_{fighter}_p{side}_render'
    namespace = dict(vars(repaired), __file__=__file__, INIT=ROOT / (leaf+'_initializer'),
                     OLD_INIT=ROOT / (leaf+'_previous_initializer'))
    exec(compile(inspect.getsource(repaired.expectation), __file__+'::whole_current_independent_initializer', 'exec'), namespace)
    guest, gfx, build, current = namespace['expectation']()
    RAM.update(guest=guest, gfx=gfx, build=build, source=source,
               referencePins=pins, historical=historical, images={})
    return current


def scene_contract(scene, log, guest, payload, fighter, side, reference, ids):
    need(not getattr(scene, 'retainedLivePipelinePassedBeforeErroneousGroundGate', False),
         'Fresh current capture must execute EVERY original live pipeline gate, never retrospective substitutes')
    proof = contract.scene_contract(scene, log, guest, payload, fighter, side, reference, ids)
    proof.update(origin=scene.groups['FLOOR_BEGIN'][0]['origin'],
                 retired=scene.groups['FLOOR_RETIRED'][0]['frame'],
                 currentLiveContinuousPipelineAccepted=True,
                 historicalReferenceIsPhysicalInputOnly=True, currentPitAudioWaveformAccepted=False)
    return proof


def functions(current):
    namespace = dict(previous.run.__globals__, __file__=__file__, __doc__=__doc__,
                     NAME=current.NAME, current=current, paths=paths, RAM=RAM, census=census,
                     scene_contract=scene_contract)
    exec(compile(inspect.getsource(previous.controls), __file__+'::whole_passive_Pit_controls', 'exec'), namespace)
    exec(compile(inspect.getsource(previous.preflight), __file__+'::whole_Pit_model_and_proxy_preflight', 'exec'), namespace)
    body = previous.run.source
    once = prepared.original.once
    body = once(body, "'-samplepath',str(ROOT/'samples')",
                "'-samplepath',str(candidate/'samples')+';'+str(ROOT/'samples')")
    body = once(body, "'-samples','-artpath'", "'-samples','-wavwrite','NUL','-artpath'")
    body = once(body, "    files.update(Path(p)for p in graphics_pins)",
                "    files.update(Path(p)for p in graphics_pins)\n"
                "    files.update(Path(p)for p in RAM['referencePins'])\n"
                "    files.add(prepared.SOURCE/'report.json')")
    body = once(body, 'scene=model.Model(guest,payload,image,ids);transport=model.Transport();errors=[];rgb_records=[];ram_guest=None',
                'scene=model.Model(guest,payload,image,ids);transport=model.Transport();errors=[];rgb_records=[];ram_guest=None\n'
                '    RAM.update(scene=scene,transport=transport,folder=CASE,output=OUT,errors=errors,rgb_records=rgb_records)')
    body = once(body, "        (CASE/'process.json').write_text(",
                "        actual=None\n"
                "        for _ in range(100):\n"
                "            actual=next((r for r in census.census()if r['ProcessId']==process.pid),None)\n"
                "            if actual or process.poll()is not None:break\n"
                "            time.sleep(.02)\n"
                "        need(actual and actual['ParentProcessId']==os.getpid()and "
                "Path(actual['ExecutablePath']).resolve()==(candidate/'mkport_candidate.exe').resolve(),"
                "'Actual current native Pit birth/path/parent/command')\n"
                "        RAM['identity']=actual\n"
                "        (CASE/'native_identity.json').write_text(json.dumps(actual,indent=2)+'\\n')\n"
                "        (CASE/'process.json').write_text(")
    body = once(body, "                            if not errors:scene.rgb[row['file']]=rgb",
                "                            frame=int(re.fullmatch(r'display_(\\d+)\\.png',row['file'])[1])\n"
                "                            begins=scene.groups['FLOOR_BEGIN'];retired=scene.groups['FLOOR_RETIRED'];lookups=scene.groups['FLOOR_PIT_LOOKUP']\n"
                "                            selected=bool(begins and frame-begins[0]['origin']in(1,32,90,128,256,384,480))\n"
                "                            selected=selected or bool(lookups and frame-lookups[0]['frame']in(2,5,8,11,14))\n"
                "                            selected=selected or bool(len(lookups)==2 and frame-lookups[1]['frame']==2)\n"
                "                            selected=selected or bool(retired and frame-retired[0]['frame']in(0,1,8,15,30))\n"
                "                            if selected:RAM['images'][frame]=rgb.copy()\n"
                "                            need(len(RAM['images'])<=18,'Bounded original physical/cinematic/retirement Pit rasters')\n"
                "                            if not errors:scene.rgb[row['file']]=rgb")
    body = once(body, "    (CASE/'result.json').write_text(",
                "    RAM['terminal']=terminal\n    (CASE/'result.json').write_text(")
    body = once(body, "'Actual complete current four-case unpressed native state/audio proof'",
                "'Historical complete physical Pit reference only; current sound acceptance remains false'")
    namespace['prepared'] = prepared
    exec(compile(body, __file__+'::whole_original_live_Pit_pipeline_current_guest', 'exec'), namespace)
    return namespace


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--fighter', choices=('kano', 'sonya'), required=True)
    parser.add_argument('--side', type=int, choices=(1, 2), required=True)
    args = parser.parse_args()
    folder, output = paths(args.fighter, args.side)
    need(not folder.exists() and not output.exists(), 'Fresh immutable actual current Pit run')
    try:
        current = initialize(args.fighter, args.side)
        scope = functions(current)
        report = scope['run'](args.fighter, args.side)
        report.update(currentPitAudioWaveformAccepted=False, historicalSoundReferenceIsPhysicalInputOnly=True,
                      originalPhaseGroundAndStockShadowContractSHA256=contract.CONTRACT_SOURCE_SHA256)
        RAM['report'] = report
    except Exception as error:
        report = dict(passed=False, error=repr(error), traceback=traceback.format_exc(),
                      fullPortAcceptance=False, currentPitAudioWaveformAccepted=False, goalStatus='active')
        print(json.dumps(report), flush=True)
    need(not output.exists(), 'Never overwrite current Pit outcome')
    output.mkdir()
    (output / 'report.json').write_text(json.dumps(report, indent=2)+'\n')
    if report['passed']:
        print(json.dumps({k:v for k,v in report.items() if k not in ('inputHashes', 'nativeScene')}, indent=2), flush=True)
        RAM['server'] = review.start(RAM['images'], folder)
    code.interact(banner='Same current native Pit capture; bounded original RGB remains in RAM.', local=dict(RAM=RAM))
