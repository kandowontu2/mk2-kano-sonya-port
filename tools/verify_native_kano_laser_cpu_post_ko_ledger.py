"""Native earned KO/reset/resume, exact all-mode health and true owned identities.

Entire original all-mode source/store replay contract retained, with its fixed
1800-field window replaced by the actual event-derived end after next-round
resume. No fabricated native fields, substituted ordinary controls or full
post-KO art/audio/ladder/all-CPU acceptance.
"""
import inspect
import re
import verify_native_cpu_ring_v2971 as original
import capture_native_kano_laser_cpu_leg_children as capture

ROOT,need,once=capture.ROOT,capture.need,capture.once


def rows(text,tag):
    return [dict(re.findall(r'(\w+)=([^\s]+)',s))for s in text.splitlines()if s.startswith('MK2_POST_KO_'+tag+' ')]


def check(b,guest,payload,gfx):
    text=b['cpuLog']
    begin,ko,resumed,end,result=(rows(text,t)for t in ('BEGIN','KO','RESUMED','END','RESULT'))
    need(all(len(v)==1 for v in (begin,ko,resumed,end,result)) and not rows(text,'FAILED'),
         'One actual first match, earned KO, next-round resume and event-defined terminal; no observation timeout')
    first,death,restart,last=(int(v[0]['frame'])for v in (begin,ko,resumed,end))
    need(first<death<restart<last and last==restart+60 and int(result[0]['frame'])==last and
         result[0]['reason']=='declared_observation_exit','Exact sixty-field native post-reset observation')
    for r in [*begin,*ko,*resumed,*end,*result]:
        need(r['ids']=='18,18' and r['states']=='1,0' and r['stage']=='0' and
             r['writes']=='0' and r['assistance']=='none','Native Sonya mirror identities/roles without state writes')
    need(ko[0]['hp'].split(',')[0]=='0' and resumed[0]['hp']=='161,161' and
         resumed[0]['mode']=='2' and end[0]['mode']=='2','Actual HP-zero loss and full-health native next combat')
    source=inspect.getsource(original.health_ledger)
    source=once(source,
        "need(last-first==1800 and len(fields)==len(by)==3602 and set(by)=={(f,s)for f in range(first,last+1)for s in (1,2)},'Every all-mode physical callback, no omitted round or transition fields')",
        "need((first,last)==event_window and len(fields)==len(by)==2*(last-first+1) and set(by)=={(f,s)for f in range(first,last+1)for s in (1,2)},'Every actual event-bounded all-mode callback, including KO/winner/reset/precombat/resumed match')")
    # The exact observed native schedule, not an older fixture's schedule.
    source=once(source,"row['schedule']==0xfffa3180","row['schedule']==actual_schedule")
    scope=dict(vars(original),event_window=(first,last),actual_schedule=int(begin[0]['schedule'],16))
    exec(compile(source,__file__+'::whole_original_all_mode_HP_source_replay_event_bound_current_schedule','exec'),scope)
    health,by=scope['health_ledger'](text,guest,'sonya')
    stores=original.rounds.rows(text,'HEALTH')
    lethal=[r for r in stores if r['slot']==1 and r['mode']==2 and r['before']>0 and r['after']==0]
    need(len(lethal)==1 and lethal[0]['frame']<death and
         by[death,1]['hp']==0 and by[death-1,1]['hp']>0,
         'Exact native collision KO store accounts for the first independently observed zero callback')
    reset=health['actualRoundResets']
    need(len(reset)==2 and {r['slot']for r in reset}=={1,2} and
         all(death<r['frame']<restart and r['after']==161 for r in reset),
         'Both true physical lifebars reset through original native mode6 routines')
    modes=[]
    for frame in range(first,last+1):
        own,victim=by[frame,2],by[frame,1]
        need(all(own[k]==victim[k]for k in ('mode','states','ids','stage','schedule','winner')),
             'Both physical observers agree on every native mode, winner and owned roster publication')
        if not modes or own['mode']!=modes[-1]:modes.append(own['mode'])
    need(modes==[2,5,6,7,2],'Actual untouched combat/winner/round-init/precombat/combat progression')
    for frame in range(restart,last+1):
        for slot in (1,2):
            r=by[frame,slot]
            need(r['mode']==2 and r['valid']==1 and r['owner']==r['actor'] and r['id']==18 and
                 r['floor']==217-135 and 0<r['hp']<=161,
                 'Both rebuilt true Sonya actors remain actually owned and grounded in live next-round combat')
    return dict(passed=True,first=first,earnedKO=death,actualNativeResume=restart,last=last,
                actualModes=modes,health=health,physicalPostResetFields=2*(last-restart+1),
                actualNativeHealthStores=len(stores),wholeGuestCurrentByteCompared=True,
                originalAllModeHealthReplayRetained=True,actualNativeRoundResetVerified=True,
                fullPostKOBodyShadowAcceptance=False,postResetOrdinaryResponseAcceptance=False,
                fullAudioAcceptance=False,allCPUContextsAccepted=False,fullPortAcceptance=False,scope=__doc__)
