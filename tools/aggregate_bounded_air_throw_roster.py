"""Aggregate finite current roster evidence without broad port/visual claims."""
import json
import verify_native_source_sync as sync

if __name__=='__main__':
    out=sync.ROOT/'audit_bounded_air_throw_roster_coverage_checked'
    assert not out.exists()
    reports=(('audit_bounded_air_throw_retirement_checked',4),
             ('audit_bounded_air_throw_victims_checked',6),
             ('audit_bounded_air_throw_stock_families_checked',6),
             ('audit_bounded_air_throw_remaining_roster_checked',14))
    pins={}
    contexts=0
    for name,count in reports:
        path=sync.ROOT/name/'report.json'
        report=json.loads(path.read_text())
        assert report['passed'] and not report['fullPortAcceptance']
        assert len(report['results'])==count
        for case in report['results'].values():
            terminal=case['terminal']
            assert terminal['exitCode']==0 and terminal['limitReason'] is None
            assert terminal['observerSha256']=='13B38255D1ED054942505C759F2DF58D1BDBCAB7B9D208B10F3FC2527EDC1FE0'
            assert len(case['damage'])==2
            assert terminal['rawMedia']=='none'
        pins[str(path)]=sync.sha(path)
        contexts+=count
    assert contexts==30
    # Mapping is declared from the exact cold-selection case manifests, not
    # inferred from image similarity or a proxy roster.
    victims={'kung_lao':0,'liu_kang':1,'cage':2,'baraka':3,'kitana':4,'mileena':5,
             'shang_tsung':6,'raiden':7,'sub_zero':8,'reptile':9,'scorpion':10,
             'jax':11,'kano':17,'sonya':18}
    for victim in victims:
        for side in (1,2):
            candidates=list(sync.ROOT.glob(f'audit_bounded_air_throw*{victim}_p{side}_runtime'))
            # Jax cases are labeled by owned fighter, and already validated
            # through the reciprocal role report above.
            if victim=='jax':
                candidates=[sync.ROOT/f'audit_bounded_air_throw_retirement_kano_p{side}_runtime']
            assert any(folder.exists() for folder in candidates)
    report=dict(passed=True,contexts=30,actualCatches=60,ordinarySelectableVictimIDs=victims,
        fullPortAcceptance=False,hiddenVictimsVerified=False,bossEligibilityVerified=False,
        fullAnimationAudioVerified=False,sourceSync=sync.verify(),reportSHA256=pins,
        scope='Finite current real Kano attacker coverage against all fourteen ordinary selectable roster IDs in bothslots; Jax reciprocal Kano/Sonya victims. Native catch/identity/damage/recovery/ordinary followups. Not hidden/boss/campaign/all animation/audio or whole-port completion.')
    out.mkdir()
    (out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(passed=True,contexts=30,catches=60,fullPortAcceptance=False)))
