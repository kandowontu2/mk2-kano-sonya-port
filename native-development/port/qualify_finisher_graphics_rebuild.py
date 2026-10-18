"""Continue independently regenerated fighter/portrait prefixes through finishers."""
import contextlib
import hashlib
import io
import json
import os
from pathlib import Path
import generate_finisher_assets as finishers
import generate_kiss_data as kiss
import generate_baby_data as baby
import generate_hud_names as names
import generate_friendship_data as friendship

PORT=Path(__file__).resolve().parent
CLEAN=PORT.parent/'baseline/clean_program'
CHAIN=CLEAN/'graphics_chain'
if CHAIN.exists():
    assert set(path.name for path in CHAIN.iterdir())<={'generated_packed','generated_ui_packed','generated_finishers','generated_kiss','generated_baby','generated_names','generated_friendship','generated_pit','generated_backbreak','generated_heads','generated_decap','generated_drain','generated_torso','generated_nut','generated_impale','nut_sources','impale_sources'}
sha=lambda b:hashlib.sha256(b).hexdigest().upper()
fighter=json.loads((PORT/'FIGHTER_SOURCE_REBUILD.json').read_text())
portrait=json.loads((PORT/'SELECTOR_SOURCE_REBUILD.json').read_text())
assert fighter['nativeDataByteIdentical'] and portrait['portraitsNativeDataByteIdentical']
for receipt,folder in ((fighter,CLEAN/'graphics_fighters'),(portrait,CLEAN/'graphics_ui')):
    for item in receipt['files']:
        assert sha((folder/item['file']).read_bytes())==item['SHA256']
body=(CLEAN/'graphics_fighters/fighter_graphics.bin').read_bytes()
ui=(CLEAN/'graphics_ui/fighter_and_ui_graphics.bin').read_bytes()
assert ui.startswith(body)
CHAIN.mkdir(exist_ok=True);(CHAIN/'generated_packed').mkdir(exist_ok=True);(CHAIN/'generated_ui_packed').mkdir(exist_ok=True)
for source,destination in (
    (CLEAN/'graphics_fighters/SONYAART.ASM',CHAIN/'generated_packed/SONYAART.ASM'),
    (CLEAN/'graphics_ui/fighter_and_ui_graphics.bin',CHAIN/'generated_ui_packed/fighter_and_ui_graphics.bin')):
    if destination.exists():
        assert destination.read_bytes()==source.read_bytes()
    else:
        os.link(source,destination)
stages=[]
for module,folder,packed,metadata,assemblies in (
    (finishers,'generated_finishers','fighter_ui_finish_graphics.bin','FINISHER_ASSETS.json',['KSFART.ASM','KSFANI.ASM']),
    (kiss,'generated_kiss','fighter_ui_finish_kiss_graphics.bin','KISS_DATA.json',['KSKSANI.ASM']),
    (baby,'generated_baby','fighter_ui_finish_baby_graphics.bin','BABY_DATA.json',['KSBABART.ASM']),
    (names,'generated_names','fighter_ui_finish_names_graphics.bin','NAMES_DATA.json',['KSNAMES.ASM']),
    (friendship,'generated_friendship','fighter_ui_finish_friend_graphics.bin','FRIEND_DATA.json',['KSFRART.ASM'])):
    module.HERE=CHAIN
    if module is names:
        module.SRC=CLEAN/'srcp'
    existing=CHAIN/folder
    reuse=existing.exists()
    if reuse:
        assert all(path.is_file() and (PORT/folder/path.name).is_file()
            and path.read_bytes()==(PORT/folder/path.name).read_bytes() for path in existing.iterdir())
    with contextlib.redirect_stdout(io.StringIO()):
        module.main(emit_sockets=False,reuse_generated=reuse)
    generated=CHAIN/folder;current=PORT/folder
    comparisons=[]
    for name in [packed,*assemblies]:
        data=(generated/name).read_bytes()
        comparisons.append(dict(file=name,SHA256=sha(data),identical=data==(current/name).read_bytes()))
    image=(generated/packed).read_bytes()
    region=image+bytes(0x600000-len(image))
    socket_results=[]
    for bank,size in ((0,0x100000),(1,0x80000)):
        for lane in range(4):
            chip=121-bank*4-lane;name=f'l1_mortal_kombat_3_u{chip}_game_rom.u{chip}'
            start=bank*0x400000+lane
            payload=region[start:start+size*4:4]
            socket_results.append(dict(file=name,SHA256=sha(payload),identical=payload==(current/name).read_bytes()))
    stages.append(dict(stage=folder,files=comparisons,sockets=socket_results,
        identical=all(item['identical'] for item in comparisons+socket_results)))
report=dict(scope='Regenerated fighter/portrait prefix through finishers, kiss, baby, HUD names and friendship',
    stages=stages,allComparedBytesIdentical=all(stage['identical'] for stage in stages),
    intermediateSocketFilesWritten=False,completeGraphicsRebuildVerified=False,
    gameplayAcceptanceImplied=False,releaseReady=False)
(PORT/'FINISHER_GRAPHICS_REBUILD.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(dict(stages=[dict(stage=stage['stage'],identical=stage['identical']) for stage in stages],
    intermediateSocketFilesWritten=False,completeGraphicsRebuildVerified=False),indent=2))
assert report['allComparedBytesIdentical']
