"""Keep an actual terminal muted-roll route without claiming audible coverage.

Raw RAM can be released after this finite source-state proof. Mixed speaker
audio is explicitly unqualified: no redundant carrier is archived for a miss.
"""
import gzip
import json
import subprocess
from pathlib import Path
import native_ai_response_context as current
import native_process_census_v6647 as native
import qualify_native_ai_response_attract as runtime
import current_tomb_winner_mix_fault_model_v5789 as audio
from inventory_current_port_storage_v4200 import allocated

ROOT, need, sha = current.ROOT, current.need, current.sha


def finish(c, boot):
    out = c['folder'] / 'finite_muted_roll_route.json'
    need(not out.exists() and c['terminal']['nativeExit'] == 0 and not native.census() and
         c['guest'] == current.expected(), 'Same terminal native job and whole independently reconstructed current guest')
    report = json.loads((c['folder']/'report.json').read_text())
    need(report['passed'] and report['requestedConfigurationAccepted'] and
         all(sha(path) == digest for path, digest in report['inputHashes'].items()), 'Every actual frozen input and transport')
    rows = lambda tag: runtime.rows(c['text'], tag)
    need([(int(r['frame']), r['value']) for r in rows('INPUT')] ==
         [(f, '1') for f in range(boot, boot+4)] + [(boot+4, '0')], 'Only ordinary four-field acknowledgement')
    need(not rows('ERROR_ENTRY') and not rows('RESET'), 'No checked native error or reset')
    rolls = [r for r in rows('SOUND') if r['word'] == '6B03']
    need(len(rolls) == 1 and rolls[0]['mode'] == rolls[0]['mute'] == '1' and rolls[0]['pc'] == 'FFFFDEC0',
         'One naturally selected Kano roll, only after original native mute')
    roll = rolls[0]
    slots = [s for s in (1, 2) if roll[f'p{s}_id'] == roll[f'p{s}_roster'] == '17' and
             roll[f'p{s}_action'] == '523' and roll[f'p{s}_actor'] == roll[f'p{s}_owner'] == roll['a8'] and
             roll[f'p{s}_main'] == roll['a13'] and int(roll[f'p{s}_hp']) > 0]
    need(len(slots) == 1, 'Actual live true-ID actor/Main ownership, not a stale roster or Liu proxy')
    sources = [r for r in audio.rows(c['text'], 'MK2_TOMB_MIX_CHANNEL')
               if int(r['frame']) >= int(roll['frame']) and int(r['channel']) >= 10]
    need(sources and all(r['sample'] == '4294967295' and r['length'] == '0' and
         r['position'] == '0' and r['bits'] == '0000000000000000' and
         r['loop'] == r['paused'] == r['writes'] == '0' and r['assistance'] == 'none' for r in sources),
         'All four startup channels remain inactive throughout actual muted roll capture')
    late = [r for r in rows('MUTE_POLICY') if r['pc'] == 'FF843960' and r['value'] == '1' and
            float(r['seconds']) < float(roll['seconds'])]
    need(late, 'Original native late mute actually precedes roll')
    source = Path(__file__).resolve()
    with gzip.open(c['folder']/'executed_muted_roll_sealer.py.gz', 'wt', encoding='utf-8') as stream:
        stream.write(source.read_text())
    result = dict(passed=True, finiteMutedRollSuppressionAccepted=True, audibleKanoAccepted=False,
                  fullAttractAudioAccepted=False, fullPortAcceptance=False, goalStatus='active',
                  nativeTerminal=c['terminal'], actualRoll=roll, physicalSlot=slots[0],
                  mutedStartupSourceStates=len(sources), actualNativeLateMute=late[-1],
                  mixedSpeakerAudioQualified=False, rawCarriersIntentionallyNotArchived=True,
                  actualNativeInputs=rows('INPUT'), actualDemoAdmissions=rows('DEMO_OWNER'),
                  remaining='Audible native Kano attract roll remains unobserved. Post-ending joins and remaining integration/combined release checks remain open.',
                  nextAction='Do not repeat this completed phase. Use the current native campaign controller for post-ending fresh-join coverage; investigate a distinct native unmuted Kano route separately.',
                  inputHashes={**report['inputHashes'], str(source):sha(source),
                               str(c['folder']/'report.json'):sha(c['folder']/'report.json'),
                               str(c['folder']/'run.log.gz'):sha(c['folder']/'run.log.gz')},
                  newBuilds=0, newROMCopies=0, newZIPs=0, publicBuildPromoted=False)
    out.write_text(json.dumps(result, indent=2)+'\n')
    storage = []
    for path in [p for p in c['folder'].rglob('*') if p.is_file()] + [source]:
        need(path.resolve().is_relative_to(ROOT) and not path.is_symlink(), 'Exact bounded evidence leaf')
        digest = sha(path)
        subprocess.run(['compact.exe', '/C', '/EXE:LZX', '/F', '/I', '/Q', str(path)], check=True, capture_output=True)
        need(sha(path) == digest, 'Evidence bytes preserved by compression')
        storage.append(dict(path=str(path), sha256=digest, allocatedBytes=allocated(path)))
    (c['folder']/'muted_roll_storage_receipt.json').write_text(json.dumps(dict(passed=True, files=storage), indent=2)+'\n')
    print(json.dumps(dict(passed=True, audibleKanoAccepted=False, mutedStartupStates=len(sources),
                         allocatedEvidenceBytes=sum(r['allocatedBytes'] for r in storage))), flush=True)
    return result
