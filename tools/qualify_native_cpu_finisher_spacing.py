"""Actual owned CPU distance/entry/continuous geometry/clean native continuation."""
import copy,gzip,hashlib,json,re,struct,subprocess
from pathlib import Path
import native_cpu_finisher_spacing_context as native
ROOT,need,sha=native.ROOT,native.need,native.sha
RUN=ROOT/'audit_native_cpu_finisher_spacing_child'
OUT=ROOT/'audit_native_cpu_finisher_spacing_child_checked'

def rows(text,prefix):
    return [dict(re.findall(r'(\w+)=([^\s]+)',s)) for s in text.splitlines() if s.startswith(prefix)]

def gate(spacing,dispatch,fields,states,losses,result,guest,expected,children):
    need(guest==expected,'Every actually initialized byte equals independently qualified six-byte distance-only model')
    lookup=spacing[0];geometry=next(r for r in spacing if r['tag']=='OWN_ENTRY')
    get=lambda tag:next(r for r in dispatch if r['tag']==tag)
    own,handoff,stop,finished=(get(tag) for tag in ('OWN_FINISH','WINNER_HANDOFF','STOP','RESULT'))
    began=int(own['frame']);done=int(handoff['frame']);ended=int(finished['frame'])
    need(lookup['tag']=='LOOKUP' and lookup['a1']=='FFF9CAE0' and lookup['a0']=='00500050' and
         lookup['pc']=='FF83B860' and int(lookup['frame'])<=began,
         'Actual native real-ID distance lookup returns Kano80/80 profile before owned finisher')
    need(geometry['frame']==own['frame'] and geometry['pc']==own['pc']=='FFFAAE10' and
         geometry['age']=='0' and geometry['h_id']==geometry['h_roster']=='18' and
         geometry['k_id']==geometry['k_roster']=='17' and geometry['h_state']=='1' and
         geometry['k_state']=='0' and geometry['h_hp']=='0' and 0<int(geometry['k_hp'])<=161,
         'Natural earned CPU Kano17 P2 win against true human Sonya18 P1, not proxy/forced health')
    for r in (lookup,geometry):
        need(r['mode']=='2' and r['h_actor']==r['h_owner'] and r['k_actor']==r['k_owner'] and
             r['writes']=='0' and r['assistance']=='none','Actual native owner/mode and passive geometry provenance')
    gap=abs(int(geometry['h_x'])-int(geometry['k_x']))
    earned_health='0,'+geometry['k_hp']
    need(int(geometry['gap'])==gap and 0<gap<=80,
         'Actual finisher starts within own legal80pixel reach, never inherited111pixel Cage spacing')
    need(own['actor']==geometry['k_actor'] and own['main']==geometry['k_main'] and
         own['id']==own['roster']=='17' and own['mode']=='2' and own['state']=='0' and
         own['health']==earned_health,'Actually executed action owner matches independently read physical actor')
    need(handoff['pc']=='FFA14870' and handoff['actor']==own['actor'] and handoff['main']==own['main'] and
         handoff['id']==handoff['roster']=='17' and handoff['health']==earned_health and
         handoff['mode']=='2' and handoff['state']=='0' and done>began,
         'Same actual owned CPU finisher reaches original native winner handoff')
    need(finished['started']==own['frame'] and finished['completed']==handoff['frame'] and
         ended==began+900 and stop['frame']==finished['frame'] and stop['mode']=='4',
         'Exactly900 observed native fields after owned entry, with complete handoff and later selection')
    need(not any(r['tag']=='WRONG_MILEENA_ENTRY' for r in dispatch),'No substituted short-table Mileena routine')
    phase=[r for r in fields if 1<=int(r['age'])<=done-began]
    need([int(r['age']) for r in phase]==list(range(1,done-began+1)),
         'Every actual consecutive finisher field through native winner handoff observed, no sampling gaps')
    child_by_frame={r['frame']:r for r in children}
    skeleton_groups={'FE9B22D0','FE9B2310','FE9B2350','FE9B23D0','FE9B2430','FE9B2490'}
    borrowed=[]
    for r in phase:
        need(int(r['frame'])==began+int(r['age']) and r['mode']=='2' and
             r['h_id']==r['h_roster']=='18' and r['k_id']==r['k_roster']=='17' and
             r['h_actor']==r['h_owner']==geometry['h_actor'] and r['h_main']==geometry['h_main'] and
             r['k_actor']==geometry['k_actor'] and r['k_main']==geometry['k_main'] and
             r['h_hp']=='0' and r['k_hp']==geometry['k_hp'] and r['writes']=='0' and r['assistance']=='none',
             'Continuous actual physical identities/owners/health and native ground actors remain stable')
        c=child_by_frame.get(r['frame'])
        need(c and c['age']==r['age'] and c['k_actor']==r['k_actor'] and c['k_main']==r['k_main'] and
             c['saved_a8']==r['k_owner'] and c['k_x']==r['k_x'] and c['k_y']==r['k_y'] and
             c['writes']=='0' and c['assistance']=='none',
             'Independently observed main-task saved A8 and child link in every actual finisher field')
        if r['k_owner']!=r['k_actor']:
            need(c['child_valid']=='1' and c['saved_a8']==c['child'] and
                 c['child'] not in (r['h_actor'],r['k_actor']) and c['child_pose'] in skeleton_groups and
                 c['child_x']==r['k_x'] and c['child_y']==r['k_y'],
                 'Borrowed animation context is exactly the attached native skeleton, never a proxy player')
            borrowed.append(c)
        actual_gap=abs(int(r['h_x'])-int(r['k_x']))
        need(int(r['gap'])==actual_gap and 0<actual_gap<=80 and
             abs(int(r['h_y'])-int(r['h_floor']))<=1 and abs(int(r['k_y'])-int(r['k_floor']))<=1,
             'Continuous actual finisher world distance and native floor anchoring, not UI/body-name substitution')
    need([int(r['age']) for r in borrowed]==list(range(84,132)) and
         {r['child_pose'] for r in borrowed}==skeleton_groups and
         len({r['child'] for r in borrowed})==1,
         'Source-native six eight-field skeleton coroutines borrow one child then restore actual Kano context')
    loss=next(r for r in losses if done<int(r['frame'])<ended)
    lossframe=int(loss['frame'])
    need(loss['stage']=='0' and loss['human_slot']=='1' and loss['fighter']=='sonya' and
         loss['writes']=='0' and loss['assistance']=='none',
         'Subsequent actual unassisted native loss state, not assumed winner presentation')
    departed=[r for r in states if done<int(r['frame'])<=lossframe and r['mode']=='3' and
              r['states']=='2,0' and r['winner']=='2' and r['actors'].split(',')[0]=='00000000']
    selected=[r for r in states if lossframe<int(r['frame'])<=ended and r['mode']=='4' and
              r['states'].split(',')[0]=='3']
    need(departed and selected and int(result['selections'])==int(loss['number'])+1 and
         result['losses']==loss['number'] and int(result['frame'])==ended and result['ending']=='-1',
         'Actor teardown, native loss and ordinary paid-continue CSS admitted after physical Coin/Start')
    return dict(ownedEntryFrame=began,ownedEntryGap=gap,ownedHandoffFrame=done,
        continuousFinisherGeometryFields=len(phase),finisherFields=done-began,
        terminalFrame=ended,laterNativeLossFrame=lossframe,continuedSelectionCount=int(result['selections']),
        nativeProfileFirstDistance=80,nativeProfileSecondDistance=80,
        borrowedSkeletonContextFields=len(borrowed),
        finiteNativeKanoDistanceAccepted=True,fullPortAcceptance=False)

