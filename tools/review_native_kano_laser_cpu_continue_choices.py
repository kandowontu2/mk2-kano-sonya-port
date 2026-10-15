"""Actual finite paid-reselect/mirror AI evidence, never a laser pass."""
import json
import traceback
from pathlib import Path
import review_native_kano_laser_audio as original
import native_process_census_v6647 as identity

ROOT,need,sha=original.ROOT,original.need,original.sha
rows=original.rows
OUT=ROOT/'audit_native_kano_laser_cpu_continue_choices_review'


def review(capture):
    need(not OUT.exists(),'Fresh actual continue/choice review; preserve failed laser test');OUT.mkdir()
    try:
        folder=capture['folder'];receipt=json.loads((folder/'report.json').read_text());checked=json.loads((folder/'checked_observer_sources.json').read_text())
        need(not receipt['passed'] and receipt['nativeExit']==0 and receipt['wholeGuestMatched'] and not receipt['errors'] and checked['passed'] and
             not any(r['ProcessId']==receipt['actualWindowsIdentity']['ProcessId'] for r in identity.census()),'Same actual native0 process terminal; failed laser transport remains failed')
        need(all(sha(p)==h for r in (receipt,checked) for p,h in r['inputHashes'].items()),'All actual executed inputs frozen')
        stderr=(folder/'stderr.log').read_text()
        need(stderr=='[LUA ERROR] in execute_function: ...b_winner_mix_observer_v5779.lua::full_native_laser_audio:140: Both complete sound ROM checks and same physical laser terminal\n',
             'Only exact no-origin observer assertion; do not waive gameplay errors')
        text=capture['text'];modes=rows(text,'MK2_LASER_CPU_CONTINUE_MODE');losses=rows(text,'MK2_LASER_CPU_CONTINUE_LOSS')
        need([int(r['number']) for r in losses]==list(range(1,20)),'Exactly19 actual defeated-human losses, not timeout-assumed wins')
        mirrors=[r for r in modes if r['mode']=='2' and r['ids']=='17,17']
        need(mirrors and all(r['states']=='1,0' for r in mirrors),'Every observed actual mirror enters with human1/CPU0, true roster17/17')
        first=rows(text,'MK2_LASER_CPU_FIRST_DISPATCH');friend=rows(text,'MK2_LASER_CPU_FRIENDSHIP');lookup=rows(text,'MK2_LASER_CPU_LOOKUP')
        need(len(first)==len(friend)==1 and first[0]['frame']==friend[0]['frame'] and first[0]['actor']==friend[0]['actor'] and first[0]['main']==friend[0]['main'],
             'Actual own CPU first dispatcher and own Friendship performer, same owned actor/main')
        bindings=[r for r in lookup if r['frame']==first[0]['frame'] and r['a1']=='FFFA1900' and r['a0']=='FFFAAE00']
        need(len(bindings)==1 and bindings[0]['actor']==first[0]['actor'] and bindings[0]['main']==first[0]['main'] and bindings[0]['hp']=='161,0',
             'Actual true Kano CPU first table resolves own performer, never Mileena/proxy')
        distances=[r for r in lookup if r['a1']=='FFF9CAE0' and r['a0']=='00960050']
        need(distances and any(0<int(first[0]['frame'])-int(r['frame'])<100 for r in distances),
             'Actual native lookup reads dedicated80/150 profiles before first performer')
        following=[r for r in mirrors if int(r['frame'])>int(first[0]['frame'])+300]
        need(following,'Actual fresh mirror combat after CPU Friendship; no persistent winner softlock')
        need(not rows(text,'MK2_LASER_ENTRY') and not rows(text,'MK2_LASER_CPU_SECOND_DISPATCH') and not capture['pcm'] and not capture['dac'] and
             not rows(text,'MK2_LASER_OVERRUN'),'No laser/RNG success fabricated, no raw audio window, no native copier overrun')
        parent=json.loads((ROOT/'audit_native_kano_laser_audio_call_frame_source/report.json').read_text())
        pins={str(Path(__file__).resolve()):sha(__file__)}
        for path in (folder/'report.json',folder/'checked_observer_sources.json',folder/'run.log.gz',folder/'stderr.log',ROOT/'audit_native_kano_laser_audio_call_frame_source/report.json'):
            pins[str(path)]=sha(path)
        report=dict(passed=True,finiteNormalPaidKanoReselectAndMirrorCombatObserved=True,actualLosses=19,
                    actualMirrorAdmissions=len(mirrors),actualOwnCPUFirstDispatcher=first[0],actualOwnFriendshipPerformer=friend[0],
                    actualOwnFirstTableBinding=bindings[0],actualOwnDedicatedDistanceLookups=distances,
                    actualSubsequentMirrorCombat=following[0],nativeExit=0,originalLaserTransportFailurePreserved=True,
                    nativeCPUMirrorLaserAccepted=False,allCPUContextsAccepted=False,fullFinisherAccepted=False,
                    fullPortAcceptance=False,wholeNewVisualRegressionAccepted=False,inputHashes=pins,
                    originalNaturalIntegrationRequirements=parent['originalNaturalIntegrationRequirements'],originalRemainingWorkGroups=parent['originalRemainingWorkGroups'],
                    thisGoalTurnClassification='progress: real native19 paid losses/reselects, owned mirror first finisher table and native distance profile; no random second choice selected',
                    goalStatus='active',latestPlayableChanged=False,newBuilds=0,newROMCopies=0,newRawMedia=0,newZIPs=0,
                    limitations=['Finite continued mirror behavior only; no all-stage/full-visual/full-audio proof.',
                                 'Native RNG did not choose the second finisher; no CPU mirror laser acceptance.'])
        need(len(report['originalNaturalIntegrationRequirements'])==14 and len(report['originalRemainingWorkGroups'])==6,'Full original scope retained')
        (OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
        print(json.dumps(dict(passed=True,nativeMirrorAdmissions=len(mirrors),actualLosses=19,CPUMirrorLaserAccepted=False)),flush=True)
        return report
    except Exception:
        (OUT/'failure.txt').write_text(traceback.format_exc());raise
