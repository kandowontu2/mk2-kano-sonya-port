"""Full original scalar chronology gates for the current twenty morph cases."""
import json
import verify_native_source_sync as sync
import verify_morph_adversity_v3233 as original

if __name__ == '__main__':
    source_sync = sync.verify()
    out = sync.ROOT/'audit_current_morph_complete_ledgers_checked'
    assert not out.exists()
    patterns = dict(forward='morph_forward_attack', formed='morph_hit',
        reverse='morph_reverse_attack', repeat_morph='repeat_morph', ko='morph_ko')
    results = {}
    for phase, stem in patterns.items():
        for target in ('kano', 'sonya'):
            for side in (1, 2):
                folder = sync.ROOT/f'audit_bounded_current_{stem}_{target}_p{side}_runtime'
                terminal = json.loads((folder/'terminal.json').read_text())
                assert terminal['exitCode'] == 0 and terminal['limitReason'] is None
                assert terminal['peakWorkingSetBytes'] <= 320*1024**2
                assert terminal['logBytes'] <= 10*1024**2
                assert not (folder/'stderr.log').read_text().strip()
                assert not any(p.suffix.lower() in ('.png', '.bin', '.wav') for p in folder.rglob('*'))
                log = (folder/'run.log').read_text()
                proof = original.verify_log(log, target, side, phase, 'added')
                # The exact original physical command chronology must matter.
                line = next(line for line in log.splitlines()
                    if line.startswith('MK2_HUMAN_SHANG_INPUT '))
                broken = log.replace(line+'\n', '', 1)
                assert broken != log
                try:
                    original.verify_log(broken, target, side, phase, 'added')
                except ValueError as error:
                    assert str(error) == 'Every exact real own morph and postrecovery walk/jump/punch physical input, no missing or duplicate commands'
                else:
                    raise AssertionError('Missing genuine physical input accepted')
                key = f'{phase}_{target}_p{side}'
                results[key] = dict(proof=proof, terminal=terminal,
                    logSHA256=sync.sha(folder/'run.log'), missingPhysicalInputRejected=True)
                print('Qualified '+key, flush=True)
    report = dict(passed=True, contexts=20, cases=results, sourceSync=source_sync,
        gateSHA256=sync.sha(original.__file__), fullPortAcceptance=False,
        scope='Current both-form/both-slot forward cancellation, formed hit, interrupted reverse retry, three repeated native cycles and morphed KO/next-round reset. Complete physical inputs, paired actor publications, native health writers and ID/floor chronology. Not transformed finishers, CPU morphs, full art/audio or campaign acceptance.')
    out.mkdir()
    (out/'report.json').write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps(dict(passed=True, contexts=20, fullPortAcceptance=False)), flush=True)
