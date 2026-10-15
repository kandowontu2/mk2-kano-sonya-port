"""Current natural Pit state + contiguous rendered/audio capture inventory.

Non-silent synchronized PCM is NOT correct voices/audio or artistic acceptance.
Native whole-scene drawing, shake/foreground and authenticity still need checks.
"""
import argparse
import hashlib
import json
import re
import sys
import wave
from pathlib import Path
import numpy as np
from PIL import Image
import verify_native_pit_scene_v635_v1 as scene
from verify_native_candidate_v635 import matched

CASES={'audit_v672_current_pit_kano_p1':('kano',1),
       'audit_v672_current_pit_sonya_p2':('sonya',2)}


def rows(log,tag):
    return [dict(re.findall(r'(\w+)=([^\s]+)',line)) for line in log.splitlines()
            if line.startswith('MK2_PIT_DISPLAY_'+tag+' ')]


def inspect(folder,fighter,side):
    inputs={};matched(folder,inputs)
    log=(folder/'run.log').read_text(encoding='utf-8-sig')
    proof=scene.verify(folder,fighter,side=side)
    result=rows(log,'RESULT');snaps=rows(log,'SNAP');lookups=rows(log,'LOOKUP')
    scene.need(len(result)==1 and len(lookups)==2,'Complete single real Pit capture')
    origin=int(result[0]['origin'])
    scene.need(origin==proof['pit_enter'] and int(result[0]['last_lookup'])==proof['pit_impact'],
               'Actual native state and display origins agree')
    scene.need(int(result[0]['snapshots'])==len(snaps)==331 and
               [int(r['frame']) for r in snaps]==list(range(origin,origin+331)),
               'Every field of declared first Pit/display window retained, no dropped frames')
    seconds=[float(r['seconds']) for r in snaps]
    scene.need(all(a<b for a,b in zip(seconds,seconds[1:])),'Actual monotonically increasing emulator time')
    pictures=[]
    for row in snaps:
        path=folder/'snap'/row['file']
        with Image.open(path) as image:
            scene.need(image.size==(400,254),'Actual complete unscaled screen dimensions')
            image.load()
        pictures.append(dict(frame=int(row['frame']),seconds=float(row['seconds']),mode=int(row['mode']),file=row['file']))
    scene.need(any(r['mode']==9 for r in pictures) and any(r['mode']==5 for r in pictures),
               'Actual native Pit and post-impact modes both represented')
    with wave.open(str(folder/'native_audio.wav'),'rb') as wav:
        scene.need((wav.getnchannels(),wav.getsampwidth(),wav.getframerate())==(2,2,48000),
                   'Actual native stereo 48kHz PCM capture')
        duration=wav.getnframes()/wav.getframerate()
        first=max(0,int((seconds[0]-2)*wav.getframerate()))
        last=min(wav.getnframes(),int((seconds[-1]+1)*wav.getframerate()))
        scene.need(last>first and seconds[-1]<duration,'Whole declared Pit audio interval retained')
        wav.setpos(first)
        pcm=np.frombuffer(wav.readframes(last-first),dtype='<i2').reshape(-1,2).astype(np.int32)
    peak=int(np.max(np.abs(pcm)))
    scene.need(peak>0 and np.count_nonzero(pcm)>48000,'Pit interval has actual non-silent mixed audio')
    commands=rows(log,'SOUND')
    scene.need(commands and all(r['writes']=='0' and r['assistance']=='none' and
               int(r['at'],16) in (0x01d01020,0x01d01030) for r in commands),
               'Actual native sound-port observation, never supplied commands')
    for path in folder.rglob('*'):
        if path.is_file():inputs[str(path)]=hashlib.sha256(path.read_bytes()).hexdigest().upper()
    return dict(passed=True,fighter=fighter,human_slot=side,native_state=proof,pictures=pictures,
                retained_frames=len(snaps),native_sound_commands=commands,
                pcm_capture=dict(duration=duration,interval_start=first/48000,interval_end=last/48000,
                                 peak=peak,nonzero_samples=int(np.count_nonzero(pcm))),
                inputHashes=inputs,cinematicAcceptance=False,audioAcceptance=False,fullPortAcceptance=False,
                scope='current_native_Pit_state_continuation_and_contiguous_display_non_silent_PCM_inventory_not_rendered_replay_shake_foreground_correct_audio_art_or_goal')


def report():
    cases={name:inspect(scene.ROOT/name,fighter,side) for name,(fighter,side) in CASES.items()}
    inputs={}
    for proof in cases.values():inputs.update(proof.pop('inputHashes'))
    for module in tuple(sys.modules.values()):
        value=getattr(module,'__file__',None)
        if value:
            path=Path(value).resolve()
            if path.is_relative_to(scene.ROOT/'tools') and path.suffix=='.py':
                inputs[str(path)]=hashlib.sha256(path.read_bytes()).hexdigest().upper()
    for relative in ('mk2/mk2-maincpu.bin','diagnostic_v545_native_roll_edge_clearance/roms/mk2ks/mk2ks.mdata'):
        path=scene.ROOT/relative;inputs[str(path)]=hashlib.sha256(path.read_bytes()).hexdigest().upper()
    return dict(passed=True,candidate=scene.NAME,cases=cases,inputHashes=inputs,
                cinematicAcceptance=False,audioAcceptance=False,fullPortAcceptance=False)


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,required=True);args=parser.parse_args()
    scene.need(not args.output.exists(),'Never overwrite evidence')
    proof=report();args.output.write_text(json.dumps(proof,indent=2)+'\n')
    print(json.dumps(dict(passed=True,retained_frames=sum(c['retained_frames'] for c in proof['cases'].values()),
                         cinematicAcceptance=False,audioAcceptance=False),indent=2))
