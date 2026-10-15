"""Baseline and in-memory corruption tests; no evidence or ROM files changed."""
import copy
import json
from pathlib import Path
import numpy as np
from PIL import Image
import verify_native_babality_performers_v739 as own
v=own.v
ROOT=Path(__file__).resolve().parents[1]

def main():
    reference=json.loads((ROOT/'audit_v726_original_baby_reference/reference.json').read_text())
    case=ROOT/'audit_v738_kano_babality_p1'
    rows=v.records((case/'run.log').read_text(encoding='utf-8-sig'))
    def positive(data):
        v.runtime_check(data,'sonya',1,reference,winner_id=17)
        own.command_check(data,'kano',1,'positive')
    positive(rows)
    total=1
    def reject(label,function):
        nonlocal total
        try:function()
        except ValueError:total+=1
        else:raise AssertionError('Accepted corrupt case: '+label)
    def alter(tag,key,value,predicate=lambda row:True):
        changed=copy.deepcopy(rows)
        next(row for t,row in changed if t==tag and predicate(row))[key]=value
        return changed
    for label,tag,key,value,predicate in (
        ('unearned rounds','RESULT','wins','1',lambda r:True),
        ('assistance','RESULT','writes','1',lambda r:True),
        ('winner proxy selection','SELECT_ID','actual','1',lambda r:r['slot']=='1'),
        ('victim proxy selection','SELECT_ID','actual','1',lambda r:r['slot']=='2'),
        ('non-native HP store','DAMAGE','pc','FF80DE20',lambda r:True),
        ('ineligible punch','FINISH_WINDOW','hp_counters','1,0',lambda r:True),
        ('wrong baby','CONSTRUCT','frame_pointer','FFB1C960',lambda r:True),
        ('wrong victim','CONSTRUCT','victim_id','1',lambda r:True),
        ('wrong lookup word','LOOKUP','value','002C',lambda r:True),
        ('wrong native victim ID','LOOKUP','live_id','1',lambda r:True),
        ('wrong winner owner','FIELD','owner','01031D10',lambda r:r['age']=='0'and r['slot']=='1'),
        ('lost victim ID','FIELD','id','1',lambda r:r['age']=='144'and r['slot']=='2'),
        ('wrong baby floor','BABY','y','173',lambda r:r['age']=='160'),
        ('wrong palette','BABY','colors','FFFF,'+','.join(v.entries(rows,'BABY')[0]['colors'].split(',')[1:]),lambda r:r['age']=='160'),
        ('non-native retirement','RETIRE','pc','FF80DE20',lambda r:r['entry']=='01060220'),
        ('wrong command case','RESULT','case','wrong_direction',lambda r:True),
        ('wrong activation time','RESULT','action',str(int(v.entries(rows,'RESULT')[0]['action'])+1),lambda r:True)):
        changed=alter(tag,key,value,predicate)
        reject(label,lambda changed=changed:positive(changed))
    for label,tag,predicate in (
        ('missing action','ENTRY',lambda r:r['entry']=='FF87E520'),
        ('missing half retirement','RETIRE',lambda r:r['entry']=='01060230'),
        ('missing reuse','BABY_REUSED',lambda r:True),
        ('missing first forward input','INPUT',lambda r:r['button']=='Right'and int(r['frame'])==int(v.entries(rows,'RESULT')[0]['window'])+20)):
        changed=[(t,r)for t,r in rows if not(t==tag and predicate(r))]
        reject(label,lambda changed=changed:positive(changed))
    reject('watchdog reboot',lambda:positive(rows+[('BOOT',copy.deepcopy(v.entries(rows,'BOOT')[0]))]))
    old=(ROOT/'audit_v732_native_baby_kano_p1/guest_maincpu.bin').read_bytes()
    new=(case/'guest_maincpu.bin').read_bytes()
    original=(ROOT/'mk2/mk2-maincpu.bin').read_bytes()
    donor=(ROOT/'mk3/mk3-maincpu.bin').read_bytes()
    own.guest_check(old,new,original,donor);total+=1
    for label,at in (('unrelated byte',0x12345),('original native gate',own.offset(0xff87e120)),
                      ('stock performer table',0xf97a0),('Kano own table row',0xf97a0+68),
                      ('Sonya own table row',0xf97a0+72),('Kano input',0xf97f2),('Sonya input',0xf9812),
                      ('Kano wrapper',0xf9840),('Sonya wrapper',0xf9860),
                      ('LK dispatch',0xff2c0+17*4),('baby art',0xf9680)):
        changed=bytearray(new);changed[at]^=1
        reject(label,lambda changed=changed:own.guest_check(old,changed,original,donor))
    needle=np.asarray(Image.open(ROOT/'audit_v726_original_baby_reference/sonya_baby.png').convert('RGBA'))
    image=np.asarray(Image.open(case/'snap/babality_160.png').convert('RGB'))
    (x,y),_=v.image_match(image,needle);total+=1
    yy,xx=np.argwhere(needle[:,:,3]!=0)[0]
    changed=image.copy();changed[y+yy,x+xx,0]^=1
    reject('rendered pixel',lambda:v.image_match(changed,needle))
    for label,case_name,winner,command in (
        ('wrong direction','audit_v738_kano_wrong_p1','kano','wrong_direction'),
        ('punch restriction','audit_v738_sonya_punch_p2','sonya','punch_used')):
        side=1 if winner=='kano'else 2
        victim='sonya'if winner=='kano'else'kano'
        negative=v.records((ROOT/case_name/'run.log').read_text(encoding='utf-8-sig'))
        own.negative_check(negative,winner,victim,side,command);total+=1
        changed=copy.deepcopy(negative)
        next(r for t,r in changed if t=='RESULT')['action']='1'
        reject(label+' accepted action',lambda:own.negative_check(changed,winner,victim,side,command))
        changed=copy.deepcopy(negative)
        next(r for t,r in changed if t=='SELECT_ID')['actual']='1'
        reject(label+' proxy selection',lambda:own.negative_check(changed,winner,victim,side,command))
    print(json.dumps({'tests_passed':total,'mutations_are_in_memory_only':True,'fullPortAcceptance':False},indent=2))

if __name__=='__main__':main()
