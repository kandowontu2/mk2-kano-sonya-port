"""Preserve actual reused-actor fault-selector failure; bind its full namespace.

The positive full ownership gate is unchanged. Only the negative packet test
now targets the true cinematic actor AND Main at the actual impact field,
instead of an earlier actor allocation at the same address. All22 original
owner faults and all36 whole original queue/RNG faults remain mandatory.
"""
import gzip
import inspect
import json
import traceback
from pathlib import Path
import qualify_native_current_pit_owned_audio as previous

ROOT,need,sha=previous.ROOT,previous.need,previous.sha


def preserve(error,ram):
    need(isinstance(error,ValueError) and str(error)==
         'Corrupted true victim ownership admitted MK2_MAUDIO_PACKET/a3',
         'Actual original packet-selector failure, not invented failure')
    tb=error.__traceback__
    while tb.tb_next:tb=tb.tb_next
    local=tb.tb_frame.f_locals
    need(tb.tb_frame.f_code.co_name=='reject' and local['label']=='MK2_MAUDIO_PACKET/a3',
         'Exact completed owner mutation frame retained')
    text,bad,good=local['text'],local['bad'],local['good']
    folder=ram['folder'];path=folder/'current_19_owned_packet_selector_failure.json'
    need(not path.exists(),'Preserve actual failure without replacement')
    lhs=text.splitlines();rhs=bad.splitlines()
    changed=[(a,b)for a,b in zip(lhs,rhs,strict=True)if a!=b]
    need(len(changed)==1,'One actual nonvacuous original packet mutation')
    before,after=changed[0]
    row=lambda s:dict(previous.re.findall(r'(\w+)=([^\s]+)',s))
    original,mutated=row(before),row(after)
    need(before.startswith('MK2_MAUDIO_PACKET ') and original['a8']==good['cinematicActor'] and
         original['a13']!=good['cinematicMain'] and int(original['frame'])<good['enter'] and
         mutated['a3']=='00000000' and original['a3']!='00000000' and
         {k:v for k,v in original.items()if k!='a3'}=={k:v for k,v in mutated.items()if k!='a3'} and
         previous.owner_gate(bad,ram['guest'],'kano',1)==good and
         previous.owner_gate(text,ram['guest'],'kano',1)==good,
         'Earlier reused A8/different Main packet is outside actual movie; complete gate ignores it correctly')
    with gzip.open(folder/'run.log.gz','rt')as reader:
        need(reader.read()==text,'Failure binds actual original completed native log')
    records=previous.host.original.pit.inventory(text)
    actual=[r for r in records['MK2_MAUDIO_PACKET']if r['a8']==good['cinematicActor'] and
            r['a13']==good['cinematicMain']]
    need(len(actual)==2 and all(int(r['frame'])==good['impact']for r in actual),
         'Two actual distinct cinematic impact/voice packets retain complete namespace')
    pins=dict(json.loads((folder/'result.json').read_text())['input_hashes'])
    for p in(Path(__file__),Path(previous.__file__),folder/'run.log.gz',
             folder/'result.json',folder/'current_19_audio_report.json'):
        pins[str(p.resolve())]=sha(p)
    need(all(sha(p)==h for p,h in pins.items()),'Whole actual failed native/checker source remains frozen')
    result=dict(passed=False,error=repr(error),traceback=''.join(traceback.format_exception(error)),
                actualOriginalPositiveOwnerGate=good,originalOwnerFaultsRejected=local['faults'],
                actualMutatedEarlierPacket=original,actualMutatedValue=mutated,
                actualCinematicPackets=actual,inputHashes=pins,
                failureIsActualFaultSelectorNamespaceMismatch=True,
                nativeRunExitedNormally=True,fullOwnerFaultSuiteAccepted=False,
                noNativeRerun=True,fullPortAcceptance=False)
    path.write_text(json.dumps(result,indent=2)+'\n')
    return result


def qualify(ram):
    failure_path=ram['folder']/'current_19_owned_packet_selector_failure.json'
    failed=json.loads(failure_path.read_text())
    need(not failed['passed'] and failed['failureIsActualFaultSelectorNamespaceMismatch'] and
         all(sha(p)==h for p,h in failed['inputHashes'].items()),
         'Actual original failed selector and entire original capture frozen')
    body=inspect.getsource(previous.qualify)
    body=previous.host.once(body,
        "('MK2_MAUDIO_PACKET','a3','00000000',f'a8={actor} ')",
        "('MK2_MAUDIO_PACKET','a3','00000000',f'a8={actor} a13={good[\"cinematicMain\"]}')")
    body=previous.host.once(body,
        "if l.startswith(tag+' ')and where in l)",
        "if l.startswith(tag+' ')and where in l and (tag!='MK2_MAUDIO_PACKET' or f'frame={impact} ' in l))")
    body=previous.host.once(body,'for p in(Path(__file__),Path(original_rng.__file__),',
        'for p in(Path(__file__),Path(previous.__file__),failure_path,Path(original_rng.__file__),')
    scope=dict(vars(previous),__file__=__file__,previous=previous,failure_path=failure_path)
    exec(compile(body,__file__+'::entire22_owner36_RNG_faults_actual_packet_namespace','exec'),scope)
    return scope['qualify'](ram)
