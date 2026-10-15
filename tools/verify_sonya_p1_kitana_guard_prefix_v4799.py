"""Independent complete per-field Kitana physical-input replay of real prefix.

Uses all original4194 ownership, action, health, reset and exact button-edge
checks. CPU context4 and separate KITANA observer names are declared changes.
No whole-campaign, ending, complete move-art/audio or finished-port acceptance.
"""
import hashlib,inspect,json,subprocess
from pathlib import Path
import verify_mirror_guard_zoning_prefix_v4194 as original
import qualify_sonya_p1_kitana_guard_source_v4795 as boundary
ROOT,need,sha=boundary.ROOT,boundary.need,boundary.sha
FOLDER=ROOT/'audit_v4797_sonya_p1_kitana_guard_ram'
OUT=ROOT/'audit_v4800_sonya_p1_kitana_guard_prefix_checked'

def make_replay():
    body=inspect.getsource(original.replay)
    changes=[("'GUARD_DECISION'","'KITANA_DECISION'"),
             ("'GUARD_FIELD'","'KITANA_FIELD'"),
             ("'GUARD_ACTION'","'KITANA_ACTION'"),
             ("f['human_slot'] == '2'","f['human_slot'] == '1'"),
             ("r['slot'] == '2'","r['slot'] == '1'"),
             ('Actual true Sonya P2 identity','Actual true Sonya P1 identity'),
             ("f['cpu_id'] == f['cpu_roster'] == '18'","f['cpu_id'] == f['cpu_roster'] == '4'"),
             ("r['tag'] == 'SPECIAL' and r['move'] == 'leg'","r['tag'] == 'SPECIAL' and r['move'] == 'leg' and r['frame'] in decisions")]
    for before,after in changes:
        need(body.count(before)==1,'Exact original replay context adaptation '+before)
        body=body.replace(before,after,1)
    need(body.count("f['cpu_roster'] == '18'")==4,'Exactly four readiness/move/approach CPU predicates')
    body=body.replace("f['cpu_roster'] == '18'","f['cpu_roster'] == '4'")
    scope=dict(vars(original),__file__=__file__)
    exec(compile(body,__file__+'::complete4194_distinct_true_Kitana_context','exec'),scope)
    return scope['replay']

def run():
    need(not OUT.exists(),'Fresh actual prefix qualification')
    boundary.source_boundary()
    preflight=json.loads((boundary.OUT/'report.json').read_text())
    guest=json.loads((FOLDER/'guest_memory_proof.json').read_text())
    need(preflight['passed'] and guest['everyActualByteComparedInRAM'] and guest['bytes']==1048576
         and guest['guestDumpFilesWritten']==0 and guest['transportSourceSHA256']==sha(ROOT/boundary.LUA)
         and guest['captureSourceSHA256']==sha(ROOT/'tools/run_sonya_p1_kitana_guard_ram_v4794.py'),
         'Actual initialized guest transport and independently qualified physical source')
    # Fixed snapshot window; only complete lines, never an unbounded growing-log read.
    with (FOLDER/'run.log').open('rb') as stream:raw=stream.read(32*1024*1024)
    raw=raw[:raw.rfind(b'\n')+1];lines=raw.splitlines(keepends=True)
    kitana_seen=False;end=None
    for i,line in enumerate(lines):
        if line.startswith(b'MK2_NAT_CAMPAIGN_KITANA_FIELD '):kitana_seen=True
        if kitana_seen and ((line.startswith(b'MK2_NAT_CAMPAIGN_LOSS ') and b' stage=2' in line)
            or (line.startswith(b'MK2_NAT_CAMPAIGN_STAGE ') and b' stage=3 ' in line)):
            end=i;break
    need(end is not None,'Actual first Kitana paid loss or actual next-stage event must exist before prefix qualification')
    raw=b''.join(lines[:end+1]);text=raw.decode();rows=original.parse(text)
    fields=[r for r in rows if r['tag']=='KITANA_FIELD'];decisions=[r for r in rows if r['tag']=='KITANA_DECISION']
    need(fields and len(fields)==len(decisions) and [r['frame'] for r in fields]==[r['frame'] for r in decisions],
         'Exactly one complete real native state and physical decision for every Kitana field')
    replay=make_replay();positive=replay(text)
    need(positive['actualNativeLegActivations']>0,'Actual own Kitana-context Leg Grab tasks, never planned commands credited')
    faults=[];f=fields[0];frame=f['frame']
    cases=[('KITANA_FIELD','human_id',1),('KITANA_FIELD','human_roster',1),
           ('KITANA_FIELD','cpu_id',1),('KITANA_FIELD','cpu_roster',1),
           ('KITANA_FIELD','human_owner','01000000'),('KITANA_FIELD','cpu_owner','01000000'),
           ('KITANA_FIELD','health','0,161'),('KITANA_FIELD','reset',1-int(f['reset'])),
           ('KITANA_FIELD','cpu_action',0x507),('KITANA_DECISION','reason','fabricated_success')]
    attack=next((r for r in rows if r['tag']=='INPUT' and r['frame'] in {f['frame'] for f in fields}
                 and r['button'] in ('Low_Punch','High_Punch')),None)
    if attack:cases.append(('INPUT','button','High_Kick'))
    for tag,key,value in cases:
        target=attack['frame'] if tag=='INPUT' else frame
        if tag=='KITANA_FIELD' and key=='cpu_action':
            target=next(r['frame'] for r in decisions if r['reason']=='grounded_approach')
        damaged=original.change(text,tag,target,key,value)
        try:replay(damaged)
        except ValueError as error:faults.append(dict(tag=tag,key=key,rejectedBy=str(error)))
        else:raise ValueError('Actual Kitana state/input fault admitted '+repr((tag,key)))
        need(replay(text)==positive,'Entire original actual prefix restored')
    pins=dict(preflight['inputHashes'])
    for p in [Path(__file__).resolve(),Path(original.__file__).resolve(),Path(boundary.__file__).resolve(),
              FOLDER/'process.json',FOLDER/'input_hashes_before.json',FOLDER/'guest_memory_proof.json',boundary.OUT/'report.json']:
        pins[str(p.resolve())]=sha(p)
    need(all(sha(p)==h for p,h in pins.items()),'Every immutable compiled/control/native prefix source byte unchanged')
    return dict(passed=True,case=positive,inputHashes=pins,actualRowFaultsRejected=faults,
        nativeLogPrefixBytes=len(raw),nativeLogPrefixSHA256=hashlib.sha256(raw).hexdigest().upper(),
        terminalBoundary=lines[end].decode().rstrip(),physicalSlot=1,humanIdentity=18,cpuIdentity=4,
        originalCompleteGuardReplayRetained=True,prefixProofOnly=True,
        actualNaturalP1TowerClearAccepted=False,fullEndingPixelsAccepted=False,completeCampaignAudioAccepted=False,
        fullPortAcceptance=False,scope=__doc__)

if __name__=='__main__':
    report=run()
    OUT.mkdir();need(subprocess.run(['compact.exe','/C','/I','/Q','/S:'+str(OUT)],capture_output=True).returncode==0,'Compressed before writes')
    (OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k!='inputHashes'},indent=2),flush=True)
