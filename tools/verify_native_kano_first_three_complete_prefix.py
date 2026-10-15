"""Finite real current Kano mirror/Jax/Raiden advances, all observed rows.

Current full guest and original native HP kernels, cold native schedules,
two earned wins per successful match, physical paid continues and owned
knife entries. No tower/ending/art/audio/victim/full-port acceptance.
"""
import hashlib
import inspect
import json
import re
from pathlib import Path
import prepare_native_kano_paired_stumble_host_checked as capture
import prepare_native_kano_paired_stumble_campaign as prepared
import check_native_scorpion_guard_first_five_prefix as reader
import qualify_native_sonya_first_nine_ladder_fights as native_health

ROOT,need,sha=prepared.ROOT,prepared.need,prepared.sha
OUT=ROOT/'audit_native_kano_first_three_complete_prefix_checked'
CUTOFF=30549
COUNTS=dict(LIVE=905,STAGE=3,SELECT_ID=12,WIN=19,LOSS=5,HEALTH=3568,
            ROM=6,STATE=383,SELECT=6,INPUT=29037,SPECIAL=181,CPU_ID=0)
OPPONENTS=(17,11,7)


def fields(rows,hp_gate,rom_oracle):
    need({tag:len(q) for tag,q in rows.items()}==COUNTS,'Entire actual twelve-category finite prefix inventory retained')
    need(rows['ROM']==rom_oracle,'All six actual cold native schedule records equal the separately checked same-guest source schedules')
    for values in rows.values():
        need(all(q['fighter']=='kano' and q['human_slot']=='1' and q['writes']=='0' and q['assistance']=='none' and
                 int(q['frame'])<CUTOFF for q in values),'Every original field is actual unassisted Kano P1 before fixed observed boundary')
    need([int(q['stage']) for q in rows['STAGE']]==[0,1,2] and
         all(q['schedule']=='FFFA3000' for q in rows['STAGE']),'All native cold sequential stages and schedules retained')
    live,states,wins,losses=rows['LIVE'],rows['STATE'],rows['WIN'],rows['LOSS']
    need([int(q['frame']) for q in live]==sorted({int(q['frame']) for q in live}),'Entire unique chronological actual live inventory')
    for q in live:
        expected=OPPONENTS[int(q['stage'])]
        need(q['human']=='17:17' and q['cpu']==f'{expected}:{expected}' and q['schedule']=='FFFA3000' and
             q['human_actor']!=q['cpu_actor'] and q['human_main']!=q['cpu_main'] and
             all(0x01000000<=int(q[k],16)<0x01100000 for k in ('human_actor','cpu_actor','human_main','cpu_main')) and
             all(0<=int(h)<=161 for h in q['health'].split(',')),
             'Every real Kano and scheduled CPU actor/Main/roster/health remains distinct and native')
    successful={}
    ends=[int(q['frame']) for q in rows['STAGE'][1:]]+[CUTOFF]
    for stage,end in enumerate(ends):
        after=max([int(q['frame']) for q in losses if int(q['stage'])==stage]+[int(rows['STAGE'][stage]['frame'])])
        earned=[q for q in wins if int(q['stage'])==stage and q['slot']=='1' and after<int(q['frame'])<end]
        need(len(earned)==2,'Exactly two genuine own round wins after the latest paid loss in each successful match')
        successful[str(stage)]=[dict(frame=int(q['frame']),health=q['health']) for q in earned]
    for q in wins:
        side=int(q['slot']);expected=17 if side==1 else OPPONENTS[int(q['stage'])]
        hp=list(map(int,q['health'].split(',')))
        witness=[s for s in states if int(s['frame'])==int(q['frame'])+1]
        need(side in (1,2) and int(q['id'])==expected and q['entry']==f'{0xfffef800+expected*32:08X}' and
             q['pc']=='FF8296B0' and all(0<=h<=161 for h in hp) and hp[side-1]>hp[2-side] and
             witness and witness[0]['winner']==q['slot'] and witness[0]['health']==q['health'] and witness[0]['mode'] in ('5','11'),
             'Every actual winner table instruction/own row/earned HP has its next-field native winner-state witness')
    selections,confirmed,inputs=rows['SELECT'],rows['SELECT_ID'],rows['INPUT']
    need([int(q['number']) for q in selections]==list(range(1,7)),'All six cold/paid selections retained in original order')
    for q in selections:
        selected=[s for s in confirmed if s['number']==q['number']]
        need(q['target']=='17' and q['schedule']=='FFFA3000' and len(selected)==2 and
             all(s['roster']=='17' and s['state']=='3' for s in selected),'All twelve actual true Kano confirmations, not a Liu proxy')
    edges={(q['button'],int(q['frame'])) for q in inputs}
    for q in losses:
        frame=int(q['frame']);number=str(int(q['number'])+1)
        need(any(s['number']==number and int(s['frame'])==frame+314 for s in selections),
             'Every actual earned loss followed by source-defined paid native selection admission')
        for button,age in [*[('Coin',a) for a in (*range(20,25),*range(270,275))],*[('Start',a) for a in range(310,315)]]:
            need((button,frame+age) in edges,'Every original Coin/Start pulse field retained for all five genuine continues')
    for q in rows['SPECIAL']:
        prior=[l for l in live if int(l['frame'])<=int(q['frame'])][-1]
        need(q['move']=='knife' and q['entry']=='FFFFB000' and q['at']=='FFFFB010' and q['pc']=='FFFFB020' and
             q['id']==q['roster']=='17' and q['actor']==q['a8']==prior['human_actor'] and
             q['main']==q['a13']==prior['human_main'] and q['stage']==prior['stage'],
             'All181 actual native knife instruction entries belong to current true Kano actor/Main, not merely intended inputs')
    health=hp_gate(rows['HEALTH'])
    return dict(completedTrueOpponentIDs=list(OPPONENTS),completedOpponents=['Kano','Jax','Raiden'],
        successfulOwnedRoundWins=successful,nativeWinnerCalls=19,actualOwnedKnifeEntries=181,
        genuinePaidContinues=5,actualLiveFields=905,actualPhysicalInputEdges=29037,nativeHealth=health)


