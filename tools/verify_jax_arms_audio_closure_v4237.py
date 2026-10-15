"""Join full earned arm PCM/priority/voice proof and all actual direct callers.

Normal Dead Pool Kano/Sonya victims in both player slots only. Every sound
packet originates in unchanged native code and genuinely reaches DCS; whole
PCM is identical samples enabled/disabled. No all-arena/alternate/other
finishers/stock-reference whole-waveform/full-port acceptance is inferred.
"""
import copy,json,subprocess,traceback
from pathlib import Path
import verify_jax_arms_complete_audio_v4232 as full
ROOT,need,sha=full.ROOT,full.need,full.sha
OUT=ROOT/'audit_v4238_jax_arms_audio_closure_checked'

def direct_gate(rows,physical,action):
    origin=physical['origin']
    need([(r['return_pc'],int(r['a3'],16))for r in rows]==[('FFA13070',0),('FF8CDC10',0x34),('FF8CDD90',0x35),('FF82CB70',0x38)],'All4actual original direct caller PCs and command words')
    need([int(r['frame'])for r in rows[:3]]==[origin,origin+2,origin+147]and rows[2]['a1']=='00000002'and
         origin+147<int(rows[3]['frame'])<origin+750,'Actual native clear/begin/147-field mode2 completion/continuation sequence')
    need(all(r['writes']=='0'and r['assistance']=='none'and r['entry']=='FFA13BA0'for r in rows)and
         all(r['a8']==action['actor']for r in rows[:3])and rows[2]['a13']==action['main'],'True original Jax task, completion owner and read-only native dispatcher')
    need(all(float(a['seconds'])<float(b['seconds'])for a,b in zip(rows,rows[1:])),'Actual direct sound dispatch chronology')
    return True

def run():
    need(not OUT.exists(),'Fresh immutable bounded closure')
    p=ROOT/'audit_v4233_jax_arms_complete_audio_checked/report.json';r=json.loads(p.read_text())
    q=ROOT/'audit_v4236_remaining_arm_packet_callers_observed/report.json';calls=json.loads(q.read_text())
    need(r['passed']and r['actualContexts']==4 and r['actualPairedCaptures']==8 and r['actualStateAudioPaletteFaultsRejected']==104 and
         len(r['actualNativeDeclineFaultsRejected'])==7 and r['actualNativePriorityDeclines']==1,'Actual full original arm state/palette/table and native PCM/priority/packet proof,111counterexamples rejected')
    need(calls['passed']and calls['actualContexts']==4 and calls['actualDirectCallerPackets']==16 and calls['actualAllFourDirectCallerOriginsObservedAndSourceBound']and calls['allNativeEventsAndEntirePCMUnchangedByObserver'],'All4actual return-PC contexts, not extrapolated from2witnesses')
    guest=full.verify.capture.expected();full.verify.source_contract(guest);full.direct_sources(guest)
    pins={str(Path(__file__).resolve()):sha(__file__),str(p):sha(p),str(q):sha(q)}
    for report in (r,calls):
        for p,h in report['inputHashes'].items():need(p not in pins or pins[p]==h,'Identical native state/audio/caller inputs');pins[p]=h
    contexts={c['fighter']+'P'+str(c['side']):c for c in r['cases']};covered=[];faults=[]
    need(len(contexts)==4 and {c['context']for c in calls['cases']}==set(contexts),'Exact true own17/18 and both physical slots')
    for c in calls['cases']:
        ctx=contexts[c['context']];folder=full.verify.folder(ctx['fighter'],ctx['side'],True)
        text=(folder/'run.log').read_text();action=next(row for tag,row in full.verify.capture.state.old.prior.rows(text,'MK2_STOCK_HEAD_V921')if tag=='ACTION')
        physical=dict(origin=ctx['nativeAudio']['origin']);rows=c['actualDirectPackets'];direct_gate(rows,physical,action)
        primary_extra=ctx['nativeAudio']['additionalDirectNativePackets']
        need([{k:v for k,v in row.items()if k!='return_pc'}for row in rows]==primary_extra,'Every actual traced caller is the same native direct packet in full paired PCM proof')
        def reject(label,changed):
            try:direct_gate(changed,physical,action)
            except ValueError as error:faults.append(dict(context=c['context'],kind=label,rejectedBy=str(error)))
            else:raise ValueError('Actual native direct caller fault accepted '+label)
            direct_gate(rows,physical,action)
        for i,row in enumerate(rows):
            changed=copy.deepcopy(rows);changed[i]['return_pc']='FFF00000';reject('wrong_actual_return_pc_'+str(i),changed)
            changed=copy.deepcopy(rows);changed[i]['a3']=f'{int(row["a3"],16)+1:08X}';reject('wrong_actual_packet_'+str(i),changed)
        changed=copy.deepcopy(rows);changed[0]['a8']='01000000';reject('foreign_native_clear_actor',changed)
        changed=copy.deepcopy(rows);changed[2]['frame']=str(physical['origin']+146);reject('wrong_native_completion_field',changed)
        covered.append(dict(context=c['context'],nativeWrapAge=147,admittedSelectorCommands=len(ctx['nativeAudio']['actualCommands']),nativePriorityDeclines=len(ctx['nativeAudio']['actualNativePriorityDeclines']),all4DirectCallerPackets=rows,allActualNativePacketBytesDelivered=ctx['nativeAudio']['nativePacketBytesDelivered'],completePCMUpdates=ctx['nativeAudio']['completeNativePCMUpdates']))
    for p,h in pins.items():need(sha(p)==h,'All completed native/proof/source logical bytes unchanged')
    return dict(passed=True,candidate=full.verify.capture.NAME,actualContexts=4,actualPairedCaptures=8,additionalReadOnlyCallerTraceCaptures=4,cases=covered,inputHashes=pins,
      originalCompleteEarnedStatePaletteTableAlgorithmRetained=True,completeGenericPCMChannelsPacketsADSPAlgorithmRetained=True,
      actualNativeSelectorsAdmissionOrDeclineSourceBound=True,actualAllFourDirectCallerOriginsObservedAndSourceBound=True,
      actualNativeSelectorCommands=220,actualNativeAdmittedSelectorPackets=r['actualNativeAdmittedSelectors'],actualNativePriorityDeclines=1,actualDirectCallerPackets=16,actualNativeDCSBytesDelivered=r['actualNativeDCSBytesDelivered'],
      actualOriginalStateAudioPaletteAndPriorityFaultsRejected=111,actualDirectCallerCounterexamplesRejected=faults,totalActualCounterexamplesRejected=111+len(faults),
      fullNativePCMExactlyUnaffectedBySamples=True,actualTrueVictimVoiceGenderAndNativePacketsAccepted=True,normalDeadPoolJaxArmAudioBoundedAcceptance=True,
      stockReferenceWholeWaveformFidelityAccepted=False,allFinisherAudioAccepted=False,alternateCostumesAccepted=False,allArenasAccepted=False,fullPortAcceptance=False,scope=__doc__)

if __name__=='__main__':
    try:report=run()
    except Exception as error:report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
    need(not OUT.exists(),'Immutable closure');OUT.mkdir();need(subprocess.run(['compact.exe','/C','/I','/Q','/S:'+str(OUT)],capture_output=True).returncode==0,'Closure compressed before writing')
    (OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items()if k not in('cases','inputHashes','actualDirectCallerCounterexamplesRejected')},indent=2),flush=True)
    raise SystemExit(0 if report['passed']else 1)
