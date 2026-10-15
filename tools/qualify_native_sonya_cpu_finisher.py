"""Finite true-ID CPU Sonya second-table finisher, earned health and teardown."""
import copy,gzip,hashlib,json,re,subprocess
from pathlib import Path
import native_cpu_finisher_spacing_context as native
import inspect_native_smoke_callers as disasm
ROOT,need,sha=native.ROOT,native.need,native.sha
RUN=ROOT/'audit_native_sonya_cpu_finisher_inventory_checked'
OUT=ROOT/'audit_native_sonya_cpu_finisher_checked'

def rows(text,prefix):
    return [dict(re.findall(r'(\w+)=([^\s]+)',s)) for s in text.splitlines() if s.startswith(prefix)]

def tagged(text,prefix):
    answer=[]
    for s in text.splitlines():
        m=re.match('^'+re.escape(prefix)+r'(\w+) ',s)
        if m:answer.append(dict(re.findall(r'(\w+)=([^\s]+)',s),tag=m[1]))
    return answer

def gate(data,guest_sha):
    meta,proof=data['meta'],data['proof']
    need(meta['passed'] and meta['nativeExit']==0 and not meta['nativeCacheOverrunObserved'] and
         meta['candidate']==native.NAME and meta['executableSHA256']==native.EXE_SHA and
         meta['guestSHA256']==proof['sha256']==guest_sha and proof['bytes']==1048576 and
         proof['executableSHA256']==native.EXE_SHA and proof['payloadSHA256']==native.PAYLOAD_SHA and
         proof['everyActualByteComparedInRAM'] and proof['guestDumpFilesWritten']==0,
         'Actual terminal and complete initialized one-MiB game match the qualified compiled candidate')
    initial=data['initial'][0]
    need(initial['frame']=='1995' and initial['mode']=='2' and
         initial['s_id']==initial['s_roster']=='18' and initial['s_state']=='0' and
         initial['k_id']==initial['k_roster']=='17' and initial['k_state']=='1',
         'Actual native UI admits genuine CPU Sonya18 P1 against human Kano17 P2')
    event=lambda tag:next(r for r in data['events'] if r['tag']==tag)
    distance,performer,own,hand,stop,finished=(event(t) for t in
        ('DISTANCE','PERFORMER','OWN_ENTRY','WINNER_HANDOFF','STOP','RESULT'))
    began,done,ended=(int(r['frame']) for r in (own,hand,stop))
    need(distance['pc']=='FF83B860' and distance['a1']=='FFF9CAE0' and distance['a0']=='00800080' and
         int(distance['frame'])<began and performer['frame']==own['frame'] and
         performer['pc']=='FF83B860' and performer['a1']=='FFFA1B60' and performer['a0']=='FFFAB200' and
         own['pc']=='FFFAB210',
         'Real-ID native128/128 approach and second performer table enter only Sonya owned action')
    def identities(r):
        need(r['s_id']==r['s_roster']=='18' and r['k_id']==r['k_roster']=='17' and
             r['s_actor']==own['s_actor'] and r['s_main']==own['s_main'] and
             r['k_actor']==own['k_actor'] and r['k_main']==own['k_main'] and
             r['s_actor']!=r['k_actor'] and r['s_main']!=r['k_main'] and
             r['s_state']=='0' and r['s_hp']==own['s_hp'] and r['k_hp']=='0' and
             r['stage']=='0' and r['schedule']=='FFFA3780' and
             r['writes']=='0' and r['assistance']=='none',
             'Continuous independently read true physical actors/roster/process/health, not borrowed-register proxies')
    for r in (distance,performer,own,hand):identities(r)
    gap=abs(int(own['s_x'])-int(own['k_x']))
    need(0<int(own['s_hp'])<=161 and 0<gap<=128 and int(own['gap'])==gap and
         own['s_context']==own['s_actor'] and own['k_context']==own['k_actor'] and
         own['mode']=='2' and own['k_state']=='1',
         'Naturally earned CPU win enters within own legal reach and genuine player context')
    need(hand['pc']=='FFA14870' and hand['mode']=='2' and hand['k_state']=='1' and
         hand['s_context']==own['k_actor'] and done>began,
         'Source-native victim animation context reaches original native winner handoff')
    need(stop['started']==finished['started']==own['frame'] and
         stop['completed']==finished['completed']==hand['frame'] and
         stop['frame']==finished['frame'] and ended==began+900 and stop['mode']=='4' and
         stop['losses']==finished['losses']=='10',
         'Complete900-field observation reaches normal paid-continue selection, not assumed cleanup')
    fields=data['fields']
    need([int(r['age']) for r in fields]==list(range(1,539)) and
         int(fields[-1]['frame'])+1==int(data['losses'][-1]['frame']),
         'Every consecutive actual actor field through teardown is present; no fictitious post-teardown actor rows')
    phase=[r for r in fields if int(r['age'])<=done-began]
    need(len(phase)==done-began==231,'Every231 consecutive own finisher fields through handoff observed')
    orb=[];borrowed=[]
    for r in fields:
        identities(r);age=int(r['age'])
        need(int(r['frame'])==began+age and r['k_context']==own['k_actor'] and
             r['s_bank']=='0202' and r['k_bank']=='0303' and
             r['s_x']==own['s_x'] and r['k_x']==own['k_x'] and int(r['gap'])==gap and
             int(r['s_y'])==int(r['s_floor']) and int(r['k_y'])==int(r['k_floor']) and
             r['k_state']==('1' if age<=530 else '2') and
             r['mode']==('2' if age<=232 else '5' if age<=530 else '3'),
             'Native grounded actors, palettes, earned health and precise winner/loss states remain coherent')
        expected_context=own['k_actor'] if 116<=age<=231 else own['s_actor']
        need(r['s_context']==expected_context,
             'Exactly native victim coroutine context116..231 then true Sonya context restored at232')
        if r['s_context']!=own['s_actor']:borrowed.append(r)
        if 56<=age<=115:
            need(r['child_valid']=='1' and r['child'] not in ('00000000',own['s_actor'],own['k_actor']) and
                 r['child_bank']=='0404' and r['s_context']==own['s_actor'],
                 'Native orb is a separately linked child, not an alternate player actor')
            orb.append(r)
        else:need(r['child_valid']=='0' and r['child']=='00000000','Orb retired before victim burn and winner presentation')
    need(len(orb)==60 and len({r['child'] for r in orb})==1 and
         len(borrowed)==116 and orb[-1]['child_x']==own['k_x'] and
         len({(r['child_x'],r['child_y']) for r in orb})>20,
         'Complete moving kiss orb reaches actual victim, retires, and victim coroutine does not replace identity')
    round_start=max(int(r['frame']) for r in data['states'] if
        int(r['frame'])<began and r['mode']=='2' and r['health']=='161,161')
    health=[r for r in data['health'] if round_start<=int(r['frame'])<began]
    damage=[r for r in health if r['slot']=='2']
    last=161
    for r in damage:
        need(r['at']=='01060EC0' and int(r['before'])==last and 0<=int(r['after'])<=last and
             r['pc']=='FF836700' and r['mask']=='FFFF' and r['writes']=='0' and r['assistance']=='none' and
             r['a8'] in (own['s_actor'],own['k_actor']) and r['a13'] in (own['s_main'],own['k_main']),
             'Every winning-round victim HP store comes from native contact with unbroken actual161-to-zero chain')
        last=int(r['after'])
    need(damage and last==0 and int(damage[-1]['frame'])<int(distance['frame']) and
         not any(r['slot']=='1' and r['before']!=r['after'] for r in health),
         'Unassisted native CPU perfect round was earned by actual damage, never injected HP/RNG/AI')
    loss=data['losses'][-1];selection=data['selects'][-1]
    need(loss['number']=='10' and done<int(loss['frame'])<int(selection['frame'])<ended and
         selection['roster']=='9' and selection['route']=='Left,Left,Left,Left' and
         all(r['writes']=='0' and r['assistance']=='none' for r in data['inputs']),
         'Genuine subsequent loss and ordinary native cursor route admitted after Coin/Start')
    after=[r for r in data['states'] if int(r['frame'])>done]
    need(any(r['mode']=='3' and r['states']=='0,2' and r['winner']=='1' for r in after) and
         any(r['mode']=='4' and r['states']=='0,3' and r['actors']=='00000000,00000000' for r in after),
         'Actual winner/loss actors retire before new selection; no persistent in-fight portrait/pose owners')
    expected_names={f'postjoin_sonya_cpu_finish_age{n}.png' for n in (1,30,60,90,180,240,330,450,900)}
    expected_names.add('postjoin_sonya_cpu_finish_winner30.png')
    images=[r for r in meta['actualScenes'] if r['filename'].startswith('postjoin_sonya_cpu_finish_')]
    need(len(images)==10 and {r['filename'] for r in images}==expected_names and
         all(r['bytes']=='406400' and r['width']=='400' and r['height']=='254' and len(r['sha256'])==64 for r in images),
         'All ten complete actual native RGB callbacks available for independent visual review')
    return dict(ownedEntryFrame=began,ownedEntryGap=gap,ownedHandoffFrame=done,
        terminalFrame=ended,continuousFinisherFields=len(phase),continuousActorFieldsThroughTeardown=len(fields),
        nativeVictimAnimationContextFields=len(borrowed),independentlyLinkedOrbFields=len(orb),
        winningRoundNativeHealthStores=len(damage),paidContinueCount=10,
        CPUPhysicalSlot=1,humanPhysicalSlot=2,nativePerformerVariant=2,
        finiteSonyaCPUFinisherAccepted=True,fullPortAcceptance=False)

