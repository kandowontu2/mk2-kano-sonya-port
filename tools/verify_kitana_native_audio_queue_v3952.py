"""Qualified3836 native Kitana inflation audio; no full-fidelity shortcut.

Full samples-on/off native PCM equality is bound to actual streamed digests.
Original fixed effect lookup/packets and physical task/state are independent.
Stock references contain legitimate RNG-dependent bone sounds; neither their
whole recording difference nor same-build evidence proves universal fidelity.
"""
import copy,hashlib,json,re,struct,subprocess,traceback
from pathlib import Path
import run_kitana_native_audio_queue_v3940 as capture
ROOT,need,sha=capture.ROOT,capture.need,capture.sha
OUT=ROOT/'audit_v3953_kitana_native_audio_queue_checked'

def tagged(text,prefix):
    return[dict(re.findall(r'(\w+)=([^\s]+)',line))for line in text.splitlines()if line.startswith(prefix+' ')]

def audio_gate(text,baseline,meta,oldmeta,guest,fighter,side):
    identity=17 if fighter=='kano'else 18
    need(meta['fighter']==oldmeta['fighter']==fighter and meta['side']==oldmeta['side']==side and
         meta['candidate']==oldmeta['candidate']==capture.NAME and meta['exit_code']==oldmeta['exit_code']==0 and
         meta['samples_enabled']and not oldmeta['samples_enabled']and not meta['stockReferenceOnly']and not oldmeta['stockReferenceOnly'],'Actual added-character paired context; references never relabelled as own')
    need(meta['guestSHA256']==oldmeta['guestSHA256']==hashlib.sha256(guest).hexdigest().upper()and
         meta['mixedPCMBytesVerifiedInRAM']==oldmeta['mixedPCMBytesVerifiedInRAM']and
         meta['mixedPCMSHA256']==oldmeta['mixedPCMSHA256']and meta['mixedPCMUpdates']==oldmeta['mixedPCMUpdates'],'Every actual native streamed whole guest/PCM byte bound; no phantom imported contribution')
    chunks=tagged(text,'MK2_BBAUDIO_PCM_DIGEST');oldchunks=tagged(baseline,'MK2_BBAUDIO_PCM_DIGEST')
    need(chunks==oldchunks and len(chunks)==meta['mixedPCMUpdates']and sum(int(r['bytes'])for r in chunks)==meta['mixedPCMBytesVerifiedInRAM']and
         all(float(a['seconds'])<float(b['seconds'])for a,b in zip(chunks,chunks[1:])),'Every whole native sound update digest/byte count/order identical samples on/off')
    physical=capture.state.gate(capture.state.rows(text),fighter,side,guest)
    selected=lambda t:[line for line in t.splitlines()if line.startswith('MK2_STOCK_HEAD_V921_')]
    need(selected(text)==selected(baseline),'Every actual original physical command/damage/native victim state unchanged by sample playback')
    rows=lambda tag:capture.rows(text,tag)
    for tag in('BEGIN','ROUTE','QUEUE','PACKET','SOUND','DELIVERY','RESULT'):need(rows(tag)==capture.rows(baseline,tag),'Every actual native audio '+tag+' event identical')
    begin=rows('BEGIN');result=rows('RESULT');need(len(begin)==len(result)==1,'One actual audio origin and stop')
    origin=int(begin[0]['origin']);need(origin==physical['origin']and result[0]['origin']==str(origin)and int(result[0]['frame'])==origin+750 and
         int(chunks[0]['frame'])in(origin,origin+1)and int(chunks[-1]['frame'])==origin+749,'Complete actual original fatality sound window through749callbacks')
    actions=[r for r in capture.state.rows(text)if r['tag']=='ACTION'];action=actions[0]
    need(begin[0]['a8']==action['actor']and begin[0]['a13']==action['main']and begin[0]['id']=='4','Original Kitana task, not added-character proxy action')
    channels=rows('CHANNEL');oldchannels=capture.rows(baseline,'CHANNEL')
    for ledger in(channels,oldchannels):
        need(len(ledger)==14*749 and {(int(r['frame']),int(r['channel']))for r in ledger}=={(f,n)for f in range(origin+1,origin+750)for n in range(14)}and
             all(int(r['sample'])==0xffffffff and r['paused']==r['loop']=='0'for r in ledger),'Every actual sample channel idle, no false marker/voice/loop')
        # samples_device::stop and natural completion clear the source and
        # source_num, not source_len/pos. The latter must remain unchanged
        # for each idle channel throughout this entire observed window.
        for n in range(14):
            retained={(r['length'],r['pos'])for r in ledger if int(r['channel'])==n}
            need(len(retained)==1,'Inactive channel length/position never advances or changes')
            length,pos=next(iter(retained));need(int(length)>=0 and float(pos)>=0,'Valid retained inactive channel metadata')
    without_retained=lambda ledger:[{k:v for k,v in r.items()if k not in('length','pos')}for r in ledger]
    need(without_retained(channels)==without_retained(oldchannels),'Every channel timeline, source, loop, paused and assistance field identical on/off')
    need(all(r['length']=='0'and float(r['pos'])==0 for r in oldchannels),'Disabled samples never obtain a source or retained sample position')
    writes=rows('SOUND');delivery=rows('DELIVERY')
    packets=rows('PACKET')
    need(packets and len(writes)==2*len(packets) and all(r['pc']in('FFA13C90','FFA13D60')and r['mask']=='FFFF'for r in writes),'Every actual native packet-store write; no synthetic import marker')
    need([r['pc']for r in writes]==['FFA13C90','FFA13D60']*len(packets),'Exact original high/low native packet-store ordering')
    for i,packet in enumerate(packets):
        high,low=writes[i*2:i*2+2];word=int(packet['a3'],16)
        need(0<=word<=65535 and tuple(int(w['word'],16)&255 for w in (high,low))==(word>>8,word&255) and
             float(packet['seconds'])<float(high['seconds'])<float(low['seconds']) and
             all(w['a8']==packet['a8'] and w['a13']==packet['a13'] and w['frame']==packet['frame'] for w in (high,low)),'Every actual full native dispatch packet and owner reaches both port bytes')
    actual=[]
    for i,w in enumerate(writes):
        first=float(w['seconds']);last=float(writes[i+1]['seconds'])if i+1<len(writes)else first+.1
        hits=[d for d in delivery if first<=float(d['seconds'])<last and int(d['word'],16)==int(w['word'],16)&255]
        need(hits,'Every native sound byte genuinely read by ADSP before subsequent write');actual.append(dict(write=w,dspRead=hits[0]))
    # Fixed native inflation effect calls are unchanged original
    # ROM instructions. Their command table record is independently decoded;
    # the actual high/low writes must match that original record exactly.
    scream=[r for r in rows('ROUTE') if r['entry']=='FFA11FD0']
    need(len(scream)==1 and scream[0]['id']==str(identity) and scream[0]['a8']==scream[0]['owner']==action['victim_actor'] and scream[0]['a13']==action['victim_main'] and scream[0]['return_pc']=='FF9EC0F0','Exactly one true victim owned native pain call')
    voice=[r for r in rows('ROUTE') if r['return_pc']=='FF9EC0F0' and r['a8']==action['victim_actor']]
    gender='FFA123B0' if identity==18 else 'FFA122D0'
    need([r['entry'] for r in voice]==['FFA11FD0','FFA12220',gender,'FFA123D0','FFA12530'] and all(r['id']==str(identity) and r['a8']==r['owner']==action['victim_actor'] and r['a13']==action['victim_main'] for r in voice),'Complete original pain/gender/RNG/native dispatch route, no borrowed fighter identity')
    base=0x38 if identity==18 else (0x32 if side==1 else 0x34)
    need(voice[1]['a0']=='00000002' and voice[1]['a1']=='32343638' and voice[3]['a0']=='00000002' and int(voice[3]['a1'],16)==base and int(voice[-1]['a0'],16) in (base,base+1),'Original packed pain tuple, actual native player/gender byte and RNG range')
    fixed=[]
    for command,return_pc in((0x60,'FF8CC8E0'),(0xa3,'FF9EC190'),(0xa5,'FF9EC1E0'),(0xa4,'FF9EC4D0'),(int(voice[-1]['a0'],16),'FF9EC0F0')):
        calls=[r for r in rows('ROUTE')if r['entry']=='FFA12530'and int(r['a0'],16)==command]
        owner_id=4 if command==0x60 else identity
        owner_actor=action['actor'] if command==0x60 else action['victim_actor']
        owner_main=action['main'] if command==0x60 else action['victim_main']
        need(len(calls)==1 and calls[0]['return_pc']==return_pc and calls[0]['id']==str(owner_id)and calls[0]['a8']==calls[0]['owner']==owner_actor and calls[0]['a13']==owner_main,'Original fixed native effect caller/task/character ownership')
        call=calls[0];table_at=(0xffa0ef20-0xff800000)//8+command*4
        header,baseword=struct.unpack_from('<HH',guest,table_at)
        later_queues=[q for q in rows('QUEUE')if float(q['seconds'])>=float(call['seconds'])]
        need(later_queues,'Actual original priority slot branch observed')
        queue=later_queues[0];slot={'FFA12A10':0,'FFA12A80':1,'FFA12B00':2}.get(queue['entry'])
        need(slot is not None and int(queue['a3'],16)==baseword and int(queue['a1'],16)==header>>8 and int(queue['a4'],16)==header&255 and
             queue['a8']==call['a8']and queue['a13']==call['a13']and queue['frame']==call['frame'],'Actual original priority/duration/base packet registers bound to table record and selected branch')
        word=baseword+slot;expected=(word>>8,word&255)
        packets=[p for p in rows('PACKET')if float(p['seconds'])>=float(queue['seconds'])]
        need(packets,'Actual original packed dispatcher observed');packet=packets[0]
        need(int(packet['a3'],16)==word and packet['a8']==call['a8']and packet['a13']==call['a13']and packet['frame']==call['frame'],'Actual native slot increment and complete dispatch packet independently observed')
        later=[w for w in writes if float(w['seconds'])>=float(call['seconds'])][:2]
        need(len(later)==2 and tuple(int(w['word'],16)&255 for w in later)==expected and
             float(call['seconds'])<float(queue['seconds'])<float(packet['seconds'])<float(later[0]['seconds'])and
             all(w['a8']==call['a8']and w['a13']==call['a13']and w['frame']==call['frame']for w in later),'Original native command-table and actual selected slot high/low bytes reach actual sound port')
        fixed.append(dict(command=command,tableAddress=f'{0xffa0ef20+command*32:08X}',originalHeader=f'{header:04X}',originalBasePacket=f'{baseword:04X}',
            actualPrioritySlot=slot,actualPacket=f'{word:04X}',actualQueue=queue,actualDispatch=packet,caller=return_pc,frame=int(call['frame']),actualWrites=later))
    return dict(passed=True,identity=identity,side=side,origin=origin,terminalFrame=origin+750,nativePacketBytesDelivered=len(actual),
        completeNativePCMFrames=meta['mixedPCMBytesVerifiedInRAM']//4,completeNativePCMUpdates=len(chunks),
        actualNativeFixedEffects=fixed,actualNativePainVoice=voice,allDispatchPacketsAndOwnersBound=True,fullPCMOnOffExactlyEqual=True,importedSampleChannelsIdle=True)

