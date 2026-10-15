"""Actual14channel callback state, exact source starts/positions/retirement.

samples.cpp records source_num from the previous length before assigning the
new length: a first playback can be audible with source_num=-1. Model that
actual source behavior; never infer silence from source_num alone here.
"""
import copy,json,struct,wave
from pathlib import Path
import current_friendship_mix_model_v6254 as mix
ROOT,need,sha=mix.ROOT,mix.need,mix.sha

def gate(text,headers,waveform):
 events=waveform['completeMarkerEvents'];clips={}
 for number in{e['sample']for e in events}|{2,3}:
  path=ROOT/'samples/mk2ks'/(mix.NAMES[number]+'.wav')
  with wave.open(str(path),'rb')as reader:
   values=mix.np.frombuffer(reader.readframes(reader.getnframes()),'<i2').copy();frequency=reader.getframerate()
  _,positions=mix.original.sample_values(values,frequency)
  clips[number]=dict(length=len(values),positions=positions)
 precise=mix.original.rows(text,'MK2_TOMB_MIX_CHANNEL')
 need(len(precise)==14*len(headers)and
      {(int(r['index']),int(r['channel']))for r in precise}=={(i,n)for i in range(1,len(headers)+1)for n in range(14)},
      'All14 actual states at every sound callback exactly once')
 initial=clips[2]['positions'][-1]
 active_channels=set();observed_first_start_bug=set()
 for row in precise:
  index=int(row['index']);channel=int(row['channel']);head=headers[index-1]
  need(row['frame']==head['frame']and row['seconds']==head['seconds']and row['writes']=='0'and
       row['assistance']=='none'and row['loop']==row['paused']=='0','Exact finite actual callback state provenance')
  prior_events=[e for e in events if e['channel']==channel and mix.original.sample_clock(row['seconds'],True)>=e['start']]
  number=0xffffffff;length=32000 if channel==0 else 0;position=initial if channel==0 else 0.0
  if prior_events:
   event=prior_events[-1];clip=clips[event['sample']];length=clip['length']
   processed=max(0,mix.original.sample_clock(row['seconds'],True)-event['start'])
   count=min(processed,len(clip['positions']));position=clip['positions'][count-1]if count else 0.0
   if processed<len(clip['positions']):
    number=event['sample']if(channel==0 or len(prior_events)>1)else 0xffffffff
    active_channels.add(channel)
    if number==0xffffffff:observed_first_start_bug.add(channel)
  need(int(row['sample'])==number and int(row['length'])==length and
       row['bits']==struct.pack('<d',position).hex().upper()and float(row['position'])==position,
       'Exact source-derived clip number/retained length/repeated-double position bits and finite retirement')
 need(active_channels==set(waveform['sourceOrderedActiveChannels']),'Every actually mixed channel independently active in source state')
 tail=[r for r in precise if int(r['index'])==len(headers)]
 need(len(tail)==14 and all(r['sample']=='4294967295'for r in tail),'All14 actual imported streams retired by natural terminal')
 return dict(passed=True,exactSourceChannelStates=len(precise),actualMixedChannels=sorted(active_channels),
             sourceFirstPlaybackMetadataQuirkObservedOnChannels=sorted(observed_first_start_bug),
             wholeRepeatedDoublePositionBitsAccepted=True,completeNativeSampleRetirement=True)

def faults(text,headers,waveform):
 rows=text.splitlines();index=next(i for i,s in enumerate(rows)if s.startswith('MK2_TOMB_MIX_CHANNEL ')and 'position=0 'not in s and 'channel=0 'not in s)
 positive=gate(text,headers,waveform);row=dict(mix.original.rows(rows[index]+'\n','MK2_TOMB_MIX_CHANNEL')[0])
 rejected=[]
 for kind,key,value in [('wrong actual source number','sample','2'),('wrong actual source position bits','bits','0000000000000000'),
                        ('actual imported stream incorrectly looped','loop','1')]:
  need(row[key]!=value,'Nonvacuous actual source-state corruption')
  changed=rows.copy();bad=dict(row,**{key:value});changed[index]='MK2_TOMB_MIX_CHANNEL '+' '.join(f'{k}={v}'for k,v in bad.items())
  try:gate('\n'.join(changed),headers,waveform)
  except ValueError as error:rejected.append(dict(kind=kind,rejectedBy=str(error)))
  else:raise ValueError('Actual source-state fault accepted')
  need(gate(text,headers,waveform)==positive,'Whole unmodified channel positive restored')
 changed=rows.copy();changed.pop(index)
 try:gate('\n'.join(changed),headers,waveform)
 except ValueError as error:rejected.append(dict(kind='one actual callback channel state omitted',rejectedBy=str(error)))
 else:raise ValueError('Omitted actual channel accepted')
 return rejected
