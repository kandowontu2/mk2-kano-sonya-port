"""Bounded native CPU random morph/turn/restore proof, NOT full integration.

The source game explicitly uses stage-14 and P1-health fixture assistance.
Morph targets, native processes and choreography are never selected by Lua.
"""
import argparse
import hashlib
import json
import re
import struct
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
PREFIX='MK2_SHANG_ROSTER_'
SCOPE='stage14_P1_health_assisted_native_CPU_random_morph_turn_restore_not_human_morph_commands_all_CPU_moves_pixels_audio_or_full_goal'
EXE='029AB9DFBA72B07BD02B5EF3653012E914D43DEDC3B6DA3E4B6B74DE79A9924D'
PAYLOAD='82FE153FB56B46A6F9D42F493451AC3D59AD61713433714ACA7704E2881F8951'


def rows(log):
    return [(line[len(PREFIX):].split()[0],dict(re.findall(r'(\w+)=([^\s]+)',line)))
            for line in log.splitlines() if line.startswith(PREFIX)]


def _verify_cycle(log,fighter,stock_rates,cycle_index=None,cycle_total=1):
    if fighter not in ('kano','sonya'):raise ValueError('Actual owned morph required')
    identity=17 if fighter=='kano' else 18
    root='FF0C1800' if identity==17 else 'FF0C1A00'
    palette='FF0C0800' if identity==17 else 'FF0C1000'
    groups=['FF0C4000','FF0C4060','FF0C40C0'] if identity==17 else ['FF0C4120','FF0C4180','FF0C41E0']
    records=rows(log);errors=[]
    def need(ok,message):
        if not ok:errors.append(message)
    def tagged(tag):return [r for t,r in records if t==tag]
    def number(r,key):
        try:return int(r.get(key,''))
        except ValueError:return -1
    def frame(r):return number(r,'frame')
    rom=tagged('ROM');timing=tagged('TURN_TABLE')
    need(len(rom)==1 and rom[0].get('random')=='19C0' and
         rom[0].get('map')=='0,1,2,3,4,5,5,7,8,9,10,11,17,18' and
         rom[0].get('lookup')=='FFFC8300','Fourteen actual native random choices and scoped lookup')
    need(len(timing)==1 and timing[0].get('human')==timing[0].get('cpu')=='FFFFBF80' and
         timing[0].get('kano')==timing[0].get('sonya')=='00000002' and
         timing[0].get('stock','').split(',')==stock_rates,'Both native turn lookups, two-field added rows and all 17 unchanged stock rows')
    need(all(r.get('writes')=='0' for _,r in records),'Morph observer must remain read-only')
    need('MK2KS_CPU_DIAGNOSTIC_LADDER_RESULT requested=14 injected=true' in log and
         'MK2KS_CPU_DIAGNOSTIC_P1_REGEN_RESULT enabled=true' in log,'Explicit stage and health fixture scope')
    need(not re.search(r'Fatal error|stack traceback|Lua error',log,re.I),'No emulator/Lua failure')
    choices=[r for r in tagged('CHOICE') if r.get('id')==str(identity)]
    stores=[r for r in tagged('STORE') if r.get('old')=='6' and r.get('id')==str(identity)]
    restores=[r for r in tagged('STORE') if r.get('old')==str(identity) and r.get('id')=='6']
    all_restores=restores[:]
    if cycle_index is not None:
        need(len(choices)==len(stores)==len(restores)==cycle_total,'Every actual requested native morph has its own forward and reverse stores')
        choices=choices[cycle_index:cycle_index+1];stores=stores[cycle_index:cycle_index+1];restores=restores[cycle_index:cycle_index+1]
    need(len(choices)==1,'Exactly one actual requested native morph choice per cycle')
    need(len(stores)==1,'Actual native forward character-ID store per cycle')
    need(len(restores)==1,'Actual native return-to-Shang store')
    count=0;start=end=-1;signature=False
    if len(choices)==len(stores)==len(restores)==1:
        choice,store,restore=choices[0],stores[0],restores[0]
        start,end=frame(store),frame(restore)
        owner=(choice.get('actor'),choice.get('main'))
        def owned(r):return (r.get('actor'),r.get('main'))==owner
        need(all(0x01000000<=int(a or '0',16)<0x01100000 for a in owner),'Valid published native actor/task')
        need(choice.get('roster')=='6' and choice.get('state')=='0' and choice.get('stage')=='14' and
             choice.get('pc')=='FF86E490','Actual stock-roster CPU morph entry')
        need(any(owned(r) and r.get('bound')=='14' and r.get('pc')=='FF86E290' and
                 frame(r)==frame(choice) for r in tagged('RNG')),'Actual native RNG call precedes chosen target')
        need(frame(choice)<start<end and 512<=end-start<=900,'Finite native timer-controlled added-form window')
        need(owned(store) and store.get('pc')=='FF86E670' and store.get('a9')==f'{identity:08X}',
             'Original forward store instruction with chosen register ID')
        need(owned(restore) and restore.get('pc')=='FFA16700' and restore.get('a0')=='00000006',
             'Original restore store instruction, not a forced host identity')
        need(any(owned(r) and r.get('root')==root and r.get('choice')==str(identity) and
                 r.get('pc')=='FF86E590' and frame(choice)<=frame(r)<start for r in tagged('LOOKUP')),
             'Own forward morph transition sequence')
        begin=[r for r in tagged('RESTORE_BEGIN') if owned(r) and r.get('id')==str(identity) and frame(choice)<=frame(r)<=end]
        lookup=[r for r in tagged('RESTORE_LOOKUP') if owned(r) and r.get('id')==str(identity) and frame(choice)<=frame(r)<=end]
        need(len(begin)==len(lookup)==1 and begin[0].get('pc')=='FFA16310' and
             lookup[0].get('root')==root and lookup[0].get('pc')=='FFA16450' and
             frame(begin[0])==frame(lookup[0])==end-12,'Native reverse entry and own restore lookup')
        actual=[r for r in tagged('GROUP') if owned(r) and frame(choice)<=frame(r)<end]
        need([r.get('group') for r in actual]==groups+groups[::-1] and
             all(r.get('pc')=='FF8387A0' for r in actual),'Three original two-part transitions in each direction')
        if len(actual)==6:
            need([frame(r) for r in actual[:3]]==[start-12,start-8,start-4] and
                 [frame(r) for r in actual[3:]]==[end-12,end-8,end-4],
                 'Native four-field transition holds without omissions')
        pals=[r for r in tagged('PALETTE') if owned(r) and frame(choice)<=frame(r)<end]
        need(len(pals)==2 and all(r.get('palette')==palette and r.get('pc')=='FF907520' for r in pals),
             'Own original transition palette in both directions')
        fields=[r for r in tagged('FIELD') if start<frame(r)<=end]
        count=len(fields)
        need([frame(r) for r in fields]==list(range(start+1,end+1)),
             'Every callback field through the full added form')
        need(all(owned(r) and r.get('id')==str(identity) and r.get('roster')=='6' and
                 r.get('state')=='0' and r.get('stage')=='14' and r.get('mode')=='2' and
                 0<number(r,'health')<=161 and 0<number(r,'floor')<200 and
                 int(r.get('pose','0'),16)>=0xfe800000 for r in fields),
             'Stable live owned body/CPU roster/floor/health for every form field')
        after=[r for r in tagged('RESTORED_FIELD') if r.get('from')==str(identity) and end<frame(r)<=end+120]
        need([number(r,'age') for r in after]==list(range(1,121)) and
             [frame(r) for r in after]==list(range(end+1,end+121)),
             '120 consecutive actual post-restoration fields')
        need(all(owned(r) and r.get('id')=='6' and r.get('roster')=='6' and r.get('state')=='0' and
                 r.get('stage')=='14' and r.get('mode')=='2' and r.get('floor')=='87' and
                 r.get('trail')=='00000000' for r in after) and
             any(r.get('vx')!='00000000' and r.get('action')=='0303' for r in after),
             'Shang returns to native floor and active CPU movement, without an attached effect')
        need(any(owned(r) and r.get('old')=='6' and r.get('id') in [str(i) for i in range(12) if i!=6] and
                 r.get('pc')=='FF86E670' and frame(r)>frame(all_restores[0])+120 for r in tagged('STORE')),
             'Later ordinary stock morph remains operational')
        if identity==18:
            legs=[frame(r) for r in fields if r.get('action')=='0110']
            signature=bool(legs)
            if signature or cycle_total==1:
                need(signature and any(owned(r) and r.get('id')=='18' and r.get('rate')=='00000002' and
                     r.get('list')=='FF020DC0' and max(legs or [end])<=frame(r)<end for r in tagged('TIMING')),
                     'Sonya signature leg action and native two-field turn after it')
    result=tagged('RESULT')
    need(len(result)==1 and result[0].get(fighter)==str(cycle_total) and result[0].get('restore_'+fighter)==str(cycle_total) and
         result[0].get('errors')=='0','Bounded observer counts agree with actual native trace')
    return dict(passed=not errors,errors=errors,fighter=fighter,form_fields=count,store_frame=start,
                restore_frame=end,signature_leg_observed=signature,scope=SCOPE,whole_character_integration_complete=False)


