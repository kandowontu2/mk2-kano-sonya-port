"""Whole same-run packet/ADSP and all19 native sound/video source positions.

Source clocks include complete50Hz sound updates,60Hz ownership playing()
updates, its main/aux short circuit, true clip EOF, new-launch stop and original
previous-length source-number assignment. No guessed cadence or PCM fitting.
Private owner fields were not captured; their retirement is not accepted here.
"""
import bisect,copy,hashlib,inspect,json,re,struct,traceback,wave
from decimal import Decimal
from pathlib import Path
import numpy as np
import qualify_native_selector_sonya_cpu_air_audio_stop as audio
import verify_current_cpu_blade_knife_audio_v6370 as packets

ROOT,need,sha=audio.ROOT,audio.need,audio.sha
OUT=ROOT/'audit_native_selector_sonya_cpu_air_channels_checked'
ATTO=10**18
PERIOD60=ATTO//60


def source_events(text,pins):
    source=inspect.getsource(audio.compound.predict_mix)
    first=source.index(' events=[]');last=source.index(' voices={c:',first)
    source="def events(text,pins):\n fighter='sonya'\n"+source[first:last]+" return events\n"
    before="['FFFD','6B01','6B02','6B00','FFFD']"
    need(source.count(before)==1,'Whole original actual-source asset/interpolation/event constructor')
    source=source.replace(before,repr(audio.ORDER),1)
    scope=dict(vars(audio.compound),__file__=__file__)
    exec(compile(source,__file__+'::whole_original_source_event_constructor','exec'),scope)
    events=scope['events'](text,pins)
    need(len(events)==8,'All eight actual imported sound starts, none filtered')
    return events


def packet_gate(records):
    source=inspect.getsource(packets.old.gate)
    first=source.index(" packets=audio('PACKET');");last=source.index(' return dict(passed=True,',first)
    source="""def verify(records):
 audio=lambda tag:records.get('MK2_MAUDIO_'+tag,[])
 identity=18
 ends=audio('RESULT');need(len(ends)==1,'Single original audio terminal');end=ends[0]
"""+source[first:last]+" return dict(packets=len(packets),portWrites=len(sounds),nativeDSPReads=len(delivery),trueWinnerMarkers=len(markers),ownedLaunchCryMarkers=len(launches))\n"
    for before,after in (
        ("packets=audio('PACKET');all_sounds=audio('SOUND');",
         "packets=audio('PACKET');all_sounds=audio('SOUND');launches=[r for r in all_sounds if r['word'] in ('6B01','6B02')];need(len(launches)==6 and all(r['mask']=='FFFF' and r['pc']==('FFF9A4C0' if r['word']=='6B01' else 'FFF9A520') and r['a8']=='010350A0' and r['a13']=='0106BF30' for r in launches),'Every genuine owned CPU launch/cry port store');"),
        ("len(markers)==1 and markers[0]['word']==('FFFE'if identity==17 else'FFFD')and markers[0]['mask']=='FFFF'and",
         "len(markers)==2 and all(r['word']==('FFFE'if identity==17 else'FFFD') and r['mask']=='FFFF' for r in markers)and"),
        ('len(all_sounds)==len(sounds)+1','len(all_sounds)==len(sounds)+2+len(launches)')):
        need(source.count(before)==1,'Only genuine imported markers differ; entire native packet/ADSP contract unchanged')
        source=source.replace(before,after,1)
    scope=dict(packets.old.gate.__globals__,__file__=__file__)
    exec(compile(source,__file__+'::whole_native_packet_port_ADSP_chronology','exec'),scope)
    return scope['verify'](records)


