"""Real complete Jax input replay and owned native ground/jump callbacks.

All original4194 state/ownership/reset/button-edge/leg/action checks retained.
Adds independently replayed pound timer and jump edges, and exact guest opcode/
register/status checks for actual callbacks. Prefix only; no campaign clear.
"""
import hashlib,inspect,json,re,struct,subprocess
from pathlib import Path
import verify_mirror_guard_zoning_prefix_v4194 as original
import qualify_sonya_p1_jax_jump_guard_source_v4809 as boundary
ROOT,need,sha=boundary.ROOT,boundary.need,boundary.sha
FOLDER=ROOT/'audit_v4811_sonya_p1_jax_jump_guard_ram'
OUT=ROOT/'audit_v4814_sonya_p1_jax_jump_guard_prefix_checked'

def make_replay():
    body=inspect.getsource(original.replay)
    changes=[("'GUARD_DECISION'","'JAX_DECISION'"),("'GUARD_FIELD'","'JAX_FIELD'"),("'GUARD_ACTION'","'JAX_ACTION'"),
      ("f['human_slot'] == '2'","f['human_slot'] == '1'"),("r['slot'] == '2'","r['slot'] == '1'"),
      ('Actual true Sonya P2 identity','Actual true Sonya P1 identity'),
      ("f['cpu_id'] == f['cpu_roster'] == '18'","f['cpu_id'] == f['cpu_roster'] == '11'"),
      ("r['tag'] == 'SPECIAL' and r['move'] == 'leg'","r['tag'] == 'SPECIAL' and r['move'] == 'leg' and r['frame'] in decisions"),
      ('    reasons = collections.Counter()','    pound, jump = -1000, -1000\n    reasons = collections.Counter()'),
      ('            leg, last_leg, upper, guard, move = None, -1000, -1000, -1000, None',
       '            leg, last_leg, upper, guard, move = None, -1000, -1000, -1000, None\n            pound, jump = -1000, -1000'),
      ('        expected = []\n        if leg is not None and frame - leg < 12:',
       """        expected = []
        if ca == 0x137:pound = frame + 40
        if frame < pound and height <= 8:
            leg = None
            if frame-jump >= 4:jump=frame
            if frame-jump < 3:
                reason='pound_jump_retry_edge';expected=['Up','Left' if hx<cx else 'Right']
            else:reason='pound_jump_retry_release'
        elif leg is not None and frame - leg < 12:"""),
      ("        need(decisions[frame]['reason'] == reason, 'Independently replayed physical decision at ' + str(frame))",
       "        need(int(decisions[frame]['pound_until'])==pound and int(decisions[frame]['jump_start'])==jump,'Actual whole physical pound/jump persistent state replayed')\n        need(decisions[frame]['reason'] == reason, 'Independently replayed physical decision at ' + str(frame))")]
    for before,after in changes:
        need(body.count(before)==1,'Exact complete original physical replay adaptation '+before)
        body=body.replace(before,after,1)
    need(body.count("f['cpu_roster'] == '18'")==4,'Exactly four readiness/move/approach CPU predicates')
    body=body.replace("f['cpu_roster'] == '18'","f['cpu_roster'] == '11'")
    scope=dict(vars(original),__file__=__file__)
    exec(compile(body,__file__+'::whole4194_plus_physical_pound_jump_edges','exec'),scope)
    return scope['replay']

