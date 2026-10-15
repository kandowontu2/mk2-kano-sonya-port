"""Opposite-slot control proof only; randomized voice selection left open."""
import json,re
from pathlib import Path
from qualify_bounded_p2_stock_head_finisher import PREFIX
import qualify_bounded_stock_head_finisher as original
import verify_native_source_sync as sync

def main():
    out=sync.ROOT/'audit_bounded_p2_stock_head_control_checked';assert not out.exists();results={}
    for fighter,ident in (('sonya',18),('kano',17)):
        folder=sync.ROOT/f'audit_bounded_p2_{fighter}_stock_head_finisher_runtime'
        terminal=json.loads((folder/'terminal.json').read_text())
        assert terminal['exitCode']==0 and terminal['limitReason'] is None
        assert not (folder/'stderr.log').read_text().strip()
        rows=[]
        with (folder/'run.log').open() as stream:
            for line in stream:
                assert '[LUA ERROR]' not in line
                if not line.startswith('MK2_STOCK_HEAD_V921_'):continue
                match=PREFIX.match(line);assert match
                tag,frame,name,side,killer,writes,assistance=match.groups()
                assert (name,side,killer,writes,assistance)==(fighter,'2','baraka','0','none')
                rows.append((tag,dict(re.findall(r'(\w+)=([^\s]+)',line))))
        control=original.gate(rows,fighter,ident)
        action=next(r for tag,r in rows if tag=='ACTION')
        assert action['actor']=='01034E90' and action['victim_actor']=='010350A0'
        assert all(r['victim'].split(':')[0]=='010350A0' and r['own'].split(':')[0]=='01034E90' for tag,r in rows if tag=='STATE')
        results[fighter]=dict(**control,physicalVictimSlot=2,terminal=terminal,logSha256=sync.sha(folder/'run.log'))
    report=dict(passed=True,results=results,sourceSync=sync.verify(),checkerSha256=sync.sha(Path(__file__)),
        voiceRandomSelectionAccepted=False,renderedP2EffectsAccepted=False,heardAudioAccepted=False,fullGoalComplete=False)
    out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(passed=True,results=results)))

if __name__=='__main__':main()
