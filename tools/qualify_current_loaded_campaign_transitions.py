"""Seal208actualloadeddependencies, never entire current campaign transfer."""
import json,re,copy
import verify_native_source_sync as sync
sync.verify();root=sync.ROOT
prep=root/'audit_current_loaded_campaign_transitions_preparation';case=root/'audit_current_loaded_campaign_transitions_runtime'
expected=json.loads((prep/'expected.json').read_text());source=json.loads((prep/'source.json').read_text());terminal=json.loads((case/'terminal.json').read_text(encoding='utf-8-sig'))
assert terminal['exitCode']==0 and terminal['limitReason']is None and terminal['elapsedSeconds']<12 and terminal['peakWorkingSetBytes']<=320*1024**2 and terminal['logBytes']<=10*1024**2
assert terminal['observerSha256'].upper()==source['LuaSHA256'].upper()==sync.sha(prep/'tables.lua').upper()
assert expected['stockSHA256']==sync.sha(root/'mk2/mk2-maincpu.bin')and expected['sourceConservationReportSHA256']==sync.sha(root/'audit_current_campaign_transition_dependencies_checked/report.json')
assert not(case/'stderr.log').read_text().strip()and not any(p.suffix.lower()in('.png','.wav','.bin')for p in case.rglob('*'))
lines=(case/'run.log').read_text().splitlines();observed=[dict(re.findall(r'(\w+)=([^\s]+)',s))for s in lines if s.startswith('MK2_CAMPAIGN_DEP ')]
def gate(rows):
    assert len(rows)==len(expected['values'])==208
    for actual,want in zip(rows,expected['values']):
        assert actual['kind']==want['kind']and int(actual['index'])==want['index']and int(actual['at'],16)==want['at']and int(actual['width'])==want['width']and int(actual['value'],16)==want['value']
        assert actual['writes']==actual['inputs']=='0'and actual['assistance']=='none'
gate(observed);faults=[]
for kind in dict.fromkeys(x['kind']for x in observed):
    bad=copy.deepcopy(observed);row=next(x for x in bad if x['kind']==kind);row['value']=f"{int(row['value'],16)^1:08X}"
    try:gate(bad)
    except AssertionError:faults.append(kind)
    else:raise AssertionError('Dependency mutation admitted:'+kind)
assert 'MK2_CAMPAIGN_DEP_DONE fields=3 inputs=0 writes=0 assistance=none'in lines
out=root/'audit_current_loaded_campaign_transitions_checked';assert not out.exists();out.mkdir()
report=dict(passed=True,actualLoadedRecords=len(observed),effectiveFaultsRejected=faults,allSixNativeSchedulesBossTailsMatchStockDerivedConservedConstruction=True,stockBossDamageAndAICallbackRowsConserved=True,endingContextRelocationActualLoaded=True,inputs=0,guestWrites=0,media=0,terminal=terminal,logSHA256=sync.sha(case/'run.log'),expectedSHA256=sync.sha(prep/'expected.json'),sourceConservationReportSHA256=expected['sourceConservationReportSHA256'],historicalEarnedFourCampaignProofRetained=True,currentWholeFourCampaignAcceptance=False,actualCurrentSecretLifecycleAccepted=False,scope='Three input-free actualloaded208scalarreads. Full6schedules+boss-tailrows, damage andstockbossAI/round/specialcallback tables, native lookupoperands and8pairedendingcontinuation operands match independentstock-derived expected. No gameplay/bossvictory/endingforce; doesnot transfer entire changedguest or certify allfourcurrentearnedcampaigns/secretteardown/heardmix/fullport.',fullPortAccepted=False)
(out/'report.json').write_text(json.dumps(report,indent=2));print(out)
