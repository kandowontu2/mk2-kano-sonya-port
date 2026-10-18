"""Freshly derive ending art from donor ROMs; compare and remove temp outputs."""
import hashlib
import json
from pathlib import Path
import tempfile
from build_ending_art import build,PORT

sha=lambda data:hashlib.sha256(data).hexdigest().upper()
checks=[]
clean=PORT.parent/'baseline/clean_program'
prior_path=PORT/'MORPH_GRAPHICS_REBUILD.json'
prior=json.loads(prior_path.read_text())
assert prior['independentAddedBankChainVerified']
prefix_path=clean/'graphics_chain'/prior['finalPackedRelativePath']
assert sha(prefix_path.read_bytes())==prior['finalAddedBankSHA256']
with tempfile.TemporaryDirectory(prefix='ending-art-check-',dir=PORT.parent/'baseline') as temporary:
    target=Path(temporary)/'ending'
    regenerated=build(target,prefix_path)
    for name in ('KSENDART.ASM','fighter_ui_finish_ending_graphics.bin',
                 'kano_page1.png','kano_page2.png','sonya_page1.png','sonya_page2.png'):
        data=(target/name).read_bytes()
        assert data==(PORT/'generated_ending'/name).read_bytes(),name
        checks.append(dict(file=name,SHA256=sha(data),identical=True))
    published=clean/'graphics_chain/generated_ending'
    published.mkdir(exist_ok=True)
    for name in ('KSENDART.ASM','fighter_ui_finish_ending_graphics.bin'):
        destination=published/name;data=(target/name).read_bytes()
        if destination.exists():assert destination.read_bytes()==data,'Refusing to overwrite changed clean graphics'
        else:destination.write_bytes(data)
report=dict(scope='Independent ending append-stage regeneration from original donor graphics and unchanged morph prefix',
    files=checks,sourcePhotoCount=2,pages=4,temporaryOutputsRemoved=True,
    earlierGraphicsChainIndependentlyRebuilt=True,independentAddedBankChainVerified=True,
    priorReportSHA256=sha(prior_path.read_bytes()),
    finalPackedRelativePath='generated_ending/fighter_ui_finish_ending_graphics.bin',
    finalAddedBankSHA256=regenerated['packedSHA256'],runtimeVerified=False,releaseReady=False)
(PORT/'ENDING_ART_REBUILD_QUALIFICATION.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
