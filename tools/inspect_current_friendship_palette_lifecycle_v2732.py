"""Actual current Kano bubble palette table/lifecycle diagnostic, both slots.
Replay every observed native palette-table store from one action baseline.
Bind constructor palette to original allocator, actual sprite/task allocation
and real scene reset/reuse. Not every victim/arena/finisher or full-port proof.
"""
import argparse,json,re,traceback
from pathlib import Path
import inspect_current_friendship_lifecycle_v2722 as life
ROOT=life.ROOT
need=life.need
PAL_FIRST,PAL_COUNT,PAL_STRIDE=0x0105bb30,60,0x40
def parse(path):
 rows=[]
 with path.open(encoding='utf-8-sig') as stream:
  for line in stream:
   match=re.match(r'MK2_CHILD_PAL_(\w+) (.*)',line)
   if match:rows.append((match[1],dict(re.findall(r'(\w+)=([^\s]+)',match[2]))))
 return rows
def words(row):
 cells=[tuple(int(value,16) for value in part.split(':')) for part in row['table'].split(',')]
 need(len(cells)==PAL_COUNT and all(len(cell)==3 and 0<=cell[0]<=0xffffffff and all(0<=v<=65535 for v in cell[1:]) for cell in cells),'Complete actual native 60-cell palette table')
 return [word for source,count,clock in cells for word in (source&65535,source>>16,count,clock)]
def palette_check(rows,control,allocated,side):
 actions=life.select(rows,'ACTION');baseline=life.select(rows,'BASELINE');constructed=life.select(rows,'CONSTRUCT');final=life.select(rows,'RESULT');states=life.select(rows,'STATE')
 need(len(actions)==len(baseline)==len(constructed)==len(final)==1 and life.number(actions[0],'frame')==control['action']==life.number(final[0],'action') and life.number(actions[0],'id')==17,'One actual true Kano palette lifecycle context')
 need(all(r['fighter']=='kano' and life.number(r,'side')==side and r['writes']=='0' and r['assistance']=='none' for _,r in rows),'All actual palette observations in true unassisted slot')
 need([life.number(r,'frame') for r in states]==list(range(control['action'],control['window']+1601)),'Every actual native palette field through scene transition')
 c=constructed[0];index=life.number(c,'paletteIndex');encoded=life.pointer(c,'palette');cell=PAL_FIRST+index*PAL_STRIDE
 need(0<=index<PAL_COUNT and encoded==index*0x101 and life.pointer(c,'object')==allocated['object'] and life.pointer(c,'task')==allocated['task'] and life.pointer(c,'cache')==allocated['task']+0x100 and life.pointer(c,'parentMain')==allocated['parentMain'] and life.pointer(c,'parent')==allocated['parent'],'Actual constructed palette bound to independent allocated bubble task/sprite')
 need(life.pointer(final[0],'object')==allocated['object'] and life.pointer(final[0],'palette')==encoded,'Same actual tracked child palette through terminal capture')
 values=words(baseline[0]);stores=[];checks=0;construction_words=None;native_increments=native_releases=0
 for tag,r in rows:
  if tag=='TABLE_STORE':
   at=life.pointer(r,'at');offset=at-PAL_FIRST
   need(0<=offset<PAL_COUNT*PAL_STRIDE and offset%16==0,'Every real palette store inside original fixed-stride table')
   slot=offset//16;before=life.pointer(r,'before');data=life.pointer(r,'data');mask=life.pointer(r,'mask');pc=life.pointer(r,'pc')
   need(before==values[slot] and 0<=data<=65535 and mask==65535,'Each original palette store matches previous independently replayed word and full native 16-bit mask')
   if pc==0xff80d550:
    need(offset%PAL_STRIDE==0x20 and before<65535 and data==before+1 and life.pointer(r,'a1')==at-0x20,'Original palette allocator increments actual reference count exactly once');native_increments+=1
   elif pc==0xff80d710:
    need(offset%PAL_STRIDE==0x20 and before>0 and data==before-1 and life.pointer(r,'a0')==data and life.pointer(r,'a1')==at-0x20,'Original palette release decrements actual positive reference count without underflow');native_releases+=1
   elif pc==0xff80cd90:
    need(data==0 and life.pointer(r,'a1')==0,'Original native palette reset clears actual table word')
   values[slot]=(before&(~mask&65535))|(data&mask);stores.append(dict(frame=life.number(r,'frame'),at=at,before=before,data=data,pc=pc,a8=life.pointer(r,'a8'),a13=life.pointer(r,'a13')))
  elif 'table' in r:
   need(words(r)==values,'Every actual complete palette snapshot matches uninterrupted original store replay');checks+=1
   if tag=='CONSTRUCT_TABLE':construction_words=list(values)
 need(construction_words is not None and checks==len(states)+2 and stores,'One original baseline only, constructor and every consecutive complete palette snapshot verified')
 source=construction_words[index*4]|construction_words[index*4+1]<<16;references=construction_words[index*4+2]
 need(source!=0 and references>0,'Actual independent bubble palette source holds a positive native reference')
 frame=life.number(c,'frame')
 entry=life.select(rows,'ALLOC_ENTRY');returned=life.select(rows,'ALLOC_RETURN')
 entries=[r for r in entry if life.number(r,'frame')==frame and life.pointer(r,'a8')==allocated['object'] and life.pointer(r,'a13')==allocated['parentMain']]
 need(len(entries)==1 and any(life.number(r,'frame')==frame and life.pointer(r,'a0')==encoded and life.pointer(r,'a8')==allocated['object'] and life.pointer(r,'a13')==allocated['parentMain'] for r in returned),'Original allocator actually enters for bubble and returns encoded palette index')
 entry_source=life.pointer(entries[0],'a0')
 need(entry_source==0xfecdf710 and any(r['frame']==frame and r['at'] in (cell,cell+16) and r['pc']==0xff80d4a0 and r['a8']==allocated['object'] and r['a13']==allocated['parentMain'] for r in stores),'Actual original source-pointer stores at independently owned bubble constructor')
 need(any(r['frame']==frame and r['at']==cell+0x20 and r['pc']==0xff80d550 and r['data']==references and r['a8']==allocated['object'] and r['a13']==allocated['parentMain'] for r in stores),'Actual original reference-count increment at bubble constructor')
 zeros=[r for r in stores if r['frame']>frame and r['at']==cell+0x20 and r['before']>0 and r['data']==0 and r['pc'] in (0xff80d710,0xff80cd90)]
 resets=life.select(rows,'RESET_ALL')+life.select(rows,'RESET_LOWER')+life.select(rows,'RESET_UPPER')
 reclaimed=[]
 for r in zeros:
  if r['pc']==0xff80cd90:need(any(life.number(reset,'frame')==r['frame'] for reset in resets),'Actual zero reference comes from observed original reset call, not missing ownership evidence')
  if r['frame']<=control['actualPointerRetirement']:reclaimed.append(r)
 return dict(actualPaletteIndex=index,actualEncodedPalette=encoded,actualAllocatorEntrySource=entry_source,actualPaletteTableSource=source,allocatorPaletteSourceIdentityAccepted=entry_source==source,actualConstructorReferenceCount=references,actualCompletePaletteSnapshots=checks,actualReplayedTableStores=len(stores),actualNativeReferenceIncrements=native_increments,actualNativeReferenceReleases=native_releases,uninterruptedCompletePaletteTableReplayAccepted=True,actualNativeBubblePaletteReferenceReclaimed=bool(reclaimed),actualBubbleReferenceReclamationEvents=reclaimed,actualOriginalPaletteResetEvents=resets,finalPaletteSource=values[index*4]|values[index*4+1]<<16,finalPaletteReferenceCount=values[index*4+2])
