"""Original-audio fidelity, native cue/voice allocation and audible overlap.

Bounded human Friendship audio acceptance only, not whole-port release QA.
"""
import argparse,hashlib,json,struct,wave
from pathlib import Path
import numpy as np
import verify_native_friendship_dispatch_v778 as scene
from build_friendship_audio_v774 import VARIANTS

HOLDS=(16,23,20,18)
def check(ok,msg):
    if not ok:raise ValueError(msg)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest().upper()
def audio(p):
    with wave.open(str(p),'rb')as w:
        check(w.getframerate()==48000 and w.getsampwidth()==2,'Expected 48k s16 PCM')
        return np.frombuffer(w.readframes(w.getnframes()),'<i2').reshape(-1,w.getnchannels()).astype(np.float64).mean(axis=1)
def guest_audio(old,new):
    check(len(old)==len(new)==0x100000,'Complete guest required')
    expected=bytearray(old)
    for first,last in((0xf9a00,0xf9e00),(0xfa200,0xfa700)):expected[first:last]=new[first:last]
    check(new==expected,'Audio edit changed unrelated guest state/tables')
    cycle=(7,8,9,10,9,8,7,6,5,4,3,4,5,6)
    for first,indices in((0xfa200,range(14)),(0xfa2e0,range(3)),(0xfa320,range(3,14))):
        words=[]
        for i in indices:
            words.extend((6,scene.BASE+0xfa480*8))
            if i in(2,4,6):words.extend((6,scene.BASE+0xfa580*8))
            words.append(scene.art.SONYA_BODY[cycle[i]]-0x1000000)
        words.append(0)
        check(struct.unpack_from('<'+'I'*len(words),new,first)==tuple(words),'Native sound/pose callback stream changed')
    check(struct.unpack_from('<8H',new,0xfa440)==(16,0x6aa0,23,0x6aa5,20,0x6aaa,18,0x6aaf),'Original hold/variant table changed')
    check(struct.pack('<3H',0x0d5f,0xeae0,0xff80)in new[0xfa580:0xfa700],'No original native 1..4 RNG call')
    check(struct.pack('<6H',0x09e0,0x6ab4,0,0x0580,0x1030,0x01d0)in new[0xf9a00:0xf9c00],'Missing explicit bubble pop dispatch')
    return sum(x!=y for x,y in zip(old,new))
def runtime(rows,winner,side,case):
    scene.runtime(rows,winner,side,case)
    cues=scene.select(rows,'AUDIO');result=scene.select(rows,'RESULT')[0]
    if case!='positive':
        check(not cues,'Friendship sound on rejected/ordinary gameplay')
        return{'cues':0}
    action=int(result['action']);fid=17 if winner=='kano'else 18
    poses=scene.select(rows,'POSE');actor=poses[0]['actor'];main=poses[0]['main']
    check(all(int(c['id'])==fid and c['actor']==actor and c['main']==main for c in cues),'Audio belongs to wrong actor/task')
    if winner=='kano':
        check(len(cues)==1 and int(cues[0]['command'],16)==0x6ab4 and int(cues[0]['frame'])-action==183,'Pop is not at the native burst phase')
        check(cues[0]['pose']=='FE9D2590','Pop changed Kano body state')
        return{'cues':1,'ages':[183],'variants':[0x6e]}
    tail=[p for p in poses if int(p['age'])>=83]
    expected=[int(p['frame'])for i,p in enumerate(tail)if i%14 in(2,4,6)]
    check([int(c['frame'])for c in cues]==expected,'Three chicken cues/cycle missing, late, early or outside scene')
    check(len(cues)>=9,'Insufficient repeated overlap')
    timers=[0]*5;last=action;variants=[];voices=[]
    for c in cues:
        frame=int(c['frame']);timers=[max(0,t-(frame-last))for t in timers];last=frame
        command=int(c['command'],16);check(0x6aa0<=command<=0x6ab3,'Command collides with native sign-extended bytes')
        variant,voice=divmod(command-0x6aa0,5)
        check(voice==timers.index(0),'Not original first-free independent voice allocation')
        timers[voice]=HOLDS[variant]
        check([int(x)for x in c['timers'].split(',')]==timers,'Native hold timers or overlap changed')
        age=frame-action
        phase=(age-83)//3%14
        check(c['pose']==f'{scene.art.SONYA_BODY[(7,8,9,10,9,8,7,6,5,4,3,4,5,6)[phase-1]]-0x1000000:08X}','Callback no longer immediately precedes its original pose')
        variants.append(variant);voices.append(voice)
    check(max(voices)>=2,'Overlapping clucks collapsed onto one voice')
    return{'cues':len(cues),'ages':[int(c['frame'])-action for c in cues],'variants':variants,'voices':voices}