def native_source(pins):
    path=ROOT/'mame-mkp/src/devices/sound/samples.cpp';text=path.read_text()
    need(sha(path)=='8BF4BB350F40B309A5CECB4591DF8EE32A3563C3E061F2D2338C8CBA76B5353F','Whole actual original samples.cpp source')
    start=text.index('bool samples_device::playing(uint8_t channel) const');end=text.index('\n}',start)+2
    need('chan.stream->update();' in text[start:end] and 'chan.source != nullptr' in text[start:end],
         'playing() actually synchronizes source, independent of saved sample number')
    start=text.index('void samples_device::stop(uint8_t channel)');end=text.index('\n}',start)+2
    need('chan.stream->update();' not in text[start:end] and 'chan.source = nullptr;' in text[start:end],
         'Stop clears pointer without updating pending cache')
    need('chan.source_num = (chan.source_len > 0) ? samplenum : -1;' in text,
         'Native source number derives from previous length, not playing pointer')
    path2=ROOT/'mame-mkp/src/mame/midway/midtunit_m.cpp';code=path2.read_text()
    for fragment in ('else if (!m_mk2ks_voices->playing(10 + slot * 2) && !m_mk2ks_voices->playing(11 + slot * 2))',
        'm_mk2ks_battle_audio_timer->adjust(attotime::from_hz(60), 0, attotime::from_hz(60));',
        'mk2ks_battle_audio_stop(slot, "new_launch");', 'if (data != 0x6b02)'):
        need(fragment in code,'Exact compiled main/aux/timer/launch operation '+fragment)
    pins[str(path)]=sha(path);pins[str(path2)]=sha(path2)


def channels(records,events,headers,pins):
    model=audio.compound.original
    sound=records['MK2_TOMB_MIX_CHANNEL'];video=records['MK2_MAUDIO_CHANNEL']
    need([(int(r['index']),int(r['channel'])) for r in sound]==[(i,c) for i in range(1,len(headers)+1) for c in range(19)],
         'Every19-channel precise callback in exact original order, no duplicates/missing rows')
    need([(int(r['frame']),int(r['channel'])) for r in video]==[(f,c) for f in range(1818,3619) for c in range(19)],
         'Every19-channel actual video callback through real original terminal')
    selection=ROOT/'samples/mk2ks/kano_select.wav';pins[str(selection)]=sha(selection)
    with wave.open(str(selection),'rb') as clip:
        need((clip.getnchannels(),clip.getsampwidth(),clip.getframerate(),clip.getnframes())==(1,2,16000,18400),'Whole initial completed native Kano selection clip')
        _,initial_positions=model.sample_values(np.frombuffer(clip.readframes(18400),'<i2').copy(),16000)
    ticks=[int(Decimal(h['seconds'])*ATTO) for h in headers]
    starts={c:[] for c in range(19)}
    for e in events:starts[e['channel']].append(e)
    active_counts={0:0,12:0,13:0};exact_video=exact_sound=0
    def expected(channel,clock):
        now=int(Decimal(clock)*ATTO)
        launched=[e for e in starts[channel] if int(Decimal(e['marker']['seconds'])*ATTO)<=now]
        if not launched:return 0xffffffff,(18400 if channel==0 else 0),(initial_positions[-1] if channel==0 else 0.0)
        event=launched[-1];source_time=int(Decimal(event['marker']['seconds'])*ATTO)
        index=bisect.bisect_right(ticks,now)-1
        last_sound=ticks[index] if index>=0 else source_time
        last_update=max(source_time,last_sound)
        if channel in (12,13):
            main=next(e for e in events if e['channel']==12 and e['marker']['frame']==event['marker']['frame'])
            onset=int(Decimal(main['marker']['seconds'])*ATTO)
            n=(now-onset)//PERIOD60
            if n>=1:
                tick=onset+n*PERIOD60
                if channel==12 or model.sample_clock(str(Decimal(tick)/ATTO),True)-main['start']>=len(main['positions']):
                    last_update=max(last_update,tick)
        count=min(len(event['positions']),max(0,model.sample_clock(str(Decimal(last_update)/ATTO),True)-event['start']))
        position=event['positions'][count-1] if count else 0.0
        previous_length=(18400 if channel==0 else 0) if len(launched)==1 else launched[-2]['length']
        number=event['sample_id'] if count<len(event['positions']) and previous_length>0 else 0xffffffff
        return number,event['length'],position
    for tag,rows,precise in (('MK2_TOMB_MIX_CHANNEL',sound,True),('MK2_MAUDIO_CHANNEL',video,False)):
        for row in rows:
            channel=int(row['channel']);want=expected(channel,row['seconds'])
            need(row['writes']==row['loop']==row['paused']=='0' and row['assistance']=='none','Every genuine state passive, finite and unpaused')
            if precise:
                head=headers[int(row['index'])-1]
                need(row['frame']==head['frame'] and row['seconds']==head['seconds'],'Each full precise row owns actual PCM callback')
            actual=(int(row['sample']),int(row['length']),float(row['position'] if precise else row['pos']))
            need(actual[:2]==want[:2] and (row['bits']==struct.pack('<d',want[2]).hex().upper() and actual[2]==want[2] if precise else row['pos']==format(want[2],'.8f')),
                 'Source-exact native19-channel state '+str((tag,row['frame'],channel,actual,want)))
            if precise:exact_sound+=1
            else:exact_video+=1
            if channel in active_counts and want[0]!=0xffffffff:active_counts[channel]+=1
    need(all(active_counts.values()),'Both winner and both battle channels have actual active-source coverage')
    # The independent original SS observer covers the same actual callback,
    # including active sources whose first saved source number is -1.
    ss=[r for r in records['MK2_SS_CHANNEL'] if 1818<=int(r['frame'])<=3617]
    by={(r['frame'],r['channel']):r for r in video}
    need(len(ss)==1800*19,'All shared original shadow-observer channel callbacks retained')
    for row in ss:
        other=by[row['frame'],row['channel']]
        need(all(row[k]==other[k] for k in ('sample','length','pos','loop','paused','writes','assistance')),
             'Each original independent shadow-observer channel state equals same native video callback')
    return dict(passed=True,exactPreciseChannelStates=exact_sound,exactVideoChannelStates=exact_video,
        independentShadowObserverStates=len(ss),activeStateCounts=active_counts,
        all19RecordedChannelClocksAccepted=True,allOriginalRepeatedDoubleBitsAccepted=True,
        nativeMainAux60HzShortCircuitSourceBound=True,firstLaunchSavedNumberFromPreviousLength=True,
        completeRecordedWindowAccepted=True,privateOwnerRetirementAccepted=False,allPriorityContextsAccepted=False)


