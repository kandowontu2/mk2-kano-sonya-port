"""Actual native counterexample and table-only repair qualified in RAM.

Not a compiled fix, art acceptance, natural campaign clear or release gate.
"""
import copy,hashlib,json,re,struct,subprocess
from pathlib import Path
import inspect_sonya_subzero_cache_trace_v4837 as probe
ROOT=probe.ROOT
OUT=ROOT/'audit_v4839_native_subzero_victim_offset_qualified'
DEST=0xfa8a0
def need(condition,message):
    if not condition:raise ValueError(message)
def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest().upper()
def off(address):return (address-0xff800000)//8

def qualify(guest,payload,stock,rows):
    u16=lambda address:struct.unpack_from('<H',guest,off(address))[0]
    u32=lambda address:struct.unpack_from('<I',guest,off(address))[0]
    need(guest[off(0xff8c2320):off(0xff8c2470)]==stock[off(0xff8c2320):off(0xff8c2470)],'Whole original616 victim offset/main40/scale/add/render instructions')
    need(guest[off(0xff82edc0):off(0xff82ee20)]==stock[off(0xff82edc0):off(0xff82ee20)],'Whole original real-ID word lookup helper')
    need(u16(0xff8c2320)==0x09c1 and u16(0xff8c2330)==0x616 and u16(0xff8c2390)==0x09e0
        and u32(0xff8c23a0)==0xff8c27d0 and u32(0xff8c23d0)==0xff82edc0
        and u16(0xff8c23f0)==0x4c07 and u16(0xff8c2410)==40 and u32(0xff8c2430)==0xff906090
        and u16(0xff8c2450)==0x24a7 and u16(0xff8c2460)==0x40e9 and u32(0xff8c2480)==0xff83bb00,
        'Source-bound native offset saved inA7, ownmain40, offset<<5 and actual renderer')
    need(u16(0xff82ede0)==0x2481 and u16(0xff82ee00)==0x8420,'Actual ID<<4 word read, not a pointer or synthetic callback')
    selected=[r for r in rows if r['frame']=='108255']
    get=lambda kind:next(r for r in selected if r['kind']==kind)
    entry,root,cell,result,bad,write=(get(k)for k in ('main_lookup','root_loaded','lookup_cell','lookup_result','cache_begin','first_global_write'))
    for row in (entry,root,cell,result,bad,write):
        need(row['actor']==row['main_owner']=='01034E90'and row['main']=='0106C620'and row['id']==row['roster']=='18'
            and row['health']=='0,105'and row['cpu_roster']=='8'and row['human_state']=='1'and row['action']=='0616'
            and row['writes']=='0'and row['assistance']=='none','Actual original zero-health trueSonya616 victim/main/physical/cpu context')
    actual_offset=u16(0xff8c27d0+18*16)
    need(actual_offset==0x2b90 and entry['a0']=='00002B90'and entry['a1']=='FF8C28F0'and entry['a9']=='00000028',
        'Actual short-table overread returned adjacent shatter-table lowword2B90, not an invalid main root')
    table=u32(0xff9060a0);main=u32(table+18*32);stream=struct.unpack_from('<I',payload,(main-0xfe800000)//8+40*4)[0]
    need(table==0xfffe4000 and main==0xff020000 and root['a0']=='FF020000'and cell['a9']=='FF020500'
        and result['a9']=='FF0248D0'and stream==0xff0248d0,'Actual original ownmain40 lookup itself is valid')
    wrong_cursor=stream+(actual_offset<<5)
    need(wrong_cursor==0xff07bad0 and payload[(wrong_cursor-0xfe800000)//8:(wrong_cursor-0xfe800000)//8+4]==b'\xff'*4
        and bad['a0']=='FFFFFFFF'and int(bad['a9'],16)==wrong_cursor+32 and write['entry']=='01060020'
        and write['pc']=='FF838860','Exact overread→offset advance→unpopulated word→FFFFFFFF group→actual global store')
    need(guest[DEST:DEST+64]==b'\xff'*64,'Complete independent program allocation unused')
    repaired=bytearray(guest)
    repaired[DEST:DEST+34]=guest[off(0xff8c27d0):off(0xff8c27d0)+34]
    struct.pack_into('<2H',repaired,DEST+34,0,0)
    struct.pack_into('<I',repaired,off(0xff8c23a0),0xff800000+DEST*8)
    changed={n for n,(before,after)in enumerate(zip(guest,repaired))if before!=after}
    need(changed and changed<=set(range(DEST,DEST+38))|set(range(off(0xff8c23a0),off(0xff8c23a0)+4)),'Only initialized table/operand bytes change; no runtime state/ID/cache repair')
    need(repaired[DEST:DEST+34]==guest[off(0xff8c27d0):off(0xff8c27d0)+34],'All seventeen existing ID-indexed words unchanged')
    own=[]
    for identity in (17,18):
        row_root=u32(table+identity*32);at=(row_root-0xfe800000)//8
        sequence=struct.unpack_from('<I',payload,at+40*4)[0]
        first=struct.unpack_from('<I',payload,(sequence-0xfe800000)//8)[0]
        need(first not in (0,1,0xffffffff)and 0xfe800000<=first<0xff800000,'Each true character keeps its own valid native dizzy group')
        count=0;group=(first-0xfe800000)//8
        while struct.unpack_from('<I',payload,group+count*4)[0]:
            descriptor=struct.unpack_from('<I',payload,group+count*4)[0]
            need(0xfe800000<=descriptor<0xff800000 and count<16,'Own actual zero-terminated composite descriptor extent')
            count+=1
        own.append(dict(identity=identity,root=f'{row_root:08X}',sequence=f'{sequence:08X}',firstGroup=f'{first:08X}',components=count,addedOffset=0))
    return dict(actualNativeRootCause='Original616 victim offset lookup overreads ID18 into adjacent shatter pointer table; 2B90<<5 advances valid ownmain40 cursor into unused payload.',
        firstBadFrame=108255,validOwnMain40=f'{stream:08X}',actualBadOffset=actual_offset,actualBadCursor=f'{wrong_cursor:08X}',
        sourceOnlyRepairQualified=True,expectedRepairedGuestSHA256=hashlib.sha256(repaired).hexdigest().upper(),
        nativeOffsetOperand='FF8C23A0',originalOffsetTable='FF8C27D0',newOffsetTable=f'{0xff800000+DEST*8:08X}',
        exactChangedGuestBytes=len(changed),ownTrueIDRows=own,allExistingSeventeenWordsPreserved=True,
        nativeInstructionsIdentityAndCopyLoopUnchanged=True,compiledFixAccepted=False,nativeRepairRuntimeAccepted=False,
        remainingFinalShatterBodyTableCappedToJaxNeedsOwnArt=True,fullPortAcceptance=False)

def main():
    need(not OUT.exists(),'Fresh immutable native cause qualification')
    guest,payload,stock,read=probe.sources();folder=ROOT/'audit_v4835_sonya_subzero_cache_trace_ram'
    meta=json.loads((folder/'result.json').read_text());proof=json.loads((folder/'guest_memory_proof.json').read_text())
    need(meta['exit_code']==0 and proof['everyActualByteComparedInRAM']and proof['sha256']==hashlib.sha256(guest).hexdigest().upper(),'Actual native terminal and entire byte-exact RAM guest')
    inspection=probe.inspect();need(inspection['traceRows']==915 and inspection['nativeRAMGuestCompared'],'Every915actual instruction and ROM-peek record independently bound')
    log=(folder/'run.log').read_text();rows=[dict(re.findall(r'(\w+)=([^\s]+)',line))for line in log.splitlines()if line.startswith('MK2_SUBZERO_CACHE_TRACE ')]
    positive=qualify(guest,payload,stock,rows);faults=[]
    for label,address in (('wrong_table_operand',0xff8c23a0),('wrong_id_stride',0xff82ede0),('wrong_word_read',0xff82ee00),
        ('wrong_advance_scale',0xff8c2450),('wrong_animation_id',0xff8c2410)):
        altered=bytearray(guest);altered[off(address)]^=1
        try:qualify(altered,payload,stock,rows)
        except ValueError as error:faults.append(dict(kind=label,rejectedBy=str(error)))
        else:raise ValueError('Native source fault admitted '+label)
    for label,key,value in (('wrong_actual_offset','a0','00000000'),('wrong_physical_identity','id','1'),('invented_health','health','161,105')):
        altered=copy.deepcopy(rows);next(r for r in altered if r['frame']=='108255'and r['kind']=='main_lookup')[key]=value
        try:qualify(guest,payload,stock,altered)
        except ValueError as error:faults.append(dict(kind=label,rejectedBy=str(error)))
        else:raise ValueError('Actual native witness fault admitted '+label)
    need(qualify(guest,payload,stock,rows)==positive,'Full actual positive restored after eight actual code/context faults')
    pins=dict(meta['input_hashes'])
    for p in (Path(__file__).resolve(),Path(probe.__file__).resolve(),ROOT/'tools/inspect_sonya_subzero_cache_trace_v4830.py',
        ROOT/'audit_v4834_sonya_subzero_cache_trace_source_checked/report.json',ROOT/'audit_v4836_sonya_subzero_cache_trace_observed/report.json',
        *(p for p in folder.rglob('*')if p.is_file())):pins[str(p.resolve())]=sha(p)
    need(all(sha(p)==h for p,h in pins.items()),'Every actual original current/public/controller/source/runtime evidence unchanged')
    report=dict(passed=True,**positive,inputHashes=pins,actualNativeTraceRows=915,actualFaultsRejected=faults,
        actualStopFrame=108257,diagnosticOnly=True,newBuilds=0,rawMediaGuestOrROMFilesWritten=0)
    OUT.mkdir();need(subprocess.run(['compact.exe','/C','/I','/Q','/S:'+str(OUT)],capture_output=True).returncode==0,'Compressed before writes')
    (OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items()if k!='inputHashes'},indent=2),flush=True)
if __name__=='__main__':main()