def fit_overlap(y,starts,clips,other_events=()):
    """Fit all coexisting original voices, allowing <=4 output sample rounding.

    MAME start() updates at a fractional PCM time; no field-scale search or
    unrestricted timing shift is allowed. Gains must retain source loudness.
    """
    check(len(starts)==len(clips)>0,'No audible cues')
    origin=min(starts)-8
    n=max(s+len(x)for s,x in zip(starts,clips))-origin+8
    starts=list(starts);clips=list(clips)
    for first,clip in other_events:
        if first+len(clip)>origin-4 and first<origin+n+4:
            starts.append(first);clips.append(clip)
    observed=y[origin:origin+n]
    check(len(observed)==n,'Truncated recorded audio')
    a=np.zeros((n,len(clips)));offsets=[0]*len(clips)
    def col(j,k):
        out=np.zeros(n);first=starts[j]+k-origin
        dst=max(0,first);src=max(0,-first);count=min(n-dst,len(clips[j])-src)
        if count>0:out[dst:dst+count]=clips[j][src:src+count]
        return out
    for j in range(len(clips)):a[:,j]=col(j,0)
    for _ in range(2):
        for j in range(len(clips)):
            best=None
            for shift in range(-4,5):
                a[:,j]=col(j,shift);g=np.linalg.lstsq(a,observed,rcond=None)[0]
                mse=float(np.mean((a@g-observed)**2))
                if best is None or mse<best[0]:best=(mse,shift)
            offsets[j]=best[1];a[:,j]=col(j,best[1])
    gain=np.linalg.lstsq(a,observed,rcond=None)[0];pred=a@gain
    energy=np.dot(observed,observed)*np.dot(pred,pred)
    check(energy>0,'Friendship samples inaudible')
    correlation=float(np.dot(observed,pred)/np.sqrt(energy))
    rms=float(np.sqrt(np.mean((observed-pred)**2)))
    check(np.all((gain>.98)&(gain<1.02)),f'Source waveform gain or voice missing: gains={gain.tolist()} correlation={correlation:.8f} rms={rms:.3f} offsets={offsets}')
    check(correlation>.9995 and rms<2,f'Wrong waveforms, lost tails or overlapping voice restarted: correlation={correlation:.8f} rms={rms:.3f} offsets={offsets}')
    return{'offset_pcm_samples':offsets,'gains':gain.tolist(),'correlation':correlation,'residual_rms_pcm':rms}

def existing_sample(root,command):
    """Reproduce the unchanged MAME samples.cpp linear interpolation.

    Include existing winner announcements in the model rather than treating
    them as Friendship noise or weakening the audible fidelity gate.
    """
    names={0xfffc:'kano_select',0xfffb:'sonya_select',0xfffe:'kano_wins',0xfffd:'sonya_wins',
           0xfffa:'sonya_kiss',0xfff9:'kano_extract',0xfff8:'sonya_burn_fire',0xfff7:'sonya_burn_victim'}
    with wave.open(str(root/f'samples/mk2ks/{names[command]}.wav'),'rb')as w:
        rate=w.getframerate();check(w.getnchannels()==1 and w.getsampwidth()==2,'Existing sample format')
        x=np.frombuffer(w.readframes(w.getnframes()),'<i2').astype(float)
    count=int(np.ceil(len(x)*48000/rate))
    # Repeated double additions match chan.pos, including rounding immediately
    # below integer source indexes. Closed-form arange/rate is not equivalent
    # to this implementation's two-index interpolation at those boundaries.
    positions=np.cumsum(np.r_[0.,np.full(count-1,rate/48000)])
    indexes=np.floor(positions).astype(int);fractions=positions-indexes
    # samples.cpp increments ipos before calculating its second source index.
    interpolated=x[indexes]*(1-fractions)+x[(indexes+2)%len(x)]*fractions
    interpolated[-1]=0 # native non-loop ending fills from the final sample
    return interpolated*(.21 if command>=0xfffb else .70)