def lifecycle_check(rows,palette_rows,control,allocated):
 task,obj=allocated['task'],allocated['object'];cache=task+0x100;phases=allocated['phases'];returns=life.select(rows,'RETURN_TASK')
 need(len(returns)==1 and life.pointer(returns[0],'target')==life.pointer(returns[0],'head')==life.pointer(returns[0],'a2')==task and life.pointer(returns[0],'entry')==0xff80e5d0,'Actual independently allocated task returned through original masked sweep')
 free_frame=life.number(returns[0],'frame')
 need(all(r['taskActive'] and not r['taskFree'] for r in phases if r['frame']<free_frame) and all(not r['taskActive'] and r['taskFree'] for r in phases if r['frame']>=free_frame),'Every actual task phase active until original return and free through terminal')
 retire=control['actualPointerRetirement'];pool_reset=life.select(palette_rows,'SPRITE_POOL_RESET')
 need(any(life.number(r,'frame')==retire and life.pointer(r,'entry')==0xff83f060 for r in pool_reset),'Actual original sprite-pool reset at native owning fighter retirement')
 reuse=[r for r in life.select(rows,'FREE_OBJECT_STORE') if life.number(r,'frame')>=retire and life.pointer(r,'pc')==0xff809150 and life.pointer(r,'before')==life.pointer(r,'a0')==obj and life.pointer(r,'merged')==life.pointer(r,'a2')!=obj and life.pointer(r,'at')==0x01060130]
 free=next((r['frame'] for r in phases if r['frame']>=retire and r['objectFree']),None)
 reused=min((life.number(r,'frame') for r in reuse),default=None)
 need(free is not None or reused is not None,'Actual sprite address reclaimed by original free pool membership or allocator reuse, not disappearance alone')
 need(all(r['objectFree'] or r['objectCache']!=cache or not 0xfe9d2610<=r['objectPose']<=0xfe9d2790 for r in phases if r['frame']>=retire),'No old live bubble cache/pose after native scene retirement')
 return dict(actualTaskReturnFrame=free_frame,actualSpritePoolResetFrame=retire,actualSpriteFreeMembershipFrame=free,actualSpriteAllocatorReuseFrame=reused,actualNativeTaskReturnAndSpriteReclaimAccepted=True)
