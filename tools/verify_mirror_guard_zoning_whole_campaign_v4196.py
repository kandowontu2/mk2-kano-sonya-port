"""Retain whole native campaign/ending/boss grammar plus complete new physical-input replay.

Requires the real terminal capture, never treats a prefix or a paid loss as a
tower clear. Whole ending pixels/audio remain separate outstanding acceptance.
"""
import hashlib
import inspect
import json
import subprocess
import traceback
from pathlib import Path
import verify_sonya_zoning700_campaign_v4015 as base
import verify_mirror_guard_zoning_prefix_v4194 as physical
import qualify_mirror_guard_zoning_source_v4192 as boundary
import run_mirror_guard_zoning_campaign_ram_v4187 as capture

ROOT, need, sha, NAME = capture.ROOT, capture.need, capture.sha, capture.NAME
FOLDER = ROOT / 'audit_v4188_sonya_mirror_guard_zoning_p2_campaign'
OUT = ROOT / 'audit_v4197_mirror_guard_zoning_whole_campaign_checked'


def guard_source_boundary():
    # Full original boss source/driver checks are retained. Only declared
    # non-boss controls and RAM sinks differ; physical replay below is separate.
    base.ring.source_boundary()
    return boundary.source_boundary()


def clone(function, substitutions, additions):
    text = inspect.getsource(function)
    for before, after in substitutions:
        need(text.count(before) == 1, 'Unique full original algorithm adaptation: ' + before)
        text = text.replace(before, after)
    scope = dict(vars(base))
    scope.update(__file__=__file__, capture=capture, NAME=NAME, **additions)
    exec(compile(text, __file__ + '::unweakened_' + function.__name__, 'exec'), scope)
    return scope[function.__name__]


ram_guest = clone(base.ram_guest,
                  [('mk2ks_guarded_campaign_guest_ram_v4006.lua', capture.LUA)], {})
matched = clone(base.matched,
                [('transport_boundary()', 'guard_source_boundary()'),
                 ("meta['strategy']=='zoning'and meta['boot_frame']==700",
                  "meta['strategy']=='guard_punish'and meta['boot_frame']==600")],
                dict(guard_source_boundary=guard_source_boundary))


def ram_guest_checked(folder, pins, wanted, text, errors):
    try:
        return ram_guest(folder, pins, wanted, text)
    except ValueError as error:
        errors.append(str(error))
        return wanted


def make_native(expected):
    whole = base.make_native(expected)
    whole.__globals__.update(NAME=NAME, matched=matched, ram_guest_checked=ram_guest_checked)

    def native(folder, text_override=None):
        result = whole(folder, text_override=text_override)
        text = (folder / 'run.log').read_text() if text_override is None else text_override
        try:
            actual = physical.replay(text)
            need(actual['reasons'].get('leg_attempt', 0) > 0 and actual['actualNativeLegActivations'] > 0,
                 'Actual native own Leg Grab tasks required, not just intended commands')
            result['actualWholeGuardInputReplay'] = actual
        except ValueError as error:
            result['passed'] = False
            result['errors'].append(str(error))
        return result
    return native


verify_original = clone(base.verify,
    [("audit_v4009_{fighter}_zoning700_p2_campaign", "audit_v4188_{fighter}_mirror_guard_zoning_p2_campaign")],
    dict(make_native=make_native, matched=matched, ram_guest=ram_guest))


def verify():
    result = verify_original('sonya')
    text = (FOLDER / 'run.log').read_text()
    positive = physical.replay(text)
    rows = physical.parse(text)
    frame = next(r['frame'] for r in rows if r['tag'] == 'GUARD_DECISION' and r['reason'] == 'leg_attempt')
    f = next(r for r in rows if r['tag'] == 'GUARD_FIELD' and r['frame'] == frame)
    faults = [('GUARD_FIELD', 'human_id', 0), ('GUARD_FIELD', 'human_roster', 0),
              ('GUARD_FIELD', 'cpu_id', 0), ('GUARD_FIELD', 'human_owner', '01000000'),
              ('GUARD_FIELD', 'health', '0,161'), ('GUARD_FIELD', 'reset', 1 - int(f['reset'])),
              ('GUARD_FIELD', 'human_action', 0x500), ('GUARD_FIELD', 'cpu_action', 0x507),
              ('GUARD_DECISION', 'reason', 'stance_guard'), ('INPUT', 'button', 'Up')]
    rejected = []
    for tag, key, value in faults:
        try:
            physical.replay(physical.change(text, tag, frame, key, value))
        except ValueError as error:
            rejected.append(dict(tag=tag, key=key, rejectedBy=str(error)))
        else:
            raise ValueError('Actual complete guard replay fault accepted')
        need(physical.replay(text) == positive, 'Whole physical positive restored after each fault')
    prefix_path = ROOT / 'audit_v4195_mirror_guard_zoning_actual_prefix_checked/report.json'
    prefix = json.loads(prefix_path.read_text())
    raw = (FOLDER / 'run.log').read_bytes()[:prefix['nativeLogPrefixBytes']]
    need(prefix['passed'] and prefix['prefixProofOnly'] and hashlib.sha256(raw).hexdigest().upper() == prefix['nativeLogPrefixSHA256'],
         'Original mirror prefix retained byte-for-byte; full original native campaign grammar below remains required')
    for path in (Path(__file__), Path(physical.__file__), Path(boundary.__file__), prefix_path):
        result['inputHashes'][str(path.resolve())] = sha(path)
    result.update(actualWholeCampaignGrammarRetained=True, actualWholeGuardInputReplay=positive,
                  actualAdditionalGuardReplayFaultsRejected=rejected,
                  endingPixelsAccepted=False, completeCampaignAudioAccepted=False, fullPortAcceptance=False)
    return result


if __name__ == '__main__':
    need(not OUT.exists(), 'Fresh immutable whole-campaign qualifier output')
    try:
        result = verify()
        report = dict(passed=True, case=result, actualNaturalSonyaP2TowerClearAccepted=result['unassisted_clear_proven'],
                      endingPixelsAccepted=False, completeCampaignAudioAccepted=False, fullPortAcceptance=False)
    except Exception as error:
        report = dict(passed=False, error=repr(error), traceback=traceback.format_exc(), fullPortAcceptance=False)
    OUT.mkdir()
    need(subprocess.run(['compact.exe', '/C', '/I', '/Q', '/S:' + str(OUT)], capture_output=True).returncode == 0,
         'Compress proof directory before writes')
    (OUT / 'report.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({k: v for k, v in report.items() if k != 'case'}, indent=2), flush=True)
    if report['passed']:
        print(json.dumps(report['case']['actualWholeGuardInputReplay'], indent=2), flush=True)
    raise SystemExit(0 if report['passed'] else 1)
