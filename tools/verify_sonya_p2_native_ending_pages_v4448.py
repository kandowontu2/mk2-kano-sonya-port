"""Four natural SonyaP2 ending pages: full RGB equality and original-source gates.

Actual RAM scanouts are bound by their complete RGB hashes to existing pinned
natural P1 scanouts. Recheck original-ROM photo, own native story font/shadow
and common stock background gates. No capture is replayed or persisted. This
does not accept whole ending transitions, all black pens, cinematics or audio.
"""
import copy,hashlib,json,re,struct,subprocess
from pathlib import Path
import numpy as np
from PIL import Image
import verify_kintaro_pressure_guard_long_whole_campaign_v4442 as campaign
import verify_current_natural_ending_photos_v3535 as photos
import verify_current_natural_ending_text_v3542 as text
import verify_original_ending_black_strip_v3551 as background
ROOT,need,sha=campaign.ROOT,campaign.need,campaign.sha
OUT=ROOT/'audit_v4449_sonya_p2_native_ending_pages_checked'

def rgb_hash(image):return hashlib.sha256(image.tobytes()).hexdigest().upper()

def exact_ram_frame(record,image):
    need(record['width']=='400' and record['height']=='254' and record['bytes']=='406400',
         'One complete actual native RAM scanout')
    need(image.shape==(254,400,3) and record['rgbSHA256']==rgb_hash(image),
         'Every actual current RGB pixel matches the pinned complete native reference')

