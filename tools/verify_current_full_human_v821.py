"""Current 52-case native human command/contact/block/miss/recovery regression.

True physical IDs/owners, original health stores and full ordinary follow-up.
This is not all victims, CPU, interrupts/KO, exact art/audio, towers or release.
"""
import argparse
import json
from pathlib import Path
import re
from PIL import Image
import verify_native_candidate_v798 as build
import verify_human_special_contacts_v635 as positive
import verify_human_special_negative_v5 as negative

ROOT=build.ROOT
need=build.need

def case_folder(name):return ROOT/('audit_v820_'+name)

def check_case(log,move,side,scenario=None,air=False):
    case=positive.verify_log(log,move,side,air,'sub_zero')if scenario is None else negative.verify_log(log,move,side,scenario,'sub_zero')
    if move=='ball':
        if scenario is not None:negative.verify_repel(log,side)
        if scenario!='miss':case.update(negative.verify_rebound(log,side,scenario=='block'))
    return case

def specs():
    for move in positive.SPECS:
        for side in (1,2):
            fixtures=[(None,False)]
            if move=='square':fixtures.append((None,True))
            fixtures += [('block',False),('miss',False)]
            if move=='leg':fixtures.append(('duck_block',False))
            for scenario,air in fixtures:
                name=f'positive_{move}{"_air"if air else ""}_p{side}'if scenario is None else f'negative_{move}_{scenario}_p{side}'
                yield name,move,side,scenario,air

def verify():
    inputs={};cases=[]
    for name,move,side,scenario,air in specs():
        folder=case_folder(name);build.matched(folder,inputs)
        launch=json.loads((folder/'result.json').read_text(encoding='utf-8-sig'))
        need((launch['move'],launch['side'],launch['victim'])==(move,side,'sub_zero'),'Exact current physical input fixture')
        need(launch.get('air')==air if scenario is None else launch['scenario']==scenario,'Declared actual contact/defense scenario')
        observer='mk2ks_human_special_matrix_v3.lua'if scenario is None else'mk2ks_human_special_negative_v9.lua'
        runner='run_current_human_special_v820.ps1'if scenario is None else'run_current_human_negative_v820.ps1'
        source=(folder/'input_sources'/observer).read_text()
        need(not re.search(r'write_u\d+|:write_|load_?state|\.value\s*=(?!=)|dofile\(',source),'Standalone real-input observer, no gameplay state writes')
        options=(folder/'input_sources'/runner).read_text()
        need('-nocheat'in options and '-noautoframeskip -frameskip 0'in options,'Cheat-disabled full callbacks')
        case=check_case((folder/'run.log').read_text(encoding='utf-8-sig'),move,side,scenario,air)
        case['capture']=folder.name;cases.append(case)
        for name in ('special_before.png','special_recovered.png','special_final.png'):
            path=folder/'snap'/name
            with Image.open(path)as image:need(image.size==(400,254),'Native screenshot inventory');image.load()
            inputs[str(path)]=build.digest(path)
    need(len(cases)==52,'Complete eight-special both-slot fixture inventory')
    for module in (build,positive,negative):inputs[str(Path(module.__file__).resolve())]=build.digest(module.__file__)
    for name in ('verify_current_full_human_v821.py','verify_human_special_matrix.py',
                 'verify_ko_round_floor_shadows.py','inspect_ground_presentation.py'):
        path=ROOT/'tools'/name;inputs[str(path)]=build.digest(path)
    return {'passed':True,'boundedMatrixPassed':True,'fullPortAcceptance':False,'candidate':build.NAME,'cases':cases,
            'positiveCases':18,'negativeCases':34,'pairedFields':sum(c['fields']for c in cases),'inputHashes':inputs,
            'scope':__doc__,'limits':'Standing square-wave is an expected anti-air non-contact path, not a blocked hit. Standing leg block takes native grab damage; crouch-block rejects it. Three PNGs per case are inventory, not exact art/pixel fidelity. Other victims/arenas/CPU/interruptions/KO/audio/campaigns remain separate gates.'}

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('output',type=Path);args=parser.parse_args()
    output=args.output.resolve();need(not output.exists(),'Do not overwrite proof')
    report=verify();output.mkdir();(output/'verification.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:report[k]for k in('candidate','positiveCases','negativeCases','pairedFields','boundedMatrixPassed','fullPortAcceptance')}))
