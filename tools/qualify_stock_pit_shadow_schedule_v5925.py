"""Whole original stock capture requalified with native typed ownership and fonts.

The actual5924 failure stays immutable. An input-parser process is not the
physical fighter Main. Mode8 font FIFO draws are not fighter floor shadows.
Global shadow enable stays1 until physical retirement, then the native clear
table writes0. None of those phases invoke the actual floor-shadow kernel.
"""
import copy,collections,inspect
import capture_stock_pit_cinematic_shadow_v5921 as captured
from capture_stock_pit_cinematic_shadow_v5921 import *
OUT=ROOT/'audit_v5926_original_stock_pit_shadow_schedule_checked'
FAILED=ROOT/'audit_v5924_original_stock_pit_cinematic_shadow_checked/report.json'

def font_draws(text,stock,fields):
 commands=rows(text,'MK2_STOCK_CINE_MODE8');descriptors={}
 for r in commands:
  source,width,height=int(r['source'],16),int(r['width']),int(r['height'])
  need(r['pc']=='FF804640'and r['command']=='9008'and 0x04000000<=source<0x04010000,
       'Every observed non-floor mode8 command is original font FIFO, not shadow kernel or imported body')
  key=source,width,height
  if key not in descriptors:
   needle=struct.pack('<I',source);found=[];pos=0
   while True:
    at=stock.find(needle,pos)
    if at<0:break
    pos=at+1;address=0xff800000+(at-8)*8
    if at>=8 and 0xffc00000<=address<0xffc10000 and struct.unpack_from('<HH',stock,at-8)==(width,height)and struct.unpack_from('<H',stock,at+4)[0]==0x1000:
     found.append(address)
   need(found,'Actual original font source, width,height and1bpp descriptor independently owned')
   descriptors[key]=found
 counts=collections.Counter(int(r['frame'])for r in commands)
 need(all(int(r['mode8'])==counts[int(r['frame'])]for r in fields)and sum(int(r['mode8'])for r in fields)==len(commands),
      'Every actual observed font command counted in its completed field, no omitted mode8 ledger')
 return dict(actualOriginalFontCommands=len(commands),actualOriginalFontDescriptors=len(descriptors),actualFloorShadowCommands=0,
             descriptorBindings=[dict(source=f'{s:08X}',width=w,height=h,originalDescriptors=[f'{a:08X}'for a in addresses])for(s,w,h),addresses in sorted(descriptors.items())])

def shadow_phase(text,fields):
 retired=next(int(r['frame'])for r in fields if r['p1']==r['p2']=='00000000')
 need(all(int(r['entries'])==int(r['copies'])==0 and int(r['shadow_enable'],16)==(1 if int(r['frame'])<retired else 0)for r in fields)and
      not rows(text,'MK2_STOCK_CINE_SHADOW_ENTRY'),
      'Whole original native shadow schedule: no floor kernel in any phase, enable1 until physical retirement then0')
 stores=rows(text,'MK2_STOCK_CINE_ENABLE_STORE')
 need(stores and stores[0]['at']=='0105EBC0'and stores[0]['before']=='0001'and stores[0]['value']=='0000'and
      stores[0]['mask']=='FFFF'and stores[0]['pc']=='FF841C20'and int(stores[0]['frame'])==retired and
      all(r['at']=='0105EBC0'and r['value']=='0000'and r['mask']=='FFFF'for r in stores),
      'Actual native short-clear table drops shadow-enable exactly at original physical retirement')
 return dict(actualPhysicalRetirementFrame=retired,nativeShadowEnableClearPC='FF841C20',actualFloorShadowCopies=0)

source=inspect.getsource(captured.finish)
source=source.replace('def finish(text,stock,pins,code,initialized):','def schedule(text,stock,pins,code,initialized,port_guest):',1)
old="need([r['entry']for r in gate]==wanted and all(r['id']=='2'and r['a8']==b['actor']and r['a13']==b['main']for r in gate),"
new="need([r['entry']for r in gate]==wanted and all(r['id']=='2'and r['a8']==b['actor']and r['a13']==gate[0]['a13']for r in gate)and gate[0]['a13']!=b['main']and gate[-2]['a0']==b['main'],"
need(source.count(old)==1,'One exact failed parser-Main versus physical-Main conflation')
source=source.replace(old,new,1)
first=source.index(" need(all(int(r['shadow_enable']")
last=source.index(' guest=current.expected();',first)
source=source[:first]+" phase=shadow_phase(text,fields)\n fonts=font_draws(text,stock,fields)\n"+source[last:]
source=source.replace('guest=current.expected();off=', 'guest=port_guest;off=',1)
source=source.replace('(0xff801000,0xff8017b0)):', '(0xff801000,0xff8017b0),(0xff841be0,0xff841c40)):',1)
source=source.replace('originalGlobalShadowEnable=0,originalNativeShadowEntries=0,originalNativeShadowCopies=0,originalAllMode8Copies=0,',
 'sourceNativeShadowPhase=phase,sourceNativeNonFloorFontDraws=fonts,originalNativeShadowEntries=0,originalNativeShadowCopies=0,',1)
scope=dict(globals(),__file__=__file__,font_draws=font_draws,shadow_phase=shadow_phase)
exec(compile(source,__file__+'::whole5921_native_typed_parser_shadow_and_font_schedule','exec'),scope)
schedule=scope['schedule'];schedule.source=source

