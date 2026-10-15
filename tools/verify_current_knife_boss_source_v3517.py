"""Actual current dedicated Knife core/native boss gate/scaler, not contact."""
import json,struct,subprocess
from pathlib import Path
import verify_current_campaign_shao_knife_retreat_v3515 as native
ROOT=native.ROOT;need=native.need;sha=native.sha
CASE=ROOT/'audit_v3516_current_kano_natural_knife_retreat_campaign'
OUT=ROOT/'audit_v3518_current_knife_boss_source_checked'
def data(raw,lo,hi):return raw[(lo-0xff800000)//8:(hi-0xff800000)//8]
def u32(raw,at):return struct.unpack_from('<I',raw,(at-0xff800000)//8)[0]
def model(guest,original,donor):
    lo,hi=0xff8b6ac0,0xff8b6bb0
    need(data(guest,lo,hi)==data(original,lo,hi),'Entire original native projectile victim-ID gate unchanged')
    need(struct.unpack('<15H',data(guest,lo,hi))==(0xa3cf,0xb7ae,0x140,0xb5ce,0x1f0,0x0b4e,0xffef,
        0x09af,0x4000,0xca03,0xc080,0x5410,0xff83,0x0320,0x0960),
        'Exact original gate excludes16 and calls original collision; Shao13 not excluded by this gate only')
    geometry=struct.unpack('<4h',data(donor,0xffa5b590,0xffa5b5d0))
    need(geometry==(35,-24,51,50),'Original actual MK3 index21 Knife core, not guessed artwork bounds')
    outer=u32(guest,0xff8eba30);row=u32(guest,outer+17*32)
    need(row==0xfffe6800 and row!=u32(guest,outer+18*32),'True dedicated Kano attack row, no Sonya row substitution')
    descriptors=[]
    for index in (16,17,18,19):
        pointer=u32(guest,row+index*32);words=struct.unpack('<9H',data(guest,pointer,pointer+144))
        need(words==(geometry[0]+100,geometry[1]+72,geometry[2],geometry[3],0x1110,
            0x1606 if index==19 else 0x1605,0,0,1),
            'Entire dedicated Knife descriptor: same donor pivot/core and declared native22damage5/6block')
        descriptors.append(dict(index=index,address=pointer,words=words))
    need(u32(guest,0xff836750)==0xffff0800 and u32(guest,0xffff0800+13*32)==0xff8369f0,
       'Actual original Shao callback retained')
    need(data(guest,0xff8369f0,0xff836a40)==data(original,0xff8369f0,0xff836a40),
       'Entire original Shao damage scaler opcodes unchanged')
    for lo,hi in ((0xff835d20,0xff835d50),(0xff836040,0xff836070),(0xff8364c0,0xff836750)):
        need(data(guest,lo,hi)==data(original,lo,hi),'Original normal/block extraction and health subtraction/store unchanged')
    return dict(actualOriginalMK3KnifeCore=geometry,currentCorePivotTranslation=[100,72],dedicatedKanoRow=row,
       actualKnifeDescriptors=descriptors,sourceDerivedPossibleShaoDamage=dict(normal16=16,block5=3,block6=4),
       sourceFrontGateOnlyNotRuntimeHitOrGuardAcceptance=True,actualBossChildContactNotYetProven=True)
def main():
    need(not OUT.exists(),'Immutable source-only proof')
    guest=(CASE/'guest_maincpu.bin').read_bytes();original=(ROOT/'mk2/mk2-maincpu.bin').read_bytes();donor=(ROOT/'mk3/mk3-maincpu.bin').read_bytes()
    need(guest==native.current.expected_current()[0],'Whole current guest independently assembled, not trusting a ROM dump')
    positive=model(guest,original,donor);faults=[]
    def reject(name,changed,message):
        need(changed!=guest,'Non-vacuous actual source fault')
        try:model(changed,original,donor)
        except ValueError as error:
            need(message in str(error),'Specific intended native source invariant');faults.append(name)
        else:raise ValueError('Corrupted actual source accepted')
    changed=bytearray(guest);struct.pack_into('<H',changed,(0xff8b6b20-0xff800000)//8,0xfff2)
    reject('frontgate_excludes_Shao13',changed,'Entire original native projectile victim-ID gate')
    changed=bytearray(guest);outer=u32(guest,0xff8eba30);struct.pack_into('<I',changed,(outer+17*32-0xff800000)//8,u32(guest,outer+18*32))
    reject('Kano_substitutes_Sonya_attack_row',changed,'True dedicated Kano attack row')
    changed=bytearray(guest);pointer=positive['actualKnifeDescriptors'][-1]['address'];changed[(pointer-0xff800000)//8+11]=23
    reject('changed_actual_Knife_damage',changed,'Entire dedicated Knife descriptor')
    changed=bytearray(guest);struct.pack_into('<I',changed,(0xffff0800+13*32-0xff800000)//8,0xff8369d0)
    reject('changed_actual_Shao_callback',changed,'Actual original Shao callback')
    need(model(guest,original,donor)==positive,'Same-path original whole source positive')
    files=(CASE/'guest_maincpu.bin',ROOT/'mk2/mk2-maincpu.bin',ROOT/'mk3/mk3-maincpu.bin',
       ROOT/'diagnostic_v3172_native_morph_shadow/mkport_candidate.exe',ROOT/'diagnostic_v3172_native_morph_shadow/roms/mk2ks/mk2ks.mdata',
       ROOT/'diagnostic_v3172_native_morph_shadow/input_sources/mame-mkp/src/mame/midway/midtunit_m.cpp',Path(__file__),Path(native.__file__))
    pins={str(p.resolve()):sha(p)for p in files}
    value=dict(passed=True,actualSourceModel=positive,actualQualifiedSourceFaults=faults,samePathSourcePositiveAccepted=True,
       actualBossKnifeContactNotYetAccepted=True,gameOrCaptureChanged=False,fullPortAcceptance=False,inputHashes=pins)
    OUT.mkdir();path=OUT/'report.json';path.write_text(json.dumps(value,indent=2)+'\n');digest=sha(path)
    result=subprocess.run(['compact.exe','/C','/I','/Q',str(path)],capture_output=True,text=True)
    need(result.returncode==0 and sha(path)==digest,'Lossless compact source proof')
    print(json.dumps({k:v for k,v in value.items()if k!='inputHashes'},indent=2),flush=True)
if __name__=='__main__':main()
