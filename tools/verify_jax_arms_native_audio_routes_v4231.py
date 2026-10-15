"""Original Jax arm-rip selectors, true victims and complete native audio.

Original3952 generic full PCM/channel/packet/ADSP grammar retained, with an
explicit50Hz sound-update deadline instead of assuming one update each video
field. Original1074 whole earned arm state/palette/table grammar retained.
No all-arena, alternate, stock whole-waveform or full-port acceptance.
"""
import hashlib,inspect,json,re,struct
from pathlib import Path
import run_jax_arms_native_audio_routes_v4212 as capture
import verify_kitana_native_audio_queue_v3952 as previous
import verify_jax_clap_native_audio_routes_v4066 as clap
ROOT,need,sha=capture.ROOT,capture.need,capture.sha

DECLINE_REPORT=ROOT/'audit_v4230_sonya_p2_arm_audio_reject_observed/report.json'

def decline_gate(call,trace,guest):
    header,word=struct.unpack_from('<HH',guest,(0xffa0ef20-0xff800000)//8+int(call['a0'],16)*4)
    requested=header>>8;priorities=[int(trace['priority'+str(i)])for i in range(3)]
    need(trace['pc']=='FFA129E0'and trace['writes']=='0'and trace['assistance']=='none'and
         trace['frame']==call['frame']and trace['a8']==call['a8']and trace['a13']==call['a13']and
         float(call['seconds'])<float(trace['seconds'])<float(call['seconds'])+.0001,'Exact actual native reject PC, owner and call-time window')
    need(requested!=0x71 and all(p>requested for p in priorities)and int(trace['a0'],16)==priorities[-1]and
         int(trace['a1'],16)==requested and int(trace['a3'],16)==word and int(trace['a4'],16)==header&255,'All3 real native priorities exceed requested original table priority; registers and duration/base packet bound')
    return True

def decline_witness(call,guest):
    report=json.loads(DECLINE_REPORT.read_text())
    need(report['passed']and report['actualContext']=='sonyaP2'and report['allNativeEventsAndEntirePCMUnchangedByObserver'],'Actual strengthened observer leaves entire native waveform and all original events unchanged')
    traces=report['actualNativePriorityDeclines'];need(len(traces)==1,'Exactly1 observed native decline')
    trace=traces[0];decline_gate(call,trace,guest)
    folder=ROOT/'audit_v4229_jax_arms_reject_sonya_p2_audio_queue_samples'
    need(call in capture.rows((folder/'run.log').read_text(),'ROUTE'),'Missing original command is the actual same call in native reject trace')
    return trace

def folder(fighter,side,enabled):
    return ROOT/f"audit_v4213_jax_arms_{fighter}_p{side}_audio_queue_{'samples'if enabled else'nosamples'}"

def physical(text,fighter,side,guest):
    return capture.state.gate(text,fighter,side,guest,folder(fighter,side,True).name)

def stock_rows(text):
    return [dict(tag=tag,**r)for tag,r in capture.state.old.prior.rows(text,'MK2_STOCK_HEAD_V921')]

def tail(text,meta,guest,identity,side,origin,action,actual,chunks):
    rows=lambda tag:capture.rows(text,tag)
    routes=rows('ROUTE');general=[r for r in routes if r['entry']=='FFA12530'];special=[r for r in routes if r['entry']=='FFA12430']
    need(len(general)==48 and len(special)==7,'All original48 general arm effects and7 post-win selectors')
    voice=[r for r in routes if r['return_pc']=='FF8BF520']
    gender='FFA123B0'if identity==18 else'FFA122D0';base=0xb7 if identity==18 else 0x85
    need([r['entry']for r in voice]==['FFA12220',gender,'FFA123D0','FFA12530']and
         all(r['id']==str(identity)and r['a8']==r['owner']==action['victim_actor']and r['a13']==action['victim_main']for r in voice),'Original arm voice/gender route in true victim task, never proxy')
    need(voice[0]['a0']=='00000001'and voice[0]['a1']=='8585B8B7'and voice[2]['a0']=='00000001'and
         int(voice[2]['a1'],16)==base and int(voice[-1]['a0'],16)==base,'Actual original count-one packed85/B7 arm voice')
    fixed=[r for r in general if r['return_pc']=='FF8BE4D0']
    need(len(fixed)==1 and fixed[0]['a0']=='00000056'and fixed[0]['id']=='11'and fixed[0]['a8']==fixed[0]['owner']==action['actor']and
         fixed[0]['a13']==action['main'],'Original arm-rip effect56 owned by actual Jax11')
    drips=[r for r in general if r['return_pc']=='FF9A68F0']
    need(len(drips)==3 and all(r['a0']=='000000C4'and r['id']==str(identity)and r['a8']==r['owner']==action['victim_actor']for r in drips),'All3 native victim bleed effectsC4, true owned victim body')
    for pc,count in(('FF9B0CB0',35),('FF9AD190',8)):
        calls=[r for r in general if r['return_pc']==pc]
        need(len(calls)==count and all(0x73<=int(r['a0'],16)<=0x75 and r['a1']=='00000073'and r['id']=='0'and r['a8']==r['owner']for r in calls),'Original spawned blood count3/base73, effect ID0 not fighter proxy '+pc)
    need({r['return_pc']for r in general}=={'FF8BE4D0','FF8BF520','FF9A68F0','FF9B0CB0','FF9AD190'},'No unexplained general sound caller')
    postwin={'FFFB70D0':0x11,'FF82A010':5,'FF8213C0':0x28,'FF821830':0x16,'FF9AC870':0x29,'FF82C810':0,'FF82C8F0':1}
    need([r['return_pc']for r in special]==list(postwin)and all(int(r['a0'],16)==postwin[r['return_pc']]and r['id']=='-1'and int(r['frame'])>origin+147 for r in special),'All actual original announcer/win-page selectors after native147-field wrap')
    queues,packets,writes=rows('QUEUE'),rows('PACKET'),rows('SOUND')
    commands=sorted(general+special,key=lambda r:float(r['seconds']));records=[];declined=[]
    for index,call in enumerate(commands):
        stop=float(commands[index+1]['seconds'])if index+1<len(commands)else float('inf')
        command=int(call['a0'],16);table=0xffa10ee0 if call['entry']=='FFA12430'else 0xffa0ef20
        header,word=struct.unpack_from('<HH',guest,(table-0xff800000)//8+command*4)
        hits=[q for q in queues if float(call['seconds'])<=float(q['seconds'])<stop and q['a8']==call['a8']and q['a13']==call['a13']]
        if not hits:
            need(identity==18 and side==2 and call['return_pc']=='FF9B0CB0'and call['a0']=='00000074','Only the independently observed SonyaP2 blood call can take genuine full-priority decline')
            trace=decline_witness(call,guest)
            need(not any(float(call['seconds'])<=float(p['seconds'])<stop and p['a8']==call['a8']and p['a13']==call['a13']for p in packets),'Actual declined call emits no native packet')
            declined.append(dict(call=call,originalHeader=f'{header:04X}',originalBasePacket=f'{word:04X}',actualNativeDecline=trace));continue
        need(len(hits)==1,'One actual original priority slot per independently decoded selector');q=hits[0]
        slot={'FFA12A10':0,'FFA12A80':1,'FFA12B00':2}.get(q['entry'])
        need(slot is not None and int(q['a1'],16)==header>>8 and int(q['a4'],16)==header&255 and int(q['a3'],16)==word and q['frame']==call['frame'],'Original table priority/duration/base packet and native branch')
        hits=[p for p in packets if float(q['seconds'])<float(p['seconds'])<stop and p['frame']==call['frame']and p['a8']==call['a8']and p['a13']==call['a13']]
        need(len(hits)==1,'One complete native dispatch per selector');packet=hits[0]
        need(int(packet['a3'],16)==word+slot and packet['frame']==call['frame'],'Original selected-slot increment and actual packet')
        pair=[w for w in writes if float(packet['seconds'])<float(w['seconds'])<stop and w['a8']==call['a8']and w['a13']==call['a13']][:2]
        need(len(pair)==2 and tuple(int(w['word'],16)&255 for w in pair)==((word+slot)>>8,(word+slot)&255)and all(w['frame']==call['frame']for w in pair),'Every decoded original command reaches both actual port bytes')
        records.append(dict(command=command,caller=call['return_pc'],selector=call['entry'],frame=int(call['frame']),originalTable=f'{table:08X}',originalHeader=f'{header:04X}',originalBasePacket=f'{word:04X}',actualPrioritySlot=slot,actualPacket=f'{word+slot:04X}',actualCall=call,actualQueue=q,actualDispatch=packet,actualWrites=pair))
    begin=rows('BEGIN')[0];end=rows('RESULT')[0]
    need(all(int(r['bytes'])==3840 for r in chunks)and all(abs(float(b['seconds'])-float(a['seconds'])-.02)<1e-9 for a,b in zip(chunks,chunks[1:])), 'Every consecutive50Hz native update,960 stereo frames at48kHz; no missing callbacks')
    need(0<=float(chunks[0]['seconds'])-float(begin['seconds'])<.020000001 and 0<=float(end['seconds'])-float(chunks[-1]['seconds'])<.020000001,'Complete actual native sound-tick window from entry through last callback before exit')
    decoded=[r['actualDispatch']for r in records]
    extra=[p for p in packets if p not in decoded]
    need(len(declined)==(1 if identity==18 and side==2 else 0)and len(extra)==4,'Complete native selector admission/decline inventory and4direct packets')
    # The generic algorithm binds EVERY packet to both actual port bytes and
    # DSP reads. Later direct packets are not relabelled as selector calls:
    # their unobserved callers still require a separate origin trace.
    return dict(passed=True,identity=identity,side=side,origin=origin,terminalFrame=origin+750,nativePacketBytesDelivered=len(actual),completeNativePCMFrames=meta['mixedPCMBytesVerifiedInRAM']//4,completeNativePCMUpdates=len(chunks),actualCommands=records,actualNativeArmVoice=voice,allObservedSelectorCommandsSourceBound=True,allDispatchPacketsAndOwnersBound=True,fullPCMOnOffExactlyEqual=True,importedSampleChannelsIdle=True,actual50HzSoundDeadlineBound=True,
        actualNativePriorityDeclines=declined,additionalDirectNativePackets=extra,additionalDirectPacketCallerOriginsAccepted=False)

def make_gate():
    source=inspect.getsource(previous.audio_gate);marker='    # Fixed native inflation effect calls are unchanged original\n'
    need(source.count(marker)==1,'Whole generic PCM/channel/packet/ADSP grammar boundary');source=source[:source.index(marker)]
    changes={
      'physical=capture.state.gate(capture.state.rows(text),fighter,side,guest)':'physical=physical_gate(text,fighter,side,guest)',
      'capture.state.rows(text)':'stock_rows(text)',
      "begin[0]['id']=='4'":"begin[0]['id']=='11'",
      'Original Kitana task, not added-character proxy action':'Original Jax arm-rip task, not added-character proxy action',
      "int(chunks[-1]['frame'])==origin+749":"int(chunks[-1]['frame'])in(origin+748,origin+749)",
    }
    for before,after in changes.items():
        need(source.count(before)==1,'Unique actual arm state/owner/50Hz deadline adaptation');source=source.replace(before,after)
    source+='    return tail(text,meta,guest,identity,side,origin,action,actual,chunks)\n'
    ns=dict(capture=capture,ROOT=ROOT,need=need,hashlib=hashlib,tagged=previous.tagged,tail=tail,physical_gate=physical,stock_rows=stock_rows)
    exec(compile(source,__file__+'::original3952_generic_audio','exec'),ns)
    return ns['audio_gate']

audio_gate=make_gate()

def source_contract(guest):
    capture.state.source_boundary();capture.state.scene_state.source_contract(guest)
    # Shared native tables/voice/gender/packet routines, name trampoline and
    # silent inactive sample behavior independently source-qualified by4066.
    # Arm routines themselves retain their entire1074 owned-data contract.
    clap.source_contract(guest)
    stock=(ROOT/'mk2/mk2-maincpu.bin').read_bytes()
    for pc,command in ((0xff8be4d0,0x56),(0xff9a68f0,0xc4)):
        at=(pc-80-0xff800000)//8;wanted=struct.pack('<5H',0x09c0,command,0x0d5f,0x2530,0xffa1)
        need(guest[at:at+10]==stock[at:at+10]==wanted,'Original literal arm/bleed selector and CALLA '+hex(pc))
    for first,last in ((0xff9b0940,0xff9b0cc0),(0xff9ad140,0xff9ad1b0)):
        lo,hi=(first-0xff800000)//8,(last-0xff800000)//8
        need(guest[lo:hi]==stock[lo:hi],'Entire original randomized blood constructor/effect code unchanged')
    lo,hi=(0xffa12530-0xff800000)//8,(0xffa12bb0-0xff800000)//8
    need(guest[lo:hi]==stock[lo:hi],'Entire original table/priority admission/three-slot compare/CLRC reject/restore routine unchanged')
    report=json.loads(DECLINE_REPORT.read_text());need(report['passed'],'Actual native SonyaP2 priority witness terminal')
    for p,h in report['inputHashes'].items():need(sha(p)==h,'Actual decline trace inputs and full event/waveform comparator unchanged')

def qualify(fighter,side,guest):
    f,b=folder(fighter,side,True),folder(fighter,side,False)
    text=(f/'run.log').read_text();baseline=(b/'run.log').read_text()
    meta=json.loads((f/'result.json').read_text());oldmeta=json.loads((b/'result.json').read_text())
    for d,m in ((f,meta),(b,oldmeta)):
        for p,h in m['input_hashes'].items():need(sha(p)==h,'Actual executed input bytes unchanged')
        need(not list(d.rglob('*.png'))and not list(d.rglob('*.wav'))and not list(d.rglob('guest*.bin')),'No raw audio/raster/guest files')
    positive=audio_gate(text,baseline,meta,oldmeta,guest,fighter,side);faults=[]
    def reject(label,t=text,b=baseline,m=meta,o=oldmeta):
        try:audio_gate(t,b,m,o,guest,fighter,side)
        except (ValueError,KeyError)as error:faults.append(dict(kind=label,rejectedBy=str(error)))
        else:raise ValueError('Actual native arm audio fault accepted '+label)
        need(audio_gate(text,baseline,meta,oldmeta,guest,fighter,side)==positive,'Original positive restored after every actual fault')
    def mutate(tag,key,new,actual=None,prefix='MK2_MAUDIO_'):
        line=next(s for s in text.splitlines()if s.startswith(prefix+tag+' ')and(actual is None or dict(re.findall(r'(\w+)=([^\s]+)',s))==actual))
        changed,n=re.subn(r'\b'+key+r'=\S+',key+'='+new,line,count=1);need(n==1 and changed!=line,'Actual non-vacuous row fault')
        return text.replace(line,changed,1),baseline.replace(line,changed,1)
    for label,tag,key,new in (('wrong_origin','BEGIN','a8','01000000'),('phantom_sample','CHANNEL','sample','0'),('looping_voice','CHANNEL','loop','1'),('idle_advances','CHANNEL','pos','123.00000000'),('foreign_writer','SOUND','pc','FFF00000'),('wrong_byte','SOUND','word','FFF7')):
        t,b=mutate(tag,key,new);reject(label,t,b)
    fixed=positive['actualCommands'][0];voice=positive['actualNativeArmVoice']
    for label,tag,key,new,actual in (('wrong_effect','ROUTE','a0','00000057',fixed['actualCall']),('foreign_voice','ROUTE','a8','01000000',voice[0]),('wrong_gender','ROUTE','entry','FFA12380',voice[1]),('wrong_voice_byte','ROUTE','a1','00000030',voice[2]),('wrong_slot','QUEUE','entry','FFA12B00',fixed['actualQueue']),('wrong_table','QUEUE','a3','00000000',fixed['actualQueue']),('wrong_packet','PACKET','a3','00000000',fixed['actualDispatch'])):
        t,b=mutate(tag,key,new,actual);reject(label,t,b)
    for tag,key,new in (('FIRST_LIVE','ids','11,1'),('ACTION','address','FF8C7820'),('ACTION','damage','321'),('WRAP','age','146'),('RESULT','wins','3'),('APPROACH','gap','64'),('HEALTH','pc','FFF00000')):
        t,b=mutate(tag,key,new,prefix='MK2_STOCK_HEAD_V921_');reject('original_earned_'+tag+'_'+key,t,b)
    for key,new in (('preserved','0'),('victim','01000000'),('flags','0040')):
        t,b=mutate('STOCK_FALLBACK',key,new,prefix='MK2_ARM_PALETTE_V1073_');reject('native_palette_'+key,t,b)
    first=float(capture.rows(text,'SOUND')[0]['seconds']);last=float(capture.rows(text,'SOUND')[1]['seconds'])
    def remove_reads(t):return '\n'.join(l for l in t.splitlines()if not(l.startswith('MK2_MAUDIO_DELIVERY ')and first<=float(dict(re.findall(r'(\w+)=([^\s]+)',l))['seconds'])<last))+'\n'
    reject('missing_ADSP_read',remove_reads(text),remove_reads(baseline))
    line=next(l for l in text.splitlines()if l.startswith('MK2_BBAUDIO_PCM_DIGEST '))
    damaged=re.sub(r'sha256=\S+','sha256='+'0'*64,line);reject('different_PCM_update',text.replace(line,damaged,1))
    chunks=previous.tagged(text,'MK2_BBAUDIO_PCM_DIGEST');middle=next(l for l in text.splitlines()if l.startswith('MK2_BBAUDIO_PCM_DIGEST ')and 'seconds='+chunks[len(chunks)//2]['seconds']+' 'in l)
    reject('missing_native50Hz_update',text.replace(middle+'\n','',1),baseline.replace(middle+'\n','',1))
    return dict(fighter=fighter,side=side,nativeAudio=positive,actualRowCounterexamplesRejected=faults)
