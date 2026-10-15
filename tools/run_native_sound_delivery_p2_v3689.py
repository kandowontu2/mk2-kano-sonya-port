"""Remaining physical P2 Tomb sound delivery/winner regression on compiled3680.

Preserve entire3682 physical input/guest/DSP/gender/full-waveform/channel gates;
only make the physical side explicit and use fresh immutable capture leaves.
"""
import inspect
import json
import traceback
from pathlib import Path
import run_native_sound_delivery_ram_v3682 as prior

ROOT,need,sha=prior.ROOT,prior.need,prior.sha
OUT=ROOT/'audit_v3691_native_sound_delivery_p2_checked'

def prepare():
    source=inspect.getsource(prior.collector)
    need(source.count('audit_v3683_')==1,'Exact fresh capture namespace')
    source=source.replace('audit_v3683_','audit_v3690_')
    needle="ROOT/'tools/verify_native_friendship_audio_v791.py',"
    need(source.count(needle)==1,'Explicit original waveform implementation input')
    source=source.replace(needle,needle+"ROOT/'mame-mkp/src/mame/shared/dcs.cpp',ROOT/'tools/run_native_sound_delivery_ram_v3682.py',")
    exec(compile(source,'<3682entireRAMcollector_freshP2_dependencies>','exec'),prior.__dict__)
    source=inspect.getsource(prior.pair)
    replacements={'def pair(fighter):':'def pair(fighter,side=2):',
      'capture(1,True);base,oldheaders,b=capture(1,False)':'capture(side,True);base,oldheaders,b=capture(side,False)',
      'native.check_log(log,fighter,1,1,guest=guest)':'native.check_log(log,fighter,side,1,guest=guest)',
      'fighter=fighter,side=1,capture=':'fighter=fighter,side=side,capture='}
    for old,new in replacements.items():
        need(source.count(old)==1,'Exact declared physical-slot change '+old);source=source.replace(old,new)
    exec(compile(source,'<entire3682audio_gate_explicitphysicalP2>','exec'),prior.__dict__)

def run():
    need(not OUT.exists(),'Fresh P2 actual runtime gate')
    old=json.loads((prior.OUT/'report.json').read_text())
    need(old['passed']and old['candidate']==prior.NAME and old['currentTombBothP1PerformersNativePacketDeliveryAndFullWinnerMixAccepted']and
         not old['completeStageVictimAudioFidelityAccepted'],'Retain completed narrow P1 gate without rerunning or promoting it')
    original=Path(prior.__file__).resolve();prior.__file__=__file__
    prepare()
    # All original run gates remain unchanged; only its result scope names P2.
    source=inspect.getsource(prior.run)
    source=source.replace('currentTombBothP1PerformersNativePacketDeliveryAndFullWinnerMixAccepted=True',
                          'currentTombBothP2PerformersNativePacketDeliveryAndFullWinnerMixAccepted=True')
    scope=dict(prior.__dict__);scope['OUT']=OUT
    exec(compile(source,'<entire3682run_explicitP2_result_scope>','exec'),scope)
    report=scope['run']();report['inputHashes'][str(original)]=sha(original)
    report['priorP1Report']=str(prior.OUT/'report.json');report['inputHashes'][report['priorP1Report']]=sha(report['priorP1Report'])
    report['priorP1NotRerun']=True;report['scope']=__doc__
    return report

if __name__=='__main__':
    try:report=run()
    except Exception as error:report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
    need(not OUT.exists(),'Immutable P2 result');OUT.mkdir();(OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items()if k not in('inputHashes','cases')},indent=2),flush=True)
    raise SystemExit(0 if report['passed']else 1)
