"""Whole original guard/leg physical replay on two real current tower stages.

Finite original native prefix only. No ending, full tower, pixels/shadow/audio
or full-port acceptance. Same live parent/native birth/command must match.
"""
import gzip
import hashlib
import inspect
import json
import re
import traceback
from pathlib import Path
import verify_mirror_guard_zoning_prefix_v4194 as old
import capture_native_kano_laser_sonya_postending_leg_guard_late as current
import native_process_census_v6647 as census

ROOT,need,sha=current.ROOT,current.need,current.sha
OUT=ROOT/'audit_native_sonya_kano_leg_guard_prefix_checked'
GAME,PARENT=176712,186024


def replay_factory():
    source=inspect.getsource(old.replay)
    changes=[("f['human_slot'] == '2'","f['human_slot'] == '1'"),
             ("f['cpu_id'] == f['cpu_roster'] == '18'","f['cpu_id'] == f['cpu_roster'] and f['cpu_roster'] in ('17','18')"),
             ("r['slot'] == '2'","r['slot'] == '1'")]
    for before,after in changes:
        need(source.count(before)==1,'Whole original replay slot/real CPU identity boundary')
        source=source.replace(before,after,1)
    need(source.count("f['cpu_roster'] == '18'")==4,'Four unchanged mirror leg/guard predicates now include actual CPU Kano')
    source=source.replace("f['cpu_roster'] == '18'","f['cpu_roster'] in ('17','18')")
    scope=dict(vars(old),__file__=__file__)
    exec(compile(source,__file__+'::whole_original_physical_guard_replay_current_Kano_and_mirror','exec'),scope)
    original=scope['replay']
    def replay(text):
        rows=old.parse(text)
        fields=[r for r in rows if r['tag']=='GUARD_FIELD']
        decisions=[r for r in rows if r['tag']=='GUARD_DECISION']
        need(fields and len(fields)==len(decisions)==len({r['frame'] for r in fields})==len({r['frame'] for r in decisions}) and
             {r['frame'] for r in fields}=={r['frame'] for r in decisions},
             'Every actual guard frame and decision paired, missing evidence never silently filtered')
        need(all(r['writes']=='0' and r['assistance']=='none' for r in fields+decisions),
             'Every actual observed state and input decision unassisted')
        return original(text)
    return replay,source


