"""Finite combined native chronology; attempted inputs are not actual activation."""
import copy,json,struct
import check_campaign_stage_chronology as chronology
import verify_native_source_sync as sync
sync.verify();root=sync.ROOT;folder=root/'audit_current_combined_smoke_v2_runtime'
rows=chronology.load(folder/'run.log');terminal=json.loads((folder/'terminal.json').read_text(encoding='utf-8-sig'))
assert terminal['exitCode']==0 and terminal['limitReason']is None and terminal['elapsedSeconds']<90
assert terminal['peakWorkingSetBytes']<320*1024**2 and terminal['logBytes']<10*1024**2
assert not(folder/'stderr.log').read_text().strip()
def gate(r):
    captures=r['COMBINED_CAPTURE'];assert [x['label']for x in captures]==['selection','ladder','fight','cleanup']
    assert [x['mode']for x in captures]==['4','7','2','2']
    assert r['SELECT_ID'][-1]['roster']=='17'and r['SELECT_ID'][-1]['state']=='3'
    fight=r['FIGHT'];assert len(fight)==1 and fight[0]['human']=='17:17'and fight[0]['cpu']=='18:18'
    live=r['LIVE'];a=live[0];assert all(x['human']=='17:17'and x['cpu']=='18:18'and x['human_actor']==a['human_actor']and x['human_main']==a['human_main']and x['cpu_actor']==a['cpu_actor']and x['cpu_main']==a['cpu_main']and all(int(y)>0 for y in x['health'].split(','))for x in live)
    assert all(x['mode']=='2'and x['states']=='0,1'and x['roster']=='18,17'for x in r['STATE']if int(x['frame'])>=int(fight[0]['frame']))
    assert not any(r.get(tag)for tag in ['LOSS','WIN'])
    special=r['SPECIAL'];assert len(special)==1;s=special[0]
    assert s['move']=='knife'and s['pc']=='FFFFB020'and s['id']==s['roster']=='17'
    assert s['actor']==s['a8']==a['human_actor']and s['main']==s['a13']==a['human_main']
    recovery=next(x for x in live if int(x['frame'])>int(s['frame'])+20 and x['actions'].split(',')[0]in('0','771','1792'))
    before=next(x for x in live if int(x['frame'])==1750);after=next(x for x in live if int(x['frame'])==1756)
    assert abs(int(after['hpos'].split(',')[0])-int(before['hpos'].split(',')[0]))>=4
    assert r['COMBINED_COMPLETE'][0]['captures']=='4'
    return dict(fight=fight[0],ownedKnife=s,recoveredControlAction=recovery,physicalBackwalkBefore=before,physicalBackwalkAfter=after)
proof=gate(rows);faults=[]
for name in ['wrong truefighter','wrong moveowner','wrong Main','missing recovery','wrong ladder mode','intervening loss','no backwalk']:
    bad=copy.deepcopy(rows)
    if name=='wrong truefighter':bad['LIVE'][0]['human']='1:1'
    elif name=='wrong moveowner':bad['SPECIAL'][0]['a8']='0'
    elif name=='wrong Main':bad['SPECIAL'][0]['a13']='0'
    elif name=='missing recovery':
        for x in bad['LIVE']:
            if int(x['frame'])>1798:x['actions']='4,771'
    elif name=='wrong ladder mode':bad['COMBINED_CAPTURE'][1]['mode']='4'
    elif name=='intervening loss':bad['LOSS']=[dict(frame='1800')]
    else:
        next(x for x in bad['LIVE']if x['frame']=='1756')['hpos']=next(x for x in bad['LIVE']if x['frame']=='1750')['hpos']
    try:gate(bad)
    except (AssertionError,StopIteration):faults.append(name)
    else:raise AssertionError('Fault admitted:'+name)
pngs=[]
for label in ['selection','ladder','fight','cleanup']:
    p=folder/(label+'.png');raw=p.read_bytes();assert raw[:8]==b'\x89PNG\r\n\x1a\n'and struct.unpack('>II',raw[16:24])==(400,254)
    pngs.append(dict(label=label,path=str(p),bytes=len(raw),SHA256=sync.sha(p)))
assert sum(x['bytes']for x in pngs)<=262144
jumps=[x for x in rows['LIVE']if int(x['hpos'].split(',')[1])<int(x['hfloor'])]
out=root/'audit_current_combined_smoke_checked';assert not out.exists();out.mkdir()
report=dict(passed=True,nativeCombinedChronology=proof,effectiveFaultsRejected=faults,PNG=pngs,totalPNGBytes=sum(x['bytes']for x in pngs),actualAirborneHumanFields=len(jumps),physicalJumpAttemptNotAutomaticallyAccepted=True,CPUVoiceCueRecords=len(rows.get('CPU_BICYCLE_CUE',[])),newAudioLifetimeAccepted=False,nativeChildPoolRetirementAccepted=False,actualLadderRasterReviewPending=True,manualCombinedVisualAcceptancePending=True,heardMixAccepted=False,fullPortAccepted=False,terminal=terminal,logSHA256=sync.sha(folder/'run.log'),scope='One genuine physical UI→native ladder mode7→trueCPU18/human17 fight→ownedKanoKnife→ordinary backwalk/guard control recovery. Actual PNG phases await visual review. No CPU bicycle voice cue occurred; no fresh audio lifetime proof or childpool retirement is claimed.')
(out/'report.json').write_text(json.dumps(report,indent=2));print(out)
