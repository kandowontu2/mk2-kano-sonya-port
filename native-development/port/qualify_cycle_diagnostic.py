"""Qualify first-phase playback only; not move/throw/gameplay acceptance."""
import csv
import hashlib
import json
import re
from pathlib import Path
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
BASE=HERE.parent/'baseline'
SRC=BASE/'mk2-rebuild-main/srcw'
RUN=BASE/'stock_wolf_animation_matrix_51'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest().upper()
def main():
    execution=json.loads((RUN/'execution.json').read_text())
    assert execution['exitCode']==0 and not execution['timedOut']
    assert execution['nativeInitialPhaseMatrix'] and not execution['customDriver'] and not execution['gameMemoryWrites']
    assert sha(Path(execution['emulator']))==execution['emulatorSHA256']
    symbols={name:int(a,16) for a,name in re.findall(r'\b([0-9a-fA-F]{8})\s+([A-Za-z_]\w*)',(SRC/'CYCTEST.MAP').read_text())}
    coverage=json.loads((HERE/'generated_templates_throws/TRANSLATION.json').read_text())
    rows=list(csv.DictReader((RUN/'cycle_objects.csv').open()))
    live=[r for r in rows if r['kid']=='17' and r['sid']=='18']
    assert len(live)>=480 and int(live[-1]['frame'])-int(live[0]['frame'])>=8200
    results={}
    for fighter,prefix,identity in [('kano','k',17),('sonya','s',18)]:
        expected=set(coverage['fighters'][fighter]['entries'])
        assert len(expected)==51 and {r[prefix+'stage'] for r in live}==expected
        pose_addresses={value for name,value in symbols.items() if name.startswith(f'ks_{fighter}_pose_')}
        assert all(int(r[prefix+'shape'],16) in pose_addresses for r in live)
        text=(HERE/f'generated_templates_throws/{fighter.upper()}ANI.ASM').read_text()
        stage_checks={}
        for index,entry in coverage['fighters'][fighter]['entries'].items():
            label=entry['label']
            body=text.split('\n'+label+'\n',1)[1].split('        .def ',1)[0]
            referenced=set(re.findall(r'ks_\w+_pose_[0-9a-f]+',body))
            expected_poses={symbols[name] for name in referenced}
            actual={int(r[prefix+'shape'],16) for r in live if r[prefix+'stage']==index}
            assert actual & expected_poses, (fighter,index,'No own script pose was displayed')
            stage_checks[index]=dict(samples=sum(r[prefix+'stage']==index for r in live),ownScriptPoseObserved=True)
        results[fighter]=dict(nativeID=identity,initialPhaseScripts=len(expected),allRecordedShapesBelongToOwnArt=True,stages=stage_checks)
    inputs=[RUN/'execution.json',RUN/'cycle_objects.csv',SRC/'CYCTEST.MAP',SRC/'CYCTEST.OUT',SRC/'KSCYCLE.ASM',
            HERE/'diagnostics/KSCENE.ASM',HERE/'diagnostics/cycle_probe.lua',HERE/'generated_templates_throws/TRANSLATION.json',
            HERE/'generated_templates_throws/KANOANI.ASM',HERE/'generated_templates_throws/SONYAANI.ASM']
    for name in ('CYCLEASM.LOG','CYCLETBL.LOG'):
        p=BASE/'mk2-rebuild-main'/name
        assert 'No Errors,  No Warnings' in p.read_text();inputs.append(p)
    link=BASE/'mk2-rebuild-main/CYCLINK.LOG'
    assert 'undefined' not in link.read_text().lower();inputs.append(link)
    inputs+=list((RUN/'snap').glob('cycle_*.png'))
    result=dict(passed=True,scope='Initial-phase native animation playback for 51 scripts per actor on stock MAME',
        liveSamples=len(live),firstLiveFrame=int(live[0]['frame']),lastLiveFrame=int(live[-1]['frame']),fighters=results,
        hostGuestMemoryWrites=False,customEmulator=False,playablePortVerified=False,pairedThrowVerified=False,
        allAnimationPhasesVerified=False,files={str(p.relative_to(ROOT)):sha(p) for p in inputs})
    (RUN/'qualification.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ('files','fighters')},indent=2))
if __name__=='__main__':main()
