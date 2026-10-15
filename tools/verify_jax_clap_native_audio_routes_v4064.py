"""Original Jax clap selectors, victim gender, effects, PCM and DCS delivery.

Entire3952 generic PCM/channel/packet/ADSP gate and original1036 earned-state
algorithm retained. Both general and Jax-specific dispatch tables decoded
from actual independently reconstructed guest. No full stock waveform or
all-finisher/audio/arena acceptance is implied by these four contexts.
"""
import copy,hashlib,inspect,json,re,struct,subprocess,traceback
from pathlib import Path
import run_jax_clap_native_audio_routes_v4059 as capture
import verify_kitana_native_audio_queue_v3952 as previous
ROOT,need,sha=capture.ROOT,capture.need,capture.sha
OUT=ROOT/'audit_v4065_jax_clap_native_audio_routes_checked'

def tail(text,meta,guest,identity,side,origin,action,actual,chunks):
    rows=lambda tag:capture.rows(text,tag)
    routes=rows('ROUTE');general=[r for r in routes if r['entry']=='FFA12530']
    special=[r for r in routes if r['entry']=='FFA12430']
    need(len(general)==24 and len(special)==8,'All24 general native calls, Jax selector and seven genuine post-win selectors')
    voice=[r for r in routes if r['return_pc']=='FF8C7D50']
    gender='FFA123B0'if identity==18 else'FFA122D0'
    base=0x48 if identity==18 else(0x45 if side==1 else 0x46)
    need([r['entry']for r in voice]==['FFA12070','FFA12220',gender,'FFA123D0','FFA12530']and
         all(r['id']==str(identity)and r['a8']==r['owner']==action['victim_actor']and r['a13']==action['victim_main']for r in voice),'Complete original true victim death-voice/player/gender route, no proxy')
    need(voice[1]['a0']=='00000001'and voice[1]['a1']=='45464748'and voice[3]['a0']=='00000001'and
         int(voice[3]['a1'],16)==base and int(voice[-1]['a0'],16)==base,'Count-one original packed death voice45/46/48 selected by true player and gender')
    winner=special[0]
    need(winner['return_pc']=='FF8C79F0'and winner['id']=='11'and winner['a0']=='00000001'and
         winner['a8']==winner['owner']==action['actor']and winner['a13']==action['main'],'Original Jax special selector1 and genuine winner task')
    postwin={'FFFB70D0':0x11,'FF82A010':5,'FF8213C0':0x28,'FF821830':0x16,'FF9AC870':0x29,'FF82C810':0,'FF82C8F0':1}
    need([r['return_pc']for r in special[1:]]==list(postwin)and all(int(r['a0'],16)==postwin[r['return_pc']]and r['id']=='-1'and
         int(r['frame'])>origin+188 for r in special[1:]),'Seven actual original announcer/win-page selectors after original completion; non-fighter tasks not relabelled as actors')
    counts={'FF9B0CB0':5,'FF9AA7E0':8,'FF9AD190':8}
    for pc,count in counts.items():
        calls=[r for r in general if r['return_pc']==pc]
        need(len(calls)==count and all(0x73<=int(r['a0'],16)<=0x75 and r['a1']=='00000073'and r['id']=='0'and
             r['a8']==r['owner']for r in calls),'Original independently spawned blood count3/base73; effect ID0 is not a fighter proxy '+pc)
    for pc in('FF8C7EA0','FF8C7FD0'):
        calls=[r for r in general if r['return_pc']==pc]
        need(len(calls)==1 and 0x1f<=int(calls[0]['a0'],16)<=0x22 and calls[0]['a1']=='0000001F'and
             calls[0]['id']==str(identity)and calls[0]['a8']==calls[0]['owner']==action['victim_actor']and calls[0]['a13']==action['victim_main'],'Original count4/base1F impact remains in true victim task '+pc)
    need({r['return_pc']for r in general}==set(counts)|{'FF8C7D50','FF8C7EA0','FF8C7FD0'},'No unexplained general sound caller')
    queues,packets,writes=rows('QUEUE'),rows('PACKET'),rows('SOUND')
    commands=sorted(general+special,key=lambda r:float(r['seconds']))
    records=[]
    for index,call in enumerate(commands):
        stop=float(commands[index+1]['seconds'])if index+1<len(commands)else float('inf')
        command=int(call['a0'],16);direct=call['entry']=='FFA12430'
        table=0xffa10ee0 if direct else 0xffa0ef20
        header,word=struct.unpack_from('<HH',guest,(table-0xff800000)//8+command*4)
        hits=[q for q in queues if float(call['seconds'])<=float(q['seconds'])<stop and q['a8']==call['a8']and q['a13']==call['a13']]
        need(len(hits)==1,'One actual priority slot for each of32 independently decoded original commands')
        q=hits[0];slot={'FFA12A10':0,'FFA12A80':1,'FFA12B00':2}.get(q['entry'])
        need(slot is not None and int(q['a1'],16)==header>>8 and int(q['a4'],16)==header&255 and
             int(q['a3'],16)==word and q['frame']==call['frame'],'Actual table priority/duration/base packet and original native branch')
        hits=[p for p in packets if float(q['seconds'])<float(p['seconds'])<stop and p['a8']==call['a8']and p['a13']==call['a13']]
        need(len(hits)==1,'One complete native dispatch for each actual selector call');packet=hits[0]
        need(int(packet['a3'],16)==word+slot and packet['frame']==call['frame'],'Original slot increment and packet independently bound')
        pair=[w for w in writes if float(packet['seconds'])<float(w['seconds'])<stop and w['a8']==call['a8']and w['a13']==call['a13']][:2]
        need(len(pair)==2 and tuple(int(w['word'],16)&255 for w in pair)==((word+slot)>>8,(word+slot)&255)and
             all(w['frame']==call['frame']for w in pair),'Every decoded original table command reaches both actual sound-port bytes')
        records.append(dict(command=command,caller=call['return_pc'],selector=call['entry'],frame=int(call['frame']),originalTable=f'{table:08X}',
            originalHeader=f'{header:04X}',originalBasePacket=f'{word:04X}',actualPrioritySlot=slot,actualPacket=f'{word+slot:04X}',actualCall=call,actualQueue=q,actualDispatch=packet,actualWrites=pair))
    return dict(passed=True,identity=identity,side=side,origin=origin,terminalFrame=origin+750,nativePacketBytesDelivered=len(actual),
        completeNativePCMFrames=meta['mixedPCMBytesVerifiedInRAM']//4,completeNativePCMUpdates=len(chunks),actualCommands=records,actualNativeDeathVoice=voice,
        allObservedSelectorCommandsSourceBound=True,allDispatchPacketsAndOwnersBound=True,fullPCMOnOffExactlyEqual=True,importedSampleChannelsIdle=True)

def make_gate():
    source=inspect.getsource(previous.audio_gate)
    marker='    # Fixed native inflation effect calls are unchanged original\n'
    need(source.count(marker)==1,'One finisher-specific boundary, entire generic algorithm retained');source=source[:source.index(marker)]
    changes={
        'physical=capture.state.gate(capture.state.rows(text),fighter,side,guest)':'physical=capture.state.gate(text,fighter,side,guest)',
        "begin[0]['id']=='4'":"begin[0]['id']=='11'",
        'Original Kitana task, not added-character proxy action':'Original Jax task, not added-character proxy action',
    }
    for before,after in changes.items():
        need(source.count(before)==1,'Unique declared Jax physical provenance adaptation');source=source.replace(before,after)
    source+='    return tail(text,meta,guest,identity,side,origin,action,actual,chunks)\n'
    ns=dict(capture=capture,ROOT=ROOT,need=need,hashlib=hashlib,tagged=previous.tagged,tail=tail)
    exec(compile(source,__file__+'::complete3952_generic_audio','exec'),ns)
    return ns['audio_gate']

audio_gate=make_gate()

def source_contract(guest):
    capture.state.source_boundary();capture.state.scene_state.source_contract(guest)
    stock=(ROOT/'mk2/mk2-maincpu.bin').read_bytes()
    # All six stock win/continuation selectors are literal MOVI/CALLA pairs.
    # The name trampoline preserves the actual Jax selector11, not a proxy.
    for pc,command in((0xff82a010,5),(0xff8213c0,0x28),(0xff821830,0x16),(0xff9ac870,0x29),(0xff82c810,0),(0xff82c8f0,1),(0xfffb70d0,0x11)):
        at=(pc-80-0xff800000)//8
        wanted=struct.pack('<5H',0x09c0,command,0x0d5f,0x2430,0xffa1)
        need(guest[at:at+10]==wanted,'Exact literal original/Jax-name selector and native call '+hex(pc))
        if pc!=0xfffb70d0:need(stock[at:at+10]==wanted,'Original stock post-win selector bytes unchanged')
    operand=(0xff8c7b50-0xff800000)//8;allowed=set(range(operand,operand+4))
    for first,last in((0xff8c7820,0xff8c8100),(0xff8ea3f0,0xff8ea480),(0xff9aa730,0xff9aa810),(0xff9ad140,0xff9ad1b0),
                       (0xff9b0940,0xff9b09a0),(0xff9b0c70,0xff9b0cb0),(0xffa0ef20,0xffa11a40),(0xffa11e60,0xffa122a0),
                       (0xffa122d0,0xffa12430),(0xffa12430,0xffa13df0)):
        lo,hi=(first-0xff800000)//8,(last-0xff800000)//8
        need(all(guest[i]==stock[i]or i in allowed for i in range(lo,hi)),'Entire original Jax/impact/blood/player-gender/dual-table/packet code; only own position operand differs')
    trampoline=0xff800000+(0xfe000+2*0x20)*8
    need(struct.unpack_from('<HI',guest,(0xffa122a0-0xff800000)//8)==(0xc080,trampoline)and
         struct.unpack_from('<12H',guest,0xfe040)==(0x0b42,0xffef,0xca06,0x0b42,0xffed,0xca03,0xc080,0x22d0,0xffa1,0xc080,0x23b0,0xffa1),'Exact true-ID female extension preserving Jade and appending18, original male/female continuations')
    native=(ROOT/'mame-mkp/src/devices/sound/samples.cpp').read_text()
    stop=native[native.index('void samples_device::stop(uint8_t channel)'):native.index('void samples_device::stop_all()')]
    need('chan.source = nullptr;'in stop and 'chan.source_num = -1;'in stop and 'chan.source_len ='not in stop and 'chan.pos ='not in stop and
         'if (chan.source != nullptr && !chan.paused)'in native and 'else\n\t\t\t\tbuffer.fill(0);'in native,'Pinned actual inactive sample source emits silence without changing retained position/length')

def run():
    need(not OUT.exists(),'Fresh immutable native audio proof')
    observed=capture.OUT/'report.json';value=json.loads(observed.read_text())
    need(value['passed']and value['actualOwnedContexts']==4 and value['actualPairedCaptures']==8,'All eight actual terminal full audio route captures')
    guest=capture.expected();source_contract(guest)
    pins={str(observed):sha(observed),str(Path(__file__).resolve()):sha(__file__),str(Path(previous.__file__).resolve()):sha(previous.__file__)}
    for p,h in value['inputHashes'].items():need(sha(p)==h,'All actual executed input/capture bytes unchanged');pins[p]=h
    cases=[]
    for fighter,side in(('kano',1),('kano',2),('sonya',1),('sonya',2)):
        folder=ROOT/f'audit_v4060_jax_clap_{fighter}_p{side}_audio_queue_samples';base=ROOT/f'audit_v4060_jax_clap_{fighter}_p{side}_audio_queue_nosamples'
        text=(folder/'run.log').read_text();baseline=(base/'run.log').read_text();meta=json.loads((folder/'result.json').read_text());oldmeta=json.loads((base/'result.json').read_text())
        positive=audio_gate(text,baseline,meta,oldmeta,guest,fighter,side);faults=[]
        def reject(label,t=text,b=baseline,m=meta,o=oldmeta):
            try:audio_gate(t,b,m,o,guest,fighter,side)
            except (ValueError,KeyError)as error:faults.append(dict(kind=label,rejectedBy=str(error)))
            else:raise ValueError('Actual native Jax audio fault accepted '+label)
            need(audio_gate(text,baseline,meta,oldmeta,guest,fighter,side)==positive,'Original positive restored after every actual fault')
        def mutate(tag,key,new,actual=None,prefix='MK2_MAUDIO_'):
            line=next(s for s in text.splitlines()if s.startswith(prefix+tag+' ')and(actual is None or dict(re.findall(r'(\w+)=([^\s]+)',s))==actual))
            changed,n=re.subn(r'\b'+key+r'=\S+',key+'='+new,line,count=1);need(n==1 and changed!=line,'Actual non-vacuous row corruption')
            return text.replace(line,changed,1),baseline.replace(line,changed,1)
        for label,tag,key,new in(('wrong_native_origin','BEGIN','a8','01000000'),('phantom_imported_voice','CHANNEL','sample','0'),('looping_voice','CHANNEL','loop','1'),
                               ('bad_native_packet_writer','SOUND','pc','FFF00000'),('wrong_native_byte','SOUND','word','FFF7'),('wrong_original_effect','ROUTE','a0','00000061'),
                               ('idle_position_advances','CHANNEL','pos','123.00000000'),('idle_length_changes','CHANNEL','length','123')):
            t,b=mutate(tag,key,new);reject(label,t,b)
        for label,actual,key,new in(('foreign_death_voice_owner',positive['actualNativeDeathVoice'][0],'a8','01000000'),
                                   ('wrong_native_gender',positive['actualNativeDeathVoice'][2],'entry','FFA12380'),
                                   ('wrong_packed_death_byte',positive['actualNativeDeathVoice'][3],'a1','00000030')):
            t,b=mutate('ROUTE',key,new,actual);reject(label,t,b)
        fixed=positive['actualCommands'][0];blood=next(c for c in positive['actualCommands']if c['caller']=='FF9AA7E0')
        for label,tag,key,new,actual in(('wrong_jax_special_selector','ROUTE','a0','00000002',fixed['actualCall']),
                                      ('borrowed_jax_actor','ROUTE','id','1',fixed['actualCall']),
                                      ('wrong_priority_slot','QUEUE','entry','FFA12B00',fixed['actualQueue']),
                                      ('wrong_table_priority','QUEUE','a1','00000000',fixed['actualQueue']),
                                      ('wrong_table_packet','QUEUE','a3','00000000',fixed['actualQueue']),
                                      ('wrong_dispatch_packet','PACKET','a3','00000000',fixed['actualDispatch']),
                                      ('wrong_blood_packet','QUEUE','a3','00000000',blood['actualQueue'])):
            t,b=mutate(tag,key,new,actual);reject(label,t,b)
        first=float(capture.rows(text,'SOUND')[0]['seconds']);last=float(capture.rows(text,'SOUND')[1]['seconds'])
        def remove_reads(s):return '\n'.join(l for l in s.splitlines()if not(l.startswith('MK2_MAUDIO_DELIVERY ')and first<=float(dict(re.findall(r'(\w+)=([^\s]+)',l))['seconds'])<last))+'\n'
        reject('missing_actual_ADSP_read',remove_reads(text),remove_reads(baseline))
        line=next(l for l in text.splitlines()if l.startswith('MK2_BBAUDIO_PCM_DIGEST '));changed=re.sub(r'sha256=\S+','sha256='+'0'*64,line);reject('different_native_PCM_update',text.replace(line,changed,1))
        m=copy.deepcopy(meta);m['mixedPCMSHA256']='0'*64;reject('phantom_whole_imported_PCM',m=m)
        m=copy.deepcopy(meta);m['stockReferenceOnly']=True;reject('reference_as_added_character',m=m)
        for tag,key,new in(('FIRST_LIVE','ids','11,1'),('ACTION','address','FF8C6040'),('ACTION','damage','321'),('WRAP','age','187'),
                            ('WRAP','pc','FFF00000'),('RESULT','wins','3'),('APPROACH','gap','100'),('HEALTH','pc','FFF00000')):
            t,b=mutate(tag,key,new,prefix='MK2_STOCK_HEAD_V921_');reject('original_earned_state_'+tag+'_'+key,t,b)
        cases.append(dict(fighter=fighter,side=side,nativeAudio=positive,actualRowCounterexamplesRejected=faults))
        print(f'{fighter}P{side}: dual table32 commands,70 actual bytes, {len(faults)} actual faults rejected',flush=True)
    return dict(passed=True,candidate=capture.NAME,actualContexts=4,actualRowCounterexamplesRejected=sum(len(c['actualRowCounterexamplesRejected'])for c in cases),
        originalCompleteEarnedStateAlgorithmRetained=True,completeGenericNativePCMPacketADSPAlgorithmRetained=True,cases=cases,inputHashes=pins,
        fullNativePCMExactlyUnaffectedBySamples=True,actualNativeDeathVoiceGenderPlayerAndPacketAccepted=True,allObservedSelectorCommandsSourceBound=True,
        actualOriginalSelectorCommands=sum(len(c['nativeAudio']['actualCommands'])for c in cases),actualNativeDCSBytesDelivered=sum(c['nativeAudio']['nativePacketBytesDelivered']for c in cases),
        stockReferenceWholeWaveformFidelityAccepted=False,allVictimFinisherAudioAccepted=False,fullPortAcceptance=False,scope=__doc__)

if __name__=='__main__':
    try:report=run()
    except Exception as error:report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
    need(not OUT.exists(),'Immutable report');OUT.mkdir();need(subprocess.run(['compact.exe','/C','/I','/Q','/S:'+str(OUT)],capture_output=True).returncode==0,'Report compressed before writes')
    (OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items()if k not in('inputHashes','cases')},indent=2),flush=True)
    raise SystemExit(0 if report['passed']else 1)
