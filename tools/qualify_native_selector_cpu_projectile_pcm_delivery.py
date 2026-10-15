"""Same whole current PCM: real owner cues, all packet/ADSP bytes and faults.

Keep the entire original packet splitting/port/firmware chronology. Exactly
three source-bound battle markers are additional direct writes, not arbitrary
exceptions. All19 source clocks retained; initial Ring release BEFORE the
declared audio origin is explicitly not accepted from this window.
"""
import hashlib,inspect,json,re,struct,traceback
from pathlib import Path
import qualify_native_selector_cpu_projectile_pcm_mix_serialized as prior
import verify_current_cpu_blade_knife_audio_v6370 as packets

capture=prior.prior.capture
model=prior.prior.model
ROOT,need,sha=prior.ROOT,prior.need,prior.sha
OUT=ROOT/'audit_native_selector_cpu_projectile_pcm_delivery_checked'


def source_cues(text,guest):
    rows=model.rows
    fields=rows(text,'MK2_CPU_PAIR_FIELD');by={int(r['frame']):r for r in fields}
    need(len(by)==len(fields)==1517,'All actual live original paired physical owner callbacks')
    for r in fields:
        need(r['actor']==r['owner']=='010350A0'and r['main']=='0106BF30'and
             r['id']==r['roster']=='18'and r['state']=='0'and r['cpu_slot']=='2'and
             r['vactor']==r['vowner']=='01034E90'and r['vmain']=='0106A370'and
             r['vid']==r['vroster']=='17'and r['vstate']=='1'and r['human_slot']=='1'and
             r['writes']=='0'and r['assistance']=='none','Every actual true Sonya CPU/human Kano owner/role, no fighter proxy')
    sounds=rows(text,'MK2_MAUDIO_SOUND');owned=[]
    specs=[('6B00',1966,'FFFFCAC0',0x207,45512),('6B01',2766,'FFF9A4C0',0x204,40720),
           ('6B02',2766,'FFF9A520',0x204,66523)]
    for word,frame,pc,action,length in specs:
        marks=[r for r in sounds if r['word']==word]
        need(len(marks)==1,'Exactly one actual source-owned battle command '+word)
        mark=marks[0];physical=by[frame+1]
        need(mark['frame']==str(frame)and mark['pc']==pc and mark['mask']=='FFFF'and
             mark['a8']==physical['actor']and mark['a13']==physical['main']and
             int(physical['action'])==action and physical['mode']=='2'and physical['hp']=='161'and
             mark['writes']=='0'and mark['assistance']=='none','Executing battle marker owns actual native action/actor/Main/physical role')
        at=(int(pc,16)-96-0xff800000)//8
        need(guest[at:at+12]==struct.pack('<6H',0x09e0,int(word,16),0,0x0580,0x1030,0x01d0),
             'Entire actual marker MOVI/direct-port source instructions')
        finish=Decimal(mark['seconds'])+Decimal(length)/48000
        window=[r for r in fields if int(r['frame'])>frame and
                Decimal(r['frame'])*Decimal('0.01827925')<=finish]
        # The base physical observer uses this exact screen period; using all
        # actual corresponding video timestamps below avoids a fitted offset.
        times={int(r['frame']):Decimal(r['seconds'])for r in rows(text,'MK2_MAUDIO_CHANNEL')if r['channel']=='0'}
        window=[r for r in fields if int(r['frame'])>frame and times[int(r['frame'])]<=finish]
        need(window and all(r['mode']=='2'and r['hp']=='161'for r in window),
             'Every retained live callback during each sound lifetime has unchanged real owner/mode/health; no premature-stop state inferred')
        owned.append(dict(word=word,frame=frame,actor=mark['a8'],main=mark['a13'],action=action,fullSourceInstructionsVerified=True))
    direct=[r for r in sounds if r['pc']not in('FFA13C90','FFA13D60')]
    need([(r['word'],r['pc'])for r in direct]==
         [('6B00','FFFFCAC0'),('FFFD','FFFB7140'),('6B01','FFF9A4C0'),('6B02','FFF9A520')],
         'Every actual direct sound write exactly owned: three battle cues plus true Sonya winner')
    stock=(ROOT/'mk2/mk2-maincpu.bin').read_bytes()
    lo,hi=(0xffa12530-0xff800000)//8,(0xffa13ed0-0xff800000)//8
    need(guest[lo:hi]==stock[lo:hi],'Entire original effect/priority queue/packet/handshake kernel unchanged')
    first=rows(text,'MK2_FIRST_PROJECTILE_ENTRY')
    need(len(first)==1 and first[0]['kind']=='ring'and first[0]['frame']=='1817'and
         rows(text,'MK2_MAUDIO_BEGIN')[0]['origin']=='1818','Initial Ring release really precedes declared audio window; do not fabricate its cue trace')
    return dict(passed=True,actualCPUIdentity=18,actualHumanIdentity=17,entireLiveOwnerFields=len(fields),
        fullSourceOwnedBattleCommands=owned,exactDirectWrites=4,initialRingReleaseBeforeAudioOriginNotObserved=True,
        allStartupReleaseAudioAccepted=False,fullMovePhaseHealthAcceptance=False)


