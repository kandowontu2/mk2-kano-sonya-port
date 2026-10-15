"""Actual Scorpion-secondary PCM/DCS observation, unchanged earned controls.

Guest, PCM and original RGB transfers are RAM-only. This first paired context
establishes an actual inventory; it does not assert independent waveform,
voice/caller/source fidelity or universal finisher/port acceptance.
"""
import argparse,hashlib,inspect,json,re,subprocess,traceback
from pathlib import Path
import numpy as np
import run_jax_arms_native_audio_routes_v4212 as previous
import run_current_scorpion_secondary_state_v4549 as state
ROOT,need,sha,NAME=previous.ROOT,previous.need,previous.sha,previous.NAME
LUA='mk2ks_scorpion_secondary_audio_ram_v4657.lua'
PREFLIGHT=ROOT/'audit_v4660_scorpion_secondary_audio_source_checked/report.json'

def collector_source():
    text=inspect.getsource(previous.capture)
    def once(before,after):
        nonlocal text
        need(text.count(before)==1,'Unique whole4212 collector adaptation '+before[:65])
        text=text.replace(before,after)
    once('audit_v4213_jax_arms_{fighter}_p{side}_audio_queue_{suffix}',
         'audit_v4661_scorpion_secondary_{fighter}_p{side}_audio_{suffix}')
    once("lua='mk2ks_jax_arms_audio_routes_ram_v4210.lua'",'lua=LUA')
    once("controller='mk2ks_stock_extended_earned_ram_v3958.lua'",
         "controller='mk2ks_scorpion_secondary_state_ram_v4534.lua'")
    once("Path(state.old.__file__),Path(state.scene_state.__file__)",
         "Path(state.__file__),Path(state.source.__file__),ROOT/state.source.CONTROL,ROOT/'mk2ks_jax_arms_audio_routes_ram_v4210.lua',Path(previous.__file__),ROOT/'tools/qualify_scorpion_secondary_audio_source_v4659.py',PREFLIGHT")
    once("MK2KS_STOCK_KILLER='jax',MK2KS_STOCK_COMMAND='bbbb_lp',MK2KS_STOCK_GAP='96'",
         "MK2KS_STOCK_KILLER='scorpion',MK2KS_STOCK_COMMAND='dfff_hp_release',MK2KS_STOCK_GAP='64'")
    once('chunks=[];headers=[];guest_sha=None','chunks=[];headers=[];guest_sha=None;state_guest=None;rgb=[]')
    marker="                else:\n                    need('hex='not in line,'No raw audio or ROM encoded data written to disk');log.write(line)"
    insertion="""                elif line.startswith(('MK2_SSECOND_GUEST ','MK2_SSECOND_RGB ')):
                    h=dict(re.findall(r'(\\w+)=([^\\s]+)',line));raw=bytes.fromhex(h.pop('hex'))
                    if line.startswith('MK2_SSECOND_GUEST '):
                        need(state_guest is None and h==dict(frame='1',bytes='1048576')and raw==guest,'Every independent physical-state whole guest byte exact in RAM')
                        state_guest=hashlib.sha256(raw).hexdigest().upper();h['sha256']=state_guest
                    else:
                        need(h['width']=='400'and h['height']=='254'and len(raw)==int(h['bytes'])==406400,'Entire unchanged physical-controller RGB transport in RAM')
                        h['sha256']=hashlib.sha256(raw).hexdigest().upper();rgb.append(h)
                    log.write(line.split(' ',1)[0]+'_DIGEST '+' '.join(f'{k}={v}'for k,v in h.items())+'\\n')
"""
    once(marker,insertion+marker)
    once('rawAudioRasterVRAMROMCopiesWritten=0,assistance=',
         'stateGuestSHA256=state_guest,nativeRGBFramesDigested=len(rgb),rawAudioRasterVRAMROMCopiesWritten=0,assistance=')
    once("need(code==0 and guest_sha and headers and not re.search(",
         "need(code==0 and state_guest==guest_sha and len(rgb)==62 and headers and not re.search(")
    once("    return folder,headers,np.frombuffer(pcm,dtype='<i2').reshape(-1,2).copy()",
         "    (folder/'native_rgb_digests.json').write_text(json.dumps(rgb,indent=2)+'\\n')\n    return folder,headers,np.frombuffer(pcm,dtype='<i2').reshape(-1,2).copy()")
    return text