def main():
    need(not OUT.exists(),'Fresh immutable native page proof')
    proof_path=campaign.OUT/'report.json';proof=json.loads(proof_path.read_text())
    need(proof['passed'] and proof['case']['passed'] and
         proof['actualNaturalSonyaP2TowerClearAccepted'] and
         proof['case']['unassisted_clear_proven'],
         'Actual whole native SonyaP2 clear and own ending qualified first')
    pins=dict(proof['case']['inputHashes'])
    def pin(p,wanted=None):
        key=str(Path(p).resolve());h=sha(p)
        need((wanted is None or h==wanted) and (key not in pins or pins[key]==h),
             'Exact original/current source and capture bytes')
        pins[key]=h
    pin(proof_path)
    prior={}
    for module,flag in ((photos,'bothNaturalP1EndingVisiblePhotosAccepted'),
                       (text,'bothNaturalP1StoryGlyphSpacingPunctuationAndBlackShadowsAccepted'),
                       (background,'bothNaturalP1NativePhotoFrameOverpaintAndCommonBackgroundAccepted')):
        p=module.OUT/'report.json';r=json.loads(p.read_text());pin(p)
        need(r['passed'] and r[flag] and not r['fullPortAcceptance'],
             'Existing original-source-qualified natural P1 reference, scoped exclusions retained')
        for path,h in r['inputHashes'].items():pin(path,h)
        prior[module.__name__]=r
    raw=(campaign.FOLDER/'run.log').read_text()
    pictures,stories,snaps,starts,ends=[photos.rows(raw,t) for t in
        ('PICTURE','TEXT','PAGE_SNAP','ENDING_START','ENDING_COMPLETED')]
    need(len(pictures)==2 and len(stories)==6 and len(snaps)==4 and len(starts)==len(ends)==1,
         'One own natural ending, both native photo/story pages, four real early/late scanouts')
    need(starts[0]['winner']=='2' and starts[0]['roster']=='18' and
         ends[0]['pictures']=='1,1' and ends[0]['texts']=='3,3',
         'True own Sonya18 ending, never inferred from an attract picture')
    frames=[dict(re.findall(r'(\w+)=([^\s]+)',line)) for line in raw.splitlines()
            if line.startswith('MK2_CAMPAIGN_RAM_FRAME_DIGEST ')]
    need(len(frames)==78 and not any('hex=' in line for line in raw.splitlines()),
         'Actual full RAM digests, no encoded raw raster persisted')
    guest=campaign.capture.expected();original_path=ROOT/'mk2/mk2-maincpu.bin'
    pin(original_path,text.ROM_SHA);original=original_path.read_bytes()
    text.source_contract(guest,original)
    graphics=bytearray(0x400000)
    for chip in prior[text.__name__]['originalFontBankChips']:
        p=Path(chip['file']);pin(p);raw_chip=p.read_bytes();lane=int(chip['regionLane'],16)-0x800000
        graphics[lane:lane+len(raw_chip)*4:4]=raw_chip
    donor=photos.graphics.load_gfx(ROOT/'roms/mk2ks')
    references=prior[photos.__name__]['cases']['sonya']['snapshots']
    stock_log=(background.CASE/'run.log').read_text()
    stock_pictures=photos.rows(stock_log,'PICTURE');records=[];faults=[]
    for page in (1,2):
        dispatch=next(p for p in pictures if p['page']==str(page));frame=int(dispatch['frame'])
        index=52+page-1;offset=0xf4900+index*4
        need(int(dispatch['entry'],16)==0xff800000+offset*8 and
             int(dispatch['value'],16)==struct.unpack_from('<H',guest,offset)[0] and
             dispatch['pc']=='FF8447E0' and dispatch['mask']=='FFFF' and dispatch['roster']=='18' and
             int(starts[0]['frame'])<frame<int(ends[0]['frame']),
             'Actual own native guest picture pointer dispatched by original renderer')
        own_stories=[s for s in stories if s['page']==str(page)]
        need(len(own_stories)==3 and {s['segment'] for s in own_stories}=={'0','1','2'},
             'All three own native text table reads')
        for s in own_stories:
            at=(0xf4a00 if page==1 else 0xf4b00)+(18*3+int(s['segment']))*4
            need(int(s['entry'],16)==0xff800000+at*8 and
                 int(s['value'],16)==struct.unpack_from('<H',guest,at)[0] and
                 s['frame']==dispatch['frame'] and s['roster']=='18',
                 'Actual own story table pointer and dispatch chronology')
        original_record,_,provenance=photos.original.reference(donor,1,page-1)
        other_record,_,_=photos.original.reference(donor,0,page-1)
        photograph=photos.rgb_record(original_record);other=photos.rgb_record(other_record)
        own_text=text.model(guest,original,graphics,18,page)
        stock_text=background.stock_text_model(original,graphics,page)
        for late,age in (('',60),('_late',180)):
            name=f'ending_page{page}{late}_{frame}.png'
            actual=[f for f in frames if f['filename']==name]
            event=[s for s in snaps if s['file']==name]
            need(len(actual)==len(event)==1 and int(event[0]['frame'])==frame+age,
                 'Actual natural native page dispatch plus exact early/late age')
            ref=next(r for r in references if r['page']==page and ('_late_' in Path(r['file']).name)==bool(late))
            pin(ref['file']);image=np.asarray(Image.open(ref['file']).convert('RGB'))
            exact_ram_frame(actual[0],image)
            # Reference and actual current RGB bytes are identical. Thus the
            # original-source pixel predicates below apply to the actual RGB,
            # not a screenshot-selected crop or a digest-only art assertion.
            photo_result=photos.photo_gate(image,photograph,page)
            photo_faults=photos.qualified_faults(image,photograph,other,page)
            text_result=text.pixel_gate(image,own_text);text_faults=text.faults(image,own_text)
            stock_frame=int(next(p for p in stock_pictures if p['page']==str(page))['frame'])
            stock_path=background.CASE/'snap'/f'ending_page{page}{late}_{stock_frame}.png'
            pin(stock_path);stock=np.asarray(Image.open(stock_path).convert('RGB'))
            mask=~(own_text['face']|own_text['shadow']|stock_text['face']|stock_text['shadow'])
            if page==1:mask[42:204,30:153]=False
            else:mask[20:138,58:336]=False
            count=background.background_gate(image,stock,mask)
            # Counterexample on the actual complete RGB record, not a frame
            # plan. The altered digest must fail the same exact equality gate.
            bad=dict(actual[0]);bad['rgbSHA256']='0'*64
            try:exact_ram_frame(bad,image)
            except ValueError as e:faults.append(dict(page=page,age=age,key='rgbSHA256',rejectedBy=str(e)))
            else:raise ValueError('Changed actual RAM RGB digest accepted')
            changed=image.copy();y,x=np.argwhere(mask)[0];changed[y,x,0]^=1
            try:exact_ram_frame(actual[0],changed)
            except ValueError as e:faults.append(dict(page=page,age=age,key='actualRGBPixel',rejectedBy=str(e)))
            else:raise ValueError('Changed actual complete RGB pixel accepted')
            exact_ram_frame(actual[0],image)
            records.append(dict(page=page,frame=frame+age,filename=name,physicalSlot=2,identity=18,
              currentRGBSHA256=actual[0]['rgbSHA256'],referenceFile=ref['file'],
              exactWholeCurrentRGBPixels=400*254,originalPhotoSource=provenance,
              photo=photo_result,text=text_result,originalCommonBackgroundPixels=count,
              originalPhotoFaults=photo_faults,originalGlyphShadowFaults=text_faults))
    for m in (photos,text,background,campaign,campaign.capture):pin(m.__file__)
    pin(__file__)
    need(all(sha(p)==h for p,h in pins.items()),'Every original and actual current input unchanged')
    report=dict(passed=True,candidate=campaign.NAME,physicalSlot=2,identity=18,pages=records,
      actualNaturalSonyaP2EndingEarlyLatePhotoTextShadowCommonBackgroundAccepted=True,
      actualFullRGBPixelsCompared=4*400*254,actualRAMRecordFaultsRejected=faults,
      currentRasterBytesBoundToPinnedQualifiedReference=True,
      rawRasterAudioROMOrBuildCopiesWritten=0,
      allTransitionFramesCinematicsAudioHiddenBackgroundOrExtraBlackPensAccepted=False,
      fullPortAcceptance=False,scope=__doc__,inputHashes=pins)
    OUT.mkdir();need(subprocess.run(['compact.exe','/C','/I','/Q','/S:'+str(OUT)],capture_output=True).returncode==0,
                    'Compress proof before writes')
    (OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k not in ('pages','inputHashes')},indent=2),flush=True)

if __name__=='__main__':main()
