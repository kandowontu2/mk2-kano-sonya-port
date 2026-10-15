"""Check exact declared physical-controller edits before running fresh native capture."""
import hashlib
import json
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'audit_v4117_guard_punish_source_preflight'


def need(condition, message):
    if not condition:
        raise ValueError(message)


def sha(path):
    with Path(path).open('rb') as file:
        return hashlib.file_digest(file, 'sha256').hexdigest().upper()


def source_boundary():
    original = ROOT / 'mk2ks_natural_campaign_shao_ring_retreat_v3485.lua'
    wrapper = ROOT / 'mk2ks_guard_punish_campaign_ram_v4112.lua'
    source, text = original.read_text(), wrapper.read_text()
    need(not re.search(r'write_u\d+|:write_|load_?state|\.value\s*=(?!=)', text),
         'No guest register, health, AI, RNG, schedule or position writes')
    literal = r'"(?:[^"\\]|\\.)*"'
    pairs = re.findall(r'once\((' + literal + r'),\s*(' + literal + r')\)', text)
    need(len(pairs) == 3, 'Exactly three explicit original strategy/local-state/boss-dispatch edits')
    decoded = [(json.loads(a), json.loads(b)) for a, b in pairs]
    need(decoded[0][0].startswith("assert(strategy=='uppercut'") and
         decoded[0][1] == decoded[0][0][:-1] + "or strategy=='guard_punish')", 'Only admit new physical strategy')
    need(decoded[1] == ('local guard_until=-1000',
         'local guard_until=-1000\nlocal gp_last,gp_leg,gp_last_leg,gp_upper,gp_guard=nil,nil,-1000,-1000,-1000'),
         'Only controller-local timing state added')
    need(decoded[2] == ("(strategy=='zoning' or leg_tactic) and (other.roster==12 or other.roster==13)",
         "(strategy=='zoning' or strategy=='guard_punish' or leg_tactic) and (other.roster==12 or other.roster==13)"),
         'Original native boss controller unchanged, only dispatch admits strategy')
    for before, after in decoded:
        need(source.count(before) == 1, 'Unique original transformation: ' + before)
        source = source.replace(before, after)
    before = json.loads(re.search(r'local original=(' + literal + ')', text)[1])
    block = re.search(r'local replacement=\[\[\n(.*?)\]\]', text, re.S)[1]
    need(before == "   elseif strategy=='zoning' then\n" and source.count(before) == 1,
         'Unique non-boss zoning branch insertion')
    need(block.startswith("   elseif strategy=='guard_punish' and (other.roster==5 or other.roster==10 or other.roster==18) then\n") and
         block.endswith("   elseif strategy=='zoning' or strategy=='guard_punish' then\n"),
         'Only true Mileena/Scorpion/Sonya grounded policy; other roster uses original zoning')
    need(block.count("press('Up')") == 0 and block.count("press('Low Punch')") == 1 and
         block.count("log('GUARD_FIELD'") == block.count("log('GUARD_DECISION'") == 1,
         'No retreat-jump spam; full actual fields/decisions logged; only physical leg command')
    source = source.replace(before, block)
    sink = json.loads(re.search(r'local guest_sink=(' + literal + ')', text)[1])
    need(source.count(sink) == 1 and
         "once(guest_sink,'_campaign_guest(raw)')" in text, 'One entire initialized guest remains RAM-only')
    source = source.replace(sink, '_campaign_guest(raw)')
    need(source.count('screen:snapshot(') == 6, 'Six original native media sinks retained')
    source = source.replace('screen:snapshot(', '_campaign_emit(')
    need('guest_maincpu.bin' not in source and 'screen:snapshot(' not in source and
         'mk2ks_mileena_campaign_trace_v3848.lua' in text and "assert(limit==5900," in text,
         'No new raw guest/raster files; native swallowing observer and host-only deadline retained')
    need(not re.search(r'write_u\d+|:write_|load_?state|\.value\s*=(?!=)', source),
         'Expanded original controller still only physical buttons/read-only observers')
    return dict(originalSourceSHA256=sha(original), wrapperSHA256=sha(wrapper),
                expandedControllerSHA256=hashlib.sha256(source.encode()).hexdigest().upper(),
                explicitControllerEdits=4, originalNativeMediaSinks=6,
                wholeGuestRAMSinkChanges=1, bossControllerBodyUnchanged=True,
                gameSourceOrPlayableChanges=0, fullPortAcceptance=False)


def main():
    need(not OUT.exists(), 'Fresh immutable source preflight')
    report = source_boundary()
    report.update(passed=True, runtimeSyntaxProven=False, campaignClearAccepted=False,
                  inputHashes={str(p.resolve()): sha(p) for p in
                    (Path(__file__), ROOT / 'mk2ks_guard_punish_campaign_ram_v4112.lua',
                     ROOT / 'mk2ks_guard_punish_campaign_ram_v4108.lua',
                     ROOT / 'mk2ks_natural_campaign_shao_ring_retreat_v3485.lua',
                     ROOT / 'tools/run_sonya_guard_punish_campaign_v4113.py',
                     ROOT / 'audit_v4111_sonya_guard_punish_campaign_observed/report.json',
                     ROOT / 'audit_v4110_sonya_guard_punish_p2_campaign/stderr.log')})
    OUT.mkdir()
    need(subprocess.run(['compact.exe', '/C', '/I', '/Q', '/S:' + str(OUT)], capture_output=True).returncode == 0,
         'Compress before writing evidence')
    (OUT / 'report.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({k: v for k, v in report.items() if k != 'inputHashes'}, indent=2))


if __name__ == '__main__':
    main()
