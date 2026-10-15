"""Current genuine Pit victims/continues and contiguous display/audio inventory.

Actual native state/cache/initial pose/20 falling steps/impact/exit and paid
continue in one slot per character. Display inventory is NOT raster replay;
non-silent PCM is NOT waveform fidelity. Own stage performers, other arenas,
cinematic completeness and full campaigns remain unproven.
"""
import argparse
import hashlib
import json
from pathlib import Path
import re
import struct
import wave
import numpy as np
from PIL import Image
import verify_native_pit_scene_v680_v1 as scene
import verify_native_candidate_v798 as candidate

def rows(log, tag):
    return [dict(re.findall(r'(\w+)=([^\s]+)', line)) for line in log.splitlines()
            if line.startswith('MK2_PIT_DISPLAY_' + tag + ' ')]

def impact_commands(log, proof, original):
    episode = proof['episodes'][0]
    ports = [r for r in rows(log, 'SOUND') if int(r['frame']) == proof['pit_impact']
             and int(r['a8'], 16) == episode['actor']]
    scene.need(len(ports) == 4 and all(r['at'] == '01D01030' and r['mask'] == 'FFFF'
               and int(r['data'], 16) >> 8 == 255 and int(r['a13'], 16) == episode['main']
               and r['writes'] == '0' and r['assistance'] == 'none' for r in ports),
               'Two complete native effect/gender commands belong to actual Pit victim')
    scene.need([r['pc'] for r in ports] == ['FFA13C90', 'FFA13D60'] * 2,
               'Original native high/low serialized DCS command stores')
    commands = [((int(ports[i]['data'], 16) & 255) << 8) | (int(ports[i+1]['data'], 16) & 255)
                for i in (0, 2)]
    voice = 0xcc if proof['actual_id'] == 17 else 0xce
    native = [struct.unpack_from('<HH', original, (0xffa0ef20 + group * 32 - 0xff800000)//8)[1]
              for group in (0xcf, voice)]
    scene.need(commands == [native[0], native[1] + 1], 'Wrong actual impact effect or male/female voice')
    return {'native_commands': [f'{c:04X}' for c in commands], 'original_voice_group': f'{voice:02X}'}

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('root', type=Path); parser.add_argument('output', type=Path)
    args = parser.parse_args(); root, output = args.root.resolve(), args.output.resolve()
    scene.need(not output.exists(), 'Do not overwrite proof')
    tracked = {}; reports = {}
    def track(path, wanted=None):
        path = Path(path); actual = hashlib.sha256(path.read_bytes()).hexdigest().upper()
        scene.need(wanted is None or actual == wanted, 'Executed input changed: ' + str(path))
        tracked[str(path.resolve())] = actual
    for module in (scene, candidate):track(Path(module.__file__))
    track(Path(__file__))
    original_path = root/'mk2/mk2-maincpu.bin'; track(original_path,
        '45B3285496DB555EFAF4A3608A4F59845DD47A82E4A0593607E0592F47B36F23')
    original = original_path.read_bytes()
    checkpoint_path = root/'audit_v796_current_audio_babality_checkpoint/verification.json'
    track(checkpoint_path); checkpoint = json.loads(checkpoint_path.read_text())
    for path, value in checkpoint['checked_inputs'].items():track(path, value)
    prior_path = root/'audit_v741_native_babality_performers_checked_inputs/verification.json'
    track(prior_path); prior = json.loads(prior_path.read_text())
    old_payload = root/'diagnostic_v737_native_babality_performers/roms/mk2ks/mk2ks.mdata'
    wanted = prior['input_hashes'].get(str(old_payload))
    scene.need(wanted == '1367D5A0D42C661CF555F42231A20A650C28E107AB9C80BD821C0BEA7EB4D5EF',
               'Previous Pit-containing payload not pinned')
    track(old_payload, wanted)
    payload_path = root/candidate.NAME/'roms/mk2ks/mk2ks.mdata'
    track(payload_path, candidate.PAYLOAD)
    payload = payload_path.read_bytes(); old = old_payload.read_bytes()
    scene.need(len(payload) == len(old) == 0x200000 and payload[0x100000:] == old[0x100000:],
               'Entire native Pit-containing payload half changed')
    old_guest_path = root/'audit_v684_pit_guest_rom_integrity/diagnostic_v680_native_pit_initial_cache/guest_maincpu.bin'
    track(old_guest_path, '8395DD271BA3A8B8FABED892E9C3E14E2BA51EC8D952A041BA667AFB8015010D')
    guest_path = root/'audit_v790_kano_friendship_p1/guest_maincpu.bin'
    track(guest_path, '9F55AA553617BD761BD3F5DD6D9701439DD98BA69527544DBB4DD744DC14CA12')
    old_guest, guest = old_guest_path.read_bytes(), guest_path.read_bytes()
    for first, last in ((0xf9380, 0xf93c0), ((0xff85bd00-0xff800000)//8, (0xff85bdb0-0xff800000)//8),
                        ((0xff85c300-0xff800000)//8, (0xff85c700-0xff800000)//8),
                        ((0xff838790-0xff800000)//8, (0xff838840-0xff800000)//8)):
        scene.need(guest[first:last] == old_guest[first:last], 'Native Pit constructor/cache/copier/faller changed')
    build_path = root/candidate.NAME/'build-info.json'; track(build_path)
    build = json.loads(build_path.read_text())
    scene.need(build['executable_sha256'] == candidate.EXE and build['payload_sha256'] == candidate.PAYLOAD,
               'Wrong build')
    track(root/candidate.NAME/'mkport_candidate.exe', candidate.EXE)
    for fighter, side, name in (('kano', 1, 'audit_v799_kano_pit_audio_p1'),
                                ('sonya', 2, 'audit_v799_sonya_pit_audio_p2')):
        folder = root/name
        metadata = json.loads((folder/'result.json').read_text(encoding='utf-8-sig'))
        manifest = json.loads((folder/'input_hashes_before.json').read_text(encoding='utf-8-sig'))
        scene.need(metadata['exit_code'] == 0 and metadata['candidate'] == candidate.NAME and
                   metadata['executable_sha256'] == candidate.EXE and metadata['payload_sha256'] == candidate.PAYLOAD
                   and metadata['player'] == fighter and metadata['human_slot'] == side
                   and metadata['assistance'] == 'none' and metadata['seconds'] == 900
                   and manifest == metadata['input_hashes'], 'Wrong/incomplete current launch')
        scene.need(all(manifest.get(path) == value for path, value in build['input_hashes'].items()),
                   'Actual build inputs missing from launch')
        for path, value in manifest.items():
            track(path, value)
            if Path(path).suffix in ('.lua', '.ps1', '.json'):
                track(folder/'input_sources'/Path(path).name, value)
        for source in ('mk2ks_natural_campaign_probe_v12.lua', 'mk2ks_natural_pit_display_v680_v1.lua'):
            text = (folder/'input_sources'/source).read_text()
            scene.need(not re.search(r'write_u\d+|:write_|load_?state|\.value\s*=(?!=)', text), 'Guest-state assistance')
        runner = (folder/'input_sources/run_natural_pit_audio_v680_v1.ps1').read_text()
        scene.need('-nocheat' in runner and '-wavwrite' in runner and '-noautoframeskip -frameskip 0' in runner,
                   'Actual cheat-disabled full capture options absent')
        log = (folder/'run.log').read_text(encoding='utf-8-sig')
        proof = scene.verify_log(log, fighter, side=side)
        proof['impact_sound_routing'] = impact_commands(log, proof, original)
        palettes = scene.rows(log, 'PIT_PALETTE')
        scene.need(len(palettes) == len(proof['episodes']), 'Missing original normal palette constructors')
        for row in palettes:
            pointer = 0xff800000 + (0xfda00 if fighter == 'kano' else 0xfdb00) * 8
            expected = struct.unpack_from('<65H', guest, (pointer-0xff800000)//8 + 2)
            scene.need(int(row['id']) == proof['actual_id'] and row['variant'] == '0' and row['count'] == '65'
                       and int(row['pointer'], 16) == pointer
                       and tuple(int(c, 16) for c in row['colors'].split(',')) == expected,
                       'Actual Pit constructor substituted or recoloured fighter')
        snaps, terminal = rows(log, 'SNAP'), rows(log, 'RESULT')
        origin = proof['pit_enter']
        scene.need(len(terminal) == 1 and int(terminal[0]['origin']) == origin and
                   int(terminal[0]['snapshots']) == len(snaps) == 331 and
                   [int(r['frame']) for r in snaps] == list(range(origin, origin+331)),
                   'Complete first-scene contiguous display window missing')
        seconds = [float(row['seconds']) for row in snaps]
        scene.need(all(a < b for a, b in zip(seconds, seconds[1:])), 'Non-monotonic capture times')
        for row in snaps:
            photo = folder/'snap'/row['file']
            with Image.open(photo) as image:
                scene.need(image.size == (400, 254), 'Wrong native captured screen size'); image.load()
        with wave.open(str(folder/'native_audio.wav'), 'rb') as wav:
            scene.need((wav.getnchannels(), wav.getsampwidth(), wav.getframerate()) == (2, 2, 48000), 'Native PCM format')
            first, last = int((seconds[0]-2)*48000), int((seconds[-1]+1)*48000)
            scene.need(0 <= first < last <= wav.getnframes(), 'Scene audio interval missing')
            wav.setpos(first); pcm = np.frombuffer(wav.readframes(last-first), dtype='<i2').astype(np.int32)
            scene.need(np.count_nonzero(pcm) > 48000, 'No audible native scene mix')
            proof['pcm_inventory'] = {'peak': int(np.max(np.abs(pcm))), 'nonzero_samples': int(np.count_nonzero(pcm)),
                                      'waveform_fidelity_acceptance': False}
        proof['retained_display_fields'] = 331
        proof['rendered_replay_acceptance'] = False
        for path in folder.rglob('*'):
            if path.is_file():track(path)
        reports[name] = proof
    output.mkdir(parents=True)
    report = {'scope': __doc__, 'candidate': candidate.NAME, 'cases': reports, 'checked_inputs': tracked,
              'boundedCurrentPitVictimStateContinueAcceptance': True, 'cinematicAcceptance': False,
              'audioWaveformAcceptance': False, 'ownStagePerformerAcceptance': False, 'fullPortAcceptance': False}
    (output/'verification.json').write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps({'cases': len(reports), 'terminal_fields': [v['terminal_frame'] for v in reports.values()],
                      'retained_display_fields': 662, 'checked_inputs': len(tracked),
                      'boundedCurrentPitVictimStateContinueAcceptance': True, 'fullPortAcceptance': False}, indent=2))

if __name__ == '__main__':
    main()
