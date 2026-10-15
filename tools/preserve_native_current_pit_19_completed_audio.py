"""Publish the full completed audio proof from its actual reporting exception.

All waveform, 29 faults and terminal checks completed before the missing
report-pin namespace name. Recover their original objects from that exact
exception, rerun the entire positive gate and bind RAM before publication.
No synthesized audio, fitted clocks, new native boot or reduced model gates.
"""
import gzip
import hashlib
import json
import traceback
from pathlib import Path
import qualify_native_current_cross_pit_19_audio_ram_context as context
import run_native_current_cross_pit_19_audio as original

ROOT, need, sha = original.ROOT, original.need, original.sha


def publish(ram, error):
    need(isinstance(error,NameError) and error.name=='previous', 'Exact final report-pin namespace error, not a model failure')
    trace=error.__traceback__
    while trace.tb_next:trace=trace.tb_next
    frame=trace.tb_frame
    need(frame.f_code.co_name=='qualify_same_capture' and
         frame.f_code.co_filename==context.__file__+'::entire_original_current19_audio_same_actual_RAM',
         'Actual completed current19 runtime tail, not an unrelated exception')
    values=frame.f_locals
    report,live,accepted=values['report'],values['live'],values['accepted']
    folder=ram['folder'];path=folder/'current_19_audio_report.json'
    need(not path.exists() and report['passed'] and report['currentCrossPit19ChannelFiniteAudioAccepted'] and
         report['accepted'] is accepted and report['waveform'] is live['waveform'] and
         not report['fullPortAcceptance'] and not report['cinematicVictimAudioOwnershipAccepted'] and
         not report['allNativePitCuePriorityAndRNGAccepted'], 'Entire originally constructed full proof after all gates, no expanded claim')
    saved=ram['captured']
    need(saved[0]==folder and values['pcm'] is saved[2] and values['chunks'] is saved[3] and
         values['buffers'] is saved[6] and values['expected'] is saved[7] and values['guest'] is ram['guest'],
         'Exact original retained source PCM/DAC/ROM/whole guest objects')
    meta=json.loads((folder/'result.json').read_text())
    need(meta['exit_code']==0 and not original.census.census() and
         all(sha(p)==h for p,h in meta['input_hashes'].items()) and
         hashlib.sha256(ram['guest']).hexdigest().upper()==meta['guestSHA256']==report['guestSHA256'] and
         hashlib.sha256(saved[2].tobytes()).hexdigest().upper()==meta['mixedPCMSHA256']==
         report['waveform']['actualSHA256']==report['waveform']['predictedSHA256'],
         'Real terminal, full current guest and entire actually retained source-exact PCM')
    with gzip.open(folder/'run.log.gz','rt')as reader:text=reader.read()
    scope=values['scope']
    restored=scope['gate'](text,meta,live,meta['fighter'],meta['side'],ram['guest'],
                           (ROOT/'mk2/mk2-maincpu.bin').read_bytes(),saved[7])
    need(all(accepted[k]==v for k,v in restored.items()) and
         len(accepted['actualAudioSourceWindowFaultsRejected'])==29 and
         all(r['kind'] and r['rejectedBy'] for r in accepted['actualAudioSourceWindowFaultsRejected']) and
         len(report['actualEarnedStateFaultsRejected'])==12 and
         report['actualEarnedStateFaultsRejected']==accepted['actualEarnedStateFaultsRejected'] and
         len(report['waveform']['actualRawMixedPCMFaultsRejected'])==4 and
         len(report['waveform']['actualMixedSourceOperationFaultsRejected'])==4,
         'Whole source-clock/window/channel/native/DAC/ROM/packet positive restored; every originally executed fault retained')
    terminal,pool=report['nativeTerminalChannels'],report['nativeTerminalOwnerPool']
    need(len(terminal)==19 and {int(r['channel'])for r in terminal}==set(range(19)) and
         all(r['sample']=='4294967295' and r['writes']=='0' and r['assistance']=='none'for r in terminal) and
         len(pool)==1 and pool[0]['actor']==pool[0]['main']=='00000000' and
         pool[0]['slots']=='0000,0;0000,0;0000,0;0000,0;0000,0', 'Entire actual terminal19/five-owner proof remains intact')
    failure_path=folder/'completed_audio_report_pin_namespace_failure.json'
    need(not failure_path.exists(), 'Preserve fresh actual reporting exception')
    sources=(Path(__file__),Path(context.__file__),Path(context.previous.__file__),Path(original.__file__),
             context.FAILURE,folder/'current_19_audio_failure.json',folder/'result.json',folder/'run.log.gz',original.SOURCE/'report.json')
    pins={str(p.resolve()):sha(p)for p in sources}
    failure_path.write_text(json.dumps(dict(passed=False,error=repr(error),traceback=''.join(traceback.format_exception(error)),
        entireOriginalAudioAndFaultSuitesCompletedBeforeError=True,errorDuringReportPinSerializationOnly=True,
        newNativeBoots=0,inputHashes=pins,fullPortAcceptance=False),indent=2)+'\n')
    pins[str(failure_path)]=sha(failure_path)
    report.update(additionalAnalysisInputHashes=pins,originalPostGateFailurePreserved=str(folder/'current_19_audio_failure.json'),
                  completedReportingNamespaceFailurePreserved=str(failure_path),
                  exactOriginalCompletedAudioObjectsBound=True,wholePositiveGateRestoredBeforePublication=True,newNativeBoots=0)
    need(all(sha(p)==h for p,h in pins.items()), 'All actual executed successor/source/native failure bytes bound')
    ram['report']=report
    path.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(passed=True,finiteCurrentCrossPit19ChannelAudio=True,fighter=meta['fighter'],side=meta['side'],
        stereoFrames=len(saved[2]),originalAudioWindowFaults=29,originalEarnedStateFaults=12,newNativeBoots=0,fullPortAcceptance=False)),flush=True)
    return report
