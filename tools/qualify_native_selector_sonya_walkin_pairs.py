"""Actual27520 repeated Kano CPU chokes on Sonya plus real missed Knife followup.

Preserve original cycle2 rejection: its ordinary-only post-handoff ledger does
not describe the actual signature move. Admit only the separately source-bound
49-field Knife body,53-field child and actual retirement, then replay both
complete original pair proofs unchanged apart from exact typed action stores.
Third choke is an uncaught attempt, not a completed paired attack.
"""
import copy
import hashlib
import inspect
import json
import re
import struct
import traceback
from pathlib import Path
import capture_native_selector_sonya_walkin_kano_cpu as capture
import qualify_native_selector_opposite_roles_checkpoint as ledger
import native_extended_cpu_pair_contract_v2939 as pair
import verify_current_kano_cpu_overlap_v1963 as knife
import capture_current_subzero_audio_v6213 as dac_model

ROOT,need,sha=capture.ROOT,capture.need,capture.sha
OUT=ROOT/'audit_native_selector_sonya_walkin_pairs_checked'
VIEWS=ROOT/'audit_native_selector_sonya_walkin_actual_views.json'
REJECTION=ROOT/'audit_native_selector_sonya_walkin_original_pair_rejection.json'
rows=ledger.rows


def followup(log,guest,cycle):
    knife.source(log,guest)
    done=[r for r in pair.rows(log,'COMPLETE') if r['cycle']==cycle]
    own=[r for r in pair.rows(log,'OWN_REGAIN') if r['cycle']==cycle]
    need(len(done)==len(own)==1,'Actual completed paired cycle and own native handoff')
    first,last=own[0]['frame'],done[0]['frame']
    entries=[r for r in rows(log,'MK2_HPHASE_CPU_NATIVE_ENTRY') if r['kind']=='knife' and first<int(r['frame'])<last]
    if not entries:return set(),dict(typedKnifeFollowup=False)
    need(cycle==2 and len(entries)==1,'Only actual separately captured second-cycle Knife followup')
    entry=entries[0];start=int(entry['frame']);actor=int(entry['actor'],16);main=int(entry['main'],16)
    need(start==2256 and actor==own[0]['actor'] and main==own[0]['main'] and entry['id']==entry['roster']=='17' and
         entry['state']=='0' and entry['entry']=='FFFFB000' and entry['pc']=='FFFFB010' and
         entry['opcode']=='574A' and entry['mask']=='FFFF','Executing own true Kano signature entry after original choke ready')
    fields={r['frame']:r for r in pair.rows(log,'FIELD') if r['cycle']==cycle}
    body=[fields[f] for f in range(start+1,start+50)]
    for i,r in enumerate(body):
        need(r['actor']==actor and r['main']==main and r['pose']==knife.BODY[17][min(i//3,7)] and
             r['action']==(4 if i<25 else 0x604) and r['flags']&0x1c==0x10 and r['body']&12==4 and
             r['vx']==r['vy']==r['gravity']==r['trail']==0 and r['y']==r['floor']==82 and
             r['xraw']==body[0]['xraw'] and r['yraw']==body[0]['yraw'], 'Every49 actual native Knife body pose/lock/timer/position')
    after=fields[start+50]
    need(after['action']==0x303 and after['flags']&0x1c==after['body']&12==0 and after['trail']==after['vy']==after['gravity']==0,
         'Actual Knife returns to independent walking without carrying paired or signature locks')
    knife.cleanup_store(log,guest,dict(actor=actor,main=main),start+49,2)
    births=[r for r in knife.overlap.rows(log,'CHILD') if r['frame']==start+3]
    need(len(births)==1,'Unique actual native Knife child allocation')
    child=births[0];a,m=child['a8'],child['a13']
    need(child['shot_owner']==actor and child['main_owner']==a and child['id']==17 and child['cycle']==cycle and
         child['entry']==0xfffc6000 and child['pc']==0xfffc6010 and len({actor,main,a,m})==4,
         'Distinct real child/Main/native parent binding')
    retired=[r for r in knife.overlap.rows(log,'RETIRE') if r['a8']==a]
    need(len(retired)==1 and retired[0]['frame']==2312 and retired[0]['a13']==m and retired[0]['shot_owner']==actor and
         retired[0]['pc']==0xff8b6830 and retired[0]['child_cycle']==cycle, 'Exact actual child native retirement under original Main')
    end=retired[0]['frame'];cs=[r for r in knife.overlap.rows(log,'CHILD_FIELD') if r['actor']==a]
    need([r['frame'] for r in cs]==list(range(start+4,end+1)), 'Every53 actual child intro/travel field through native retirement')
    ev=[r for r in knife.overlap.rows(log,'EVENT') if r['kind']=='group' and r['a8']==a]
    need([r['frame'] for r in ev[:6]]==list(range(start+3,start+21,3)) and
         [r['a0'] for r in ev[:6]]==list(knife.INTRO) and [r['frame'] for r in ev[6:]]==list(range(start+22,end)) and
         [r['a0'] for r in ev[6:]]==[knife.FLIGHT[17][i%len(knife.FLIGHT[17])] for i in range(end-start-22)],
         'Whole native child startup cadence and cyclic travel sequence, no invented impact')
    direction=-1 if body[0]['facing']&16 else 1
    for r in cs:
        age=r['frame']-start
        need((r['main'],r['owner'],r['shot_owner'],r['id'],r['type'],r['parameter'],r['child_cycle'],r['vy'],r['body'])==
             (m,a,actor,17,81,0x80000,cycle,0,2), 'Every child owns distinct native Main and real Kano parent')
        if age<=22:
            want=(knife.INTRO[min((age-4)//3,5)],body[0]['xraw']-direction*100*65536,body[0]['yraw']-72*65536,
                  direction*0x80000&0xffffffff if age==22 else 0,0)
        else:
            elapsed=age-23
            want=(knife.FLIGHT[17][elapsed%len(knife.FLIGHT[17])],body[0]['xraw']-direction*12*65536+direction*elapsed*0x80000,
                  body[0]['yraw']-40*65536,direction*0x80000&0xffffffff,0)
        need((r['pose'],r['xraw'],r['yraw'],r['vx'],r['action'])==want, 'Every actual child physical intro/travel tuple matches source, not labels alone')
    need(not [r for r in knife.overlap.rows(log,'HEALTH') if r['a8']==a], 'Actual missed projectile has no borrowed collision/damage proof')
    stores=[r for r in pair.flag_rows(log) if r['slot']==2 and r['cycle']==cycle and r['kind']=='action' and r['pc'] in (0xfffc3890,0xfffc3f70)]
    need([(r['frame'],r['pc'],r['before'],r['after']) for r in stores]==[(2256,0xfffc3890,0x303,4),(2281,0xfffc3f70,4,0x604)],
         'Only actual two source-bound native signature action publications')
    for r in stores:
        need(r['a1']==r['after'] and (r['op0'],r['op1'])==(0xb02d,0x1f0) and r['actor']==actor and r['main']==main and
             r['a8']==actor and r['a13']==main and r['at']==main+0x1f0, 'Exact A1 native signature publication ABI/opcode/address')
        need(struct.unpack_from('<HH',guest,(r['pc']-32-0xff800000)//8)==(r['op0'],r['op1']), 'Actual current signature store source words')
    return {(r['pc'],r['before'],r['after']) for r in stores},dict(typedKnifeFollowup=True,start=start,bodyFields=49,
        child=a,childMain=m,childFields=len(cs),nativeRetirement=end,collisionDamageAccepted=False,actuallyMissed=True)


def paired(log,guest,cycle):
    allowed,proof=followup(log,guest,cycle)
    source=inspect.getsource(pair.verify_pair)
    changes=[("register='a1' if n['pc']==0xff83c340 else 'a0'",
              "register='a1' if n['pc']in(0xff83c340,0xfffc3890,0xfffc3f70) else 'a0'"),
             ("n['pc']==0xff83c340 and n['after']==0x106)",
              "n['pc']==0xff83c340 and n['after']==0x106 or (n['pc'],n['before'],n['after']) in typed_follow_allowed)")]
    for before,after in changes:
        need(source.count(before)==1,'Only exact separately proven typed signature action-store context')
        source=source.replace(before,after,1)
    scope=dict(vars(pair),typed_follow_allowed=allowed)
    exec(compile(source,__file__+'::whole_original_pair_plus_actual_source_bound_knife_publications','exec'),scope)
    value=scope['verify_pair'](log,'sonya',cycle,guest)
    need(value['passed'],'Whole original paired contact/recovery proof '+str(value['errors']))
    return dict(originalPair=value,typedSignatureFollowup=proof)


def execute(state):
    need(not OUT.exists(),'Immutable actual walk-in pair qualification')
    folder,text,images=capture.RAM_CASES[capture.KEY];held=capture.NATIVE_HANDLES[capture.KEY]
    meta=json.loads((folder/'result.json').read_text());transport=json.loads((capture.OUT/'report.json').read_text())
    need(transport['passed'] and meta['passed'] and held['process'].poll()==meta['nativeExit']==0 and
         held['identity']==transport['actualNativeIdentity'] and
         (held['identity']['ProcessId'],held['identity']['ParentProcessId'],held['identity']['createdUnix'])==(27520,38752,1791760361.8604069),
         'Exact original terminal27520, unchanged candidate, actual physical walk-in case')
    rejection=json.loads(REJECTION.read_text())
    need(not rejection['passed'] and rejection['cycles'][0]['passed'] and not rejection['cycles'][1]['passed'] and
         rejection['cycles'][1]['errors']==['Continuous real original action-store instruction/register/ownership ledger'],
         'Original ordinary-only second-cycle rejection retained, not concealed or relabelled')
    pins=dict(transport['inputHashes']);whole=ledger.gate(text,state['guest'])
    completes=pair.rows(text,'COMPLETE');need([r['cycle'] for r in completes]==[1,2],'Exactly two actual completed chokes; third not relabelled')
    positive=[paired(text,state['guest'],r['cycle']) for r in completes]
    faults=[]
    def change(tag,key,value,**where):
        line=next(s for s in text.splitlines() if s.startswith(tag+' ') and all(dict(re.findall(r'(\w+)=([^\s]+)',s)).get(k)==str(v) for k,v in where.items()))
        bad,n=re.subn(r'\b'+key+r'=\S+',key+'='+value,line,count=1);need(n==1 and bad!=line,'Effective actual pair/source corruption')
        return text.replace(line,bad,1)
    cases=[('held_Sonya_pose','MK2_CPU_PAIR_FIELD','vpose','FE829500',dict(frame=2200)),
        ('signature_register','MK2_CPU_PAIR_FLAG','a1','00000005',dict(frame=2256,kind='action',slot=2)),
        ('signature_store_opcode','MK2_CPU_PAIR_FLAG','op0','B00D',dict(frame=2256,kind='action',slot=2)),
        ('signature_native_entry','MK2_HPHASE_CPU_NATIVE_ENTRY','opcode','574B',dict(frame=2256)),
        ('child_parent','MK2_CPU_OVERLAP_CHILD_FIELD','shot_owner','01034E90',dict(frame=2260)),
        ('child_phase','MK2_CPU_OVERLAP_CHILD_FIELD','pose','FF614040',dict(frame=2260)),
        ('child_velocity','MK2_CPU_OVERLAP_CHILD_FIELD','vx','00080001',dict(frame=2280)),
        ('child_retire_main','MK2_CPU_OVERLAP_RETIRE','a13','0106A370',dict(frame=2312))]
    for name,tag,key,value,where in cases:
        bad=change(tag,key,value,**where)
        try:paired(bad,state['guest'],2)
        except (ValueError,AssertionError,KeyError,IndexError) as error:faults.append(dict(name=name,rejectedBy=str(error)))
        else:raise ValueError('Actual typed pair/followup corruption admitted '+name)
    need([paired(text,state['guest'],r['cycle']) for r in completes]==positive and len(faults)==8,
         'Every complete original pair positive restored after eight effective actual faults')
    third=[r for r in pair.rows(text,'EVENT') if r['cycle']==3]
    need(not [r for r in third if r['kind'] in ('step','pulse','release','damage')] and
         [r['frame'] for r in third if r['kind']=='own_ready']==[3151,3213,3309,3407,3505,3599],
         'Third actual uncaught attempt returns to original ready; never falsely completed or persistently locked')
    rasters=ledger.rasters.rasters(images,meta['actualScenes']);need(len(rasters)==175,'Every175 native whole RGB callback digest')
    views=json.loads(VIEWS.read_text());need(views['passed'] and views['actualNativeIdentity']==held['identity'] and
         views['originalIdentityRevalidatedBeforeAndAfter'] and len(views['actualViewedCallbacks'])==12,'Twelve actually viewed exact original native images')
    for r in views['actualViewedCallbacks']:
        a=rasters[r['index']];need(r['header']==a['header'] and r['nativeRGBSHA256']==a['nativeRGBSHA256'] and
            r['SHA256']==a['header']['sha256'] and r['actualReconstructedAlpha']==a['actualReconstructedAlpha'], 'Every actual view bound to complete native pixels')
    audio=capture.AUDIO[capture.KEY]
    for tag,chunks,headers in (('MK2_BBAUDIO_PCM_DIGEST',audio['pcmChunks'],audio['pcmHeaders']),('MK2_NATIVE_DAC_RAM_DIGEST',audio['dacChunks'],audio['dacHeaders'])):
        records=rows(text,tag);need(len(records)==len(chunks)==len(headers)==1645 and all(r==dict(h,sha256=hashlib.sha256(b).hexdigest().upper())
            for r,h,b in zip(records,headers,chunks,strict=True)), 'Complete actual PCM/DAC byte and header digests')
    dg,df,dh=dac_model.dac_models(1645);dac=dg(audio['dacChunks'],audio['dacHeaders'],audio['pcmHeaders']);audio_faults=list(df(audio['dacChunks'],audio['dacHeaders'],audio['pcmHeaders']))
    rg,rf=capture.original.previous.original.audio_model.rom_models(audio['expectedROM'])
    rom=[rg(bytes(audio['rom'][p]),p) for p in ('startup','terminal')]
    for p in ('startup','terminal'):audio_faults.extend(rf(bytes(audio['rom'][p]),p))
    need(len(audio_faults)==12,'Whole native DAC and both sound-ROM corruption suites')
    for p in (Path(__file__),Path(pair.__file__),Path(knife.__file__),Path(dac_model.__file__),VIEWS,REJECTION,capture.OUT/'report.json',
              ROOT/'tools/read_native_selector_sonya_walkin_frames.py',ROOT/'tools/read_native_selector_sonya_walkin_frames_remote.py',
              *(p for p in folder.rglob('*') if p.is_file())):
        p=str(p.resolve());d=sha(p);need(p not in pins or pins[p]==d,'Immutable actual walk-in proof source');pins[p]=d
    need(all(sha(p)==d for p,d in pins.items()),'Entire source/evidence inventory after faults')
    value=dict(passed=True,goalStatus='active',actualNativeIdentity=held['identity'],wholeNativeStateHealthChoices=whole,
        completedPairs=positive,actualPairFollowupFaultsRejected=faults,actualUncaughtThirdAttemptOwnReadyFrames=[3151,3213,3309,3407,3505,3599],
        wholeNativeRGBCallbacks=175,actualViews=views,wholeNativeDAC=dac,nativeDACModelSHA256=dh,wholeSoundROM=rom,
        actualDACROMFaultsRejected=audio_faults,completeStereoFrames=1645*960,inputHashes=pins,
        requirements=transport['requirements'],remainingGroups=transport['remainingGroups'],
        allArenaCPUContextsAccepted=False,fullBodyShadowPixelGeometryAccepted=False,sourceMixedWaveformAccepted=False,
        fullPortAcceptance=False,publicPlayableChanged=False,newNativeGamesDuringQualification=0,newBuilds=0,newROMCopies=0,newRawMediaFiles=0,newZIPs=0)
    OUT.mkdir();(OUT/'report.json').write_text(json.dumps(value,indent=2)+'\n')
    print('PASS two complete source-bound CPU chokes/Sonya recovery, typed missed Knife cleanup, third missed attempt,12 views/whole DAC-ROM',flush=True)
    return value


def safe_execute(state):
    try:return execute(state)
    except Exception as error:
        need(not OUT.exists(),'Preserve actual walk-in qualification rejection')
        OUT.mkdir();(OUT/'failure.json').write_text(json.dumps(dict(passed=False,error=repr(error),traceback=traceback.format_exc(),
            goalStatus='active',fullPortAcceptance=False),indent=2)+'\n')
        raise
