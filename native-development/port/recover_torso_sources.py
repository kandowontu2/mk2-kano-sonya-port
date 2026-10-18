"""Preserve authored torso sprites/guides without importing legacy game code."""
import json
from pathlib import Path
from PIL import Image
from generate_head_sources import PORT,sha
import import_character_art as art
OUT=PORT/'assets/torso_sources'
FILES=(
 ('art_native_torso_v951','kano-upper-torsos.png','8728BE7511E511B1FA2D3582F63C8422FB636AF2EDE04BB3387BA14D9A620F6E'),
 ('art_native_torso_v951','sonya-upper-torsos.png','1E3CF3FE88077D8FB5053435F818B504537D11F499D3B8DF75ED8D0C9586639C'),
 ('art_native_torso_v951','lower-stumps.png','F17F2528885C2E751965A7E9634CFA2358DB833A2A84C87F2577468730828DE0'),
 ('art_native_torso_blood_v976','kano-upper-blood-guide.png','14E02525A7E0B6167054D4C88B35EAEA3F3DC40535B18B42EFAE1FB01FF9E297'),
 ('art_native_torso_blood_v976','lower-blood-guide.png','39C4CEF599A4846FAE393F9311E59857EFBAE0FA0900849D1B7126D0CA23F37E'))

def main():
    assert not OUT.exists(),'Do not overwrite preserved authored inputs'
    OUT.mkdir()
    records=[]
    for folder,name,expected in FILES:
        raw=(art.ROOT/folder/name).read_bytes()
        assert sha(raw)==expected
        (OUT/name).write_bytes(raw)
        with Image.open(OUT/name) as image:
            records.append(dict(file=name,source=folder+'/'+name,SHA256=expected,
                                mode=image.mode,size=list(image.size)))
    manifest=dict(format='MK2KS-TORSO-AUTHORED-INPUTS-1',assets=records,
        upperCellSize=[512,512],upperColumns=3,upperRows=2,upperPosesPerActor=6,
        lowerCellSize=[627,1254],lowerColumns=2,
        bloodGuideMeaning='Cyan regions classify authored red wound pixels, not costume red',
        nativeRootIndex=57,generatedROMData=False,runtimeVerified=False,fullPortVerified=False)
    (OUT/'TORSO_INPUTS.json').write_text(json.dumps(manifest,indent=2)+'\n')
    print(json.dumps(dict(preservedAssets=len(records),generatedROMData=False)))

if __name__=='__main__':main()
