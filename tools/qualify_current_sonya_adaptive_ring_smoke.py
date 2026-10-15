"""One physical ready-plan, owned native Ring and actual ready follow-up."""
import copy,json
import check_campaign_stage_chronology as chronology
import verify_native_source_sync as sync
sync.verify();root=sync.ROOT;folder=root/'audit_current_sonya_adaptive_ring_smoke_runtime'
rows=chronology.load(folder/'run.log');terminal=json.loads((folder/'terminal.json').read_text(encoding='utf-8-sig'))
assert terminal['exitCode']==0 and terminal['limitReason']is None and terminal['elapsedSeconds']<90 and terminal['peakWorkingSetBytes']<320*1024**2 and terminal['logBytes']<10*1024**2
assert not(folder/'stderr.log').read_text().strip()and not any(p.suffix.lower()in('.png','.bin','.wav')for p in folder.rglob('*'))
def gate(r):
    assert len(r['RING_READY_PLAN'])==len(r['SPECIAL'])==len(r['RING_RECOVERED'])==len(r['RING_FOLLOWUP_COMPLETE'])==1
    plan,entry,recovery,complete=(r[t][0]for t in['RING_READY_PLAN','SPECIAL','RING_RECOVERED','RING_FOLLOWUP_COMPLETE'])
    assert plan['id']==plan['roster']=='18'and plan['owner']==plan['actor']and plan['action']in('0','771')
    assert plan['y']==plan['floor']and all(int(plan[k],16)==0 for k in ['vy','vx','gravity','trail'])and int(plan['flags'],16)&0x1c==0 and int(plan['body'],16)&0x0c==0
    assert int(plan['gap'])>=150 and plan['cpu_action']in('0','771')and int(plan['cpu_flags'],16)&0x18==0
    assert int(plan['frame'])<int(entry['frame'])<int(recovery['frame'])and int(complete['frame'])==int(recovery['frame'])+120
    assert entry['move']=='ring'and entry['pc']=='FFFFB420'and entry['id']==entry['roster']=='18'
    assert entry['actor']==entry['a8']==recovery['actor']==recovery['owner']==plan['actor']and entry['main']==entry['a13']==recovery['main']==plan['main']
    assert recovery['id']=='18'and recovery['action']in('0','771')and recovery['y']==recovery['floor']and int(recovery['flags'],16)&0x1c==0 and int(recovery['body'],16)&0x0c==0
    live=r['LIVE'];first=live[0]
    assert all(x['selection']=='1'and x['human']=='18:18'and x['cpu']=='17:17'and x['human_actor']==plan['actor']and x['human_main']==plan['main']and x['cpu_actor']==first['cpu_actor']and x['cpu_main']==first['cpu_main']and all(int(y)>0 for y in x['health'].split(','))for x in live)
    assert all(x['mode']=='2'and x['states']=='1,0'and x['roster']=='18,17'for x in r['STATE']if int(x['frame'])>=1690)
    assert not r.get('LOSS')and not r.get('WIN')and len(r['SELECT'])==1
    result=r['RESULT'][0];assert result['selections']=='1'and result['losses']==result['native_win_reads']=='0'
    assert int(result['live_fields'])==int(result['frame'])-int(result['first_live'])+1
    assert all(int(x['after'])>0 for x in r['HEALTH'])
    return dict(plan=plan,entry=entry,recovery=recovery,followup=complete,allNativeLiveBranchCallbacks=int(result['live_fields']))
proof=gate(rows);faults=[]
for label in ['unready plan','wrong actor','wrong Main','wrong identity','no recovery','short followup','intervening loss','missing live admission']:
    bad=copy.deepcopy(rows)
    if label=='unready plan':bad['RING_READY_PLAN'][0]['vy']='1'
    elif label=='wrong actor':bad['SPECIAL'][0]['a8']='0'
    elif label=='wrong Main':bad['SPECIAL'][0]['a13']='0'
    elif label=='wrong identity':bad['SPECIAL'][0]['id']='1'
    elif label=='no recovery':bad['RING_RECOVERED']=[]
    elif label=='short followup':bad['RING_FOLLOWUP_COMPLETE'][0]['frame']='1907'
    elif label=='intervening loss':bad['LOSS']=[dict(frame='1900')]
    else:bad['RESULT'][0]['live_fields']='337'
    try:gate(bad)
    except (AssertionError,ValueError):faults.append(label)
    else:raise AssertionError('Fault admitted:'+label)
out=root/'audit_current_sonya_adaptive_ring_smoke_checked';assert not out.exists();out.mkdir()
report=dict(passed=True,actualOwnedRingEntryReadyRecoveryAnd120FollowupAccepted=True,proof=proof,effectiveFaultsRejected=faults,nativePortWordCount=len(rows['COMBINED_SOUND_WORD']),actualBallAudioCueCount=len(rows.get('COMBINED_AUDIO_CUE',[])),newAudioLifetimeAccepted=False,ADSPByteConsumptionProven=False,heardMixAccepted=False,allFieldExactMainPublicationLogged=False,scope='One physical clean-ready locked-direction Ring, actual true18owned native entry and clean-ready recovery,120fields followup. Native live branch count proves everycallback admitted mode2/states1,0/bothMainowners; exactMain/IDs checked on loggedLIVE samples and STATEpublication changes, not everyfield nativeIDstore coverage. NoCPUball/privatevoicecue observed; portwords notADSPreceipt/heardmix. Priorcurrent4PNGselection/ladder/UImanualacceptance retained separately; no new images/allmoves/allarenas/fullport.',fullPortAccepted=False,terminal=terminal,logSHA256=sync.sha(folder/'run.log'))
(out/'report.json').write_text(json.dumps(report,indent=2));print(out)
