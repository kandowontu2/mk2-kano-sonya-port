"""Current matched input-only idle/jump/crouch/walk grounding checkpoint."""
import argparse
import json
import re
from pathlib import Path
from inspect_native_idle_feet_v635_v2 import inspect
from verify_native_ui_flow_v635 import ROOT, NAME, EXE, PAYLOAD, digest


def need(condition,message):
    if not condition:raise ValueError(message)


def check_presentation(value,fighter,side):
    need(value['samples']==37 and value['idle_samples']==11,'All fixed current-field sample windows')
    need(value['body_mismatches']==value['vram_mismatches']==0,'All independent indexed VRAM words and body pixels exact')
    expected=17 if fighter=='kano'else 18
    for record in value['records']:
        need(record['body'][side]['id']==expected and record['body'][3-side]['id']==4,'Imported fighter and stock Kitana controls are actual IDs')
    need(value['idle_sole_rows'][1]==value['idle_sole_rows'][2],'Native stock and imported idle soles share the actual displayed floor line')
    need(value['idle_native_ground_offsets'][1]==value['idle_native_ground_offsets'][2]==[-1],'Same native stage/camera-relative idle contact line')
    need(any(not r['body'][side]['grounded']for r in value['records'])and
         any(not r['body'][3-side]['grounded']for r in value['records']),'Both genuine native jumps were observed')
    need(all(r['body'][side]['grounded']and r['body'][3-side]['grounded']for r in value['records']if 288<=r['age']<=312),
         'Both owned fighters recover to their own physical floors after jumps')
    need(all(r['body'][side]['grounded']and r['body'][3-side]['grounded']for r in value['records']if r['age']>=432),
         'Crouch release and walking retain both native physical floors')


def verify(folder,fighter,side):
    folder=Path(folder)
    result=json.loads((folder/'result.json').read_text(encoding='utf-8-sig'))
    before=json.loads((folder/'input_hashes_before.json').read_text(encoding='utf-8-sig'))
    need((result['exit_code'],result['candidate'],result['executable_sha256'],result['payload_sha256'],
          result['fighter'],result['side'],result['assistance'])==(0,NAME,EXE,PAYLOAD,fighter,side,'none'),'Exact terminal native ground run')
    need(before==result['input_hashes'],'Exact launch inputs before/after')
    for filename,sha in before.items():
        need(digest(filename)==sha,'Changed launch input: '+filename)
        if Path(filename).suffix in ('.lua','.ps1','.json'):
            need(digest(folder/'input_sources'/Path(filename).name)==sha,'Frozen launch input changed')
    build=json.loads((folder/'input_sources/build-info.json').read_text(encoding='utf-8-sig'))
    for filename,sha in build['input_hashes'].items():need(digest(filename)==sha,'Changed current build input')
    observer=(folder/'input_sources/mk2ks_ground_presentation_v9_probe.lua').read_text()
    need(not re.search(r'write_u\d+|:write_|load_?state|\.value\s*=(?!=)|dofile\(',observer),'Read-only observer, real two-human input')
    log=(folder/'run.log').read_text(encoding='utf-8-sig')
    need('INVALID' not in log,'Real owned identities remain valid through movement')
    final=re.findall(r'^MK2_GROUND_RESULT .+$',log,re.M)
    need(len(final)==1 and 'terminalAge=480 ' in final[0],'Entire idle/jump/crouch/walk sequence completes')
    value=inspect(folder)
    check_presentation(value,fighter,side)
    return dict(passed=True,fighter=fighter,side=side,scope=value['scope'],presentation=value,fullPortAcceptance=False,floorAcceptance=False)


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path)
    args=parser.parse_args()
    results={f'{fighter}_p{side}':verify(ROOT/f'audit_v644_native_idle_{fighter}_p{side}',fighter,side)
             for side in (1,2)for fighter in ('kano','sonya')}
    encoded=json.dumps(dict(candidate=NAME,cases=results,fullPortAcceptance=False,floorAcceptance=False),indent=2)
    if args.output:args.output.write_text(encoded+'\n',encoding='utf-8')
    else:print(encoded)
