"""Current Baraka full physical/pixel capture plus original native DCS/PCM.

No state writes or proxies; whole original921/1014 and exact5527 pixel gates.
Audio observer is whole3939 with only actual original Baraka action origin.
Paired native recordings stay in RAM, no duplicated ROM/EXE/build trees.
"""
import inspect,json,re,struct,traceback
from pathlib import Path
import numpy as np
import verify_current_baraka_pixels_v5527 as qualified

original=qualified.original
ROOT,need,sha=original.ROOT,original.need,original.sha
BASE=ROOT/'audit_v5534_current_baraka_audio_ram'
OUT=ROOT/'audit_v5535_current_baraka_audio_observation'
PARENT=ROOT/'audit_v5531_current_baraka_qualified_progress/progress.json'
LUA=ROOT/'mk2ks_current_baraka_audio_ram_v5532.lua'
COMPLETED=[]
save=original.save;digest=original.digest

source=inspect.getsource(original.transport.capture)
edits={
 'def capture(spec,guest,payload,expected_gfx,reference,pins,source_image):':
 'def capture(spec,guest,payload,expected_gfx,reference,pins,source_image,enabled):',
 "folder=BASE/f'{fighter}_p{side}'":"folder=BASE/f'{fighter}_p{side}_{\"samples\"if enabled else\"nosamples\"}'",
 'Cage victim context':'Baraka audio victim context',
 "MK2KS_STOCK_KILLER='cage',MK2KS_STOCK_COMMAND='ddff_lp'":"MK2KS_STOCK_KILLER='baraka',MK2KS_STOCK_COMMAND='bbbb_hp'",
 "'-samplepath',str(ROOT/'samples'),'-samples'":"'-samplepath',str(ROOT/'samples'),'-samples'if enabled else'-nosamples'",
 "'-video','none','-sound','none'":"'-video','none','-sound','none','-samplerate','48000'",
 'MK2_CURRENT_CAGE_RAM_':'MK2_CURRENT_BARAKA_RAM_',
 "killer='cage',command='ddff_lp'":"killer='baraka',command='bbbb_hp'",
 'native_torso_gfx.bin':'native_death_gfx.bin',
 'source-PNG torso graphics exact':'source-PNG head/body graphics exact',
 'actualNativeSectionPixelsAndScanout':'actualNativeHeadBodyPixelsAndScanout',
 'all six complete native section scanouts':'all fourteen complete native head/body scanouts',
 'ram,images,headers,buffers,gfx={},{},[],{},{}':
 'ram,images,headers,buffers,gfx={},{},[],{},{}\n    chunks=[];pcm_headers=[];audio_guest=None',
 "                if line.startswith('MK2_CURRENT_BARAKA_RAM_'):":
 """                if line.startswith(('MK2_BBAUDIO_PCM ','MK2_MAUDIO_GUEST ')):
                    tag=line.split()[0];r=dict(re.findall(r'(\\w+)=([^\\s]+)',line));raw=bytes.fromhex(r.pop('hex'))
                    need(len(raw)==int(r['bytes']),'Every complete native audio/guest transport buffer');r['sha256']=digest(raw)
                    if tag=='MK2_BBAUDIO_PCM':
                        need(len(raw)%4==0,'Complete stereo signed16 native PCM update');chunks.append(raw);pcm_headers.append(r)
                    else:
                        need(audio_guest is None and raw==guest,'Independent whole initialized audio-observed guest exact');audio_guest=raw
                    out.write(tag+'_DIGEST '+' '.join(k+'='+str(v)for k,v in r.items())+'\\n')
                elif line.startswith('MK2_CURRENT_BARAKA_RAM_'):""",
 "    final.update(passed=True,effectiveActualNativeRecordFaults=faults":
 """    pcm=b''.join(chunks)
    need(audio_guest==guest and pcm_headers and all(float(a['seconds'])<float(b['seconds'])for a,b in zip(pcm_headers,pcm_headers[1:])),
         'Whole initialized audio guest and complete chronological actual PCM capture')
    final.update(samplesEnabled=enabled,actualPCMUpdates=len(pcm_headers),actualPCMBytes=len(pcm),actualMixedPCMSHA256=digest(pcm),
                 allRequestedGuestMediaBuffersRAMOnly=True)
    final.update(passed=True,effectiveActualNativeRecordFaults=faults""",
 '    return final':
 '    return dict(final=final,folder=folder,log=log,ram=ram,images=images,pcmHeaders=pcm_headers,pcm=np.frombuffer(pcm,"<i2").reshape(-1,2).copy())',
}
for before,after in edits.items():
    need(source.count(before)==1,'Whole current capture only explicit audio transport/context addition: '+before)
    source=source.replace(before,after,1)
