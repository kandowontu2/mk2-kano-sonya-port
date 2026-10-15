"""Source-bound actual input-only Square discovery and whole native ledgers.

Seven real runs retained including three genuine no-Square scenarios. Native
branch decisions and every 26-check miss boundary are checked, not inferred from
unrelated damage. This inventory is not move-phase/raster/audio acceptance.
"""
import json,re,struct,sys,traceback
from pathlib import Path
import verify_native_friendship_palette_assembly_v2750 as assembly
import verify_native_extended_cpu_v2946 as ledgers
import run_native_cpu_square_dispatch_v2995 as dispatch
import current_sonya_cpu_square_contract_v2045 as square
import verify_current_cpu_overlap_v1911 as overlap

ROOT=assembly.ROOT
OUT=ROOT/'audit_v2999_native_cpu_square_inventory_checked'
need=assembly.need
HEX=set('entry pc opcode mask status actor main owner action pose xraw yraw vx vy gravity flags body facing trail schedule start stop at before after op0 op1 op2'.split())|{f'a{i}'for i in range(15)}
TEXT={'kind','assistance','words'}

def rows(log,tag):
    result=[]
    for line in log.splitlines():
        if not line.startswith(tag+' '):continue
        values=re.findall(r'(\w+)=([^\s]+)',line)
        need(len(values)==len(dict(values)),'Unambiguous actual boundary fields')
        result.append({k:v if k in TEXT else int(v,16 if k in HEX else 10)for k,v in values})
    return result

