"""Naturally selected CPU laser: whole exact native/source mix and CPU ownership.

Finite CPU mirror only, not all victims/AI choices/full visual/full-port proof.
"""
import inspect
import json
from pathlib import Path
import review_native_kano_laser_audio as original

ROOT,need,sha=original.ROOT,original.need,original.sha


def review(capture):
    waveform=inspect.getsource(original.waveform)
    for old,new in [("'sonya_laser_scream'","'kano_laser_scream'"),
                    ('sample_id=(17,18,19,21,22)[cue]','sample_id=(17,18,20,21,22)[cue]')]:
        need(waveform.count(old)==1,'Only exact true Kano mirror waveform adaptation');waveform=waveform.replace(old,new)
    source=inspect.getsource(original.review)
    changes=[("folder=capture['folder'];side=int(folder.name[-1]);out=ROOT/f'audit_native_kano_laser_audio_p{side}_review'",
              "folder=capture['folder'];side=2;out=ROOT/'audit_native_kano_laser_cpu_audio_review'"),
             ('report=dict(passed=True,finiteNativeLaserAudioAccepted=True,physicalSlot=side,',
              'report=dict(passed=True,finiteNativeLaserAudioAccepted=True,naturallySelectedCPULaserAccepted=True,trueVictimID=17,physicalSlot=side,'),
             ('One actual earned true Kano versus Sonya laser in the indicated physical slot only.',
              'One naturally chosen native CPU Kano versus true Kano mirror, CPU physical slot2 only.')]
    for old,new in changes:
        need(source.count(old)==1,'Whole exact original audio review conserved');source=source.replace(old,new)
    anchor="        sound=waveform(capture,pins)"
    extra='''        e=entry[0];origin=int(e['frame'])
        need(e['cpu_state']=='0' and e['victim_state']=='1' and e['hp'].split(',')[1]=='0',
             'Actually defeated human and naturally native CPU owner, not human/proxy activation')
        guard=rows(text,'MK2_LASER_CPU_LASER_GUARD')
        second=rows(text,'MK2_LASER_CPU_SECOND_DISPATCH')
        need(any(int(r['frame'])==origin and r['actor']==e['actor'] and r['main']==e['main'] for r in guard) and
             any(0<=origin-int(r['frame'])<400 and r['actor']==e['actor'] and r['main']==e['main'] for r in second),
             'Actual native second finisher dispatcher and own boss/victim guard precede same owned performer')
        fields=rows(text,'MK2_LASER_FIELD')
        need(fields and {int(r['slot']) for r in fields}=={1,2},'Both true owned actors observed throughout actual finisher')
        for r in fields:
            own=int(r['slot'])==2
            need(r['id']==r['roster']=='17' and r['owner']==r['actor'] and
                 r['actor']==e['actor' if own else 'victim'] and r['main']==e['main' if own else 'victim_main'],
                 'Every actual observed CPU/human identity field remains true owned Kano17')
        need(not rows(text,'MK2_LASER_OVERRUN') and not any(r['entry']=='FFA11FD0' for r in rows(text,'MK2_MAUDIO_ROUTE')),
             'No native render overrun or stock proxy voice on true Kano mirror')
        sound=waveform(capture,pins)'''
    need(source.count(anchor)==1,'Actual native CPU ownership gates before whole waveform');source=source.replace(anchor,extra)
    scope=dict(vars(original),__file__=str(Path(__file__).resolve()))
    exec(compile(waveform,__file__+'::whole_native_CPU_mirror_mix','exec'),scope)
    exec(compile(source,__file__+'::same_actual_CPU_trial_review','exec'),scope)
    return scope['review'](capture)
