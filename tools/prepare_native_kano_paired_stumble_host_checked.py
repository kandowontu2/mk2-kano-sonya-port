"""Preserve original host-boundary failure; compile exact inline successor.

One whitespace-sensitive host matcher is corrected. Lua/physical controls,
full source initializer, finite deadline and full remaining goal unchanged.
Source-only preflight starts no native game and compiles no emulator/probe.
"""
import argparse
import code
import hashlib
import inspect
import json
import traceback
from pathlib import Path
from types import SimpleNamespace
import prepare_native_kano_paired_stumble_campaign as previous

ROOT, need, sha = previous.ROOT, previous.need, previous.sha
OUT = ROOT / 'audit_native_kano_paired_stumble_host_checked'
SOURCE = ROOT / 'audit_native_kano_paired_stumble_host_checked_source'
INIT = ROOT / 'audit_native_kano_paired_stumble_host_checked_initializer'
OLD_INIT = ROOT / 'audit_native_kano_paired_stumble_host_checked_previous_initializer'
RAM = {}


def functions(provider):
    source = inspect.getsource(previous.functions)
    before = "('  actualNaturalTowerClearAccepted=False,',"
    after = "('actualNaturalTowerClearAccepted=False,',"
    source = previous.once(source,before,after)
    scope = dict(vars(previous),__file__=__file__,OUT=OUT,RAM=RAM)
    exec(compile(source,__file__+'::entire_original_host_adapter_with_exact_inline_keyword_boundary','exec'),scope)
    return scope['functions'](provider)


def source_guard():
    original = previous.source_guard()
    failure_path = previous.SOURCE / 'host_preflight_failure.json'
    failure = json.loads(failure_path.read_text())
    need(not failure['passed'] and not failure['hostCompiled'] and failure['nativeBoots']==failure['emulatorBuilds']==0,
         'Entire original actual host-matching failure preserved, never relabelled as gameplay')
    metadata_path = ROOT / previous.repaired.NAME / 'build-info.json'
    metadata = json.loads(metadata_path.read_text(encoding='utf-8-sig'))
    provider = SimpleNamespace(GUEST_SHA=metadata['expected_guest_sha256'],EXE_SHA=metadata['executable_sha256'],
                              PAYLOAD_SHA=metadata['payload_sha256'])
    scope,host = functions(provider)
    need(scope['OUT']==OUT and scope['CONTROLLERS']==previous.CONTROLLERS and
         "MK2KS_TEST_FIGHTER='kano',MK2KS_CAMPAIGN_SIDE='1'" in host and
         "MK2KS_CAMPAIGN_STRATEGY='zoning',MK2KS_BOSS_PHYSICAL_POLICY='shao_knife_retreat'" in host and
         "MK2KS_CAMPAIGN_OBSERVER_LIMIT='5900'" in host and "'-str','6000'" in host and
         "'-nocheat'" in host and "'-noautoframeskip','-frameskip','0'" in host,
         'Entire actual host compiles with all original physical policies, finite deadline and native flags')
    report = dict(original)
    report.update(wholePythonHostCompiled=True,hostSourceSHA256=hashlib.sha256(host.encode()).hexdigest().upper(),
        exactOriginalInlineKeywordBoundaryCorrected=True,originalHostPreflightFailurePreserved=True)
    report['inputHashes'] = dict(original['inputHashes'])
    for p in (failure_path,previous.SOURCE/'report.json',metadata_path,Path(__file__).resolve()):
        report['inputHashes'][str(p)] = sha(p)
    if SOURCE.exists():
        need(json.loads((SOURCE/'report.json').read_text())==report,'Existing complete compiled-host preflight stays unchanged')
    else:
        SOURCE.mkdir(); (SOURCE/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    return report


def run():
    scope = dict(vars(previous),__file__=__file__,OUT=OUT,SOURCE=SOURCE,INIT=INIT,OLD_INIT=OLD_INIT,
                 RAM=RAM,source_guard=source_guard,functions=functions)
    exec(compile(inspect.getsource(previous.run),__file__+'::whole_original_current_Kano_campaign_capture','exec'),scope)
    return scope['run']()


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--source-only',action='store_true');args=parser.parse_args()
    if args.source_only:
        proof=source_guard()
        print(json.dumps(dict(passed=True,sourceOnlyAccepted=True,wholePythonHostCompiled=True,
            hostSourceSHA256=proof['hostSourceSHA256'],nativeBoots=0,emulatorBuilds=0,
            nativeGameplayAccepted=False,fullPortAcceptance=False)),flush=True)
    else:
        try: captured=run()
        except Exception as error:
            folder=OUT if OUT.exists() else (INIT if INIT.exists() else SOURCE)
            if folder.exists():
                path=folder/'current_capture_failure.json';need(not path.exists(),'Preserve actual successor capture failure')
                path.write_text(json.dumps(dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False),indent=2)+'\n')
            print(json.dumps(dict(passed=False,error=repr(error),traceback=traceback.format_exc())),flush=True)
        code.interact(banner='Same actual compiled-host Kano trial; whole goal remains open.',local=dict(RAM=RAM))
