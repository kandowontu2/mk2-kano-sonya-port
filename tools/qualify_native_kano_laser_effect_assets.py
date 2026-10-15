"""Original grey smoke/laser bone recipes and full native camera mapping.

Reconstruct whole actual source initializer in RAM; source-only acceptance.
No shortened effects, red-cloud substitution, guest assistance, new game
build, ROM/gfx copies or public promotion. Actual emitters/runtime remain.
"""
import gzip
import hashlib
import inspect
import json
import re
import struct
import subprocess
import traceback
from pathlib import Path

import qualify_native_kano_laser_phases as prior

ROOT=prior.ROOT
STAGE=ROOT/'source_native_kano_laser_effect_assets'
OUT=ROOT/'audit_native_kano_laser_effect_assets_source'
FIRST,LAST=0xafb80,0xafdc0
BEGIN,END='// KANO_LASER_EFFECT_ASSETS_BEGIN','// KANO_LASER_EFFECT_ASSETS_END'
need,sha,address,u32=prior.need,prior.sha,prior.address,prior.u32


def contract(guest,base,donor):
    expected=bytearray(base)
    need(all(value==255 for value in base[FIRST:LAST]),'Unused actual prior initialized allocation')
    frames=struct.unpack_from('<6I',donor,(0xffa9dc40-0xff800000)//8)
    need(frames==(0xffc884e0,0xffc88570,0xffc885e0,0xffc88650,0xffc886c0,0),
         'Full actual original grey smoke stream')
    palette_at=(0xffcd6540-0xff800000)//8
    palette=donor[palette_at:palette_at+34]
    need(struct.unpack_from('<HH',palette)==(16,0),'Original grey palette count and transparent entry')
    expected[0xafc60:0xafc82]=palette
    details=[]
    for index,source in enumerate(frames[:-1]):
        original=(source-0xff800000)//8
        width,height,x,y,graphic,flags=struct.unpack_from('<4HIH',donor,original)
        need(0<width<=180 and 0<height<=180 and 0<=graphic<0x08000000,'Actual owned smoke descriptor')
        frame=0xafb80+index*20;group=0xafc00+index*8
        expected[frame:frame+14]=donor[original:original+14]
        struct.pack_into('<I',expected,frame+8,graphic+0x10000000)
        struct.pack_into('<IH',expected,frame+14,address(0xafc60),0)
        struct.pack_into('<II',expected,group,address(frame),0)
        struct.pack_into('<I',expected,0xafc40+index*4,address(group))
        details.append(dict(original=f'{source:08X}',nativeFrame=f'{address(frame):08X}',
            nativeComposite=f'{address(group):08X}',size=[width,height],anchor=[x,y],
            originalGraphic=f'{graphic:08X}',nativeGraphic=f'{graphic+0x10000000:08X}',flags=f'{flags:04X}'))
    struct.pack_into('<I',expected,0xafc54,0)
    recipe_at=(0xffa94880-0xff800000)//8
    recipes=[]
    for part in range(5):
        count,x,y,gravity,frame,stream,flags,xmin,yrange,ymin,cadence,arcs=struct.unpack_from('<4H2I6H',donor,recipe_at+part*28)
        signed=lambda value:value-65536 if value&0x8000 else value
        need(count==(2,2,10,1,1)[part] and flags&1 and gravity==0x4000 and
             stream==(0xffa98680,0xffa98860,0xffa98ec0,0xffa99080,0xffa993e0)[part] and
             frame==u32(donor,(stream-0xff800000)//8),'Actual original paired laser bones and same imported bone art')
        values=(count,count*2,signed(x)&0xffffffff,signed(y)&0xffffffff,gravity,
                (flags&0xfffe)<<8,xmin<<8,yrange<<8,ymin<<8,cadence,arcs,address(0xae500+part*56))
        struct.pack_into('<12I',expected,0xafca0+part*48,*values)
        recipes.append(dict(part=part,sourceCount=count,independentCount=count*2,offset=[signed(x),signed(y)],
            gravity=gravity,xVelocityRange=(flags&0xfffe)<<8,xVelocityMinimum=xmin<<8,
            yVelocityRange=yrange<<8,yVelocityMinimum=ymin<<8,cadence=cadence,arcs=arcs,
            directions='Each source item emits separately randomized positive and negative X particles',
            nativeStream=f'{values[-1]:08X}'))
    need(struct.unpack_from('<H',donor,recipe_at+140)[0]==0 and
         sum(row['independentCount'] for row in recipes)==32,'Whole five-row recipe and32pairedparticles')
    struct.pack_into('<HIH',expected,0xafda0,0x0d5f,0xff8381d0,0x0960)
    need(guest==expected,'Whole guest exact: five grey frames, palette, own bone recipe and native camera wrapper only')
    need(guest[0xadf40:0xadf5e]==base[0xadf40:0xadf5e] and
         guest[0xae000:0xae900]==base[0xae000:0xae900],'Sonya red ash and shared bone art unchanged')
    return dict(greySmokeFrames=details,greySmokeColors=16,greySmokeNativeStream=f'{address(0xafc40):08X}',
        nativePalette=f'{address(0xafc60):08X}',sourceSmokeCadence=4,sourceSmokeFields=20,
        pairedBoneRecipes=recipes,boneCount=32,nativeCameraWrapper=f'{address(0xafda0):08X}',
        nativeCameraConstructor='FF8381D0',nativeCameraWorker='FFA0D4E0')


def disassemble(file,start,end):
    result=subprocess.run([str(ROOT/'mame-mkp/unidasm.exe'),str(file),'-arch','tms34010',
        '-basepc',hex(start),'-skip',hex((start-0xff800000)//8),'-count',str(end-start),'-norawbytes'],
        text=True,capture_output=True,check=True)
    return [line.split(':',1)[1].strip() for line in result.stdout.splitlines()]


def camera_contract():
    original=ROOT/'mk3/mk3-maincpu.bin';native=ROOT/'mk2/mk2-maincpu.bin'
    old_reset=disassemble(original,0xff959290,0xff959360)
    old_ctor=disassemble(original,0xff959200,0xff959290)
    native_ctor=disassemble(native,0xff8381d0,0xff838320)
    old_tracking=disassemble(original,0xff90c020,0xff90c510)
    native_tracking=disassemble(native,0xffa0d4e0,0xffa0d9d0)
    operands={0xff95fe70:0xff840020,0xff926f20:0xff80e280,0xff926960:0xff80dcc0,
        0x105d870:0x105d100,0x105f470:0x105ece0,0x105d890:0x105d120,0x105dae0:0x105d350,
        0x105f490:0x105ed00,0x105f480:0x105ecf0,0x105f4a0:0x105ed10,
        0xff90bbf0:0xff9fb280,0xff90afc0:0xff9f9e00,0xff90af30:0xff9f9d90}
    def normalize(line):
        def operand(match):
            value=int(match.group(1),16)
            if 0xff90c020<=value<0xff90c510:value+=0xffa0d4e0-0xff90c020
            else:value=operands.get(value,value)
            return f'{value:X}h'
        line=re.sub(r'\b([0-9A-F]+)h',operand,line)
        # Keep MKII's own native unsigned arena comparisons; no code patch.
        return line.replace('JRGT','JRHI').replace('JRLT','JRC')
    need(old_reset[-1]=='RETS' and [normalize(line) for line in old_reset[:-1]+old_ctor]==native_ctor,
         'Full original camera reset+constructor matches native4/103cleanup/origin/task, not a prefix coincidence')
    need([normalize(line) for line in old_tracking]==native_tracking,
         'Entire original/native tracking routines map: actual actor, origin/bounds, callback/sleep, threshold6 and anchor199')
    return dict(fullConstructorMatched=True,fullTrackingMatched=True,
        originalConstructor='FF9591E0',nativeConstructor='FF8381D0',
        originalWorker='FF90C020',nativeWorker='FFA0D4E0',threshold=6,screenAnchor=199,
        paletteProcess=False,originalReset=old_reset,originalConstructorInstructions=old_ctor,
        nativeConstructorInstructions=native_ctor,originalTracking=old_tracking,nativeTracking=native_tracking,
        differences='Native MKII globals/callbacks/scheduler and its own unsigned arena-bound comparisons retained unchanged')


def main():
    need(not OUT.exists() and not prior.visual.native.census(),'Fresh immutable successor, no live native game')
    OUT.mkdir();harness=''
    try:
        receipt=json.loads((prior.OUT/'report.json').read_text())
        need(receipt['passed'] and receipt['sourceOnlyAccepted'] and not receipt['nativeRuntimeAccepted'] and
             all(sha(p)==h for p,h in receipt['inputHashes'].items()),'Whole previous source and all dependencies conserved')
        old=(prior.STAGE/'midtunit_m.cpp').read_text();new=(STAGE/'midtunit_m.cpp').read_text()
        need(new.count(BEGIN)==new.count(END)==1,'One appended source block')
        first=new.index('\n\t'+BEGIN);last=new.index(END)+len(END);block=new[first:last]
        need(new[:first-1]+new[last:]==old,'Only appended own laser assets; previous gameplay and accepted source untouched')
        for leaf in ('midtunit.cpp','midtunit.h'):need(sha(STAGE/leaf)==sha(prior.STAGE/leaf),'Unchanged host/audio/platform source')
        previous_harness=json.loads(gzip.open(prior.OUT/'executed_sources.json.gz','rt').read())['actualNewInitializerHarness']
        anchor='\t// KANO_LASER_PHASES_END';need(previous_harness.count(anchor)==1,'Exact frozen source boundary')
        harness=previous_harness.replace(anchor,anchor+'\n'+block)
        # Compile using this successor's own output folder, never the old one.
        scope=dict(vars(prior),OUT=OUT)
        exec(compile(inspect.getsource(prior.compile_probe),__file__+'::isolated_compile','exec'),scope)
        base=prior.palette.prior.prior.prior.prior.prior.prior.visual.prior.expected()
        payload=prior.palette.prior.prior.prior.prior.prior.prior.effects.PAYLOAD.read_bytes()
        guest,probe=scope['compile_probe'](harness,base,payload)
        previous=bytearray(guest);previous[FIRST:LAST]=b'\xff'*(LAST-FIRST)
        need(hashlib.sha256(previous).hexdigest().upper()==receipt['proposedGuestSHA256'],'Whole actual prior initialized guest exact')
        donor=(ROOT/'mk3/mk3-maincpu.bin').read_bytes()
        results=contract(guest,bytes(previous),donor);camera=camera_contract();faults=[]
        for name,at in (('smoke_width',0xafb80),('smoke_graphic',0xafb88),('smoke_palette_link',0xafb8e),
            ('smoke_group',0xafc00),('smoke_stream',0xafc40),('smoke_termination',0xafc54),('grey_palette',0xafc64),
            ('paired_count',0xafca4),('own_y_anchor',0xafcac),('own_y_range',0xafcbc),
            ('bone_stream',0xafccc),('camera_call',0xafda2),('previous_sonya',0xaf090)):
            wrong=bytearray(guest);wrong[at]^=1
            try:contract(bytes(wrong),bytes(previous),donor)
            except ValueError as error:faults.append(dict(name=name,rejected=str(error)))
            else:raise ValueError('Fault admitted: '+name)
        paths=[Path(__file__),Path(prior.__file__),prior.OUT/'report.json',prior.OUT/'executed_sources.json.gz',
            ROOT/'mk2/mk2-maincpu.bin',ROOT/'mk3/mk3-maincpu.bin',ROOT/'mame-mkp/unidasm.exe',
            ROOT/'PLAY_LATEST_KANO_SONYA.cmd',*(STAGE/f for f in ('midtunit_m.cpp','midtunit.cpp','midtunit.h'))]
        report=dict(passed=True,sourceOnlyAccepted=True,nativeRuntimeAccepted=False,fullPortAcceptance=False,
            proposedGuestSHA256=hashlib.sha256(guest).hexdigest().upper(),assetContract=results,
            nativeCameraMapping=camera,negativeFaultsRejected=faults,
            originalNaturalIntegrationRequirements=receipt['originalNaturalIntegrationRequirements'],
            originalRemainingWorkGroups=receipt['originalRemainingWorkGroups'],goalStatus='active',
            inputHashes={str(p.resolve()):sha(p) for p in paths},newBuilds=0,newROMCopies=0,newGraphicsCopies=0,
            newRawMedia=0,newZIPs=0,latestPlayableChanged=False,
            limitations=['Source-only typed graphics/recipes and camera wrapper; not full laser gameplay acceptance.',
                'Emitter must preserve original paired directions, own Y offsets32/64 and range10/11, not reuse Sonya anchoring.',
                'Grey emitter cadence/birth/velocity/finite cleanup, victim pose/offset, sound/priority, human/CPU activation and earned native tests remain.',
                'All original14requirements/sixremainingworkgroups and verified release remain.'])
        need(len(report['originalNaturalIntegrationRequirements'])==14 and len(report['originalRemainingWorkGroups'])==6,
             'Entire natural-game scope retained')
        with gzip.open(OUT/'executed_sources.json.gz','wt') as stream:
            json.dump(dict(actualNewInitializerHarness=harness,actualAppendedBlock=block),stream)
        need(probe.parent.resolve()==OUT.resolve(),'Exact terminal temporary source probe only');probe.unlink()
        (OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
        print(json.dumps(dict(passed=True,guest=report['proposedGuestSHA256'],greySmokeFrames=5,
            boneParticles=32,fullNativeCameraMapping=True,nativeRuntimeAccepted=False,faults=len(faults))))
    except Exception:
        (OUT/'failure.txt').write_text(traceback.format_exc())
        with gzip.open(OUT/'failed_executed_sources.json.gz','wt') as stream:json.dump(dict(actualInitializerHarness=harness),stream)
        raise


if __name__=='__main__':main()
