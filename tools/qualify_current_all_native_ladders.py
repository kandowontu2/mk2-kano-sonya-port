"""Actual loaded six-order roster preservation; not campaign-completion proof."""
import json
import re
import verify_native_source_sync as sync


def gate(text):
    assert 'LUA ERROR' not in text.upper()
    rows=[dict(re.findall(r'(\w+)=([^ ]+)',line)) for line in text.splitlines()
          if line.startswith('MK2_LADDER_TABLE ')]
    assert len(rows)==6 and [r['order'] for r in rows]==list(map(str,range(6)))
    for row in rows:
        ids=list(map(int,row['ids'].split(',')))
        assert len(ids)==18 and ids[:13].count(17)==ids[:13].count(18)==1
        assert len(set(ids[:13]))==13 and ids[13:]==[14,6,12,13,65535]
        assert row['original_regular_preserved']=='11' and row['boss_tail_preserved']=='5'
        assert row['writes']=='0' and row['assistance']=='none'
    assert 'MK2_LADDER_GEOMETRY positions=16 minimum_frame_height=49 writes=0 assistance=none' in text
    assert 'MK2_LADDER_RESULT frame=700 writes=0 assistance=none' in text
    return rows


sync.verify()
folder=sync.ROOT/'audit_current_all_native_ladders_runtime'
terminal=json.loads((folder/'terminal.json').read_text())
assert terminal['exitCode']==0 and terminal['limitReason'] is None
assert terminal['peakWorkingSetBytes']<=320*1024*1024 and terminal['elapsedSeconds']<90
assert terminal['logBytes']<=10*1024*1024
assert terminal['observerSha256']==sync.sha(sync.ROOT/'audit_current_all_native_ladders_preparation/attract.lua')
assert not (folder/'stderr.log').read_text().strip()
text=(folder/'run.log').read_text()
rows=gate(text)
try:
    gate(text.replace('ids=17,11','ids=0,11',1))
except AssertionError:
    pass
else:
    raise AssertionError('Proxy roster mutation accepted')
out=sync.ROOT/'audit_current_all_native_ladders_checked'
assert not out.exists()
out.mkdir()
report=dict(passedLoadedTableChecks=True,orders=rows,portraitPositions=16,
            originalBossTailPreserved=True,proxyMutationRejected=True,
            logSHA256=sync.sha(folder/'run.log'),allCampaignsCompleted=False,
            allLadderPixelsAccepted=False,fullPortAccepted=False)
(out/'report.json').write_text(json.dumps(report,indent=2))
print('PASS: all six loaded ladders contain both true IDs, preserve stock order/tail and non-overlapping portrait positions; campaign completion remains unproven')
