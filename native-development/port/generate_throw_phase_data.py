"""Own throw phase data, extracted as typed art records, never CPU opcodes.

Not a complete throw implementation: release, facing and full victim coverage
must be implemented and qualified before these phase records can be enabled.
"""
import hashlib
import json
from pathlib import Path
import struct
import import_character_art as art

PORT=Path(__file__).resolve().parent
OUT=PORT/'generated_throw'
assert not OUT.exists()
OUT.mkdir()
p=art.parser
data=(art.ROOT/'mk3/mk3-maincpu.bin').read_bytes()
assert hashlib.sha256(data).hexdigest().upper()=='1BC7A53A023F15B20F01398F87E38478A27C670DF27EA320E36125D0957EE651'
lines=['; Own throw ART phases and explicit paired-victim XY records.',
       '; Not executable donor code. Not a complete throw action.',
       '        .include mainequ.asm','        .data']
refs=set();report={}
expected={'kano':(2,3,2),'sonya':(1,5,2)}
for actor,root,block in [('kano',p.KANO_MAIN,p.KANO_BLOCK),('sonya',p.SONYA_MAIN,p.SONYA_BLOCK)]:
    cursor=p.stock_file(p.u32(data,p.stock_file(root)+35*4))
    phases=[]
    for phase,count in enumerate(expected[actor]):
        poses=[]
        for _ in range(count):
            pose=p.u32(data,cursor);cursor+=4
            assert p.frame_group(data,pose,*block)
            label=f'ks_{actor}_pose_{pose:08x}'
            assert f'.def {label}\n' in (PORT/'generated_packed'/f'{actor.upper()}ART.ASM').read_text()
            refs.add(label);poses.append(label)
        tail=p.u32(data,cursor);cursor+=4
        facing=False
        if actor=='kano' and phase==2:
            # Preserve evidence of the facing command; do not silently discard
            # it or pretend that phase-only art constitutes the finished move.
            assert tail==2 and p.u32(data,cursor)==0
            cursor+=4;facing=True
        else:assert tail==0
        name=f'ks_{actor}_throw_phase{phase}'
        lines.extend([f'        .def {name}',name,'        .long '+','.join(poses+['0'])])
        phases.append({'label':name,'poses':poses,'nativeFacingCommandAfterPhase':facing})
    victims={}
    for owner,index in [('kano',38),('sonya',39)]:
        cursor=p.stock_file(p.u32(data,p.stock_file(root)+index*4))
        records=[]
        count=3 if owner=='kano' else 5
        for _ in range(count):
            token,xy,pose=struct.unpack_from('<III',data,cursor);cursor+=12
            assert token==10 and p.frame_group(data,pose,*block)
            x,y=struct.unpack('<hh',struct.pack('<I',xy))
            label=f'ks_{actor}_pose_{pose:08x}'
            assert f'.def {label}\n' in (PORT/'generated_packed'/f'{actor.upper()}ART.ASM').read_text()
            refs.add(label);records.append([x,y,label])
        assert p.u32(data,cursor)==0;cursor+=4
        flight=[]
        while p.u32(data,cursor)!=0:
            pose=p.u32(data,cursor);cursor+=4
            assert len(flight)<8 and p.frame_group(data,pose,*block)
            label=f'ks_{actor}_pose_{pose:08x}'
            refs.add(label);flight.append(label)
        name=f'ks_th_{owner}_v_{actor}'
        lines.extend([f'        .def {name},{name}_flight',name])
        for x,y,label in records:lines.extend([f'        .word {x},{y}',f'        .long {label}'])
        lines.extend([name+'_flight','        .long '+','.join(flight+['0'])])
        victims[owner]={'pairedRecordCount':count,'records':records,'flightPoses':flight}
    report[actor]={'bodyPhases':phases,'asVictim':victims,'runtimeVerified':False}
lines[4:4]=['        .ref '+name for name in sorted(refs)]
source=('\n'.join(lines)+'\n').encode()
(OUT/'KSTHANI.ASM').write_bytes(source)
result={'actors':report,'sourceSHA256':hashlib.sha256(source).hexdigest().upper(),
        'originalRosterVictimAdaptationPending':True,'pairedRuntimePending':True,
        'kanoFacingControlPending':True,'completeThrowMove':False,'fullPortVerified':False}
(OUT/'THROW_DATA.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'bodyPhaseLengths':expected,'addedVictimPairs':4,'completeThrowMove':False}))