from decimal import Decimal


def packet_gate(text):
    source=inspect.getsource(packets.old.gate)
    first=source.index(" packets=audio('PACKET');");last=source.index(' return dict(passed=True,',first)
    block=source[first:last]
    need(block.count('len(all_sounds)==len(sounds)+1')==1,'Only actual additional three owned direct cues differ')
    block=block.replace('len(all_sounds)==len(sounds)+1','len(all_sounds)==len(sounds)+4',1)
    source="""def gate(text):
 records=old.inventory(text)
 audio=lambda tag:records.get('MK2_MAUDIO_'+tag,[])
 identity=18
 ends=audio('RESULT');need(len(ends)==1,'Single original audio terminal');end=ends[0]
"""+block+"\n return dict(packets=len(packets),portWrites=len(sounds),nativeDSPReads=len(delivery),trueWinnerMarkers=len(markers),additionalOwnedBattleMarkers=3)\n"
    scope=dict(packets.old.gate.__globals__,old=packets.old)
    exec(compile(source,__file__+'::whole_original_packet_port_ADSP_plus_three_bound_battle_cues','exec'),scope)
    return scope['gate'](text)


def clock_gate(text,headers,extra,waveform):
    records=model.rows(text,'MK2_TOMB_MIX_CHANNEL')
    need([(r['frame'],r['seconds'],int(r['index']),int(r['channel']))for r in records]==
         [(h['frame'],h['seconds'],i+1,c)for i,h in enumerate(headers)for c in range(19)],
         'All19 exact source snapshots bind original sound callback/header/index/order')
    scope=dict(vars(prior.prior),__file__=__file__)
    source=inspect.getsource(prior.prior.channel_clocks)
    before="need(actual==want,'Every source-derived native channel/length/position "
    need(source.count(before)==1,'Only declared video8-decimal serialization adaptation')
    source=source.replace(before,"need(actual[:2]==want[:2]and (r['pos']==format(want[2],'.8f')if video else actual[2]==want[2]),'Every source-derived native channel/length/position ",1)
    exec(compile(source,__file__+'::whole_exact_native_channel_clocks','exec'),scope)
    return scope['channel_clocks'](text,headers,extra,waveform)


