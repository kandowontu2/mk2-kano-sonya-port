"""Independent morph encoding after the independently rebuilt split prefix."""
import contextlib
import io
import json
from pathlib import Path
from build_inflation_assets import sha
import build_morph_assets as morph

PORT=Path(__file__).resolve().parent
CHAIN=PORT.parent/'baseline/clean_program/graphics_chain'
prior_path=PORT/'SPLIT_GRAPHICS_REBUILD.json'
prior=json.loads(prior_path.read_text())
assert prior['independentAddedBankChainVerified'] and prior['allComparedBytesIdentical']
prefix=CHAIN/prior['finalPackedRelativePath']
assert sha(prefix.read_bytes())==prior['finalAddedBankSHA256']
output=CHAIN/'generated_morph'
assert not output.exists(),'Never overwrite an independent rebuild'
with contextlib.redirect_stdout(io.StringIO()):
    morph.main(prefix_path=prefix,output=output,emit_sockets=False)
comparisons=[]
for name in ('KSMOART.ASM','fighter_ui_finish_morph_graphics.bin'):
    data=(output/name).read_bytes()
    comparisons.append(dict(file=name,SHA256=sha(data),identical=data==(PORT/'generated_morph'/name).read_bytes()))
packed=(output/'fighter_ui_finish_morph_graphics.bin').read_bytes()
region=packed+bytes(0x600000-len(packed))
for bank,size in ((0,0x100000),(1,0x80000)):
    for lane in range(4):
        chip=121-bank*4-lane;start=bank*0x400000+lane
        name=f'l1_mortal_kombat_3_u{chip}_game_rom.u{chip}'
        data=region[start:start+size*4:4]
        comparisons.append(dict(file=name,SHA256=sha(data),identical=data==(PORT/'generated_morph'/name).read_bytes()))
assert all(item['identical'] for item in comparisons)
assert not list(output.glob('*.u*'))
report=dict(scope='Independent morph graphics regeneration from editable indexed sources and palette words',
    files=comparisons,allComparedBytesIdentical=True,independentAddedBankChainVerified=True,
    priorReportSHA256=sha(prior_path.read_bytes()),finalAddedBankSHA256=sha(packed),
    finalAddedBankBytes=len(packed),finalPackedRelativePath=str((output/'fighter_ui_finish_morph_graphics.bin').relative_to(CHAIN)),
    duplicateSocketFilesWritten=False,gameplayAcceptanceImplied=False,releaseReady=False)
(PORT/'MORPH_GRAPHICS_REBUILD.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items() if k!='files'},indent=2))
