"""Rebuild head/decap/drain art from indexed sources and clean prior bank."""
import contextlib
import hashlib
import io
import json
from pathlib import Path
import build_head_assets as heads

PORT=Path(__file__).resolve().parent
CHAIN=PORT.parent/'baseline/clean_program/graphics_chain'
sha=lambda b:hashlib.sha256(b).hexdigest().upper()
prior=json.loads((PORT/'PIT_BACKBREAK_REBUILD.json').read_text())
assert prior['allComparedBytesIdentical']
backbreak=next(stage for stage in prior['stages'] if stage['stage']=='generated_backbreak')
for item in backbreak['files']:
    if item['file'].endswith(('.ASM','.bin')):
        assert sha((CHAIN/'generated_backbreak'/item['file']).read_bytes())==item['SHA256']
prefix=CHAIN/'generated_backbreak/fighter_ui_finish_backbreak_graphics.bin'
stages=[]
for mode,folder,asm,packed in (
    ('head','generated_heads','KSHDART.ASM','fighter_ui_finish_heads_graphics.bin'),
    ('decap','generated_decap','KSDCART.ASM','fighter_ui_finish_decap_graphics.bin'),
    ('drain','generated_drain','KSDRART.ASM','fighter_ui_finish_drain_graphics.bin')):
    output=CHAIN/folder;assert not output.exists()
    with contextlib.redirect_stdout(io.StringIO()):
        heads.main(mode_override=mode,prefix_path=prefix,output=output,emit_sockets=False)
    comparisons=[]
    for name in (asm,packed):
        data=(output/name).read_bytes()
        comparisons.append(dict(file=name,SHA256=sha(data),identical=data==(PORT/folder/name).read_bytes()))
    image=(output/packed).read_bytes();region=image+bytes(0x600000-len(image))
    for bank,size in ((0,0x100000),(1,0x80000)):
        for lane in range(4):
            chip=121-bank*4-lane;name=f'l1_mortal_kombat_3_u{chip}_game_rom.u{chip}'
            start=bank*0x400000+lane;payload=region[start:start+size*4:4]
            comparisons.append(dict(file=name,SHA256=sha(payload),identical=payload==(PORT/folder/name).read_bytes()))
    stages.append(dict(stage=folder,files=comparisons,byteIdentical=all(item['identical'] for item in comparisons)))
    assert stages[-1]['byteIdentical'],folder
    prefix=output/packed
report=dict(scope='Head/decap/drain source data regenerated from clean backbreaker prefix',
    stages=stages,allComparedBytesIdentical=all(stage['byteIdentical'] for stage in stages),
    independentIndexDecodeVerified=True,intermediateSocketFilesWritten=False,
    completeGraphicsRebuildVerified=False,gameplayAcceptanceImplied=False,releaseReady=False)
(PORT/'HEAD_CHAIN_REBUILD.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(dict(stages=[stage['stage'] for stage in stages],allComparedBytesIdentical=report['allComparedBytesIdentical'],
    intermediateSocketFilesWritten=False,completeGraphicsRebuildVerified=False),indent=2))
assert report['allComparedBytesIdentical']
