"""Same physically earned laser with whole raw PCM/DAC retained only in RAM.

Transport acceptance is not cue/waveform/full-port acceptance. Observe the
same actual process to terminal; never restart on an observation timeout.
"""
import argparse
import code
import inspect
import json
from types import SimpleNamespace
import capture_native_sonya_orb_worker_lifetime as transport
import capture_native_kano_laser_burst as prior
import qualify_native_kano_laser_audio as qualified

ROOT=qualified.ROOT
NAME='diagnostic_native_kano_laser_audio'
LUA=ROOT/'mk2ks_native_kano_laser_audio.lua'
GUARD=ROOT/'audit_native_kano_laser_audio_call_frame_source'
need,sha=qualified.need,qualified.sha
providers=prior.providers


def functions():
    expected=inspect.getsource(transport.expected)
    old='base=source.prior.prior.prior.prior.prior.visual.prior.expected();payload=source.prior.prior.prior.prior.prior.effects.PAYLOAD.read_bytes()'
    need(expected.count(old)==1,'Whole source initializer boundary');expected=expected.replace(old,'base,payload=providers()')
    run=inspect.getsource(transport.run)
    changes=[
        ('audit_native_sonya_orb_worker_lifetime_p{side}','audit_native_kano_laser_audio_p{side}'),
        ("env['MK2KS_ORB_SIDE']","env['MK2KS_LASER_SIDE']"),
        ("'-samplerate','48000'","'-samplerate','48000','-wavwrite','NUL','-samples'"),
        ('capture=dict(rgbFrames=[],errors=[],guestCount=0,folder=out)',
         'capture=dict(rgbFrames=[],errors=[],guestCount=0,folder=out,pcm=[],dac=[],romChunks=[])'),
        ('paths=[Path(__file__),LUA,',
         'paths=[Path(__file__),LUA,ROOT/"mk2ks_native_kano_laser_burst.lua",ROOT/"mk2ks_native_kano_laser_typed_epochs.lua",ROOT/"mk2ks_native_kano_laser_action.lua",ROOT/"mk2ks_current_tomb_winner_mix_observer_v5779.lua",'),
        ("else:raise ValueError('Unexpected raw native block')",
         "elif tag=='MK2_BBAUDIO_PCM':\n"
         "                            need(len(raw)==3840,'Whole native48k stereo PCM callback');capture['pcm'].append(dict(header=head,pixels=raw))\n"
         "                        elif tag=='MK2_NATIVE_DAC_RAM':\n"
         "                            need(len(raw)==(int(head['consumed'])+4)*4,'Whole original native DAC callback/prefix');capture['dac'].append(dict(header=head,pixels=raw))\n"
         "                        elif tag=='MK2_NATIVE_DCS_ROM':\n"
         "                            need(len(raw)==65536,'Whole sound ROM block');capture['romChunks'].append(dict(header=head,pixels=raw))\n"
         "                        else:raise ValueError('Unexpected raw native block')"),
        ('frames=len(capture[\'rgbFrames\']),errors=capture[\'errors\']',
         'frames=len(capture[\'rgbFrames\']),pcmCallbacks=len(capture[\'pcm\']),dacCallbacks=len(capture[\'dac\']),errors=capture[\'errors\']'),
    ]
    for old,new in changes:
        need(run.count(old)==1,'Exact terminal-first audio transport boundary');run=run.replace(old,new)
    run=run.replace('MK2_ORB_','MK2_LASER_')
    scope=dict(vars(transport),ROOT=ROOT,NAME=NAME,LUA=LUA,need=need,sha=sha,providers=providers,
        __file__=__file__,source=SimpleNamespace(OUT=GUARD,__file__=qualified.__file__))
    exec(compile(expected,__file__+'::whole_actual_guest_expectation','exec'),scope)
    exec(compile(run,__file__+'::same_handle_whole_audio_transport','exec'),scope)
    return scope['run']


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--side',type=int,choices=(1,2),required=True);args=parser.parse_args()
    capture=functions()(args.side);server=transport.serve(capture)
    print(json.dumps(dict(ramReviewPort=server.server_port,nativeHandleTerminal=True,frames=len(capture['rgbFrames']),pcmCallbacks=len(capture['pcm']))),flush=True)
    code.interact(banner='Same native trial terminal; whole rasters/PCM/DAC retained in RAM.',local=dict(capture=capture,server=server))