def run():
 need(not OUT.exists(),'Fresh immutable original native schedule qualification, no reboot')
 failed=json.loads(FAILED.read_text());terminal=json.loads((FOLDER/'terminal.json').read_text())
 need(failed['passed']is False and failed['error']=="ValueError('Complete actual original history/range/finish/opponent/action gate chain, true owned Cage')"and
      terminal['exit_code']==0 and not(FOLDER/'stderr.log').read_text(),'Preserve exact actual5924 post-gate failure and clean native terminal')
 with gzip.open(FOLDER/'run.log.gz','rt')as f:text=f.read()
 need('Average speed:'in text and 'DEADLINE'not in text and not re.search(r'LUA ERROR|Lua error|stack traceback|WRONG CHECKSUMS',text),
      'Whole actual original run, no hidden runtime/deadline failure')
 pins=json.loads((FOLDER/'input_hashes_before.json').read_text())
 for p in (Path(__file__),Path(captured.__file__),Path(previous.__file__),FAILED,ROOT/'mk2_stock_pit_shadow_inventory_v5916.lua',
           ROOT/'mk2_stock_pit_cinematic_shadow_v5920.lua',FOLDER/'run.log.gz',FOLDER/'terminal.json',FOLDER/'process.json'):
  pins[str(p)]=sha(p)
 need(all(sha(p)==h for p,h in pins.items()),'Whole executed/current/original/failed sources and buffers unchanged')
 stock=STOCK.read_bytes();guest=current.expected()
 initialized=rows(text,'MK2_STOCK_PIT_GUEST_DIGEST')
 need(len(initialized)==1 and initialized[0]['bytes']=='1048576'and initialized[0]['sha256']==sha(STOCK),
      'Actual whole initialized stock guest, not a proxy or reconstructed comparison target')
 positive=schedule(text,stock,pins,0,sha(STOCK),guest)
 tests=[]
 def reject(name,changed,code=guest):
  need(changed!=text or code!=guest,'Non-vacuous mutation of actual stock evidence/source')
  try:schedule(changed,stock,pins,0,sha(STOCK),code)
  except ValueError as error:tests.append(dict(name=name,rejectedBy=str(error)))
  else:raise ValueError('Altered actual original Pit shadow schedule accepted '+name)
 lines=text.splitlines()
 def changed(tag,key,value,choose=lambda r:True):
  result=list(lines)
  for i,line in enumerate(result):
   if not line.startswith(tag+' '):continue
   r=dict(re.findall(r'(\w+)=([^\s]+)',line))
   if not choose(r):continue
   result[i]=re.sub(r'\b'+key+r'=[^\s]+',key+'='+str(value),line,count=1);return '\n'.join(result)+'\n'
  raise ValueError('No actual field available for fault '+tag+' '+key)
 reject('foreign native parser process',changed('MK2_STAGE_ENTRY','a13','00000000',lambda r:r['entry']=='FF876E50'))
 reject('input process substituted for physical fighter Main',changed('MK2_STOCK_CINE_BEGIN','main','0106CD10'))
 reject('shadow-enable survives physical retirement',changed('MK2_STOCK_CINE_FIELD','shadow_enable','0001',lambda r:r['p1']==r['p2']=='00000000'))
 reject('native shadow kernel falsely activated',changed('MK2_STOCK_CINE_FIELD','entries','1'))
 reject('physical shadow copy falsely present',changed('MK2_STOCK_CINE_FIELD','copies','1'))
 reject('font misattributed to native shadow kernel',changed('MK2_STOCK_CINE_MODE8','pc','FF8015A0'))
 reject('one-bit shifted actual original font source',changed('MK2_STOCK_CINE_MODE8','source','04000BE2'))
 reject('changed original font width',changed('MK2_STOCK_CINE_MODE8','width','999'))
 reject('omitted actual font ledger count',changed('MK2_STOCK_CINE_FIELD','mode8','0',lambda r:int(r['mode8'])>0))
 reject('wrong native shadow clear PC',changed('MK2_STOCK_CINE_ENABLE_STORE','pc','FF841C10'))
 rejected_field=next(s for s in lines if s.startswith('MK2_STOCK_CINE_FIELD '))
 reject('omitted completed physical field',text.replace(rejected_field+'\n','',1))
 for address,name in ((0xff8046f0,'native global shadow dispatcher source'),(0xff801090,'native actor shadow eligibility source'),
                       (0xff841c10,'native short-clear source')):
  code=bytearray(guest);code[(address-0xff800000)//8]^=1;reject(name,text,bytes(code))
 need(len(tests)==14 and schedule(text,stock,pins,0,sha(STOCK),guest)==positive,'All14 actual schedule/source faults reject and complete positive restores')
 positive.update(effectiveActualScheduleFaultsRejected=tests,newNativeBoots=0,executedFailedPostGatePreserved=str(FAILED),
   originalStockPitShadowSchedulingAccepted=True,currentPortShadowPolicyAccepted=False,
   previousGoalTurnClassification='progress: physically earned original ordinary Pit and original cinematic captures change next action',
   thisGoalTurnClassification='progress: source-native ownership and every original font mode8 draw qualified independently from absent floor shadow calls,14actual data/source corruptions rejected',
   fullPortAcceptance=False,qualifierSourceSHA256=sha(Path(__file__)))
 return positive

if __name__=='__main__':
 try:report=run()
 except Exception as error:report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),goalStatus='active',fullPortAcceptance=False)
 OUT.mkdir();save(OUT/'report.json',report)
 for p in (Path(__file__),OUT/'report.json'):
  before=sha(p);done=subprocess.run(['compact.exe','/C','/F','/EXE:LZX','/Q',str(p)],capture_output=True)
  need(done.returncode==0 and sha(p)==before,'Lossless bounded qualified text')
 print(json.dumps({k:v for k,v in report.items()if k not in('inputHashes','remaining','sourceNativeCommand','sourceNativeNonFloorFontDraws','effectiveActualScheduleFaultsRejected')},indent=2),flush=True)
 raise SystemExit(0 if report['passed']else 1)
