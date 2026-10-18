"""Rebuild newer own-victim graphics after the independent impale prefix."""
import contextlib
import io
import json
from pathlib import Path
import build_arm_rip_assets as arm
import build_inflation_assets as inflation
import build_ingestion_assets as ingestion
from build_inflation_assets import sha

PORT=Path(__file__).resolve().parent
CHAIN=PORT.parent/'baseline/clean_program/graphics_chain'
prior=json.loads((PORT/'FINAL_GRAPHICS_REBUILD.json').read_text())
assert prior['independentAddedBankChainVerified'] and prior['allComparedBytesIdentical']
prefix=CHAIN/'generated_impale/fighter_ui_finish_impale_graphics.bin'
assert sha(prefix.read_bytes())==prior['finalAddedBankSHA256']
stages=[]
for module,folder,assembly,packed_name,options in (
    (arm,'generated_arm_rip','KSARART.ASM','fighter_ui_finish_arm_graphics.bin',{}),
    (inflation,'generated_inflation_v3','KSINFART.ASM','fighter_ui_finish_inflate_graphics.bin',
     dict(source_root=PORT/'assets/inflation_v3')),
    (ingestion,'generated_ingestion','KSINART.ASM','fighter_ui_finish_ingest_graphics.bin',dict(emit_sockets=False))):
    output=CHAIN/folder
    assert not output.exists(), 'Never overwrite an independent rebuild'
    with contextlib.redirect_stdout(io.StringIO()):
        module.main(prefix_path=prefix,output=output,**options)
    comparisons=[]
    for name in (assembly,packed_name):
        data=(output/name).read_bytes()
        comparisons.append(dict(file=name,SHA256=sha(data),identical=data==(PORT/folder/name).read_bytes()))
    packed=(output/packed_name).read_bytes()
    region=packed+bytes(0x600000-len(packed))
    for bank,size in ((0,0x100000),(1,0x80000)):
        for lane in range(4):
            chip=121-bank*4-lane
            name=f'l1_mortal_kombat_3_u{chip}_game_rom.u{chip}'
            start=bank*0x400000+lane
            data=region[start:start+size*4:4]
            comparisons.append(dict(file=name,SHA256=sha(data),identical=data==(PORT/folder/name).read_bytes()))
    assert all(c['identical'] for c in comparisons), folder
    assert not list(output.glob('*.u*')), 'No duplicate physical sockets should be written'
    stages.append(dict(stage=folder,files=comparisons,byteIdentical=True))
    prefix=output/packed_name
report=dict(scope='Independent arm-rip/inflation/ingestion regeneration after clean impale prefix',
    stages=stages,allComparedBytesIdentical=True,independentAddedBankChainVerified=True,
    priorReportSHA256=sha((PORT/'FINAL_GRAPHICS_REBUILD.json').read_bytes()),
    finalAddedBankSHA256=sha(prefix.read_bytes()),finalAddedBankBytes=prefix.stat().st_size,
    finalPackedRelativePath=str(prefix.relative_to(CHAIN)),
    duplicateSocketFilesWritten=False,gameplayAcceptanceImplied=False,releaseReady=False)
(PORT/'OWN_VICTIM_GRAPHICS_REBUILD.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items() if k!='stages'},indent=2))
