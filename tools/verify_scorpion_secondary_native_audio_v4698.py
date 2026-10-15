"""Four actual secondary-fatality voice/effect/table/packet/PCM contexts.

Whole original generic channel/PCM/owned packet/DSP gates retained. True17/18
pain and death routes, original literal effects and every actual selector are
source-bound. Four directly dispatched packets still lack caller witnesses;
independent stock whole-waveform/all-finisher/full-port fidelity stays open.
"""
import copy,hashlib,inspect,json,re,struct,subprocess,traceback
from pathlib import Path
import verify_kitana_native_audio_queue_v3952 as original
import run_scorpion_secondary_audio_ram_v4664 as current
ROOT,need,sha=current.ROOT,current.need,current.sha
OUT=ROOT/'audit_v4699_scorpion_secondary_native_audio_checked'
CASES=[]

def stock_rows(text):
    rows=[]
    for line in text.splitlines():
        prefix='MK2_STOCK_HEAD_V921_'
        if line.startswith(prefix):rows.append(dict(tag=line.split(' ',1)[0][len(prefix):],**dict(re.findall(r'(\w+)=([^\s]+)',line))))
    return rows

def tail(text,baseline,meta,oldmeta,guest,fighter,side,physical,action,origin,actual,chunks):
    rows=lambda tag:current.previous.rows(text,tag)
    ref=(ROOT/f'audit_v4552_scorpion_secondary_{fighter}_p{side}_native_state_ram/run.log').read_text()
    need(current.old.selected(text)==current.old.selected(baseline)==current.old.selected(ref),
         'Every original cold earned/state/guest/62RGB event exactly retained, even if both audio logs are damaged identically')
    need(meta['stateGuestSHA256']==meta['guestSHA256']==oldmeta['stateGuestSHA256'],
         'Both independent whole initialized guest witnesses match actual paired streams')
    identity=physical['identity'];routes=rows('ROUTE');pain=[];death=[]
    for caller,entry,count,packed,base,age in(
      ('FF8BC890','FFA11FD0',2,'32343638',0x38 if identity==18 else(0x32 if side==1 else 0x34),27+side),
      ('FF8BCB00','FFA12070',1,'45464748',0x48 if identity==18 else(0x45 if side==1 else 0x46),71+side)):
        voice=[r for r in routes if r['return_pc']==caller]
        gender='FFA123B0'if identity==18 else'FFA122D0'
        need([r['entry']for r in voice]==[entry,'FFA12220',gender,'FFA123D0','FFA12530']and
             all(r['id']==str(identity)and r['a8']==r['owner']==action['victim_actor']and
                 r['a13']==action['victim_main']and int(r['frame'])==origin+age for r in voice),
             'Entire actual native voice/gender chronology belongs to true physical victim '+caller)
        need(voice[1]['a0']==voice[3]['a0']==f'{count:08X}'and voice[1]['a1']==packed and
             int(voice[3]['a1'],16)==base and base<=int(voice[-1]['a0'],16)<base+count,
             'Original packed native player/gender byte and legitimate RNG range '+caller)
        if caller=='FF8BC890':pain=voice
        else:death=voice
    general=[r for r in routes if r['entry']=='FFA12530'];special=[r for r in routes if r['entry']=='FFA12430']
    callers={'FF8BC860':1,'FF8BC890':1,'FF9A6F60':1,'FF9A72C0':1,'FF8BCA80':1,
             'FF8BCAD0':1,'FF8BCB00':1,'FF8BD010':1,'FF9ADC00':1,'FF9AD190':8}
    need(len(general)==17 and {pc:sum(r['return_pc']==pc for r in general)for pc in callers}==callers,
         'All17 actual original general effect/voice/spawn callers, no unexplained selector')
    for caller,command in(('FF8BC860',0x44),('FF8BCA80',0x44),('FF8BCAD0',0x56)):
        call=next(r for r in general if r['return_pc']==caller)
        need(int(call['a0'],16)==command and call['id']==str(identity)and call['a8']==call['owner']==action['victim_actor']and
             call['a13']==action['victim_main'],'Original fixed secondary effect and true physical victim owner '+caller)
    for caller in('FF9A6F60','FF9A72C0','FF9ADC00'):
        call=next(r for r in general if r['return_pc']==caller)
        need(call['a0']=='000000C4'and call['a8']==call['owner']and call['id']==(str(identity)if caller=='FF9A6F60'else'0'),
             'Native bleed/spawn effect ID0 is not a fighter proxy '+caller)
        if caller=='FF9A6F60':need(call['a8']==action['victim_actor'],'Original attached victim bleed owner')
    split=next(r for r in general if r['return_pc']=='FF8BD010')
    need(split['a1']=='0000001F'and 0x1f<=int(split['a0'],16)<=0x21 and split['id']==str(identity)and
         split['a8']==split['owner']==action['victim_actor']and split['a13']==action['victim_main'],
         'Original count3/base1F secondary effect RNG route, true victim task')
    blood=[r for r in general if r['return_pc']=='FF9AD190']
    need(all(r['a1']=='00000073'and 0x73<=int(r['a0'],16)<=0x75 and r['id']=='0'and r['a8']==r['owner']for r in blood),
         'All eight real blood-effect constructors retain original count3/base73 and actual effect owners')
    post={'FFFB70D0':0x10,'FF82A010':5,'FF8213C0':0x28,'FF821830':0x16,'FF9AC870':0x29,'FF82C810':0,'FF82C8F0':1}
    need([r['return_pc']for r in special]==list(post)and all(int(r['a0'],16)==post[r['return_pc']]and r['id']=='-1'for r in special),
         'Every original Scorpion10 winner/announcer/continue selector, no Jax or proxy name')
    commands=sorted(general+special,key=lambda r:float(r['seconds']));queues=rows('QUEUE');packets=rows('PACKET');bound=[]
    need(len(commands)==len(queues)==24,'All24 actual selectors admitted; no unobserved decline substituted')
    for index,call in enumerate(commands):
        stop=float(commands[index+1]['seconds'])if index+1<len(commands)else float('inf')
        table=0xffa0ef20 if call['entry']=='FFA12530'else 0xffa10ee0
        header,word=struct.unpack_from('<HH',guest,(table-0xff800000)//8+int(call['a0'],16)*4)
        q=[r for r in queues if float(call['seconds'])<=float(r['seconds'])<stop and r['a8']==call['a8']and r['a13']==call['a13']]
        need(len(q)==1,'Exactly one actual table admission per selector');q=q[0]
        slot={'FFA12A10':0,'FFA12A80':1,'FFA12B00':2}.get(q['entry'])
        need(slot is not None and q['frame']==call['frame']and int(q['a1'],16)==header>>8 and
             int(q['a4'],16)==header&255 and int(q['a3'],16)==word,'Original priority/duration/base word and genuine native selected slot')
        p=[r for r in packets if float(q['seconds'])<float(r['seconds'])<stop and r['a8']==call['a8']and r['a13']==call['a13']]
        need(len(p)==1 and p[0]['frame']==call['frame']and int(p[0]['a3'],16)==word+slot,
             'Every original native admitted selector reaches exact owned packet with selected-slot increment')
        bound.append(dict(call=call,queue=q,packet=p[0],originalTable=f'{table:08X}',header=f'{header:04X}',word=f'{word:04X}',slot=slot))
    extra=[p for p in packets if p not in [x['packet']for x in bound]]
    need(len(extra)==4 and [p['a3']for p in extra]==['00000000','00000034','00000035','00000038'],
         'Exactly four actual direct native packets, not relabelled as source-qualified selector callers')
    need(all(int(c['bytes'])==3840 for c in chunks)and
         all(abs(float(b['seconds'])-float(a['seconds'])-.02)<1e-9 for a,b in zip(chunks,chunks[1:])),
         'Every actual50Hz complete stereo sound update retained')
    need(0<=float(chunks[0]['seconds'])-float(rows('BEGIN')[0]['seconds'])<.020000001 and
         int(chunks[-1]['frame'])in(origin+748,origin+749),'Complete actual native750-field sound observation, separate later physical teardown')
    return dict(passed=True,identity=identity,side=side,origin=origin,sourceQualifiedPainVoice=pain,sourceQualifiedDeathVoice=death,
                actualSourceBoundSelectors=bound,actualNativeDCSBytesDelivered=len(actual),actualPCMUpdates=len(chunks),
                fullMixedPCMOnOffExactlyEqual=True,trueVictimNativeGenderVoiceAccepted=True,
                actualDirectNativePackets=extra,directPacketCallerOriginsAccepted=False,stockWholeWaveformReferenceAccepted=False,
                allFinisherVictimAudioAccepted=False,fullPortAcceptance=False)

def make_gate():
    text=inspect.getsource(original.audio_gate);marker='    # Fixed native inflation effect calls are unchanged original\n'
    need(text.count(marker)==1,'Whole original generic PCM/channel/packet/DSP boundary');text=text[:text.index(marker)]
    changes=[
      ('physical=capture.state.gate(capture.state.rows(text),fighter,side,guest)','physical=current.state.contract(text,fighter,side)'),
      ('capture.state.rows(text)','stock_rows(text)'),
      ("physical['origin']","physical['actualNativeActivation']"),
      ("int(result[0]['frame'])==origin+750","int(result[0]['frame'])==int(current.state.rows(text,'MK2_SSECOND_','RESULT')[0]['frame'])"),
      ("int(chunks[-1]['frame'])==origin+749","int(chunks[-1]['frame'])in(origin+748,origin+749)"),
      ("begin[0]['id']=='4'","begin[0]['id']=='10'"),
      ('Original Kitana task, not added-character proxy action','Original Scorpion10 task, not added-character proxy action')]
    for before,after in changes:
        need(text.count(before)==1,'Exact complete generic audio adaptation '+before);text=text.replace(before,after)
    text+='    return tail(text,baseline,meta,oldmeta,guest,fighter,side,physical,action,origin,actual,chunks)\n'
    scope=dict(capture=current.previous,current=current,need=need,hashlib=hashlib,tagged=original.tagged,stock_rows=stock_rows,tail=tail)
    exec(compile(text,__file__+'::whole3952_generic_PCM_channels_packets_DSP','exec'),scope)
    return scope['audio_gate']

gate=make_gate()

def source_contract(guest):
    current.state.source.source_boundary();stock=(ROOT/'mk2/mk2-maincpu.bin').read_bytes()
    for first,last in((0xff8bbfe0,0xff8bd040),(0xff8ea3f0,0xff8ea4c0),(0xff9a6d00,0xff9a7400),
      (0xff9adb00,0xff9adc80),(0xff9ad140,0xff9ad1b0),(0xffa0ef20,0xffa122a0),(0xffa122d0,0xffa13df0)):
        a,b=(first-0xff800000)//8,(last-0xff800000)//8
        need(guest[a:b]==stock[a:b],'Whole original secondary/effect/voice/table/priority/packet source '+hex(first))
    for pc,command in((0xff8bc860,0x44),(0xff8bca80,0x44),(0xff8bcad0,0x56),(0xff9a6f60,0xc4),(0xff9a72c0,0xc4),(0xff9adc00,0xc4)):
        a=(pc-80-0xff800000)//8
        need(guest[a:a+10]==struct.pack('<5H',0x09c0,command,0x0d5f,0x2530,0xffa1),'Exact original literal/CALLA selector source '+hex(pc))
    for pc,target in((0xff8bc890,0x1fd0),(0xff8bcb00,0x2070)):
        need(struct.unpack_from('<3H',guest,(pc-48-0xff800000)//8)==(0x0d5f,target,0xffa1),'Exact original pain/death caller source')
    need(struct.unpack_from('<HI',guest,(0xffa122a0-0xff800000)//8)==(0xc080,0xff800000+(0xfe000+2*0x20)*8)and
         struct.unpack_from('<12H',guest,0xfe040)==(0x0b42,0xffef,0xca06,0x0b42,0xffed,0xca03,0xc080,0x22d0,0xffa1,0xc080,0x23b0,0xffa1),
         'Exact true18 native female branch extension preserving original male/Jade semantics, no proxy identity')

def run():
    need(not OUT.exists(),'Fresh immutable four-context native audio qualification');guest=current.state.source.current.expected();source_contract(guest)
    pins={str(Path(__file__).resolve()):sha(__file__),str(Path(original.__file__).resolve()):sha(original.__file__)}
    for fighter,side in(('kano',1),('kano',2),('sonya',1),('sonya',2)):
        f=ROOT/f'audit_v4667_scorpion_secondary_{fighter}_p{side}_audio_samples';b=ROOT/f'audit_v4667_scorpion_secondary_{fighter}_p{side}_audio_nosamples'
        text=(f/'run.log').read_text();baseline=(b/'run.log').read_text();meta=json.loads((f/'result.json').read_text());oldmeta=json.loads((b/'result.json').read_text())
        observation=ROOT/f'audit_v4668_scorpion_secondary_{fighter}_p{side}_audio_observed/report.json';proof=json.loads(observation.read_text())
        need(proof['passed']and proof['completeMixedPCMEqualSamplesOnOff']and proof['everyOriginalColdStateAndRGBEventUnchanged'],
             'Actual terminal full waveform byte comparison and whole cold state/RGB, not digest-only inferred waveform')
        for p,h in proof['inputHashes'].items():need(p not in pins or pins[p]==h,'Consistent actual native/audio inputs');pins[p]=h
        pins[str(observation)]=sha(observation)
        positive=gate(text,baseline,meta,oldmeta,guest,fighter,side);faults=[]
        def reject(label,t=text,bt=baseline,m=meta,om=oldmeta):
            try:gate(t,bt,m,om,guest,fighter,side)
            except (ValueError,KeyError)as error:faults.append(dict(kind=label,rejectedBy=str(error)))
            else:raise ValueError('Actual native secondary audio fault accepted '+label)
            need(gate(text,baseline,meta,oldmeta,guest,fighter,side)==positive,'Whole actual positive restored after every real row fault')
        def mutate(tag,key,value,row=None,prefix='MK2_MAUDIO_'):
            line=next(l for l in text.splitlines()if l.startswith(prefix+tag+' ')and(row is None or dict(re.findall(r'(\w+)=([^\s]+)',l))==row))
            changed,n=re.subn(r'\b'+key+r'=\S+',key+'='+value,line,count=1);need(n==1 and changed!=line,'Non-vacuous actual source/owned audio row fault')
            return text.replace(line,changed,1),baseline.replace(line,changed,1)
        for tag,key,value in(('BEGIN','a8','01000000'),('BEGIN','id','1'),('CHANNEL','sample','0'),('CHANNEL','pos','123.00000000'),
                              ('SOUND','pc','FFF00000'),('SOUND','word','FFF7')):
            t,bt=mutate(tag,key,value);reject(tag+'_'+key,t,bt)
        pain,death=positive['sourceQualifiedPainVoice'],positive['sourceQualifiedDeathVoice'];fixed=positive['actualSourceBoundSelectors'][0]
        for label,tag,key,value,row in(
          ('foreign_true_voice','ROUTE','id','1',pain[0]),('wrong_gender','ROUTE','entry','FFA123B0'if fighter=='kano'else'FFA122D0',pain[2]),
          ('wrong_packed_pain','ROUTE','a1','32340038',pain[1]),('wrong_death_byte','ROUTE','a1','00000049',death[3]),
          ('wrong_literal_effect','ROUTE','a0','00000043',fixed['call']),('wrong_queue_word','QUEUE','a3','00000000',fixed['queue']),
          ('wrong_queue_priority','QUEUE','a1','00000000',fixed['queue']),('wrong_packet','PACKET','a3','00000000',fixed['packet'])):
            t,bt=mutate(tag,key,value,row);reject(label,t,bt)
        first=float(current.previous.rows(text,'SOUND')[0]['seconds']);stop=float(current.previous.rows(text,'SOUND')[1]['seconds'])
        remove=lambda t:'\n'.join(l for l in t.splitlines()if not(l.startswith('MK2_MAUDIO_DELIVERY ')and first<=float(dict(re.findall(r'(\w+)=([^\s]+)',l))['seconds'])<stop))+'\n'
        reject('missing_actual_DSP_read',remove(text),remove(baseline))
        chunks=original.tagged(text,'MK2_BBAUDIO_PCM_DIGEST');line=next(l for l in text.splitlines()if l.startswith('MK2_BBAUDIO_PCM_DIGEST ')and 'seconds='+chunks[len(chunks)//2]['seconds']+' 'in l)
        reject('missing50Hzupdate',text.replace(line+'\n','',1),baseline.replace(line+'\n','',1))
        m=copy.deepcopy(meta);m['mixedPCMSHA256']='0'*64;reject('phantom_whole_waveform',m=m)
        t,bt=mutate('GUEST_DIGEST','sha256','0'*64,prefix='MK2_SSECOND_');reject('wrong_physical_guest',t,bt)
        CASES.append(dict(fighter=fighter,side=side,nativeAudio=positive,actualFaultsRejected=faults))
        print(f'{fighter}P{side}: original voices,24 selectors,56DSP bytes and full paired waveform; {len(faults)} real faults rejected',flush=True)
    need(all(sha(p)==h for p,h in pins.items()),'All executed native/source/capture evidence unchanged')
    return dict(passed=True,actualContexts=4,cases=CASES,inputHashes=pins,actualSelectorsSourceBound=96,
                actualNativeDCSBytesDelivered=224,actualRowFaultsRejected=sum(len(c['actualFaultsRejected'])for c in CASES),
                bothTrueVictimNativeVoiceGendersBothSlotsAccepted=True,wholeGenericPCMChannelsPacketsDSPRetained=True,
                directPacketCallerOriginsAccepted=False,stockWholeWaveformReferenceAccepted=False,
                allFinisherVictimAudioAccepted=False,fullPortAcceptance=False,rawMediaFilesWritten=0,scope=__doc__)

if __name__=='__main__':
    try:report=run()
    except Exception as error:report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),completed=CASES,fullPortAcceptance=False)
    OUT.mkdir();need(subprocess.run(['compact.exe','/C','/I','/Q','/S:'+str(OUT)],capture_output=True).returncode==0,'Compressed before writes')
    (OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items()if k not in('inputHashes','cases','completed')},indent=2),flush=True)
    raise SystemExit(0 if report['passed']else 1)
