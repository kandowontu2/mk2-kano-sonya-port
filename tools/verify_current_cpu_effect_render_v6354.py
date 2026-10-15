"""Keep failed capture; explicitly verify its numeric-word/digest transport.

The6348 formatter hashes every data field, including16bit allocator words.
This is not a runtime difference: compare every old numeric observation's
exact two-byte digest and every other character, preserving the failed report.
No guest address/state normalization, dropped rows, new emulator or raw files.
Full641-field raster/FIFO/owned-palette/art/erase gate stays intact.
"""
import gzip,hashlib,inspect,json,re
from pathlib import Path
import verify_current_cpu_effect_render_v6350 as prior
ROOT,need,sha=prior.ROOT,prior.need,prior.sha
OUT=ROOT/'audit_v6355_current_cpu_effect_render_checked'


def transport_contract():
 meta=json.loads((prior.CASE/'result.json').read_text());terminal=json.loads((prior.CASE/'native_terminal.json').read_text())
 need(meta['passed']is False and meta['error']=="ValueError('Whole actual input/AI/RNG/health/state/pool chronology unchanged')"and
      meta['nativeExit']==terminal['exitCode']==0 and terminal['naturalTerminal']and not terminal['observationErrors']and
      meta['proof']['everyActualByteComparedInRAM']and meta['proof']['sha256']==prior.capture.terminal.current.GUEST_SHA,
      'Exact recorded serialization-only rejection after terminal0, whole guest and error-free complete model')
 need(meta['independentSemantics']['blade']['bodyFields']==38 and len(meta['independentSemantics']['knives'])==1,
      'Full original native motion/state/HP/choice gate actually completed before serialization rejection')
 with gzip.open(prior.CASE/'run.log.gz','rt',encoding='utf-8')as file:current=file.read()
 previous=ROOT/'audit_v6342_current_cpu_blade_allocation_ram/run.log.gz'
 qualified=json.loads((ROOT/'audit_v6344_current_cpu_blade_allocation_checked/report.json').read_text())
 need(qualified['passed']and sha(previous)==qualified['inputHashes'][str(previous)],'Original actual native allocation chronology qualified and immutable')
 with gzip.open(previous,'rt',encoding='utf-8')as file:old=file.read()
 prefixes=('MK2_CPU_PAIR_','MK2_P2CPU_','MK2_CPU_ROUND_','MK2_CPU_OVERLAP_','MK2_KNIFE_PAIR_','MK2_CPU_CHOICE_','MK2_BLADE_ALLOC_')
 def word_to_digest(line):
  word=re.search(r'\bdata=([0-9A-F]{4})(?=\s)',line)
  if not word:return line
  digest=hashlib.sha256(bytes.fromhex(word[1])).hexdigest().upper()
  return line[:word.start()]+'data_sha256='+digest+line[word.end():]
 actual=[line for line in current.splitlines()if line.startswith(prefixes)]
 wanted=[word_to_digest(line)for line in old.splitlines()if line.startswith(prefixes)]
 need(actual==wanted,'Every entire original record exact under declared two-byte numeric digest transport, no omitted fields/rows')
 words=sum(bool(re.search(r'\bdata=[0-9A-F]{4}(?=\s)',line))for line in old.splitlines()if line.startswith(prefixes))
 need(words==3326,'Every actual free-head and parent-field numeric half-store included')
 # Recover counters only from exact source-model operation tags, not guessed
 # timings or accepted targets. Model fields were persisted before rejection.
 kinds={}
 for line in current.splitlines():
  if line.startswith('MK2_NAT_CAMPAIGN_'):
   kind=line.split()[0];kinds[kind]=kinds.get(kind,0)+1
 records=json.loads((prior.CASE/'continuous_scene_records.json').read_text())
 need(len(records)==641 and [r['frame']for r in records]==list(range(1870,2511)),
      'Every complete source-perfect scene actually modeled before independent chronology formatting check')
 shifts=[];fills=[];dispatch=[]
 for line in current.splitlines():
  if line.startswith(('MK2_NAT_CAMPAIGN_FLOOR_SHIFT_FILL ','MK2_NAT_CAMPAIGN_FLOOR_SHIFT ','MK2_NAT_CAMPAIGN_FLOOR_QUEUE_DISPATCH ')):
   tag,row=prior.model.parse(line)
   if tag=='FLOOR_SHIFT_FILL':fills.append(row)
   elif tag=='FLOOR_SHIFT':shifts.append(row)
   else:dispatch.append(row)
 meta['continuousRender']=dict(fields=len(records),exactRGBPixels=sum(r['exactRGBPixels']for r in records),
    preBuffers=kinds.get('MK2_NAT_CAMPAIGN_FLOOR_PRE_FRAME',0),flips=sum(r['modeledFlip']for r in records),
    shiftLoads=kinds.get('MK2_NAT_CAMPAIGN_FLOOR_SHIFT_LOAD',0),shiftFills=len(fills),
    shiftTransfers=len(shifts)+sum(len(prior.model.original.erase.copies_for_fill(r))for r in fills),
    cpuWrites=kinds.get('MK2_NAT_CAMPAIGN_FLOOR_CPU',0),paletteChecks=sum(1869<=r['frame']<2510 for r in dispatch),
    actualPixelFaultGuardsExercised=2,
    actualPixelGuardEvidence='Unchanged mandatory first-snapshot VRAM/RGB bit guards followed by all641fields without any model error; rejection messages were not persisted by failed collector',
    oneInitialBaseOnly=kinds.get('MK2_NAT_CAMPAIGN_FLOOR_BASE',0)==1,comparisonTargetsNeverSeedReplay=True,
    countersSource='Persisted exact native operation tags and original model records, not missing failed-capture summary')
 need(meta['continuousRender']['oneInitialBaseOnly'],'One actual initial VRAM base, not later comparison reseeding')
 return meta,terminal,dict(originalCapturePassed=False,originalCaptureRejectionPreserved=True,
       wholeOriginalChronologyVerified=True,exactOriginalRecordRows=len(actual),numericWordsCryptographicallyCompared=words,
       allNonwordCharactersExact=True,guestAddressNormalization=False,newNativeBoots=0)


