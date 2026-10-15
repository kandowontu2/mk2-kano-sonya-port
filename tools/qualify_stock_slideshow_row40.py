"""Actual native lookup failure and minimal stock-table conservation repair.

Never turn a reset/aborted observer into gameplay acceptance. The proposed
repair restores one original picture pointer, not a renderer bound/skip.
"""
import argparse
import copy
import gzip
import hashlib
import json
import re
import struct
from pathlib import Path
import kano_ball_launch_context_v6642 as prior
import decode_native_picture as decoder

ROOT,need,sha=prior.ROOT,prior.need,prior.sha
RUN=ROOT/'audit_natural_smoke_route_sonya_p2_graphics_picture_lookup_guarded'
OUT=ROOT/'audit_stock_slideshow_row40_source'
STAGE=ROOT/'source_stock_slideshow_row40'
OLD=ROOT/'source_v6636_kano_ball_launch'
TABLE=0xf4900
ENTRY=0xff800000+(TABLE+40*4)*8
POINTER=0x058b1bc0
EDITS={
 'just 40 stock entries, whereas real IDs 11h/12h require indices 50..53.':
 '41 stock entries, including the alternate Johnny Cage biography photo;\n\t   real IDs 11h/12h require indices 50..53.',
 'std::copy_n(rom + rom_offset(0xff8f48f0), 40 * 4, rom + ending_picture_table);':
 'std::copy_n(rom + rom_offset(0xff8f48f0), 41 * 4, rom + ending_picture_table);',
 'for (unsigned index = 40; index < 50; index++)':
 'for (unsigned index = 41; index < 50; index++)',
}


def records(text):
    tags=('MK2_GRAPHICS_PICTURE_LOOKUP','MK2_GRAPHICS_PICTURE_HEADER',
          'MK2_GRAPHICS_ANCESTRY','MK2_GRAPHICS_WATCHDOG','MK2_SECRET_NATIVE_RESET')
    return {tag:[dict(re.findall(r'(\w+)=([^\s]+)',l)) for l in text.splitlines()
                 if l.startswith(tag+' ')] for tag in tags}