def run():
    need(not OUT.exists(),'Fresh immutable independent audio proof')
    observation=ROOT/'audit_v3942_kitana_native_audio_queue_observed/report.json';source=json.loads(observation.read_text());need(source['passed']and source['actualOwnedContexts']==4 and source['actualPairedCaptures']==8,'All actual primary captures terminal and full PCM checked')
    guest=capture.expected();stock=(ROOT/'mk2/mk2-maincpu.bin').read_bytes();pins={str(observation):sha(observation),str(Path(__file__).resolve()):sha(__file__)}
    operands=(0xff8cc790,0xff8ccc80,0xff9ec840,0xff9ec8b0,0xff9ecbd0)
    allowed={i for operand in operands for i in range((operand-0xff800000)//8,(operand-0xff800000)//8+4)}
    for first,last in((0xff8cc650,0xff8cdc40),(0xff9ec070,0xff9ed4c0),(0xffa0ef20,0xffa10ee0),(0xffa11fd0,0xffa122a0),(0xffa122d0,0xffa12430),(0xffa12530,0xffa13df0)):
        lo,hi=(first-0xff800000)//8,(last-0xff800000)//8
        need(all(guest[i]==stock[i] or i in allowed for i in range(lo,hi)),'Entire original native inflation/voice/effect/packet code, only five independently qualified data operands differ')
    trampoline=0xff800000+(0xfe000+2*0x20)*8
    need(struct.unpack_from('<HI',guest,(0xffa122a0-0xff800000)//8)==(0xc080,trampoline),'Actual explicit true-ID native female extension entry')
    words=(0x0b42,0xffef,0xca06,0x0b42,0xffed,0xca03,0xc080,0x22d0,0xffa1,0xc080,0x23b0,0xffa1)
    need(struct.unpack_from('<12H',guest,0xfe040)==words,'Exact native compares16/18 preserving Jade and appending Sonya, male/female original continuations')
    for p,h in source['inputHashes'].items():need(sha(p)==h,'All actual executed inputs and source/state/pair evidence unchanged');pins[p]=h
    sample_source=ROOT/'mame-mkp/src/devices/sound/samples.cpp';native=sample_source.read_text()
    stop=native[native.index('void samples_device::stop(uint8_t channel)'):native.index('void samples_device::stop_all()')]
    need('chan.source = nullptr;'in stop and 'chan.source_num = -1;'in stop and 'chan.source_len ='not in stop and 'chan.pos ='not in stop,'Actual source clears playback without resetting retained length/position')
    need('if (chan.source != nullptr && !chan.paused)'in native and 'else\n\t\t\t\tbuffer.fill(0);'in native,'Actual source emits silence when source is null, independent of retained metadata')
    need(str(sample_source)in pins,'The same actual sample-engine source was pinned before every capture')
    cases=[]
    for fighter,side in(('kano',1),('kano',2),('sonya',1),('sonya',2)):
        folder=ROOT/f'audit_v3941_kitana_{fighter}_p{side}_audio_queue_samples';base=ROOT/f'audit_v3941_kitana_{fighter}_p{side}_audio_queue_nosamples'
        text=(folder/'run.log').read_text();baseline=(base/'run.log').read_text();meta=json.loads((folder/'result.json').read_text());oldmeta=json.loads((base/'result.json').read_text())
        positive=audio_gate(text,baseline,meta,oldmeta,guest,fighter,side);faults=[]
        def reject(label,changed_text=text,changed_base=baseline,changed_meta=meta,changed_old=oldmeta):
            try:audio_gate(changed_text,changed_base,changed_meta,changed_old,guest,fighter,side)
            except (ValueError,KeyError)as error:faults.append(dict(kind=label,rejectedBy=str(error)))
            else:raise ValueError('Actual audio fault accepted '+label)
            need(audio_gate(text,baseline,meta,oldmeta,guest,fighter,side)==positive,'Exact positive restored after actual audio fault')
        def replace_actual(tag,key,new):
            line=next(s for s in text.splitlines()if s.startswith('MK2_MAUDIO_'+tag+' '));changed,count=re.subn(r'\b'+key+r'=\S+',key+'='+new,line,count=1);need(count==1 and changed!=line,'Non-vacuous actual audio row fault');return text.replace(line,changed,1),baseline.replace(line,changed,1)
        for label,tag,key,value in(('wrong_native_origin','BEGIN','a8','01000000'),('phantom_imported_voice','CHANNEL','sample','0'),('looping_voice','CHANNEL','loop','1'),('bad_native_packet_writer','SOUND','pc','FFF00000'),('wrong_sound_byte','SOUND','word','FFF7'),('wrong_native_effect_code','ROUTE','a0','00000061')):
            changed,changed_base=replace_actual(tag,key,value);reject(label,changed,changed_base)
        for label,key,value in(('idle_position_advances','pos','123.00000000'),('idle_source_length_changes','length','123')):
            changed,changed_base=replace_actual('CHANNEL',key,value);reject(label,changed,changed_base)
        for label,actual,key,value in (
            ('foreign_pain_voice_owner',positive['actualNativePainVoice'][0],'a8','01000000'),
            ('wrong_pain_gender_branch',positive['actualNativePainVoice'][2],'entry','FFA12380'),
            ('wrong_original_packed_pain_byte',positive['actualNativePainVoice'][3],'a1','00000030')):
            line=next(s for s in text.splitlines() if s.startswith('MK2_MAUDIO_ROUTE ') and dict(re.findall(r'(\w+)=([^\s]+)',s))==actual)
            damaged,n=re.subn(r'\b'+key+r'=\S+',key+'='+value,line,count=1);need(n==1 and damaged!=line,'Actual non-vacuous pain-route fault')
            reject(label,text.replace(line,damaged,1),baseline.replace(line,damaged,1))
        # These faults target the actual first fixed effect's selected branch,
        # not an unrelated earlier generic sound-dispatch entry.
        fixed=positive['actualNativeFixedEffects'][0]
        for label,tag,key,value,actual in(
            ('wrong_priority_slot','QUEUE','entry','FFA12B00',fixed['actualQueue']),
            ('wrong_table_priority','QUEUE','a1','00000000',fixed['actualQueue']),
            ('wrong_table_packet','QUEUE','a3','00000000',fixed['actualQueue']),
            ('wrong_dispatched_packet','PACKET','a3','00000000',fixed['actualDispatch'])):
            line=next(s for s in text.splitlines()if s.startswith('MK2_MAUDIO_'+tag+' ')and dict(re.findall(r'(\w+)=([^\s]+)',s))==actual)
            damaged,n=re.subn(r'\b'+key+r'=\S+',key+'='+value,line,count=1);need(n==1 and damaged!=line,'Non-vacuous actual fixed native queue fault')
            reject(label,text.replace(line,damaged,1),baseline.replace(line,damaged,1))
        w=capture.rows(text,'SOUND')[0];first=float(w['seconds']);last=float(capture.rows(text,'SOUND')[1]['seconds'])
        def remove_deliveries(value):
            return '\n'.join(s for s in value.splitlines()if not(s.startswith('MK2_MAUDIO_DELIVERY ')and first<=float(dict(re.findall(r'(\w+)=([^\s]+)',s))['seconds'])<last))+'\n'
        reject('missing_actual_ADSP_read',remove_deliveries(text),remove_deliveries(baseline))
        line=next(s for s in text.splitlines()if s.startswith('MK2_BBAUDIO_PCM_DIGEST '));changed=re.sub(r'sha256=\S+','sha256='+'0'*64,line);reject('different_native_PCM_update',text.replace(line,changed,1))
        changed=copy.deepcopy(meta);changed['mixedPCMSHA256']='0'*64;reject('phantom_whole_imported_PCM',changed_meta=changed)
        changed=copy.deepcopy(meta);changed['stockReferenceOnly']=True;reject('stock_reference_as_selected_Sonya_or_Kano',changed_meta=changed)
        cases.append(dict(fighter=fighter,side=side,nativeAudio=positive,actualRowCounterexamplesRejected=faults))
    return dict(passed=True,candidate=capture.NAME,actualContexts=4,actualRowCounterexamplesRejected=76,cases=cases,inputHashes=pins,
        inactiveChannelMetadataSourceQualified=True,activeChannelAndEveryPCMByteChecksRetained=True,
        nativeFixedEffectCommandsSourceBound=True,actualNativePainVoiceGenderAndPacketAccepted=True,actualNativeDCSBytesDelivered=sum(c['nativeAudio']['nativePacketBytesDelivered']for c in cases),fullNativePCMExactlyUnaffectedBySamples=True,
        stockReferenceWholeWaveformFidelityAccepted=False,allVictimFinisherAudioAccepted=False,fullPortAcceptance=False,scope=__doc__)

if __name__=='__main__':
    try:report=run()
    except Exception as error:report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
    need(not OUT.exists(),'Immutable report');OUT.mkdir();need(subprocess.run(['compact.exe','/C','/I','/Q','/S:'+str(OUT)],capture_output=True).returncode==0,'Inherited report compression')
    (OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items()if k not in('inputHashes','cases')},indent=2),flush=True)
    raise SystemExit(0 if report['passed']else 1)
