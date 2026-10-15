"""Current v786 paired startup interruptions/retries and blade/bicycle KO.

This is NOT all moves/victims/interrupt points/CPU/pixels or full port acceptance.
Frozen legacy drivers remain untouched; v4 drivers add read-only field evidence.
"""
import json
import re
import struct
from pathlib import Path
import verify_current_lifecycle_v2 as life
import verify_native_candidate_v798 as build
from verify_ko_round_floor_shadows import digest,need

ROOT=build.ROOT
KO_CASES=[('blade',1,'kano'),('blade',2,'kitana'),('bicycle',1,'sonya'),('bicycle',2,'sub_zero')]
INT_CASES=[(m,s,v)for m in ('blade','bicycle','leg')for s in (1,2)
           for v in (('sonya',)if m=='blade'else('kano','sonya'))]
HEX={'actor','main','owner','pose','vx','vy','gravity','flags','body','trail','action',
     'entry','pc','a8','a13','mask'}
IDS={'kano':17,'sonya':18}
ENTRIES={'blade':{'action':0xfff8cc00,'create':0xfff8d800,'strike':0xfff8e400},
         'bicycle':{'action':0xfff9a400,'strike':0xfff9ee00,'tick':0xfff9d000,'release':0xfff9e000},
         'leg':{'action':0xfff80800,'strike':0xfff83800}}

def rows(log,tag):
    out=[]
    for line in log.splitlines():
        if not line.startswith('MK2_INTERRUPT_'+tag+' '):continue
        row=dict(re.findall(r'(\w+)=([^\s]+)',line))
        for key,value in row.items():
            if key in HEX:row[key]=int(value,16)
            elif re.fullmatch(r'-?\d+',value):row[key]=int(value)
        out.append(row)
    return out

def clean(f):
    return (f['y']==f['floor'] and f['vx']==f['vy']==f['gravity']==f['trail']==0 and
            f['flags']&0x1c==0 and f['body']&0x0c==0 and f['action']==0x303)

def matched(folder,inputs):
    build.matched(folder,inputs)
    result=json.loads((folder/'result.json').read_text(encoding='utf-8-sig'))
    need(result['observer_passed'] and result['exit_code']==0 and not result['cheats'] and
         result['memory_assistance']=='none' and result['candidate']==build.NAME and
         result['candidate_executable_sha256']==build.EXE and result['payload_sha256']==build.PAYLOAD,
         'Exact completed current unassisted launch')
    manifest=json.loads((folder/'input_hashes_before.json').read_text(encoding='utf-8-sig'))
    need(manifest==result['input_hashes'],'Before/after launch input inventory')
    required={'mk2ks_selector_exit_test.lua','mk2ks_native_shang_morph.lua'}
    need(required<={Path(p).name for p in manifest},'All transitive cold-selection Lua inputs tracked')
    for path,sha in manifest.items():
        need(digest(path)==sha,'Frozen launch input changed: '+path);inputs[path]=sha
        if Path(path).suffix in ('.lua','.ps1','.json'):
            need(digest(folder/'input_sources'/Path(path).name)==sha,'Frozen launch source changed: '+path)
        if Path(path).suffix=='.lua':
            source=Path(path).read_text()
            need(not re.search(r'write_u\d+|:write_|load_?state|\.value\s*=(?!=)',source),
                 'Tracked observers cannot inject guest state')
    info=ROOT/build.NAME/'build-info.json'
    metadata=json.loads(info.read_text(encoding='utf-8-sig'))
    need(metadata['executable_sha256']==build.EXE and metadata['payload_sha256']==build.PAYLOAD,
         'Current exact build metadata')
    for path,sha in metadata['input_hashes'].items():
        need(manifest.get(path)==sha and digest(path)==sha,'Every actual current build input tracked: '+path)
    need(digest(ROOT/build.NAME/'mkport_candidate.exe')==build.EXE and
         digest(ROOT/build.NAME/'roms/mk2ks/mk2ks.mdata')==build.PAYLOAD,
         'Actual current executable and matched payload bytes')
    for path in (info,folder/'run.log',folder/'result.json',folder/'input_hashes_before.json'):
        inputs[str(path)]=digest(path)
    for path in (folder/'snap').rglob('*.png'):inputs[str(path)]=digest(path)
    return result

