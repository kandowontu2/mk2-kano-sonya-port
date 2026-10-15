"""Current repaired guest: entire original cross-Tomb native render replay.

Use the actual current19 audio matrix as physical-input/branch reference.
Retain the whole one-base CPU/DMA/VRAM/palette/body/shadow/erase model.
Only bounded original RGB fields remain in RAM for individual visual review.
"""
import argparse
import code
import inspect
import json
import traceback
from pathlib import Path
from types import SimpleNamespace
import run_current_cross_tomb_render_ram_v5847 as previous
import prepare_native_cross_tomb_19_audio_manifest_checked as prepared
import native_process_census_v6647 as census
import native_ram_raster_review as review

ROOT, need, sha = prepared.ROOT, prepared.need, prepared.sha
MATRIX = ROOT / 'audit_native_cross_tomb_19_audio_matrix_checked/report.json'
RAM = {}


def paths(fighter, side):
    need(fighter in ('kano', 'sonya') and side in (1, 2), 'Exact true fighter and physical slot')
    return (ROOT / f'audit_native_current_cross_tomb_{fighter}_p{side}_render_ram',
            ROOT / f'audit_native_current_cross_tomb_{fighter}_p{side}_render_checked')


def initialize(fighter, side):
    need(not census.census(), 'Never replace an existing native test')
    source = prepared.functions()['source_guard']()
    matrix = json.loads(MATRIX.read_text())
    need(matrix['passed'] and len(matrix['cases']) == 4 and matrix['totalSampleChannels'] == 19 and
         matrix['guestSHA256'] == source['guestSHA256'] and
         all(sha(p) == h for p, h in matrix['inputHashes'].items()), 'Whole completed current sound/branch reference frozen')
    repaired = prepared.original.repaired
    leaf = f'audit_native_current_cross_tomb_{fighter}_p{side}_render'
    scope = dict(vars(repaired), __file__=__file__, INIT=ROOT / (leaf + '_initializer'),
                 OLD_INIT=ROOT / (leaf + '_previous_initializer'))
    exec(compile(inspect.getsource(repaired.expectation), __file__ + '::whole_current_independent_initializer', 'exec'), scope)
    guest, gfx, build, current = scope['expectation']()
    RAM.update(guest=guest, gfx=gfx, build=build, matrix=matrix, source=source, images={})
    return current


def functions(current):
    timing = SimpleNamespace(source=SimpleNamespace(OUT=prepared.SOURCE))
    namespace = dict(previous.run.__globals__, __file__=__file__, __doc__=__doc__,
                     NAME=current.NAME, current=current, timing=timing, RAM=RAM, paths=paths, census=census)
    controls = previous.controls.source
    exec(compile(controls, __file__ + '::whole_current_passive_controls', 'exec'), namespace)
    exec(compile(previous.preflight.source, __file__ + '::whole_current_tuple_and_render_preflight', 'exec'), namespace)
    body = previous.run.source
    once = prepared.original.once
    body = once(body, 'audit_v5843_current_cross_tomb_audio_checked/report.json', MATRIX.relative_to(ROOT).as_posix())
    body = once(body, "'-samplepath',str(ROOT/'samples')",
                "'-samplepath',str(candidate/'samples')+';'+str(ROOT/'samples')")
    body = once(body, "'-samples','-artpath'", "'-samples','-wavwrite','NUL','-artpath'")
    body = once(body, 'scene=model.Model(guest,payload,image,ids);transport=model.Transport();errors=[];rgb_records=[];ram_guest=None',
                "scene=model.Model(guest,payload,image,ids);transport=model.Transport();errors=[];rgb_records=[];ram_guest=None\n"
                "    RAM.update(scene=scene,transport=transport,folder=CASE,output=OUT,errors=errors,rgb_records=rgb_records)")
    body = once(body, "        (CASE/'process.json').write_text(",
                "        actual=None\n"
                "        for _ in range(100):\n"
                "            actual=next((r for r in census.census()if r['ProcessId']==process.pid),None)\n"
                "            if actual or process.poll()is not None:break\n"
                "            time.sleep(.02)\n"
                "        need(actual and actual['ParentProcessId']==os.getpid()and "
                "Path(actual['ExecutablePath']).resolve()==(candidate/'mkport_candidate.exe').resolve(),"
                "'Actual native render birth/path/parent/command')\n"
                "        RAM['identity']=actual\n"
                "        (CASE/'native_identity.json').write_text(json.dumps(actual,indent=2)+'\\n')\n"
                "        (CASE/'process.json').write_text(")
    body = once(body, "                            if not errors:scene.rgb[row['file']]=rgb",
                "                            frame=int(re.fullmatch(r'display_(\\d+)\\.png',row['file'])[1])\n"
                "                            begins=scene.groups['FLOOR_BEGIN'];retired=scene.groups['FLOOR_RETIRED']\n"
                "                            if begins and (frame-begins[0]['origin']in(1,32,90,128,256,384,480)or "
                "(retired and frame-retired[0]['frame']in(0,1,15,30))):RAM['images'][frame]=rgb.copy()\n"
                "                            need(len(RAM['images'])<=11,'Bounded individual original native raster review')\n"
                "                            if not errors:scene.rgb[row['file']]=rgb")
    body = once(body, "    (CASE/'result.json').write_text(",
                "    RAM['terminal']=terminal\n    (CASE/'result.json').write_text(")
    exec(compile(body, __file__ + '::whole_current_cross_tomb_render_transport_and_gates', 'exec'), namespace)
    return namespace


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--fighter', choices=('kano', 'sonya'), required=True)
    parser.add_argument('--side', type=int, choices=(1, 2), required=True)
    args = parser.parse_args()
    folder, output = paths(args.fighter, args.side)
    need(not folder.exists() and not output.exists(), 'Fresh immutable actual render case')
    try:
        current = initialize(args.fighter, args.side)
        scope = functions(current)
        report = scope['run'](args.fighter, args.side)
        RAM['report'] = report
    except Exception as error:
        report = dict(passed=False, error=repr(error), traceback=traceback.format_exc(),
                      fullPortAcceptance=False, goalStatus='active')
        print(json.dumps(report), flush=True)
    need(not output.exists(), 'Never overwrite native rendering outcome')
    output.mkdir()
    (output / 'report.json').write_text(json.dumps(report, indent=2) + '\n')
    if report['passed']:
        print(json.dumps({k:v for k,v in report.items()if k not in('inputHashes','nativeScene','nativeBranch')}, indent=2), flush=True)
        RAM['server'] = review.start(RAM['images'], folder)
    code.interact(banner='Same current native render trial; bounded original RGB only in RAM.', local=dict(RAM=RAM))
