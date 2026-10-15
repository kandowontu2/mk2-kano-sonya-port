"""Verify the observed Pit lookup defect, not a fix or campaign acceptance."""
import hashlib,json,re,struct,sys
from pathlib import Path

ROOT=Path(__file__).resolve().parent.parent
EXE='C0778D6A8199D9582A50A0B1AD7DBE1B33016D2E388035914BA3191266DC656B'
SOURCE='217D08ED8CB6F4D03D1A6F24C3E43555204B9FA7B52B63C43FE8E5421157ED35'
ORIGINAL='45B3285496DB555EFAF4A3608A4F59845DD47A82E4A0593607E0592F47B36F23'
TABLE=0xff85e6b0

def rows(log,tag):
    return [dict(re.findall(r'(\w+)=([^\s]+)',line))for line in log.splitlines()
            if line.startswith('MK2_NAT_CAMPAIGN_'+tag+' ')]

def h(row,key):return int(row[key],16)

def contract(log):
    errors=[]
    def require(ok,message):
        if not ok:errors.append(message)
    boots,results=rows(log,'BOOT'),rows(log,'RESULT')
    require(len(boots)==len(results)==1,'Exactly one cold boot and terminal result')
    require(not re.search(r'\[LUA ERROR\]|fatal error|access violation',log,re.I),'No observer/runtime error')
    allrows=[dict(re.findall(r'(\w+)=([^\s]+)',line))for line in log.splitlines()
             if line.startswith('MK2_NAT_CAMPAIGN_')and 'frame='in line]
    require(all(r.get('writes')=='0'and r.get('assistance')=='none'for r in allrows),'Input-only observation declared consistently')
    fields=[int(r['frame'])for r in allrows]
    require(fields==sorted(fields),'Monotonic observer fields; no duplicate registered campaign')
    operands=rows(log,'PIT_OPERANDS');table=rows(log,'PIT_ROM')
    require(len(operands)==1 and h(operands[0],'first')==h(operands[0],'second')==TABLE,'Both original Pit lookup operands observed')
    require(len(table)==19 and [int(r['id'])for r in table]==list(range(19)),'Runtime table rows 0..18 observed')
    require(len(table)==19 and h(table[17],'value')==1 and h(table[18],'value')==0xff85e830,'Missing Kano stream and Sonya stock alias observed')
    lookups=rows(log,'PIT_LOOKUP')
    require(len(lookups)==1,'Exactly one reproduced bad native lookup')
    if len(lookups)==1:
        r=lookups[0]
        require(int(r['frame'])==16784 and h(r,'at')==TABLE+17*32 and h(r,'value')==1 and
            h(r,'pc')==0xff83b850 and h(r,'a1')==TABLE and int(r['id'])==int(r['table_slot'])==17 and
            int(r['mode'])==9,'True-ID Kano native slot17 lookup returns token1 as its stream')
    draws=rows(log,'DRAW')
    scene=[r for r in draws if int(r['frame'])==16785 and h(r,'entry')==0xff85c420]
    require(len(scene)==1 and h(scene[0],'a9')==1 and int(scene[0]['actor_id'])==17,'Scene consumes the invalid stream1 on the next field')
    render=[r for r in draws if int(r['frame'])==16785 and h(r,'entry')==0xff838790]
    require(len(render)==1 and h(render[0],'a0')==0x9f9f9f9f and h(render[0],'a9')==0x21 and
        h(render[0],'cache')==0x0105ed30,'Invalid low-memory stream yields unmapped sprite group')
    if len(lookups)==len(scene)==len(render)==1:
        require(all(h(r,'a8')==0x0102d6f0 and h(r,'a13')==0x0106aa60 for r in (lookups[0],scene[0],render[0])),
            'Lookup, scene consumption and draw have the same cinematic drawable/task')
    components=rows(log,'COMPONENT')
    overrun=[r for r in components if int(r['frame'])==16785 and h(r,'source')>=0x9f9f9f9f]
    require(len(overrun)>=2,'Actual malformed component reads observed')
    if overrun:
        require(h(overrun[0],'source')==0x9f9f9f9f and h(overrun[0],'dst')==0x0105ed30 and
            all(h(r,'value')==0xffffffff for r in overrun),'Unmapped source values enter native sprite cache')
        require(all(h(b,'source')-h(a,'source')==32 and h(b,'dst')-h(a,'dst')==112
            for a,b in zip(overrun,overrun[1:])),'Native source/cache overrun strides are continuous')
    transitions=rows(log,'TRANSITION');health=rows(log,'HEALTH')
    require(any(int(r['frame'])==16666 and h(r,'at')==0x010601d0 and r['before']=='2'and
        r['after']=='9'and h(r,'pc')==0xff8eb4e0 and h(r,'a8')==0x01034020 for r in transitions),
        'Actual falling Kano enters native Pit cinematic mode9')
    for address in (0x010602f0,0x01060ec0):
        require(any(int(r['frame'])==16785 and h(r,'at')==address and r['after']=='32382'and
            h(r,'pc')==0xff838a10 and h(r,'a8')==0x0102d6f0 for r in health),
            f'Native malformed sprite store reaches physical health {address:08X}')
    require(any(int(r['frame'])==16955 and h(r,'entry')==0xffffffe0 and
        r['mode']==r['stage']=='32382'for r in rows(log,'BOUNDARY')),'Actual reset vector fetched after corruption')
    require(len(results)==1 and results[0]['reset']=='16955'and results[0]['selections']=='7'and
        results[0]['losses']=='6'and results[0]['ending']=='-1','Terminal result retains genuine continues and reset, not clear')
    return errors