def verify_interrupt(log,move,side,victim):
    need(not re.search(r'LUA ERROR|Lua error|Fatal error|INTERRUPT_ERROR|access violation',log,re.I),
         'No actual runtime or driver errors')
    marker='MK2KS_'+move.upper()+'_INTERRUPT_RESULT pass=true '
    need(marker in log,'Complete original counter/retry driver')
    for marker in ('MK2KS_EXIT_RESULT pass=true ','MK2KS_DISPLAY_RESULT pass=true ',
                   'MK2KS_HUD_SHADOW_RESULT pass=true ','MK2KS_STABILITY stalled_frames=0 trap_frames=0'):
        need(marker in log,'Original cold selection/presentation/stability guard')
    names=[victim,victim];names[side-1]='kano'if move=='blade'else'sonya'
    need(rows(log,'BOOT')==[dict(move=move,side=side,names=','.join(names),writes=0)],'Actual boot roles')
    fields=rows(log,'FIELD');need(fields,'Actual paired field observer required')
    by={(f['frame'],f['slot']):f for f in fields};first=min(f['frame']for f in fields);last=max(f['frame']for f in fields)
    need(len(fields)==len(by)==(last-first+1)*2 and set(by)=={(f,s)for f in range(first,last+1)for s in (1,2)},
         'Every callback for both live actors without gaps or duplicates')
    owners={n:(by[first,n]['actor'],by[first,n]['main'])for n in (1,2)}
    floors={n:by[first,n]['floor']for n in (1,2)}
    for f in fields:
        n=f['slot'];need(f['writes']==0 and f['mode']==2 and f['state']==1 and
         f['id']==f['roster']==IDS[names[n-1]] and f['owner']==f['actor'] and
         (f['actor'],f['main'])==owners[n] and f['floor']==floors[n] and
         0x01000000<=f['actor']<0x01100000 and 0x01000000<=f['main']<0x01100000 and
         0<=f['hp']<=161 and f['phase']in(1,2), 'Native identity/Main ownership, own floor and health')
    need(all(by[first,n]['hp']==161 for n in (1,2)),'Original unassisted match health')
    events=rows(log,'EVENT');known={**ENTRIES[move],'ready':0xff861350,'idle':0xff861500}
    for e in events:
        n=e['slot'];need(e['kind']in known and e['entry']==known[e['kind']] and
         e['pc']==(0xff835480 if e['kind']=='strike'else e['entry']+16) and
         (e['actor'],e['main'])==owners[n] and e['owner']==e['a8']==e['actor'] and
         e['a13']==e['main'] and e['id']==IDS[names[n-1]] and e['writes']==0,
         'Typed actual instruction/data-reader provenance and owner')
    actions=[e for e in events if e['kind']=='action']
    need(len(actions)==2 and [e['phase']for e in actions]==[1,2] and
         all(e['slot']==side for e in actions),'One own original special per interrupted attempt/retry')
    health=rows(log,'HEALTH');damage=[h for h in health if h['before']!=h['after']]
    need(len(damage)==2,'Only the actual uppercut and successful retry damage')
    counter,retry=damage;amount={'blade':26,'bicycle':22,'leg':35}[move]
    need(counter['slot']==side and counter['phase']==1 and counter['before']==161 and counter['after']==121 and
         actions[0]['frame']<=counter['frame']<actions[0]['frame']+40,'Counter hits an already active native special')
    need(retry['slot']==3-side and retry['phase']==2 and retry['before']==161 and retry['after']==161-amount and
         actions[1]['frame']<retry['frame']<actions[1]['frame']+100,'Successful own retry damages only original opponent')
    for h in health:
        need(h['pc']==0xff836700 and h['writes']==0 and h['mask']==0xffff and
             0<=h['after']<=h['before']<=161,'Original collision stores, never health assistance')
    for n in (1,2):
        for frame in range(first,last):
            stores=[h for h in health if h['slot']==n and h['frame']==frame]
            a,b=by[frame,n]['hp'],by[frame+1,n]['hp']
            if stores:
                need(stores[0]['before']==a and stores[-1]['after']==b and
                     all(x['after']==y['before']for x,y in zip(stores,stores[1:])), 'Complete ordered native health ledger')
            else:need(a==b,'Unexplained health change')
    strikes=[e for e in events if e['kind']=='strike']
    need(strikes and all(e['phase']==2 and e['slot']==side for e in strikes),
         'Interruption precedes every catch/strike; retry uses original collision reader')
    if move=='bicycle':
        ticks=[e for e in events if e['kind']=='tick'];releases=[e for e in events if e['kind']=='release']
        need(len(ticks)==48 and all(e['phase']==2 and e['slot']==side for e in ticks) and
             [e['frame']for e in ticks]==list(range(ticks[0]['frame'],ticks[0]['frame']+48)) and
             len(releases)==1 and releases[0]['phase']==2 and releases[0]['slot']==3-side,
             'No first-attempt pair; full consecutive 48-tick retry and victim release')
    if move=='blade':
        creates=[e for e in events if e['kind']=='create']
        need(len(creates)==2 and [e['phase']for e in creates]==[1,2], 'One actual attached blade per attempt')
        need(any(by[f,side]['trail']!=0 for f in range(actions[0]['frame']+1,counter['frame']+1)),
             'Blade was active, not a pre-entry counter fixture')
        hit_frames=re.findall(r'^MK2KS_BLADE_INTERRUPT_HIT frame=(\d+)$',log,re.M)
        cleanup_frames=re.findall(r'^MK2KS_BLADE_INTERRUPT_CLEANUP frame=(\d+)$',log,re.M)
        need(len(hit_frames)==len(cleanup_frames)==1 and int(hit_frames[0])==counter['frame'],
             'Actual native blade damage/cleanup observations')
        cleanup=int(cleanup_frames[0])
        # P2's hit handoff can run on the next native task field. Bind to
        # the observed original cleanup, not an invented same-field deadline.
        need(0<=cleanup-counter['frame']<=1 and
             all(by[f,side]['trail']==0 for f in range(cleanup+1,actions[1]['frame']+1)),
             'Original observed hit handoff immediately removes cancelled blade attachment')
    clean_between=[f for f in range(counter['frame']+1,actions[1]['frame'])if
                   all(clean(by[f,n])for n in (1,2))]
    need(clean_between,'Both actors actually recover before retry; not merely summary states')
    for phase in (1,2):
        for n in (1,2):
            need(any(e['kind']=='ready'and e['phase']==phase and e['slot']==n for e in events),
                 'Each actual Main has original ready continuation in each phase')
    need(all(clean(by[last,n])for n in (1,2)),'Both final actors grounded, idle and fully detached')
    inputs=rows(log,'INPUT');keys={(i['frame'],i['slot'],i['button'])for i in inputs}
    need(len(keys)==len(inputs) and all(i['writes']==0 for i in inputs),'Real input inventory')
    epoch=actions[0]['frame']-actions[0]['age']
    delay=(3-side if move=='leg'else 10-side if move=='bicycle'else 11-side)
    need(all((epoch+delay+k,3-side,'hp')in keys for k in range(4)), 'Actual opponent uppercut input')
    need(any((f,3-side,'down')in keys for f in range(epoch+delay-8,epoch+delay)), 'Real crouch before uppercut')
    return dict(move=move,side=side,victim=victim,pairedFields=len(fields),counterDamage=40,
                retryDamage=amount,firstFullyRecoveredFrame=clean_between[0],fullPortAcceptance=False)

