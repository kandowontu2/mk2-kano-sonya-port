"""Actual crossed-position CPU mirror bindings and inspected raster metadata.

Human/CPU roles follow actor/main/native states, never screen-left assumptions.
All19 checkpoints were individually viewed from the same RAM-only carrier.
This is sampled visual evidence, not entire-raster/finisher/port acceptance.
"""
import json
import traceback
from pathlib import Path
import review_native_kano_laser_audio as original

ROOT,need,sha=original.ROOT,original.need,original.sha
rows=original.rows
OUT=ROOT/'audit_native_kano_laser_cpu_motion_binding_visuals_review'


def review(capture):
    need(not OUT.exists(),'Fresh actual CPU dispatch/crossed-actor/raster review');OUT.mkdir()
    try:
        folder=capture['folder'];parent_path=ROOT/'audit_native_kano_laser_cpu_motion_audio_review/report.json'
        parent=json.loads(parent_path.read_text());transport=json.loads((folder/'report.json').read_text());checked=json.loads((folder/'checked_observer_sources.json').read_text())
        need(parent['passed'] and parent['naturallySelectedCPULaserAccepted'] and transport['passed'] and transport['nativeExit']==0 and checked['passed'] and
             all(sha(p)==h for r in (parent,transport,checked) for p,h in r['inputHashes'].items()),'Same accepted actual CPU mirror/source mix and immutable native inputs')
        text=capture['text'];entry=rows(text,'MK2_LASER_ENTRY')[0];origin=int(entry['frame'])
        dispatch=[r for r in rows(text,'MK2_LASER_CPU_SECOND_DISPATCH') if int(r['frame'])==origin]
        guard=[r for r in rows(text,'MK2_LASER_CPU_LASER_GUARD') if int(r['frame'])==origin]
        lookup=[r for r in rows(text,'MK2_LASER_CPU_LOOKUP') if r['a1']=='FFFA1B60' and r['a0']=='FFD86600' and int(r['frame'])==origin]
        need(len(dispatch)==len(guard)==len(lookup)==1,'Actual native CPU second table resolves own laser guard exactly once')
        for r in dispatch+guard+lookup:
            need(r['actor']==entry['actor'] and r['main']==entry['main'] and r['victim']==entry['victim'] and r['hp']=='161,0' and r['gap']=='166',
                 'Native CPU source context and actual defeated human remain identical across table/guard/performer')
        distances=[r for r in rows(text,'MK2_LASER_CPU_LOOKUP') if r['a1']=='FFF9CAE0' and r['a0']=='00960050' and
                   0<=origin-int(r['frame'])<100 and r['actor']==entry['actor'] and r['main']==entry['main']]
        need(distances,'Actual native dedicated80/150 profile read before this CPU finisher approach')
        fields=rows(text,'MK2_LASER_FIELD')
        need(fields and {int(r['slot']) for r in fields}=={1,2},'Both actual physical-slot identities observed')
        first=[r for r in fields if r['age']=='1'];need(len(first)==2,'Both whole first-field actor records')
        human=next(r for r in first if r['slot']=='1');cpu=next(r for r in first if r['slot']=='2')
        need(human['actor']==entry['victim'] and cpu['actor']==entry['actor'] and
             human['state']=='1' and cpu['state']=='0' and human['hp']=='0' and cpu['hp']=='161' and
             int(cpu['x'])<int(human['x']) and int(human['x'])-int(cpu['x'])==166,
             'Actual CPU is screen-left after ordinary crossing, human screen-right; roles never inferred from left/right or palette')
        for r in fields:
            role=cpu if r['slot']=='2' else human
            need(r['id']==r['roster']=='17' and r['actor']==role['actor'] and r['main']==role['main'] and r['owner']==r['actor'],
                 'Every actual observed field keeps correct actor/main/native identity and ownership through visual finisher')
        ages=(1,21,48,68,72,100,132,164,169,172,175,196,240,450,600,750)
        rasters=[]
        need(len(capture['rgbFrames'])==19,'Exactly three original campaign rasters plus16 CPU finisher checkpoints')
        for index,row in enumerate(capture['rgbFrames']):
            head=row['header'];raw=row['pixels']
            need(int(head['width'])==400 and int(head['height'])==254 and len(raw)==406400 and
                 original.hashlib.sha256(raw).hexdigest().upper()==head['sha256'] and set(raw[3::4])=={255},
                 'Whole actual native raster digest/geometry and opaque fourth byte')
            if index>=3:need(int(head['age'])==ages[index-3] and int(head['frame'])==origin+ages[index-3],
                              'Every requested native checkpoint is the actual expected field, no substituted/reordered raster')
            rasters.append(dict(header=head,individuallyViewed=True,wholeRawRasterDigestMatched=True))
        need(all(r['header']['sha256']=='86936966FDD61FE53E79A5A1A904C523B5D2F7BE4359EE5880D90D2686567E40'
                 for r in rasters if r['header'].get('age') in ('169','172')),'Two sampled native full-white flash fields match original accepted recipe')
        pins={str(Path(__file__).resolve()):sha(__file__),str(parent_path):sha(parent_path)}
        for path in (folder/'report.json',folder/'checked_observer_sources.json',folder/'run.log.gz',
                     ROOT/'tools/review_native_kano_laser_cpu_motion_audio.py',ROOT/'tools/review_native_kano_laser_cpu_audio.py',
                     ROOT/'audit_native_kano_laser_cpu_motion_audio_lua_full_source/report.json'):
            pins[str(path)]=sha(path)
        report=dict(passed=True,finiteNaturalCPUSecondDispatcherBindingAccepted=True,actualCPUSecondDispatcher=dispatch[0],
                    actualCPUSecondTableBinding=lookup[0],actualOwnCPUVictimGuard=guard[0],actualDedicatedDistanceLookups=distances,
                    crossedHumanCPUPositionsBoundToCorrectActors=True,firstActualNativeActorFields=first,
                    trueIdentityOwnershipFieldsChecked=len(fields),sampledNativeCPUMirrorRastersIndividuallyInspected=rasters,
                    wholeNativeMixedWaveformAccepted=True,stereoFrames=parent['wholeNativeMixedWaveform']['comparedStereoFrames'],
                    nativeWinnerAge196Accepted=True,nativeActualTerminalAge751Accepted=True,
                    fullFinisherAccepted=False,allCPUContextsAccepted=False,wholeNewVisualRegressionAccepted=False,fullPortAcceptance=False,
                    originalNaturalIntegrationRequirements=parent['originalNaturalIntegrationRequirements'],originalRemainingWorkGroups=parent['originalRemainingWorkGroups'],
                    inputHashes=pins,goalStatus='active',latestPlayableChanged=False,newBuilds=0,newROMCopies=0,newRawMedia=0,newZIPs=0,
                    previousGoalTurnClassification='progress: two actual CPU-vs-Sonya activations and first full exact source mix, with retained fixture-stop failure',
                    thisGoalTurnClassification='progress: actual19 paid mirror losses and native first choice; repaired full-controller parser; natural CPU mirror second table/guard/performer, crossed identities, full exact audio and all19 sampled rasters inspected',
                    limitations=['One naturally selected CPU physical-slot2 Kano mirror with normal motion before defeat.',
                                 'Sixteen finisher checkpoints and three original campaign rasters, not all video fields.',
                                 'No complete particle/arena/reset/rejoin/all-victim/all-CPU-branch/full14+6acceptance.'])
        need(len(report['originalNaturalIntegrationRequirements'])==14 and len(report['originalRemainingWorkGroups'])==6,'Full original goal scope retained')
        (OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
        print(json.dumps(dict(passed=True,nativeCPUSecondDispatch=True,crossedActorIdentityFields=len(fields),stereoFrames=report['stereoFrames'],sampledRastersInspected=19)),flush=True)
        return report
    except Exception:
        (OUT/'failure.txt').write_text(traceback.format_exc());raise
