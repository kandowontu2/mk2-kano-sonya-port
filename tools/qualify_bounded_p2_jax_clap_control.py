"""Separate earned P2 victim control proof; audio packet priority remains open."""
import copy, inspect, json, re
from pathlib import Path
import qualify_bounded_p2_jax_clap_audio_route as original
import verify_native_source_sync as sync

source = inspect.getsource(original.gate)
boundary = "    branches=[(i,b) for i,(tag,b) in enumerate(audio) if tag=='BRANCH'];assert len(branches)==1\n"
assert source.count(boundary) == 1
source = source[:source.index(boundary)] + "    return dict(actionFrame=int(a['frame']),wrapFrame=int(w['frame']),terminalFrame=int(t['frame']),trueIDStates=len(states),damage=322,nativeWins=2,victimSlot=2)\n"
namespace = {}
exec(compile(source, __file__ + '::unchanged_control_gate', 'exec'), namespace)
gate = namespace['gate']

def main():
    out = sync.ROOT/'audit_bounded_p2_jax_clap_control_checked'
    assert not out.exists()
    results = {}
    for fighter, ident in [('sonya',18),('kano',17)]:
        folder = sync.ROOT/f'audit_bounded_p2_{fighter}_jax_clap_audio_route_runtime'
        terminal = json.loads((folder/'terminal.json').read_text())
        assert terminal['exitCode'] == 0 and terminal['limitReason'] is None
        assert not (folder/'stderr.log').read_text().strip()
        rows = []
        with (folder/'run.log').open() as stream:
            for line in stream:
                assert '[LUA ERROR]' not in line
                if not line.startswith('MK2_STOCK_HEAD_V921_'): continue
                match = original.PREFIX.match(line)
                assert match and (match[3],match[4],match[5],match[6],match[7]) == (fighter,'2','jax','0','none')
                rows.append((match[1],dict(re.findall(r'(\w+)=([^\s]+)',line))))
        positive = gate(rows, [], ident)
        faults = []
        for tag, key, value in [('ACTION','address','FF8CB4A0'),('ACTION','victim_actor','01034E90'),('RESULT','damage','321'),('STATE','victim','010350A0:0106B150:1')]:
            bad = copy.deepcopy(rows)
            next(row for kind,row in bad if kind==tag)[key] = value
            try: gate(bad, [], ident)
            except AssertionError: faults.append(tag+'.'+key)
            else: raise AssertionError('Fault accepted')
        results[fighter] = dict(**positive,rejectedFaults=faults,terminal=terminal,logSha256=sync.sha(folder/'run.log'))
    report = dict(passed=True,results=results,sourceSync=sync.verify(),checkerSha256=sync.sha(Path(__file__)),originalCheckerSha256=sync.sha(Path(original.__file__)),audioPriorityVerified=False,renderedP2ArtAccepted=False,fullGoalComplete=False)
    out.mkdir()
    (out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(passed=True,results=results)))

if __name__ == '__main__': main()