def tagged(text,prefix):
    answer=[]
    for line in text.splitlines():
        match=re.match(r'^'+re.escape(prefix)+r'(\w+) ',line)
        if match:answer.append(dict(re.findall(r'(\w+)=([^\s]+)',line),tag=match[1]))
    return answer

if __name__=='__main__':
    need(not OUT.exists(),'Fresh immutable actual spacing proof')
    guest=native.expected();meta=json.loads((RUN/'result.json').read_text())
    proof=json.loads((RUN/'guest_memory_proof.json').read_text())
    need(meta['nativeExit']==0 and not meta['nativeCacheOverrunObserved'] and
         proof['everyActualByteComparedInRAM'] and proof['sha256']==hashlib.sha256(guest).hexdigest().upper() and
         not meta['fullPortAcceptance'],'Actual native terminal, entire initialized guest, no global-copy overrun')
    text=gzip.open(RUN/'run.log.gz','rt',encoding='utf-8').read()
    need(not re.search(r'LUA ERROR|stack traceback|fatal error|access violation|MK2_MILEENA_CAMPAIGN_OVERRUN ',text,re.I),
         'Entire actual native run has no observer error or original corrupting cache stores')
    spacing=tagged(text,'MK2_FINISH_SPACING_')
    dispatch=tagged(text,'MK2_FINISH_DISPATCH_REGRESSION_')
    fields=[r for r in spacing if r['tag']=='FIELD']
    children=rows(text,'MK2_FINISH_CHILD_FIELD ')
    decisions=[r for r in spacing if r['tag'] in ('LOOKUP','OWN_ENTRY')]
    states=rows(text,'MK2_NAT_CAMPAIGN_STATE ');losses=rows(text,'MK2_NAT_CAMPAIGN_LOSS ')
    result=rows(text,'MK2_NAT_CAMPAIGN_RESULT ')[0]
    positive=gate(decisions,dispatch,fields,states,losses,result,guest,guest,children)
    previous_spacing=ROOT/'audit_native_cpu_finisher_spacing'
    original_spacing=gzip.open(previous_spacing/'run.log.gz','rt',encoding='utf-8').read()
    preserved=json.loads((ROOT/'audit_native_cpu_finisher_saved_context_checker_failure/report.json').read_text())
    trajectory=lambda t:[s for s in t.splitlines() if s.startswith(('MK2_NAT_CAMPAIGN_',
        'MK2_FINISH_SPACING_','MK2_FINISH_DISPATCH_REGRESSION_','MK2_CAMPAIGN_RAM_FRAME_DIGEST '))]
    need(preserved['checkerFailure'] and not preserved['nativeGameFailure'] and
         all(sha(p)==h for p,h in preserved['actualRunInputHashes'].items()) and
         trajectory(text)==trajectory(original_spacing),
         'Whole original native trajectory and every RGB callback reproduced with independent child provenance')
    source=(ROOT/'source_native_cpu_finisher_spacing/midtunit_m.cpp').read_text()
    for fragment in ('leg_code({0x098c,0x00c0,0x4d69,0xb7a8,0x0190,0x0147,',
        'constexpr unsigned kano_skeleton_arm_phases[]={5,6,6,7,8,8};',
        'leg_movi(0,8); leg_cooperate(native_address(kano_skeleton_animate));'):
        need(fragment in source,'Whole qualified native borrowed-child animation source '+fragment)
    previous=ROOT/'audit_native_cpu_finisher_repair_regression_current_oracle'
    original=gzip.open(previous/'run.log.gz','rt',encoding='utf-8').read()
    until=int(decisions[0]['frame'])
    prefix=lambda value:[s for s in value.splitlines() if s.startswith('MK2_NAT_CAMPAIGN_') and
                        'frame=' in s and int(re.search(r'frame=(\d+)',s)[1])<until]
    need(prefix(text)==prefix(original),'Original complete physical campaign trajectory conserved until first actual changed profile lookup')
    controller=ROOT/'mk2ks_natural_campaign_shao_ring_retreat_v3485.lua'
    need(meta['inputHashes'][str(controller)]==sha(controller) and
         "if age>=310 and age<315 then press('Start')end" in controller.read_text(),
         'Whole actually executed physical paid-continue controller unchanged')
    images=[r for r in meta['actualScenes'] if r['filename'].startswith('postjoin_finisher_regression_')]
    need({r['filename'] for r in images}=={f'postjoin_finisher_regression_age{n}.png' for n in (1,30,90,180,330,900)} and
         len(images)==6 and all(r['bytes']=='406400' and len(r['sha256'])==64 for r in images),
         'Six entire actual native RGB fields captured in RAM, not visual acceptance by checksum')
    faults=[]
    for label,collection,tag,key,value in (
        ('inherited_Cage_profile','decisions','LOOKUP','a0','01100070'),
        ('proxy_identity','decisions','OWN_ENTRY','k_id','1'),
        ('unearned_winner','decisions','OWN_ENTRY','h_hp','161'),
        ('wrong_physical_owner','decisions','OWN_ENTRY','k_owner','01034E90'),
        ('actual_old_wide_gap','decisions','OWN_ENTRY','k_x','171'),
        ('faked_small_gap_field','decisions','OWN_ENTRY','gap','1'),
        ('wrong_native_action','dispatch','OWN_FINISH','pc','FF8D2420'),
        ('missing_native_handoff','dispatch','WINNER_HANDOFF','pc','FF838860'),
        ('early_exit','dispatch','RESULT','frame','36316'),
        ('bad_floor_origin','fields','FIELD','k_y','90')):
        data=dict(decisions=copy.deepcopy(decisions),dispatch=copy.deepcopy(dispatch),fields=copy.deepcopy(fields))
        next(r for r in data[collection] if r['tag']==tag)[key]=value
        try:gate(data['decisions'],data['dispatch'],data['fields'],states,losses,result,guest,guest,children)
        except (ValueError,StopIteration) as e:faults.append(dict(name=label,rejected=str(e)))
        else:raise ValueError('Actual spacing counterexample admitted: '+label)
    missing=fields[1:]
    try:gate(decisions,dispatch,missing,states,losses,result,guest,guest,children)
    except ValueError as e:faults.append(dict(name='missing_consecutive_finisher_field',rejected=str(e)))
    else:raise ValueError('Continuous native geometry gap admitted')
    changed=bytearray(guest);changed[0xf395c+68]^=1
    try:gate(decisions,dispatch,fields,states,losses,result,bytes(changed),guest,children)
    except ValueError as e:faults.append(dict(name='wrong_actual_initialized_guest',rejected=str(e)))
    else:raise ValueError('Actual guest distance corruption admitted')
    for label,key,value in (('wrong_attached_object','child','01034E90'),
        ('unmatched_saved_context','saved_a8','01034E90'),('wrong_skeleton_pose','child_pose','FF00DAC0'),
        ('detached_skeleton_origin','child_x','171')):
        altered=copy.deepcopy(children);next(r for r in altered if r['age']=='90')[key]=value
        try:gate(decisions,dispatch,fields,states,losses,result,guest,guest,altered)
        except ValueError as e:faults.append(dict(name=label,rejected=str(e)))
        else:raise ValueError('Independent child ownership fault admitted: '+label)
    need(gate(decisions,dispatch,fields,states,losses,result,guest,guest,children)==positive,'Whole actual positive restored after counterexamples')
    pins=dict(meta['inputHashes']);need(all(sha(p)==h for p,h in pins.items()),'Every compiled and executed input frozen')
    pins.update({str(p.resolve()):sha(p) for p in [Path(__file__),*(p for p in RUN.iterdir() if p.is_file())]})
    report=dict(passed=True,**positive,actualFaultsRejected=faults,actualNativeRGBScenes=images,
        wholePreChangedProfileTrajectoryConserved=True,wholeOriginalSpacingTrajectoryAndRGBReproduced=True,
        independentChildObjectLinkObserved=True,inputHashes=pins,
        actualVisualReviewPending=True,audioAcceptance=False,SonyaCPURuntimeAccepted=False,
        secondPerformerRuntimeAccepted=False,otherPhysicalSlotRuntimeAccepted=False,
        noNewSecondChoreographyClaim=True,allOriginalGoalRequirementsStillActive=True,
        publicBuildPromoted=False,goalStatus='active')
    OUT.mkdir();(OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    subprocess.run(['compact.exe','/C','/EXE:LZX','/F','/I','/Q',str(OUT/'report.json')],check=True,capture_output=True)
    print(json.dumps({k:v for k,v in report.items() if k not in ('inputHashes','actualFaultsRejected','actualNativeRGBScenes')},indent=2))