def capture(folder,build,player,approach,policy,pins):
    def pin(path,wanted=None):
        path=Path(path);path=(path if path.is_absolute()else ROOT/path).resolve()
        actual=assembly.sha(path)
        need(wanted is None or actual==wanted,'Unchanged actual input '+str(path))
        need(str(path)not in pins or pins[str(path)]==actual,'Consistent immutable input')
        pins[str(path)]=actual
    candidate=assembly.NAME if build=='new'else assembly.prior.NAME
    guest,old,payload,_,_=assembly.expected();guest=guest if build=='new'else old
    meta=json.loads((folder/'result.json').read_text(encoding='utf-8-sig'))
    before=json.loads((folder/'input_hashes_before.json').read_text(encoding='utf-8-sig'))
    info=json.loads((ROOT/candidate/'build-info.json').read_text(encoding='utf-8-sig'))
    need(meta['exit_code']==0 and meta['candidate']==candidate and meta['player']==player and
         meta['boot_frame']==(613 if build=='new'else 604)and meta['confirm_age']==264 and
         meta['approach']==approach and meta['policy']==policy and meta['assistance']=='none'and
         not meta['cheats_enabled']and(meta['cpu_slot'],meta['human_slot'])==(2,1)and before==meta['input_hashes'],
         'Terminal normal physical fixture, no native choices prescribed')
    need(meta['executable_sha256']==info['executable_sha256']and meta['payload_sha256']==info['payload_sha256']and
         all(before.get(file)==wanted for file,wanted in info['input_hashes'].items()),'All compiled inputs match captured runtime')
    pin(ROOT/candidate/'build-info.json');pin(ROOT/candidate/'mkport_candidate.exe',info['executable_sha256'])
    pin(ROOT/candidate/'roms/mk2ks/mk2ks.mdata',info['payload_sha256'])
    need((folder/'guest_maincpu.bin').read_bytes()==guest and (ROOT/candidate/'roms/mk2ks/mk2ks.mdata').read_bytes()==payload,
         'Whole guest independently reconstructed, not sampled or address-masked')
    for file,wanted in before.items():
        pin(file,wanted)
        if Path(file).suffix in('.lua','.ps1','.json'):pin(folder/'input_sources'/Path(file).name,wanted)
        if Path(file).suffix=='.lua':
            need(not re.search(r':write_|write_u\d+|\.value\s*=(?!=)|load_?state|:reset\(',Path(file).read_text()),'No guest/register/AI/RNG/HP injection')
    log=(folder/'run.log').read_text(encoding='utf-8-sig')
    need(not re.search(r'LUA ERROR|stack traceback|fatal error|access violation',log,re.I),'No emulator or observer failure')
    cold=ledgers.pair.rows_prefix(log,'MK2_P2CPU_COLD_LIVE ');selection=ledgers.pair.rows_prefix(log,'MK2_P2CPU_SELECT_RESULT ')
    need(len(cold)==len(selection)==1 and cold[0]['human_id']==selection[0]['human_id']==ledgers.pair.HUMANS[player]and
         cold[0]['cpu_id']==selection[0]['initial_cpu']==18 and selection[0]['checks']==50 and selection[0]['errors']==0,
         'Actual natural CPU Sonya and actual human selected through native CSS')
    health,round_by=ledgers.health_ledger(log,guest,player)
    state=ledgers.state_ledgers(log,guest,player,round_by)
    square.source(log,guest)
    windows=rows(log,'MK2_SQUARE_BOUNDARY_CODE')
    need({(w['start'],w['stop'])for w in windows}=={(0xffffd1c0,0xffffd340),(0xff831a60,0xff831bc0),(0xff876be0,0xff876e00)}and len(windows)==3,
         'Full added native hit continuation windows')
    for w in windows:
        words=[int(x,16)for x in w['words'].split(',')];lo,hi=((w[k]-0xff800000)//8 for k in('start','stop'))
        need(struct.pack('<'+'H'*len(words),*words)==guest[lo:hi],'Every added hit continuation word source-bound')
    for path in folder.rglob('*'):
        if path.is_file():pin(path)
    return log,guest,dict(candidate=candidate,health=health,stateLedger=state,cold=cold[0],selection=selection[0])

def boundary(log,guest,player):
    events=rows(log,'MK2_SQUARE_BOUNDARY_EVENT');snapshots=rows(log,'MK2_SQUARE_BOUNDARY_ENTRY_STATE')
    native=[r for r in overlap.rows(log,'EVENT')if r['kind']=='square']
    entries=[r for r in events if r['kind']=='entry']
    need(len(entries)==len(native)and len(snapshots)==2*len(entries),'Every actual Square has both native entry snapshots')
    result=[]
    for event,original in zip(entries,native):
        need(event['frame']==original['frame']and event['a8']==original['a8']and event['a13']==original['a13'],
             'Independent original and boundary native entry agree')
        own=[r for r in snapshots if r['serial']==event['serial']and r['slot']==2]
        human=[r for r in snapshots if r['serial']==event['serial']and r['slot']==1]
        need(len(own)==len(human)==1,'Both actual physical entry actors')
        for r,identity,state in ((own[0],18,0),(human[0],ledgers.pair.HUMANS[player],1)):
            need(r['frame']==event['frame']and r['owner']==r['actor']and(r['id'],r['roster'],r['state'],r['mode'])==(identity,identity,state,2)and
                 r['hp']>0 and r['floor']==r['stage_floor']-(135 if identity==18 else 134)and r['stage']==0 and r['schedule']==0xfffa3180,
                 'Native entry identity, ownership, floor and live health')
        need((own[0]['actor'],own[0]['main'])==(event['a8'],event['a13'])and own[0]['action']==0x303 and own[0]['flags']&0x1c==0 and own[0]['body']&12==0,
             'Real clean CPU entry, not a proxy')
        group=[r for r in events if r['serial']==event['serial']]
        need([r['kind']for r in group]==['entry']+['collision_return']*26,'Genuine Square miss, no native hit entry')
        for r in group:
            need(r['writes']==0 and r['assistance']=='none'and r['mask']==65535 and r['pc']==r['entry']+16 and
                 r['carry']==(r['status']>>30)&1 and struct.unpack_from('<H',guest,(r['entry']-0xff800000)//8)[0]==r['opcode']and
                 (r['a8'],r['a13'])==(own[0]['actor'],own[0]['main']),'All native collision boundaries owned and source-bound')
        collisions=group[1:]
        need([r['frame']for r in collisions]==list(range(event['frame']+9,event['frame']+35))and
             [r['a11']for r in collisions]==list(range(26,0,-1))and all(r['entry']==0xffffcef0 and r['carry']==0 and r['a0']==0xffffda00 for r in collisions),
             'All twenty-six actual native collision returns, decrement and miss carry')
        result.append(dict(start=event['frame'],serial=event['serial'],nativeCollisionChecks=26,hitEntries=0,entryStates=[human[0],own[0]],
                           fullMovePhaseAccepted=False,renderOrAudioAccepted=False))
    return result

def verify():
    pins={};cases={}
    for build,player,approach,policy in dispatch.CASES:
        folder=ROOT/dispatch.name((build,player,approach,policy))
        log,guest,case=capture(folder,build,player,approach,policy,pins)
        moves=boundary(log,guest,player)
        case.update(squareBoundaries=moves,actualSquareEntries=len(moves),noSquareScenario=not moves)
        cases[folder.name]=case
        print(folder.name+': actual Square entries='+str(len(moves))+', full state/health ledgers checked',flush=True)
    need(sum(c['actualSquareEntries']for c in cases.values())==4 and sum(c['noSquareScenario']for c in cases.values())==3,
         'Retain all genuine branch misses, no falsified special passes')
    for module in tuple(sys.modules.values()):
        file=getattr(module,'__file__',None)
        if file and Path(file).resolve().is_relative_to(ROOT/'tools')and Path(file).suffix=='.py':pins[str(Path(file).resolve())]=assembly.sha(file)
    pins[str((ROOT/'audit_v2996_native_cpu_square_dispatch/report.json').resolve())]=assembly.sha(ROOT/'audit_v2996_native_cpu_square_dispatch/report.json')
    for file,wanted in pins.items():need(assembly.sha(file)==wanted,'All immutable source/capture inputs unchanged')
    return dict(passed=True,cases=cases,actualPhysicalFixtures=7,actualSquareEntries=4,genuineNoSquareScenarios=3,
                exactNativeMissCollisionChecks=104,wholeStateHealthLedgersAccepted=True,
                fullMovePhaseAcceptance=False,allCPUAccepted=False,fullPortAcceptance=False,inputHashes=pins,scope=__doc__)

if __name__=='__main__':
    need(not OUT.exists(),'Immutable actual discovery inventory')
    try:report=verify()
    except Exception as error:report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
    OUT.mkdir();(OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items()if k not in('inputHashes','cases')},indent=2),flush=True)
    raise SystemExit(0 if report['passed']else 1)