def verify(folder):
    errors=[];inputs={}
    metadata=json.loads((folder/'result.json').read_text(encoding='utf-8-sig'))
    for filename,expected in metadata['input_hashes'].items():
        file=Path(filename);actual=hashlib.sha256(file.read_bytes()).hexdigest().upper()
        if actual!=expected:errors.append('Input changed: '+filename)
        inputs[filename]=actual
    if metadata['exit_code']!=0 or metadata['executable_sha256']!=EXE or metadata['assistance']!='none' or metadata['unassisted_clear_proven']:
        errors.append('Matched diagnostic build/input-only terminal metadata')
    if hashlib.sha256((ROOT/'mame-mkp/src/mame/midway/midtunit_m.cpp').read_bytes()).hexdigest().upper()!=SOURCE:
        errors.append('Unchanged v545 gameplay source required')
    original=(ROOT/'mk2/mk2-maincpu.bin').read_bytes()
    if hashlib.sha256(original).hexdigest().upper()!=ORIGINAL:errors.append('Original native program changed')
    word=lambda a:struct.unpack_from('<H',original,(a-0xff800000)//8)[0]
    long=lambda a:struct.unpack_from('<I',original,(a-0xff800000)//8)[0]
    expected={0xff83b7f0:0x4c01,0xff83b800:0xb500,0xff83b810:0x1f0,
              0xff83b820:0x24a0,0xff83b830:0x4020,0xff83b840:0x8600,
              0xff8387f0:0x9605,0xff838a10:0x9061,0xff85c320:0x09e0,0xff85c490:0x09e0}
    if any(word(a)!=v for a,v in expected.items()):errors.append('Original true-ID lookup and sprite-copy instruction contract')
    if long(0xff85c330)!=TABLE or long(0xff85c4a0)!=TABLE:errors.append('Original scene lookup operands')
    if long(TABLE+17*32)!=1 or long(TABLE+18*32)!=long(TABLE):errors.append('Original out-of-table rows')
    script=folder/'input_sources/mk2ks_natural_campaign_probe_v6.lua'
    if re.search(r':(?:write_\w+|soft_reset|load)\s*\(',script.read_text()):errors.append('Observer must not write/reset/load the guest')
    log=(folder/'run.log').read_text(encoding='utf-8-sig');errors+=contract(log)
    runtime=rows(log,'PIT_ROM')
    if len(runtime)==19 and any(h(r,'value')!=long(TABLE+i*32)for i,r in enumerate(runtime)):
        errors.append('Runtime table differs from original native bytes')
    for file in folder.rglob('*'):
        if file.is_file():inputs[str(file)]=hashlib.sha256(file.read_bytes()).hexdigest().upper()
    return dict(passed=not errors,defectEstablished=not errors,errors=errors,fullPortAcceptance=False,
        fixed=False,candidate='diagnostic_v545_native_roll_edge_clearance',
        scope='one_actual_Kano_P1_CPU_Pit_fatality_missing_lookup_and_native_cache_memory_overrun_not_a_fix_or_full_campaign',
        sonyaScope='runtime_unextended_slot18_aliases_stock_Kung_Lao_stream_not_observed_Sonya_Pit_execution',inputHashes=inputs)

if __name__=='__main__':
    proof=verify(ROOT/'audit_v592_pit_actual_lookup_kano_p1')
    print(json.dumps(proof,indent=2));sys.exit(0 if proof['passed']else 1)
