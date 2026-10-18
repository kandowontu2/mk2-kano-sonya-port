"""Finish the independently regenerated graphics chain without socket copies."""
import contextlib
import hashlib
import io
import json
from pathlib import Path
import zipfile
import build_torso_assets as torso
import build_nut_assets as nut
import build_impale_assets as impale
import import_character_art as art

PORT=Path(__file__).resolve().parent
CLEAN=PORT.parent/'baseline/clean_program'
CHAIN=CLEAN/'graphics_chain'
sha=lambda b:hashlib.sha256(b).hexdigest().upper()
prior=json.loads((PORT/'HEAD_CHAIN_REBUILD.json').read_text())
assert prior['allComparedBytesIdentical']
drain=next(stage for stage in prior['stages'] if stage['stage']=='generated_drain')
for item in drain['files']:
    if item['file'].endswith(('.ASM','.bin')):
        assert sha((CHAIN/'generated_drain'/item['file']).read_bytes())==item['SHA256']
# Verify the art palette extraction input is still exactly the original ROM.
with zipfile.ZipFile(art.ROOT/'mk3.zip') as z:
    program=bytearray(1048576);program[::2]=z.read('mk321u54.bin');program[1::2]=z.read('mk321u63.bin')
assert bytes(program)==(art.ROOT/'mk3/mk3-maincpu.bin').read_bytes()
assert sha(program)=='1BC7A53A023F15B20F01398F87E38478A27C670DF27EA320E36125D0957EE651'
with zipfile.ZipFile('C:/Users/kando/Downloads/mk2-rebuild-main.zip') as z:
    native=z.read('mk2-rebuild-main/src/MKLK.ASM').replace(b'\r\n',b'\n')
assert native==(PORT.parent/'baseline/mk2-rebuild-main/srcw/MKLK.ASM').read_bytes().replace(b'\r\n',b'\n')
for actor in ('KANO','SONYA'):
    assert (CLEAN/f'srcp/{actor}ANI.ASM').read_bytes()==(PORT/f'generated_templates_candidate/{actor}ANI.ASM').read_bytes()
prefix=CHAIN/'generated_drain/fighter_ui_finish_drain_graphics.bin'
stages=[]
for module,folder,asm,packed,source_folder in (
    (torso,'generated_torso','KSTRART.ASM','fighter_ui_finish_torso_graphics.bin',None),
    (nut,'generated_nut','KSNUTART.ASM','fighter_ui_finish_nut_graphics.bin','nut_sources'),
    (impale,'generated_impale','KSIMART.ASM','fighter_ui_finish_impale_graphics.bin','impale_sources')):
    output=CHAIN/folder;assert not output.exists()
    options=dict(prefix_path=prefix,output=output,emit_sockets=False)
    if source_folder:
        options['source_output']=CHAIN/source_folder
    else:
        options['template_root']=CLEAN/'srcp'
    with contextlib.redirect_stdout(io.StringIO()):
        module.main(**options)
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
report=dict(scope='Final torso/nut/impale stages from independently regenerated drain prefix',
    stages=stages,allComparedBytesIdentical=all(stage['byteIdentical'] for stage in stages),
    finalAddedBankSHA256=sha(prefix.read_bytes()),finalAddedBankBytes=prefix.stat().st_size,
    independentAddedBankChainVerified=True,intermediateSocketFilesWritten=False,
    originalMK2SocketCopyAuditIncluded=False,fullGraphicsRebuildVerified=False,
    gameplayAcceptanceImplied=False,releaseReady=False)
(PORT/'FINAL_GRAPHICS_REBUILD.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({key:value for key,value in report.items() if key!='stages'},indent=2))
assert report['allComparedBytesIdentical']
