"""Loaded relocation proof, expressly not earned ending execution."""
import copy,json,re
import verify_native_source_sync as sync
sync.verify()
folder=sync.ROOT/'audit_current_ending_scene_operands_runtime'
out=sync.ROOT/'audit_current_ending_scene_operands_checked'
assert not out.exists()
terminal=json.loads((folder/'terminal.json').read_text(encoding='utf-8-sig'))
assert terminal['exitCode']==0 and terminal['limitReason'] is None
assert not (folder/'stderr.log').read_text().strip()
def load(path):
    text=path.read_text();assert 'LUA ERROR' not in text
    return [(l.split()[0].removeprefix('MK2_LIGHT_ATTRACT_'),dict(re.findall(r'(\w+)=([^\s]+)',l))) for l in text.splitlines() if l.startswith('MK2_LIGHT_ATTRACT_')]
rows=load(folder/'run.log')
new_tags={'ENDING_SCENE_WORD','ENDING_SCENE_TABLE','ENDING_SCENE_STOCK'}
assert [(t,r) for t,r in rows if t not in new_tags]==load(sync.ROOT/'audit_current_ending_asset_tables_runtime/run.log')
expected={'FF844700':'0270','FF8448A0':'0270','FF844720':'0170','FF844970':'0170',
          'FF844740':'0190','FF844AB0':'0190','FF844760':'01B0','FF844B40':'01B0'}
tables={'FF8F51C0':'FFFA5000','FF8F53E0':'FFFA5800','FF8447B0':'FFFA4800'}
def gate(records):
    words=[r for t,r in records if t=='ENDING_SCENE_WORD']
    assert len(words)==8 and {r['at']:r['actual'] for r in words}==expected
    pointers=[r for t,r in records if t=='ENDING_SCENE_TABLE']
    assert len(pointers)==3 and {r['at']:r['actual'] for r in pointers}==tables
    stock=[r for t,r in records if t=='ENDING_SCENE_STOCK']
    assert len(stock)==1 and stock[0]['picture_rows_preserved']=='41'
    assert all(r['frame']=='600' and r['writes']=='0' and r['assistance']=='none' for t,r in records if t in new_tags)
gate(rows)
bad=copy.deepcopy(rows);next(r for t,r in bad if t=='ENDING_SCENE_WORD')['actual']='0310'
try:gate(bad)
except AssertionError:pass
else:raise AssertionError('Unrelocated vulnerable scene slot accepted')
out.mkdir();report=dict(loadedEndingSceneOperandsPassed=True,oldAssetObservationsUnchanged=True,
    pairedSceneFields=expected,textPictureOperands=tables,stockPicturesPreserved=41,
    unrelocatedSceneSlotFaultRejected=True,terminal=terminal,logSHA256=sync.sha(folder/'run.log'),
    earnedEndingExecution=False,endingPixelsAccepted=False,postEndingJoinAccepted=False,fullPortAccepted=False)
(out/'report.json').write_text(json.dumps(report,indent=2));print(json.dumps(report))
