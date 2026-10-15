"""Actual final-KO to native-ending/attract audio windows, complete phase gates.

Requires original accepted cold native transcript equality, whole guest/RGB,
every stereo PCM update, all14 inactive sample channels, actual source PCs and
sound-port bytes read by DCS. No independent stock waveform or raster claim.
"""
import copy,json,re,subprocess
from pathlib import Path
import run_native_ending_audio_campaign_ram_v4511 as observed
ROOT,need,sha=observed.ROOT,observed.need,observed.sha
OUT=ROOT/'audit_v4515_native_ending_audio_window_checked'

def records(text,prefix):
    return [dict(re.findall(r'(\w+)=([^\s]+)',s)) for s in text.splitlines() if s.startswith(prefix+' ')]

def gate(text,baseline,meta,base_meta,fighter):
    reference=ROOT/('audit_v4485_kano_current_p2_campaign_ram' if fighter=='kano' else
                    'audit_v4440_sonya_kintaro_pressure_guard_long_p2_campaign')/'run.log'
    original=reference.read_text()
    prefix=lambda t,tag:records(t,'MK2_NAT_CAMPAIGN_'+tag)
    whole=lambda t:[s for s in t.splitlines() if s.startswith(('MK2_NAT_CAMPAIGN_','MK2_MILEENA_CAMPAIGN_',
                     'MK2_BOSS_KNIFE_','MK2_CAMPAIGN_GUEST_RAM_DIGEST ','MK2_CAMPAIGN_RAM_FRAME_DIGEST '))]
    need(whole(text)==whole(baseline)==whole(original),'All original full native campaign/guest/RGB records exactly equal qualified reference')
    starts=prefix(original,'ENDING_START');ends=prefix(original,'ENDING_COMPLETED');stops=prefix(original,'RESULT')
    need(len(starts)==len(ends)==len(stops)==1,'Exactly one qualified native owned ending and natural terminal')
    origin,attract,terminal=map(lambda r:int(r['frame']),(starts[0],ends[0],stops[0]))
    zero=[r for r in prefix(original,'HEALTH') if r['slot']=='1' and r['after']=='0' and int(r['frame'])<origin]
    final=max(zero,key=lambda r:int(r['frame']));window=int(final['frame'])
    identity=17 if fighter=='kano' else 18
    def one(tag):
        found=observed.rows(text,tag);need(len(found)==1,'One actual native audio '+tag);return found[0]
    w,b,e,result=(one(t) for t in ('WINDOW','BEGIN','ATTRACT','RESULT'))
    need(int(w['frame'])==int(w['window'])==window and w['pc']=='FF836700' and w['at']=='010602F0' and
         w['mask']=='FFFF' and w['after']=='0' and int(w['before'])>0 and int(w['identity'])==identity and
         all(w[k]==final[k] for k in ('before','after','pc','at','a8','a13')) and w['own_boss_winner_reads']=='1',
         'Actual final native source collision KO/task/register provenance before ending, never supplied window')
    need(int(b['frame'])==int(b['origin'])==origin and int(b['identity'])==identity and b['roster']==str(identity) and
         b['winner']=='2' and b['health']==starts[0]['health'] and b['actors']==starts[0]['actors']=='00000000,00000000',
         'Actual true own actor-retired ending BEGIN equals original native ending')
    need(int(e['frame'])==attract and int(e['origin'])==origin and int(e['age'])==attract-origin and
         e['mode']==ends[0]['mode']=='11' and e['roster']==ends[0]['roster'] and
         int(result['frame'])==terminal and int(result['window'])==window and int(result['origin'])==origin and
         int(result['attract'])==attract and terminal==attract+300,
         'Complete actual native ending/attract plus300 window, not shortened or host-timeout victory')
    fields=observed.rows(text,'FIELD')
    need([int(r['frame']) for r in fields]==list(range(window+1,terminal+1)),
         'Every final-KO/ending/attract field through original natural terminal')
    channels=observed.rows(text,'CHANNEL');pairs={(r['frame'],r['channel']) for r in channels}
    need(len(channels)==len(pairs)==len(fields)*14 and pairs=={(r['frame'],str(n)) for r in fields for n in range(14)},
         'All fourteen actual sample channels in every consecutive field')
    need(all(int(r['sample'])==0xffffffff and r['loop']==r['paused']=='0' for r in channels),
         'No active/looped/paused imported channel anywhere in ending/attract audio window')
    audio=records(text,'MK2_EAUDIO_PCM_DIGEST');base_audio=records(baseline,'MK2_EAUDIO_PCM_DIGEST')
    need(audio==base_audio and len(audio)==meta['mixedPCMUpdates']==base_meta['mixedPCMUpdates'] and
         sum(int(h['bytes']) for h in audio)==meta['mixedPCMBytesVerifiedInRAM']==base_meta['mixedPCMBytesVerifiedInRAM'] and
         meta['mixedPCMSHA256']==base_meta['mixedPCMSHA256'],
         'Every actual complete stereo PCM update/whole RAM waveform equal samples on/off')
    need(audio and all(h['bytes']=='3840' for h in audio) and
         0<=float(audio[0]['seconds'])-float(w['seconds'])<.02000001 and
         0<=float(result['seconds'])-float(audio[-1]['seconds'])<.02000001 and
         all(abs(float(y['seconds'])-float(x['seconds'])-.02)<1e-8 for x,y in zip(audio,audio[1:])),
         'Actual50Hz full stereo update clock covers final native KO through natural terminal')
    need(not any('hex=' in s for s in text.splitlines()),'No raw native PCM/guest/RGB on disk')
    for tag in ('WINDOW','BEGIN','WINNER','ATTRACT','FIELD','ROUTE','QUEUE','PACKET','SOUND','DELIVERY','RESULT'):
        need(observed.rows(text,tag)==observed.rows(baseline,tag),'Exact paired native '+tag+' inventory')
    sound=observed.rows(text,'SOUND');delivery=observed.rows(text,'DELIVERY')
    writes=[r for r in sound if r['pc'] in ('FFA13C90','FFA13D60')]
    need(writes,'Actual ending/attract native DCS commands, not only a silent successful exit')
    delivered=[]
    for i,r in enumerate(writes):
        first=float(r['seconds']);last=float(writes[i+1]['seconds']) if i+1<len(writes) else first+.1
        hits=[d for d in delivery if first<=float(d['seconds'])<last and int(d['word'],16)==int(r['word'],16)&255]
        need(hits,'Every actual native ending sound byte delivered to DCS before following port write')
        delivered.append(dict(write=r,dspRead=hits[0]))
    return dict(passed=True,fighter=fighter,physicalSlot=2,identity=identity,window=window,ending=origin,attract=attract,
                terminal=terminal,consecutiveNativeFields=len(fields),actualChannelStates=len(channels),
                nativePCMUpdates=len(audio),wholeNativePCMBytes=meta['mixedPCMBytesVerifiedInRAM'],
                wholeNativePCMSHA256=meta['mixedPCMSHA256'],nativeDeliveredBytes=delivered,
                completeActualEndingAttractMixedPCMNoImportedContributionAccepted=True,
                independentOriginalDCSWaveformReferenceAccepted=False,fullEndingTransitionRasterAccepted=False,fullPortAcceptance=False)

