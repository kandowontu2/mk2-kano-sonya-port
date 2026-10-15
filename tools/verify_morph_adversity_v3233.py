"""Full paired human morphology interruptions, KO/round reset and repetition.

Normal buttons and complete real health ledger, no memory/CPU/RNG assistance.
This does not certify direct shadow/raster/erase, audio, arenas, CPU or endings.
"""
import inspect,json,re,traceback,struct
from collections import defaultdict
from pathlib import Path
import verify_native_friendship_palette_assembly_v2750 as assembly
import verify_human_shang_v3174 as human
ROOT=assembly.ROOT;need=assembly.need
OUT=ROOT/'audit_v3234_morph_adversity_checked'
HEX={'actor','main','owner','pose','action','vx','vy','gravity','flags','body','trail','pc','mask','a8','a13','a9','a0','root','group','palette','event','entry'}
def rows(log,tag):
    records=[]
    for t,r in human.rows(log):
        if t!=tag:continue
        for k,v in tuple(r.items()):
            if k in HEX:r[k]=int(v,16)
            elif re.fullmatch(r'-?\d+',v):r[k]=int(v)
        records.append(r)
    return records
def explicit_attack_schema(log):
    lines=[]
    for line in log.splitlines():
        if line.startswith('MK2_HUMAN_SHANG_ATTACK '):
            # This actual immutable observer used form twice: first provenance
            # kind, then native form-start frame. Require the exact complete
            # grammar before giving the second field its unambiguous name.
            match=re.fullmatch(r'(MK2_HUMAN_SHANG_ATTACK frame=\d+ side=[12] target=(?:kano|sonya) profile=adversity_(?:forward|formed|reverse|ko|repeat_morph) form=(?:added|stock_cage) ordinal=\d+ slot=[12] due=\d+ gap=\d+ choice=-?\d+) form=(-?\d+)( reverse=-?\d+ writes=0)',line)
            need(match is not None,'Exact actual explicit attack provenance-kind/form-start grammar')
            line=match[1]+' form_start='+match[2]+match[3]
        if line.startswith('MK2_HUMAN_SHANG_'):
            keys=re.findall(r'(\w+)=',line)
            need(len(keys)==len(set(keys)),'No unqualified ambiguous actual field names')
        lines.append(line)
    return '\n'.join(lines)

def expected_own_inputs(target,side,phase,form):
    result={};back='Left'if side==1 else'Right';forward='Right'if side==1 else'Left'
    def add(ages,*buttons):
        for age in ages:result[age]=','.join(buttons)
    starts=(100,800,1500)if phase=='repeat_morph'else(300,)if phase=='ko'else(100,)
    for start in starts:
        if form=='stock_cage':
            add((start,start+1,start+4,start+5),back);add((start+8,start+9),'Down','Low_Punch')
        elif target=='kano':
            add((start,start+1),back);add((start+4,start+5),'Down');add((start+8,start+9),back,'Low_Kick')
        else:add(range(start,start+8),'Down','Low_Punch','Block')
    if phase not in('ko','repeat_morph'):
        add(range(1100,1110),forward);add(range(1140,1143),'Up');add(range(1250,1254),'High_Punch')
    return result

def clean(r):
    return r['action']==0x303 and r['y']==r['floor']and r['vx']==r['vy']==r['gravity']==r['trail']==0 and r['flags']&0x1c==0 and r['body']&0x0c==0