scope=dict(original.transport.__dict__,ROOT=ROOT,BASE=BASE,LUA=LUA,COMPLETED=COMPLETED,model=original.model,
    verify_pixels=qualified.verified,record_faults=original.record_faults,digest=digest,__file__=__file__)
exec(compile(source,__file__+'.entire5509_capture_current5527_Baraka_audio_transport','exec'),scope)
capture=scope['capture']


def rows(log,tag):
    return [dict(re.findall(r'(\w+)=([^\s]+)',line))for line in log.splitlines()if line.startswith('MK2_MAUDIO_'+tag+' ')]


def paired_observation(a,b,fighter,side,guest):
    need(a['final']['samplesEnabled']and not b['final']['samplesEnabled'],'Actual enabled/disabled pair')
    selected=lambda t:[line for line in t.splitlines()if line.startswith(('MK2_STOCK_HEAD_V921_','MK2_ROLLING_HEAD_V1003_','MK2_CURRENT_BARAKA_SCENE_'))]
    need(selected(a['log'])==selected(b['log']),'Every original physical/parser/palette/FIFO/ordered dispatch/display row unchanged by samples')
    need(a['ram']==b['ram']and a['images'].keys()==b['images'].keys()
         and all(np.array_equal(a['images'][key],b['images'][key])for key in a['images']),
         'Whole actual guest/GFX/each native palette/every whole displayed frame samples-on/off exact')
    timeline=lambda hs:[{k:v for k,v in h.items()if k!='sha256'}for h in hs]
    need(timeline(a['pcmHeaders'])==timeline(b['pcmHeaders'])and a['pcm'].shape==b['pcm'].shape,
         'Every actual whole sound interval and stereo sample aligned')
    need(np.array_equal(a['pcm'],b['pcm'])and np.any(a['pcm']),
         'Entire actual native non-silent PCM is samples-on/off byte exact, no phantom imported audio')
    for tag in('BEGIN','ROUTE','QUEUE','PACKET','SOUND','DELIVERY','RESULT'):
        need(rows(a['log'],tag)==rows(b['log'],tag),'Every native audio '+tag+' event unchanged by samples')
    begin=rows(a['log'],'BEGIN');end=rows(a['log'],'RESULT')
    action=[r for tag,r in original.model.original.records(a['log'],'MK2_STOCK_HEAD_V921')if tag=='ACTION'][0]
    need(len(begin)==len(end)==1 and begin[0]['id']=='3'and begin[0]['a8']==action['actor']and begin[0]['a13']==action['main']
         and begin[0]['frame']==action['frame']and end[0]['origin']==begin[0]['origin']and end[0]['frame']=='5198',
         'Audio origin is actual original Baraka action/task, full native terminal not early observation exit')
    origin=int(begin[0]['origin']);hs=a['pcmHeaders']
    need(int(hs[0]['frame'])in(origin,origin+1)and int(hs[-1]['frame'])==origin+749,
         'Whole original audio window through749fields, not truncated at animation completion')
    channels=rows(a['log'],'CHANNEL');disabled=rows(b['log'],'CHANNEL')
    for ledger in(channels,disabled):
        need(len(ledger)==14*749 and {(int(r['frame']),int(r['channel']))for r in ledger}==
             {(f,n)for f in range(origin+1,origin+750)for n in range(14)}and
             all(int(r['sample'])==0xffffffff and r['paused']==r['loop']=='0'for r in ledger),
             'Every actual imported voice/effect channel idle through complete native finisher window')
        for n in range(14):
            need(len({(r['length'],r['pos'])for r in ledger if int(r['channel'])==n})==1,
                 'Retained inactive source length/position never advances')
    need(all(r['length']=='0'and float(r['pos'])==0 for r in disabled),'Disabled channels never loaded an imported sample')
    writes=rows(a['log'],'SOUND');packets=rows(a['log'],'PACKET');delivery=rows(a['log'],'DELIVERY');matched=[]
    need(packets and len(writes)==2*len(packets)and [r['pc']for r in writes]==['FFA13C90','FFA13D60']*len(packets),
         'All genuine native high/low packet-store writes in exact original order')
    for i,packet in enumerate(packets):
        high,low=writes[2*i:2*i+2];word=int(packet['a3'],16)
        need(0<=word<=65535 and tuple(int(w['word'],16)&255 for w in(high,low))==(word>>8,word&255)
             and float(packet['seconds'])<float(high['seconds'])<float(low['seconds'])
             and all(w['mask']=='FFFF'and all(w[k]==packet[k]for k in('a8','a13','frame'))for w in(high,low)),
             'Every actual full dispatch packet/actor/task reaches exact two port bytes')
    for i,w in enumerate(writes):
        first=float(w['seconds']);last=float(writes[i+1]['seconds'])if i+1<len(writes)else first+.1
        hits=[d for d in delivery if first<=float(d['seconds'])<last and int(d['word'],16)==int(w['word'],16)&255]
        need(hits,'Every actual native port byte read by ADSP before the next write');matched.append(dict(write=w,dspRead=hits[0]))
    return dict(passed=True,fighter=fighter,side=side,origin=origin,terminal=5198,allOriginalPhysicalAndExactPixelGatesRetained=True,
        pairedWholeFramesExact=len(a['images']),completeNativePCMUpdates=len(hs),completeNativeStereoFrames=len(a['pcm']),
        nativePortBytesDelivered=len(matched),actualDeliveredBytes=matched,fullNativePCMOnOffExactlyEqual=True,
        trueVictimPainGenderAndFixedSourceCommandsAccepted=False,sourceQualifiedNativeDCSWaveformAccepted=False,
        completeBarakaFinisherAudioAccepted=False,fullPortAcceptance=False)


