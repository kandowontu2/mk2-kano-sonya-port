"""Preserve an observed native secret entry without inventing a full pass."""
import gzip
import hashlib
import json
from pathlib import Path


def preserve(c):
    folder = c['folder']
    assert c['terminal']['nativeExit'] == 0
    assert not (folder/'executed_sources.json.gz').exists()
    sources = {}
    for name,digest in c['pins'].items():
        raw = Path(name).read_bytes()
        assert hashlib.sha256(raw).hexdigest().upper() == digest
        if Path(name).suffix in ('.py','.lua'):
            sources[name] = dict(sha256=digest,text=raw.decode('utf-8'))
    with gzip.open(folder/'executed_sources.json.gz','wt',encoding='utf-8') as f:
        json.dump(sources,f)
    records = {tag:[l for l in c['text'].splitlines() if l.startswith(tag+' ')]
               for tag in ('MK2_STAGE_BOOT','MK2_STAGE_SECRET_ACCEPT','MK2_STAGE_SECRET_FIGHT',
                           'MK2_STAGE_SECRET_WALK','MK2_STAGE_SECRET_JUMP','MK2_STAGE_SECRET_PUNCH',
                           'MK2_STAGE_SECRET_RESULT','MK2_SECRET_DEADLINE')}
    assert records['MK2_STAGE_SECRET_ACCEPT'] and records['MK2_STAGE_SECRET_FIGHT']
    assert not records['MK2_STAGE_SECRET_RESULT']
    result = dict(preservedActualRun=True, originalTransportReportPassed=c['report']['passed'],
                  actualNativeTerminal=c['terminal'], entireExecutedTextSources=len(sources),
                  completeSecretControlSequenceAccepted=False, fullPortAcceptance=False,
                  nativeBootRecords=len(records['MK2_STAGE_BOOT']),
                  wholeGuestTransports=c['guestCount'],wholeGFXTransports=c['gfxCount'],
                  actualRecords=records,
                  resetCause='unresolved; original native job reset later in attract, not during secret admission',
                  newBuilds=0,newROMCopies=0,newRawMedia=0,
                  originalTransportReportSHA256=hashlib.sha256((folder/'report.json').read_bytes()).hexdigest().upper())
    (folder/'incomplete_native_secret_run.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(dict(preservedActualRun=True, nativeExit=0, nativeBootRecords=result['nativeBootRecords'],
                         actualSecretFightObserved=True, completeSecretControlsAccepted=False)))
    return result
