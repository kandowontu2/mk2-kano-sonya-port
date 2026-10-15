"""Original split activation, earned true-ID rounds,179+120 native completion."""
import copy,inspect,json,re
from pathlib import Path
import qualify_bounded_jax_clap_finisher as p1
import qualify_bounded_p2_jax_clap_control as p2
from qualify_bounded_stock_head_body_footprints import PREFIX
import verify_native_source_sync as sync

def main():
    out=sync.ROOT/'audit_bounded_kung_lao_split_finisher_checked';assert not out.exists();results={}
    for side in (1,2):
        source=inspect.getsource(p1.gate) if side==1 else p2.source
        changes={"a['address']=='FF8C7820'":"a['address']=='FF8C6040'","x['own'].split(':')[-1]=='11'":"x['own'].split(':')[-1]=='0'"}
        for before,after in changes.items():assert source.count(before)==1;source=source.replace(before,after)
        if side==2:
            before="int(w['frame'])-int(a['frame'])==188";assert source.count(before)==1
            source=source.replace(before,"int(w['frame'])-int(a['frame'])==179")
        else:source=source.replace("    assert t['reason']","    assert int(w['frame'])-int(a['frame'])==179\n    assert t['reason']",1)
        namespace={};exec(compile(source,__file__+'::native_split_gate','exec'),namespace);gate=namespace['gate']
        for fighter,ident in [('sonya',18),('kano',17)]:
            folder=sync.ROOT/f'audit_bounded_{fighter}_p{side}_kung_lao_split_finisher_runtime'
            t=json.loads((folder/'terminal.json').read_text());assert t['exitCode']==0 and t['limitReason'] is None
            assert not (folder/'stderr.log').read_text().strip();rows=[]
            with (folder/'run.log').open() as stream:
                for line in stream:
                    assert '[LUA ERROR]' not in line
                    if not line.startswith('MK2_STOCK_HEAD_V921_'):continue
                    m=PREFIX.match(line);assert m and (m[3],m[4],m[5],m[6],m[7])==(fighter,str(side),'kung_lao','0','none')
                    rows.append((m[1],dict(re.findall(r'(\w+)=([^\s]+)',line))))
            def run(value):return gate(value,ident) if side==1 else gate(value,[],ident)
            accepted=run(rows);faults=[]
            for tag,key,value in [('ACTION','address','FF8C7820'),('ACTION','damage','321'),('WRAP','frame','1')]:
                bad=copy.deepcopy(rows);target=next(r for kind,r in bad if kind==tag);assert target[key]!=value;target[key]=value
                try:run(bad)
                except AssertionError:faults.append(tag+'.'+key)
                else:raise AssertionError('Control fault accepted')
            results[f'{fighter}P{side}']=dict(physical=accepted,nativeActionFields=179,followthroughFields=120,
                rejectedFaults=faults,terminal=t,logSha256=sync.sha(folder/'run.log'))
    report=dict(passed=True,results=results,sourceSync=sync.verify(),checkerSha256=sync.sha(Path(__file__)),
        renderedArtAccepted=False,heardAudioAccepted=False,allFinishersAccepted=False,fullGoalComplete=False)
    out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(passed=True,cases={k:r['physical'] for k,r in results.items()})))

if __name__=='__main__':main()
