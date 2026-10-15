"""Match OWN shrinking feet to actual stock phase anchors, not stance anchors.

Stage/qualify a coordinate-only successor of the actually compiled repair.
No bitmap edits, ROM writes, native game launches, source overwrites or release
promotion. The ongoing original campaign is unchanged. Full goal remains open.
"""
import hashlib
import json
import struct
import subprocess
from pathlib import Path

import upgrade_ksui_previews as decode
import verify_native_shang_drain_startup as initial
import verify_native_shang_drain_startup_successor as corrected

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'audit_native_shang_drain_anchors_source'
STAGE=ROOT/'source_native_shang_drain_anchors'
BASE=ROOT/'source_native_shang_owned_drain'
ASSETS=ROOT/'art_native_shang_drain_encoded_v1/asset-report.json'
COMPILER=Path('C:/Strawberry/c/bin/g++.exe')
STOCK_FRAMES=(0xffbf0db0,0xffbf18b0,0xffbf1920)
FRAME_BYTES=(0xb10c0,0xb10d4,0xb10e8,0xb10fc,0xb1110,0xb1124)


def need(value,reason):
    if not value:raise ValueError(reason)


def digest(data):
    return hashlib.sha256(data).hexdigest().upper()


def sha(path):
    return digest(Path(path).read_bytes())