def verify(folder):
 meta=json.loads((folder/'result.json').read_text(encoding='utf-8-sig'));before=json.loads((folder/'inputs_before.json').read_text(encoding='utf-8-sig'));side=meta['side']
 need(meta['exit_code']==0 and meta['winner']=='kano' and side in (1,2) and meta['candidate']==life.native.scene.current.NAME and meta['guest_writes']==0 and meta['assistance']=='none' and not meta['cheats_enabled'] and meta['command_case']=='positive' and meta['samples_enabled'] and meta['observation']==1600 and meta['requested_gap']==160 and before==meta['input_hashes'],'Actual terminal unchanged-build unassisted physical palette capture')
 pins=life.native.scene.launch.source_pins()
 def pin(path,wanted=None):
  path=str(path);actual=life.native.scene.launch.sha(path);need(wanted is None or actual==wanted,'Immutable actual palette dependency '+path);need(path not in pins or pins[path]==actual,'Consistent actual dependency '+path);pins[path]=actual
 for file,wanted in before.items():
  pin(file,wanted)
  if Path(file).suffix in ('.lua','.ps1','.json'):pin(folder/'input_sources'/Path(file).name,wanted)
 source=(ROOT/'mk2ks_current_friendship_palette_lifecycle_v2729.lua').read_text()
 need(source.count("dofile('mk2ks_current_friendship_lifecycle_v2715.lua')")==1 and not re.search(r':write_|set_value|clear_value|load_?state|\.value\s*=(?!=)',source),'New palette observer read-only over unchanged physical/render/lifecycle driver')
 old_runner=(ROOT/'tools/run_current_friendship_lifecycle_v2716.ps1').read_text()
 expected=old_runner.replace('"$root/mk2ks_current_friendship_lifecycle_v2715.lua"','"$root/mk2ks_current_friendship_palette_lifecycle_v2729.lua","$root/mk2ks_current_friendship_lifecycle_v2715.lua"',1).replace('-autoboot_script "$root/mk2ks_current_friendship_lifecycle_v2715.lua"','-autoboot_script "$root/mk2ks_current_friendship_palette_lifecycle_v2729.lua"')
 need(expected==(ROOT/'tools/run_current_friendship_palette_lifecycle_v2730.ps1').read_text(),'Entire physical launcher unchanged except read-only palette wrapper and frozen manifest pin')
 guest,_,payload=life.native.scene.current.expected();need((folder/'guest_maincpu.bin').read_bytes()==guest and (ROOT/life.native.scene.current.NAME/'roms/mk2ks/mk2ks.mdata').read_bytes()==payload,'Whole actual current guest/payload independently reconstructed')
 stock_path=ROOT/'mk2/mk2-maincpu.bin';stock=stock_path.read_bytes();pin(stock_path,'45B3285496DB555EFAF4A3608A4F59845DD47A82E4A0593607E0592F47B36F23')
 for start,end in ((0xff80cad0,0xff80d7a0),(0xff8087b0,0xff808a20),(0xff83f060,0xff83f200),(0xff83ae20,0xff83b3f0),(0xff80e0e0,0xff80e620),(0xff8090b0,0xff809270)):
  a,b=(start-0xff800000)//8,(end-0xff800000)//8;need(guest[a:b]==stock[a:b],'Original native palette/task/sprite allocation/release/reset code unchanged')
 native_rows=life.native.scene.previous.parse(folder/'run.log');image=life.native.graphics.graphics(pins);control=life.native.inventory(native_rows,'kano',side,guest,image)
 old_log=ROOT/f'audit_v2691_current_kano_friendship_shadow_p{side}/run.log';pin(old_log)
 filtered=lambda rs:[(tag,r) for tag,r in rs if not tag.startswith('SHADOW_')]
 need(filtered(native_rows)==filtered(life.native.scene.previous.parse(old_log)),'Every actual original input/health/pose/WIN/part/cue/transition record unchanged')
 life_rows=life.parse(folder/'run.log');allocated=life.check(life_rows,control,'kano',side);palette_rows=parse(folder/'run.log')
 result=palette_check(palette_rows,control,allocated,side);cleanup=lifecycle_check(life_rows,palette_rows,control,allocated)
 for path in folder.rglob('*'):
  if path.is_file():pin(path)
 pin(Path(__file__).resolve());life.native.scene.launch.module_pins(pins)
 return dict(passed=True,diagnosticCompleted=True,fighter='kano',side=side,control=control,**result,**cleanup,wholeActualGuestAndPayloadReconstructed=True,originalNativePaletteAndLifecycleCodeUnchanged=True,physicalInputsAndNativeChronologyUnchanged=True,gameChanged=False,allAuxiliaryEffectsAccepted=False,fullFinisherAcceptance=False,fullPortAcceptance=False,inputHashes=pins,scope=__doc__)
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('folder',type=Path);p.add_argument('--output',type=Path,required=True);a=p.parse_args();need(not a.output.exists(),'Immutable actual palette lifecycle diagnostic')
 try:r=verify(a.folder)
 except Exception as error:r=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
 a.output.mkdir();(a.output/'report.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps({k:v for k,v in r.items() if k!='inputHashes'},indent=2),flush=True);raise SystemExit(0 if r['passed'] else 1)
