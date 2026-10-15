"""Actual two-slot stock/mirror/added-victim source-mix matrix.

Verify stock voice selection, priority packet and both real ADSP deliveries,
not just the existence of a dispatcher call. Every body identity field is
checked. No universal victim/CPU/visual/port acceptance is inferred.
"""
import gzip
import json
import traceback
from decimal import Decimal
from pathlib import Path
import review_native_kano_laser_audio as original
import native_process_census_v6647 as identity

ROOT,need,sha=original.ROOT,original.need,original.sha
OUT=ROOT/'audit_native_kano_laser_victim_audio_matrix_review'


def stock_delivery(text,entry):
    routes=[r for r in original.rows(text,'MK2_MAUDIO_ROUTE') if r['a8']==entry['victim'] and r['a13']==entry['victim_main']]
    need([r['entry'] for r in routes]==['FFA11FD0','FFA12220','FFA123B0','FFA123D0','FFA12530'] and
         all(r['id']=='4' and r['owner']==entry['victim'] and r['return_pc']=='FFD87310' for r in routes),
         'Complete actual Kitana dispatcher/gender/RNG-selection/record path retains true victim/caller')
    need(routes[1]['a1']=='32343638' and routes[3]['a0']=='00000002' and int(routes[-1]['a0'],16) in (0x36,0x38),
         'Actual original two-choice female stock voice family, not male or imported scream')
    packet=[r for r in original.rows(text,'MK2_MAUDIO_PACKET') if r['a8']==entry['victim'] and r['a13']==entry['victim_main']]
    need(len(packet)==1 and packet[0]['a1']=='00000034','Actual original admitted stock priority34 packet, not silently dropped call')
    ports=[r for r in original.rows(text,'MK2_MAUDIO_SOUND') if r['a8']==entry['victim'] and r['a13']==entry['victim_main'] and
           r['pc'] in ('FFA13C90','FFA13D60')]
    command=int(packet[0]['a3'],16)
    need(len(ports)==2 and [r['pc'] for r in ports]==['FFA13C90','FFA13D60'] and
         [int(r['word'],16) for r in ports]==[0xff00|(command>>8),0xff00|(command&255)] and
         all(r['mask']=='FFFF' for r in ports), 'Exact stock selected command high/low port instructions delivered once')
    deliveries=original.rows(text,'MK2_MAUDIO_DELIVERY');selected=[]
    for port,byte in zip(ports,(command>>8,command&255)):
        start=Decimal(port['seconds'])
        actual=[r for r in deliveries if start<=Decimal(r['seconds'])<start+Decimal('.0001')]
        need(actual and actual[0]['word']==f'{byte:04X}' and actual[0]['mask']=='FFFF','Actual ADSP input latch consumed each stock selected byte')
        selected.append(actual[0])
    return dict(selectedStockVoice=int(routes[-1]['a0'],16),nativePriority=0x34,nativeCommand=command,
                actualRoutes=routes,actualPacket=packet[0],actualPorts=ports,actualADSPDeliveries=selected)