def verify_log(log,fighter,stock_rates):
    identity=17 if fighter=='kano' else 18
    count=sum(tag=='CHOICE' and record.get('id')==str(identity) for tag,record in rows(log))
    if count<=1:return _verify_cycle(log,fighter,stock_rates)
    cycles=[_verify_cycle(log,fighter,stock_rates,index,count) for index in range(count)]
    errors=sorted(set(error for cycle in cycles for error in cycle['errors']))
    if fighter=='sonya' and not any(c['signature_leg_observed'] for c in cycles):
        errors.append('At least one actual Sonya signature leg action and subsequent native turn in the random fixture')
    if any(a['restore_frame']>=b['store_frame'] for a,b in zip(cycles,cycles[1:])):
        errors.append('Requested morph cycles must not overlap or be reused')
    return dict(passed=not errors,errors=errors,fighter=fighter,form_fields=sum(c['form_fields'] for c in cycles),
                store_frame=cycles[0]['store_frame'],restore_frame=cycles[-1]['restore_frame'],
                morph_cycles=cycles,post_restore_fields=120*count,
                signature_leg_scope='each_observed_leg_cycle_checks_subsequent_turn_at_least_one_leg_cycle_required_for_Sonya',
                later_stock_morph_scope='observed_after_first_restoration_in_same_fixture_not_required_after_every_random_repeat',
                scope=SCOPE,whole_character_integration_complete=False)


