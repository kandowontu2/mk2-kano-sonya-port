"""Current native Ring front gate/dedicated descriptors; no boss contact assumed."""
import json,struct,subprocess
from pathlib import Path
import verify_current_campaign_shao_guarded_highkick_v3461 as native
ROOT=native.ROOT;need=native.need;sha=native.sha
CASE=ROOT/'audit_v3462_current_sonya_natural_guarded_highkick_campaign'
OUT=ROOT/'audit_v3482_current_ring_boss_frontgate_checked'

def data(raw,lo,hi):return raw[(lo-0xff800000)//8:(hi-0xff800000)//8]
def u32(raw,at):return struct.unpack_from('<I',raw,(at-0xff800000)//8)[0]

def model(guest,original):
    lo,hi=0xff8b6ac0,0xff8b6bb0
    need(data(guest,lo,hi)==data(original,lo,hi),'Entire original projectile victim-ID front gate unchanged')
    words=struct.unpack('<15H',data(guest,lo,hi))
    need(words==(0xa3cf,0xb7ae,0x0140,0xb5ce,0x01f0,0x0b4e,0xffef,
                 0x09af,0x4000,0xca03,0xc080,0x5410,0xff83,0x0320,0x0960),
         'Exact victim pointer/ID/CMPI16/return-or-original-collision ABI')
    excluded=(~words[6])&65535
    need(excluded==16 and excluded not in (12,13),'Native front gate excludes only16, not either boss; later collision not assumed')
    outer=u32(guest,0xff8eba30);row=u32(guest,outer+18*32)
    descriptors=[]
    for index in (16,17,18,19,23):
        pointer=u32(guest,row+index*32);actual=struct.unpack('<9H',data(guest,pointer,pointer+144))
        geometry=(77,35,47,27)if index==23 else(108,35,36,11)
        need(actual==(*geometry,0x1110,0x1606 if index in (19,23)else 0x1605,0,0,1),
             'Actual dedicated Sonya Ring descriptor keeps original native22damage and5/6block')
        descriptors.append(dict(index=index,address=pointer,words=actual))
    need(u32(guest,0xff836750)==0xffff0800 and u32(guest,0xffff0800+13*32)==0xff8369f0,
         'Actual original Shao damage callback retained')
    need(data(guest,0xff8369f0,0xff836a40)==data(original,0xff8369f0,0xff836a40),
         'Original Shao damage scaler opcodes unchanged')
    return dict(excludedOriginalVictimIdentity=excluded,Kintaro12AndShao13NotExcludedByThisFrontGate=True,
        dedicatedSonyaRow=row,actualRingDescriptors=descriptors,
        sourceDerivedPossibleShaoDamage=dict(normal=(22>>1)+(22>>2),block5=(5>>1)+(5>>2),block6=(6>>1)+(6>>2)),
        laterCollisionAndGuardAndBossContactNotAssumed=True,bossRingRuntimeContactAccepted=False)

def main():
    need(not OUT.exists(),'Immutable actual front-gate proof')
    guest=(CASE/'guest_maincpu.bin').read_bytes();original=(ROOT/'mk2/mk2-maincpu.bin').read_bytes()
    need(guest==native.current.expected_current()[0],'Whole current initialized guest independently reconstructed')
    positive=model(guest,original);faults=[]
    def reject(label,changed,message):
        need(changed!=guest,'Non-vacuous actual current program fault')
        try:model(changed,original)
        except ValueError as error:
            need(message in str(error),'Specific original gate/descriptor/scaler invariant');faults.append(label)
        else:raise ValueError('Corrupted actual front-gate proof accepted')
    changed=bytearray(guest);struct.pack_into('<H',changed,(0xff8b6b20-0xff800000)//8,0xfff2)
    reject('changed_frontgate_to_exclude_Shao13',changed,'Entire original projectile victim-ID front gate')
    changed=bytearray(guest);struct.pack_into('<I',changed,(0xff8b6b70-0xff800000)//8,0xff835430)
    reject('wrong_original_collision_target',changed,'Entire original projectile victim-ID front gate')
    changed=bytearray(guest);changed[(positive['actualRingDescriptors'][-1]['address']-0xff800000)//8+11]=23
    reject('changed_actual_Ring_normal_damage',changed,'Actual dedicated Sonya Ring descriptor')
    changed=bytearray(guest);struct.pack_into('<I',changed,(0xffff0800-0xff800000)//8+13*4,0xff8369d0)
    reject('wrong_actual_Shao_damage_callback',changed,'Actual original Shao damage callback')
    need(model(guest,original)==positive,'Same-path unchanged actual source positive')
    files=(CASE/'guest_maincpu.bin',ROOT/'mk2/mk2-maincpu.bin',ROOT/'diagnostic_v3172_native_morph_shadow/mkport_candidate.exe',
        ROOT/'diagnostic_v3172_native_morph_shadow/roms/mk2ks/mk2ks.mdata',
        ROOT/'diagnostic_v3172_native_morph_shadow/input_sources/mame-mkp/src/mame/midway/midtunit_m.cpp',Path(__file__),Path(native.__file__))
    pins={str(p.resolve()):sha(p)for p in files}
    for file,digest in pins.items():need(sha(file)==digest,'Actual current source/program/playable bytes unchanged')
    value=dict(passed=True,actualSourceModel=positive,actualQualifiedSourceFaults=faults,samePathSourcePositiveAccepted=True,
        signatureMoveBossRuntimeNotYetProven=True,gameOrCaptureChanged=False,rawAudioFilesWritten=0,newBuildsOrROMCopies=0,
        fullPortAcceptance=False,inputHashes=pins)
    OUT.mkdir();path=OUT/'report.json';path.write_text(json.dumps(value,indent=2)+'\n');digest=sha(path)
    result=subprocess.run(['compact.exe','/C','/I','/Q',str(path)],capture_output=True,text=True)
    need(result.returncode==0 and sha(path)==digest,'Lossless source-gate report compression')
    print(json.dumps({k:v for k,v in value.items()if k!='inputHashes'},indent=2),flush=True)

if __name__=='__main__':main()
