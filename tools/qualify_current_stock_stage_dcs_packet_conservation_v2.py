"""Correct v1's byte-equality wording: full source differs only by CRLF."""
from pathlib import Path
source = Path(__file__).with_name('qualify_current_stock_stage_dcs_packet_conservation.py').read_text()
source = source.replace('audit_current_stock_stage_dcs_packet_conservation_checked',
                        'audit_current_stock_stage_dcs_packet_conservation_v2_checked')
source = source.replace('currentHostSoundFunctionExactlyConserved=True,',
                        'currentHostSoundFunctionLogicalSourceExactlyConserved=True, rawFunctionBytesEqual=False,\n                correction="V1 byte-for-byte wording was too strong: actual function bytes differ only by newline encoding; whole normalized function equality and all transport gates pass. V1 retained as executed.",')
source = source.replace('is byte-for-byte conserved from', 'has identical entire normalized-line-ending source to')
marker = 'function_hash = source_gate(current, historical)'
assert source.count(marker) == 1
source = source.replace(marker, marker + '''
    current_raw = current_path.read_bytes().split(b'void midtunit_state::midtunit_sound_w(',1)[1]
    old_raw = old_path.read_bytes().split(b'void midtunit_state::midtunit_sound_w(',1)[1]
    assert current_raw != old_raw
    assert current_raw.replace(b'\\r\\n',b'\\n') == old_raw.replace(b'\\r\\n',b'\\n')
''')
exec(compile(source, __file__, 'exec'))
