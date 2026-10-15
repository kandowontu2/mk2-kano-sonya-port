"""Independent source/whole-payload/native data check, not runtime or art QA."""
import hashlib,json,struct,subprocess
from pathlib import Path
import numpy as np
from PIL import Image
import verify_current_cpu_square_v3280 as old
import build_native_death_art_v900 as decoder
ROOT=old.ROOT;OUT=ROOT/'audit_v3820_native_mileena_victim_data_checked'
ASSET=ROOT/'asset_v3812_native_mileena_victims'
SOURCE=ROOT/'source_v3814_native_mileena_victims/midtunit_m.cpp'
def sha(b):return hashlib.sha256(b).hexdigest().upper()
def need(c,s):
    if not c:raise ValueError(s)
def off(a):return (a-0xff800000)//8
def addr(a):return 0xff800000+a*8
def check(base,original,payload,guest,reference):
    expected=bytearray(base);meta=payload[0x1f6000:0x1f6400];expected[0x1f6000:0x1f6400]=meta
    fields=struct.unpack_from('<4s18I',payload,0x1f6000)
    need(fields[0]==b'KME1','Owned swallowing header')
    sizes=fields[2],fields[4]
    need(fields[1:]==(0x122000,sizes[0],0x154000,sizes[1],0x1f80000,0x1f6100,0xac000,15,20,0x1f6280,0xac200,0x1f6300,0xac280,0xac2a0,0x1f6380,0xac300,7,8),'Exact allocation/grammar header')
    need(meta[76:256]==b'\xff'*180 and meta[556:640]==b'\xff'*84,'Untouched header/descriptor gap')
    need(meta[760:768]==b'\xff'*8 and meta[836:896]==b'\xff'*60 and meta[972:]==b'\xff'*52,'Exact metadata padding')
    index=0;pixels=[];startgfx=0x1f80000
    for fi,(name,sex,count,pixel_begin,limit,stream)in enumerate((('kano','male',7,0x122000,0x130000,0xac280),('sonya','female',8,0x154000,0x160000,0xac2a0))):
        need(base[pixel_begin:limit]==b'\xff'*(limit-pixel_begin),'New pixels occupy only verified free storage')
        image=Image.open(ROOT/'art_native_mileena_v3810'/f'{name}-swallowing.png')
        need(image.mode=='RGBA' and image.size==(1536,1024),'Selected alpha atlas format')
        cells=[]
        for phase in range(8):
            cell=image.crop((phase%4*384,phase//4*512,(phase%4+1)*384,(phase//4+1)*512))
            yy,xx=np.where(np.asarray(cell)[:,:,3]>=128)
            if phase>=count:need(not len(xx),'Unused cell empty');continue
            box=(int(xx.min()),int(yy.min()),int(xx.max())+1,int(yy.max())+1)
            need(box[0]>=2 and box[1]>=2 and box[2]<=382 and box[3]<=510,'Entire source pose contained')
            cells.append(cell.crop(box))
        factor=reference['stock'][sex]['poses'][0]['size'][1]/cells[0].height
        palette_at=(0xfda00,0xfdb00)[fi]
        need(struct.unpack_from('<I',guest,palette_at)[0]==65,'Current native palette count includes transparent slot')
        packed_palette=struct.unpack_from('<64H',guest,palette_at+4)
        ramps=np.array([((v>>10&31)*255//31,(v>>5&31)*255//31,(v&31)*255//31)for v in packed_palette[:63]],dtype=np.int32)
        cursor=pixel_begin;firstgfx=startgfx
        for phase,cell in enumerate(cells):
            w,h=round(cell.width*factor),round(cell.height*factor);bounds=reference['stock'][sex]['poses'][phase]['bounds']
            left=bounds[2]-w;top=round((bounds[1]+bounds[3]-h)/2)
            d=struct.unpack_from('<4hIHIH',payload,0x1f6100+index*20)
            need(d==(w,h,-left,-top,startgfx*8,0x6000,addr(palette_at),0),'Source-bound own descriptor/costume/clipping plane')
            need(struct.unpack_from('<2I',payload,0x1f6280+index*8)==(addr(0xac000+index*20),0),'Owned native group terminates')
            need(struct.unpack_from('<I',payload,0x1f6300+fi*32+phase*4)[0]==addr(0xac200+index*8),'No proxy/descriptor as stream')
            scaled=np.asarray(cell.resize((w,h),Image.Resampling.LANCZOS));rgb=scaled[:,:,:3].astype(np.int32)
            # Independently match encoder's original RGB555 color-distance
            # convention; this is pen selection, not display DAC fidelity.
            expected_indices=np.argmin(np.sum((rgb[:,:,None,:]-ramps[None,None,:,:])**2,axis=3),axis=2).astype(np.uint8)+1
            expected_indices[scaled[:,:,3]<128]=0
            n=(w*h*6+7)//8;actual=decoder.unpack(payload[cursor:cursor+n],w*h)
            need(actual==expected_indices.tobytes(),'Every own palette pen independently decoded from native packed art')
            require_padding=(-n)%4;need(payload[cursor+n:cursor+n+require_padding]==b'\xff'*require_padding,'Preserved packed alignment padding')
            pixels.append(dict(fighter=name,phase=phase,visible=int(np.count_nonzero(expected_indices)),size=[w,h],bounds=[left,top,bounds[2],top+h]))
            padded=(n+3)&~3;cursor+=padded;startgfx+=padded;index+=1
        need(cursor-pixel_begin==sizes[fi] and cursor<=limit,'Exact actual pixel-bank extent')
        expected[pixel_begin:cursor]=payload[pixel_begin:cursor]
        need(struct.unpack_from('<I',payload,0x1f6300+fi*32+count*4)[0]==0,'Native stream end; unchanged seven/eight count')
    need(bytes(expected)==payload and len(payload)==0x200000,'Whole payload: absolutely no unrelated changes')
    rows=struct.unpack_from('<19I',payload,0x1f6380)
    need(rows[:17]==struct.unpack_from('<17I',original,off(0xff9e9140)) and rows[17:]==(addr(0xac280),addr(0xac2a0)),'Only true17/18 rows extended; original seventeen words unchanged')
    result=bytearray(guest)
    need(result[0xac000:0xac34c]==b'\xff'*0x34c,'Entire program allocation was genuinely unoccupied')
    for p,r,n in ((0x1f6100,0xac000,300),(0x1f6280,0xac200,120),(0x1f6300,0xac280,32),(0x1f6320,0xac2a0,36),(0x1f6380,0xac300,76)):result[r:r+n]=payload[p:p+n]
    need(struct.unpack_from('<I',result,off(0xff9e7ea0))[0]==0xff9e9140,'Original consumer operand')
    struct.pack_into('<I',result,off(0xff9e7ea0),addr(0xac300))
    return bytes(result),pixels
def main():
    need(not OUT.exists(),'Immutable new proof')
    guest,_,base,_,_=old.expected_current();original=(ROOT/'mk2/mk2-maincpu.bin').read_bytes()
    payload=(ASSET/'roms/mk2ks/mk2ks.mdata').read_bytes();reference=json.loads((ROOT/'art_reference_mileena_v3801/reference.json').read_text())
    expected,pixels=check(base,original,payload,guest,reference)
    report=json.loads((ASSET/'report.json').read_text())
    need(sha(payload)==report['outputPayloadSHA256'] and sha(expected)==report['expectedGuestSHA256'],'Whole reconstruction agrees, no masked bytes')
    before=(ROOT/'diagnostic_v3680_native_sound_packet_guard/input_sources/mame-mkp/src/mame/midway/midtunit_m.cpp').read_text()
    source=SOURCE.read_text();start=source.index('\t// Mileena\'s native swallowing victim lookup');end=source.index('\t// The shared native inflation/explosion victim task',start)
    block=source[start:end];need(source[:start]+source[end:]==before,'Entire host source except single inserted initialization data loader unchanged')
    need('m_maincpu->'not in block and 'install_'not in block and 'write16('not in block,'No runtime hooks, ID writes or cache-copy suppression')
    need(block.count('write32(')==1 and 'write32(rom_offset(0xff9e7ea0),native_address(eaten_native_table));'in block,'Only original lookup operand redirected')
    faults=[]
    for name,offset in [('header',0x1f6000),('bank_extent',0x1f6008),('proxy_stream_kano',0x1f6300),('proxy_stream_sonya',0x1f6320),('missing_kano_end',0x1f631c),('missing_sonya_end',0x1f6340),('nonterminating_group',0x1f6284),('stock_row',0x1f6380),('kano_row',0x1f63c4),('sonya_row',0x1f63c8),('wrong_owned_palette',0x1f610e),('pixel_data',0x122000),('unrelated_payload',0x100)]:
        changed=bytearray(payload);changed[offset]^=1
        try:check(base,original,changed,guest,reference)
        except (ValueError,struct.error):faults.append(name)
        else:raise ValueError('Fault accepted: '+name)
    restored,_=check(base,original,payload,guest,reference);need(restored==expected and len(faults)==13,'Restored positive after actual data faults')
    pins={str(p.resolve()):sha(p.read_bytes())for p in (SOURCE,Path(__file__),ASSET/'report.json',ASSET/'roms/mk2ks/mk2ks.mdata',ROOT/'tools/build_native_mileena_victim_art_v3811.py',ROOT/'tools/mileena_victim_selected_prompts_v3809.json',ROOT/'art_reference_mileena_v3801/reference.json',ROOT/'art_native_mileena_v3810/kano-swallowing.png',ROOT/'art_native_mileena_v3810/sonya-swallowing.png')}
    OUT.mkdir();need(subprocess.run(['compact.exe','/C','/I','/Q','/S:'+str(OUT)],capture_output=True).returncode==0,'Evidence compression')
    value=dict(passed=True,scope=__doc__,stagedSource=str(SOURCE),stagedSourceSHA256=sha(SOURCE.read_bytes()),expectedGuestSHA256=sha(expected),payloadSHA256=sha(payload),sourceUnrelatedCodeUnchanged=True,wholePayloadAccepted=True,actualDataFaultsRejected=faults,decodedFrames=pixels,requiresCompilationAndNativeRuntimeRegression=True,runtimeAcceptance=False,artAcceptance=False,fullPortAcceptance=False,inputHashes=pins)
    (OUT/'report.json').write_text(json.dumps(value,indent=2)+'\n');print(json.dumps({k:value[k]for k in ('passed','expectedGuestSHA256','requiresCompilationAndNativeRuntimeRegression','runtimeAcceptance','artAcceptance')}))
if __name__=='__main__':main()
