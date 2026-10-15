"""Full original mixed PCM review, typed stock or mirror voice branch.

No actual window, source tail, native DAC or native announcement is removed.
Keep prior Sonya cases and all original14requirements/6groups intact.
"""
import inspect
import json
from pathlib import Path
import review_native_kano_laser_audio as original

ROOT,need,sha=original.ROOT,original.need,original.sha


def review(capture):
    victim=capture['victimID'];need(victim in (4,17),'Same actual source-qualified victim')
    waveform=inspect.getsource(original.waveform)
    if victim==17:
        changes=[("'sonya_laser_scream'","'kano_laser_scream'"),
                 ('sample_id=(17,18,19,21,22)[cue]','sample_id=(17,18,20,21,22)[cue]')]
    else:
        changes=[("['6B40','6B41','6B42','6B43','6B44','FFFE']","['6B40','6B41','6B43','6B44','FFFE']"),
                 ('for c in (0,14,15,16)','for c in (0,14,15)')]
    for old,new in changes:
        need(waveform.count(old)==1,'Only exact actually exercised voice-branch adaptation');waveform=waveform.replace(old,new)
    source=inspect.getsource(original.review)
    changes=[("folder=capture['folder'];side=int(folder.name[-1]);out=ROOT/f'audit_native_kano_laser_audio_p{side}_review'",
              "folder=capture['folder'];side=json.loads((folder/'report.json').read_text())['side'];out=ROOT/f'audit_native_kano_laser_audio_p{side}_victim{victim}_review'"),
             ('if int(row[\'channel\']) not in (0,14,15,16):',
              'if int(row[\'channel\']) not in '+('(0,14,15,16):' if victim==17 else '(0,14,15):')),
             ('report=dict(passed=True,finiteNativeLaserAudioAccepted=True,physicalSlot=side,',
              'report=dict(passed=True,finiteNativeLaserAudioAccepted=True,physicalSlot=side,trueVictimID=victim,nativeStockVoiceBranchAccepted=victim<17,importedKanoMirrorScreamAccepted=victim==17,'),
             ('One actual earned true Kano versus Sonya laser in the indicated physical slot only.',
              'One actual earned true Kano versus the indicated stock or mirror victim, physical slot only.')]
    for old,new in changes:
        need(source.count(old)==1,'Complete original review scope conserved');source=source.replace(old,new)
    anchor="        sound=waveform(capture,pins)"
    extra='''        routes=rows(text,'MK2_MAUDIO_ROUTE')
        native_voice=[r for r in routes if r['entry']=='FFA11FD0']
        if victim<17:
            need(len(native_voice)==1 and native_voice[0]['id']==str(victim) and
                 native_voice[0]['a8']==entry[0]['victim'] and native_voice[0]['a13']==entry[0]['victim_main'] and
                 native_voice[0]['owner']==entry[0]['victim'],
                 'Actual stock native voice helper retains true victim ID/actor/main ownership')
        else:
            need(not native_voice,'True Kano mirror takes original own scream, never stock native proxy')
        sound=waveform(capture,pins)'''
    need(source.count(anchor)==1,'Actual native voice branch checked before full waveform');source=source.replace(anchor,extra)
    scope=dict(vars(original),victim=victim,__file__=__file__)
    exec(compile(waveform,__file__+'::whole_true_victim_source_mix','exec'),scope)
    exec(compile(source,__file__+'::whole_native_victim_review','exec'),scope)
    return scope['review'](capture)