def run():
    need(not OUT.exists(),'Fresh immutable finite current Kano prefix gate')
    identity_path=capture.OUT/'native_identity.json';proof_path=capture.OUT/'guest_memory_proof.json'
    source_path=capture.SOURCE/'report.json';pins_path=capture.OUT/'input_hashes_before.json'
    nine_path=ROOT/'audit_native_sonya_first_nine_ladder_fights_checked/report.json'
    kernel_path=native_health.reset.INIT/'native_reset_kernel_report.json'
    identity,proof,source,pins,nine,kernel=[json.loads(p.read_text()) for p in
        (identity_path,proof_path,source_path,pins_path,nine_path,kernel_path)]
    need(identity in prepared.census.census() and source['passed'] and source['wholePythonHostCompiled'] and nine['passed'] and kernel['passed'] and
         proof['bytes']==1048576 and proof['everyActualByteComparedInRAM'] and proof['guestDumpFilesWritten']==0 and
         proof['sha256']==nine['currentWholeGuestSHA256']==kernel['proof']['wholeGuestSHA256'] and
         proof['captureSourceSHA256']==sha(capture.__file__) and proof['transportSourceSHA256']==sha(ROOT/prepared.LUA) and
         all(sha(p)==h for report in (source,nine,kernel) for p,h in report['inputHashes'].items()) and
         all(sha(p)==h for p,h in pins.items()),'Exact live native identity, full actual initialized guest and all unchanged original compiled/control/kernel evidence bound')
    lines=reader.complete_lines(capture.OUT/'run.log.gz')
    need(not any(l.startswith(('MK2_CURRENT_CAMPAIGN_CACHE_FAILURE ','MK2_MILEENA_CAMPAIGN_OVERRUN ')) for l in lines),
         'No observed corruption in entire actual stream')
    parse=lambda seq,tag:[dict(re.findall(r'(\w+)=([^\s]+)',l)) for l in seq if l.startswith('MK2_NAT_CAMPAIGN_'+tag+' ')]
    admitted=[q for q in parse(lines,'STAGE') if q['stage']=='3']
    need(len(admitted)==1 and int(admitted[0]['frame'])==CUTOFF and admitted[0]['schedule']=='FFFA3000' and
         any(q['stage']=='3' and q['human']=='17:17' and q['cpu']=='4:4' and int(q['frame'])>CUTOFF+120 for q in parse(lines,'LIVE')),
         'Actual next Kitana admission and later true fight fields observed, not a predicted advancement')
    rows={tag:[q for q in parse(lines,tag) if int(q['frame'])<CUTOFF] for tag in COUNTS}
    oracle=parse(reader.complete_lines(reader.OLD/'run.log.gz'),'ROM')
    oracle=[dict(q,fighter='kano') for q in oracle]
    factory=inspect.getsource(native_health.contract)
    factory=native_health.once(factory,'need(len(starts)==221,','need(len(starts)==19,')
    factory=native_health.once(factory,"return scope['fields']","return scope['health_history']")
    scope=dict(vars(native_health),__file__=__file__)
    exec(compile(factory,__file__+'::whole_original_native_health_history19_refills_per_slot','exec'),scope)
    hp_gate=scope['contract'](kernel['proof'])
    positive=fields(rows,hp_gate,oracle)
    trials=[]
    for stage in range(3):
        i=next(i for i,q in enumerate(rows['LIVE']) if int(q['stage'])==stage)
        trials.extend([('LIVE',i,'human','1:1'),('LIVE',i,'cpu','18:1'),('LIVE',i,'human_main','00000000'),('STAGE',stage,'schedule','00000000')])
    trials.extend(('WIN',i,'slot','2') for i,q in enumerate(rows['WIN']) if q['slot']=='1')
    trials.extend([('SPECIAL',0,'pc','FFF00000'),('SPECIAL',180,'a8','01000000'),('SPECIAL',0,'roster','1'),
        ('SELECT_ID',11,'state','1'),('SELECT',0,'target','1'),('ROM',0,'list','00000000')])
    for pc in ('FF9DECE0','FF9DED10','FF9DEF40','FF9DEF70','FF825930','FF825960','FF836700'):
        i=next(i for i,q in enumerate(rows['HEALTH']) if q['pc']==pc);trials.append(('HEALTH',i,'after','65534'))
    first_loss=int(rows['LOSS'][0]['frame'])
    for button,age in (('Coin',20),('Coin',270),('Start',310)):
        i=next(i for i,q in enumerate(rows['INPUT']) if q['button']==button and int(q['frame'])==first_loss+age)
        trials.append(('INPUT',i,'button','High_Punch'))
    faults=[]
    for tag,index,key,value in trials:
        bad=dict(rows);bad[tag]=list(rows[tag]);bad[tag][index]=dict(bad[tag][index],**{key:value})
        try:fields(bad,hp_gate,oracle)
        except (ValueError,IndexError,KeyError) as error:faults.append(dict(tag=tag,row=index,field=key,rejectedBy=str(error)))
        else:raise ValueError('False actual current Kano native evidence admitted')
    for tag in COUNTS:
        if tag=='CPU_ID':continue
        bad=dict(rows);bad[tag]=rows[tag][1:]
        try:fields(bad,hp_gate,oracle)
        except ValueError as error:faults.append(dict(tag=tag,row=0,field='missing',rejectedBy=str(error)))
        else:raise ValueError('Omitted original current Kano record admitted')
    need(fields(rows,hp_gate,oracle)==positive and identity in prepared.census.census(),
         'Entire positive chronology restored and same exact original native identity remains live after fault suite')
    for p in (Path(__file__),Path(capture.__file__),Path(prepared.__file__),Path(reader.__file__),Path(native_health.__file__),
              identity_path,proof_path,source_path,pins_path,nine_path,kernel_path):pins[str(p.resolve())]=sha(p)
    need(all(sha(p)==h for p,h in pins.items()),'Every original actual input stays unchanged after finite gate')
    tags=tuple('MK2_NAT_CAMPAIGN_'+t+' ' for t in COUNTS)
    prefix=[l for l in lines if l.startswith(tags) and int(re.search(r'\bframe=(\d+)\b',l)[1])<CUTOFF]
    OUT.mkdir();(OUT/'report.json').write_text(json.dumps(dict(passed=True,finiteCurrentKanoFirstThreeLadderAdvancesAccepted=True,
        actualNativeIdentity=identity,accepted=positive,completeOriginalInventory=COUNTS,cutoffExclusive=CUTOFF,
        actuallyObservedFinalPrefixField=max(int(re.search(r'\bframe=(\d+)\b',l)[1]) for l in prefix),
        completeOriginalPrefixRows=len(prefix),completeOriginalPrefixSHA256=hashlib.sha256(''.join(prefix).encode()).hexdigest().upper(),
        actualNextStage=admitted[0],semanticFaultsRejected=faults,explicitUnobservedCPU_IDCategory=True,
        fullTowerAccepted=False,endingAccepted=False,freshJoinAccepted=False,KanoPairedVictimAccepted=False,
        artAccepted=False,audioAccepted=False,allFinishersAccepted=False,fullPortAcceptance=False,
        originalNaturalIntegrationRequirements=source['originalNaturalIntegrationRequirements'],
        originalRemainingWorkGroups=source['originalRemainingWorkGroups'],inputHashes=pins,
        newBuilds=0,newNativeBoots=0,newROMCopies=0,newRawMedia=0,newZIPs=0,goalStatus='active'),indent=2)+'\n')
    print(json.dumps(dict(passed=True,finiteCurrentKanoFirstThreeLadderAdvancesAccepted=True,actualNativePID=identity['ProcessId'],
        accepted=positive,semanticFaultsRejected=len(faults),fullPortAcceptance=False)),flush=True)


if __name__=='__main__':
    try:run()
    except Exception as error:
        need(not OUT.exists(),'Preserve original actual finite Kano gate outcome')
        OUT.mkdir();(OUT/'failure.json').write_text(json.dumps(dict(passed=False,error=repr(error),fullPortAcceptance=False),indent=2)+'\n')
        raise
