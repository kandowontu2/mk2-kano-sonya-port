"""Extract compact frame sheets for human review, without raw media caches."""
import argparse
import json
from pathlib import Path
import shutil
import subprocess

ROOT=Path(__file__).resolve().parent.parent/'videos_showcase_20261015'
FF=shutil.which('ffmpeg')

def main():
    parser=argparse.ArgumentParser();parser.add_argument('group',choices=['special','fatality','friendly','stage','basic','morph']);args=parser.parse_args()
    groups={'special':['kano_knife','kano_blade','kano_choke','kano_ball','sonya_ring','sonya_bicycle','sonya_leg','sonya_square'], 'fatality':['kano_primary_v2','kano_secondary','sonya_primary','sonya_secondary'], 'friendly':['kano_friendship','sonya_friendship','kano_babality','sonya_babality'], 'stage':[f'{f}_{m}' for f in ('kano','sonya') for m in ('deadpool','tomb','pit')], 'basic':[f'{f}_{m}' for f in ('kano','sonya') for m in ('uppercut','sweep','roundhouse','throw','standing_block','crouching_block')], 'morph':['shang_kano','shang_sonya']}
    out=ROOT/('review_'+args.group);assert not out.exists();out.mkdir()
    rows=[]
    for key in groups[args.group]:
        case=ROOT/(key+'_v2' if key=='kano_uppercut' else key);r=json.loads((case/'verification.json').read_text());assert r['passed']
        clip=next(case.glob('*.mp4'))
        frames=int(next(x for x in r['finalProbe']['streams'] if x['codec_type']=='video')['nb_frames'])
        picks=[50,90,140,200] if args.group=='special' else [int(frames*x) for x in (.1,.3,.5,.75)]
        select='+'.join(f'eq(n\\,{x})' for x in picks)
        target=out/(key+'.png')
        subprocess.run([FF,'-v','error','-nostdin','-i',str(clip),'-vf',f'select={select},tile=4x1','-frames:v','1',str(target)],check=True,timeout=15,creationflags=0x08000000)
        rows.append(target)
    cmd=[FF,'-v','error','-nostdin']
    for row in rows:cmd+=['-i',str(row)]
    cmd+=['-filter_complex',f'vstack=inputs={len(rows)}','-frames:v','1',str(out/'sheet.png')]
    subprocess.run(cmd,check=True,timeout=15,creationflags=0x08000000)
    (out/'index.json').write_text(json.dumps(dict(topToBottom=groups[args.group],columns='Four chronological samples, not exhaustive scene verification'),indent=2))
    print(out/'sheet.png')

if __name__=='__main__':main()
