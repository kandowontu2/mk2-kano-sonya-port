"""Compare all actual runtime chips with current native build inputs."""
import zipfile
from pathlib import Path
from current_graphics import verify_archive_sockets

PORT=Path(__file__).resolve().parent
SRC=PORT.parent/'baseline/mk2-rebuild-main/srcp'

def verify(archive, execution):
    for lane,name in enumerate(('mk321u54.bin','mk321u63.bin')):
        assert archive.read(name)==b''.join((SRC/f'rom/P12{part}.{lane}').read_bytes() for part in ('F8','FC'))
    verify_archive_sockets(archive)
    sound='soundp' if '--sound-candidate' in execution['testArguments'] else 'soundw'
    for chip in range(2,6):
        assert archive.read(f'l1_mortal_kombat_3_u{chip}_music_spch.u{chip}')==(SRC.parent/sound/f'U{chip}.ROM').read_bytes()
    with zipfile.ZipFile(PORT.parents[1]/'roms/mk2.zip') as original:
        for bank,(first,second) in enumerate(((14,19),(16,20),(17,22))):
            for lane,(letter,socket) in enumerate((('ug',first),('uj',first),('ug',second),('uj',second))):
                assert archive.read(f'l1_mortal_kombat_3_u{133-bank*4-lane}_game_rom.u{133-bank*4-lane}')==original.read(f'l1_mortal_kombat_ii_game_rom_{letter}{socket}.{letter}{socket}')
