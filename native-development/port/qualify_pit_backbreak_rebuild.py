"""Continue clean graphics chain through readonly authored Pit/backbreaker sources."""
import hashlib
import json
from pathlib import Path
import build_pit_assets as pit
import rebuild_backbreak_data as backbreak

PORT=Path(__file__).resolve().parent
CHAIN=PORT.parent/'baseline/clean_program/graphics_chain'
prior=json.loads((PORT/'FINISHER_GRAPHICS_REBUILD.json').read_text())
assert prior['allComparedBytesIdentical']
friend=next(stage for stage in prior['stages'] if stage['stage']=='generated_friendship')
for item in friend['files']:
    assert hashlib.sha256((CHAIN/'generated_friendship'/item['file']).read_bytes()).hexdigest().upper()==item['SHA256']
stages=[]
prefix=CHAIN/'generated_friendship/fighter_ui_finish_friend_graphics.bin'
for folder,builder,packed in (
    ('generated_pit',pit.build,'fighter_ui_finish_pit_graphics.bin'),
    ('generated_backbreak',backbreak.build,'fighter_ui_finish_backbreak_graphics.bin')):
    output=CHAIN/folder;assert not output.exists()
    outputs,source_report=builder(prefix)
    comparisons=[]
    for name,data in outputs.items():
        if name.endswith('.json'):continue  # Provenance formatting can differ.
        comparisons.append(dict(file=name,SHA256=hashlib.sha256(data).hexdigest().upper(),
            identical=data==(PORT/folder/name).read_bytes()))
    assert all(item['identical'] for item in comparisons),folder
    output.mkdir()
    # Persist only the small ASM/packed image/metadata, not eight socket copies.
    for name,data in outputs.items():
        if not name.endswith(tuple(f'.u{i}' for i in range(114,122))):
            (output/name).write_bytes(data)
    stages.append(dict(stage=folder,files=comparisons,sourceReport=source_report,byteIdentical=True))
    prefix=output/packed
report=dict(scope='Authored PGM Pit and backbreaker stages from regenerated friendship prefix',
    stages=stages,allComparedBytesIdentical=True,intermediateSocketFilesWritten=False,
    completeGraphicsRebuildVerified=False,gameplayAcceptanceImplied=False,releaseReady=False)
(PORT/'PIT_BACKBREAK_REBUILD.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(dict(stages=[stage['stage'] for stage in stages],allComparedBytesIdentical=True,
    intermediateSocketFilesWritten=False,completeGraphicsRebuildVerified=False),indent=2))
