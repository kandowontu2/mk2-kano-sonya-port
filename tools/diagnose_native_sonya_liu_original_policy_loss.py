"""Complete frozen Liu failure; distinguish real attacks from guarded inputs.

Keep every target category/row bound to its terminal stream. Native HP resets
and same-value collision stores are not damage. Earlier earned SubZero and
eleven preceding fights remain finite accepted evidence, not a tower clear.
"""
import collections
import gzip
import hashlib
import json
import re
from pathlib import Path
import run_native_sonya_subzero_guard_pressure_campaign as capture

ROOT,need,sha=capture.ROOT,capture.need,capture.sha
OUT=ROOT/'audit_native_sonya_liu_original_policy_loss_diagnosed'
START=391498


def run():
    need(not OUT.exists(), 'Fresh compact complete terminal Liu diagnosis')
    paths=[ROOT/'audit_native_sonya_liu_original_policy_preserved/report.json',
           ROOT/'audit_native_sonya_liu_original_policy_retirement/report.json',
           ROOT/'audit_native_subzero_guard_pressure_earned_clear_phase_bound_checked/report.json']
    saved,retired,clear=[json.loads(path.read_text()) for path in paths]
    need(saved['preservationPassed'] and not saved['passed'] and retired['passed'] and
         clear['passed'] and clear['finiteNativeSonyaSubZeroClearAccepted'] and
         clear['actualObservedNextStage']['frame']==str(START),
         'Actual failed later campaign retired; complete earned SubZero result retained')
    pins={}
    for proof in (saved,retired,clear):
        need(not proof['fullPortAcceptance'], 'All original requirements remain open')
        for path,digest in proof['inputHashes'].items():
            need(sha(path)==digest and (path not in pins or pins[path]==digest), 'Every frozen original input unchanged')
            pins[path]=digest
    counts,decisions,actions,cpu_fields,damage=(collections.Counter() for _ in range(5))
    hashes=collections.defaultdict(hashlib.sha256);whole=hashlib.sha256()
    wins,losses,examples=[],[],[]
    field=decision=physical=None;total=0;native_legs=0
    log_path=capture.OUT/'run.log.gz'
    with gzip.open(log_path,'rt',encoding='utf-8') as stream:
        for line in stream:
            need(line.endswith('\n'), 'Entire complete terminal stream')
            need(not line.startswith(('MK2_CURRENT_CAMPAIGN_CACHE_FAILURE ','MK2_MILEENA_CAMPAIGN_OVERRUN ')), 'No native cache failure in whole campaign')
            if not line.startswith('MK2_NAT_CAMPAIGN_'): continue
            row=dict(re.findall(r'(\w+)=([^\s]+)',line))
            if int(row.get('frame','0'))<START: continue
            tag=line.split()[0].removeprefix('MK2_NAT_CAMPAIGN_')
            need(row['writes']=='0' and row['assistance']=='none', 'Every actual target record unassisted')
            counts[tag]+=1;total+=1;whole.update(line.encode());hashes[tag].update(line.encode())
            if tag=='GUARD_FIELD':
                need(row['stage']=='12' and row['human_id']==row['human_roster']=='18' and
                     row['cpu_id']==row['cpu_roster']=='1' and
                     row['human_actor']==row['human_owner'] and row['cpu_actor']==row['cpu_owner'],
                     'Every target field actual true Sonya/Liu ownership')
                field=row;cpu_fields[row['cpu_action']]+=1
            elif tag=='GUARD_DECISION': decisions[row['reason']]+=1;decision=row
            elif tag=='INPUT': physical=row
            elif tag=='GUARD_ACTION': actions[row['after']]+=1
            elif tag=='SPECIAL':
                need(field is not None and field['frame']==row['frame'] and row['move']=='leg' and
                     row['entry']=='FFF80800' and row['at']=='FFF80810' and row['pc']=='FFF80830' and
                     row['id']==row['roster']=='18' and row['stage']=='12' and
                     row['actor']==row['a8']==field['human_actor'] and row['main']==row['a13']==field['human_main'],
                     'Every actual custom activation is the source-native owned leg entry, not buttons')
                native_legs+=1
            elif tag=='HEALTH' and field is not None:
                before,after=int(row['before']),int(row['after'])
                attacker='cpu' if row['slot']=='1' else 'human'
                if (row['frame']==field['frame'] and row['pc']=='FF836700' and
                    row['a8']==field[attacker+'_actor'] and row['a13']==field[attacker+'_main'] and 0<=after<before<=161):
                    key=(row['slot'],field['human_action'],field['cpu_action'],before-after)
                    damage[key]+=1
                    if len(examples)<12:
                        examples.append(dict(nativeStore=row,sameActualField=field,
                                             precedingDecision=decision,precedingPhysicalInput=physical))
            elif tag=='WIN': wins.append(row)
            elif tag=='LOSS': losses.append(row)
    need(counts['GUARD_FIELD']==counts['GUARD_DECISION']>0 and
         len(losses)==saved['statistics']['lossesByStage']['12']==143 and
         len([row for row in wins if row['slot']=='1'])==saved['statistics']['ownWinReadsByStage']['12']==4 and
         native_legs==saved['statistics']['nativeLegActivationsByStage']['12'],
         'All actual unsuccessful attempts, rare own rounds and native leg entries retained')
    for path in (*paths,log_path,Path(__file__).resolve(),Path(capture.__file__)):
        pins[str(path.resolve())]=sha(path)
    need(all(sha(path)==digest for path,digest in pins.items()), 'Every frozen input still unchanged')
    report=dict(diagnosisCompleted=True,gameplayAccepted=False,fullPortAcceptance=False,
        completeTargetRows=total,completeTargetSHA256=whole.hexdigest().upper(),
        completeCategorySHA256={tag:digest.hexdigest().upper() for tag,digest in hashes.items()},
        counts=dict(counts),decisionCounts=dict(decisions),nativeHumanActionStores=dict(actions),
        observedNativeCpuActionFields=dict(cpu_fields),actualOwnedNativeLegEntries=native_legs,
        completeOwnedCollisionDamageInventory=[dict(slot=k[0],humanAction=k[1],cpuAction=k[2],damage=k[3],count=v)
                                               for k,v in sorted(damage.items())],
        firstOwnedCollisionDamageExamples=examples,allActualWins=wins,allActualLosses=losses,
        originalFullLogRetained=True,earlierEarnedSubZeroNotDiscarded=True,
        engineDefectNotInferredFromControllerLosses=True,inputHashes=pins,
        originalNaturalIntegrationRequirements=saved['originalNaturalIntegrationRequirements'],
        originalRemainingWorkGroups=saved['originalRemainingWorkGroups'],newBuilds=0,newROMCopies=0,
        newRawMedia=0,newZIPs=0,goalStatus='active')
    OUT.mkdir();(OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({key:report[key] for key in ('completeTargetRows','counts','decisionCounts',
                     'actualOwnedNativeLegEntries','observedNativeCpuActionFields','completeOwnedCollisionDamageInventory')},indent=2),flush=True)
    return report


if __name__=='__main__':
    run()