def main(root,out):
    check(not out.exists(),'Do not overwrite proof');tracked={};reports={}
    def track(p,wanted=None):
        actual=sha(p);check(wanted is None or wanted==actual,'Input changed: '+str(p));tracked[str(p.resolve())]=actual
    track(Path(__file__));track(Path(scene.__file__))
    asset_proof=root/'audit_v774_original_friendship_audio_checked/verification.json';track(asset_proof)
    proof=json.loads(asset_proof.read_text())
    check(proof['all_20_cluck_channel_commands_pcm_identical_within_variant'],'Original channel oracle absent')
    for p,h in proof['checked_inputs'].items():track(Path(p),h)
    baseline=audio(root/'audit_v772_original_friendship_isolated_baseline/native_mix.wav')
    templates={}
    for name,cmd in VARIANTS:
        path=root/f'samples/mk2ks/{name}.wav';track(path)
        source=audio(root/f'audit_v772_original_friendship_isolated_{cmd:04x}/native_mix.wav')-baseline
        metadata=proof['assets'][name];start=round(metadata['hardware_seconds']*48000)
        nz=np.flatnonzero(source);original=source[start:int(nz[-1])+3]
        clip=audio(path)
        check(len(clip)==len(original)and np.max(np.abs(clip*.7-original))<=.350001,'Sample differs from complete original DCS delta')
        if cmd!=0x6e:
            for ch in range(5):
                other=audio(root/f'audit_v772_original_friendship_isolated_{cmd+ch:04x}/native_mix.wav')-baseline
                check(np.array_equal(source,other),'Channel commands no longer identical')
        templates[cmd]=clip*.7
    scene_proof=root/'audit_v778_native_friendship_dispatch_checked/verification.json';track(scene_proof)
    prior=json.loads(scene_proof.read_text());check(prior['boundedHumanFriendshipDispatchAcceptance'],'Current scene not accepted')
    for p,h in prior['checked_inputs'].items():track(Path(p),h)
    old_guest=root/'audit_v768_kano_friendship_p1/guest_maincpu.bin'
    old_proof=json.loads((root/'audit_v769_native_friendship_dispatch_checked/verification.json').read_text())
    track(old_guest,old_proof['checked_inputs'][str(old_guest.resolve())]);old=old_guest.read_bytes()
    all_variants=set();total=0
    for winner in('kano','sonya'):
        for side,case in((1,'positive'),(2,'positive'),(1,'wrong_command'),(2,'punch_used')):
            suffix=f'{winner}_friendship_p{side}'if case=='positive'else f'{winner}_wrong_p1'if case=='wrong_command'else f'{winner}_punch_p2'
            folder=root/f'audit_v{780 if case=="positive"else 777}_{suffix}';result=json.loads((folder/'result.json').read_text(encoding='utf-8-sig'))
            check(result['exit_code']==0 and result['samples_enabled'],'Samples disabled or unfinished case')
            for p,h in result['input_hashes'].items():track(Path(p),h)
            track(folder/'native_mix.wav',result['mix_sha256'])
            rows=scene.parse(folder/'run.log');report=runtime(rows,winner,side,case)
            report['guest_audio_changed_bytes']=guest_audio(old,(folder/'guest_maincpu.bin').read_bytes())
            total+=report['cues']
            if case=='positive':
                silent=root/f'audit_v777_{winner}_baseline_p{side}'
                sr=json.loads((silent/'result.json').read_text(encoding='utf-8-sig'))
                check(sr['exit_code']==0 and not sr['samples_enabled']and sr['guest_writes']==0 and sr['assistance']=='none','Not a terminal physical-input baseline')
                for p,h in sr['input_hashes'].items():track(Path(p),h)
                for name in('result.json','run.log','guest_maincpu.bin'):track(silent/name)
                track(silent/'native_mix.wav',sr['mix_sha256'])
                check((silent/'guest_maincpu.bin').read_bytes()==(folder/'guest_maincpu.bin').read_bytes(),'Baseline guest differs')
                baseline_rows=scene.parse(silent/'run.log');runtime(baseline_rows,winner,side,'positive')
                check([(k,r)for k,r in rows if k!='VOICE']==baseline_rows,'Silent baseline gameplay/timing differs')
                earlier=root/f'audit_v777_{suffix}';previous=json.loads((earlier/'result.json').read_text(encoding='utf-8-sig'))
                check(result['mix_sha256']==previous['mix_sha256'],'Read-only extra voice tracing changed actual recorded mix')
                mix=audio(folder/'native_mix.wav');quiet=audio(silent/'native_mix.wav')
                check(mix.shape==quiet.shape,'Baseline mix duration differs')
                delta=mix-quiet;cues=scene.select(rows,'AUDIO');groups=[]
                other_events=[]
                for voice in scene.select(rows,'VOICE'):
                    cmd=int(voice['command'],16)
                    other_events.append((round(float(voice['seconds'])*48000),existing_sample(root,cmd)))
                track(root/'mame-mkp/src/devices/sound/samples.cpp')
                for first in range(0,len(cues),1 if winner=='kano'else 3):
                    group=cues[first:first+(1 if winner=='kano'else 3)]
                    commands=[0x6e if winner=='kano'else(0xa5,0xaa,0xaf,0x96)[(int(c['command'],16)-0x6aa0)//5]for c in group]
                    all_variants.update(commands)
                    try:groups.append(fit_overlap(delta,[round(float(c['seconds'])*48000)for c in group],[templates[c]for c in commands],other_events))
                    except ValueError as error:raise ValueError(f'{folder.name} group {first}: {error}')from error
                report['audible_groups']=groups
            reports[folder.name]=report
    check(all_variants=={0x6e,0xa5,0xaa,0xaf,0x96},'Not all original voices exercised')
    out.mkdir(parents=True)
    report={'scope':__doc__,'cases':reports,'checked_inputs':tracked,'audible_cues':total,
            'boundedHumanFriendshipAudioAcceptance':True,'fullFinisherAcceptance':False,'fullPortAcceptance':False}
    (out/'verification.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({'cases':len(reports),'audible_cues':total,'checked_inputs':len(tracked),'fullPortAcceptance':False}))
if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('root',type=Path);p.add_argument('output',type=Path);a=p.parse_args();main(a.root,a.output)