def callbacks(text,guest):
    rows=[]
    expected=dict(ground_entry=0xff86dd90,ground_result=0xff86e020,ground_damage=0xff86e070,human_jump=0xff831360)
    for line in text.splitlines():
        if not line.startswith('MK2_JAX_GROUND_NATIVE '):continue
        r=dict(re.findall(r'(\w+)=([^\s]+)',line));rows.append(r)
        address=expected[r['kind']]
        need(r['human_slot']=='1' and r['fighter']=='sonya' and r['writes']=='0' and r['assistance']=='none'
             and r['h_id']=='18' and r['c_id']=='11','True native physical P1 Sonya/Jax callback scope')
        for who in ('h','c'):
            need(r[who+'_actor']==r[who+'_owner'] and 0x01000000<=int(r[who+'_actor'],16)<0x01100000
                 and 0x01000000<=int(r[who+'_main'],16)<0x01100000,'Actual callback actor/Main/owner')
        who='h' if r['kind']=='human_jump' else 'c'
        need(r['a8']==r[who+'_actor'] and r['a13']==r[who+'_main'],'Actual original instruction belongs to physical actor')
        need(int(r['entry'],16)==int(r['at'],16)==address and int(r['pc'],16)==address+16 and r['mask']=='FFFF'
             and int(r['opcode'],16)==struct.unpack_from('<H',guest,(address-0xff800000)//8)[0],
             'Exact actual initialized guest instruction fetch/address/PC/opcode/mask')
        need(int(r['carry'])==(int(r['status'],16)>>30)&1 and all(0<int(hp)<=161 for hp in r['health'].split(',')),
             'Actual native Carry/status/live health')
        if r['kind']=='ground_result':
            moving=int(r['h_vy'],16)!=0 or int(r['h_y'])!=int(r['h_floor'])
            need(int(r['carry'])==int(moving),'Exact original real target vertical velocity/Y/Main-floor ground-helper Carry')
    need(any(r['kind']=='ground_result' for r in rows) and any(r['kind']=='human_jump' for r in rows),
         'Actual ground helper and owned human jump must execute; never planned inputs or fixtures')
    return dict(actualNativeCallbacks=len(rows),actualNativeGroundEntries=sum(r['kind']=='ground_entry' for r in rows),
      actualNativeGroundResults=sum(r['kind']=='ground_result' for r in rows),
      actualNativeGroundResultsSkippingMovingOrAirborneTarget=sum(r['kind']=='ground_result' and r['carry']=='1' for r in rows),
      actualNativeGroundResultsAdmittingGroundedTarget=sum(r['kind']=='ground_result' and r['carry']=='0' for r in rows),
      actualNativeGroundDamageInstructionsReached=sum(r['kind']=='ground_damage' for r in rows),
      actualNativeOwnedHumanJumpEntries=sum(r['kind']=='human_jump' for r in rows),examples=rows[:12])

def run():
    need(not OUT.exists(),'Fresh actual Jax prefix proof')
    boundary.source_boundary();preflight=json.loads((boundary.OUT/'report.json').read_text())
    guest=boundary.capture.previous.expected();proof=json.loads((FOLDER/'guest_memory_proof.json').read_text())
    need(proof['everyActualByteComparedInRAM'] and proof['sha256']==hashlib.sha256(guest).hexdigest().upper()
         and proof['transportSourceSHA256']==sha(ROOT/boundary.LUA)
         and proof['captureSourceSHA256']==sha(ROOT/'tools/run_sonya_p1_jax_jump_guard_ram_v4808.py'),
         'Actual entire current guest RAM comparison and exact new executed controller/capture')
    with (FOLDER/'run.log').open('rb') as stream:raw=stream.read(64*1024*1024)
    raw=raw[:raw.rfind(b'\n')+1];lines=raw.splitlines(keepends=True);seen=False;end=None
    for n,line in enumerate(lines):
        if line.startswith(b'MK2_NAT_CAMPAIGN_JAX_FIELD '):seen=True
        if seen and ((line.startswith(b'MK2_NAT_CAMPAIGN_LOSS ') and b' stage=4' in line)
                    or (line.startswith(b'MK2_NAT_CAMPAIGN_STAGE ') and b' stage=5 ' in line)):
            end=n;break
    need(end is not None,'Actual first Jax paid loss or actual next-stage boundary before qualification')
    raw=b''.join(lines[:end+1]);text=raw.decode();rows=original.parse(text)
    fields=[r for r in rows if r['tag']=='JAX_FIELD'];decisions=[r for r in rows if r['tag']=='JAX_DECISION']
    need(fields and [r['frame'] for r in fields]==[r['frame'] for r in decisions],
         'One complete actual native field and physical decision per Jax field')
    replay=make_replay();positive=replay(text);native=callbacks(text,guest);faults=[]
    f=fields[0];frame=f['frame']
    for tag,key,value in (('JAX_FIELD','human_id',1),('JAX_FIELD','cpu_id',1),('JAX_FIELD','human_owner','01000000'),
                          ('JAX_FIELD','health','0,161'),('JAX_FIELD','reset',1-int(f['reset'])),
                          ('JAX_DECISION','reason','fabricated_evasion'),('JAX_DECISION','pound_until',0),
                          ('JAX_DECISION','jump_start',0),('INPUT','button','High_Kick')):
        target=frame
        if tag=='INPUT':target=next(r['frame'] for r in decisions if r['reason']=='pound_jump_retry_edge')
        damaged=original.change(text,tag,target,key,value)
        try:replay(damaged)
        except ValueError as error:faults.append(dict(tag=tag,key=key,rejectedBy=str(error)))
        else:raise ValueError('Actual physical Jax replay fault admitted '+key)
        need(replay(text)==positive,'Entire actual physical prefix restored')
    line=next(l for l in text.splitlines() if l.startswith('MK2_JAX_GROUND_NATIVE ') and ' kind=ground_result ' in l)
    r=dict(re.findall(r'(\w+)=([^\s]+)',line))
    for key,value in (('pc','FFF00000'),('a8','01000000'),('opcode','0000'),('carry',str(1-int(r['carry'])))):
        altered=re.sub(r'\b'+key+r'=[^\s]+',key+'='+value,line,count=1)
        need(altered!=line,'Actual callback mutation')
        try:callbacks(text.replace(line,altered,1),guest)
        except ValueError as error:faults.append(dict(tag='MK2_JAX_GROUND_NATIVE',key=key,rejectedBy=str(error)))
        else:raise ValueError('Actual original native callback fault admitted '+key)
        need(callbacks(text,guest)==native,'Every actual native callback positive restored')
    pins=dict(preflight['inputHashes'])
    for p in [Path(__file__).resolve(),Path(original.__file__).resolve(),Path(boundary.__file__).resolve(),
              FOLDER/'process.json',FOLDER/'input_hashes_before.json',FOLDER/'guest_memory_proof.json',boundary.OUT/'report.json']:
        pins[str(p.resolve())]=sha(p)
    need(all(sha(p)==h for p,h in pins.items()),'All immutable actual compiled/control/native prefix inputs unchanged')
    return dict(passed=True,case=positive,nativeCallbacks=native,inputHashes=pins,actualRowAndCallbackFaultsRejected=faults,
        nativeLogPrefixBytes=len(raw),nativeLogPrefixSHA256=hashlib.sha256(raw).hexdigest().upper(),
        terminalBoundary=lines[end].decode().rstrip(),physicalSlot=1,humanIdentity=18,cpuIdentity=11,
        originalCompleteGuardReplayRetained=True,prefixProofOnly=True,actualNaturalP1TowerClearAccepted=False,
        fullEndingPixelsAccepted=False,completeCampaignAudioAccepted=False,fullPortAcceptance=False,scope=__doc__)

if __name__=='__main__':
    report=run();OUT.mkdir()
    need(subprocess.run(['compact.exe','/C','/I','/Q','/S:'+str(OUT)],capture_output=True).returncode==0,'Compressed before writes')
    (OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k!='inputHashes'},indent=2),flush=True)
