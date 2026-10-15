"""Add the compiled native HUD initialization to the full ROM-lane oracle.

The first terminal carrier lost one rejected name stream before retention.
It can still prove exact native raster/grounding using independently predicted
name pixels, but is explicitly not a complete captured-source inventory.
No running game state, executed source or failed receipt is changed.
"""
import copy, inspect, json, struct
from pathlib import Path
import capture_launch_ground_ram as previous
import launch_ground_model as base

ROOT,need,sha=base.ROOT,base.need,base.sha

def reconstruct(pins):
 gfx=base.reconstruct(pins)
 source=ROOT/base.current.NAME/'input_sources/mame-mkp/src/mame/midway/midtunit_m.cpp'
 pins[str(source)]=sha(source);text=source.read_text()
 for fragment in ('unsigned const image = 0x1e00000 + fighter * 0x400;',
                  'unsigned const width = face_width + 1;',
                  'mask[y * mask_width + x] > 48',
                  'index = 2; // same dark edge as stock HUD lettering',
                  'gfx[image + pixel / 2] |= index << ((pixel & 1) * 4);'):
  need(fragment in text,'Actual compiled native name initialization: '+fragment)
 original_path=ROOT/'mk2/mk2-maincpu.bin';ui_path=ROOT/'roms/mk2ks/mk2ks.ui'
 for path in (original_path,ui_path):pins[str(path)]=sha(path)
 original=original_path.read_bytes();ui=ui_path.read_bytes()
 colors=struct.unpack_from('<H',ui,6)[0];names=8+2*(colors*2+ui[4]*ui[5]);mw,mh=ui[names:names+2]
 need(mw>0 and mh>=10 and names+2+2*mw*mh<=len(ui),'Entire native name masks')
 at=(0xffa79400-0xff800000)//8;ow=struct.unpack_from('<H',original,at)[0];origin=struct.unpack_from('<I',original,at+8)[0]
 need(not any(gfx[0x1e00000:0x1e00800]),'Original native empty HUD storage')
 ramp=[]
 for y in range(10):
  counts=[0]*16;best=0
  for x in range(ow):
   bit=origin+(y*ow+x)*4;pen=(int.from_bytes(gfx[bit//8:bit//8+2],'little')>>(bit%8))&15
   if pen==3 or 5<=pen<=11:
    counts[pen]+=1
    if counts[pen]>counts[best]:best=pen
  need(best!=0,'Actual original native HUD gold ramp');ramp.append(best)
 for fighter in range(2):
  mask=ui[names+2+fighter*mw*mh:names+2+(fighter+1)*mw*mh]
  xs=[x for y in range(10)for x in range(mw)if mask[y*mw+x]>48];need(bool(xs),'Nonempty actual native name')
  left,right=min(xs),max(xs);fw=right-left+1;w=fw+1
  face=lambda x,y:0<=x<fw and 0<=y<10 and mask[y*mw+left+x]>48
  for y in range(10):
   for x in range(w):
    pen=ramp[y]if face(x,y)else 2 if x and(face(x-1,y)or(y and face(x-1,y-1)))else 0
    pixel=y*w+x;gfx[0x1e00000+fighter*0x400+pixel//2]|=pen<<((pixel&1)*4)
 return gfx

source=base.source
before="    buffers=carrier['gfx']"
need(source.count(before)==1,'Exact original numeric parser binding')
source=source.replace(before,"    buffers={k:{field:(int(v) if field in ('offset','first','bytes') else v) for field,v in r.items()} for k,r in carrier['gfx'].items()}")
scope=dict(base.scope);exec(compile(source,__file__+'::entire_original_raster_with_numeric_metadata','exec'),scope)
inspect_ground=scope['inspect']

def check(carrier):
 value=inspect_ground(carrier);base.contract.check_ground(value,carrier['fighter'],carrier['side']);return value

original=base.original
contract=base.contract
graphics=base.graphics
current=base.current

def qualify_first(carrier,gfx):
 need(carrier['terminal']['pid']==156896 and carrier['terminal']['nativeExit']==0 and
      carrier['errors']==[dict(stage='decode',error="ValueError('Every complete actually drawn stock/imported source stream matches independently reconstructed compiled graphics')")],
      'Exactly retained original native terminal and original single failed source gate')
 need(not(carrier['folder']/'stderr.log').read_text(),'Actual native empty stderr')
 dmas=original.rows(carrier['text'],'DMA')
 missing={f"{r['source']:08X}_{r['command']:04X}_{r['width']}_{r['height']}"for r in dmas if r['width']and r['height']and r['command']&15!=12}-set(carrier['gfx'])
 need(missing=={'0F000000_C002_33_10'},'Only missing actual stream is compiled native Kano HUD name')
 for r in carrier['gfx'].values():
  start,size=int(r['first']),int(r['bytes'])
  need(bytes.fromhex(r['data'])==gfx[start:start+size],'Every retained complete native source stream exact')
 local=dict(carrier,gfx=dict(carrier['gfx']))
 start=0x1e00000;size=33*10*4//8+8
 local['gfx']['0F000000_C002_33_10']=dict(key='0F000000_C002_33_10',offset=str(start*8),first=str(start),bytes=str(size),data=gfx[start:start+size].hex())
 value=check(local)
 fields=original.rows(carrier['text'],'FIELD');results=original.rows(carrier['text'],'RESULT')
 need(len(fields)==962 and [(r['age'],r['slot'])for r in fields]==[(a,s)for a in range(481)for s in(1,2)]and
      len(results)==1 and results[0]['terminalAge']==480,'Entire original native window')
 for r in fields:
  wanted=17 if r['slot']==1 else 4
  need(r['id']==r['roster']==wanted and r['owner']==r['actor']and r['state']==1 and r['hp']==161 and
       r['floor']==r['stageY']-{17:134,4:133}[wanted],'Entire actual physical identity/health/ground window')
 return dict(passed=True,wholeGroundAndShadow=value,nativeTerminal=carrier['terminal'],fighter='kano',side=1,
             actualRGBFrames=len(carrier['images']),completeRetainedSourceGraphicsStreams=len(carrier['gfx']),
             completeCapturedSourceInventoryAccepted=False,missingCapturedStreams=sorted(missing),
             independentNativeHudPredictionUsedOnlyForRaster=True,originalFailedReportPreserved=True,
             allArenaGroundAcceptance=False,fullPortAcceptance=False)

capture_scope=dict(vars(previous),model=__import__(__name__))
exec(compile(inspect.getsource(previous.capture),__file__+'::unchanged_original_remaining_cases','exec'),capture_scope)
capture=capture_scope['capture']

def continue_remaining(carriers):
 out=ROOT/'audit_launch_ground_native_names_checked';need(not out.exists(),'Fresh additive report')
 pins=dict(carriers[0]['inputHashes']);gfx=reconstruct(pins)
 for path in (Path(__file__),Path(base.__file__),Path(previous.__file__)):pins[str(path)]=sha(path)
 need(all(sha(p)==h for p,h in pins.items()),'All actual original source/candidate pins preserved')
 first=qualify_first(carriers[0],gfx);out.mkdir();previous.save(out/'kano_p1_same_terminal.json',dict(first,inputHashes=pins))
 print(json.dumps(dict(case='kano_p1_same_terminal',passed=True,completeCapturedSourceInventoryAccepted=False)),flush=True)
 guest=current.expected();accepted=[first]
 for fighter,side in (('kano',2),('sonya',1),('sonya',2)):
  c=capture(fighter,side,guest,gfx,pins);carriers.append(c)
  need(c['report']['passed'],'Entire fresh remaining actual mobility case');accepted.append(c['report'])
 report=dict(passed=True,candidate=current.NAME,cases=accepted,inputHashes=pins,currentBothSlotDeadPoolGroundAndShadowAccepted=True,
             newNativeBoots=3,originalFirstTerminalPreserved=True,firstCapturedSourceInventoryAccepted=False,
             newBuilds=0,newROMCopies=0,newZIPs=0,newRawMedia=0,allArenaGroundAcceptance=False,fullPortAcceptance=False)
 previous.save(out/'report.json',report);return report
