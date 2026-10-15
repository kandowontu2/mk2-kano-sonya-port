"""Independent all-record native opcode/ROM binding and exact repaired route."""
import collections, copy, hashlib, json, re, struct, subprocess
from pathlib import Path
import run_native_subzero_offset_regression_v4856 as capture

ROOT,need,sha=capture.ROOT,capture.need,capture.sha
OUT=ROOT/'audit_v4867_native_subzero_offset_regression_checked'

def parse(log):
    rows=[]; fields=[]
    for line in log.splitlines():
        if line.startswith('MK2_SUBZERO_CACHE_TRACE '):
            rows.append(dict(re.findall(r'(\w+)=([^\s]+)',line)))
        elif line.startswith('MK2_SUBZERO_REPAIR_FIELD '):
            fields.append(dict(re.findall(r'(\w+)=([^\s]+)',line)))
    return rows,fields

def verify(guest,payload,rows,fields,log):
    need(len(rows)==877,'Every actual native trace record, not a selected subset')
    need(hashlib.sha256(guest).hexdigest().upper()==capture.GUEST_SHA,'Entire expected qualified initialized ROM')
    def read(address,fmt='<I'):
        raw,base=(guest,0xff800000)if address>=0xff800000 else(payload,0xfe800000)
        at=(address-base)//8
        need(address%16==0 and at>=0 and at+struct.calcsize(fmt)<=len(raw),'Exact native ROM read bounds')
        return struct.unpack_from(fmt,raw,at)[0]
    for row in rows:
        need(row['writes']=='0' and row['assistance']=='none' and row['id']==row['roster']=='18',
             'Every observed instruction real Sonya and read-only context')
        address=int(row['entry'],16)
        need(int(row['pc'],16)==address+16 and row['mask']=='FFFF' and read(address,'<H')==int(row['value'],16),
             'Every actual native opcode/PC/mask bound to initialized ROM')
        for reg in ('a0','a5','a9'):
            address=int(row[reg],16)
            if 0xfe800000<=address<=0xffffffc0 and address%16==0:
                need(read(address)==int(row[reg+'_rom32'],16),'Every actual register-selected ROM peek independently bound')
    at=[r for r in rows if r['frame']=='108255' and r['action']=='0616']
    pick=lambda kind:next(r for r in at if r['kind']==kind)
    entry,root,result,cache=(pick(k)for k in('main_lookup','root_loaded','lookup_result','cache_begin'))
    for row in (entry,root,result,cache):
        need(row['actor']==row['main_owner']=='01034E90' and row['main']=='0106C620' and
             row['health']=='0,105' and row['cpu_roster']=='8' and row['human_state']=='1' and row['stage']=='7',
             'Same actual native zero-health Sonya/Sub-Zero/physical owner/0616 context as original counterexample')
    need(entry['a0']=='00000000' and entry['a1']=='FFFD4620' and entry['a9']=='00000028',
         'Actual dedicated real-ID18 victim offset returned zero')
    need(read(0xff8c23a0)==0xfffd4500 and read(0xfffd4620,'<H')==0,'Actual new native table operand and row')
    need(root['a0']=='FF020000' and result['a9']=='FF0248D0' and
         cache['a0']=='FF0320C0' and cache['a9']=='FF0248F0' and read(0xff0248d0)==0xff0320c0,
         'Actual valid own main40 and native group renderer, not FFFFFFFF or proxy art')
    body=next(r for r in rows if r['kind']=='shatter_body_lookup')
    need(body['frame']=='108311' and body['action']=='0616' and body['a9']=='00000160',
         'Actual native task advances56frames and existing body lookup still clamps to11')
    need([int(f['frame'])for f in fields]==list(range(108240,108601)),
         'Every361 consecutive real post-defect physical/native field, no omitted gaps')
    for field in fields:
        need(field['roster']=='18' and field['actor']=='01034E90' and field['state']=='1' and
             field['writes']=='0' and field['assistance']=='none','Actual real actor and valid physical state through complete regression window')
    need(any(f['victim_action']=='0616' and f['pose']=='FF0320C0' for f in fields) and
         fields[-1]['victim_action']=='050A', 'Actual victim task advances to subsequent native death task, not frozen forever')
    need('MK2_MILEENA_CAMPAIGN_OVERRUN 'not in log and 'first_bad=-1'in log and
         'global_cache_stores=0'in log and 'frame=108600 first_bad=-1'in log,
         'Actual original cache/global witness zero and actual terminal bounded stop')
    return dict(actualNativeRecordsBound=len(rows),actualPostDefectFields=len(fields),
        kindCounts=dict(collections.Counter(r['kind']for r in rows)),
        realVictimIdentity=18,actualDefectFrame=108255,actualBodyLookupFrame=108311,
        actualSubsequentDeathAction='050A',nativeVictimTaskAdvanced=True,nativeGlobalCacheOverrunRows=0,
        exactNativeDizzyGroup='FF0320C0',ownShatterBodyArtAccepted=False,fullPortAcceptance=False)