if __name__=='__main__':
    need(not OUT.exists(),'Fresh immutable finite Sonya qualification')
    guest=native.expected();digest=hashlib.sha256(guest).hexdigest().upper()
    text=gzip.open(RUN/'run.log.gz','rt',encoding='utf-8').read()
    need(not re.search(r'LUA ERROR|stack traceback|fatal error|access violation|MK2_SONYA_CPU_FINISH_OVERRUN ',text,re.I) and
         (RUN/'stderr.log').read_bytes()==b'','Entire actual native run free of observer errors and corrupting cache stores')
    events=tagged(text,'MK2_SONYA_CPU_FINISH_')
    data=dict(meta=json.loads((RUN/'result.json').read_text()),proof=json.loads((RUN/'guest_memory_proof.json').read_text()),
        events=[r for r in events if r['tag'] not in ('FIELD','HEALTH')],
        fields=[r for r in events if r['tag']=='FIELD'],health=[r for r in events if r['tag']=='HEALTH'],
        initial=rows(text,'MK2_SONYA_CPU_CONTINUE_INITIAL '),states=rows(text,'MK2_SONYA_CPU_CONTINUE_STATE '),
        losses=rows(text,'MK2_SONYA_CPU_CONTINUE_LOSS '),selects=rows(text,'MK2_SONYA_CPU_CONTINUE_SELECT '),
        inputs=rows(text,'MK2_SONYA_CPU_CONTINUE_INPUT '))
    positive=gate(data,digest)
    original=ROOT/'audit_native_sonya_cpu_finisher'
    before=gzip.open(original/'run.log.gz','rt',encoding='utf-8').read()
    trajectory=lambda t:[s for s in t.splitlines() if s.startswith(('MK2_UI_','MK2_SONYA_','MK2_CAMPAIGN_RAM_FRAME_DIGEST '))]
    need(trajectory(text)==trajectory(before),
         'All28264 original physical/UI/native health/state/geometry and RGB rows exactly reproduced; only initial inventory observer changed')
    preserved=json.loads((original/'missing_inventory_callback_failure_preserved.json').read_text())
    need(preserved['nativeExit']==0 and not preserved['nativeGameFailure'] and
         preserved['requiredWholeGuestInventoryMissing'] and
         all(sha(p)==h for p,h in preserved['originalInputHashes'].items()),
         'Actual executed failed observation and every original source preserved, not rewritten into a pass')
    source=(ROOT/'source_native_cpu_finisher_spacing/midtunit_m.cpp').read_text()
    for fragment in ('leg_code({0xb20a,0x00c0,0xb34d,0x0190,0x0960});',
        'leg_call(0xff83efd0);','leg_movi(0,4); leg_cooperate(0xff842360);',
        'leg_call(0xff8cdc40);','leg_branch(0xc080,0xffa14860);'):
        need(fragment in source,'Whole actual compiled native orb/victim/retirement/winner source '+fragment)
    instructions={int(s.split(':',1)[0],16):s.split(':',1)[1].strip() for s in disasm.disassemble()}
    helper={0xff842360:'MMTM   A12,A8,A9',0xff842390:'MOVE   *A13(140h),A8,1',
        0xff8423f0:'JA     FF83C340h',0xff842430:'MMFM   A12,A8,A9'}
    need(all(instructions.get(at)==s for at,s in helper.items()),
         'Original native victim coroutine explicitly saves own A8, animates opponent, then restores saved context')
    faults=[]
    def reject(label,collection,index,key,value):
        altered=copy.deepcopy(data)
        target=altered[collection] if index is None else altered[collection][index]
        target[key]=value
        try:gate(altered,digest)
        except (ValueError,StopIteration) as e:faults.append(dict(name=label,rejected=str(e)))
        else:raise ValueError('Native Sonya counterexample admitted: '+label)
    for label,collection,tag,key,value in (
        ('old_Cage_profile','events','DISTANCE','a0','01100070'),
        ('short_native_second_table','events','PERFORMER','a1','FF8BA390'),
        ('wrong_finisher_action','events','PERFORMER','a0','FF8D2410'),
        ('proxy_player_identity','events','OWN_ENTRY','s_id','1'),
        ('unearned_victim_health','events','OWN_ENTRY','k_hp','161'),
        ('fake_small_reach','events','OWN_ENTRY','gap','1'),
        ('missing_winner_handoff','events','WINNER_HANDOFF','pc','FF838860'),
        ('wrong_handoff_victim_context','events','WINNER_HANDOFF','s_context','0102FE20'),
        ('early_observation_exit','events','STOP','frame','22934')):
        reject(label,collection,next(i for i,r in enumerate(data[collection]) if r['tag']==tag),key,value)
    for label,age,key,value in (
        ('shifted_floor_origin',30,'s_y','83'),('detached_orb_child',60,'child','010350A0'),
        ('wrong_orb_bank',60,'child_bank','0303'),('missing_victim_context',180,'s_context','01034E90'),
        ('context_not_restored',232,'s_context','010350A0'),('changed_actual_roster',240,'k_roster','1'),
        ('victim_health_regeneration',330,'k_hp','1')):
        reject(label,'fields',next(i for i,r in enumerate(data['fields']) if r['age']==str(age)),key,value)
    last_damage=max(i for i,r in enumerate(data['health']) if int(r['frame'])<positive['ownedEntryFrame'])
    reject('non_native_HP_injection','health',last_damage,'pc','FFFAB210')
    reject('broken_HP_contact_chain','health',last_damage,'before','161')
    reject('wrong_complete_guest_digest','proof',None,'sha256','0'*64)
    reject('missing_entire_guest_compare','proof',None,'everyActualByteComparedInRAM',False)
    altered=copy.deepcopy(data);altered['fields'].pop(29)
    try:gate(altered,digest)
    except ValueError as e:faults.append(dict(name='missing_consecutive_field',rejected=str(e)))
    else:raise ValueError('Missing native actor field admitted')
    reject('wrong_paid_continue_route','selects',-1,'route','Right')
    need(gate(data,digest)==positive,'Whole finite actual positive restored after counterexamples')
    pins=dict(data['meta']['inputHashes']);need(all(sha(p)==h for p,h in pins.items()),'Every actual compiled/executed dependency frozen')
    pins.update({str(p.resolve()):sha(p) for p in [Path(__file__),Path(disasm.__file__),
        ROOT/'mame-mkp/unidasm.exe',ROOT/'mk2/mk2-maincpu.bin',
        ROOT/'tools/review_native_sonya_cpu_finisher_ram.py',
        original/'missing_inventory_callback_failure_preserved.json',*(p for p in RUN.iterdir() if p.is_file())]})
    report=dict(passed=True,**positive,actualFaultsRejected=faults,inputHashes=pins,
        candidate=native.NAME,executableSHA256=native.EXE_SHA,guestSHA256=digest,
        originalWholeTrajectoryAndEveryRGBCallbackReproduced=True,
        actualNativeRGBScenes=[r for r in data['meta']['actualScenes'] if r['filename'].startswith('postjoin_sonya_cpu_finish_')],
        actualVisualReview=dict(wholeNativeFramesDisplayed=10,rawMediaFilesWritten=0,
            observations=['Kiss launch/orb/victim burn appear in the captured native field order.',
                'Sonya and Kano remain grounded; actual winner text reads SONYA WINS.',
                'No character selection portrait/preview pose persists into finisher or winner presentation.',
                'Age900 shows a genuine new native paid-continue selection screen.'],
            completeAllVictimsArenasFinishersAccepted=False),
        nativeVictimCoroutineInstructions={f'{at:08X}':s for at,s in helper.items()},
        audioAcceptance=False,otherPhysicalSlotAndFirstPerformerRuntimeAccepted=False,
        noNewSecondFinisherChoreographyClaim=True,publicBuildPromoted=False,
        allOriginalGoalRequirementsStillActive=True,goalStatus='active')
    OUT.mkdir();(OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    subprocess.run(['compact.exe','/C','/EXE:LZX','/F','/I','/Q',str(OUT/'report.json')],check=True,capture_output=True)
    print(json.dumps(dict(positive,actualFaultsRejected=len(faults),actualNativeFramesReviewed=10),indent=2))