def verify_log(log,target,side,phase,form):
    need(target in('kano','sonya')and side in(1,2)and phase in('forward','formed','reverse','ko','repeat_morph')and form in('added','stock_cage'),
      'Explicit independently specified physical case')
    identity=2 if form=='stock_cage'else 17 if target=='kano'else 18
    need(not re.search(r'LUA ERROR|Fatal error|access violation|stack traceback|WRONG CHECKSUMS|might not run correctly',log,re.I),'No native or observer runtime error')
    log=explicit_attack_schema(log)
    profile='adversity_'+phase
    for _,r in human.rows(log):
        need((r['side'],r['target'],r['profile'],r['form'],r['writes'])==(str(side),target,profile,form,'0'),
          'Consistent read-only actual physical case provenance')
    start=rows(log,'MATCH');end=rows(log,'RESULT');css=rows(log,'CSS')
    need(len(start)==len(end)==len(css)==1,'One native CSS/match/terminal lifecycle')
    epoch=start[0]['frame'];last=epoch+2400
    need(css[0]['frame']<epoch and start[0]['own_id']==6 and start[0]['own_roster']==6 and
      start[0]['other_roster']==17 and start[0]['own_state']==start[0]['other_state']==1 and
      start[0]['hp1']==start[0]['hp2']==161 and end[0]['frame']==last and end[0]['errors']==0 and end[0]['match']==epoch,
      'Actual cold two-human Shang/Kano selection and complete terminal2400 fields')
    fields=rows(log,'FIELD')
    need([r['frame']for r in fields]==list(range(epoch,last+1))and[r['age']for r in fields]==list(range(2401)),
      'Every native2401 callback field, including round and postmatch transitions')
    pairs=rows(log,'PAIR');missing=rows(log,'PAIR_MISSING')
    by={(r['frame'],r['slot']):r for r in pairs}
    all_records={(r['frame'],r['slot']):r for r in pairs+missing}
    need(len(all_records)==len(pairs)+len(missing)==4802 and set(all_records)=={(f,s)for f in range(epoch,last+1)for s in(1,2)},
      'Complete actual paired physical actor or missing-publication evidence every callback')
    need(not missing or phase=='ko'and all(r['mode']in(3,6)for r in missing),
      'Missing actor only in native KO round-reinitialization mode6 or postmatch mode3, never live mode2')
    need(all(r['frame']==epoch+r['age']and r['slot']in(1,2)and r['owner']==r['actor']and
      0x01000000<=r['actor']<0x01100000 and 0x01000000<=r['main']<0x01100000 for r in pairs),
      'Every actual published physical actor/Main belongs to its native owner')
    owners={s:(by[epoch,s]['actor'],by[epoch,s]['main'])for s in(1,2)}
    health=rows(log,'HEALTH');at=defaultdict(list)
    for h in health:
        need(h['slot']in(1,2)and h['mask']==0xffff and 0<=h['before']<=65535 and 0<=h['after']<=65535,
          'Exact actual native health word and full mask')
        at[h['frame'],h['slot']].append(h)
    field_by={r['frame']:r for r in fields}
    for f in range(epoch,last):
        for s in(1,2):
            a,b=field_by[f][f'hp{s}'],field_by[f+1][f'hp{s}'];stores=at[f,s]
            if stores:
                need(stores[0]['before']==a and stores[-1]['after']==b and
                  all(x['after']==y['before']for x,y in zip(stores,stores[1:])),
                  'Complete chronological native health ledger including original round refill animation')
            else:need(a==b,'No unexplained guest health changes')
    need(all(epoch<=h['frame']<last for h in health),'No out-of-window or unaccounted terminal health write')
    damage=[h for h in health if h['pc']==0xff836700 and h['before']!=h['after']]
    for h in damage:
        attacker=by[h['frame'],3-h['slot']]
        need(0<=h['after']<h['before']<=161 and (h['a8'],h['a13'])==(attacker['actor'],attacker['main']),
          'Actual original collision damage writer belongs to the opposite real human actor/Main')
    allowed={0xff836700,0xff825930,0xff825960,0xff9dece0,0xff9ded10,0xff9def40,0xff9def70}
    need(all(h['pc']in allowed for h in health),'Every health change uses original collision/round initialization writer, no assistance')
    live=[r for r in pairs if r['mode']==2]
    need(live and all(r['state']==1 and r['roster']==(6 if r['slot']==side else 17)and
      r['id']in((6,identity)if r['slot']==side else(17,))and 0<=r['hp']<=161 and r['pose']>=0xfe800000 and r['trail']==0
      for r in live),'Every actual live native identity/roster/human controller/pose/health/effect state')
    for r in live:
        if r['id']in(6,17,18):
            need(r['floor']=={6:87,17:82,18:81}[r['id']],'Character-owned canonical floor through hit and restoration')
    choices=rows(log,'CHOICE');stores=rows(log,'STORE');reverse=rows(log,'RESTORE_BEGIN')
    forward=[r for r in stores if r['old']==6 and r['id']==identity]
    restores=[r for r in stores if r['old']==identity and r['id']==6]
    need(all(r['id']==identity and r['pc']==0xff86e490 and (r['actor'],r['main'])==owners[side]for r in choices),
      'Real native player-command target choice, never CPU ID alias')
    need(all(r['pc']==0xff86e670 and r['a9']==identity for r in forward)and
      all(r['pc']==0xffa16700 and r['a0']==6 for r in restores)and
      len(stores)==len(forward)+len(restores)and end[0]['forms']==len(forward)and end[0]['restores']==len(restores),
      'All original forward/reverse character stores and observer counts, no unknown identity write')
    own_damage=[h for h in damage if h['slot']==side]
    attacks=rows(log,'ATTACK');inputs=rows(log,'INPUT');op=rows(log,'OPINPUT')
    expected=expected_own_inputs(target,side,phase,form)
    need(len(inputs)==len(expected)and{r['age']:r['buttons']for r in inputs}==expected,
      'Every exact real own morph and postrecovery walk/jump/punch physical input, no missing or duplicate commands')
    need(all(r['frame']==epoch+r['age']and r['actor']==owners[side][0]and
      r['id']==by[r['frame'],side]['id']for r in inputs),
      'Physical player buttons belong to the actual native actor and its current live identity')
    need(all(r['slot']==3-side and r['button']in('Left','Right','Down','High_Punch')for r in op),
      'Opponent uses normal directional/crouch/punch controls only')
    op_by=defaultdict(set)
    for r in op:op_by[r['frame']].add(r['button'])
    for attack in attacks:
        need(attack['slot']==3-side and attack['gap']==abs(by[attack['frame'],side]['x']-by[attack['frame'],3-side]['x']),
          'Every actual normal attack edge binds exact physical published actor positions; misses are not invented contacts')
        need(all('Down'in op_by[f]for f in range(attack['frame']-10,attack['frame']+4))and
          all('High_Punch'in op_by[f]for f in range(attack['frame'],attack['frame']+4)),
          'Actual continuous crouch and complete four-field high-punch edge, not an unexecuted input plan')
    for h in own_damage:
        need(any(by.get((f,3-side),{}).get('action')==0x107 for f in range(h['frame']-8,h['frame']+1))or phase=='ko',
          'Counter really entered native uppercut action before the observed damage')
    summary={}
    if phase=='forward':
        need(len(choices)==1 and not stores and not reverse and len(own_damage)==1 and
          own_damage[0]['before']==161 and own_damage[0]['after']==121 and
          choices[0]['frame']<own_damage[0]['frame']<choices[0]['frame']+16,
          'Actual40HP hit interrupts forward transition before any native form store')
        need(all(r['id']==6 for r in live if r['slot']==side),'Interrupted forward keeps real Shang identity')
        summary['forwardCancelledBeforeIDStore']=True
    elif phase in('formed','reverse'):
        need(len(choices)==len(forward)==len(restores)==1 and len(own_damage)==1 and
          (own_damage[0]['before'],own_damage[0]['after'])==(161,121)and
          forward[0]['frame']<own_damage[0]['frame']<restores[0]['frame']and
          512<=restores[0]['frame']-forward[0]['frame']<=900,
          'One actual40HP interruption and finite original timer/form/restore lifecycle')
        need(reverse and reverse[0]['frame']==forward[0]['frame']+512 and
          all(r['id']==identity and r['pc']==0xffa16310 for r in reverse),
          'Original512-field native restore entry remains independently observed')
        if phase=='reverse':
            need(len(reverse)==2 and reverse[0]['frame']<own_damage[0]['frame']<reverse[0]['frame']+12 and
              own_damage[0]['frame']<reverse[1]['frame']and restores[0]['frame']==reverse[1]['frame']+12,
              'Actually interrupted reverse retries after reaction and completes its real native12-field return')
            summary['reverseInterruptedAndRetried']=True
        else:
            need(len(reverse)==1 and own_damage[0]['frame']<reverse[0]['frame']and restores[0]['frame']==reverse[0]['frame']+12,
              'Actual formed-body uppercut recovers before the normal native return')
        summary['restoreFrame']=restores[0]['frame']
    elif phase=='repeat_morph':
        need(len(choices)==len(forward)==len(restores)==len(reverse)==3 and not damage and not attacks,
          'Three genuine repeated normal morph cycles with no attack or HP assistance')
        for choice,begin,rev,finish in zip(choices,forward,reverse,restores):
            need(choice['frame']<begin['frame']and rev['frame']==begin['frame']+512 and finish['frame']==rev['frame']+12,
              'Each separate native repeated morph retains its own512timer and12field return')
        need(all(a['frame']<b['frame']for a,b in zip(restores,choices[1:])),
          'No overlap or reuse of a prior morph cycle')
        summary['completeRepeatedCycles']=3
    else:
        zeros=[h for h in own_damage if h['after']==0]
        need(zeros and forward and choices and zeros[0]['frame']>forward[0]['frame']and
          by[zeros[0]['frame'],side]['id']==identity and by[zeros[0]['frame'],side]['roster']==6,
          'Actual original collision KO while genuinely morphed, not HP injection or postrestore KO')
        ko=zeros[0]['frame']
        need(any(r['frame']>ko and r['mode']==5 and r['hp']==0 and r['id']==identity for r in pairs if r['slot']==side),
          'Actual imported morphed victim reaches native dead/round-end state')
        recovered=[r for r in live if r['slot']==side and r['frame']>ko+50 and r['hp']==161 and r['id']==6 and r['floor']==87]
        need(recovered,'Native new-round spawn restores real Shang roster/body/full health/own floor without ID assistance')
        reinit=[r for r in missing if r['mode']==6]
        need(not reinit or len(reinit)==2 and{r['slot']for r in reinit}=={1,2}and
          len({r['frame']for r in reinit})==1 and ko<reinit[0]['frame']<recovered[0]['frame'],
          'Only one exact paired native round-initialization gap between real morphed KO and restored next-round actors')
        premorph=[h for h in own_damage if h['frame']<choices[0]['frame']]
        need(len(premorph)==1 and(premorph[0]['before'],premorph[0]['after'])==(161,121)and
          by[premorph[0]['frame'],side]['id']==6,
          'KO qualification starts with one real original40HP uppercut to Shang, not injected pre-morph health')
        summary.update(actualMorphedKOFrame=ko,nativeNextRoundShangFrame=recovered[0]['frame'],
          observedVictimKOCount=len(zeros),fullMatchMayEndNaturally=True)
    if phase!='ko':
        need(all(r['mode']==2 for r in pairs)and not missing,'Entire non-KO game stays in genuine playable mode')
        tail=by[last,side]
        need(tail['id']==6 and clean(tail),'Final genuine restored Shang stance has no attached effect or stuck reaction')
        if own_damage:
            hit=own_damage[0]['frame']
            need(any(clean(r)and r['frame']>hit and r['frame']<hit+170 for r in live if r['slot']==side),
              'Actually interrupted body returns to native standing control within170fields')
        if phase!='repeat_morph':
            own=[r for r in live if r['slot']==side]
            need(any(1100<=r['age']<1130 and r['vx']!=0 for r in own)and
              any(1140<=r['age']<1190 and r['y']<r['floor']and r['action']==0x30b for r in own)and
              any(1250<=r['age']<1280 and r['action']==0x101 for r in own),
              'Real post-interruption/restoration walk jump punch remain responsive')
    # Live IDs may change only after original native stores within each round.
    for f in range(epoch,last):
        a,b=by.get((f,side)),by.get((f+1,side))
        if a and b and a['mode']==b['mode']==2 and a['state']==b['state']==1 and a['id']!=b['id']:
            need(any(r['frame']==f and r['old']==a['id']and r['id']==b['id']for r in stores),
              'Every live identity boundary is explained by its actual native character store')
    return dict(passed=True,target=target,side=side,phase=phase,form=form,
      callbackFields=2401,pairedPhysicalFields=len(pairs),actualMissingPostmatchPublications=len(missing),
      liveHumanFields=len(live),nativeHealthWrites=len(health),actualOwnDamageWrites=len(own_damage),
      originalNativeIDStores=len(stores),originalChoiceEvents=len(choices),nativeHealthWriterPCs=sorted({h['pc']for h in health}),
      actualNormalAttackEdges=len(attacks),summary=summary,
      allCPUArtShadowEraseArenaAudioFinisherBranchesAccepted=False,fullPortAcceptance=False)

