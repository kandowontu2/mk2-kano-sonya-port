"""Read-only live/terminal native campaign statistics, never acceptance."""
import argparse
import gzip
import json
import re
from pathlib import Path
import native_process_census_v6647 as census

ROOT = Path(__file__).resolve().parents[1]


def inspect(folder_name):
    if not re.fullmatch(r'audit_[a-z0-9_]+',folder_name):
        raise ValueError('Exact workspace audit leaf required')
    folder = ROOT / folder_name
    identity = json.loads((folder / 'native_identity.json').read_text())
    actual = next((q for q in census.census() if q['ProcessId'] == identity['ProcessId']),None)
    if actual != identity:
        terminal = json.loads((folder / 'native_terminal.json').read_text())
        if actual is not None or terminal['identity'] != identity:
            raise ValueError('Same exact original native identity required')
    lines = []
    with gzip.open(folder / 'run.log.gz','rt',encoding='utf-8') as stream:
        try:
            for line in stream:
                if line.endswith('\n'): lines.append(line)
        except EOFError:
            pass
    parse = lambda tag: [dict(re.findall(r'(\w+)=([^\s]+)',line)) for line in lines if line.startswith(tag+' ')]
    live, losses, wins, specials = map(parse,('MK2_NAT_CAMPAIGN_LIVE','MK2_NAT_CAMPAIGN_LOSS',
        'MK2_NAT_CAMPAIGN_WIN','MK2_NAT_CAMPAIGN_SPECIAL'))
    stages = sorted({int(r['stage']) for r in live})
    return dict(statisticsOnly=True,exactOriginalNativePID=identity['ProcessId'],originalNativeStillLive=actual is not None,
        latestNativeField=live[-1] if live else None,
        lossesByStage={str(stage):sum(r['stage']==str(stage) for r in losses) for stage in stages},
        ownWinReadsByStage={str(stage):sum(r['stage']==str(stage) and r['slot']=='1' for r in wins) for stage in stages},
        minimumObservedCPUHealthByStage={str(stage):min(int(r['health'].split(',')[1]) for r in live if r['stage']==str(stage)) for stage in stages},
        nativeLegActivationsByStage={str(stage):sum(r.get('stage')==str(stage) and r.get('move')=='leg' for r in specials) for stage in stages},
        nativeGlobalCacheFailureRows=len(parse('MK2_CURRENT_CAMPAIGN_CACHE_FAILURE')),
        fullPortAcceptance=False,goalStatus='active')


if __name__ == '__main__':
    parser=argparse.ArgumentParser();parser.add_argument('folder');args=parser.parse_args()
    print(json.dumps(inspect(args.folder),indent=2))
