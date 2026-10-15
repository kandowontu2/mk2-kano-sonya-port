"""Native high-kick/Shao damage ABI, actual ordered stores, qualified faults."""
import json
import struct
import subprocess
from collections import Counter
from pathlib import Path
import verify_current_campaign_shao_highkick_v3440 as native
import diagnose_current_boss_damage_action_order_v2385 as ordered

ROOT=native.ROOT;need=native.need;sha=native.sha
CAPTURE=ROOT/'audit_v3426_current_sonya_natural_defensive_leg_highkick_campaign'
PROOF=ROOT/'audit_v3448_current_sonya_highkick_campaign_outcomes/report.json'
OUT=ROOT/'audit_v3452_current_highkick_damage_model_checked'

def data(raw,lo,hi):return raw[(lo-0xff800000)//8:(hi-0xff800000)//8]
def u32(raw,at):return struct.unpack_from('<I',raw,(at-0xff800000)//8)[0]

def model(guest,original,hits,doses):
    for lo,hi in ((0xff870c00,0xff870ce0),(0xff837570,0xff837770),
                  (0xff835d20,0xff835d50),(0xff836040,0xff836070),
                  (0xff8369f0,0xff836a40)):
        need(data(guest,lo,hi)==data(original,lo,hi),'Entire original high-kick selector/strike/damage path unchanged')
    need(struct.unpack('<3H',data(guest,0xff835d20,0xff835d50))==(0x4cea,0x260a,0x2d0a),
         'Normal damage extracts descriptor word5 high byte')
    need(struct.unpack('<3H',data(guest,0xff836040,0xff836070))==(0x4cea,0x270a,0x2d0a),
         'Block damage extracts descriptor word5 low byte')
    need(struct.unpack('<5H',data(guest,0xff8369f0,0xff836a40))==(0x4d42,0x2fea,0x2fc2,0x404a,0x0960),
         'Exact original Shao reduction: (damage>>1)+(damage>>2)')
    original_table=u32(original,0xff836750);table=u32(guest,0xff836750)
    need(original_table==0xff8367b0 and table==0xffff0800,
         'Exact source-assembled nineteen-ID damage-table relocation')
    need(data(guest,table,table+19*32)==data(original,original_table,original_table+17*32)+bytes(8),
         'All original seventeen damage callbacks retained; two true added IDs have independent zero callbacks')
    need(u32(guest,table+13*32)==0xff8369f0,'Actual original Shao callback, no difficulty or power replacement')
    expected=bytearray(data(original,0xff8364c0,0xff8367a0))
    struct.pack_into('<I',expected,(0xff836750-0xff8364c0)//8,table)
    need(data(guest,0xff8364c0,0xff8367a0)==expected,
         'Every original damage/health/dispatch opcode retained except exact four-byte table operand')
    outer=u32(guest,0xff8eba30)
    need(data(guest,outer,outer+17*32)==data(original,0xff8eba90,0xff8eba90+17*32),
         'All original seventeen attack rows preserved')
    donor=u32(original,u32(original,0xff8eba90+32)+6*32)
    descriptors=[]
    for identity in (17,18):
        row=u32(guest,outer+identity*32);descriptor=u32(guest,row+6*32)
        need(row!=u32(original,0xff8eba90+32)and descriptor!=donor,
             'Dedicated true-ID row/descriptor, not a character proxy')
        need(data(guest,descriptor,descriptor+144)==data(original,donor,donor+144),
             'Whole original high-kick descriptor retained on actual own row')
        words=struct.unpack('<9H',data(guest,descriptor,descriptor+144))
        need(words==(85,70,65,30,0x0606,0x0c03,0,0,1),'Exact native high-kick geometry/reaction/damage descriptor')
        descriptors.append(dict(identity=identity,row=row,descriptor=descriptor,words=words))
    need(descriptors[0]['row']!=descriptors[1]['row']and descriptors[0]['descriptor']!=descriptors[1]['descriptor'],
         'Independent Kano/Sonya attack storage')
    raw_normal=descriptors[0]['words'][5]>>8;raw_block=descriptors[0]['words'][5]&255
    scale=lambda v:(v>>1)+(v>>2)
    normal,blocked=scale(raw_normal),scale(raw_block)
    counts=Counter()
    need(len(hits)==94 and all(h['actualDamageWriterAction']==0x113 for h in hits),'All94actual ordered native0113 damage stores')
    for hit in hits:
        dose=doses[hit['event']]
        need(dose['before']>=raw_normal and hit['damage']==dose['before']-dose['after'] and
             dose['pc']==0xff836700 and dose['slot']==2,
             'Original real Shao health store, no remaining-health clamp explanation')
        need(hit['damage']in(normal,blocked),'Actual damage must match one of the exact native branches')
        counts[hit['damage']]+=1
    need(dict(counts)=={normal:92,blocked:2},'Exact94store native damage distribution')
    return dict(rawNormalDamage=raw_normal,rawBlockDamage=raw_block,ShaoNormalDamage=normal,
        ShaoBlockDamage=blocked,actualDamageHistogram=dict(counts),descriptors=descriptors,
        inferredNormalBranchCompatibleStores=92,inferredBlockBranchCompatibleStores=2,
        branchClassificationIsSourceDerivedInferenceNotDirectBranchTrace=True,
        totalDamage=sum(h['damage']for h in hits))

def run():
    need(not OUT.exists(),'Immutable native damage proof')
    proof=json.loads(PROOF.read_text());need(proof['passed']and not proof['fullPortAcceptance'],'Accepted complete ordered campaign outcomes')
    logpath=CAPTURE/'run.log';need(sha(logpath)==proof['inputHashes'][str(logpath)],'Unchanged actual campaign log')
    guest=(CAPTURE/'guest_maincpu.bin').read_bytes();original=(ROOT/'mk2/mk2-maincpu.bin').read_bytes()
    need(guest==native.current.expected_current()[0],'Whole current guest independently source assembled')
    rows=native.old.parse(logpath.read_text(encoding='utf-8-sig'),1,'sonya')
    hits=[row for row in ordered.classify(rows,1)if row['stage']==16]
    doses={row['event']:row for row in rows if row['tag']=='HEALTH'}
    positive=model(guest,original,hits,doses)
    faults=[]
    def reject(label,g,h,expected_error):
        try:model(g,original,h,doses)
        except ValueError as error:
            need(expected_error in str(error),'Qualified intended damage invariant, not unrelated exception');faults.append(label)
        else:raise ValueError('Invalid native damage evidence accepted')
    changed=bytearray(guest);at=(positive['descriptors'][0]['descriptor']-0xff800000)//8+10
    changed[at+1]=13
    reject('changed_actual_Kano_normal_damage',changed,hits,'Whole original high-kick descriptor')
    changed=bytearray(guest);at=(0xff836a10-0xff800000)//8;changed[at]^=1
    reject('changed_original_Shao_shift',changed,hits,'Entire original high-kick selector/strike/damage path')
    changed=bytearray(guest);struct.pack_into('<I',changed,(0xffff0800-0xff800000)//8+13*4,0xff8369d0)
    reject('wrong_actual_Shao_callback',changed,hits,'All original seventeen damage callbacks')
    changed=[dict(h)for h in hits];changed[0]['damage']=2
    reject('forged_actual_health_delta',guest,changed,'Original real Shao health store')
    need(model(guest,original,hits,doses)==positive,'Same-path unchanged positive control')
    pins={str(path.resolve()):sha(path)for path in (PROOF,logpath,CAPTURE/'guest_maincpu.bin',
        ROOT/'mk2/mk2-maincpu.bin',ROOT/'diagnostic_v3172_native_morph_shadow/mkport_candidate.exe',
        ROOT/'diagnostic_v3172_native_morph_shadow/roms/mk2ks/mk2ks.mdata',
        ROOT/'diagnostic_v3172_native_morph_shadow/input_sources/mame-mkp/src/mame/midway/midtunit_m.cpp',
        Path(__file__),Path(native.__file__),Path(ordered.__file__))}
    for file,digest in pins.items():need(sha(file)==digest,'Actual model/source/capture bytes unchanged')
    return dict(passed=True,candidate='diagnostic_v3172_native_morph_shadow',actualCurrentDamageModel=positive,
        specificActualCounterexamples=faults,samePathPositiveControlAccepted=True,
        gameOrCaptureChanged=False,rawAudioFilesWritten=0,newBuildsOrROMCopies=0,
        fullPortAcceptance=False,inputHashes=pins,
        conclusion='Observed9/1damage exactly matches native high-kick12/3 and original Shao shift/add callback:92normal-compatible stores and2block-compatible stores total830. Classification is source-derived inference, not captured branch execution. Both characters have dedicated true-ID original descriptors. This does not prove a Shao clear, general controller improvement or a character defect.')

if __name__=='__main__':
    value=run();OUT.mkdir();path=OUT/'report.json';path.write_text(json.dumps(value,indent=2)+'\n');digest=sha(path)
    result=subprocess.run(['compact.exe','/C','/I','/Q',str(path)],capture_output=True,text=True)
    need(result.returncode==0 and sha(path)==digest,'Lossless model report compression')
    print(json.dumps({k:v for k,v in value.items()if k!='inputHashes'},indent=2),flush=True)