def verify():
    inputs={};interruptions=[];knockouts=[]
    original=ROOT/'mk2/mk2-maincpu.bin'
    need(digest(original)=='45B3285496DB555EFAF4A3608A4F59845DD47A82E4A0593607E0592F47B36F23',
         'Original MKII instruction reference')
    raw=original.read_bytes()
    need(struct.unpack_from('<H',raw,(0xff835470-0xff800000)//8)[0]==0x9401,
         'Original collision descriptor MOVE instruction; actual PC is Ff835480, not descriptor+16')
    need(struct.unpack_from('<H',raw,(0xff83bb00-0xff800000)//8)[0]==0x9720,
         'Original native animation list reader instruction')
    inputs[str(original)]=digest(original)
    for move,side,victim in INT_CASES:
        folder=ROOT/f'audit_v823_interrupt_{move}_p{side}_{victim}';meta=matched(folder,inputs)
        need((meta['move'],meta['side'],meta['victim'])==(move,side,victim),'Case metadata')
        interruptions.append(verify_interrupt((folder/'run.log').read_text(encoding='utf-8-sig'),move,side,victim))
    for move,side,victim in KO_CASES:
        folder=ROOT/f'audit_v823_ko_{move}_p{side}_{victim}';meta=matched(folder,inputs)
        need((meta['move'],meta['side'],meta['victim'])==(move,side,victim),'Case metadata')
        log=(folder/'run.log').read_text(encoding='utf-8-sig');proof=life.verify(log,move,side,victim)
        need(proof['passed'],'Full existing per-field KO/round verification: '+str(proof['errors']))
        need(all(e['pc']==0xff835480 for e in life.rows(log,'EVENT')if e['kind']=='strike'),
             'KO moves use original native collision descriptor reader')
        proof['fullPortAcceptance']=False;knockouts.append(proof)
    for file in ('tools/verify_current_interrupt_and_ko_v824.py','tools/verify_current_lifecycle_v2.py',
                 'tools/verify_current_lifecycle.py',
                 'tools/verify_native_candidate_v798.py','tools/verify_ko_round_floor_shadows.py',
                 'tools/inspect_ground_presentation.py','tools/test_current_interrupt_and_ko_v825.py',
                 'tools/run_current_interrupt_v823.ps1','tools/run_current_lifecycle_v823.ps1'):
        inputs[str(ROOT/file)]=digest(ROOT/file)
    return dict(passed=True,fullPortAcceptance=False,candidate=build.NAME,interruptions=interruptions,
                knockouts=knockouts,inputHashes=inputs,scope='Three paired startup interruption/retry families '
                'in both slots, plus four blade/bicycle full field choreography KO/round-two paths. '
                'Not all victims/moves/interrupt points/KO cases/CPU, full pixels, campaign, finishers, audio or release acceptance.')

if __name__=='__main__':
    import sys
    output=ROOT/sys.argv[1]
    need(not output.exists(),'Do not overwrite accepted evidence')
    proof=verify();output.mkdir()
    (output/'verification.json').write_text(json.dumps(proof,indent=2)+'\n')
    print(json.dumps({'candidate':proof['candidate'],'interruptions':len(proof['interruptions']),
        'knockouts':len(proof['knockouts']),'pairedFields':sum(p['pairedFields']for p in proof['interruptions'])+
        sum(p['actual_fields']for p in proof['knockouts']),'passed':proof['passed'],'fullPortAcceptance':False}))
