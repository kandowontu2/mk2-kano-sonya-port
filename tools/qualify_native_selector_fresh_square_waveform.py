"""Whole retained mixed PCM, actual Square and two native Sonya winners."""
import hashlib
import inspect
import json
import struct
import traceback
from pathlib import Path
import numpy as np
import current_cpu_compound_audio_model_v6444 as model
import qualify_native_selector_fresh_lowkick_controls as controls
import verify_native_source_sync as sync

OUT=sync.ROOT/'audit_native_selector_fresh_square_waveform_checked'


def binding():
    source=inspect.getsource(model.predict_mix)
    for before,after in (
        ("['FFFD','6B01','6B02','6B00','FFFD']", "['FFFD','6B00','FFFD']"),
        ('for c in(0,12,13)', 'for c in(0,12)'),
    ):
        sync.need(source.count(before)==1,'Only actual event and exercised channel inventory differs')
        source=source.replace(before,after,1)
    scope=dict(vars(model))
    exec(compile(source,__file__+'::actual_recorded_event_inventory','exec'),scope)
    return scope['predict_mix'],hashlib.sha256(source.encode()).hexdigest().upper()


def main(prepared):
    try:
        sync.need(not OUT.exists(),'Fresh immutable whole waveform evidence')
        capture=json.loads(controls.CAPTURE.read_text()); key=prepared.SCOPE['KEY']
        handle=prepared.NATIVE_HANDLES[key]
        sync.need(capture['passed'] and handle['process'].poll()==0 and handle['identity']==capture['actualNativeIdentity'],
                  'Same actual terminal process; no new game')
        pins=dict(capture['inputHashes'])
        for p in (Path(__file__),Path(model.__file__),Path(model.original.__file__),Path(controls.__file__),controls.CAPTURE):
            pins[str(p.resolve())]=sync.sha(p)
        sync.need(all(sync.sha(p)==h for p,h in pins.items()),'All complete actual capture/model inputs intact')
        text=prepared.RAM_CASES[key][1]; audio=prepared.AUDIO[key]
        native=controls.gate(text,prepared.STATE['guest'])
        for tag,chunks,headers in (
            ('MK2_BBAUDIO_PCM_DIGEST',audio['pcmChunks'],audio['pcmHeaders']),
            ('MK2_NATIVE_DAC_RAM_DIGEST',audio['dacChunks'],audio['dacHeaders']),
        ):
            rows=model.rows(text,tag)
            sync.need(len(rows)==len(chunks)==len(headers)==1646 and
                      all(r==dict(h,sha256=hashlib.sha256(raw).hexdigest().upper()) for r,h,raw in zip(rows,headers,chunks,strict=True)),
                      'Every complete actual PCM/DAC callback digest bound')
        markers=[r for r in model.rows(text,'MK2_MAUDIO_SOUND') if r['pc']=='FFFB7140' or r['word'] in ('6B00','6B01','6B02')]
        sync.need([(r['frame'],r['word'],r['pc']) for r in markers]==
                  [('2328','FFFD','FFFB7140'),('2571','6B00','FFFFCAC0'),('3203','FFFD','FFFB7140')],
                  'Entire real two-winner/one-Square event inventory')
        square=markers[1]; pc=int(square['pc'],16)
        sync.need((square['a8'],square['a13'],square['mask'],square['writes'],square['assistance']) ==
                  ('010350A0','0106BF30','FFFF','0','none') and
                  prepared.STATE['guest'][(pc-96-0xff800000)//8:(pc-0xff800000)//8]==
                  struct.pack('<6H',0x09e0,0x6b00,0,0x0580,0x1030,0x01d0),
                  'Actual native Sonya actor and complete executing Square port instruction')
        predict,model_hash=binding()
        pcm=np.frombuffer(b''.join(audio['pcmChunks']),'<i2').reshape(-1,2)
        waveform=predict(audio['dacChunks'],audio['dacHeaders'],pcm,text,'sonya',pins)
        OUT.mkdir(); (OUT/'waveform.json').write_text(json.dumps(waveform,indent=2)+'\n')
        sync.need(waveform['passed'] and waveform['comparedStereoFrames']==1580160
                  and waveform['differentChannelSamples']==0 and waveform['actualSHA256']==waveform['predictedSHA256'],
                  'All actual mixed stereo samples match unchanged native source model')
        sync.need(all(sync.sha(p)==h for p,h in pins.items()),'All source/native/asset pins unchanged')
        report=dict(passed=True,actualNativeIdentity=capture['actualNativeIdentity'],wholeNativeAndControls=native,
                    wholeMixedWaveform=waveform,wholeSourceModelSHA256=model_hash,inputHashes=pins,
                    privateVoiceInterruptionAccepted=False,heardQualityAccepted=False,fullPortAcceptance=False,
                    limitations='Whole recorded mixed PCM source comparison. Not every overlap/priority/interruption context or listening/visual/full-port acceptance.',
                    newGames=0,newBuilds=0,newROMCopies=0,newRawMediaFiles=0)
        (OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n'); return report
    except BaseException:
        OUT.mkdir(exist_ok=True)
        (OUT/'failure.json').write_text(json.dumps(dict(passed=False,error=traceback.format_exc()),indent=2)+'\n')
        raise