def execute(state):
    need(not OUT.exists()and not capture.prior.current.prior.identity.census(),'Same terminal original native game; no replay')
    path=prior.OUT/'report.json';positive=json.loads(path.read_text());waveform=positive['wholeMixedWaveform']
    need(positive['passed']and waveform['passed']and waveform['differentChannelSamples']==0 and
         waveform['actualSHA256']==waveform['predictedSHA256']and waveform['comparedStereoFrames']==1579200 and
         all(sha(p)==h for p,h in positive['inputHashes'].items()),'Entire original four-cue/native DCS waveform and exact clocks intact')
    folder,text,images=capture.RAM_CASES[capture.KEY];held=capture.NATIVE_HANDLES[capture.KEY]
    need(held['process'].poll()==0 and held['identity']==positive['actualNativeIdentity']and held['process'].pid==47172,
         'Same exact original terminal native handle')
    pins=dict(positive['inputHashes']);extra=prior.prior.sources(text,pins);headers=capture.AUDIO[capture.KEY]['pcmHeaders']
    def gate(value,guest=state['guest']):
        return dict(cues=source_cues(value,guest),packets=packet_gate(value),
            clocks=clock_gate(value,headers,prior.prior.sources(value,pins),waveform))
    whole=gate(text)
    def alter(tag,key,value,**where):
        for line in text.splitlines():
            if line.startswith(tag+' '):
                row=dict(re.findall(r'(\w+)=([^\s]+)',line))
                if all(row.get(k)==str(v)for k,v in where.items()):
                    changed,n=re.subn(r'\b'+key+r'=\S+',key+'='+value,line,count=1)
                    need(n==1 and changed!=line,'Every actual source/audio fault changes one observed record')
                    return text.replace(line,changed,1)
        raise ValueError('No actual fault target '+tag+' '+str(where))
    trials=[
        ('square_owner',alter('MK2_MAUDIO_SOUND','a8','01034E90',word='6B00')),
        ('bicycle_main',alter('MK2_MAUDIO_SOUND','a13','0106A370',word='6B01')),
        ('actual_CPU_identity',alter('MK2_CPU_PAIR_FIELD','id','1',frame=1967)),
        ('actual_human_role',alter('MK2_CPU_PAIR_FIELD','vstate','0',frame=2767)),
        ('wrong_square_command',alter('MK2_MAUDIO_SOUND','word','6B03',word='6B00')),
        ('wrong_packet',alter('MK2_MAUDIO_PACKET','a3','000000BE',frame=1837)),
        ('wrong_native_port_byte',alter('MK2_MAUDIO_SOUND','word','FF01',pc='FFA13C90',frame=1837)),
        ('wrong_DSP_delivery',alter('MK2_MAUDIO_DELIVERY','word','0001',dsp_pc='03A1')),
        ('wrong_winner_identity',alter('MK2_MAUDIO_SOUND','word','FFFE',pc='FFFB7140')),
        ('exact_Square_position_bit',alter('MK2_TOMB_MIX_CHANNEL','bits','0000000000000000',frame=1966,channel=12)),
        ('wrong_Square_pointer_length',alter('MK2_TOMB_MIX_CHANNEL','length','40720',frame=1966,channel=12)),
        ('cached_bicycle_wrong_source_number',alter('MK2_TOMB_MIX_CHANNEL','sample','4294967295',frame=2767,channel=12)),
        ('first_load_cry_number_not_pointer',alter('MK2_TOMB_MIX_CHANNEL','sample','15',frame=2767,channel=13)),
        ('video_owner_timer_clock',alter('MK2_MAUDIO_CHANNEL','pos','0.00000000',frame=2000,channel=12)),
        ('video_cry_short_circuit_clock',alter('MK2_MAUDIO_CHANNEL','pos','0.00000000',frame=2780,channel=13)),
        ('looping_launch',alter('MK2_TOMB_MIX_CHANNEL','loop','1',frame=2767,channel=12)),
        ('private_finisher_channel_leak',alter('MK2_TOMB_MIX_CHANNEL','sample','5',frame=2767,channel=14)),
        ('native_callback_frame',alter('MK2_TOMB_MIX_CHANNEL','frame','2766',frame=2767,channel=12))]
    faults=[]
    for label,bad in trials:
        try:gate(bad)
        except(AssertionError,ValueError,KeyError,IndexError,StopIteration)as error:faults.append(dict(fault=label,rejectedBy=str(error)))
        else:raise ValueError('Actual native sound counterexample admitted '+label)
        print('Current full-mix source/clock/packet fault rejected: '+label,flush=True)
    for label,address in(('actual_Square_store_opcode',0xffffca90),('actual_bicycle_command_opcode',0xfff9a460)):
        bad=bytearray(state['guest']);bad[(address-0xff800000)//8]^=1
        try:gate(text,bytes(bad))
        except(AssertionError,ValueError,KeyError)as error:faults.append(dict(fault=label,rejectedBy=str(error)))
        else:raise ValueError('Actual native command source corruption admitted '+label)
    need(gate(text)==whole,'Entire original native cue/packet/clock positive restored after every actual fault')
    for p in(Path(__file__),Path(prior.__file__),Path(prior.prior.__file__),Path(packets.__file__),Path(packets.old.__file__),
             path,prior.OUT/'waveform.json',prior.prior.OUT/'failure.json'):
        pins[str(p.resolve())]=sha(p)
    need(all(sha(p)==h for p,h in pins.items()),'All executed original/successor sources/failures/receipts pinned unchanged')
    OUT.mkdir();report=dict(passed=True,goalStatus='active',actualNativeIdentity=held['identity'],wholeCurrentSourceAudio=whole,
        completeStereoFrames=1579200,wholeMixedPCMSHA256=waveform['actualSHA256'],actualRecordSourceFaultsRejected=faults,
        retainedPCMAndSourceFaults=waveform['actualRawMixedPCMFaultsRejected']+waveform['actualMixedSourceOperationFaultsRejected']+waveform['additionalActualSourceFaultsRejected'],
        requirements=positive['requirements'],remainingGroups=positive['remainingGroups'],inputHashes=pins,
        currentFiniteKanoSonyaAllFourCueMixedAudioAccepted=True,allStartupReleaseAudioAccepted=False,
        allArenasSlotsVictimsAudioAccepted=False,heardAudioQualityAccepted=False,fullPortAcceptance=False,
        publicPlayableChanged=False,newNativeGames=0,newBuilds=0,newROMCopies=0,newRawMedia=0,newZIPs=0)
    capture.prior.current.prior.save(OUT/'report.json',report)
    print('PASS current finite Kano/Sonya full-cue mixed audio/source/77 packets/all19 clocks/20 actual faults; full goal remains active',flush=True)
    return report


def safe_execute(state):
    try:return execute(state)
    except Exception as error:
        need(not OUT.exists(),'Preserve original actual audio qualification failure')
        OUT.mkdir();capture.prior.current.prior.save(OUT/'failure.json',dict(passed=False,goalStatus='active',error=repr(error),
            traceback=traceback.format_exc(),newNativeGames=0,fullPortAcceptance=False))
        raise
