"""Current earned split audio: complete PCM/ports and original effect routes.

Retain the entire3952 generic PCM/channel/packet/ADSP algorithm. Only the
finisher-specific native callers and actual voice family differ. Every
observed general command, including original randomized blood effects, is
independently bound to original command-table/priority-slot/packet bytes.
No original-stock whole-waveform or all-finisher acceptance is implied.
"""
import copy,hashlib,inspect,json,re,struct,subprocess,traceback
from pathlib import Path
import run_kung_lao_native_audio_queue_v4001 as capture
import verify_kitana_native_audio_queue_v3952 as previous
ROOT,need,sha=capture.ROOT,capture.need,capture.sha
OUT=ROOT/'audit_v4005_kung_lao_native_audio_queue_checked'

def split_tail(text,meta,guest,identity,side,origin,action,actual,chunks):
    rows=lambda tag:capture.rows(text,tag)
    routes=rows('ROUTE');general=[r for r in routes if r['entry']=='FFA12530']
    need(len(general)==54,'All six native task calls and48 original blood-effect calls')
    voice=[r for r in routes if r['return_pc']=='FF8CEB30'and r['a8']==action['victim_actor']]
    gender='FFA123B0'if identity==18 else'FFA122D0';base=0xb7 if identity==18 else 0x85
    need([r['entry']for r in voice]==['FFA12220',gender,'FFA123D0','FFA12530']and
         all(r['id']==str(identity)and r['a8']==r['owner']==action['victim_actor']and r['a13']==action['victim_main']for r in voice),'Complete true victim native split voice/gender route, no proxy identity')
    need(voice[0]['a0']=='00000001'and voice[0]['a1']=='8585B8B7'and voice[2]['a0']=='00000001'and int(voice[2]['a1'],16)==base and int(voice[-1]['a0'],16)==base,'Original count-one packed split voice: same male85/femaleB7 byte in both physical slots')
    needed={'FF8C61E0':(0xd6,0,action['actor'],action['main']),
            'FF8C6370':(0x97,0,action['actor'],action['main']),
            'FF8CEB30':(base,identity,action['victim_actor'],action['victim_main']),
            'FF8CF030':(0x96,identity,action['victim_actor'],action['victim_main'])}
    fixed=[];blood=[]
    for pc,(_,_,_,_)in needed.items():need(sum(r['return_pc']==pc for r in general)==1,'One original fixed native task caller '+pc)
    for pc in('FF8CEC30','FF8CF0E0'):
        calls=[r for r in general if r['return_pc']==pc]
        need(len(calls)==1 and 0x1f<=int(calls[0]['a0'],16)<=0x22 and calls[0]['a1']=='0000001F'and
             calls[0]['id']==str(identity)and calls[0]['a8']==calls[0]['owner']==action['victim_actor']and calls[0]['a13']==action['victim_main'],'Both original native count4/base1F impact calls retain true victim owner')
    for pc,count in(('FF9B0CB0',40),('FF9AD190',8)):
        calls=[r for r in general if r['return_pc']==pc]
        need(len(calls)==count and all(0x73<=int(r['a0'],16)<=0x75 and r['a1']=='00000073'and r['id']=='0'and r['a8']==r['owner']for r in calls),'Original independently spawned blood effect count3/base73 routing; ID0 is an effect, not a fighter proxy')
    need({r['return_pc']for r in general}==set(needed)|{'FF8CEC30','FF8CF0E0','FF9B0CB0','FF9AD190'},'No unexplained general-command caller')
    queues,packets,writes=rows('QUEUE'),rows('PACKET'),rows('SOUND')
    for index,call in enumerate(general):
        pc=call['return_pc'];command=int(call['a0'],16)
        if pc in needed:
            wanted,owner_id,actor,main=needed[pc]
            need(command==wanted and call['id']==str(owner_id)and call['a8']==call['owner']==actor and call['a13']==main,'Actual original fixed split command and native task ownership')
        stop=float(general[index+1]['seconds'])if index+1<len(general)else float('inf')
        candidates=[q for q in queues if float(call['seconds'])<=float(q['seconds'])<stop and q['a8']==call['a8']and q['a13']==call['a13']]
        need(len(candidates)==1,'Every original general command actually enters exactly one native priority slot')
        q=candidates[0];slot={'FFA12A10':0,'FFA12A80':1,'FFA12B00':2}.get(q['entry'])
        header,word=struct.unpack_from('<HH',guest,(0xffa0ef20-0xff800000)//8+command*4)
        need(slot is not None and int(q['a1'],16)==header>>8 and int(q['a4'],16)==header&255 and int(q['a3'],16)==word and q['frame']==call['frame'],'Whole original command-table priority/duration/base packet and actual native branch')
        candidates=[p for p in packets if float(q['seconds'])<float(p['seconds'])<stop and p['a8']==call['a8']and p['a13']==call['a13']]
        need(len(candidates)==1,'One complete actual native packed dispatch per original command');packet=candidates[0]
        need(int(packet['a3'],16)==word+slot and packet['frame']==call['frame'],'Original selected-slot increment and exact actual dispatch packet')
        pair=[w for w in writes if float(packet['seconds'])<float(w['seconds'])<stop and w['a8']==call['a8']and w['a13']==call['a13']][:2]
        need(len(pair)==2 and tuple(int(w['word'],16)&255 for w in pair)==((word+slot)>>8,(word+slot)&255)and all(w['frame']==call['frame']for w in pair),'Every independently decoded general command reaches both native sound-port bytes')
        record=dict(command=command,caller=pc,frame=int(call['frame']),originalHeader=f'{header:04X}',originalBasePacket=f'{word:04X}',actualPrioritySlot=slot,actualPacket=f'{word+slot:04X}',actualQueue=q,actualDispatch=packet,actualWrites=pair)
        (blood if pc in('FF9B0CB0','FF9AD190')else fixed).append(record)
    return dict(passed=True,identity=identity,side=side,origin=origin,terminalFrame=origin+750,nativePacketBytesDelivered=len(actual),completeNativePCMFrames=meta['mixedPCMBytesVerifiedInRAM']//4,completeNativePCMUpdates=len(chunks),actualNativeFixedEffects=fixed,actualOriginalBloodEffects=blood,actualNativeSplitVoice=voice,allDispatchPacketsAndOwnersBound=True,allGeneralCommandsSourceBound=True,fullPCMOnOffExactlyEqual=True,importedSampleChannelsIdle=True)

def make_gate():
    source=inspect.getsource(previous.audio_gate)
    marker='    # Fixed native inflation effect calls are unchanged original\n'
    need(source.count(marker)==1,'One declared finisher-specific boundary; complete generic algorithm retained')
    source=source[:source.index(marker)]
    replacements={
        'physical=capture.state.gate(capture.state.rows(text),fighter,side,guest)':"physical=capture.state.gate(capture.state.rows(text),fighter,side,guest,(ROOT/capture.NAME/'roms/mk2ks/mk2ks.mdata').read_bytes())",
        "begin[0]['id']=='4'":"begin[0]['id']=='0'",
        'Original Kitana task, not added-character proxy action':'Original Kung Lao task, not added-character proxy action'}
    for old,new in replacements.items():need(source.count(old)==1,'Exactly one declared split-specific adaptation');source=source.replace(old,new)
    source+='    return split_tail(text,meta,guest,identity,side,origin,action,actual,chunks)\n'
    namespace=dict(capture=capture,ROOT=ROOT,need=need,hashlib=hashlib,tagged=previous.tagged,split_tail=split_tail)
    exec(compile(source,'<retained3952_generic_audio_with_split_tail>','exec'),namespace)
    return namespace['audio_gate']

audio_gate=make_gate()

def run():
    need(not OUT.exists(),'Fresh immutable original native audio proof')
    observed=ROOT/'audit_v4003_kung_lao_native_audio_queue_observed/report.json';value=json.loads(observed.read_text())
    need(value['passed']and value['actualOwnedContexts']==4 and value['actualPairedCaptures']==8,'All eight actual terminal primary sound captures')
    guest=capture.expected();stock=(ROOT/'mk2/mk2-maincpu.bin').read_bytes();pins={str(observed):sha(observed),str(Path(__file__).resolve()):sha(__file__),str(Path(previous.__file__).resolve()):sha(previous.__file__)}
    allowed=set(range((0xff8cea70-0xff800000)//8,(0xff8cea70-0xff800000)//8+4))
    for first,last in((0xff8c6040,0xff8c6700),(0xff8ce9f0,0xff8cf110),(0xff8ea3f0,0xff8ea480),(0xff9b0940,0xff9b09a0),(0xff9ad140,0xff9ad1b0),(0xffa0ef20,0xffa10ee0),(0xffa11e60,0xffa122a0),(0xffa122d0,0xffa12430),(0xffa12530,0xffa13df0)):
        lo,hi=(first-0xff800000)//8,(last-0xff800000)//8
        need(all(guest[i]==stock[i]or i in allowed for i in range(lo,hi)),'Whole original native split/impact/blood/voice/table/packet code; only declared own victim-table operand differs')
    trampoline=0xff800000+(0xfe000+2*0x20)*8
    need(struct.unpack_from('<HI',guest,(0xffa122a0-0xff800000)//8)==(0xc080,trampoline)and struct.unpack_from('<12H',guest,0xfe040)==(0x0b42,0xffef,0xca06,0x0b42,0xffed,0xca03,0xc080,0x22d0,0xffa1,0xc080,0x23b0,0xffa1),'Exact native true-ID female extension compares16/18 and continues original male/female routes')
    for p,h in value['inputHashes'].items():need(sha(p)==h,'All actual executed input/capture bytes unchanged');pins[p]=h
    sample_source=ROOT/'mame-mkp/src/devices/sound/samples.cpp';native=sample_source.read_text();stop=native[native.index('void samples_device::stop(uint8_t channel)'):native.index('void samples_device::stop_all()')]
    need('chan.source = nullptr;'in stop and 'chan.source_num = -1;'in stop and 'chan.source_len ='not in stop and 'chan.pos ='not in stop and 'if (chan.source != nullptr && !chan.paused)'in native and 'else\n\t\t\t\tbuffer.fill(0);'in native and str(sample_source)in pins,'Executed sample-engine source: retained inactive metadata emits silence and never advances')
    cases=[]
    for fighter,side in(('kano',1),('kano',2),('sonya',1),('sonya',2)):
        folder=ROOT/f'audit_v4002_kung_lao_{fighter}_p{side}_audio_queue_samples';base=ROOT/f'audit_v4002_kung_lao_{fighter}_p{side}_audio_queue_nosamples'
        text=(folder/'run.log').read_text();baseline=(base/'run.log').read_text();meta=json.loads((folder/'result.json').read_text());oldmeta=json.loads((base/'result.json').read_text())
        positive=audio_gate(text,baseline,meta,oldmeta,guest,fighter,side);faults=[]
        def reject(label,t=text,b=baseline,m=meta,o=oldmeta):
            try:audio_gate(t,b,m,o,guest,fighter,side)
            except (ValueError,KeyError)as error:faults.append(dict(kind=label,rejectedBy=str(error)))
            else:raise ValueError('Actual native audio fault accepted '+label)
            need(audio_gate(text,baseline,meta,oldmeta,guest,fighter,side)==positive,'Actual positive restored after each fault')
        def mutate(tag,key,new,actual=None):
            line=next(s for s in text.splitlines()if s.startswith('MK2_MAUDIO_'+tag+' ')and(actual is None or dict(re.findall(r'(\w+)=([^\s]+)',s))==actual))
            changed,n=re.subn(r'\b'+key+r'=\S+',key+'='+new,line,count=1);need(n==1 and changed!=line,'Non-vacuous actual row corruption')
            return text.replace(line,changed,1),baseline.replace(line,changed,1)
        for label,tag,key,new in(('wrong_native_origin','BEGIN','a8','01000000'),('phantom_imported_voice','CHANNEL','sample','0'),('looping_voice','CHANNEL','loop','1'),('bad_native_packet_writer','SOUND','pc','FFF00000'),('wrong_native_byte','SOUND','word','FFF7'),('wrong_original_effect_code','ROUTE','a0','00000061'),('idle_position_advances','CHANNEL','pos','123.00000000'),('idle_source_length_changes','CHANNEL','length','123')):
            t,b=mutate(tag,key,new);reject(label,t,b)
        for label,actual,key,new in(('foreign_voice_owner',positive['actualNativeSplitVoice'][0],'a8','01000000'),('wrong_native_gender',positive['actualNativeSplitVoice'][1],'entry','FFA12380'),('wrong_packed_voice_byte',positive['actualNativeSplitVoice'][2],'a1','00000030')):
            t,b=mutate('ROUTE',key,new,actual);reject(label,t,b)
        fixed=positive['actualNativeFixedEffects'][0];blood=positive['actualOriginalBloodEffects'][0]
        for label,tag,key,new,actual in(('wrong_priority_slot','QUEUE','entry','FFA12B00',fixed['actualQueue']),('wrong_table_priority','QUEUE','a1','00000000',fixed['actualQueue']),('wrong_table_packet','QUEUE','a3','00000000',fixed['actualQueue']),('wrong_dispatch_packet','PACKET','a3','00000000',fixed['actualDispatch']),('wrong_blood_source_packet','QUEUE','a3','00000000',blood['actualQueue'])):
            t,b=mutate(tag,key,new,actual);reject(label,t,b)
        first=float(capture.rows(text,'SOUND')[0]['seconds']);last=float(capture.rows(text,'SOUND')[1]['seconds'])
        def remove_reads(s):return '\n'.join(l for l in s.splitlines()if not(l.startswith('MK2_MAUDIO_DELIVERY ')and first<=float(dict(re.findall(r'(\w+)=([^\s]+)',l))['seconds'])<last))+'\n'
        reject('missing_actual_ADSP_read',remove_reads(text),remove_reads(baseline))
        line=next(l for l in text.splitlines()if l.startswith('MK2_BBAUDIO_PCM_DIGEST '));changed=re.sub(r'sha256=\S+','sha256='+'0'*64,line);reject('different_native_PCM_update',text.replace(line,changed,1))
        m=copy.deepcopy(meta);m['mixedPCMSHA256']='0'*64;reject('phantom_whole_imported_PCM',m=m)
        m=copy.deepcopy(meta);m['stockReferenceOnly']=True;reject('reference_as_added_character',m=m)
        cases.append(dict(fighter=fighter,side=side,nativeAudio=positive,actualRowCounterexamplesRejected=faults))
    return dict(passed=True,candidate=capture.NAME,actualContexts=4,actualRowCounterexamplesRejected=sum(len(c['actualRowCounterexamplesRejected'])for c in cases),cases=cases,inputHashes=pins,fullNativePCMExactlyUnaffectedBySamples=True,actualNativeSplitVoiceGenderAndPacketAccepted=True,allObservedGeneralCommandsSourceBound=True,actualNativeGeneralCommands=sum(len(c['nativeAudio']['actualNativeFixedEffects'])+len(c['nativeAudio']['actualOriginalBloodEffects'])for c in cases),actualNativeDCSBytesDelivered=sum(c['nativeAudio']['nativePacketBytesDelivered']for c in cases),stockReferenceWholeWaveformFidelityAccepted=False,allVictimFinisherAudioAccepted=False,fullPortAcceptance=False,scope=__doc__)

if __name__=='__main__':
    try:report=run()
    except Exception as error:report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
    need(not OUT.exists(),'Immutable report');OUT.mkdir();need(subprocess.run(['compact.exe','/C','/I','/Q','/S:'+str(OUT)],capture_output=True).returncode==0,'Report compressed before writes')
    (OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items()if k not in('inputHashes','cases')},indent=2),flush=True)
    raise SystemExit(0 if report['passed']else 1)