def stock_anchors():
    program_path=ROOT/'mk2/mk2-maincpu.bin';program=program_path.read_bytes()
    need(digest(program)=='45B3285496DB555EFAF4A3608A4F59845DD47A82E4A0593607E0592F47B36F23', 'Exact original stock program')
    pins={str(program_path):digest(program)}
    gfx=bytearray(0xc00000)
    for bank,pair in enumerate(((14,19),(16,20),(17,22))):
        for lane,(side,chip) in enumerate((('g',pair[0]),('j',pair[0]),('g',pair[1]),('j',pair[1]))):
            path=ROOT/'mk2'/f'l1_mortal_kombat_ii_game_rom_u{side}{chip}.u{side}{chip}'
            data=path.read_bytes();need(len(data)==0x100000,'Whole original stock graphics chip')
            pins[str(path)]=digest(data)
            gfx[bank*0x400000+lane:bank*0x400000+lane+0x400000:4]=data
    reference=json.loads((ROOT/'art_reference_native_shang_drain/reference.json').read_text())
    need(reference['passed'] and all(reference['inputHashes'][p]==h for p,h in pins.items()), 'Original decoded reference binds every actual graphics byte')
    u32=lambda at:struct.unpack_from('<I',program,(at-0xff800000)//8)[0]
    stream=u32(0xff9d7770+32)
    groups=struct.unpack_from('<9I',program,(stream-0xff800000)//8)
    need(groups[3]==groups[8]==0 and groups[4:8]==(groups[1],groups[0],groups[1],groups[2]) and
         tuple(u32(g)for g in groups[:3])==STOCK_FRAMES and all(u32(g+32)==0 for g in groups[:3]),
         'Original six/eight-field stock choreography and three single-descriptor composites')
    palette=[(0,0,0,0)]+[(255,255,255,255)]*255
    rows=[]
    for phase,address in enumerate(STOCK_FRAMES):
        spec=decode.component_spec(program,address)
        image=decode.decode_component(gfx,palette,*spec[:4])
        feet=[x for x in range(image.width)if any(image.getpixel((x,y))[3]for y in range(image.height-3,image.height))]
        need(feet and image.getbbox()==(0,0,spec[2],spec[3]),'Actual stock opaque foot band and full bitmap bounds')
        foot=round((min(feet)+max(feet))/2)
        rows.append(dict(phase=phase,descriptor=address,width=spec[2],height=spec[3],xOffset=spec[4],yOffset=spec[5],
                         opaqueFootXs=feet,footCenter=foot,nativeFootX=foot-spec[4],nativeBottom=spec[3]-spec[5],
                         actualStockRGBASHA256=digest(image.tobytes()),graphicsSourceBits=spec[0],command=spec[1]))
    need([r['nativeFootX']for r in rows]==[14,16,17] and [r['nativeBottom']for r in rows]==[120,116,112],
         'Independent actual stock foot trajectories, not zero-centred standing anchors')
    return rows,pins


def fragment(asset,stock):
    old_rows=[r for fighter in asset['fighters']for r in fighter['frames']]
    new_rows=[]
    for i,row in enumerate(old_rows):
        anchor=stock[i%3]
        need(row['height']==anchor['height'] and row['xOffset']==row['plantedFootCenter'] and
             row['height']-row['yOffset']==(139 if i<3 else 140),'Exact old standing-coordinate assumption identified')
        x=row['plantedFootCenter']-anchor['nativeFootX'];y=row['height']-anchor['nativeBottom']
        new_rows.append(dict(identity=17+i//3,phase=i%3,descriptor=0xff800000+FRAME_BYTES[i]*8,
                             previousX=row['xOffset'],previousY=row['yOffset'],x=x,y=y,
                             matchedNativeFootX=anchor['nativeFootX'],matchedNativeBottom=anchor['nativeBottom']))
    need([r['x']for r in new_rows]==[6,4,2,12,8,4] and [r['y']for r in new_rows]==[5,3,1,5,3,1], 'Both own identity-specific foot centres match stock anchors')
    spec=lambda row:'{'+','.join(str(row[k])for k in ('width','height','xOffset','yOffset'))+'}'
    snippet='''
    // SHANG_OWNED_DRAIN_ANCHORS_BEGIN
    // These shrinking sprites have stock125/119/113 heights, but their
    // old normal-stance139/140 bottoms caused a jump to the native skeleton.
    // Match actual stock opaque-foot trajectories14/16/17 and120/116/112.
    // Native DMA retains mirroring; own bitmap/palette/timing/skeleton unchanged.
    constexpr int16_t shrink_old_geometry[6][4]={OLD};
    constexpr int16_t shrink_new_offsets[6][2]={NEW};
    constexpr unsigned shrink_stock_frames[3]={0xffbf0db0,0xffbf18b0,0xffbf1920};
    constexpr int16_t shrink_stock_geometry[3][4]={{49,125,-2,5},{50,119,-2,3},{50,113,-3,1}};
    for(unsigned phase=0;phase<3;phase++)
        for(unsigned word=0;word<4;word++)
            if(read16(rom_offset(shrink_stock_frames[phase])+word*2)!=uint16_t(shrink_stock_geometry[phase][word]))
                fatalerror("MK2KS: original native shrinking anchor changed");
    // Validate ALL old descriptors before writing either character.
    for(unsigned pose=0;pose<6;pose++)
        for(unsigned word=0;word<4;word++)
            if(read16(0xb10c0+pose*20+word*2)!=uint16_t(shrink_old_geometry[pose][word]))
                fatalerror("MK2KS: original owned shrinking geometry changed");
    for(unsigned pose=0;pose<6;pose++){
        write16(0xb10c0+pose*20+4,uint16_t(shrink_new_offsets[pose][0]));
        write16(0xb10c0+pose*20+6,uint16_t(shrink_new_offsets[pose][1]));
    }
    // SHANG_OWNED_DRAIN_ANCHORS_END
'''.replace('{OLD}','{'+','.join(spec(r)for r in old_rows)+'}').replace('{NEW}','{'+','.join('{'+str(r['x'])+','+str(r['y'])+'}'for r in new_rows)+'}')
    return snippet,new_rows


def harness(snippet):
    return r'''
#include <cstdint>
#include <iostream>
#include <stdexcept>
#include <vector>
#include <io.h>
#include <fcntl.h>
void fatalerror(char const *s){throw std::runtime_error(s);}
int main(){
 _setmode(_fileno(stdin),_O_BINARY);_setmode(_fileno(stdout),_O_BINARY);
 std::vector<uint8_t> rom(0x100000);
 std::cin.read(reinterpret_cast<char*>(rom.data()),rom.size());if(!std::cin)return 2;
 auto rom_offset=[](uint32_t value){return(value-0xff800000U)/8;};
 auto read16=[&](unsigned at){return uint16_t(rom.at(at))|(uint16_t(rom.at(at+1))<<8);};
 auto write16=[&](unsigned at,uint16_t v){rom.at(at)=v;rom.at(at+1)=v>>8;};
 try{
''' + snippet + r'''
 }catch(std::exception const &e){std::cerr<<e.what();return 5;}
 std::cout.write(reinterpret_cast<char*>(rom.data()),rom.size());return std::cout?0:3;
}
'''


def main():
    need(not OUT.exists() and not STAGE.exists(), 'One fresh immutable coordinate successor')
    build_guard_path=ROOT/'audit_native_shang_drain_build_source/report.json'
    startup_path=ROOT/'audit_native_shang_drain_startup_successor/report.json'
    prefix_path=ROOT/'audit_native_shang_drain_preceding_campaign_checked/report.json'
    guard,startup,prefix=[json.loads(p.read_text())for p in (build_guard_path,startup_path,prefix_path)]
    need(guard['passed'] and startup['passed'] and prefix['passed'] and
         startup['actualNativeInitializedWindowsAccepted'] and prefix['accepted']['completeOriginalRows']==1009959,
         'Actually compiled repair/full native startup and entire original thirteen-fight replay')
    for proof in (guard,startup,prefix):
        need(not proof['fullPortAcceptance'] and all(sha(p)==h for p,h in proof['inputHashes'].items()),'All frozen original game/source evidence unchanged')
    for leaf,h in guard['stagedSourceHashes'].items():need(sha(BASE/leaf)==h, 'Exact actual current driver source')
    asset=json.loads(ASSETS.read_text());stock,pins=stock_anchors()
    snippet,rows=fragment(asset,stock)
    before_source=(BASE/'midtunit_m.cpp').read_text()
    anchor='    // SHANG_OWNED_DRAIN_END\n'
    need(before_source.count(anchor)==1,'Exact complete compiled drain-block end')
    after_source=before_source.replace(anchor,anchor+snippet,1)
    OUT.mkdir()
    (OUT/'independent_predecessor').mkdir()
    wanted=initial.expected(OUT/'independent_predecessor')
    wanted['owned'],_=corrected.expected_owned((ROOT/corrected.NAME/'roms/mk2ks/mk2ks.mdata').read_bytes())
    need({k:digest(v)for k,v in wanted.items()}==startup['actualWindowHashes'],'Whole independently initialized actual predecessor, including43 existing low bytes')
    after=bytearray(wanted['high'])
    for i,row in enumerate(rows):struct.pack_into('<hh',after,FRAME_BYTES[i]+4,row['x'],row['y'])
    changed=[i for i,(a,b)in enumerate(zip(wanted['high'],after))if a!=b]
    allowed={at+byte for at in FRAME_BYTES for byte in (4,5,6,7)}
    need(len(changed)==18 and set(changed)<=allowed,'Only six X/Y offsets; every other program byte conserved')
    probe=OUT/'anchor_initializer_probe.exe';cpp=harness(snippet)
    built=subprocess.run([str(COMPILER),'-std=c++17','-O1','-Wall','-Wextra','-Werror','-x','c++','-','-o',str(probe)],input=cpp,text=True,capture_output=True)
    need(built.returncode==0 and not built.stdout and not built.stderr,'Actual complete guarded coordinate fragment compiles warning-free')
    probe_hash=sha(probe)
    actual=subprocess.run([str(probe)],input=wanted['high'],capture_output=True)
    need(actual.returncode==0 and not actual.stderr and actual.stdout==after,'Actual C++ full1MiB output equals independent exact coordinate model')
    faults=[]
    for label,addresses in [('owned',FRAME_BYTES),('stock',[(pc-0xff800000)//8 for pc in STOCK_FRAMES])]:
        for i,at in enumerate(addresses):
            for word in range(4):
                bad=bytearray(wanted['high']);bad[at+word*2]^=1
                rejected=subprocess.run([str(probe)],input=bad,capture_output=True)
                need(rejected.returncode==5 and rejected.stderr and not rejected.stdout,'Actual pre-write guard rejects all changed geometry words')
                faults.append(f'{label}_{i}_word{word}')
    need(len(faults)==36 and probe.resolve().parent==OUT.resolve() and sha(probe)==probe_hash,'All36 actual malformed inputs rejected; exact temporary output terminal')
    retired=probe.stat().st_size;probe.unlink();need(not probe.exists(),'Small temporary compiler output retired')
    STAGE.mkdir()
    (STAGE/'native_shang_drain_anchors.inc').write_text(snippet)
    (STAGE/'midtunit_m.cpp').write_text(after_source)
    for leaf in ('midtunit.cpp','midtunit.h'):(STAGE/leaf).write_bytes((BASE/leaf).read_bytes())
    for p in (Path(__file__),Path(initial.__file__),Path(corrected.__file__),Path(decode.__file__),ASSETS,COMPILER,
              build_guard_path,startup_path,prefix_path,ROOT/'art_reference_native_shang_drain/reference.json',
              *(BASE/leaf for leaf in ('midtunit_m.cpp','midtunit.cpp','midtunit.h')),
              ROOT/'tools/read_live_shang_drain_frames.py',ROOT/'tools/read_live_shang_drain_frames_remote.py'):
        pins[str(p.resolve())]=sha(p)
    need(all(sha(p)==h for p,h in pins.items()),'Every original art/source/actual native proof unchanged')
    report=dict(passed=True,sourceOnlyAccepted=True,coordinateOnlyRepair=True,ownPixelsPalettesTimingSkeletonUnchanged=True,
        actualStockAnchors=stock,ownCoordinateRepair=rows,changedHighBytes=18,changedHighOffsets=[hex(i)for i in changed],
        proposedGuestSHA256=digest(after),proposedOwnedSHA256=digest(wanted['owned']),proposedNewGraphicsSHA256=digest(wanted['graphics']),
        actualCppWholeHighConservationAccepted=True,actualCppFaultsRejected=faults,
        retiredTemporaryCompilerOutputBytes=retired,inputHashes=pins,
        stagedSourceHashes={leaf:sha(STAGE/leaf)for leaf in ('midtunit_m.cpp','midtunit.cpp','midtunit.h','native_shang_drain_anchors.inc')},
        actualRuntimeBodyFrameSHA256='08A97CFD7FAEB5276FA14C904A12F21D4591066DE7264198457A94167F926C8F',
        actualRuntimeSkeletonFrameSHA256='CCF53610FFAED9F7AA37AA694EE8DCEE555C537427C40A450F0EFDA8B5C0AE84',
        visualFinding='Runtime v1 body/skeleton transition jumps. Its normal-stance foot centre0 and bottoms139/140 differ from actual stock phase foot centres14/16/17 and bottoms120/116/112.',
        newNativeBuilds=0,newROMCopies=0,newRawGameplayMedia=0,newZIPs=0,publicPlayableChanged=False,
        nativeRepairAccepted=False,artworkRuntimeAccepted=False,audioAccepted=False,fullPortAcceptance=False,
        originalNaturalIntegrationRequirements=guard['originalNaturalIntegrationRequirements'],
        originalRemainingWorkGroups=guard['originalRemainingWorkGroups'],goalStatus='active')
    (OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(passed=True,sourceOnlyAccepted=True,changedHighBytes=18,actualCppFaultsRejected=36,
                         proposedGuestSHA256=report['proposedGuestSHA256'],nativeRepairAccepted=False)),flush=True)
    return report


if __name__=='__main__':main()
