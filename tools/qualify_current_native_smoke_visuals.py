"""Same accepted native full-cycle records plus exactly four bounded PNGs."""
import ast
import json
import re
import struct
import verify_native_source_sync as sync
sync.verify()
tree=ast.parse((sync.ROOT/'tools/qualify_current_sonya_natural_smoke.py').read_text())
defs=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='load']
assert len(defs)==1
exec(compile(ast.Module(body=defs,type_ignores=[]),__file__+'::read_only_records','exec'))
out=sync.ROOT/'audit_current_native_smoke_visuals_checked'
assert not out.exists()
cases=[];total=0
for fighter,baseline in [('sonya','audit_current_sonya_smoke_transition_batched'),
                         ('kano','audit_current_kano_smoke_64_cadence')]:
    proof=json.loads((sync.ROOT/(baseline+'_checked')/'report.json').read_text())
    assert proof['completedRunAccepted'] and proof['normalTwoHumanReturnAccepted']
    prior=sync.ROOT/(baseline+'_runtime')
    assert sync.sha(prior/'run.log')==proof['logSHA256']
    folder=sync.ROOT/('audit_current_native_smoke_visuals_'+fighter+'_runtime')
    terminal=json.loads((folder/'terminal.json').read_text(encoding='utf-8-sig'))
    assert terminal['exitCode']==0 and terminal['limitReason'] is None
    assert terminal['peakWorkingSetBytes']<=320*1024*1024 and terminal['logBytes']<=10*1024*1024
    assert terminal['observerSha256']==sync.sha(sync.ROOT/('audit_current_native_smoke_visuals_preparation/'+fighter+'.lua'))
    assert not (folder/'stderr.log').read_text().strip()
    rows,old=load(folder/'run.log'),load(prior/'run.log')
    for tag in set(rows)|set(old):
        if tag!='VISUAL_SAVED':assert rows.get(tag,[])==old.get(tag,[]),tag
    saved=rows['VISUAL_SAVED'];assert len(saved)==2
    assert [(r['name'],r['count']) for r in saved]==[('secret_fight.png','1'),('normal_return.png','2')]
    assert saved[0]['frame']==rows['SECRET_FIGHT'][0]['frame']
    assert int(saved[1]['frame'])==int(rows['SECRET_RETURN'][0]['frame'])+40
    paths=sorted(folder.rglob('*.png'))
    assert sorted(p.name for p in paths)==['normal_return.png','secret_fight.png']
    size=sum(p.stat().st_size for p in paths);assert size<=112*1024;total+=size
    images=[]
    for path in paths:
        with path.open('rb') as stream:header=stream.read(24)
        assert header[:8]==b'\x89PNG\r\n\x1a\n' and header[12:16]==b'IHDR'
        assert struct.unpack('>II',header[16:24])==(400,254)
        images.append(dict(path=str(path),sha256=sync.sha(path),bytes=path.stat().st_size))
    cases.append(dict(fighter=fighter,actualGameplayAndControlsUnchanged=True,
                      images=images,terminal=terminal,logSHA256=sync.sha(folder/'run.log')))
assert total<=224*1024
out.mkdir()
(out/'report.json').write_text(json.dumps(dict(passedObserverNeutrality=True,cases=cases,
    images=4,totalImageBytes=total,visualReviewPending=True,allFramesReviewed=False,
    secretAudioAccepted=False,fullPortAccepted=False),indent=2))
print(json.dumps(dict(passed=True,images=4,totalImageBytes=total)))
