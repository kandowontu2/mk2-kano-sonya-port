"""Qualify only actual cold native progression; no invented campaign clear."""
import copy,json
import verify_native_source_sync as sync
import check_campaign_stage_chronology as chronology

def gate(rows):
    assert all(r['writes']=='0' and r['assistance']=='none' and r['human_slot']=='2' and r['fighter']=='sonya' for records in rows.values() for r in records)
    assert rows['BOOT'][0]['boot']=='600' and rows['BOOT'][0]['strategy']=='leg'
    assert all(r['human']=='18:18' for r in rows['LIVE'])
    return chronology.check(rows,2,18,list(range(13))+[14,15,16])

def main():
    source=sync.verify();folder=sync.ROOT/'audit_current_sonya_p2_native_start_runtime'
    out=sync.ROOT/'audit_current_sonya_p2_native_start_checked';assert not out.exists()
    terminal=json.loads((folder/'terminal.json').read_text());complete=terminal['exitCode']==0 and terminal['limitReason'] is None
    assert complete or (terminal['limitReason']=='wall_limit' and terminal['exitCode']!=0)
    assert terminal['elapsedSeconds']<=(90 if complete else 92) and terminal['peakWorkingSetBytes']<=320*1024*1024 and terminal['logBytes']<=10*1024*1024
    assert terminal['observerSha256']==sync.sha(sync.ROOT/'audit_current_sonya_p2_native_start_preparation/campaign.lua')
    assert not (folder/'stderr.log').read_text().strip()
    assert not any(p.suffix.lower() in ('.png','.bin','.wav') for p in folder.rglob('*'))
    rows=chronology.load(folder/'run.log');stages=gate(rows)
    if complete:assert rows['RESULT'][0]['frame']=='30000' and rows['HOST_BOUND'][0]['maximum_fields']=='30000'
    else:assert not rows.get('RESULT')
    bad=copy.deepcopy(rows);bad['LIVE'][0]['human']='18:1'
    try:gate(bad)
    except AssertionError:pass
    else:raise AssertionError('Proxy accepted')
    wins=[r for r in rows.get('WIN',[]) if r['slot']=='2']
    report=dict(passedObservationChecks=True,completedRunAccepted=complete,sourceSync=source,terminal=terminal,stages=stages,
                earnedOwnRoundWins=len(wins),actualFightContexts=rows.get('FIGHT',[]),logSHA256=sync.sha(folder/'run.log'),
                proxyIdentityRejected=True,fullCampaignAcceptance=False,fullPortAcceptance=False,
                scope='Current genuine cold P2 Sonya18 boot600 native coin/start selection and schedule, existing leg-grab controls, earned native health/wins qualify observed stage advances. No forced schedule/opponent/health/difficulty or assumed full clear/endings/audio/art/release acceptance.')
    out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:report[k] for k in ('passedObservationChecks','completedRunAccepted','stages','earnedOwnRoundWins')}))

if __name__=='__main__':main()
