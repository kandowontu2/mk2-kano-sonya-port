"""Entire original3908 native fixed-effect/queue/packet/ADSP algorithm.

The obsolete paired3836 metadata/PCM gate is not fabricated. Current live
source DAC/PCM/ROM prediction is a separate prerequisite. Retain every
original fixed caller, command-table, queue slot, packet byte and DSP read.
"""
import inspect,re,struct
import verify_mileena_native_audio_queue_v3908 as prior
import capture_current_mileena_source_audio_v6232 as host
ROOT,need,sha=host.ROOT,host.need,host.sha

def native_routes(text,guest,fighter,side):
 source=inspect.getsource(prior.audio_gate)
 marker="    writes=rows('SOUND');delivery=rows('DELIVERY')"
 need(source.count(marker)==1,'Complete original native packet/fixed effect boundary')
 source=source[source.index(marker):]
 replacements=(("meta['mixedPCMBytesVerifiedInRAM']//4","sum(int(r['bytes'])for r in chunks)//4"),
               ("fullPCMOnOffExactlyEqual=True","fullSourcePCMPredictionRequiredSeparately=True"))
 for before,after in replacements:
  need(source.count(before)==1,'Only current source-audio metadata obligation changes')
  source=source.replace(before,after,1)
 prefix='''def gate(text,guest,fighter,side):
    identity=17 if fighter=='kano'else 18
    physical=host.state(text,fighter,side,guest)
    origin=physical['actionFrame']
    rows=lambda tag:prior.capture.rows(text,tag)
    begin=rows('BEGIN');result=rows('RESULT')
    need(len(begin)==len(result)==1 and begin[0]['origin']==str(origin)and begin[0]['id']=='5'and
         result[0]['origin']==str(origin)and int(result[0]['frame'])==origin+601,'One true stock5 native action and complete601 terminal')
    action=next(r for r in host.health.original.parse(text)if r['tag']=='ACTION')
    need(begin[0]['a8']==f"{action['actor']:08X}"and begin[0]['a13']==f"{action['main']:08X}",
         'Actual native Mileena action owns the real stock actor/task, not a proxy victim')
    chunks=prior.tagged(text,'MK2_BBAUDIO_PCM_DIGEST')
    need(chunks and all(int(r['bytes'])==3840 for r in chunks)and
         int(chunks[0]['frame'])in(origin,origin+1)and int(chunks[-1]['frame'])==origin+600,
         'All complete captured native audio callbacks through the original600field window')
'''
 scope=dict(prior.audio_gate.__globals__,prior=prior,host=host)
 exec(compile(prefix+source,__file__+'::entire_original3908_fixed_native_effects_and_delivery','exec'),scope)
 return scope['gate'](text,guest,fighter,side)

def source_contract(guest):
 stock=(ROOT/'mk2/mk2-maincpu.bin').read_bytes()
 for first,last in((0xff8d2410,0xff8d2b70),(0xffa0ef20,0xffa10ee0),(0xffa12530,0xffa13df0)):
  lo,hi=(first-0xff800000)//8,(last-0xff800000)//8
  need(guest[lo:hi]==stock[lo:hi],'Whole original swallowing/effect table/native packet dispatcher source unchanged')
 return True

def faults(text,guest,fighter,side):
 positive=native_routes(text,guest,fighter,side);rejected=[]
 def reject(label,bad):
  need(bad!=text,'Actual native audio row changed')
  try:native_routes(bad,guest,fighter,side)
  except (ValueError,KeyError)as error:rejected.append(dict(kind=label,rejectedBy=str(error)))
  else:raise ValueError('Accepted actual native sound fault '+label)
  need(native_routes(text,guest,fighter,side)==positive,'Complete source-audio positive restored')
 def alter(tag,actual,key,value):
  line=next(s for s in text.splitlines()if s.startswith('MK2_MAUDIO_'+tag+' ')and dict(re.findall(r'(\w+)=([^\s]+)',s))==actual)
  bad,n=re.subn(r'\b'+key+r'=\S+',key+'='+value,line,count=1)
  need(n==1 and bad!=line,'Exact actual field counterexample')
  return text.replace(line,bad,1)
 fixed=positive['actualNativeFixedEffects'][0]
 queue=fixed['actualQueue'];packet=fixed['actualDispatch']
 wrongslot=(fixed['actualPrioritySlot']+1)%3
 reject('actual selected priority slot',alter('QUEUE',queue,'entry',('FFA12A10','FFA12A80','FFA12B00')[wrongslot]))
 reject('actual priority/header',alter('QUEUE',queue,'a1',f"{int(queue['a1'],16)^1:08X}"))
 reject('actual base sound packet',alter('QUEUE',queue,'a3',f"{int(queue['a3'],16)^1:08X}"))
 reject('actual dispatched packet',alter('PACKET',packet,'a3',f"{int(packet['a3'],16)^1:08X}"))
 writes=prior.capture.rows(text,'SOUND');first=writes[0]
 reject('actual port writer',alter('SOUND',first,'pc','FFF00000'))
 reject('actual full native sound word',alter('SOUND',first,'word',f"{int(first['word'],16)^1:04X}"))
 start=float(first['seconds']);end=float(writes[1]['seconds'])
 bad='\n'.join(s for s in text.splitlines()if not(s.startswith('MK2_MAUDIO_DELIVERY ')and
     start<=float(dict(re.findall(r'(\w+)=([^\s]+)',s))['seconds'])<end))+'\n'
 reject('actual first ADSP delivery omitted',bad)
 return rejected
