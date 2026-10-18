"""Power-on route fidelity and earned Kintaro match; not final full-port approval."""
import csv
import json
from inspect_normal_runtime import BASE,PORT,sha
from refresh_special_videos import command


def main():
    run=BASE/'stock_wolf_2219_kano_continuous_short_route'
    execution=json.loads((run/'execution.json').read_text())
    assert not execution.get('planningStateLoadUsed',False)
    assert '--campaign-short-route' in execution['testArguments']
    observer=(run/'autoboot.lua').read_text()
    assert ':save(' not in observer and ':load(' not in observer
    command(PORT/'audit_campaign_run.py',run.name)
    source=BASE/'stock_wolf_2219_kano_short_search/chosen.csv'
    with source.open() as stream:expected=list(csv.DictReader(stream))
    with (run/'short_route_replay.csv').open() as stream:actual=list(csv.DictReader(stream))
    assert len(actual)==len(expected)==37
    for index,(old,new) in enumerate(zip(expected,actual),1):
        assert int(new['frame'])==130294+index*120
        assert all(new[k]==old[k] for k in new if k!='frame'),(index,old,new)
    reference=BASE/'stock_wolf_2219_kano_kintaro_varied_finish_uppercut13/campaign.csv'
    count=0
    with reference.open() as old,(run/'campaign.csv').open() as new:
        previous=iter(csv.DictReader(old))
        for row in csv.DictReader(new):
            if int(row['frame'])>=130294:break
            assert row==next(previous),'Changed human-ladder prefix'
            count+=1
    audit=json.loads((run/'CAMPAIGN_AUDIT.json').read_text())
    matches=[r for r in audit['naturallyDefeatedOpponents'] if r['opponent']==12]
    assert len(matches)==1 and matches[0]['naturalWinningRounds']==2
    report=dict(scope='Continuous startup replay, earned Kintaro match and37 exact input-route boundary states',
        stateLoadUsed=False,humanPrefixRowsMatched=count,routeBoundariesMatched=37,
        nativeKintaroMatch=matches[0],fullCampaignVerified=False,fullPortVerified=False,
        pins={str(p):sha(p) for p in (run/'autoboot.lua',run/'execution.json',run/'campaign.csv',
            run/'short_route_replay.csv',run/'CAMPAIGN_AUDIT.json',source,reference)})
    (run/'CONTINUOUS_ROUTE_QUALIFICATION.json').write_text(json.dumps(report,indent=2)+'\n')
    print('Verified continuous no-load Kintaro match and37 identical boundary states; full campaign still separate')


if __name__=='__main__':main()