def run():
    guest=original.model.current.expected();parent=json.loads(PARENT.read_text())
    need(parent['passed']and parent['goalStatus']=='active','Qualified exact current native Baraka frontier retained')
    pins=dict(parent['newInputHashes']);pins[str(PARENT)]=sha(PARENT)
    for p in(Path(__file__),LUA,ROOT/'mk2ks_kitana_audio_queue_ram_v3939.lua',ROOT/'tools/verify_kitana_native_audio_queue_v3952.py'):
        pins[str(p.resolve())]=sha(p)
    need(all(sha(p)==h for p,h in pins.items()),'Current/public/controller/source/asset bytes unchanged before paired native captures')
    payload=(ROOT/original.model.current.NAME/'roms/mk2ks/mk2ks.mdata').read_bytes()
    reference,gfx=original.model.source_art(guest,payload,pins);image=original.transport.source_graphics(payload,pins)
    a=capture(('kano',1),guest,payload,gfx,reference,pins,image,True)
    b=capture(('kano',1),guest,payload,gfx,reference,pins,image,False)
    result=paired_observation(a,b,'kano',1,guest)
    return dict(passed=True,goalStatus='active',remaining=parent['remaining'],parentAdditiveJournal=str(PARENT),
        thisGoalTurnClassification='progress: actual current Baraka native PCM/port/ADSP observation paired enabled/disabled, preserving full original physical and exact rendered head/body gates',
        cases=[result],newNativeBoots=2,newBuilds=0,newDeletedFiles=0,publicPlayableChanged=False,refreshedReleaseZIP=False,
        allVictimSlotsAudioAccepted=False,completeBarakaFinisherAudioAccepted=False,fullPortAcceptance=False,newInputHashes=pins,
        nextAction='Independently decode native Baraka source callsites/command tables and true victim pain/gender/queue branches; retain actual paired observation, then qualify both victims and both slots and full waveform fidelity.')


if __name__=='__main__':
    need(not OUT.exists(),'Fresh immutable actual current Baraka audio observation')
    try:report=run()
    except Exception as error:report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),completedCases=COMPLETED,goalStatus='active',fullPortAcceptance=False)
    OUT.mkdir();save(OUT/'progress.json',report)
    print(json.dumps({k:v for k,v in report.items()if k not in('cases','completedCases','remaining','newInputHashes')},indent=2),flush=True)
    raise SystemExit(0 if report['passed']else 1)
