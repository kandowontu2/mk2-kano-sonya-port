"""Same physical route, original picture render, full native terminal.

This accepts the specific repaired reset route, not every secret, ending,
audio, stage, UI or finisher context in the complete Kano/Sonya objective.
"""
import gzip
import hashlib
import json
import re
import struct
from pathlib import Path
import numpy as np
from PIL import Image
import stock_slideshow_row40_context as current
import qualify_stock_slideshow_row40 as source
import decode_native_picture as decoder
import check_natural_smoke_route as original
from verify_current_ending_presentation_v680_v1 import locate_photo

ROOT,need=current.ROOT,current.need
OLD=source.RUN


def prefix_ledger(text,boundary):
    tags=('MK2_STAGE_INPUT ','MK2_SECRET_HEALTH ','MK2_STAGE_SECRET_FIELD ',
          'MK2_STAGE_MATCH ','MK2_STAGE_WINDOW ','MK2_STAGE_TOASTY ',
          'MK2_STAGE_SECRET_ACCEPT ','MK2_STAGE_SECRET_FIGHT ',
          'MK2_STAGE_SECRET_WALK ','MK2_STAGE_SECRET_JUMP ',
          'MK2_STAGE_SECRET_PUNCH ','MK2_STAGE_SECRET_RECOVER ')
    kept=[]
    for line in text.splitlines():
        # The old failed job genuinely resets and restarts its frame counter.
        # Compare its pre-failure first epoch only; retain the whole failed
        # capture elsewhere and never accept that run as a terminal pass.
        if line.startswith('MK2_SECRET_NATIVE_RESET '):break
        if line.startswith(tags):
            frame=re.search(r'\bframe=(\d+)\b',line)
            need(frame is not None,'Every original native physical/owner/health record has frame')
            if int(frame[1])<boundary:kept.append(line)
    need(len(kept)>250000,'Whole actually executed pre-failure physical/owner/health history')
    return kept


def prefix_screen_digests(text,boundary):
    kept=[]
    for line in text.splitlines():
        if line.startswith('MK2_SECRET_NATIVE_RESET '):break
        if line.startswith('MK2_HPHASE_RGB_DIGEST '):
            r=dict(re.findall(r'(\w+)=([^\s]+)',line))
            if int(r['frame'])<boundary:kept.append(r)
    need(len(kept)>=30,'Complete original native pre-failure screen set, not just one favorable frame')
    return kept


def route_gate(c,rows):
    need(c['report']['passed'] and c['guestCount']==c['gfxCount']==1 and
         c['terminal']['nativeExit']==0 and not c['decodeErrors'],
         'Whole actual compiled native job terminal with one uncorrupted boot/memory/GFX transport')
    need(not rows['MK2_SECRET_NATIVE_RESET'] and not rows['MK2_GRAPHICS_WATCHDOG'] and
         len(rows['MK2_STAGE_BOOT'])==1, 'No machine reset or graphics-copy I/O write anywhere in the entire replay')
    lookup,header,returned=(rows[t] for t in
        ('MK2_GRAPHICS_PICTURE_LOOKUP','MK2_GRAPHICS_PICTURE_HEADER','MK2_GRAPHICS_PICTURE_RETURN'))
    need(len(lookup)==len(header)==len(returned)==1,'One real restored row40 lookup/header/native return')
    lookup,header,returned=lookup[0],header[0],returned[0]
    need(lookup['pc']=='FF8447E0' and int(lookup['at'],16)==source.ENTRY and
         int(lookup['A8'],16)==source.ENTRY and lookup['data']=='00001BC0' and
         lookup['A8words'].startswith('1BC0058B'), 'Actual original loader reads complete original row40 pointer')
    need(header['pc']=='FF903650' and header['A8']=='058B1BC0' and
         header['A8words'].startswith('008A009E000100FE') and header['frame']==lookup['frame'],
         'Actual original decoder receives genuine138x158 picture, one frame,254 colors')
    need(returned['pc']=='FF844870' and int(returned['frame'])>=int(header['frame']) and
         float(returned['seconds'])>float(header['seconds']),
         'Original decoder really completes and returns to the native biography caller')
    need(all(r['writes']=='0' and r['assistance']=='none' for r in (lookup,header,returned)),
         'Only passive read observations; no pointer/health/RNG/CPU assistance')
    oldreport=json.loads((source.OUT/'report.json').read_text())
    boundary=int(oldreport['actualNativeFailure']['actualLookup']['frame'])
    need(int(lookup['frame'])==boundary,'Repaired stock lookup naturally reached on exactly the same native field')
    with gzip.open(OLD/'run.log.gz','rt',encoding='utf-8') as f: oldtext=f.read()
    oldprefix=prefix_ledger(oldtext,boundary)
    prefix=prefix_ledger(c['text'],boundary)
    need(prefix==oldprefix,'Every original physical input, HP store, true character/owner field and native match/secret/control event before failure unchanged')
    oldscreens=prefix_screen_digests(oldtext,boundary)
    screens=prefix_screen_digests(c['text'],boundary)
    need(screens==oldscreens,'Every full native pre-failure selection/ladder/fight/secret/recovery screen byte unchanged')
    fields=rows['MK2_STAGE_SECRET_FIELD']
    last=max(int(r['frame']) for r in fields)
    need(last>=int(returned['frame'])+1000 and len(rows['MK2_SECRET_DEADLINE'])==1,
         'Whole same native replay continues at least1000fields after repaired return through original deadline/terminal')
    first=int(rows['MK2_STAGE_MATCH'][0]['frame'])
    health,by=original.physical_ledger(c,first,last,rows)
    need(by[last,1]['mode']==by[last,2]['mode'], 'Both complete terminal physical slots retained')
    return dict(actualLookup=lookup,actualHeader=header,actualNativeReturn=returned,
                wholeUnchangedPreFailureRecords=len(prefix),
                unchangedPrefixSHA256=hashlib.sha256(('\n'.join(prefix)+'\n').encode()).hexdigest().upper(),
                unchangedOriginalNativeScreens=screens,wholeNativeScreenPixelsConserved=len(screens)*400*254,
                wholeOriginalHealthLedger=health,firstNativeMatchFrame=first,lastNativeField=last,
                postReturnFields=last-int(returned['frame']))


