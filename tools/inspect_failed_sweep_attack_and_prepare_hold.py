"""Bind actual stock poses and prepare earlier physical Back hold."""
import json,re,struct
import verify_native_source_sync as sync
from classify_observed_native_pose_sequences import classify

def main():
    root=sync.ROOT;sync.verify()
    stock=(root/'mk2/mk2-maincpu.bin').read_bytes()
    stockroot=struct.unpack_from('<I',stock,0x020c2a+4*4)[0]
    old=root/'audit_bounded_sweep_reaction_preparation'
    out=root/'audit_bounded_held_back_sweep_preparation';assert not out.exists()
    observed={}
    for fighter in ('sonya','kano'):
        folder=root/f'audit_bounded_{fighter}_sweep_reaction_runtime'
        rows=[]
        with (folder/'run.log').open() as stream:
            for line in stream:
                if '_FIELD ' in line:
                    r=dict(re.findall(r'(\w+)=([^\s]+)',line))
                    if r['slot']=='2' and 1416<=int(r['frame'])<=1430:rows.append(r)
        census=classify(stock,0xff800000,stockroot,sorted({r['pose'] for r in rows}))
        observed[fighter]=dict(actualStockPoseReferences=census,
                              logSha256=sync.sha(folder/'run.log'))
    lua=(old/'prepared_observer.lua').read_text()
    needle="if age>=112 and age<116 then input(2,b.x>a.x and 'Right' or 'Left')end"
    assert lua.count(needle)==1
    lua=lua.replace(needle,"if age>=96 and age<116 then input(2,b.x>a.x and 'Right' or 'Left')end")
    lua=lua.replace('physical_sweep_recovery','physical_held_back_sweep_recovery')
    out.mkdir();target=out/'prepared_observer.lua';target.write_text(lua)
    for fighter in ('sonya','kano'):
        runner=(old/f'run_{fighter}.ps1').read_text().replace(old.name,out.name)
        runner=runner.replace(sync.sha(old/'prepared_observer.lua'),sync.sha(target))
        runner=runner.replace(f'audit_bounded_{fighter}_sweep_reaction_runtime',
                              f'audit_bounded_{fighter}_held_back_sweep_runtime')
        (out/f'run_{fighter}.ps1').write_text(runner)
    (out/'report.json').write_text(json.dumps(dict(priorActualAttackPoseEvidence=observed,
        prepared=True,acceptance=False),indent=2)+'\n')
    print(json.dumps(observed))

if __name__=='__main__':main()