def execute(state):
    need(not OUT.exists(),'Fresh immutable full actual19-channel/packet proof')
    capture=audio.contact.control.capture;held=capture.NATIVE_HANDLES[capture.KEY]
    parent=ROOT/'audit_native_selector_sonya_cpu_air_sealed.json';proof=json.loads(parent.read_text());pins=dict(proof['inputHashes'])
    need(proof['passed'] and held['process'].poll()==0 and proof['actualNativeIdentity']==held['identity'] and all(sha(p)==h for p,h in pins.items()),'Same sealed actual50372 terminal and every whole source/native input')
    text=capture.RAM_CASES[capture.KEY][1];headers=capture.AUDIO[capture.KEY]['pcmHeaders']
    records=packets.old.inventory(text);events=source_events(text,pins);native_source(pins)
    packet=packet_gate(records);clock=channels(records,events,headers,pins)
    need((packet['packets'],packet['portWrites'],packet['nativeDSPReads'],packet['trueWinnerMarkers'],packet['ownedLaunchCryMarkers'])==(133,266,266,2,6),'All native packet/ADSP and all private port stores accounted')
    faults=[]
    def corrupt(tag,key,value,**where):
        rows=records[tag];target=next(r for r in rows if all(r.get(k)==str(v) for k,v in where.items()))
        need(target[key]!=str(value),'Effective actual record corruption')
        return dict(records,**{tag:[dict(r,**{key:str(value)}) if r is target else r for r in rows]})
    trials=[]
    for label,tag,key,value,where,check in (
        ('native_packet_value','MK2_MAUDIO_PACKET','a3','00000301',dict(frame=1817),packet_gate),
        ('native_high_port_prefix','MK2_MAUDIO_SOUND','word','0003',dict(pc='FFA13C90',frame=1817),packet_gate),
        ('native_low_port_owner','MK2_MAUDIO_SOUND','a8','01034E90',dict(pc='FFA13D60',frame=1817),packet_gate),
        ('native_ADSP_byte','MK2_MAUDIO_DELIVERY','word','0004',dict(frame=1817,dsp_pc='03A1'),packet_gate),
        ('private_launch_wrong_owner','MK2_MAUDIO_SOUND','a13','0106A370',dict(frame=2731,word='6B01'),packet_gate),
        ('private_cry_wrong_PC','MK2_MAUDIO_SOUND','pc','FFF9A690',dict(frame=2806,word='6B02'),packet_gate)):
        trials.append((label,corrupt(tag,key,value,**where),check))
    for label,tag,key,value,where in (
        ('first_launch_saved_number','MK2_MAUDIO_CHANNEL','sample',14,dict(frame=2392,channel=12)),
        ('active_cry_position','MK2_MAUDIO_CHANNEL','pos','1.00000000',dict(frame=2751,channel=13)),
        ('active_cry_length','MK2_MAUDIO_CHANNEL','length',66522,dict(frame=2751,channel=13)),
        ('whole_precise_double_bits','MK2_TOMB_MIX_CHANNEL','bits','0000000000000000',dict(channel=13,frame=2751)),
        ('winner_video_sample','MK2_MAUDIO_CHANNEL','sample',2,dict(frame=2150,channel=0)),
        ('foreign_channel','MK2_MAUDIO_CHANNEL','length',1,dict(frame=2751,channel=18)),
        ('looped_battle_channel','MK2_MAUDIO_CHANNEL','loop',1,dict(frame=2751,channel=12)),
        ('independent_shadow_channel','MK2_SS_CHANNEL','pos','0.00000000',dict(frame=2751,channel=13))):
        trials.append((label,corrupt(tag,key,value,**where),lambda r:channels(r,events,headers,pins)))
    for tag,check in (('MK2_MAUDIO_DELIVERY',packet_gate),('MK2_TOMB_MIX_CHANNEL',lambda r:channels(r,events,headers,pins))):
        trials.append(('missing_'+tag,dict(records,**{tag:records[tag][1:]}),check))
        trials.append(('duplicate_'+tag,dict(records,**{tag:[records[tag][0],*records[tag]]}),check))
    for label,bad,check in trials:
        try:check(bad)
        except (ValueError,AssertionError,KeyError,IndexError) as error:faults.append(dict(kind=label,rejectedBy=str(error)))
        else:raise ValueError('Effective actual sound-channel/packet fault admitted: '+label)
    need(len(faults)==18 and packet_gate(records)==packet and channels(records,events,headers,pins)==clock,'All18 effective faults reject and full native positive restored')
    for p in (Path(__file__),parent,Path(packets.__file__),Path(packets.old.__file__),Path(audio.__file__)):
        key=str(p.resolve());digest=sha(p);need(key not in pins or pins[key]==digest,'No executed source/prior proof altered');pins[key]=digest
    need(all(sha(p)==h for p,h in pins.items()),'Entire whole source/native inventory unchanged')
    value=dict(passed=True,goalStatus='active',actualNativeIdentity=held['identity'],nativeExit=0,wholeNativePacketADSPChronology=packet,
        all19ChannelClocks=clock,effectiveFaultsRejected=faults,inputHashes=pins,requirements=proof['requirements'],remainingGroups=proof['remainingGroups'],
        completeRecorded19ChannelClocksAccepted=True,wholeRecordedNativePacketsAccepted=True,privateOwnerRetirementAccepted=False,
        allHitGruntProducersIndividuallyAccepted=False,allOverlapPriorityContextsAccepted=False,heardAudioQualityAccepted=False,fullPortAcceptance=False,
        publicPlayableChanged=False,newNativeGames=0,newBuilds=0,newROMCopies=0,newRawMediaFiles=0,newZIPs=0)
    OUT.mkdir();(OUT/'report.json').write_text(json.dumps(value,indent=2)+'\n');return value


def safe_execute(state):
    try:return execute(state)
    except Exception as error:
        need(not OUT.exists(),'Preserve actual full-channel/packet rejection')
        OUT.mkdir();(OUT/'failure.json').write_text(json.dumps(dict(passed=False,error=repr(error),traceback=traceback.format_exc(),goalStatus='active',fullPortAcceptance=False),indent=2)+'\n')
        raise
