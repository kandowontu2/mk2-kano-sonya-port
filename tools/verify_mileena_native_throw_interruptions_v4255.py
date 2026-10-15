"""Source-bound native opponent captures interrupting four actual uppercut entries.

The exact original victim-task action clear is observed, not inferred from
the intended buttons. Original action507 is written in the stock ground-throw
routine. We do not assert that every observed507 value proves that entry ran;
this bounded proof binds the actual victim clear and subsequent owned state.
"""
import hashlib,json,struct,subprocess
from pathlib import Path
import verify_mileena_duck_pressure_prefix_v4249 as physical
ROOT,need,sha=physical.ROOT,physical.need,physical.sha
FOLDER=physical.FOLDER
OUT=ROOT/'audit_v4256_mileena_native_throw_interruptions_checked'
off=lambda address:(address-0xff800000)//8

def check(text,guest,native):
    for first,last in ((0xff842710,0xff8429f0),(0xff8b6e80,0xff8b6ff0)):
        need(guest[off(first):off(last)]==native[off(first):off(last)],'Entire original victim capture and throw action tail unchanged')
    need(guest[off(0xff842870):off(0xff8428a0)]==struct.pack('<3H',0x5600,0xb00d,0x01f0),
         'Original CLR A0 / MOVE A0 to opponent Main+1F0; observed post-fetch PCFF8428A0')
    need(guest[off(0xff8b6f60):off(0xff8b6fa0)]==struct.pack('<4H',0x09c0,0x0507,0xb00d,0x01f0),
         'Original ground-throw action507 and attacker Main store')
    need(guest[off(0xff8b6f30):off(0xff8b6f60)]==struct.pack('<3H',0x0d5f,0x2730,0xff84),
         'Original throw calls victim capture FF842730')
    rows=physical.parse(text)
    fields={r['frame']:r for r in rows if r['tag']=='DUCK_FIELD'}
    handlers=[r for r in rows if r['tag']=='DUCK_HANDLER']
    actions=[r for r in rows if r['tag']=='DUCK_ACTION']
    need(len(handlers)==4,'Four actual true own uppercut routine entries')
    findings=[]
    for h in handlers:
        starts=[r for r in actions if h['frame']<=r['frame']<=h['frame']+2 and r['actor']==h['actor'] and int(r['after'])==0x107]
        clears=[r for r in actions if h['frame']<=r['frame']<=h['frame']+2 and r['actor']==h['actor'] and r['pc']=='FF8428A0']
        need(len(clears)==1,'One actual original opponent victim-task clear per entry')
        r=clears[0]
        need(r['actor']==r['owner']==r['a8']==h['actor'] and r['main']==r['a13']==h['main'] and
             int(r['at'],16)==int(r['main'],16)+0x1f0 and r['mask']=='FFFF' and r['after']=='0' and
             r['id']==r['roster']=='18' and r['writes']=='0' and r['assistance']=='none',
             'Actual victim Main clear has original owner/address/mask/registers/zero, not port cleanup')
        need(len(starts)<=1 and r['before']==('263' if starts else '770'),
             'Actual uppercut action cleared after start, or preparation interrupted before action start')
        if starts:need(starts[0]['frame']==r['frame'] and starts[0]['pc']=='FF83C340',
                       'Genuine original HUMAN107 followed by native opponent capture same field')
        f=fields.get(r['frame']+1)
        need(f is not None and f['human_actor']==h['actor'] and f['human_main']==h['main'] and
             f['human_owner']==h['actor'] and f['human_id']==f['human_roster']=='18' and
             f['cpu_id']==f['cpu_roster']=='5' and f['human_action']=='0' and f['cpu_action']=='1287' and
             int(f['flags'],16)&4 and int(f['h_floor'])-int(f['h_y'])>8 and f['health']==r['health'],
             'Next genuine owned field is captured/lifted with native opponent507, before damage')
        findings.append(dict(handlerFrame=h['frame'],actualUppercutStarted=bool(starts),nativeOpponentClear=r,
                             nextActualOwnedField=f))
    need(sum(f['actualUppercutStarted'] for f in findings)==3,'Three started uppercuts interrupted, one preparation interrupted')
    return findings

def main():
    need(not OUT.exists(),'Fresh immutable source-bound proof')
    text=(FOLDER/'run.log').read_text();physical.replay(text)
    guest=physical.capture.expected();native=(ROOT/'mk2/mk2-maincpu.bin').read_bytes()
    proof=json.loads((FOLDER/'guest_memory_proof.json').read_text())
    need(proof['everyActualByteComparedInRAM'] and proof['sha256']==hashlib.sha256(guest).hexdigest().upper(),
         'Exact current native guest, every actual byte verified in RAM')
    positive=check(text,guest,native);faults=[]
    original=positive[0]['nativeOpponentClear']
    line=next(l for l in text.splitlines() if l.startswith('MK2_NAT_CAMPAIGN_DUCK_ACTION ') and
              'frame='+str(original['frame'])+' ' in l and 'pc=FF8428A0 ' in l)
    import re
    cases=[]
    for key,value in (('pc','FFF00000'),('after','263'),('owner','01000000'),('at','01000000'),('mask','00FF'),('a8','01000000'),('a13','01000000'),('before','770')):
        damaged,n=re.subn(r'\b'+key+r'=\S+',key+'='+value,line,count=1)
        need(n==1 and damaged!=line,'Non-vacuous actual native interruption fault')
        cases.append((key,text.replace(line,damaged,1),guest))
    f=positive[0]['nextActualOwnedField']
    cases.append(('opponent_not_throw_category',physical.previous.change(text,'DUCK_FIELD',f['frame'],'cpu_action',0x303),guest))
    bad=bytearray(guest);bad[off(0xff8b6f60)+2]^=1
    cases.append(('changed_original_throw_opcode',text,bytes(bad)))
    bad=bytearray(guest);bad[off(0xff842870)]^=1
    cases.append(('changed_original_victim_clear',text,bytes(bad)))
    for label,damaged,binary in cases:
        try:check(damaged,binary,native)
        except ValueError as error:faults.append(dict(fault=label,rejectedBy=str(error)))
        else:raise ValueError('Native interruption fault accepted '+label)
        need(check(text,guest,native)==positive,'Exact source/capture positive restored after each fault')
    pins=dict(json.loads((FOLDER/'input_hashes_before.json').read_text()))
    for p in (Path(__file__),Path(physical.__file__),FOLDER/'run.log',FOLDER/'result.json',FOLDER/'guest_memory_proof.json',ROOT/'mk2/mk2-maincpu.bin',ROOT/'audit_v4254_mileena_duck_pressure_activation_observed/report.json'):
        pins[str(p.resolve())]=sha(p)
    need(all(sha(p)==h for p,h in pins.items()),'All original and actual current bytes unchanged')
    report=dict(passed=True,actualNativeUppercutEntries=4,actualHuman107Starts=3,
      actualOriginalOpponentCaptures=4,actualInterruptions=positive,actualFaultsRejected=faults,
      originalGroundThrow507SetterSourceBound=True,everyObserved507ActualEntryProven=False,
      nativeOpponentCaptureNotPortCleanup=True,gameplayFixRequiredByThisEvidence=False,
      inputHashes=pins,naturalTowerClearAccepted=False,fullPortAcceptance=False,scope=__doc__)
    OUT.mkdir();need(subprocess.run(['compact.exe','/C','/I','/Q','/S:'+str(OUT)],capture_output=True).returncode==0,'Compress before writing')
    (OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k not in ('inputHashes','actualInterruptions')},indent=2),flush=True)

if __name__=='__main__':main()