def run():
    need(not OUT.exists(),'Fresh exact original live prefix qualification')
    folder=current.OUT
    identity=json.loads((folder/'native_identity.json').read_text())
    actual=next((q for q in census.census() if q['ProcessId']==GAME),None)
    need(actual==identity and actual['ParentProcessId']==PARENT,'Exact original live PID/parent/path/birth/full command')
    pieces=[]
    with gzip.open(folder/'run.log.gz','rt',encoding='utf-8') as stream:
        try:
            for line in stream:
                pieces.append(line)
                if line.startswith('MK2_NAT_CAMPAIGN_STAGE ') and ' stage=2 ' in line: break
        except EOFError: pass
    text=''.join(pieces)
    need(pieces and pieces[-1].startswith('MK2_NAT_CAMPAIGN_STAGE ') and ' stage=2 ' in pieces[-1] and pieces[-1].endswith('\n'),
         'Complete native prefix through earned admission to stage2, not observation time')
    need(text.count('MK2_CURRENT_CAMPAIGN_PHYSICAL_POLICY ')==1 and
         not re.search(r'MK2_CURRENT_CAMPAIGN_CACHE_FAILURE |MK2_MILEENA_CAMPAIGN_OVERRUN |LUA ERROR|stack traceback|fatal error',text),
         'Actual late loader ran once and original observed prefix contains no native errors/cache overruns')
    replay,source=replay_factory();positive=replay(text);rows=old.parse(text)
    guard=[r for r in rows if r['tag']=='GUARD_FIELD'];specials=[r for r in rows if r['tag']=='SPECIAL' and r['move']=='leg']
    need({r['cpu_id'] for r in guard}=={'17','18'} and positive['actualNativeLegActivations']>=4 and
         positive['reasons'].get('leg_attempt',0)>=4 and positive['actualOwnNativeRoundWins']>=4 and
         positive['stages']==[0,1,2] and all(r['fighter']=='sonya' and r['human_slot']=='1' for r in rows),
         'Actual two true opponents, repeated own native leg entries, original button edges, earned round wins and next-stage admission')
    damage=[r for r in rows if r['tag']=='HEALTH' and r['slot']=='2' and r['pc']=='FF836700' and int(r['after'])<int(r['before'])]
    need(damage,'Actual native CPU health decreases observed, not planned inputs')
    target=next(r['frame'] for r in rows if r['tag']=='GUARD_DECISION' and r['reason']=='leg_attempt')
    field=next(r for r in guard if r['frame']==target);faults=[]
    def reject(name,bad):
        need(bad!=text,'Each actual semantic counterexample changes captured evidence')
        try: replay(bad)
        except (ValueError,AssertionError) as error: faults.append(dict(fault=name,rejectedBy=str(error)))
        else: raise ValueError('False actual physical/native evidence accepted: '+name)
        need(replay(text)==positive,'Entire real positive restored after every semantic fault')
    for key,value in [('human_id','0'),('human_roster','0'),('cpu_id','0'),('cpu_roster','1'),
                      ('human_owner','01000000'),('cpu_owner','01000000'),('health','0,161'),
                      ('reset',1-int(field['reset'])),('human_action',0x500),('cpu_action',0x507)]:
        reject('field_'+key,old.change(text,'GUARD_FIELD',target,key,value))
    reject('wrong_native_decision',old.change(text,'GUARD_DECISION',target,'reason','stance_guard'))
    reject('wrong_actual_input',old.change(text,'INPUT',target,'button','Up'))
    for tag in ('GUARD_FIELD','GUARD_DECISION'):
        line=next(s for s in text.splitlines() if s.startswith(f'MK2_NAT_CAMPAIGN_{tag} frame={target} '))
        reject('missing_'+tag,text.replace(line+'\n','',1))
    action=next(r for r in rows if r['tag']=='GUARD_ACTION')
    action_line=next(s for s in text.splitlines() if s.startswith(f"MK2_NAT_CAMPAIGN_GUARD_ACTION frame={action['frame']} ") and
                     ' after='+action['after']+' ' in s and ' actor='+action['actor']+' ' in s)
    for key,value in [('owner','01000000'),('at','01000000'),('a8','01000000'),('mask','00FF')]:
        reject('native_action_'+key,text.replace(action_line,re.sub(r'\b'+key+r'=\S+',key+'='+value,action_line,count=1),1))
    first=specials[0]
    for key,value in [('pc','FFF00000'),('a8','01000000'),('roster','1')]:
        reject('native_leg_'+key,old.change(text,'SPECIAL',first['frame'],key,value))
    need(len(faults)==21,'All actual native state/ownership/input/missing-field/activation faults rejected semantically')
    proof=json.loads((folder/'guest_memory_proof.json').read_text())
    meta=json.loads((ROOT/current.prior.prior.NAME/'build-info.json').read_text(encoding='utf-8-sig'))
    before=json.loads((folder/'input_hashes_before.json').read_text())
    need(proof['everyActualByteComparedInRAM'] and proof['bytes']==1048576 and
         proof['sha256']==meta['expected_guest_sha256'] and proof['executableSHA256']==meta['executable_sha256'] and
         proof['payloadSHA256']==meta['payload_sha256'] and proof['captureSourceSHA256']==sha(current.__file__) and
         proof['transportSourceSHA256']==sha(ROOT/current.LUA) and all(sha(p)==h for p,h in before.items()),
         'Entire independently reconstructed actual current guest/executable/payload/executed source proof intact')
    actual_after=next((q for q in census.census() if q['ProcessId']==GAME),None)
    need(actual_after==actual,'Same original real live job after replay, never restarted')
    pins=dict(before)
    for p in [Path(__file__),Path(old.__file__),Path(current.__file__),folder/'native_identity.json',
              folder/'guest_memory_proof.json',folder/'input_hashes_before.json',current.SOURCE/'report.json',current.INIT/'report.json']:
        pins[str(p.resolve())]=sha(p)
    OUT.mkdir()
    with gzip.open(OUT/'actual_original_native_prefix.log.gz','wt',encoding='utf-8') as stream: stream.write(text)
    with gzip.open(OUT/'whole_original_physical_replay_source.json.gz','wt',encoding='utf-8') as stream: json.dump(dict(wholeReplaySource=source),stream)
    for p in OUT.iterdir(): pins[str(p.resolve())]=sha(p)
    report=dict(passed=True,finitePhysicalPrefixAccepted=True,actualNativeIdentity=actual,originalPTYSession=7157,
        actualWholeOriginalGuardInputReplay=positive,actualCounterexamplesRejected=faults,
        trueOpponentIDs=[17,18],actualCPUDamageStoreCount=len(damage),
        damageScope='Observed original FF836700 CPU health stores; full move damage/choreography proof remains separate',
        guestProof=proof,nativePrefixBytes=len(text.encode()),nativePrefixSHA256=hashlib.sha256(text.encode()).hexdigest().upper(),
        everyOriginalObservedGuardFieldRetained=True,originalStage2Admission=pieces[-1].strip(),
        originalRequirements=json.loads((current.SOURCE/'report.json').read_text())['originalNaturalIntegrationRequirements'],
        remainingWorkGroups=json.loads((current.SOURCE/'report.json').read_text())['originalRemainingWorkGroups'],
        inputHashes=pins,actualCampaignStillLive=True,endingReached=False,postEndingJoinAccepted=False,
        fullTowerAccepted=False,fullPixelShadowAudioAcceptance=False,fullPortAcceptance=False,goalStatus='active',
        newBuilds=0,newROMCopies=0,newRawMedia=0,newZIPs=0,publicPlayableChanged=False,
        nextAction='Continue observing the same original session7157/native176712/parent186024 to actual terminal. Never restart on an observation timeout.')
    (OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(passed=True,actualGuardFields=positive['actualCompleteGuardFields'],nativeLegEntries=positive['actualNativeLegActivations'],
        ownRoundWins=positive['actualOwnNativeRoundWins'],faults=len(faults),sameNativeLive=GAME,fullTowerAccepted=False)),flush=True)


if __name__=='__main__':
    try: run()
    except Exception as error:
        need(not OUT.exists(),'Preserve immutable original qualifier result');OUT.mkdir()
        (OUT/'failure.json').write_text(json.dumps(dict(passed=False,error=repr(error),traceback=traceback.format_exc(),
            fullPortAcceptance=False,goalStatus='active'),indent=2)+'\n')
        print(json.dumps(dict(passed=False,error=repr(error),traceback=traceback.format_exc())),flush=True)
