"""Complete physical-body source/clip/display gate, independent arm-rip census."""
import collections,copy,inspect,json,re
from pathlib import Path
import qualify_bounded_jax_clap_body_pixels as previous
from qualify_bounded_jax_arms_draw_census import states
import verify_native_source_sync as sync

source=inspect.getsource(previous.coverage_gate).replace('188','147').replace('189','148')
namespace=dict(previous.__dict__);exec(compile(source,__file__+'::147_field_gate','exec'),namespace)
coverage_gate=namespace['coverage_gate']

def main():
    out=sync.ROOT/'audit_bounded_jax_arms_body_pixels_checked';assert not out.exists();results={}
    proof=json.loads((sync.ROOT/'audit_bounded_jax_arms_draw_census_checked/report.json').read_text());assert proof['passed']
    for side in (1,2):
        for fighter in ('sonya','kano'):
            key=f'{fighter}P{side}';census=sync.ROOT/f'audit_bounded_{fighter}_p{side}_jax_arms_draw_census_runtime'
            assert sync.sha(census/'run.log')==proof['results'][key]['logSha256']
            folder=sync.ROOT/f'audit_bounded_{fighter}_p{side}_jax_arms_body_pixels_runtime'
            terminal=json.loads((folder/'terminal.json').read_text())
            assert terminal['exitCode']==0 and terminal['limitReason'] is None and not (folder/'stderr.log').read_text().strip()
            old=states(census,fighter,side);tags={tag for tag,r in old}
            assert [row for row in states(folder,fighter,side) if row[0] in tags]==old
            ready=int(next(r for tag,r in old if tag=='ACTION')['frame']);expected=collections.Counter()
            with (census/'run.log').open() as stream:
                for line in stream:
                    if not line.startswith('MK2_EFFECT_CENSUS_FIFO '):continue
                    r=dict(re.findall(r'(\w+)=([^\s]+)',line))
                    if r['physical']=='0':continue
                    size=int(r['size'],16);xy=int(r['xy'],16)
                    expected[(int(r['frame']),r['physical'],r['id'],r['pose'],r['source'],size&1023,(size>>16)&1023,xy&1023,(xy>>16)&511,(int(r['command'],16)>>16)&65535)]+=1
            groups=previous.summaries_at(folder);positive=coverage_gate(groups,ready,expected);faults=[]
            for fault in ('visible_mismatch','missing_draw','wrong_clip'):
                bad=copy.deepcopy(groups)
                if fault=='visible_mismatch':bad['COMPLETE_FOOTPRINT'][0]['display_fail']='1'
                elif fault=='missing_draw':bad['IDLE_OPAQUE'].pop(0)
                else:bad['IDLE_OPAQUE'][0]['native_clipped']='9999'
                try:coverage_gate(bad,ready,expected)
                except AssertionError:faults.append(fault)
                else:raise AssertionError('Fault accepted')
            results[key]=dict(**positive,rejectedFaults=faults,terminal=terminal,logSha256=sync.sha(folder/'run.log'))
    report=dict(passed=True,results=results,sourceSync=sync.verify(),checkerSha256=sync.sha(Path(__file__)),nonphysicalEffectsAccepted=False,subjectiveAllArtAccepted=False,heardAudioAccepted=False,fullGoalComplete=False)
    out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(passed=True,cases={k:{f:v for f,v in r.items() if f not in ('terminal','logSha256')} for k,r in results.items()})))

if __name__=='__main__':main()
