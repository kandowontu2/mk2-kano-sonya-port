"""Actual initializer conservation and opcodes for two CSS-only draw-order hooks."""
import gzip,json,re,struct,subprocess
from pathlib import Path
import verify_native_shang_drain_anchors_startup as startup

ROOT=startup.ROOT
OUT=ROOT/'audit_native_selector_layers_source'
STAGE=ROOT/'source_native_selector_layers'
BASE=ROOT/'source_native_shang_drain_anchors'
need,sha,digest=startup.initial.need,startup.initial.sha,startup.initial.digest
addr=lambda b:0xff800000+b*8
off=lambda a:(a-0xff800000)//8
PHOTO=0xf95a0
NUMBER=0xf95f0

def execute(high,pc,descriptor,z=0):
    a0=0x13572468;equal=False;stores=0
    for _ in range(12):
        op=struct.unpack_from('<H',high,off(pc))[0];pc+=16
        if op==0x0b65:
            immediate=struct.unpack_from('<I',high,off(pc))[0];pc+=32
            equal=descriptor==((~immediate)&0xffffffff)
        elif op in (0xca80,0xcb80,0xc080):
            target=struct.unpack_from('<I',high,off(pc))[0];pc+=32
            if op==0xc080 or (equal if op==0xca80 else not equal):
                if target==0xff83f610:return z,stores
                need(addr(PHOTO)<=target<addr(0xf9600),'Bounded generated selector branch')
                pc=target
        elif op==0x09c0:
            a0=struct.unpack_from('<h',high,off(pc))[0]&0xffffffff;pc+=16
        elif op==0xb308:
            field=struct.unpack_from('<H',high,off(pc))[0];pc+=16
            need(field==0xc0,'Only native sprite depth is written')
            z=a0;stores+=1
        else:raise ValueError('Unexpected actual helper instruction '+hex(op))
    raise ValueError('No exact original native registration tail')