def verify():
    need(not OUT.exists(),'Never overwrite adversity evidence')
    dispatch=ROOT/'audit_v3219_morph_adversity_dispatch/report.json'
    job=json.loads(dispatch.read_text())
    expected={(target,side,phase,'added')for target in('kano','sonya')for side in(1,2)
      for phase in('forward','formed','reverse','ko','repeat_morph')}
    expected|={('kano',side,phase,'stock_cage')for side in(1,2)for phase in('forward','reverse')}
    need(job['passed']and job['captures']==24 and
      {(r['target'],r['side'],r['phase'],r['form'])for r in job['cases'].values()}==expected,
      'All24specified normal-human native processes terminal')
    ko_dispatch=ROOT/'audit_v3230_morph_ko_dispatch/report.json'
    ko_job=json.loads(ko_dispatch.read_text())
    need(ko_job['passed']and ko_job['captures']==4 and
      {(r['target'],r['side'],r['phase'],r['form'])for r in ko_job['cases'].values()}==
      {(t,s,'ko','added')for t in('kano','sonya')for s in(1,2)},
      'All four newly qualified normal-hit-prepared real morph KO fixtures terminal')
    pins=assembly.source_check();guest,*_=assembly.expected()
    build=json.loads((ROOT/human.CANDIDATE/'build-info.json').read_text(encoding='utf-8-sig'))
    cases={}
    def pin(path,wanted=None):
        path=Path(path).resolve();actual=assembly.sha(path)
        need(wanted is None or wanted==actual,'Actual immutable capture input '+str(path))
        need(str(path)not in pins or pins[str(path)]==actual,'Consistent current evidence')
        pins[str(path)]=actual
    for target,side,phase,form in sorted(expected):
        key=f'{target}_p{side}_{phase}_{form}';folder=ROOT/f'audit_v{3229 if phase=="ko"else 3217}_morph_adversity_{key}'
        meta=json.loads((folder/'result.json').read_text(encoding='utf-8-sig'))
        before=json.loads((folder/'input_hashes_before.json').read_text(encoding='utf-8-sig'))
        need((meta['exit_code'],meta['lua_errors'],meta['candidate'],meta['target'],meta['side'],meta['phase'],meta['form'],
          meta['executable_sha256'],meta['payload_sha256'],meta['assistance'],meta['cheats_enabled'])==
          (0,0,human.CANDIDATE,target,side,phase,form,human.EXE,human.PAYLOAD,'none',False),
          'Exact actual matched cold native adversity case')
        need(before==meta['input_hashes']and all(before.get(p)==h for p,h in build['input_hashes'].items()),
          'Every compiled dependency frozen before and after native execution')
        need((folder/'guest_maincpu.bin').read_bytes()==guest,'Whole actual initialized guest independently source assembled')
        for file,wanted in before.items():
            pin(file,wanted);source=Path(file)
            if source.suffix in('.lua','.ps1','.json'):pin(folder/'input_sources'/source.relative_to(ROOT),wanted)
            if source.suffix=='.lua':
                need(not re.search(r':write_|write_u\d+|\.value\s*=(?!=)|load_?state|:reset\(',source.read_text()),
                  'Observer supplies no guest ID/HP/CPU/RNG/position/timer/reset writes')
        log=(folder/'run.log').read_text(encoding='utf-8-sig')
        need(log.count('MK2_MORPH_GUEST frame=1 bytes=1048576 start=FF800000 stop=100000000 writes=0')==1,
          'One actual full initialized guest, never fabricated ID trace')
        value=verify_log(log,target,side,phase,form)
        original=(ROOT/'mk2/mk2-maincpu.bin').read_bytes()
        for pc in value['nativeHealthWriterPCs']:
            lo=(pc-128-0xff800000)//8;hi=(pc+128-0xff800000)//8
            context=bytearray(original[lo:hi])
            if pc==0xff836700:
                # Source declares only the nearby indexed damage table base
                # extension here. Preserve every collision/word-store opcode,
                # every17stock callback, and real appended human null callbacks.
                pointer=(0xff836750-0xff800000)//8
                table=0xfe100;stock=(0xff8367b0-0xff800000)//8
                need(struct.unpack_from('<I',original,pointer)[0]==0xff8367b0 and
                  struct.unpack_from('<I',guest,pointer)[0]==0xffff0800 and
                  guest[table:table+17*4]==original[stock:stock+17*4]and
                  guest[table+17*4:table+19*4]==bytes(8),
                  'Actual source-bound19-row damage table retains all17stock callbacks and appended real human null callbacks')
                struct.pack_into('<I',context,pointer-lo,0xffff0800)
            need(guest[lo:hi]==context,
              'Whole actual native health-write context unchanged except exactly source-bound extended-table pointer')
        for file in folder.rglob('*'):
            if file.is_file():pin(file)
        cases[key]=value
        print(key+' full actual native health/identity/round lifecycle passed',flush=True)
    for side in(1,2):
        for phase in('forward','reverse'):
            a=cases[f'kano_p{side}_{phase}_added'];b=cases[f'kano_p{side}_{phase}_stock_cage']
            need(a['originalNativeIDStores']==b['originalNativeIDStores']and
              a['actualOwnDamageWrites']==b['actualOwnDamageWrites']and
              a['actualNormalAttackEdges']==b['actualNormalAttackEdges']and
              a['summary'].get('forwardCancelledBeforeIDStore')==b['summary'].get('forwardCancelledBeforeIDStore')and
              a['summary'].get('reverseInterruptedAndRetried')==b['summary'].get('reverseInterruptedAndRetried'),
              'Actual native stock morphs have the same qualified cancellation/return-retry semantics')
    for p,h in job['inputHashes'].items():pin(p,h)
    for p,h in ko_job['inputHashes'].items():pin(p,h)
    pin(ko_dispatch)
    pin(dispatch);pin(__file__);pin(human.__file__);pin(ROOT/human.CANDIDATE/'build-info.json')
    return dict(passed=True,candidate=human.CANDIDATE,physicalCases=24,completeCallbackFields=57624,
      fullCallbackPhysicalPublications=115248,currentAddedCharacterCases=20,nativeStockComparisonCases=4,
      completeRepeatedMorphCycles=12,allActualFullGuestsSourceBound=True,
      supersededUnqualifiedKOFixtures=4,newActualMorphedKOFixtures=4,
      exactOwnNormalPhysicalInputsAccepted=True,allNativeRoundHealthRefillAnimationStoresAccepted=True,
      actualNativeUppercutForwardCancelFormedHitReverseRetryAndMorphedKORoundResetAccepted=True,
      directArtShadowEraseArenaAudioAndCPUAcceptance=False,fullPortAcceptance=False,cases=cases,inputHashes=pins)

if __name__=='__main__':
    try:value=verify()
    except Exception as error:value=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
    need(not OUT.exists(),'Immutable report')
    OUT.mkdir();(OUT/'report.json').write_text(json.dumps(value,indent=2)+'\n')
    print(json.dumps({k:v for k,v in value.items()if k not in('cases','inputHashes','traceback')},indent=2),flush=True)
    raise SystemExit(0 if value['passed']else 1)
