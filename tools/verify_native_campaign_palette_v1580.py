"""Source-bound normal/alternate, Sonya charge and native frozen costume colours."""
import struct
from pathlib import Path
import numpy as np
import verify_native_floor_campaign_v1573 as campaign
import verify_ring_glow_source_v1310 as charge
from verify_finish_display_v798 import check_owned_body_palette

ROOT=campaign.ROOT

def sources(guest,pins):
    donor_path=ROOT/'mk3/mk3-maincpu.bin';donor=donor_path.read_bytes()
    assert campaign.digest(donor_path)=='1BC7A53A023F15B20F01398F87E38478A27C670DF27EA320E36125D0957EE651'
    pins[str(donor_path)]=campaign.digest(donor_path)
    original_path=ROOT/'mk2/mk2-maincpu.bin';original=original_path.read_bytes()
    assert campaign.digest(original_path)=='45B3285496DB555EFAF4A3608A4F59845DD47A82E4A0593607E0592F47B36F23'
    pins[str(original_path)]=campaign.digest(original_path)
    # Original freeze writes Main action 0401 and calls the native palette
    # lookup. Its instruction sequence is unchanged; only the ID-indexed
    # palette table is extended with actual imported character records.
    start=(0xff8d9bb0-0xff800000)//8;end=(0xff8d9c20-0xff800000)//8
    assert guest[start:end]==original[start:end]==struct.pack('<7H',0x09c0,0x401,0xb00d,0x1f0,0x0d5f,0x0960,0xff91)
    lookup=(0xff910960-0xff800000)//8
    expected=bytearray(original[lookup:lookup+16])
    struct.pack_into('<I',expected,2,0xff800000+0xfd900*8)
    assert guest[lookup:lookup+16]==expected
    table=(0xff9109e0-0xff800000)//8
    assert guest[0xfd900:0xfd900+17*4]==original[table:table+17*4]
    for identity,address,dest in((17,0xffa66010,0xf59a0),(18,0xffa643a0,0xf5a40)):
        source=(address-0xff800000)//8
        assert struct.unpack_from('<H',donor,source)[0]==64
        assert guest[dest:dest+130]==donor[source:source+130]
        assert struct.unpack_from('<I',guest,0xfd900+identity*4)[0]==0xff800000+dest*8
    source=(0xffc96fb0-0xff800000)//8
    assert struct.unpack_from('<H',donor,source)[0]==64
    words=list(struct.unpack_from('<64H',donor,source+2));words[0]=0
    assert guest[0xfc000:0xfc082]==struct.pack('<H64H',64,*words)
    for module in(campaign,charge):pins[str(Path(module.__file__).resolve())]=campaign.digest(Path(module.__file__))
    pins[str(Path(__file__).resolve())]=campaign.digest(Path(__file__))

def check(q,actual,guest,ids,side):
    hero=ids[side-1]
    if q['slot']!=side or q['id']!=q['roster'] or q['id']!=hero or hero not in(17,18):
        raise ValueError('Actual owned palette requires the declared true native fighter')
    bank=q['bank']&0x7f00
    if len(actual)!=32768:raise ValueError('Complete actual native palette memory required')
    if q['action']==0x401:
        off=0xf59a0 if hero==17 else 0xf5a40
        if struct.unpack_from('<H',guest,off)[0]!=64:raise ValueError('Original native frozen palette size')
        raw=struct.unpack_from('<64H',guest,off+2)
        expected=np.array([sum(((((c>>s)&31)<<3)|(((c>>s)&31)>>2))<<dest
                              for s,dest in((10,16),(5,8),(0,0)))for c in raw],dtype=np.uint32)
        if not np.array_equal(actual[bank:bank+64],expected):raise ValueError('Exact true-ID native frozen palette required in original frozen action')
        return dict(kind='native_frozen',bank=bank,count=64,source=0xff800000+off*8)
    if hero==18 and q['pose']in charge.CHARGE_POSES:
        try:charge.check_charge_palette(q,actual)
        except AssertionError as error:raise ValueError(str(error))from error
        return dict(kind='native_sonya_ring_charge',bank=bank,count=64,source=0xff800000+0xfc000*8)
    result=check_owned_body_palette(q,actual,guest,ids,side)
    result['kind']='native_alternate'if q['body']&64 else'native_normal'
    return result
