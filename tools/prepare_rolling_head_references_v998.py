"""Read-only checkpoint validation and unmodified/scaled artwork references."""
import hashlib
import json
import shutil
from pathlib import Path
from PIL import Image
import build_native_death_art_v900 as death

ROOT = death.ROOT
OUT = ROOT/'art_native_rolling_heads_v998'
GENERATED = Path(r'C:\Users\kando\.codex\generated_images\01a054e7-3dff-78b2-ba5c-269642375adb')


def main():
    if OUT.exists():
        raise ValueError('Never replace artwork/evidence')
    checkpoint = json.loads((ROOT/'audit_v995_owned_torso_blood_checkpoint/checkpoint.json').read_text())
    for filename, wanted in checkpoint['inputHashes'].items():
        actual = hashlib.sha256(Path(filename).read_bytes()).hexdigest().upper()
        if actual != wanted:
            raise ValueError('Current checkpoint changed: '+filename)
    assert not checkpoint['fullPortAccepted']
    OUT.mkdir()
    records = {}
    for name, filename in (
            ('kano-heads-rejected-draft.png','exec-14c42040-f1e5-4ca7-aac0-f3e779eb686e.png'),
            ('sonya-heads-rejected-draft.png','exec-46c3685b-e723-4df3-9ed0-4535bf6ad815.png')):
        source = GENERATED/filename
        shutil.copy2(source,OUT/name)
        records[name] = dict(original=str(source),sha256=death.sha(source.read_bytes()),
                             selected=False,reason='incorrect diagonal orientations; not encoded')
    for fighter in ('kano','sonya'):
        path = ROOT/'art_native_death_v893'/f'{fighter}-heads.png'
        parts = death.components(path)
        assert len(parts)==7
        image=parts[0][1]
        image.resize((image.width*2,image.height*2),Image.Resampling.NEAREST).save(OUT/f'{fighter}-upright-reference-2x.png')
    sheet=Image.new('RGBA',(1536,512),(0,0,0,0))
    for column,pose in enumerate((2,4,6)):
        path=ROOT/'audit_v997_native_rolling_head_references'/f'liu-head-{pose}.png'
        image=Image.open(path).convert('RGBA')
        image=image.resize((image.width*12,image.height*12),Image.Resampling.NEAREST)
        sheet.alpha_composite(image,(column*512+(512-image.width)//2,(512-image.height)//2))
    sheet.save(OUT/'native-135-225-315-reference-12x.png')
    (OUT/'reference-review.json').write_text(json.dumps(dict(
        checkpointPinsValidated=len(checkpoint['inputHashes']),romWrites=0,
        nativeAngles=[0,90,135,180,225,270,315],
        existingKanoSourceMapping=[0,6,5,4,3,2,1],
        kanoMappingRuntimeAccepted=False,sonyaMissingAngles=[135,225,315],
        rejectedDrafts=records,fullPortAccepted=False),indent=2)+'\n')
    print(json.dumps(dict(validatedPins=len(checkpoint['inputHashes']),output=str(OUT),romWrites=0)))


if __name__=='__main__':
    main()
