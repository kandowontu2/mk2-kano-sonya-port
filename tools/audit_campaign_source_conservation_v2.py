"""Correct only the audit's sample lookup; preserve the failed first receipt."""
import inspect
import re
from pathlib import Path
import audit_campaign_source_conservation as original


def main():
    source = inspect.getsource(original.main)
    first = "        for path in sorted((oldbuild / 'samples/mk2ks').glob('*.wav')):"
    last = "        need(len(sample_checks) == 16, 'All sixteen prior samples, not just announcers')"
    start = source.index(first)
    end = source.index(last, start) + len(last)
    replacement = '''        declaration = (oldbuild / 'input_sources/mame-mkp/src/mame/midway/midtunit.cpp').read_text()
        block = declaration.split('static const char *const mk2ks_voice_names[] =', 1)[1].split('};', 1)[0]
        names = re.findall(r'"([^"*][^"]*)"', block)
        need(len(names) == 16 and len(set(names)) == 16, 'All actual old registered samples')
        launcher = (ROOT / 'TEST_KANO_BALL_LAUNCH_V6640.cmd').read_text()
        need('-samplepath "diagnostic_v6640_kano_ball_launch\\\\samples;samples"' in launcher,
             'Actual candidate-first/shared-fallback sample search order')
        for name in names:
            path = ROOT / 'samples/mk2ks' / (name + '.wav')
            override = newbuild / 'samples/mk2ks' / path.name
            target = override if override.is_file() else path
            digest = sha(path)
            need(sha(target) == digest and parent['inputHashes'].get(str(path)) == digest,
                 'Whole actual shared old sample and current resolved sample: ' + path.name)
            pins[str(path)] = pins[str(target)] = digest
            sample_checks.append(path.name)
        need(len(sample_checks) == 16, 'All sixteen prior samples, not just announcers')
        pins[str(ROOT / 'tools/audit_campaign_source_conservation.py')] = sha(ROOT / 'tools/audit_campaign_source_conservation.py')
        pins[str(ROOT / 'audit_campaign_source_conservation/report.json')] = sha(ROOT / 'audit_campaign_source_conservation/report.json')'''
    source = source[:start] + replacement + source[end:]
    scope = dict(vars(original), __file__=__file__, re=re,
                 OUT=original.ROOT / 'audit_campaign_source_conservation_v2')
    exec(compile(source, __file__ + '::whole_audit_shared_sample_path_correction', 'exec'), scope)
    scope['main']()


if __name__ == '__main__':
    main()
