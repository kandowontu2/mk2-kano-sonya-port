"""Entire predecessor progression contract plus complete native bar refills.

Preserve the overly strict health-check failure. Every sentinel belongs to a
full original 81-store chain in each physical slot; no health rows are dropped.
"""
import gzip
import hashlib
import inspect
import json
import struct
from pathlib import Path
import qualify_native_sonya_first_four_ladder_fights as prior
import capture_native_kano_laser_audio as audio

ROOT, need, sha = prior.ROOT, prior.need, prior.sha
OUT = ROOT / 'audit_native_sonya_first_four_ladder_refills_checked'
INIT = ROOT / 'audit_native_sonya_first_four_ladder_refills_initializer'
REFILL_PROOF = None


def expected_guest():
    need(not INIT.exists(), 'One fresh small source initializer; never an emulator rebuild')
    INIT.mkdir()
    factory=inspect.getsource(audio.functions)
    need(factory.count("return scope['run']")==1, 'Whole frozen source initializer factory')
    scope=dict(vars(audio),__file__=__file__)
    exec(compile(factory.replace("return scope['run']",'return scope'),__file__+'::whole_original_initializer_factory','exec'),scope)
    old,build=scope['functions']()['expected'](INIT)
    need(hashlib.sha256(old).hexdigest().upper()=='AB1A0AEAE5BBE6457D591C8B9491E439E4DCA8F08A2E37A3710A3FA67769EF6E',
         'Entire independently reconstructed predecessor guest matches actual prior source')
    guest=bytearray(old)
    at=(0xff875bd0-0xff800000)//8
    need(all(q==255 for q in guest[0xfd7a0:0xfd7f0]), 'Actual unused repaired table storage')
    guest[0xfd7a0:0xfd7a0+68]=old[at:at+68]
    struct.pack_into('<II',guest,0xfd7a0+68,0x2303bce0,0x2303bce0)
    struct.pack_into('<I',guest,(0xff8752a0-0xff800000)//8,0xfffebd00)
    proof=json.loads((prior.FOLDER/'guest_memory_proof.json').read_text())
    need(hashlib.sha256(guest).hexdigest().upper()==proof['sha256'], 'Full independently reconstructed repaired guest equals original actual native proof')
    stock=(ROOT/'mk2/mk2-maincpu.bin').read_bytes();lo,hi=0xff9dec90,0xff9def80
    a,b=(lo-0xff800000)//8,(hi-0xff800000)//8
    need(guest[a:b]==stock[a:b], 'Whole original native FFFF/initial4/add2/final161 refill kernel byte-identical')
    constants={0xff9dec90:0x09c0,0xff9deca0:0xffff,0xff9ded80:0x188a,0xff9dee00:0x104a,0xff9dee20:0xff5e,0xff9dee50:0x00a1}
    need(all(struct.unpack_from('<H',guest,(at-0xff800000)//8)[0]==value for at,value in constants.items()),
         'Independent original sentinel/loop/final health instruction constants')
    (INIT/'report.json').write_text(json.dumps(dict(passed=True,sourceOnlyAccepted=True,
        wholeExpectedGuestSHA256=proof['sha256'],wholeOriginalNativeRefillKernelSHA256=hashlib.sha256(guest[a:b]).hexdigest().upper(),
        smallInitializerProbesCompiled=1,emulatorBuilds=0,newROMCopies=0,guestDumpFilesWritten=0,
        nativeGameplayAccepted=False,fullPortAcceptance=False),indent=2)+'\n')
    return dict(originalRefillKernelSHA256=hashlib.sha256(guest[a:b]).hexdigest().upper(),wholeGuestSHA256=proof['sha256'])


def refills(health):
    need(REFILL_PROOF is not None and len(health)==39914, 'Complete source-qualified native health-store inventory')
    sequences=[]
    for slot in ('1','2'):
        stores=[q for q in health if q['slot']==slot]
        start_pc,step_pc=('FF9DECE0','FF9DEF40') if slot=='1' else ('FF9DED10','FF9DEF70')
        reset_pc='FF825930' if slot=='1' else 'FF825960'
        address='010602F0' if slot=='1' else '01060EC0'
        starts=[(i,q) for i,q in enumerate(stores) if q['pc']==start_pc]
        need(len(starts)==223, 'All actual original inter-round and next-match refills in each slot')
        consumed=set()
        for index,start in starts:
            frame=int(start['frame']);actor,task=start['a8'],start['a13']
            need(start['before']=='161' and start['after']=='65535' and
                 all(0x01000000<=int(value,16)<0x01100000 for value in (actor,task)), 'Each original full sentinel and native task context')
            consumed.add(index);previous=65535
            for age,value in enumerate([*range(4,161,2),161]):
                need(index+age+1<len(stores), 'No omitted original native fill store')
                q=stores[index+age+1]
                need(q['pc']==step_pc and int(q['frame'])==frame+age and int(q['before'])==previous and
                     int(q['after'])==value and q['a8']==actor and q['a13']==task,
                     'Every original refill value, previous-health chain, exact field, writer and task ownership')
                consumed.add(index+age+1);previous=value
            sequences.append(dict(slot=slot,startFrame=frame,endFrame=frame+79,actualStores=81,actor=actor,main=task))
        for index,q in enumerate(stores):
            need(q['at']==address and q['pc'] in (start_pc,step_pc,reset_pc,'FF836700') and
                 (index in consumed or 0<=int(q['before'])<=161 and 0<=int(q['after'])<=161),
                 'Every observed health store uses exact native slot/writer; invalid health only in complete source-native refill')
            if q['pc']=='FF836700': need(0<=int(q['after'])<int(q['before'])<=161, 'Every collision store genuine native damage, including KO saturation')
            elif q['pc']==reset_pc: need(q['after']=='161', 'Every original full-health reset retained')
    need([q['startFrame'] for q in sequences if q['slot']=='1']==[q['startFrame'] for q in sequences if q['slot']=='2'],
         'Both complete native physical-slot refill chains paired on same round transitions')
    return dict(completeNativeRefillSequences=446,totalNativeRefillStores=446*81,completeAllHealthStoreCoverage=True,source=REFILL_PROOF)


def run():
    global REFILL_PROOF
    failure=prior.OUT/'failure.json'
    need(failure.exists() and not json.loads(failure.read_text())['passed'], 'Original strict health assumption failure retained')
    REFILL_PROOF=expected_guest()
    source=inspect.getsource(prior.fields)
    old="    for q in health:\n        need(q['slot'] in ('1','2') and 0<=int(q['before'])<=161 and 0<=int(q['after'])<=161,\n             'All observed original native health stores bounded; observers never return replacement data')"
    need(source.count(old)==1, 'Only native refill handling replaces wrong bounded-health assertion; all progression checks retained')
    source=source.replace(old,"    refills(health)")
    before="    for q in selected:\n"
    need(source.count(before)==1, 'Complete selection inventory strengthened, no original rows dropped')
    source=source.replace(before,"    need(len(selected)==208, 'Entire original physical selection inventory retained')\n"+before)
    scope=dict(vars(prior),__file__=__file__,OUT=OUT,refills=refills)
    exec(compile(source,__file__+'::whole_original_progression_with_source_native_refills','exec'),scope)
    verify=inspect.getsource(prior.run)
    before="    cases += [('ROM',0,'ids',rows['ROM'][0]['ids'].replace('17,11,7','1,11,7'))]"
    after=before+"\n    for slot in ('1','2'):\n        for pc,key,value in ((('FF9DECE0' if slot=='1' else 'FF9DED10'),'after','65534'),(('FF9DEF40' if slot=='1' else 'FF9DEF70'),'after','5')):\n            index=next(i for i,q in enumerate(rows['HEALTH']) if q['slot']==slot and q['pc']==pc)\n            cases.append(('HEALTH',index,key,value))\n    cases.append(('HEALTH',0,'pc','FF838860'))"
    need(verify.count(before)==1, 'All original progression semantic faults plus real refill faults retained')
    verify=verify.replace(before,after)
    before="    pins=dict(retained['inputHashes'])"
    after=before+"\n    for p in (Path(prior.__file__).resolve(),failure,INIT/'report.json',ROOT/'mk2/mk2-maincpu.bin',Path(audio.__file__).resolve()):\n        pins[str(p)]=sha(p)"
    need(verify.count(before)==1, 'Actual strict-check failure and new original-kernel reconstruction bound')
    verify=verify.replace(before,after)
    before="semanticFaultsRejected=faults,originalCampaignTransportPassed=False,"
    after="semanticFaultsRejected=faults,nativeHealthRefills=refills(rows['HEALTH']),smallSourceInitializerProbesCompiled=1,originalCampaignTransportPassed=False,"
    need(verify.count(before)==1, 'Complete native refill evidence added without changing acceptance scope')
    scope.update(prior=prior,failure=failure,INIT=INIT,audio=audio)
    exec(compile(verify.replace(before,after),__file__+'::whole_original_positive_and_fault_qualification','exec'),scope)
    return scope['run']()


if __name__=='__main__':
    try: run()
    except Exception as error:
        need(not OUT.exists(), 'Preserve actual qualification failure once')
        OUT.mkdir();(OUT/'failure.json').write_text(json.dumps(dict(passed=False,error=repr(error),fullPortAcceptance=False),indent=2)+'\n')
        raise
