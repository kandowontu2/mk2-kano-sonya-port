"""Check generated fatality DATA and native assembly, not game implementation."""
import json
from pathlib import Path
import re
from generate_finisher_assets import HERE
from import_character_art import sha

def main():
    output=HERE/'generated_finishers'
    build=HERE.parent/'baseline/mk2-rebuild-main'
    src=build/'srcp'
    report=json.loads((output/'FINISHER_ASSETS.json').read_text())
    assert (build/'FOK.TXT').read_text().strip()=='DONE'
    assert not (build/'FFAIL.TXT').exists()
    pins={}
    for module,logname,key in [('KSFART','FART','sourceSHA256'),('KSFANI','FANI','animationSourceSHA256')]:
        original=output/f'{module}.ASM';assembled=src/f'{module}.ASM'
        assert sha(original.read_bytes())==sha(assembled.read_bytes())==report[key]
        text=original.read_text()
        assert not re.search(r'^\s*\.text\b',text,re.M|re.I)
        log=build/f'{logname}.LOG';obj=src/f'{module}.OBJ'
        assert re.search(r'No Errors,\s+No Warnings',log.read_text())
        assert obj.stat().st_size>0 and obj.stat().st_mtime>=assembled.stat().st_mtime
        for path in [original,assembled,log,obj]:pins[str(path)]=sha(path.read_bytes())
    graphics=(output/'fighter_ui_finish_graphics.bin').read_bytes()
    prefix=(HERE/'generated_ui_packed/fighter_and_ui_graphics.bin').read_bytes()
    assert graphics[:len(prefix)]==prefix
    assert len(graphics)==report['totalGraphicsBytes']<=0x600000
    region=bytearray(0x600000)
    for bank,size in [(0,0x100000),(1,0x80000)]:
        for lane in range(4):
            chip=121-bank*4-lane;name=f'l1_mortal_kombat_3_u{chip}_game_rom.u{chip}'
            raw=(output/name).read_bytes()
            assert len(raw)==size and sha(raw)==report['sockets'][name]
            start=bank*0x400000+lane
            region[start:start+size*4:4]=raw
    assert region==graphics+bytes(0x600000-len(graphics))
    for frame in report['framePins']:
        start=frame['packedByteOffset'];size=(frame['bits']+7)//8
        assert sha(graphics[start:start+size])==frame['SHA256']
    for path in [Path(__file__),HERE/'generate_finisher_assets.py',output/'FINISHER_ASSETS.json',
                 build/'FASM.BAT',HERE/'dosbox-finish.conf']:
        pins[str(path)]=sha(path.read_bytes())
    result=dict(scope='finisher typed data generation, native assembly and graphics socket round-trip only',
                compositePoses=report['compositePoses'],frameRecords=report['frameRecords'],
                nativeModulesAssembled=['KSFART','KSFANI'],nativeAssemblerErrors=0,nativeAssemblerWarnings=0,
                existingGraphicsPreserved=True,standardWolfSockets=True,
                programLinked=False,finisherActionsImplemented=False,runtimeVerified=False,
                releaseReady=False,pins=pins)
    (output/'ASSEMBLY_CHECK.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='pins'},indent=2))

if __name__=='__main__':main()
