"""Retain failed checker; cover every recorded field and original RNG result.

Actual original FFA123D0 is CALL RNG, DEC, ADD base, JR record dispatcher.
For a two-choice family both base and base+1 are real stock voices. Captures
contain0..626, not merely0..450: inspect the entire actual body timeline.
"""
from pathlib import Path
import struct
import review_native_kano_laser_victim_audio_matrix as failed

source=Path(failed.__file__).read_text()
changes=[
    ("OUT=ROOT/'audit_native_kano_laser_victim_audio_matrix_review'",
     "OUT=ROOT/'audit_native_kano_laser_victim_audio_matrix_full_timeline_review'"),
    ("int(routes[-1]['a0'],16) in (0x36,0x38)",
     "int(routes[-1]['a1'],16) in (0x36,0x38) and int(routes[-1]['a0'],16) in (int(routes[-1]['a1'],16),int(routes[-1]['a1'],16)+1)"),
    ("    return dict(selectedStockVoice=int(routes[-1]['a0'],16)",
     "    native=(ROOT/'mk2/mk2-maincpu.bin').read_bytes();at=(0xffa123d0-0xff800000)//8\n"
     "    need(native[at:at+12]==struct.pack('<6H',0x0d5f,0xeae0,0xff80,0x1420,0x4020,0xc010),'Whole original native RNG/DEC/ADD/JR voice-selection kernel')\n"
     "    return dict(originalRNGKernelHex=native[at:at+12].hex().upper(),selectedStockVoice=int(routes[-1]['a0'],16)"),
    ('cases=[];pins=', 'observed_fields=0;cases=[];pins='),
    ("need(len(fields)==902 and {(int(r['age']),int(r['slot'])) for r in fields}=={(a,s) for a in range(451) for s in (1,2)},",
     "last=max(int(r['age']) for r in fields);need(450<=last<=750 and len(fields)==(last+1)*2 and {(int(r['age']),int(r['slot'])) for r in fields}=={(a,s) for a in range(last+1) for s in (1,2)},"),
    ('Every actor field in complete0..450 native body timeline, not selected IDs',
     'Every actor field in complete recorded native body timeline including all0..450 required fields'),
    ("frames+=review['wholeNativeMixedWaveform']['comparedStereoFrames']",
     "frames+=review['wholeNativeMixedWaveform']['comparedStereoFrames'];observed_fields+=len(fields)"),
    ('totalIdentityFieldsChecked=5412','totalIdentityFieldsChecked=observed_fields'),
    ('trueIdentityFields=5412','trueIdentityFields=observed_fields'),
    ("        cases=[]", "        cases=[]"),
]
# A no-op boundary is unnecessary; preserve only real, exact corrections.
changes.pop()
for old,new in changes:
    failed.need(source.count(old)==1,'Exact failed checker boundary; no game/input/audio/source changes')
    source=source.replace(old,new)
anchor="        cases=[]"  # The variables above are deliberately initialized in one line.
pin_anchor="        for victim in (4,17,18):"
addition='''        for path in (ROOT/'tools/review_native_kano_laser_victim_audio_matrix.py',
                     ROOT/'audit_native_kano_laser_victim_audio_matrix_review/failure.txt',ROOT/'mk2/mk2-maincpu.bin'):
            pins[str(path)]=sha(path)
        for victim in (4,17,18):'''
failed.need(source.count(pin_anchor)==1,'Original full six-case loop retained')
source=source.replace(pin_anchor,addition)
scope=dict(__name__='__main__',__file__=str(Path(__file__).resolve()),struct=struct)
exec(compile(source,str(Path(__file__).resolve()),'exec'),scope)
