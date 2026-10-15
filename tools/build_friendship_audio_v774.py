"""Lossless baseline-subtracted original Friendship audio and channel oracle.

Keeps original hardware delivery-to-audio latency and tails, with no fades or
creative gain changes. Mono samples compensate only the port's 0.70 route.
Original hardware-only probes are not port gameplay acceptance.
"""
import argparse,hashlib,json,re,struct,wave
from pathlib import Path
import numpy as np

VARIANTS=(('kano_bubble_pop',0x6e),('sonya_chicken_a5',0xa5),
          ('sonya_chicken_aa',0xaa),('sonya_chicken_af',0xaf),('sonya_chicken_96',0x96))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest().upper()
def check(ok,msg):
    if not ok:raise ValueError(msg)
def audio(p):
    with wave.open(str(p),'rb')as w:
        check((w.getframerate(),w.getnchannels(),w.getsampwidth())==(48000,2,2),'Original PCM format')
        return np.frombuffer(w.readframes(w.getnframes()),'<i2').reshape(-1,2).astype(np.int32)
def build(root,out,samples):
    check(not out.exists(),'Do not overwrite proof')
    tracked={};rows={};deltas={};time=None
    def track(p,wanted=None):
        h=sha(p);check(wanted is None or h==wanted,'Input changed: '+str(p));tracked[str(p.resolve())]=h
    track(Path(__file__))
    commands=['baseline','006e']+[f'{base+ch:04x}'for base in(0xa5,0xaa,0xaf,0x96)for ch in range(5)]
    for cmd in commands:
        folder=root/f'audit_v772_original_friendship_isolated_{cmd}'
        result=json.loads((folder/'result.json').read_text(encoding='utf-8-sig'))
        check(result['exit_code']==0 and result['command']==cmd and result['guest_ram_writes']==0 and result['assistance']=='DCS_sound_port_only','Nonterminal/wrong original capture')
        for p,h in result['input_hashes'].items():track(Path(p),h)
        for name in('result.json','run.log','native_mix.wav'):track(folder/name)
        track(folder/'native_mix.wav',result['mix_sha256'])
        rows[cmd]=audio(folder/'native_mix.wav')
        if cmd!='baseline':
            log=(folder/'run.log').read_text(encoding='utf-8-sig')
            check(f'command={cmd.upper()}'in log,'Requested hardware command missing')
            times=re.findall(r'MK3_FRIEND_ISOLATED_TIME frame=\d+ seconds=([\d.]+) address=01680000 data=([\dA-F]{4}) mask=00FF',log)
            check(len(times)==2 and [int(x[1],16)for x in times]==[int(cmd,16)>>8,int(cmd,16)&255],'Actual two hardware bytes')
            start=float(times[0][0]);check(abs(float(times[1][0])-start-0.000025)<1e-9,'Original DCS byte interval')
            check(time is None or time==start,'Time-aligned captures required');time=start
    baseline=rows['baseline'];start=round(time*48000)
    for cmd in commands[1:]:
        check(rows[cmd].shape==baseline.shape,'Baseline duration')
        delta=rows[cmd]-baseline
        check(not np.any(delta[:start]),'Difference before hardware delivery')
        check(np.array_equal(delta[:,0],delta[:,1]),'Original stereo not dual mono')
        deltas[cmd]=delta[:,0]
    for base in(0xa5,0xaa,0xaf,0x96):
        check(all(np.array_equal(deltas[f'{base:04x}'],deltas[f'{base+ch:04x}'])for ch in range(5)),'Native channel variants not identical')
    original=root/'mk3/mk3-maincpu.bin';track(original);rom=original.read_bytes()
    source_tables={}
    for at,wanted in((0xffaa65d0,[0x006e1f21]*2),(0xffaa6ad0,[0x00a51010,0x00aa1017,0x00af1014,0x00961012])):
        got=list(struct.unpack_from('<'+'I'*len(wanted),rom,(at-0xff800000)//8))
        check(got==wanted,'Original sound tables changed');source_tables[f'{at:08X}']=got
    assets={}
    for name,command in VARIANTS:
        delta=deltas[f'{command:04x}'];nz=np.flatnonzero(delta)
        check(len(nz)>0 and nz[0]>=start,'Missing original audio')
        end=int(nz[-1])+3
        check(not np.any(delta[end:]),'Tail cropped')
        raw=delta[start:end];scaled=np.rint(raw/.70)
        check(np.max(np.abs(scaled))<32767,'Sample clipping')
        pcm=scaled.astype('<i2')
        check(np.max(np.abs(pcm.astype(float)*.70-raw))<=.35+1e-8,'Route compensation not reversible')
        asset=samples/(name+'.wav');check(not asset.exists(),'Do not overwrite sample '+str(asset))
        assets[name]={'command':command,'hardware_seconds':time,'first_pcm_delay_seconds':(int(nz[0])-start)/48000,
                     'frames':len(pcm),'original_peak':int(np.max(np.abs(raw))),
                     'source_pcm_sha256':hashlib.sha256(raw.astype('<i2').tobytes()).hexdigest().upper(),
                     'route':.70,'native_channel_variants':5 if command!=0x6e else 1,'file':str(asset.resolve())}
        samples.mkdir(parents=True,exist_ok=True)
        with wave.open(str(asset),'wb')as w:w.setparams((1,2,48000,0,'NONE','not compressed'));w.writeframes(pcm.tobytes())
        track(asset);assets[name]['sha256']=sha(asset)
    out.mkdir(parents=True)
    report={'scope':__doc__,'checked_inputs':tracked,'original_sound_tables':source_tables,'assets':assets,
            'all_20_cluck_channel_commands_pcm_identical_within_variant':True,'fullPortAcceptance':False}
    (out/'verification.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({'assets':len(assets),'checked_inputs':len(tracked),'fullPortAcceptance':False}))
if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('root',type=Path);p.add_argument('output',type=Path);p.add_argument('samples',type=Path)
    a=p.parse_args();build(a.root,a.output,a.samples)