def main():
    need(not OUT.exists(),'Fresh independent runtime qualification')
    path=capture.OUT/'report.json'; prior=json.loads(path.read_text())
    need(prior['passed'] and prior['actualNativeExit']==0 and not prior['fullPortAcceptance'],
         'Actual consumed successful finite native run, not whole-port acceptance')
    folder=capture.FOLDER; log=(folder/'run.log').read_text()
    guest=capture.expected(); payload=(ROOT/capture.NAME/'roms/mk2ks/mk2ks.mdata').read_bytes()
    proof=json.loads((folder/'guest_memory_proof.json').read_text())
    need(proof['everyActualByteComparedInRAM'] and proof['sha256']==capture.GUEST_SHA,
         'Whole actual initialized guest compared in RAM at actual new executable')
    rows,fields=parse(log);positive=verify(guest,payload,rows,fields,log);faults=[]
    for label,kind,key,value in (
        ('wrong_offset','main_lookup','a0','00002B90'),
        ('wrong_identity','main_lookup','id','1'),
        ('wrong_native_health','main_lookup','health','161,105'),
        ('wrong_native_opcode','main_lookup','value','0000'),
        ('wrong_native_peek','lookup_result','a9_rom32','FFFFFFFF'),
        ('proxy_dizzy','cache_begin','a0','FF011F60'),
    ):
        altered=copy.deepcopy(rows)
        next(r for r in altered if r['frame']=='108255' and r['action']=='0616' and r['kind']==kind)[key]=value
        try:verify(guest,payload,altered,fields,log)
        except ValueError as error:faults.append(dict(kind=label,rejectedBy=str(error)))
        else:raise ValueError('Actual record fault admitted '+label)
        need(verify(guest,payload,rows,fields,log)==positive,'Whole actual positive restored')
    for label,altered in (
        ('missing_post_defect_field',fields[:80]+fields[81:]),
        ('corrupted_physical_state',[dict(f,state='1296')if f['frame']=='108256'else f for f in fields]),
        ('missing_native_completion',[dict(f,victim_action='0616')if f['frame']=='108600'else f for f in fields]),
    ):
        try:verify(guest,payload,rows,altered,log)
        except ValueError as error:faults.append(dict(kind=label,rejectedBy=str(error)))
        else:raise ValueError('Actual field fault admitted '+label)
        need(verify(guest,payload,rows,fields,log)==positive,'Whole actual positive restored')
    pins=dict(prior['inputHashes'])
    for p in(path,Path(__file__).resolve(),ROOT/'tools/run_native_subzero_offset_regression_v4852.py',
              ROOT/'art_reference_subzero_shatter_v4865/reference.json'):
        pins[str(p.resolve())]=sha(p)
    need(all(sha(p)==h for p,h in pins.items()),'All actual compiled/controller/runtime/reference evidence unchanged')
    report=dict(passed=True,**positive,actualRowAndFieldFaultsRejected=faults,actualNativeStopFrame=108600,
        initializedGuestEveryByteComparedInRAM=True,candidate=capture.NAME,physicalInputsUnchanged=True,
        nativeRuntimeOverreadRepairAcceptedForActualSonyaCase=True,trueKanoNativeFinisherStillRequiresRegression=True,
        publicPlayableChanged=False,inputHashes=pins)
    OUT.mkdir();need(subprocess.run(['compact.exe','/C','/I','/Q','/S:'+str(OUT)],capture_output=True).returncode==0,'Compressed before proof')
    (OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items()if k!='inputHashes'},indent=2),flush=True)

if __name__=='__main__':main()
