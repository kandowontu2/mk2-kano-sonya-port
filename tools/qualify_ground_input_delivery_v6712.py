"""Actual IN0/IN2 delivery and full original physical/body/recovery contract.

This attempt has no incoming hit. It remains unexercised for interruption;
correct input delivery, repeated native actions and actual damage are separate
evidence. Preserve original sound-status label and lexical failures unchanged.
"""
import collections,json,re,subprocess
from pathlib import Path
import launch_interruption_model_v6689 as model
ROOT,need,sha=model.ROOT,model.need,model.sha


def delivered(text):
 controls=collections.defaultdict(list)
 high={'Up':1,'Down':2,'Left':4,'Right':8,'High_Punch':16,'Block':32,'High_Kick':64}
 low={'Low_Punch':1,'Low_Kick':2}
 for tag in('MK2_HSPECIAL_INPUT','MK2_INTERRUPT_INPUT'):
  for r in model.rows(text,tag):
   need(r['writes']=='0'and r['assistance']=='none'and r['slot']in('1','2')and r['button']in high.keys()|low.keys()|{'Coin','Start'},'Complete physical controller inventory, including boot/selection IN1 operations')
   controls[int(r['frame'])].append(r)
 def expected(frame,table,stride):
  return 65535-sum({table[r['button']]<<(stride*(int(r['slot'])-1))for r in controls[frame-1]if r['button']in table})
 counts={};traces={}
 for tag,address,table,stride in [('MK2_INTERRUPT_IO','01600000',high,8),('MK2_INTERRUPT_LOW_IO','01600020',low,4)]:
  rows=model.rows(text,tag);need(rows,'Every actual port has real native reads')
  for r in rows:
   need(r['at']==address and r['mask']=='FFFF'and r['writes']=='0'and r['assistance']=='none'and
        int(r['value'],16)==expected(int(r['frame']),table,stride),'Every actual native port word exactly matches preceding physical input-update callbacks: '+tag)
  irq=[r for r in rows if r['pc']==('FF8171E0'if stride==8 else'FF817330')]
  ready=int(model.rows(text,'MK2_HSPECIAL_READY')[0]['frame']);last=int(model.rows(text,'MK2_HSPECIAL_RESULT')[0]['frame'])
  need([int(r['frame'])for r in irq]==list(range(ready,last)),'Every original native IRQ field through final draw retained; queued terminal callback does not execute another IRQ: '+tag)
  counts[address]=len(rows);traces[address]=len(irq)
 return dict(passed=True,completeNativeReads=counts,completeIRQFields=traces,wholeBothPlayerPhysicalBitDeliveryAccepted=True,
             sourceCadence='Native ioport input-update precedes emu.register_frame overrides; the original next-field IRQ reads those overrides')


def qualify(carrier):
 out=ROOT/'audit_v6713_ground_input_delivery_checked'
 need(not out.exists()and carrier['report']['passed']and carrier['terminal']['nativeExit']==0 and not carrier['decodeErrors'],'Fresh same-terminal qualification')
 pins=dict(carrier['pins']);need(all(sha(p)==h for p,h in pins.items()),'Actually executed source/candidate pins intact')
 incoming=[r for r in model.rows(carrier['text'],'MK2_INTERRUPT_HEALTH')if int(r['slot'])==carrier['side']and int(r['after'])<int(r['before'])]
 need(not incoming,'Do not promote this real miss to an interruption acceptance')
 compiled=ROOT/model.current.NAME/'input_sources/mame-mkp/src/mame/midway/midtunit.cpp'
 source=compiled.read_text()
 for statement in('map(0x01600000, 0x0160000f).portr("IN0");','map(0x01600020, 0x0160002f).portr("IN2");',
                  'map(0x01d00000, 0x01d0001f).r(FUNC(midtunit_state::midtunit_sound_state_r));'):
  need(source.count(statement)==1,'Actual compiled native address-map source, not the previous observer label')
 proof=delivered(carrier['text']);faults=[]
 for tag in('MK2_INTERRUPT_IO','MK2_INTERRUPT_LOW_IO'):
  line=next(s for s in carrier['text'].splitlines()if s.startswith(tag+' '));value=re.search(r'\bvalue=(\w+)',line)[1]
  bad=carrier['text'].replace(line,line.replace('value='+value,'value='+format(int(value,16)^1,'04X'),1),1)
  try:delivered(bad)
  except ValueError as error:faults.append(dict(fault=tag+' actual bit flipped',rejectedBy=str(error)))
  else:raise ValueError('Actual port-bit fault admitted')
  bad=carrier['text'].replace(line+'\n','',1)
  try:delivered(bad)
  except ValueError as error:faults.append(dict(fault=tag+' original IRQ callback omitted',rejectedBy=str(error)))
  else:raise ValueError('Omitted real original IRQ field admitted')
 code=(ROOT/'tools/launch_interruption_model_v6686.py').read_text()
 code=code[code.index('def phase(carrier):'):code.index(" health=rows(text,'MK2_INTERRUPT_HEALTH')")]+" return whole\n"
 scope=dict(vars(model));exec(compile(code,__file__+'::entire_original_physical_body_gate_no_incoming_claim','exec'),scope)
 physical=scope['phase'](carrier)
 need(physical['twoRealSpecialCyclesAndCleanupVerified'],'Both complete real native cycles, ordinary follow-up and source body/FIFO contract')
 for p in(Path(__file__),Path(model.__file__),ROOT/'tools/launch_interruption_model_v6686.py',compiled,
          ROOT/'mame-mkp/src/emu/ioport.cpp',ROOT/'mk2ks_launch_ground_io_v6706.lua',ROOT/'mk2ks_launch_ground_io_fixed_v6709.lua',
          ROOT/'source_history_v6714/qualify_ground_input_delivery_v6712.py',ROOT/'audit_v6714_input_inventory_rejection/failure.json',*carrier['folder'].rglob('*')):
  if p.is_file():pins[str(p.resolve())]=sha(p)
 need(delivered(carrier['text'])==proof and all(sha(p)==h for p,h in pins.items()),'Positive and complete executed source/evidence intact')
 report=dict(passed=True,actualNativeTerminal=carrier['terminal'],nativeInputDelivery=proof,wholePhysicalAndBodyContract=physical,
             actualInputFaultsRejected=faults,inputHashes=pins,correctedPriorObserverAddress='01D00000 is DCS status, not IN0',
             noUppercutEntriesObserved=not model.rows(carrier['text'],'MK2_INTERRUPT_UPPERCUT'),genuineIncomingHealthStores=0,
             gameplayInterruptionAccepted=False,sourceWaveformAccepted=False,fullPortAcceptance=False,goalStatus='active',
             newNativeBoots=0,newBuilds=0,newROMCopies=0,newZIPs=0,newRawMedia=0)
 out.mkdir();p=out/'report.json';p.write_text(json.dumps(report,indent=2)+'\n');h=sha(p)
 need(subprocess.run(['compact.exe','/C','/EXE:LZX','/F','/I','/Q',str(p)],capture_output=True).returncode==0 and sha(p)==h,'Lossless exact finite proof')
 print(json.dumps(dict(passed=True,nativeReads=proof['completeNativeReads'],IRQFields=proof['completeIRQFields'],actualFaults=len(faults),interruptionAccepted=False)),flush=True)
 return report