def failure_gate(rows,guest,stock):
    lookup,header,watchdog,reset=(rows[tag] for tag in
        ('MK2_GRAPHICS_PICTURE_LOOKUP','MK2_GRAPHICS_PICTURE_HEADER',
         'MK2_GRAPHICS_WATCHDOG','MK2_SECRET_NATIVE_RESET'))
    need(len(lookup)==len(header)==len(watchdog)==len(reset)==1,
         'One actual last picture lookup/header/runaway/watchdog reset chain')
    lookup,header,watchdog,reset=lookup[0],header[0],watchdog[0],reset[0]
    need(lookup['pc']=='FF8447E0' and int(lookup['at'],16)==ENTRY and
         int(lookup['A8'],16)==ENTRY and lookup['data']=='00000000',
         'Actual original loader dereferences relocated stock row40 as zero')
    need(header['pc']=='FF903650' and header['A8']=='00000000' and
         int(header['frame'])==int(lookup['frame']),
         'That same zero pointer enters the original picture decoder')
    copies=[r for r in rows['MK2_GRAPHICS_ANCESTRY'] if r['at']=='FF904EE0' and
            r['frame']==header['frame']]
    need(len(copies)==1 and copies[0]['B9']=='00000000' and
         copies[0]['B5']=='00000002' and copies[0]['A11']=='FFFFFFFE',
         'Actual malformed zero-width row enters stock copy with underflowed count')
    need(watchdog['pc']=='FF904F80' and watchdog['at']=='01D81060' and
         watchdog['B9']=='00000000' and int(watchdog['A5'],16)>0xff000000 and
         reset['pc']=='FF904F90' and reset['watchdogPC']=='FF904F80' and
         reset['watchdogSeconds']=='3.000000000000' and
         int(lookup['frame'])<int(watchdog['frame'])<int(reset['frame']),
         'Same native unbounded row copy writes I/O then resets after real watchdog interval')
    need(all(r['writes']=='0' and r['assistance']=='none'
             for r in (lookup,header,watchdog,reset,*copies)), 'No guest-state assistance')
    need(struct.unpack_from('<I',guest,TABLE+160)[0]==0 and
         struct.unpack_from('<I',stock,(0xff8f48f0-0xff800000)//8+160)[0]==POINTER,
         'Missing relocated pointer equals the actual failed lookup; original stock pointer nonzero')
    # Earlier task-field stores already use the reviewed extended task layout;
    # compare the complete unchanged lookup arithmetic, not those old stores.
    for lo,hi in ((0xff844790,0xff8447b0),(0xff8447d0,0xff844860),
                  (0xff84a540,0xff84a720),(0xff903640,0xff905020)):
        a,b=(lo-0xff800000)//8,(hi-0xff800000)//8
        need(guest[a:b]==stock[a:b], 'Whole stock lookup arithmetic/caller/decoder/copy instructions unchanged')
    return dict(actualLookup=lookup,actualHeader=header,actualBadCopy=copies[0],
                actualWatchdog=watchdog,actualReset=reset)


def original_picture(stock):
    gfx=bytearray(0xc00000)
    pins={}
    banks=(('ug14','uj14','ug19','uj19'),('ug16','uj16','ug20','uj20'),
           ('ug17','uj17','ug22','uj22'))
    for bank,lanes in enumerate(banks):
        for lane,name in enumerate(lanes):
            path=ROOT/'mk2'/('l1_mortal_kombat_ii_game_rom_'+name+'.'+name)
            raw=path.read_bytes();need(len(raw)==0x100000,'Whole original native graphics lane')
            pins[str(path)]=sha(path)
            gfx[bank*0x400000+lane:(bank+1)*0x400000:4]=raw
    pointer=struct.unpack_from('<I',stock,(0xff8f48f0-0xff800000)//8+160)[0]
    need(pointer==POINTER,'Original row40 unchanged')
    need(struct.unpack_from('<I',stock,(0xff8f48f0-0xff800000)//8+164)[0]==0x4f300d5f,
         'Row41 begins following native CALLA instruction, not another picture pointer')
    image,report=decoder.decode(gfx,(pointer-0x02000000)//8)
    need(image.size==(138,158) and report['decoded_pixels']==21804 and
         report['palette_count']==254, 'Complete genuine alternate stock biography photo decodes')
    report['decodedPixelSHA256']=hashlib.sha256(image.tobytes()).hexdigest().upper()
    return report,pins


def expected_guest(base):
    need(struct.unpack_from('<I',base,TABLE+160)[0]==0,'Only originally missing row40 repaired')
    guest=bytearray(base);struct.pack_into('<I',guest,TABLE+160,POINTER)
    need(sum(a!=b for a,b in zip(base,guest))==4 and len(guest)==len(base)==0x100000,
         'Exactly four original-pointer data bytes, all other full guest bytes preserved')
    return bytes(guest)


def check_sources():
    expected={name:(OLD/name).read_text() for name in ('midtunit_m.cpp','midtunit.cpp','midtunit.h')}
    for a,b in EDITS.items():
        need(expected['midtunit_m.cpp'].count(a)==1,'Single complete source correction '+a)
        expected['midtunit_m.cpp']=expected['midtunit_m.cpp'].replace(a,b,1)
    for name,text in expected.items():
        need((STAGE/name).read_text()==text,'Entire staged source equals exact conservation repair '+name)
    return {name:sha(STAGE/name) for name in expected}


def main(stage=False):
    need(not OUT.exists(), 'Fresh immutable evidence; preserve failed runs')
    report=json.loads((RUN/'report.json').read_text())
    need(not report['passed'] and report['nativeTerminal']['nativeExit']==0,
         'Failed original native transport preserved, not converted to full pass')
    with gzip.open(RUN/'executed_sources.json.gz','rt',encoding='utf-8') as f: archive=json.load(f)
    for name,digest in report['inputHashes'].items():
        if name in archive:
            need(archive[name]['sha256']==digest==hashlib.sha256(archive[name]['text'].encode()).hexdigest().upper(),
                 'Every originally executed whole text source archived')
        else:need(sha(name)==digest,'Every original native/ROM/artifact input unchanged')
    with gzip.open(RUN/'run.log.gz','rt',encoding='utf-8') as f: rows=records(f.read())
    base=prior.expected();stock=(ROOT/'mk2/mk2-maincpu.bin').read_bytes()
    actual=failure_gate(rows,base,stock)
    faults=[]
    for label,tag,key,value in (
        ('wrong stock table row','MK2_GRAPHICS_PICTURE_LOOKUP','at','FFFA4CE0'),
        ('nonzero decoder pointer','MK2_GRAPHICS_PICTURE_HEADER','A8','058B1BC0'),
        ('valid copy width','MK2_GRAPHICS_WATCHDOG','B9','0000008A'),
        ('wrong reset writer','MK2_SECRET_NATIVE_RESET','watchdogPC','FF814E90')):
        bad=copy.deepcopy(rows);bad[tag][0][key]=value
        try:failure_gate(bad,base,stock)
        except ValueError as error:faults.append(dict(fault=label,rejected=str(error)))
        else:raise ValueError('Corrupted actual evidence accepted')
    picture,pins=original_picture(stock)
    guest=expected_guest(base)
    for name in (Path(__file__).resolve(),Path(prior.__file__),ROOT/'mk2/mk2-maincpu.bin',
                 RUN/'report.json',RUN/'executed_sources.json.gz',RUN/'run.log.gz',Path(decoder.__file__)):
        pins[str(name)]=sha(name)
    result=dict(passed=True,diagnosisOnlyAccepted=True,sourceOnlyAccepted=stage,
                nativeFixAccepted=False,compiledFixAccepted=False,fullPortAcceptance=False,
                resetCause='Relocated shared picture table discarded valid stock row40; Johnny Cage biography caller explicitly requests index28h.',
                actualNativeFailure=actual,originalPicture=picture,actualRecordFaultsRejected=faults,
                proposedStockPointer=POINTER,proposedGuestSHA256=hashlib.sha256(guest).hexdigest().upper(),
                expectedGuestChangedBytes=4,priorCandidate=prior.NAME,newBuilds=0,newROMCopies=0,
                stagedSourceHashes=check_sources() if stage else {},inputHashes=pins,goalStatus='active')
    OUT.mkdir();(OUT/'report.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:result[k] for k in ('passed','sourceOnlyAccepted','expectedGuestChangedBytes','proposedGuestSHA256','nativeFixAccepted')}))


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--staged',action='store_true');args=p.parse_args();main(args.staged)
