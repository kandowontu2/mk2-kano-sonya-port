"""Read existing compact traces; do not infer exact hits from sparse samples."""
import collections,json
import verify_native_source_sync as sync
import check_campaign_stage_chronology as chronology

def main():
    source=sync.verify();out=sync.ROOT/'audit_current_reptile_controller_failures';assert not out.exists()
    cases={}
    for name in ('crouch_counter_long','reactive','counter_gap','ring_spacing'):
        folder=sync.ROOT/f'audit_current_sonya_reptile_{name}_runtime'
        terminal=json.loads((folder/'terminal.json').read_text());assert terminal['exitCode']==0 and terminal['limitReason'] is None
        rows=chronology.load(folder/'run.log');stages=chronology.check(rows,2,18,list(range(13))+[14,15,16])
        live=[r for r in rows['LIVE'] if r['stage']=='1'];assert live and all(r['human']=='18:18' and r['cpu']=='9:9' for r in live)
        start=int(rows['STAGE'][1]['frame'])
        health=[r for r in rows.get('HEALTH',[]) if int(r['frame'])>=start and r['pc']=='FF836700' and 0<=int(r['after'])<int(r['before'])<=161]
        damage={str(slot):sum(int(r['before'])-int(r['after']) for r in health if r['slot']==str(slot)) for slot in (1,2)}
        specials=collections.Counter(r['move'] for r in rows.get('SPECIAL',[]) if r['stage']=='1')
        actions=[collections.Counter(r['actions'].split(',')[index] for r in live) for index in (0,1)]
        wins=[r for r in rows['WIN'] if r['stage']=='1']
        cases[name]=dict(logSHA256=sync.sha(folder/'run.log'),terminal=terminal,stages=stages,
            nativeSpecialEntryCounts=dict(specials),nativeDamageByVictimSlot=damage,
            sparseHumanActionCounts=dict(actions[0]),sparseCPUActionCounts=dict(actions[1]),
            earnedOwnRoundWins=sum(r['slot']=='2' for r in wins),earnedCpuRoundWins=sum(r['slot']=='1' for r in wins),
            sparseThrowFields=sum(r['actions'].split(',')[0]=='1287' for r in live),
            actualUppercutActivations=len(rows.get('COUNTER_ACTIVATION',[])))
    report=dict(passedObservationChecks=True,sourceSync=source,cases=cases,noNewGames=True,
        exactHitBlockRecoveryAttributionAccepted=False,fullCampaignAcceptance=False,fullPortAcceptance=False,
        scope='Compare four already executed current Reptile9/Sonya18 traces. Native owned special entries and FF836700 health decreases are exact;30-field action samples cannot establish every collision, throw, block or recovery cause.')
    out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:{f:v[f] for f in ('nativeSpecialEntryCounts','nativeDamageByVictimSlot','earnedOwnRoundWins','earnedCpuRoundWins','sparseThrowFields','actualUppercutActivations')} for k,v in cases.items()}))

if __name__=='__main__':main()
