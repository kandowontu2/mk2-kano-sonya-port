"""Read the same live native prefix; no replay, controls or process changes."""
import gzip
import json
import re
from pathlib import Path
import capture_native_paired_stumble_campaign as capture

ROOT, need, sha = capture.ROOT, capture.need, capture.sha
GAME, PARENT = 129056, 64112


def inspect_prefix():
    identity = json.loads((capture.OUT / 'native_identity.json').read_text())
    actual = next((p for p in capture.base.census.census() if p['ProcessId'] == GAME), None)
    need(actual == identity and identity['ParentProcessId'] == PARENT,
         'Exact original live native PID/path/parent/birth/command')
    lines = []
    with gzip.open(capture.OUT / 'run.log.gz', 'rt', encoding='utf-8') as stream:
        try:
            for line in stream:
                if line.endswith('\n'):
                    lines.append(line)
        except EOFError:
            pass
    text = ''.join(lines)
    parse = lambda tag: [dict(re.findall(r'(\w+)=([^\s]+)', line))
                         for line in lines if line.startswith(tag + ' ')]
    losses = parse('MK2_NAT_CAMPAIGN_LOSS')
    wins = parse('MK2_NAT_CAMPAIGN_WIN')
    paired = parse('MK2_PAIRED_STUMBLE_VICTIM')
    live = parse('MK2_NAT_CAMPAIGN_LIVE')
    failure = parse('MK2_CURRENT_CAMPAIGN_CACHE_FAILURE')
    need(live and paired and not failure and not re.search(r'LUA ERROR|stack traceback|fatal error', text),
         'Actual paired handoff reached without native global-cache corruption or loader errors')
    return text, dict(actualNativeIdentity=identity, latestNativeField=live[-1],
        observedLossesByStage={str(stage): sum(r['stage'] == str(stage) for r in losses) for stage in (0, 1, 2)},
        ownNativeWinReadsByStage={str(stage): sum(r['stage'] == str(stage) and r['slot'] == '1' for r in wins) for stage in (0, 1, 2)},
        actualPairedHandoffs=paired, actualGlobalCacheStores=len(failure),
        endingReached=bool(parse('MK2_NAT_CAMPAIGN_ENDING_COMPLETED')),
        postEndingJoinReached=bool(parse('MK2_POSTENDING_COMPLETE')),
        fullPortAcceptance=False, goalStatus='active')


if __name__ == '__main__':
    _, report = inspect_prefix()
    print(json.dumps({k: v for k, v in report.items() if k not in ('actualNativeIdentity', 'actualPairedHandoffs')}, indent=2))
