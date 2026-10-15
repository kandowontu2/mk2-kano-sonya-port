"""Seal finite actual rematch evidence, keeping unsuccessful secrets explicit."""
import gzip
import hashlib
import json
from pathlib import Path
import check_natural_smoke_route as proof
import preserve_natural_smoke_attempt as archive

ROOT, need = proof.ROOT, proof.need


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest().upper()


def restored_capture(template, folder):
    folder = ROOT/folder
    report = json.loads((folder/'report.json').read_text())
    need(report['passed'] and report['nativeTerminal']['nativeExit'] == 0, 'Original actual transport passed; secret remains unaccepted')
    with gzip.open(folder/'run.log.gz', 'rt', encoding='utf-8') as f:
        text = f.read()
    records = proof.inventory(text)
    need(len(records['MK2_HPHASE_GUEST_DIGEST']) == len(records['MK2_HPHASE_GFX_DIGEST']) == 1 and
         records['MK2_HPHASE_GUEST_DIGEST'][0]['sha256'] == hashlib.sha256(template['guest']).hexdigest().upper() and
         records['MK2_HPHASE_GFX_DIGEST'][0]['sha256'] == hashlib.sha256(template['gfx']).hexdigest().upper(),
         'Entire original actual transported guest/GFX match retained current RAM sources, never replayed')
    with gzip.open(folder/'executed_sources.json.gz', 'rt', encoding='utf-8') as f:
        executed = json.load(f)
    for path, wanted in report['inputHashes'].items():
        if path in executed:
            raw = executed[path]['text'].encode()
            need(hashlib.sha256(raw).hexdigest().upper() == executed[path]['sha256'] == wanted,
                 'Whole originally executed source restored from immutable source archive')
        else:
            need(digest(path) == wanted, 'Unchanged original executable/ROM/reference input')
    return dict(template, folder=folder, fighter='kano', side=2, text=text,
                report=report, pins=report['inputHashes'], terminal=report['nativeTerminal'])


def seal(c, result, faults, failed_sources=()):
    need(c['terminal']['nativeExit'] == 0 and proof.rotation_gate(c) == result and len(faults) == 7,
         'Same terminal and whole earned rotation ledger rerun; actual fault set executed')
    need(not proof.capture_host.native.census(), 'Native games are terminal')
    path = c['folder']/'arena_rotation_contract.json'
    need(not path.exists(), 'Fresh narrow receipt, not a relabelled secret pass')
    result = dict(result, actualFaultsRejected=faults, gameBytesChanged=False, newBuilds=0, newROMCopies=0,
                  newRawMedia=0, newZIPs=0, wholeSecretAudioAccepted=False,
                  sourceHashes={str(Path(p).resolve()): digest(p) for p in (proof.__file__, __file__, archive.__file__)},
                  captureLogSHA256=digest(c['folder']/'run.log.gz'), originalTransportReportSHA256=digest(c['folder']/'report.json'))
    if failed_sources:
        messages = ['UnboundLocalError: first', 'UnboundLocalError: health',
                    'Unqualified native health writer FF814E90', 'Whole normal paid challenger input Start']
        need(len(failed_sources) == len(messages), 'Each original checker rejection retained separately')
        rejected = [dict(passed=False, sourceSHA256=hashlib.sha256(s.encode()).hexdigest().upper(),
                         source=s, error=e, nativeGameFailure=False) for s, e in zip(failed_sources, messages)]
        with gzip.open(c['folder']/'original_checker_rejections.json.gz', 'wt', encoding='utf-8') as f:
            json.dump(rejected, f)
        result['originalCheckerRejectionsPreserved'] = len(rejected)
    path.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({k: result[k] for k in ('passed', 'fighter', 'physicalSlot', 'nativeMatches', 'earnedTwoWinWindows', 'actualSecretFightAccepted')}), flush=True)
    return result
