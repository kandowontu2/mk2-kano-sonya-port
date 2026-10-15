"""Finite current stock-victim packet transport, not fresh waveform acceptance."""
import copy
import hashlib
import json
import re
from pathlib import Path
import verify_native_source_sync as sync

ROOT = sync.ROOT
OUT = ROOT / 'audit_current_stock_stage_dcs_packet_conservation_checked'
OLD = ROOT / 'diagnostic_native_paired_stumble_table_ps7'


def sound_function(text):
    marker = 'void midtunit_state::midtunit_sound_w('
    assert text.count(marker) == 1
    return text[text.index(marker):]


def source_gate(current, historical):
    assert current == historical, 'Entire historical accepted host sound transport retained'
    for literal in ('m_maincpu->pc() == 0xffa13c90U', 'm_maincpu->pc() == 0xffa13d60U',
                    '!native_packet && (data == 0xfff8 || data == 0xfff7)',
                    '!native_packet && (data == 0xfffa || data == 0xfff9)',
                    '!native_packet && data >= 0xfffb && data <= 0xfffe',
                    'm_dcs->reset_w(data & 0x100);', 'm_dcs->data_w(data & 0xff);'):
        assert literal in current, literal
    return hashlib.sha256(current.encode()).hexdigest().upper()


def packet_gate(rows):
    assert rows and all(r['writes'] == '0' and r['assistance'] == 'none' and r['mute'] == '0' for r in rows)
    native = [r for r in rows if r['pc'] in ('FFA13C90', 'FFA13D60')]
    markers = [r for r in rows if r['pc'] not in ('FFA13C90', 'FFA13D60')]
    assert len(markers) == 1 and markers[0]['pc'] == 'FFFB7140' and markers[0]['word'] in ('FFFD', 'FFFE')
    assert len(native) > 10 and len(native) % 2 == 0
    pairs = []
    for high, low in zip(native[::2], native[1::2]):
        assert high['pc'] == 'FFA13C90' and low['pc'] == 'FFA13D60'
        assert high['frame'] == low['frame'] and high['age'] == low['age']
        assert all(0xFF00 <= int(r['word'], 16) <= 0xFFFF for r in (high, low))
        pairs.append(dict(age=int(high['age']), packet=f"{int(high['word'],16)&255:02X}{int(low['word'],16)&255:02X}"))
    return dict(nativeBytes=len(native), completePairs=len(pairs), packets=pairs,
                nativeFFMarkerRangeBytes=sum(0xFFF7 <= int(r['word'],16) <= 0xFFFE for r in native),
                separateOwnWinnerMarker=markers[0])


def main():
    assert not OUT.exists()
    verified = sync.verify()
    current_path = ROOT / 'mame-mkp/src/mame/midway/midtunit_m.cpp'
    old_path = OLD / 'input_sources/mame-mkp/src/mame/midway/midtunit_m.cpp'
    old_manifest = json.loads((OLD / 'build-info.json').read_text(encoding='utf-8-sig'))
    old_pins = {str(Path(k).resolve()): v for k,v in old_manifest['input_hashes'].items()}
    assert old_pins[str(old_path.resolve())] == sync.sha(old_path)
    current = sound_function(current_path.read_text())
    historical = sound_function(old_path.read_text())
    function_hash = source_gate(current, historical)
    historical_reports = [ROOT/'audit_native_cross_tomb_19_audio_matrix_checked/report.json',
                          ROOT/'audit_native_current_pit_19_audio_matrix_checked/report.json']
    for path in historical_reports:
        report = json.loads(path.read_text())
        assert report['passed'] and report.get('candidate', 'diagnostic_native_paired_stumble_table_ps7') == 'diagnostic_native_paired_stumble_table_ps7'
    cases = []
    pins = {str(p): sync.sha(p) for p in [current_path, old_path, OLD/'build-info.json', *historical_reports]}
    groups = [('audit_current_stock_tomb_audio_checked', 'audit_current_stock_tomb_audio_'),
              ('audit_current_stock_pit_kano_audio_checked', 'audit_current_stock_pit_other_sides_audio_'),
              ('audit_current_stock_pit_sonya_audio_checked', 'audit_current_stock_pit_other_sides_audio_')]
    faults = []
    for report_name, prefix in groups:
        path = ROOT/report_name/'report.json'; report=json.loads(path.read_text())
        assert report['passedWinnerCueLifetime']; pins[str(path)] = sync.sha(path)
        for case in report['cases']:
            log = ROOT/(prefix+case['case']+'_runtime')/'run.log'
            assert sync.sha(log) == case['logSHA256']; pins[str(log)] = sync.sha(log)
            rows = [dict(re.findall(r'(\w+)=([^\s]+)', line)) for line in log.read_text().splitlines() if line.startswith('MK2_STAGE_AUDIO_WORD ')]
            proof = packet_gate(rows)
            cases.append(dict(case=case['case'], logSHA256=sync.sha(log), **proof))
            for label, mutation in [('missing native low byte', lambda r: r.pop(next(i for i,x in enumerate(r) if x['pc']=='FFA13D60'))),
                                    ('wrong native store PC', lambda r: r[0].update(pc='FFA13D60')),
                                    ('invalid native sign extension', lambda r: r[0].update(word='1234')),
                                    ('split pair field', lambda r: r[0].update(frame='0'))]:
                bad=copy.deepcopy(rows); mutation(bad)
                try: packet_gate(bad)
                except AssertionError: faults.append(dict(case=case['case'], kind=label))
                else: raise AssertionError('Fault admitted: '+label)
    for label, bad in [('removed packet PC protection', current.replace('!native_packet &&','',1)),
                       ('changed DCS low-byte delivery', current.replace('data & 0xff);','data & 0xfe);'))]:
        assert bad != current
        try: source_gate(bad, historical)
        except AssertionError: faults.append(dict(kind=label))
        else: raise AssertionError('Source fault admitted')
    assert all(sync.sha(p)==v for p,v in pins.items())
    report=dict(passed=True, currentHostSoundFunctionExactlyConserved=True,
                soundFunctionSHA256=function_hash, currentStockVictimCompletePacketTransport=cases,
                effectiveFaultsRejected=faults, sourceSyncCompileInputs=verified['trackedCanonicalCompileInputs'],
                inputHashes=pins, newEmulatorRuns=0, newMedia=0, freshWaveformOrHeardMixAccepted=False,
                historicalFiniteAudioAcceptanceRetained=True, fullPortAcceptance=False,
                scope='Four current earned stock-victim Tomb/Pit cases: every captured native sound byte belongs to a complete same-field sign-extended two-byte original packet, and the entire host DCS transport function is byte-for-byte conserved from the historical accepted 19-channel finite Tomb/Pit audio candidate. Native FF marker-range bytes cannot be stolen by imported marker routes. This is transport/source conservation, not a fresh stock voice sample, priority/RNG, DAC or heard-mix proof, and does not transfer whole old gameplay.')
    OUT.mkdir(); (OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(passed=True,cases=len(cases),nativePairs=sum(c['completePairs'] for c in cases),faults=len(faults))))


if __name__ == '__main__':
    main()
