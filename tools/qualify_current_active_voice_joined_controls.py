"""Combine exact active-clip cut and actual own-ID post-join control gates."""
import ast,copy,json
from pathlib import Path
import check_campaign_stage_chronology as chronology
import verify_native_source_sync as sync
sync.verify()
folder=sync.ROOT/'audit_current_active_voice_joined_controls_runtime'
out=sync.ROOT/'audit_current_active_voice_joined_controls_checked'
assert not out.exists()
terminal=json.loads((folder/'terminal.json').read_text(encoding='utf-8-sig'))
assert terminal['exitCode']==0 and terminal['limitReason'] is None
assert not (folder/'stderr.log').read_text().strip()
rows=chronology.load(folder/'run.log')
old=chronology.load(sync.ROOT/'audit_current_cpu_sonya_active_voice_join_runtime/run.log')
cutoff=int(old['JOIN_SELECTION'][0]['frame'])
for tag in set(rows)|set(old):
    assert [r for r in rows.get(tag,[]) if int(r['frame'])<cutoff]==[r for r in old.get(tag,[]) if int(r['frame'])<cutoff],tag
def extract(name):
    source=Path(__file__).with_name(name).read_text()
    tree=ast.parse(source)
    function=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='gate')
    return ast.get_source_segment(source,function)
audio=extract('qualify_current_cpu_sonya_active_voice_join.py')
context={'length':66523};exec(compile(audio,__file__+'::audio','exec'),context)
audio_gate=context['gate'];audio_proof=audio_gate(rows)
controls=extract('qualify_current_native_joined_controls_scoped.py')
before="rows['JOIN_TRIGGER'][0]['id']==rows['JOIN_TRIGGER'][0]['roster']=='18'"
after="rows['JOIN_TRIGGER'][0]['id']=='18' and rows['JOIN_TRIGGER'][0]['cue']=='6B01'"
assert controls.count(before)==1
controls=controls.replace(before,after)
context={};exec(compile(controls,__file__+'::controls','exec'),context)
control_gate=context['gate'];control_proof=control_gate(rows,[17,18])
bad=copy.deepcopy(rows);bad['JOINED_MATCH_PAIR'][0]['id']='1'
try:control_gate(bad,[17,18])
except AssertionError:pass
else:raise AssertionError('Post-join proxy accepted')
out.mkdir();report=dict(activeClipCutAndPostJoinControlsPassed=True,audioProof=audio_proof,
    gameplayProof=control_proof,priorNativeJoinPrefixUnchangedBefore=cutoff,
    postJoinProxyFaultRejected=True,terminal=terminal,logSHA256=sync.sha(folder/'run.log'),
    allJoinedMovesAccepted=False,postEndingJoinAccepted=False,fullPortAccepted=False)
(out/'report.json').write_text(json.dumps(report,indent=2));print(json.dumps(control_proof))