def main():
 failure=ROOT/'audit_v6351_current_cpu_effect_render_checked/failure.json'
 need(not json.loads(failure.read_text())['passed'],'Earlier premature report-read failure retained')
 source=inspect.getsource(prior.main)
 changes={
  "meta=json.loads((CASE/'result.json').read_text());terminal=json.loads((CASE/'native_terminal.json').read_text())":'meta,terminal,serialization_record=transport_contract()',
  "meta['passed']and terminal['naturalTerminal']":"serialization_record['wholeOriginalChronologyVerified']and terminal['naturalTerminal']",
  "meta['originalWholePhysicalTrajectoryUnchanged']":"serialization_record['wholeOriginalChronologyVerified']",
  'for path in(PARENT,Path(__file__),':"for path in(ROOT/'tools/verify_current_cpu_effect_render_v6350.py',ROOT/'tools/verify_current_cpu_effect_render_v6352.py',ROOT/'audit_v6351_current_cpu_effect_render_checked/failure.json',PARENT,Path(__file__),",
  "goalStatus='active',parentAdditiveJournal=str(PARENT)":"goalStatus='active',serializationRecord=serialization_record,parentAdditiveJournal=str(PARENT)",
 }
 for before,after in changes.items():
  need(source.count(before)==1,'Only explicit serialization acceptance bridge, full render/art/geometry/fault gate unchanged');source=source.replace(before,after,1)
 scope=dict(prior.__dict__,__file__=__file__,OUT=OUT,transport_contract=transport_contract)
 exec(compile(source,__file__+'::complete_effect_gate_actual_numeric_digest_transport','exec'),scope)
 scope['main']()


if __name__=='__main__':
 try:main()
 except Exception as error:
  import traceback
  OUT.mkdir(exist_ok=True);(OUT/'failure.json').write_text(json.dumps(dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False),indent=2)+'\n');raise