def capture(fighter,side,enabled,guest):
    import qualify_scorpion_secondary_audio_source_v4659 as source
    source.boundary();preflight=json.loads(PREFLIGHT.read_text())
    need(preflight['passed']and all(sha(p)==h for p,h in preflight['inputHashes'].items()),'Qualified actual audio/control sources unchanged before boot')
    scope=dict(vars(previous),__file__=__file__,previous=previous,state=state,LUA=LUA,PREFLIGHT=PREFLIGHT)
    exec(compile(collector_source(),__file__+'::whole4212_RAM_only_secondary_capture','exec'),scope)
    need(scope['capture'].__globals__['state'] is state,'Actual whole state gate module binding')
    return scope['capture'](fighter,side,enabled,guest)

def selected(text):
    return [line for line in text.splitlines()if line.startswith(('MK2_STOCK_HEAD_V921_','MK2_SSECOND_'))]

def pair(fighter,side):
    guest=state.source.current.expected()
    f,h,a=capture(fighter,side,True,guest)
    b,oh,ba=capture(fighter,side,False,guest)
    t=(f/'run.log').read_text();bt=(b/'run.log').read_text()
    reference=ROOT/f'audit_v4552_scorpion_secondary_{fighter}_p{side}_native_state_ram'
    need(selected(t)==selected(bt)==selected((reference/'run.log').read_text()),
         'Every original input/health/KO/cooperative/retirement/whole guest/62RGB event byte-exact versus cold native state')
    physical=state.contract(t,fighter,side);need(physical==state.contract(bt,fighter,side),'Entire original physical state contract retained')
    need(h==oh and a.shape==ba.shape and np.array_equal(a,ba)and np.any(a!=0),
         'Every complete actual native PCM update and full non-silent stereo waveform equal samples on/off')
    rows=lambda tag:previous.rows(t,tag)
    for tag in ('BEGIN','ROUTE','QUEUE','PACKET','SOUND','DELIVERY','RESULT'):
        need(rows(tag)==previous.rows(bt,tag),'Whole actual native audio '+tag+' inventory identical on/off')
    begin,end=rows('BEGIN'),rows('RESULT');origin=physical['actualNativeActivation']
    own=state.rows(t,'MK2_SSECOND_','BEGIN')[0];terminal=state.rows(t,'MK2_SSECOND_','RESULT')[0]
    need(len(begin)==len(end)==1 and begin[0]['origin']==end[0]['origin']==str(origin)and
         begin[0]['a8']==own['actor']and begin[0]['a13']==own['main']and begin[0]['id']=='10'and
         end[0]['frame']==terminal['frame']and int(end[0]['frame'])>origin+960,
         'Actual audio origin bound to earned Scorpion10 task, distinct real controller terminal')
    need(all(int(r['bytes'])==3840 for r in h)and
         all(abs(float(y['seconds'])-float(x['seconds'])-.02)<1e-9 for x,y in zip(h,h[1:]))and
         int(h[0]['frame'])in(origin,origin+1)and int(h[-1]['frame'])in(origin+748,origin+749),
         'Every consecutive actual50Hz sound update across complete original750-field audio window')
    expected={(frame,n)for frame in range(origin+1,origin+750)for n in range(14)}
    channels=[]
    for observed in(t,bt):
        ledger=previous.rows(observed,'CHANNEL')
        need(len(ledger)==len(expected)and {(int(r['frame']),int(r['channel']))for r in ledger}==expected,
             'Every14 sample channels in all749 real callbacks, none missing or duplicated')
        channels.append(dict(allIdle=all(int(r['sample'])==0xffffffff and r['loop']==r['paused']=='0'for r in ledger),
                             activeStates=[r for r in ledger if int(r['sample'])!=0xffffffff]))
    writes,deliveries,packets=rows('SOUND'),rows('DELIVERY'),rows('PACKET');matched=[]
    need(packets and len(writes)==2*len(packets)and [r['pc']for r in writes]==['FFA13C90','FFA13D60']*len(packets),
         'Every real original high/low DCS packet write, no phantom import marker')
    for i,packet in enumerate(packets):
        high,low=writes[i*2:i*2+2];word=int(packet['a3'],16)
        need(tuple(int(r['word'],16)&255 for r in (high,low))==(word>>8,word&255)and
             float(packet['seconds'])<float(high['seconds'])<float(low['seconds'])and
             all(r['a8']==packet['a8']and r['a13']==packet['a13']and r['frame']==packet['frame']and r['mask']=='FFFF'for r in (high,low)),
             'Every actual native full packet bound to both exact owned writes')
    for i,w in enumerate(writes):
        first=float(w['seconds']);last=float(writes[i+1]['seconds'])if i+1<len(writes)else first+.1
        hits=[r for r in deliveries if first<=float(r['seconds'])<last and int(r['word'],16)==int(w['word'],16)&255]
        need(hits,'Every actual DCS byte read before next native write');matched.append(dict(write=w,dspRead=hits[0]))
    pins={str(Path(__file__).resolve()):sha(__file__)}
    for folder in(f,b,reference):
        meta=json.loads((folder/'result.json').read_text())
        for p,digest in meta['input_hashes'].items():
            need(p not in pins or pins[p]==digest,'Consistent executed native/audio/state inputs');pins[p]=digest
        for p in folder.rglob('*'):
            if p.is_file():pins[str(p)]=sha(p)
    need(all(sha(p)==v for p,v in pins.items()),'Every executed source/native evidence byte unchanged')
    return dict(passed=True,candidate=NAME,fighter=fighter,side=side,capture=str(f),baseline=str(b),
                state=physical,nativeAudioOrigin=origin,actualNativeStop=int(terminal['frame']),
                actualPCMUpdates=len(h),actualStereoFrames=len(a),nonzeroSamples=int(np.count_nonzero(a)),
                completeMixedPCMEqualSamplesOnOff=True,everyOriginalColdStateAndRGBEventUnchanged=True,
                importedChannels=channels,nativeDeliveredBytes=len(matched),nativePackets=packets,
                actualRoutes=rows('ROUTE'),actualQueues=rows('QUEUE'),actualDelivery=matched,inputHashes=pins,
                sourceQualifiedVoiceEffectCallerFidelity=False,stockWholeWaveformReferenceAccepted=False,
                allVictimFinisherAudioAccepted=False,fullPortAcceptance=False,rawMediaFilesWritten=0,scope=__doc__)

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--fighter',choices=('kano','sonya'),required=True)
    parser.add_argument('--side',type=int,choices=(1,2),required=True);args=parser.parse_args()
    out=ROOT/f'audit_v4662_scorpion_secondary_{args.fighter}_p{args.side}_audio_observed'
    need(not out.exists(),'Fresh immutable paired audio observation')
    try:report=pair(args.fighter,args.side)
    except Exception as error:report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
    out.mkdir();need(subprocess.run(['compact.exe','/C','/I','/Q','/S:'+str(out)],capture_output=True).returncode==0,'Compressed before writes')
    (out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items()if k not in('inputHashes','actualRoutes','actualQueues','actualDelivery','nativePackets')},indent=2),flush=True)
    raise SystemExit(0 if report['passed']else 1)
