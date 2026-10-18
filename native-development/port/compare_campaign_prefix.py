"""Prove a matchup-only controller change preserved the preceding trace."""
import csv
import hashlib
import json
from pathlib import Path
import sys


def prefix(lines, opponent):
    header = lines[0]
    kept = []
    for line in lines[1:]:
        row = next(csv.DictReader([header,line]))
        if row['mode'] == '2' and int(row['p2char']) == opponent:
            return kept
        kept.append(line)
    raise AssertionError('Target matchup never reached')


def compare(first, second, opponent):
    assert first and first[0] == second[0], 'Trace columns differ'
    left,right=prefix(first,opponent),prefix(second,opponent)
    assert left == right, 'Pre-matchup trace differs'
    return dict(opponentID=opponent,identicalPreMatchupRows=len(left),
                prefixSHA256=hashlib.sha256(''.join(left).encode()).hexdigest().upper(),
                matchupOutcomeVerified=False)


if __name__ == '__main__':
    base=Path(__file__).resolve().parent.parent/'baseline'
    first,second=(base/name for name in sys.argv[1:3])
    for folder in (first,second):
        execution=json.loads((folder/'execution.json').read_text())
        assert execution['exitCode']==0 and not execution['timedOut']
        assert execution['controllerSHA256']==hashlib.sha256((folder/'autoboot.lua').read_bytes()).hexdigest().upper()
    report=compare((first/'campaign.csv').read_text().splitlines(keepends=True),
                   (second/'campaign.csv').read_text().splitlines(keepends=True),int(sys.argv[3]))
    report['runs']=[first.name,second.name]
    report['pins']={str(path):hashlib.sha256(path.read_bytes()).hexdigest().upper()
                    for folder in (first,second) for path in
                    (folder/'campaign.csv',folder/'execution.json',folder/'autoboot.lua')}
    report['pins'][str(Path(__file__).resolve())]=hashlib.sha256(Path(__file__).read_bytes()).hexdigest().upper()
    (second/'CAMPAIGN_PREFIX_COMPARISON.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({key:value for key,value in report.items() if key!='pins'}))
