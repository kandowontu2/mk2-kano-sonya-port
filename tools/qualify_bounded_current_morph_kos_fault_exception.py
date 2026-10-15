"""Reuse complete original scalar health/input/round ledger, current binary."""
import json
import verify_native_source_sync as sync
import verify_morph_adversity_v3233 as original

if __name__ == '__main__':
    source_sync = sync.verify()
    out = sync.ROOT/'audit_bounded_current_morph_kos_checked'
    assert not out.exists()
    lua = sync.ROOT/'audit_bounded_current_morph_kos_preparation/morph_ko.lua'
    cases = {}
    for target in ('kano', 'sonya'):
        for side in (1, 2):
            folder = sync.ROOT/f'audit_bounded_current_morph_ko_{target}_p{side}_runtime'
            terminal = json.loads((folder/'terminal.json').read_text())
            assert terminal['exitCode'] == 0 and terminal['limitReason'] is None
            assert terminal['peakWorkingSetBytes'] <= 320*1024**2
            assert terminal['logBytes'] <= 10*1024**2
            assert terminal['observerSha256'] == sync.sha(lua)
            assert not (folder/'stderr.log').read_text().strip()
            assert not any(p.suffix.lower() in ('.png', '.bin', '.wav') for p in folder.rglob('*'))
            log = (folder/'run.log').read_text()
            proof = original.verify_log(log, target, side, 'ko', 'added')
            broken = log.replace('pc=FF836700', 'pc=DEADBEEF', 1)
            assert broken != log
            try:
                original.verify_log(broken, target, side, 'ko', 'added')
            except ValueError as error:
                assert str(error) == 'Every health change uses original collision/round initialization writer, no assistance'
            else:
                raise AssertionError('Foreign health writer accepted')
            cases[f'{target}{side}'] = dict(proof=proof, terminal=terminal,
                logSHA256=sync.sha(folder/'run.log'), foreignHealthWriterRejected=True)
    report = dict(passed=True, cases=cases, sourceSync=source_sync,
        observerSHA256=sync.sha(lua), gateSHA256=sync.sha(original.__file__),
        fullPortAcceptance=False,
        scope='Four current genuine-input morphed KOs and native next-round Shang resets, complete paired identity/health/input chronology. Not full CPU, campaign, art, audio or finisher acceptance.')
    out.mkdir()
    (out/'report.json').write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps(dict(passed=True, contexts=4, fullPortAcceptance=False)))