def change(text,prefix,frame,key,value):
    lines=text.splitlines();matches=[i for i,s in enumerate(lines) if s.startswith(prefix+f' frame={frame} ')]
    need(matches,'Actual observed field for counterexample')
    i=matches[0];before=lines[i];lines[i],count=re.subn(r'\b'+key+r'=[^\s]+',key+'='+str(value),before,count=1)
    need(count==1 and lines[i]!=before,'Non-vacuous actual field mutation')
    return '\n'.join(lines)+'\n'

def main():
    need(not OUT.exists(),'Fresh actual new audio qualification')
    path=observed.OUT/'report.json';proof=json.loads(path.read_text())
    need(proof['passed'] and proof['newEndingNativePCMWindowObservationsAccepted'],'Four actual terminal RAM audio observations passed first')
    pins=dict(proof['inputHashes']);pins[str(path)]=sha(path);pins[str(Path(__file__).resolve())]=sha(__file__)
    need(all(sha(p)==h for p,h in pins.items()),'All actual sources/compiled/native evidence unchanged')
    cases=[]
    for case in proof['cases']:
        folder,base=Path(case['capture']),Path(case['baseline'])
        text=(folder/'run.log').read_text();baseline=(base/'run.log').read_text()
        meta=json.loads((folder/'result.json').read_text());base_meta=json.loads((base/'result.json').read_text())
        positive=gate(text,baseline,meta,base_meta,case['fighter']);faults=[]
        def reject(label,bad):
            try:gate(bad,baseline,meta,base_meta,case['fighter'])
            except ValueError as error:faults.append(dict(label=label,rejectedBy=str(error)))
            else:raise ValueError('Actual complete audio window counterexample accepted '+label)
            need(gate(text,baseline,meta,base_meta,case['fighter'])==positive,'Exact whole positive restored after every audio-window fault')
        for tag,frame,key,value in (('WINDOW',positive['window'],'pc','FFF00000'),
                                   ('WINDOW',positive['window'],'before',0),
                                   ('BEGIN',positive['ending'],'identity',0),
                                   ('ATTRACT',positive['attract'],'roster','0,17'),
                                   ('CHANNEL',positive['window']+1,'sample',7)):
            reject(tag+':'+key,change(text,'MK2_EAUDIO_'+tag,frame,key,value))
        field=next(s for s in text.splitlines() if s.startswith('MK2_EAUDIO_FIELD '))
        reject('missing_consecutive_audio_field',text.replace(field+'\n','',1))
        pcm=next(s for s in text.splitlines() if s.startswith('MK2_EAUDIO_PCM_DIGEST '))
        reject('missing_complete_native_PCM_update',text.replace(pcm+'\n','',1))
        frame=int(dict(re.findall(r'(\w+)=([^\s]+)',pcm))['frame'])
        reject('wrong_actual_PCM_update_hash',change(text,'MK2_EAUDIO_PCM_DIGEST',frame,'sha256','0'*64))
        d=next(s for s in text.splitlines() if s.startswith('MK2_EAUDIO_DELIVERY '))
        reject('missing_actual_DCS_read',text.replace(d+'\n','',1))
        positive['actualAudioWindowFaultsRejected']=faults;cases.append(positive)
    need({c['fighter'] for c in cases}=={'kano','sonya'},'Both real character/slot ending contexts')
    need(all(sha(p)==h for p,h in pins.items()),'Every actual proof/source byte unchanged after complete positive/fault gates')
    report=dict(passed=True,candidate=observed.NAME,cases=cases,inputHashes=pins,
                currentBothP2CompleteEndingAttractMixedPCMNoImportedContributionAccepted=True,
                independentOriginalDCSWaveformReferenceAccepted=False,allEndingAudioFidelityAccepted=False,
                fullEndingTransitionRasterAccepted=False,fullPortAcceptance=False,scope=__doc__)
    OUT.mkdir();need(subprocess.run(['compact.exe','/C','/I','/Q','/S:'+str(OUT)],capture_output=True).returncode==0,
                    'Audio proof compressed before writes')
    (OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k not in ('inputHashes','cases')},indent=2),flush=True)
    print(json.dumps([{k:v for k,v in c.items() if k not in ('nativeDeliveredBytes',)} for c in cases],indent=2),flush=True)

if __name__=='__main__':main()