def main():
    need(not OUT.exists(),'One fresh selector source proof')
    prior=json.loads((ROOT/'audit_native_shang_drain_anchors_startup/report.json').read_text())
    terminal=json.loads((ROOT/'audit_native_shang_anchor_terminal_checked/report.json').read_text())
    need(prior['passed'] and terminal['passed'] and terminal['sameOriginalNativeTerminal'] and
         terminal['finiteSonyaNormalShrinkingCrashAndOrdinaryRecoveryAccepted'] and
         not terminal['fullPortAcceptance'],'Actual preceding native initialization and terminal recovery')
    pins={}
    for proof in (prior,terminal):
        for p,h in proof['inputHashes'].items():
            need(sha(p)==h and (p not in pins or pins[p]==h),'Original frozen evidence '+p);pins[p]=h
    before=(BASE/'midtunit_m.cpp').read_text();source=(STAGE/'midtunit_m.cpp').read_text()
    begin='\t// NATIVE_SELECTOR_LAYERS_BEGIN\n';end='\t// NATIVE_SELECTOR_LAYERS_END\n'
    need(source.count(begin)==source.count(end)==1,'One additive CSS-only fragment')
    start=source.index(begin);finish=source.index(end)+len(end)
    fragment=source[start:finish]
    need(source[:start]+source[finish+1:]==before,'Every original source byte outside additive block unchanged')
    for leaf in ('midtunit.cpp','midtunit.h'):
        need((BASE/leaf).read_bytes()==(STAGE/leaf).read_bytes(),'All other driver bytes unchanged')
    OUT.mkdir();model=OUT/'independent_predecessor';model.mkdir()
    wanted=startup.expected(model);high=wanted['high'];expected=bytearray(high)
    photo_words=(0x0b65,0xd7ff,0,0xca80,addr(PHOTO+24)&65535,addr(PHOTO+24)>>16,
                 0x0b65,0xd6ff,0,0xcb80,addr(PHOTO+32)&65535,addr(PHOTO+32)>>16,
                 0x09c0,0x51,0xb308,0xc0,0xc080,0xf610,0xff83)
    number_words=(0x09c0,0x52,0xb308,0xc0,0xc080,0xf610,0xff83)
    struct.pack_into('<19H',expected,PHOTO,*photo_words)
    struct.pack_into('<7H',expected,NUMBER,*number_words)
    struct.pack_into('<I',expected,off(0xff894020),addr(PHOTO))
    struct.pack_into('<I',expected,off(0xff8965e0),addr(NUMBER))
    compiler=Path('C:/Strawberry/c/bin/g++.exe');probe=OUT/'initializer_probe.exe'
    harness=r'''
#include <cstdint>
#include <iostream>
#include <stdexcept>
#include <vector>
#include <initializer_list>
#include <io.h>
#include <fcntl.h>
void fatalerror(char const *s){throw std::runtime_error(s);}
int main(){
 _setmode(_fileno(stdin),_O_BINARY);_setmode(_fileno(stdout),_O_BINARY);
 std::vector<uint8_t> memory(0x100000);std::cin.read(reinterpret_cast<char*>(memory.data()),memory.size());if(!std::cin)return 2;
 uint8_t *const rom=memory.data();
 auto offset=[](uint32_t a){return(a-0xff800000U)/8;};
 auto address=[](unsigned b){return 0xff800000U+b*8;};
 auto read16=[](uint8_t const*p){return unsigned(p[0])|(unsigned(p[1])<<8);};
 auto read32=[&](unsigned b){return uint32_t(rom[b])|(uint32_t(rom[b+1])<<8)|(uint32_t(rom[b+2])<<16)|(uint32_t(rom[b+3])<<24);};
 auto word=[&](unsigned b,uint16_t v){rom[b]=v;rom[b+1]=v>>8;};
 auto longword=[&](unsigned b,uint32_t v){for(unsigned i=0;i<4;i++)rom[b+i]=v>>(i*8);};
 auto code=[&](unsigned b,std::initializer_list<uint16_t>w){for(auto v:w){word(b,v);b+=2;}};
 try{
'''+fragment+r'''
 }catch(std::exception const&e){std::cerr<<e.what();return 5;}
 std::cout.write(reinterpret_cast<char*>(rom),memory.size());return std::cout?0:3;
}
'''
    build=subprocess.run([str(compiler),'-std=c++17','-O1','-Wall','-Wextra','-Werror','-x','c++','-','-o',str(probe)],input=harness,text=True,capture_output=True)
    need(build.returncode==0 and not build.stdout and not build.stderr,'Actual guarded C++ fragment compiles warning-free')
    actual=subprocess.run([str(probe)],input=high,capture_output=True)
    need(actual.returncode==0 and not actual.stderr and actual.stdout==expected,'Actual full1MiB initializer equals independent CSS-only model')
    guards=list(range(PHOTO,0xf9600))+[off(a)+i for a in (0xff894010,0xff8965d0)for i in (0,2,4)]+[b+i for b in (0xfe500,0xfe520)for i in (0,2)]
    faults=[]
    for at in guards:
        bad=bytearray(high);bad[at]^=1
        result=subprocess.run([str(probe)],input=bad,capture_output=True)
        need(result.returncode==5 and result.stderr and not result.stdout,'Every actual guarded-byte mutation rejected')
        faults.append(hex(at))
    need(len(faults)==106,'All106 actual initializer guard faults rejected')
    codepath=OUT/'selector-layer-helpers.bin';codepath.write_bytes(expected[PHOTO:0xf9600])
    disassembler=ROOT/'mame-mkp/unidasm.exe'
    decoded=subprocess.run([str(disassembler),str(codepath),'-arch','tms34010','-basepc',hex(addr(PHOTO)),'-norawbytes'],capture_output=True,text=True)
    need(decoded.returncode==0 and not decoded.stderr and
         'CMPI   FFFF2800h,A5' in decoded.stdout and 'CMPI   FFFF2900h,A5' in decoded.stdout and
         decoded.stdout.count('MOVE   A0,*A8(C0h),1')==2 and
         decoded.stdout.count('JA     FF83F610h')==2,'Actual native decoder confirms two descriptor compares and long depth writes/original registration tails')
    (OUT/'selector-layer-helpers.disasm.txt').write_text(decoded.stdout)
    cases=[]
    descriptors=[struct.unpack_from('<I',high,0xfe480+i*8)[0]for i in range(14)]
    descriptors+=list(range(0xffff2700,0xffff2a01,16))+[0,0xffffffff,0x01000000,0xdeadbeef]
    for descriptor in descriptors:
        observed=execute(expected,addr(PHOTO),descriptor)
        correct=(0x51,1)if descriptor in (0xffff2800,0xffff2900)else(0,0)
        need(observed==correct,'Only two actual own CSS descriptors change photo depth')
        need(execute(expected,addr(NUMBER),descriptor)==(0x52,1),'All native CSS player numbers render above photos/bodies')
        cases.append(dict(descriptor=f'{descriptor:08X}',photo=observed,number=(0x52,1)))
    depth_path=ROOT/'audit_native_anchor_ui_depth_ram/sonya_p1_kano_p2_two/run.log.gz'
    observed=[dict(re.findall(r'(\w+)=([^\s]+)',line))for line in gzip.open(depth_path,'rt')if line.startswith('MK2_ANCHOR_UI_DEPTH ') and 'frame=938 'in line]
    need(len(observed)==18 and [r['z']for r in observed[:16]]==['00000000']*16 and
         [(r['id'],r['z'])for r in observed[-2:]]==[('0011','0000004F'),('0012','00000050')],
         'Actual confirmed photos/numbers precede own bodies; authoritative layering cause')
    failure=ROOT/'audit_native_anchor_ui_depth_ram/failure.json'
    need('Same original independent full campaign remains live' in failure.read_text(),'Preserve actual whole depth collector concurrent-terminal failure')
    probe_bytes=probe.stat().st_size;probe.unlink()
    for p in (Path(__file__),compiler,disassembler,codepath,depth_path,failure,
              ROOT/'mk2ks_native_anchor_ui_depth_ram.lua',ROOT/'tools/capture_native_anchor_ui_depth_ram.py',
              ROOT/'audit_native_shang_anchor_terminal_checked/report.json',ROOT/'audit_native_shang_drain_anchors_startup/report.json',
              *(BASE/leaf for leaf in ('midtunit_m.cpp','midtunit.cpp','midtunit.h'))):pins[str(p.resolve())]=sha(p)
    need(all(sha(p)==h for p,h in pins.items()),'All actual frozen evidence unchanged')
    report=dict(passed=True,sourceOnlyAccepted=True,nativeRuntimeAccepted=False,fullPortAcceptance=False,
        sourceAdditiveOnly=True,allOtherDriverBytesUnchanged=True,actualCppFullHighConservationAccepted=True,
        actualCppFaultsRejected=faults,helperModelCases=cases,actualPredecessorConfirmedNativeDepthRows=observed,
        onlyCSSCreationCallsChanged=['FF894010','FF8965D0'],ownPhotoDepth=81,nativeNumberDepth=82,
        stockPhotoAndBodyDepthUnchanged=True,gameplayAnimationGeometryAudioTeardownUnchanged=True,
        proposedGuestSHA256=digest(expected),proposedOwnedSHA256=digest(wanted['owned']),proposedNewGraphicsSHA256=digest(wanted['graphics']),
        changedHighBytes=sum(a!=b for a,b in zip(high,expected)),
        stagedSourceHashes={leaf:sha(STAGE/leaf)for leaf in ('midtunit_m.cpp','midtunit.cpp','midtunit.h')},inputHashes=pins,
        retiredTemporaryCompilerOutputBytes=probe_bytes,newNativeBoots=0,newROMCopies=0,newRawMedia=0,newZIPs=0,publicPlayableChanged=False,
        originalNaturalIntegrationRequirements=terminal['originalNaturalIntegrationRequirements'],originalRemainingWorkGroups=terminal['originalRemainingWorkGroups'],goalStatus='active')
    (OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(passed=True,sourceOnly=True,changedHighBytes=report['changedHighBytes'],faultsRejected=106,guestSHA256=report['proposedGuestSHA256'])),flush=True)

if __name__=='__main__':main()
