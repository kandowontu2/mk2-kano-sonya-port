"""Only replace the rejected byte literal with complete original opcode words."""
import struct
from pathlib import Path
import qualify_native_selector_opposite_roles_geometry as rejected

ROOT=rejected.ROOT
SOURCE=ROOT/'tools/qualify_native_selector_opposite_roles_throw_floor_geometry.py'
IMPORT_FAILURE=ROOT/'audit_native_selector_opposite_roles_throw_floor_geometry_import_rejection/report.json'
source=SOURCE.read_text()
before="BRANCH=bytes.fromhex('A0B50002E00BF7FF0DB00002E0090000FCFFC9093A00E1090000F4FFC2090060A31884701070B6000ECA280C0506687FF18C0')"
after="BRANCH=struct.pack('<25H',0xB5A0,0x0200,0x0BE0,0xFFF7,0xB00D,0x0200,0x09E0,0,0xFFFC,0x09C9,0x003A,0x09E1,0,0xFFF4,0x09C2,0x6000,0x18A3,0x0147,0x0B07,0x0060,0xA2EC,0xC080,0x6650,0xFF87,0xC018)"
source=rejected.current.replace(source,before,after)
source=rejected.current.replace(source,
    "OUT=ROOT/'audit_native_selector_opposite_roles_throw_floor_geometry_checked'",
    "OUT=ROOT/'audit_native_selector_opposite_roles_throw_floor_geometry_words_checked'")
source=rejected.current.replace(source,
    'for path in (Path(__file__),PARENT,FAILURE,Path(rejected.__file__),Path(template.__file__),',
    'for path in (Path(__file__),SOURCE,IMPORT_FAILURE,PARENT,FAILURE,Path(rejected.__file__),Path(template.__file__),')
scope=dict(__file__=__file__,struct=struct,SOURCE=SOURCE,IMPORT_FAILURE=IMPORT_FAILURE)
exec(compile(source,__file__+'::complete_original_instruction_words_only','exec'),scope)
OUT=scope['OUT']
floor_gate=scope['floor_gate']
bindings=scope['bindings']
execute=scope['execute']
safe_execute=scope['safe_execute']
