"""Finite natural CPU Kano finisher, real lookup, clean handoff/transition proof."""
import copy,gzip,hashlib,json,re,struct,subprocess
from pathlib import Path
import native_cpu_finisher_dispatch_context as native
ROOT,need,sha=native.ROOT,native.need,native.sha
RUN=ROOT/'audit_native_cpu_finisher_repair_regression_current_oracle'
OUT=ROOT/'audit_native_cpu_finisher_repair_regression_checked'
def rows(text,prefix):
    return [dict(re.findall(r'(\w+)=([^\s]+)',s))for s in text.splitlines()if s.startswith(prefix)]
def gate(events,guest):
    get=lambda name:next(r for r in events if r['tag']==name)
    lookup,entry,handoff,result=(get(n)for n in ('LOOKUP','OWN_FINISH','WINNER_HANDOFF','RESULT'))
    need(lookup['a1']=='FFFA1900' and lookup['a0']=='FFFAAE00' and lookup['pc']=='FF83B860',
         'Actual native ID-indexed first performer lookup returns Kano owned action')
    need(entry['pc']=='FFFAAE10' and entry['frame']==lookup['frame']=='36170',
         'Original cold physical replay reaches corrected finisher at same original lookup field')
    for r in (lookup,entry,handoff):
        need(r['id']==r['roster']=='17' and r['actor']=='010350A0' and r['main']=='010749F0' and
             r['mode']=='2' and r['state']=='0' and r['health']=='0,109' and
             r['writes']=='0' and r['assistance']=='none','Actual physical CPU Kano, natural earned win, mode/ownership')
    need(handoff['pc']=='FFA14870' and int(handoff['frame'])>36170 and
         result['started']=='36170' and result['completed']==handoff['frame'] and
         int(result['frame'])==37070,'Native owned finisher completes and exact900-field observation ends normally')
    need(not any(r['tag']=='WRONG_MILEENA_ENTRY' for r in events),'Never substitute Mileena performer')
    rd=lambda bit:struct.unpack_from('<I',guest,(bit-0xff800000)//8)[0]
    need(rd(0xff876b50)==0xfffa1900 and rd(0xfffa1900+17*32)==0xfffaae00 and
         rd(0xfffa1900+18*32)==0xfffab200 and rd(0xff876b90)==0xfffa1b60,
         'Actual complete guest contains exact independently qualified owned17/18 tables')
    return dict(lookupFrame=36170,ownedFinishCompletedFrame=int(handoff['frame']),
        terminalFrame=int(result['frame']),postLookupObservedFields=900,trueCPUKano=True,
        noCacheOverrun=True,finiteNativeRepairAccepted=True,fullPortAcceptance=False)

def transition_gate(text,events):
    loss=next(r for r in rows(text,'MK2_NAT_CAMPAIGN_LOSS ') if r['number']=='10')
    result=rows(text,'MK2_NAT_CAMPAIGN_RESULT ')[0]
    stop=next(r for r in events if r['tag']=='STOP')
    need(loss['frame']=='36709' and loss['stage']=='0' and loss['human_slot']=='1' and
         loss['fighter']=='sonya' and loss['writes']=='0' and loss['assistance']=='none',
         'Actual native mode3/state2/lost-winner/retired-human-actor guard observes later tenth loss')
    need(result['frame']=='37070' and result['selections']=='11' and result['losses']=='10' and
         result['ending']=='-1' and stop['frame']=='37070' and stop['mode']=='4' and
         stop['actor']=='00000000' and stop['main']=='01068E30' and stop['roster']=='65535',
         'Actual native loss teardown followed by ordinary paid-continue CSS; no invented post-handoff LIVE')
    return dict(lossFrame=36709,continuedSelectionCount=11,terminalSelectionMode=4,
                terminalSelectionSchedulerTask='01068E30',terminalCPUSelectionRosterCleared=True)
def check():
    need(not OUT.exists(),'Fresh immutable finite proof')
    guest=native.expected();meta=json.loads((RUN/'result.json').read_text())
    need(meta['nativeExit']==0 and not meta['nativeCacheOverrunObserved'] and
         not meta['fullPortAcceptance'],'Actual native terminal, no cache writes, no inherited whole-port claim')
    proof=json.loads((RUN/'guest_memory_proof.json').read_text())
    need(proof['everyActualByteComparedInRAM'] and proof['sha256']==hashlib.sha256(guest).hexdigest().upper(),
         'Entire actually initialized1MiB guest matches new compiled independent model')
    text=gzip.open(RUN/'run.log.gz','rt',encoding='utf-8').read()
    need(not re.search(r'LUA ERROR|stack traceback|fatal error|access violation|MK2_MILEENA_CAMPAIGN_OVERRUN ',text,re.I),
         'No observer/native error or original global-copy overrun in complete log')
    events=[]
    for line in text.splitlines():
        match=re.match(r'^MK2_FINISH_DISPATCH_REGRESSION_(\w+) ',line)
        if match:events.append(dict(re.findall(r'(\w+)=([^\s]+)',line),tag=match[1]))
    positive=gate(events,guest)
    old=gzip.open(ROOT/'audit_native_cpu_kano_finish_lookup_cause/run.log.gz','rt',encoding='utf-8').read()
    prefix=lambda value:[s for s in value.splitlines() if s.startswith('MK2_NAT_CAMPAIGN_') and
                        'frame='in s and int(re.search(r'frame=(\d+)',s)[1])<36170]
    need(prefix(old)==prefix(text),'Whole original physical campaign trajectory identical until actual corrected lookup')
    first=ROOT/'audit_native_cpu_finisher_repair_regression'
    preserved=json.loads((first/'stale_host_metadata_failure_preserved.json').read_text())
    firsttext=gzip.open(first/'run.log.gz','rt',encoding='utf-8').read()
    trajectory=lambda value:[s for s in value.splitlines()if s.startswith('MK2_NAT_CAMPAIGN_') or
        s.startswith('MK2_FINISH_DISPATCH_REGRESSION_') or s.startswith('MK2_CAMPAIGN_RAM_FRAME_DIGEST ')]
    need(preserved['hostOracleFailure'] and preserved['nativeExit']==0 and
         trajectory(firsttext)==trajectory(text),
         'Same entire native trajectory and every raster digest reproduced after host-only oracle correction')
    images=[r for r in meta['actualScenes']if r['filename'].startswith('postjoin_finisher_regression_')]
    need({r['filename']for r in images}=={f'postjoin_finisher_regression_age{n}.png'for n in (1,30,90,180,330,900)} and
         len(images)==6 and all(r['bytes']=='406400'and len(r['sha256'])==64 for r in images),
         'Six actual complete native RGB callbacks retained in RAM; not art acceptance by checksum')
    live=rows(text,'MK2_NAT_CAMPAIGN_LIVE ')
    tail=[r for r in live if int(r['frame'])>int(positive['ownedFinishCompletedFrame'])]
    failure=ROOT/'audit_native_cpu_finisher_handoff_checker_failure/report.json'
    failed=json.loads(failure.read_text())
    need(failed['checkerFailure'] and not failed['nativeGameFailure'] and
         all(sha(p)==h for p,h in failed['actualRunInputHashes'].items()),
         'Original overly narrow LIVE-only checker failure and every actual run file preserved')
    controller=ROOT/'mk2ks_natural_campaign_shao_ring_retreat_v3485.lua'
    source=controller.read_text()
    for boundary in (
        'mode==3 and state==2 and winner==opponent and p:read_u32(slots[side].actor)==0',
        "if age>=20 and age<25 or age>=270 and age<275 then press('Coin')end",
        "if age>=310 and age<315 then press('Start')end",
        'mode==4 and state==3 and p:read_u16(slots[side].roster)<=18',
        'css=frame;selections=selections+1;plan=route(p:read_u16(slots[side].roster))'):
        need(boundary in source and meta['inputHashes'][str(controller)]==sha(controller),
             'Whole actually executed physical continue controller and native observation guard '+boundary)
    transition=transition_gate(text,events)
    faults=[]
    for label,tag,key,value in (
        ('proxy_identity','OWN_FINISH','id','1'),('wrong_physical_actor','OWN_FINISH','actor','01034E90'),
        ('unearned_full_health','OWN_FINISH','health','161,109'),('attract_not_game','OWN_FINISH','mode','1'),
        ('wrong_performer_result','LOOKUP','a0','FF8D2410'),('original_short_table','LOOKUP','a1','FF8BA210'),
        ('no_winner_handoff','WINNER_HANDOFF','pc','FF838860'),('early_host_exit','RESULT','frame','36316')):
        changed=copy.deepcopy(events);next(r for r in changed if r['tag']==tag)[key]=value
        try:gate(changed,guest)
        except (ValueError,StopIteration)as error:faults.append(dict(name=label,rejected=str(error)))
        else:raise ValueError('Actual finite runtime fault admitted: '+label)
    need(gate(events,guest)==positive,'Complete original runtime positive restored after eight faults')
    for label,before,after in (
        ('wrong_later_loss','number=10 stage=0','number=10 stage=1'),
        ('no_new_selection','selections=11 losses=10','selections=10 losses=10'),
        ('wrong_selection_scheduler','actor=00000000 main=01068E30','actor=00000000 main=010749F0'),
        ('still_gameplay','health=0,109 mode=4 state=0','health=0,109 mode=2 state=0')):
        need(before in text,'Actual continuation counterexample boundary')
        changed=text.replace(before,after)
        changed_events=copy.deepcopy(events)
        stop=next(r for r in changed_events if r['tag']=='STOP')
        if label=='wrong_selection_scheduler':stop['main']='010749F0'
        if label=='still_gameplay':stop['mode']='2'
        try:transition_gate(changed,changed_events)
        except (ValueError,StopIteration)as error:faults.append(dict(name=label,rejected=str(error)))
        else:raise ValueError('Actual continuation fault admitted: '+label)
    need(transition_gate(text,events)==transition,'Exact actual continuation positive restored')
    pins=dict(meta['inputHashes']);need(all(sha(p)==h for p,h in pins.items()),'All actual compiled and executed inputs frozen')
    pins.update({str(p.resolve()):sha(p)for p in [Path(__file__),failure,*(p for p in RUN.iterdir()if p.is_file())]})
    return dict(passed=True,**positive,wholeOriginalPreLookupTrajectoryConserved=True,
        actualNativeRGBScenes=images,actualNativeLiveRows=len(live),postHandoffNativeRows=len(tail),
        actualNativePostHandoffTransition=transition,
        actualFaultsRejected=faults,inputHashes=pins,visualReviewPending=True,audioAcceptance=False,
        otherSlotAndSecondFinisherRuntimeAccepted=False,allOriginalGoalRequirementsStillActive=True,
        publicBuildPromoted=False,goalStatus='active')
if __name__=='__main__':
    report=check();OUT.mkdir();(OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    subprocess.run(['compact.exe','/C','/EXE:LZX','/F','/I','/Q',str(OUT/'report.json')],check=True,capture_output=True)
    print(json.dumps({k:v for k,v in report.items()if k not in ('inputHashes','actualFaultsRejected','actualNativeRGBScenes')},indent=2))
