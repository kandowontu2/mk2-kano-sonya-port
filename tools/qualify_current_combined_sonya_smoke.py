"""Honest partial: Sonya combined UI/contact, no observed Ring or Ball voice."""
import copy,json,struct
import check_campaign_stage_chronology as chronology
import verify_native_source_sync as sync
sync.verify();root=sync.ROOT;folder=root/'audit_current_combined_sonya_smoke_runtime'
rows=chronology.load(folder/'run.log');terminal=json.loads((folder/'terminal.json').read_text(encoding='utf-8-sig'))
assert terminal['exitCode']==0 and terminal['limitReason']is None and terminal['elapsedSeconds']<90 and terminal['peakWorkingSetBytes']<320*1024**2 and terminal['logBytes']<10*1024**2
assert not(folder/'stderr.log').read_text().strip()
def gate(r):
    captures=r['COMBINED_CAPTURE'];assert [x['label']for x in captures]==['selection','ladder','fight','cleanup']and [x['mode']for x in captures]==['4','7','2','2']
    assert r['SELECT_ID'][-1]['roster']=='18'and r['SELECT_ID'][-1]['state']=='3'
    assert len(r['FIGHT'])==1 and r['FIGHT'][0]['human']=='18:18'and r['FIGHT'][0]['cpu']=='17:17'
    first=r['LIVE'][0]
    assert all(x['human']=='18:18'and x['cpu']=='17:17'and x['human_actor']==first['human_actor']and x['human_main']==first['human_main']and x['cpu_actor']==first['cpu_actor']and x['cpu_main']==first['cpu_main']and all(int(v)>0 for v in x['health'].split(','))for x in r['LIVE'])
    assert all(x['mode']=='2'and x['states']=='1,0'and x['roster']=='18,17'for x in r['STATE']if int(x['frame'])>=1690)
    assert not r.get('LOSS')and not r.get('WIN')and r['COMBINED_COMPLETE'][0]['captures']=='4'
    assert all(x['writes']=='0'and x['assistance']=='none'for x in r['COMBINED_SOUND_WORD'])
    assert not r.get('SPECIAL')and not r.get('COMBINED_AUDIO_CUE')and not r.get('COMBINED_AUDIO_OWNER')
    return first
first=gate(rows);faults=[]
for label in ['wrong identity','wrong Main','wrong ladder mode','intervening loss','fabricated special','changed sound assistance']:
    bad=copy.deepcopy(rows)
    if label=='wrong identity':bad['LIVE'][0]['human']='1:1'
    elif label=='wrong Main':bad['LIVE'][-1]['human_main']='0'
    elif label=='wrong ladder mode':bad['COMBINED_CAPTURE'][1]['mode']='4'
    elif label=='intervening loss':bad['LOSS']=[dict(frame='1800')]
    elif label=='fabricated special':bad['SPECIAL']=[dict(move='ring')]
    else:bad['COMBINED_SOUND_WORD'][0]['writes']='1'
    try:gate(bad)
    except AssertionError:faults.append(label)
    else:raise AssertionError('Fault admitted:'+label)
pngs=[]
for label in ['selection','ladder','fight','cleanup']:
    p=folder/(label+'.png');raw=p.read_bytes();assert raw[:8]==b'\x89PNG\r\n\x1a\n'and struct.unpack('>II',raw[16:24])==(400,254)
    pngs.append(dict(label=label,path=str(p),bytes=len(raw),SHA256=sync.sha(p)))
assert sum(x['bytes']for x in pngs)<=262144
contact=[x for x in rows['HEALTH']if x['slot']=='1'and x['pc']=='FF836700'and x['a8']==first['cpu_actor']and x['a13']==first['cpu_main']and int(x['after'])<int(x['before'])]
assert contact
out=root/'audit_current_combined_sonya_smoke_checked';assert not out.exists();out.mkdir()
report=dict(finiteCombinedUIIdentityContactObservationPassed=True,completeCombinedSpecialAudioSmokeAccepted=False,actualRingEntries=0,actualKanoBallAudioCues=0,newVoiceLifetimeAccepted=False,nativePortWordCount=len(rows['COMBINED_SOUND_WORD']),ADSPByteConsumptionProven=False,actualOwnedCPUContactStores=contact,effectiveFaultsRejected=faults,PNG=pngs,totalPNGBytes=sum(x['bytes']for x in pngs),manualVisualPhaseReviewPending=True,heardMixAccepted=False,fullPortAccepted=False,terminal=terminal,logSHA256=sync.sha(folder/'run.log'),scope='Genuine physical Sonya18selection/native laddermode7/trueSonya18human-Kano17CPU combat and contact. Ringinputattempt during CPUcontact did not produce an actual SPECIAL entry; CPU Ballmarker was notobserved. No activation defect/full Ringrecovery/audioEOF/jump asserted; existing qualified allhumanmoves remain retained. Portwords are actual host mappedwrites only, not ADSP consumption.')
(out/'report.json').write_text(json.dumps(report,indent=2));print(out)
