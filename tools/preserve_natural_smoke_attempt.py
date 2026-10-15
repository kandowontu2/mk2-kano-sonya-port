"""Preserve an unsuccessful controller attempt and its executed text sources."""
import gzip
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def preserve(capture, reason='Raw arena7 rematch suppression prevented paid challenger before match8; later CSS assertion'):
    out = capture['folder']
    assert capture['terminal']['nativeExit'] == 0
    assert not capture['report']['actualSecretRouteAccepted']
    assert not (out/'executed_sources.json.gz').exists()
    sources = {}
    for name, digest in capture['pins'].items():
        path = Path(name)
        if path.suffix in ('.lua', '.py'):
            raw = path.read_bytes()
            assert hashlib.sha256(raw).hexdigest().upper() == digest
            sources[name] = dict(sha256=digest, text=raw.decode('utf-8'))
    with gzip.open(out/'executed_sources.json.gz', 'wt', encoding='utf-8') as f:
        json.dump(sources, f)
    with gzip.open(out/'executed_sources.json.gz', 'rt', encoding='utf-8') as f:
        saved = json.load(f)
    assert all(hashlib.sha256(v['text'].encode()).hexdigest().upper() == v['sha256'] for v in saved.values())
    text = capture['text']
    matches = [line for line in text.splitlines() if line.startswith('MK2_STAGE_MATCH ')]
    windows = [line for line in text.splitlines() if line.startswith('MK2_STAGE_WINDOW ')]
    assert len(matches)-1 <= len(windows) <= len(matches) and len(matches) >= 7
    assert all('kos=2 damage=322' in line for line in windows)
    assert not any(line.startswith('MK2_STAGE_SECRET_ACCEPT ') for line in text.splitlines())
    result = dict(preservedFailedAttempt=True, secretRouteAccepted=False,
                  nativeTerminal=capture['terminal'], executedSources=len(sources),
                  earnedTwoPlayerMatches=matches, nativeTwoWinWindows=windows,
                  controllerFailure=reason,
                  gameSideSecretFailureEstablished=False, newBuilds=0, newROMCopies=0,
                  originalReportSHA256=hashlib.sha256((out/'report.json').read_bytes()).hexdigest().upper())
    (out/'preserved_failure.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(dict(preservedFailedAttempt=True, nativeExit=0, earnedMatches=len(matches),
                         wholeExecutedSources=len(sources), secretRouteAccepted=False)))
    return result