def verify(folder,fighter,*,exe_sha=EXE,candidate=None):
    original=(ROOT/'mk2/mk2-maincpu.bin').read_bytes()
    rates=[f'{v:08X}' for v in struct.unpack_from('<17I',original,(0xff8702c0-0xff800000)//8)]
    proof=verify_log((folder/'run.log').read_text(encoding='utf-8-sig'),fighter,rates)
    result=json.loads((folder/'result.json').read_text(encoding='utf-8-sig'))
    errors=proof['errors']
    if hashlib.sha256(original).hexdigest().upper()!='45B3285496DB555EFAF4A3608A4F59845DD47A82E4A0593607E0592F47B36F23':
        errors.append('Exact original native table reference binary')
    if result.get('exit_code')!=0 or result.get('executable_sha256')!=exe_sha or result.get('payload_sha256')!=PAYLOAD or (candidate is not None and result.get('candidate')!=candidate):
        errors.append('Exact successful matched candidate/payload identity')
    before=json.loads((folder/'input_hashes_before.json').read_text(encoding='utf-8-sig'))
    if before!=result.get('input_hashes'):errors.append('Frozen before/after probe inputs')
    build=json.loads((folder/'input_sources/build-info.json').read_text(encoding='utf-8-sig'))
    checks=dict(before,**build['input_hashes'])
    for file,expected in checks.items():
        path=Path(file)
        if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest().upper()!=expected:
            errors.append('Exact current checked input: '+file)
    proof['passed']=not errors
    proof['checked_inputs']=len(checks)
    return proof


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('case',type=Path)
    parser.add_argument('fighter',choices=['kano','sonya']);parser.add_argument('--output',type=Path)
    parser.add_argument('--exe-sha',default=EXE);parser.add_argument('--candidate')
    args=parser.parse_args();proof=verify(args.case,args.fighter,exe_sha=args.exe_sha,candidate=args.candidate)
    if args.output:
        if args.output.exists():raise SystemExit('Refusing to overwrite proof')
        args.output.write_text(json.dumps(proof,indent=2)+'\n')
    print(json.dumps(proof,indent=2));raise SystemExit(0 if proof['passed'] else 1)
