"""Inspect actual linked ending records; does not claim earned ending runtime."""
import hashlib
import json
from pathlib import Path
import re
import struct
from current_graphics import graphics_metadata

PORT=Path(__file__).resolve().parent
SRC=PORT.parent/'baseline/mk2-rebuild-main/srcp'
sha=lambda data:hashlib.sha256(data).hexdigest().upper()
metadata=graphics_metadata()
source_audit=json.loads((PORT/'CAMPAIGN_ENDING_AUDIT.json').read_text())
assert source_audit['dedicatedDispatchMatchesGenerator']
for name,digest in source_audit['sourceSHA256'].items(): assert sha((SRC/name).read_bytes())==digest
lanes=[b''.join((SRC/f'rom/P12{part}.{lane}').read_bytes() for part in ('F8','FC')) for lane in (0,1)]
rom=bytearray(1048576);rom[::2]=lanes[0];rom[1::2]=lanes[1]
symbols={name:int(address,16) for address,name in re.findall(r'\b([0-9a-fA-F]{8})\s+([A-Za-z_]\w*)',(SRC/'MK2P.MAP').read_text())}
listing=(SRC/'UNZIP.LST').read_text()
def local(name):
    match=re.search(r'^\s+\d+\s+([0-9a-fA-F]{8})\s+'+name+r'\s*$',listing,re.M)
    assert match,name
    return int(match[1],16)
base=symbols['show_a0_ending']-local('show_a0_ending')
def read(address,count):
    assert 0xff800000<=address and address+count*8<=0x100000000 and address%8==0
    start=(address-0xff800000)//8
    return bytes(rom[start:start+count])
def pointer(address): return struct.unpack('<I',read(address,4))[0]
images=[]
for image in metadata['images']:
    label=image['label'];address=symbols[label]
    width,height,x,y,gfx,control,palette=struct.unpack('<HHhhIHI',read(address,18))
    assert (width,height,x,y)==(image['width'],image['height'],0,0)
    assert gfx==(0xc00000+image['packedOffset'])*8 and control==0
    assert struct.unpack('<H',read(palette,2))[0]==256
    assert sha(read(palette+16,512))==image['paletteSHA256']
    images.append(dict(label=label,address=f'{address:08X}',width=width,height=height,
        graphicsBitAddress=f'{gfx:08X}',nativeEightBitDMA=True,paletteWords=256))
pages=[]
routine=read(base+local('ks_story_show'),(local('ks_story_kano')-local('ks_story_show'))//8)
expected_calls={'murder_myoinit_score':2,'clr_scrn':2,'gso_dmawnz_ns':1,
                'set_xy_coordinates':1,'insobj2a8':1,'display_on':2,
                'page_0_setup_no_init':1,'display_off':1,'sync_wait_dma_q':1,'grab_screen':1}
for name,count in expected_calls.items():
    instruction=struct.pack('<HI',0x0d5f,symbols[name])
    assert sum(routine[offset:offset+6]==instruction for offset in range(0,len(routine)-5,2))==count,name
# Real linked MOVI/absolute MOVE pair, not merely a source-string assertion.
restore=(struct.pack('<HI',0x09e0,symbols['dlists_bogus'])+
         struct.pack('<HI',0x0780,symbols['dlists']))
assert sum(routine[offset:offset+len(restore)]==restore
           for offset in range(0,len(routine)-len(restore)+1,2))==1
assert routine.index(struct.pack('<HI',0x0d5f,symbols['clr_scrn']))<routine.index(restore)
assert routine.index(restore)<routine.index(struct.pack('<HI',0x0d5f,symbols['gso_dmawnz_ns']))
for actor in ('kano','sonya'):
    row=base+local('ks_story_'+actor)
    for page,xy in ((1,0x0029001e),(2,0x0019003c)):
        image,coordinates,text=struct.unpack('<III',read(row,12))
        assert image==symbols[f'ks_end_{actor}_picture{page}']
        assert coordinates==xy
        assert text==base+local(f'ks_story_{actor}_text{page}')
        pages.append(dict(actor=actor,page=page,recordAddress=f'{row:08X}',
            imageAddress=f'{image:08X}',textAddress=f'{text:08X}',x=xy&65535,y=xy>>16))
        row+=96
    assert pointer(row)==0
report=dict(scope='Actual current program-ROM image/palette/page records',
    programSHA256=sha(rom),images=images,pages=pages,
    ownImageAndPalettePointersVerified=True,twoPagesAndTerminatorPerCharacterVerified=True,
    nativeObjectDisplayListRestoredAfterPageReset=True,
    actualNativeCallCounts=expected_calls,
    originalEndingFallbackSourcePreserved=True,endingRuntimeVerified=False,
    campaignVerified=False,releaseReady=False)
report['sourceSHA256']={name:sha((SRC/name).read_bytes()) for name in ('UNZIP.ASM','UNZIP.LST','KSENDART.ASM','MK2P.MAP')}
(PORT/'ENDING_LINK_QUALIFICATION.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