def photo_oracle():
    gfx=bytearray(0xc00000)
    banks=(('ug14','uj14','ug19','uj19'),('ug16','uj16','ug20','uj20'),('ug17','uj17','ug22','uj22'))
    for bank,lanes in enumerate(banks):
        for lane,name in enumerate(lanes):
            raw=(ROOT/'mk2'/('l1_mortal_kombat_ii_game_rom_'+name+'.'+name)).read_bytes()
            need(len(raw)==0x100000,'Entire original stock graphics lane')
            gfx[bank*0x400000+lane:(bank+1)*0x400000:4]=raw
    at=(source.POINTER-0x02000000)//8
    image,report=decoder.decode(gfx,at)
    palette=np.frombuffer(gfx,dtype='<u2',count=254,offset=at+8)
    rgb5=np.stack(((palette>>10)&31,(palette>>5)&31,palette&31),axis=1)
    rgb=((rgb5<<3)|(rgb5>>2)).astype(np.uint8)
    photo=rgb[np.asarray(image)]
    return photo,report


def qualify(c):
    out=c['folder']/'native_stock_row40_regression.json'
    need(not out.exists(),'Fresh finite native qualification; never overwrite actual transport')
    need(c['guest']==current.expected(),'Entire live current guest equals independently source-derived four-byte repair')
    rows=original.inventory(c['text'])
    result=route_gate(c,rows)
    photo,oracle=photo_oracle()
    screens=[]
    clearing=[]
    for delay in (20,60,180):
        actual=[r for r in c['rgbFrames'] if r['header']['stage']==f'stock_row40_visible{delay}.png']
        need(len(actual)==1,'One actual full-screen native biography capture at delay'+str(delay))
        frame=actual[0]
        need(hashlib.sha256(frame['pixels']).hexdigest().upper()==frame['header']['sha256'],
             'Every captured screen byte retained unchanged')
        image=np.asarray(Image.frombytes('RGB',(400,254),frame['pixels'],'raw','BGRX'))
        if delay==20:
            # The actual native presentation is still on its black page at
            # this early sample. The original failed all-three-photo checker
            # remains archived. Do not crop/score a black screen as a photo.
            need(np.all(image==0),'Entire early native clearing page contains no leaked selector artwork')
            clearing.append(frame['header'])
            continue
        matches=locate_photo(image,photo)
        need(len(matches)==1,'Entire original138x158 stock photograph matches actual native biography raster')
        screens.append(dict(header=frame['header'],exactPhotoPosition=matches[0],matchedSourcePixels=21804))
    faults=[]
    for label,tag,key,value in (
        ('wrong restored table row','MK2_GRAPHICS_PICTURE_LOOKUP','at','FFFA4CE0'),
        ('zero decoder pointer','MK2_GRAPHICS_PICTURE_HEADER','A8','00000000'),
        ('wrong native return','MK2_GRAPHICS_PICTURE_RETURN','pc','FF904F90')):
        # Preserve the complete original ledger by reference; only the one
        # faulted actual diagnostic record is copied. The gate never edits it.
        bad=dict(rows);bad[tag]=[dict(r) for r in rows[tag]];bad[tag][0][key]=value
        try:route_gate(c,bad)
        except ValueError as error:faults.append(dict(fault=label,rejected=str(error)))
        else:raise ValueError('Actual pointer/return fault accepted')
    badphoto=photo.copy();badphoto[79,69]^=1
    need(not locate_photo(image,badphoto),'One wrong source-photo pixel rejects complete original-image match')
    faults.append(dict(fault='one source photograph pixel',rejected='complete exact native photo match'))
    result.update(passed=True,resetRouteAccepted=True,fullPortAcceptance=False,
                  actualNativeTerminal=c['terminal'],nativeEarlyClearingFrames=clearing,
                  exactOriginalPhotoFrames=screens,originalPhotoOracle=oracle,
                  actualFaultsRejected=faults,publicPlayableChanged=False,newRawMedia=0,
                  scope='Same Sonya P2 earned secret/return/attract route and repaired stock biography only; no full secret-survival/audio/release acceptance.',
                  inputHashes={str(Path(p).resolve()):current.sha(p) for p in
                    (Path(__file__),Path(current.__file__),Path(source.__file__),Path(original.__file__),Path(decoder.__file__))})
    out.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(dict(resetRouteAccepted=True,exactOriginalPhotoPixels=2*21804,
                         actualFaultsRejected=4,postReturnFields=result['postReturnFields'],fullPortAcceptance=False)))
    return result