def main():
    need(not OUT.exists(),'Fresh immutable full typed-victim matrix');OUT.mkdir()
    try:
        need(not identity.census(),'Every actual native game handle terminal')
        source_path=ROOT/'audit_native_kano_laser_audio_call_frame_source/report.json';source=json.loads(source_path.read_text())
        cases=[];pins={str(Path(__file__).resolve()):sha(__file__),str(source_path):sha(source_path)};frames=0;faults=[]
        for victim in (4,17,18):
            for side in (1,2):
                suffix='' if victim==18 else f'_victim{victim}'
                folder=ROOT/f'audit_native_kano_laser_audio_p{side}{suffix}'
                review_path=ROOT/f'audit_native_kano_laser_audio_p{side}{suffix}_review/report.json';review=json.loads(review_path.read_text())
                need(review['passed'] and review['finiteNativeLaserAudioAccepted'] and review['physicalSlot']==side and
                     review['wholeNativeMixedWaveform']['differentChannelSamples']==0 and review['all19ChannelsObserved'] and
                     review['nativeSceneAudioCleanupAccepted'] and not review['fullPortAcceptance'] and
                     all(sha(p)==h for p,h in review['inputHashes'].items()),'Same finite whole native mix and all executed inputs preserved')
                pins[str(review_path)]=sha(review_path);log_path=folder/'run.log.gz';pins[str(log_path)]=sha(log_path)
                text=gzip.open(log_path,'rt').read();entries=original.rows(text,'MK2_LASER_ENTRY');need(len(entries)==1,'One genuinely earned activation')
                entry=entries[0];fields=original.rows(text,'MK2_LASER_FIELD')
                need(len(fields)==902 and {(int(r['age']),int(r['slot'])) for r in fields}=={(a,s) for a in range(451) for s in (1,2)},
                     'Every actor field in complete0..450 native body timeline, not selected IDs')
                for row in fields:
                    own=int(row['slot'])==side
                    need(row['id']==row['roster']==str(17 if own else victim) and
                         row['actor']==entry['actor' if own else 'victim'] and row['main']==entry['main' if own else 'victim_main'],
                         'Official true actor/roster/main remains unchanged in every native action/winner field, never proxy')
                markers=original.rows(text,'MK2_LAUDIO_MARKER')
                need([r['marker'] for r in markers]==(['6B40','6B41','6B43','6B44'] if victim==4 else ['6B40','6B41','6B42','6B43','6B44']),
                     'Stock victim dispatch versus own original scream branch, exact full core marker order')
                native=stock_delivery(text,entry) if victim==4 else None
                if victim!=4:
                    scream=[r for r in review['wholeNativeMixedWaveform']['sourceEvents'] if r['marker']['word']=='6B42']
                    need(len(scream)==1 and scream[0]['channel']==16 and scream[0]['sample_id']==(20 if victim==17 else 19) and
                         scream[0]['length']==(152786 if victim==17 else 180070), 'Actual complete own Kano/Sonya source clip in true victim channel')
                if victim==4:
                    bad=text.replace(f"word={native['actualPorts'][0]['word']} mask=FFFF pc=FFA13C90 a8={entry['victim']}",
                                     f"word=FFFE mask=FFFF pc=FFA13C90 a8={entry['victim']}",1)
                    need(bad!=text,'Nonvacuous actual native stock port fault')
                    try:stock_delivery(bad,entry)
                    except ValueError as error:faults.append(dict(physicalSlot=side,victimID=victim,rejected=str(error)))
                    else:raise ValueError('Corrupt stock byte admitted')
                frames+=review['wholeNativeMixedWaveform']['comparedStereoFrames']
                cases.append(dict(physicalSlot=side,trueVictimID=victim,identityFieldsChecked=len(fields),
                                  stereoFrames=review['wholeNativeMixedWaveform']['comparedStereoFrames'],all19ChannelsTerminal=True,
                                  stockNativeQueueAndDSP=native,wholeMixSHA256=review['wholeNativeMixedWaveform']['actualSHA256']))
        need(len(faults)==2,'Both actual stock channel byte faults rejected')
        cmd=ROOT/'PLAY_LATEST_KANO_SONYA.cmd';need(sha(cmd)=='D6BABF8CBC1F4CB020F3D7F3A2C8C5A3A762B946E83D56FC1E5BA3B398129DE5','Public launcher not silently promoted')
        pins[str(cmd)]=sha(cmd)
        report=dict(passed=True,bothSlotsKitanaNativeVoiceQueueDSPMixAccepted=True,bothSlotsKanoMirrorScreamMixAccepted=True,
                    bothSlotsSonyaVictimScreamMixAccepted=True,cases=cases,totalStereoFramesCompared=frames,totalIdentityFieldsChecked=5412,
                    stockNativePortFaultsRejected=faults,allVictimsAccepted=False,allPriorityRNGContextsAccepted=False,nativeCPULaserAccepted=False,
                    fullFinisherAccepted=False,wholeNewVisualRegressionAccepted=False,fullPortAcceptance=False,
                    originalNaturalIntegrationRequirements=source['originalNaturalIntegrationRequirements'],originalRemainingWorkGroups=source['originalRemainingWorkGroups'],
                    previousGoalTurnClassification='progress: actual both-slot whole laser audio accepted and compiler cache retired',
                    thisGoalTurnClassification='progress: new victim constants source-qualified by actual installed Lua; actual both-slot Kitana native queue/DSP and Kano mirror source scream/fullmix tested without new builds',
                    inputHashes=pins,goalStatus='active',latestPlayableChanged=False,newBuilds=0,newROMCopies=0,newRawMedia=0,newZIPs=0,
                    remaining=['Other stock voice families/actors, native CPU activation and legal fallback/rejection.',
                               'Full current visual/particle/arena/scene/reset/rejoin regression and all original14+6 requirements before final CMD/ZIP.'])
        need(len(report['originalNaturalIntegrationRequirements'])==14 and len(report['originalRemainingWorkGroups'])==6,'Full natural-integration objective retained')
        (OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(dict(passed=True,cases=6,stereoFrames=frames,trueIdentityFields=5412,fullPortAccepted=False)))
    except Exception:
        (OUT/'failure.txt').write_text(traceback.format_exc());raise


if __name__=='__main__':main()
