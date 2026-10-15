"""Effective faults on original retained speaker/DAC buffers; no game writes."""
import copy
import hashlib
import json
import numpy as np
import qualify_native_attract_dcs_audio_v2 as model
need=model.need

def check(c):
    out=c['folder']/'native_attract_audio_faults.json'
    need(not out.exists(),'Fresh actual original-buffer counterexamples')
    predicted,actual,m=model.predict(c)
    need(np.array_equal(predicted,actual),'Entire actual source-positive before counterexamples')
    faults=[]
    for label,n,ch in (('first actual speaker sample',0,0),('final actual speaker sample',len(actual)-1,1),
                       ('actual muted Kano startup leaks audio',330*960,0),('actual muted Sonya startup leaks audio',495*960,1)):
        bad=actual.copy();bad[n,ch]^=1
        need(not np.array_equal(predicted,bad),'Real altered native PCM rejected')
        faults.append(dict(fault=label,differentSamples=int(np.count_nonzero(predicted!=bad))))
    need(predicted.shape!=actual[:-1].shape,'Actual missing final stereo frame rejected')
    faults.append(dict(fault='actual final stereo frame omitted',rejectedBy='whole shape'))
    convert=lambda signal:(np.clip(signal,-1,1).astype(np.float64)*32767).astype('<i2')
    kano_omitted=m['voice'].copy();kano_omitted[:165*960]=0
    one_sample_late=np.zeros_like(m['voice']);one_sample_late[1:]=m['voice'][:-1]
    for label,wrong in (('original native DCS contribution omitted',convert(m['voice'])),
                        ('Kano actual name contribution discarded',convert(np.float32(m['dcs']+kano_omitted))),
                        ('name source starts one sample late',convert(np.float32(m['dcs']+one_sample_late))),
                        ('native .70 name-route gain omitted',convert(np.float32(m['dcs']+np.float32(m['voice']/np.float32(.70)))))):
        need(wrong.shape==actual.shape and not np.array_equal(wrong,actual),'Nonvacuous actual source-operation fault rejected')
        faults.append(dict(fault=label,differentSamples=int(np.count_nonzero(wrong!=actual))))
    for label,key,value in (('actual native DAC gain halved','volume','3F000000'),('actual ring cursor altered','current_out','0')):
        bad=dict(c,dacHeaders=[dict(h) for h in c['dacHeaders']]);bad['dacHeaders'][0][key]=value
        need(value!=c['dacHeaders'][0][key],'Effective actual header corruption')
        try:model.predict(bad)
        except ValueError as error:faults.append(dict(fault=label,rejectedBy=str(error)))
        else:raise ValueError('Actual invalid native DAC source admitted')
    old=json.loads((model.ROOT/'audit_native_ai_response_attract/native_attract_audio_finite.json').read_text())
    need(hashlib.sha256(actual.tobytes()).hexdigest().upper()==old['actualSHA256'],
         'All634560 original stereo frames unchanged by added passive DCS observation')
    result=dict(passed=True,faultsRejected=faults,wholePriorActualPCMUnchanged=True,comparedStereoFrames=len(actual),
        nativeTerminal=c['terminal'],fullAttractAudioAccepted=False,fullPortAcceptance=False,goalStatus='active')
    out.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(dict(passed=True,effectiveFaultsRejected=len(faults),wholePriorActualPCMUnchanged=True)),flush=True)
    return result
