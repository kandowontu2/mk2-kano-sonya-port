"""Qualify actual3680 DSP delivery/channel logs against missing/extra/wrong cues.

Pure mutations of actual observed metadata, never emulator/game injections.
Every rejected case restores and rechecks its exact positive control.
"""
import copy
import json
from pathlib import Path
import run_native_sound_delivery_ram_v3682 as prior

ROOT,need,sha=prior.ROOT,prior.need,prior.sha
OUT=ROOT/'audit_v3693_native_sound_delivery_faults_checked'
rows=prior.prior.rows

def check(groups):
    native=[r for r in groups['SOUND']if r['pc']in('FFA13C90','FFA13D60')]
    delivery=groups['DELIVERY'];channels=groups['CHANNEL']
    need(len(delivery)==len(native)>0,'One actual DSP input read for every native packet byte, no extra imported delivery')
    need(all(r['mask']=='FFFF'and int(r['word'],16)<=255 for r in delivery),'Only full original low-byte DSP input reads')
    need(all(r['mask']=='FFFF'for r in native),'Native fullword packet-port writes')
    for i,(write,received)in enumerate(zip(native,delivery)):
        end=float(native[i+1]['seconds'])if i+1<len(native)else float(write['seconds'])+.1
        need(int(received['word'],16)==(int(write['word'],16)&255)and
             float(write['seconds'])<=float(received['seconds'])<end,'Actual in-order native-byte delivery before next packet write')
    origin=int(groups['BEGIN'][0]['origin']);by={(int(r['frame']),int(r['channel'])):r for r in channels}
    need(len(by)==len(channels)==14*650,'All complete actual sample-channel callbacks')
    active=[r for r in channels if int(r['sample'])!=0xffffffff]
    expected=groups['winnerSample']
    need(active and all(r['channel']=='0'and int(r['sample'])==expected and r['length']=='32000'and r['loop']==r['paused']=='0'for r in active),
         'Only finite correct winner sample, no native packet starts imported fire/effect')
    need(all(int(by[origin+650,n]['sample'])==0xffffffff for n in range(14)),'Every sample channel idle after full winner tail')
    return dict(nativeBytes=len(native),nativeF8Delivered=sum(int(r['word'],16)==0xf8 for r in delivery),sampleCallbacks=len(channels))

def run():
    need(not OUT.exists(),'Fresh immutable counterexample report')
    cases=[];pins={str(Path(__file__).resolve()):sha(__file__),str(Path(prior.__file__).resolve()):sha(prior.__file__)}
    for report_path in(ROOT/'audit_v3684_native_sound_delivery_ram_checked/report.json',ROOT/'audit_v3691_native_sound_delivery_p2_checked/report.json'):
        report=json.loads(report_path.read_text());need(report['passed']and report['candidate']==prior.NAME,'Actual terminal compiled3680 runtime gate')
        pins[str(report_path)]=sha(report_path)
        for case in report['cases']:
            log_path=ROOT/case['capture']/'run.log';log=log_path.read_text()
            need(sha(log_path)==report['inputHashes'][str(log_path)],'Bound actual capture bytes')
            pins[str(log_path)]=sha(log_path)
            groups={tag:rows(log,tag)for tag in('BEGIN','SOUND','DELIVERY','CHANNEL')}
            groups['winnerSample']=2 if case['fighter']=='kano'else 3
            positive=check(groups);faults=[]
            def reject(label,mutate):
                changed=copy.deepcopy(groups);mutate(changed)
                try:check(changed)
                except ValueError as error:faults.append(dict(fault=label,rejectedBy=str(error)))
                else:raise ValueError('Actual wrong delivery/channel accepted: '+label)
                need(check(groups)==positive,'Original exact positive restored after every fault')
            reject('omitted actual DSP read',lambda g:g['DELIVERY'].pop(0))
            reject('phantom direct marker forwarded to DCS',lambda g:g['DELIVERY'].append(dict(g['DELIVERY'][-1],word='00FE')))
            reject('wrong actual low-byte read',lambda g:g['DELIVERY'][0].update(word=f"{int(g['DELIVERY'][0]['word'],16)^1:04X}"))
            reject('partial actual DSP mask',lambda g:g['DELIVERY'][0].update(mask='00FF'))
            reject('read predates native packet',lambda g:g['DELIVERY'][0].update(seconds=str(float(g['SOUND'][0]['seconds'])-1)))
            reject('reversed actual native delivery',lambda g:g['DELIVERY'].reverse())
            active_index=next(i for i,r in enumerate(groups['CHANNEL'])if int(r['sample'])!=0xffffffff)
            reject('wrong winner sample on owned voice channel',lambda g:g['CHANNEL'][active_index].update(sample='6'))
            reject('winner cue routed to fire channel',lambda g:g['CHANNEL'][active_index].update(channel='2'))
            reject('looping winner cue',lambda g:g['CHANNEL'][active_index].update(loop='1'))
            final_index=next(i for i,r in enumerate(groups['CHANNEL'])if int(r['frame'])==int(groups['BEGIN'][0]['origin'])+650 and r['channel']=='2')
            reject('actual native F8 starts imported Sonya fire',lambda g:g['CHANNEL'][final_index].update(sample='6',length='61600',pos='1'))
            cases.append(dict(fighter=case['fighter'],side=case['side'],positive=positive,rejectedActualFaults=faults))
    need(len(cases)==4 and sum(len(c['rejectedActualFaults'])for c in cases)==40,'Both true performers/both slots, forty qualified metadata faults')
    return dict(passed=True,candidate=prior.NAME,cases=cases,totalRejectedActualMetadataFaults=40,inputHashes=pins,
      noMissingExtraOrMisroutedObservedNativeBytes=True,wholeNativeDCSWaveformAcceptance=False,fullPortAcceptance=False)

if __name__=='__main__':
    report=run();OUT.mkdir();(OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items()if k not in('inputHashes','cases')},indent=2))
