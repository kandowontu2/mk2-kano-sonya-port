"""Input-only native human morph commands. Not a full game/release/pixel gate."""
import argparse
import hashlib
import json
import re
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
CANDIDATE='diagnostic_v3172_native_morph_shadow'
EXE='1835D8E05A25E193D0934560115A8C77B2F15C92B8BA3FF1BA06AA0C7D59BD24'
PAYLOAD='ED9023949F73BD719F8BC688C69230C68239D7CC140F814C1A4E54A5BF561BC3'
SCOPE='input_only_both_human_slots_native_morph_inputs_eligibility_owned_projectile_restore_controls_and_three_stock_fallbacks_not_full_game_pixels_audio_or_release'
PREFIX='MK2_HUMAN_SHANG_'
POSITIVE={'native','block2','block_first','lp_first'}
STOCK={'stock_lp':(2,'FF964BD0','FF86E360'),
       'stock_lk':(3,'FF964AD0','FF86E380'),
       'stock_block':(4,'FF964770','FF86E3A0')}
NEGATIVE={'kano':{'wrong_button','reversed','expired','extra_button','airborne'},
          'sonya':{'no_down','no_lp','no_block','extra_button','airborne'}}


def rows(log):
    return [(line[len(PREFIX):].split()[0],dict(re.findall(r'(\w+)=([^\s]+)',line)))
            for line in log.splitlines() if line.startswith(PREFIX)]


def expected_inputs(target,side,profile):
    """Independent physical command specification, including rejection controls."""
    back,forward=('Left','Right') if side==1 else ('Right','Left')
    result={}
    def add(ages,*buttons):
        for age in ages:result.setdefault(age,[]).extend(buttons)
    if profile=='airborne':add(range(90,93),'Up')
    if profile=='stock_lp':
        add([100,101,104,105],back);add([108,109],'Down','Low_Punch')
    elif profile=='stock_lk':
        add([100,101,104,105],'Down');add([108,109],'Low_Kick')
    elif profile=='stock_block':add([100,101,104,105,108,109],'Block')
    elif target=='kano':
        direction=forward if profile=='reversed' else back
        add([100,101],direction);add([104,105],'Down')
        last=158 if profile=='expired' else 108
        add([last,last+1],direction,'High_Kick' if profile=='wrong_button' else 'Low_Kick')
        if profile=='extra_button':add([last,last+1],'Block')
    else:
        for age in range(100,108):
            if profile!='no_down':add([age],'Down')
            if profile!='no_lp' and not (profile=='block_first' and age<103):add([age],'Low_Punch')
            if profile!='no_block' and not (profile=='lp_first' and age<103):add([age],'Block_2' if profile=='block2' else 'Block')
            if profile=='extra_button':add([age],'High_Punch')
    return {age:','.join(buttons) for age,buttons in result.items()}


def verify_log(log,target,side,profile):
    if target not in NEGATIVE or side not in (1,2) or profile not in POSITIVE|STOCK.keys()|NEGATIVE[target]:
        raise ValueError('Explicit valid physical case required')
    if target=='kano' and profile in POSITIVE-{'native'}:raise ValueError('Sonya chord variants only')
    errors=[]
    def need(ok,message):
        if not ok:errors.append(message)
    records=rows(log)
    def tagged(tag):return [r for t,r in records if t==tag]
    def num(r,k,base=10):
        try:return int(r.get(k,''),base)
        except ValueError:return -1
    def frame(r):return num(r,'frame')
    need(not re.search(r'Fatal error|\[LUA ERROR\]|stack traceback|access violation|exception at',log,re.I),'No runtime/observer error')
    need(all(r.get('writes')=='0' and r.get('side')==str(side) and r.get('target')==target and r.get('profile')==profile for _,r in records),'Consistent read-only case provenance')
    need(not tagged('ERROR'),'No observer-detected error')
    rom=tagged('ROM');css=tagged('CSS');matches=tagged('MATCH');results=tagged('RESULT')
    need(len(rom)==1 and (rom[0].get('lp'),rom[0].get('block'),rom[0].get('lk'))==('FFFC9000','FFFC9100','FFFC8800'),'Actual extended native Shang event-table bindings')
    need(len(css)==len(matches)==len(results)==1,'Single real selection, match and terminal record')
    fields=tagged('FIELD')
    need([num(r,'age') for r in fields]==list(range(1001)),'All 1001 consecutive gameplay fields')
    if len(matches)!=1 or not fields:
        return dict(passed=False,errors=errors,target=target,side=side,profile=profile,scope=SCOPE,whole_character_integration_complete=False)
    match=matches[0];owner=(match.get('actor'),match.get('main'));start_match=frame(match)
    def owned(r):return (r.get('actor'),r.get('main'))==owner
    need(all(0x01000000<=num(match,k,16)<0x01100000 for k in ('actor','main')),'Valid actual published actor/process')
    need(all(match.get(k)==v for k,v in {'own_state':'1','own_roster':'6','own_id':'6','other_state':'1','other_roster':'17','hp1':'161','hp2':'161'}.items()),'Full-health real two-human Shang/Kano start')
    need(css[0].get('mode')=='4' and frame(css[0])<start_match if css else False,'Real select precedes established match')
    need([frame(r) for r in fields]==list(range(start_match,start_match+1001)),'No gaps or duplicate gameplay fields')
    need(all(owned(r) and r.get('mode')=='2' and r.get('state')=='1' and r.get('roster')=='6' and 0<num(r,'hp1')<=161 and 0<num(r,'hp2')<=161 and 0<num(r,'floor')<200 and num(r,'pose',16)>=0xfe800000 for r in fields),'Live human controller, roster, pose, floor and health throughout')
    inputs=[r for r in tagged('INPUT') if 90<=num(r,'age')<=170]
    need({num(r,'age'):r.get('buttons') for r in inputs}==expected_inputs(target,side,profile) and len(inputs)==len(expected_inputs(target,side,profile)),'Exact physical command or deliberate invalid variant')
    need(all(r.get('actor')==owner[0] and r.get('id')=='6' and r.get('facing')==('right' if side==1 else 'left') and frame(r)==start_match+num(r,'age') for r in inputs),'Correct controller, facing and original identity at input')
    positive=profile in POSITIVE or profile in STOCK
    identity=STOCK[profile][0] if profile in STOCK else 17 if target=='kano' else 18
    root=STOCK[profile][1] if profile in STOCK else 'FF0C1800' if target=='kano' else 'FF0C1A00'
    entry=STOCK[profile][2] if profile in STOCK else 'FFFC8E00' if target=='kano' else 'FFFC8F00'
    choices=tagged('CHOICE');stores=tagged('STORE')
    first=last=-1;form_fields=0
    if positive:
        need(len(choices)==1 and len(stores)==2,'One native forward choice and two native ID stores')
        if len(choices)==1 and len(stores)==2:
            choice=choices[0];form,restore=stores;first,last=frame(form),frame(restore)
            need(owned(choice) and choice.get('id')==str(identity) and choice.get('pc')=='FF86E490' and start_match+100<=frame(choice)<=start_match+116,'Actual requested morph from native player command')
            need(any(r.get('actor')==owner[0] and 0x01000000<=num(r,'event',16)<0x01100000 and r.get('entry')==entry and r.get('pc')=='FF877200' and frame(r)==frame(choice) for r in tagged('GATE')),'Stock airborne/busy/scheduler gate selects actual target stub')
            need(owned(form) and form.get('old')=='6' and form.get('id')==str(identity) and form.get('pc')=='FF86E670' and form.get('a9')==f'{identity:08X}','Original native forward ID store, not an alias')
            need(owned(restore) and restore.get('old')==str(identity) and restore.get('id')=='6' and restore.get('pc')=='FFA16700' and restore.get('a0')=='00000006','Original native reverse ID store')
            need(frame(choice)<first and 512<=last-first<=900,'Finite native timed morph and restoration')
            lookup=tagged('LOOKUP');reverse=tagged('RESTORE_LOOKUP');begin=tagged('RESTORE_BEGIN')
            need(len(lookup)==len(reverse)==len(begin)==1 and owned(lookup[0]) and lookup[0].get('root')==root and lookup[0].get('pc')=='FF86E590' and frame(lookup[0])==frame(choice),'Own forward sequence lookup')
            need(len(reverse)==len(begin)==1 and owned(reverse[0]) and owned(begin[0]) and reverse[0].get('root')==root and reverse[0].get('pc')=='FFA16450' and begin[0].get('id')==str(identity) and begin[0].get('pc')=='FFA16310' and frame(begin[0])==frame(reverse[0]) and first+512==frame(begin[0])<last,'Native timed reverse entry and correct sequence')
            for r in fields:
                expected=identity if first<frame(r)<=last else 6
                need(r.get('id')==str(expected),'Character identity agrees with actual native store boundaries')
            form_fields=sum(first<frame(r)<=last for r in fields)
            if profile not in STOCK:
                groups=['FF0C4000','FF0C4060','FF0C40C0'] if target=='kano' else ['FF0C4120','FF0C4180','FF0C41E0']
                actual=tagged('GROUP');palette='FF0C0800' if target=='kano' else 'FF0C1000'
                need([r.get('group') for r in actual]==groups+groups[::-1] and all(owned(r) and r.get('pc')=='FF8387A0' for r in actual),'All three original composite groups forward and backward')
                need([frame(r) for r in actual]==[first-12,first-8,first-4,last-12,last-8,last-4],'Native four-field transition holds')
                pals=tagged('PALETTE')
                need(len(pals)==2 and all(owned(r) and r.get('palette')==palette and r.get('pc')=='FF907520' for r in pals),'Own transition palette in both directions')
                need(all(r.get('floor')==('82' if target=='kano' else '81') for r in fields if first<frame(r)<=last),'Canonical added-character floor throughout the form')
                action=tagged('PROJECTILE_ACTION');create=tagged('PROJECTILE_CREATE')
                need(len(action)==len(create)==1 and owned(action[0]) and owned(create[0]) and action[0].get('id')==create[0].get('id')==str(identity) and action[0].get('entry')==('FFFFB000' if target=='kano' else 'FFFFB400') and create[0].get('entry')==('FFFC5800' if target=='kano' else 'FFFC5C00') and first<frame(action[0])<frame(create[0])<last,'Own native projectile action and child creation while morphed')
                need(sum(r.get('action')=='0004' for r in fields if first<frame(r)<=last)==(25 if target=='kano' else 15) and sum(r.get('action')=='0604' for r in fields if first<frame(r)<=last)==(24 if target=='kano' else 35),'Complete own projectile body release/recovery holds')
                opponent='hp2' if side==1 else 'hp1'
                need(any(r.get(opponent)=='155' for r in fields if first<frame(r)<last),'Actual projectile blocked for six points without health assistance')
            else:
                need(not tagged('GROUP') and not tagged('PALETTE'),'Stock fallback does not use added-character transition assets')
    else:
        need(not choices and not stores and not tagged('LOOKUP') and not tagged('RESTORE_BEGIN') and not tagged('RESTORE_LOOKUP'),'Invalid commands cannot morph or alter identity')
        need(all(r.get('id')=='6' for r in fields),'Rejected command keeps actual Shang body')
        if profile=='airborne':
            need(any(100<=num(r,'age')<=110 and num(r,'y')<num(r,'floor') and r.get('vy')!='00000000' for r in fields),'Airborne rejection was genuinely tested off the floor')
    after=[r for r in fields if num(r,'age')>=800]
    need(all(r.get('id')=='6' and r.get('floor')=='87' and r.get('trail')=='00000000' for r in after),'Shang restored with original floor and no attached effect')
    need(any(820<=num(r,'age')<850 and r.get('vx')!='00000000' for r in after) and any(850<=num(r,'age')<900 and num(r,'y')<87 and r.get('action')=='030B' for r in after) and any(920<=num(r,'age')<950 and r.get('action')=='0101' for r in after),'Post-command walk, jump and punch remain responsive')
    need(len(results)==1 and results[0].get('forms')==results[0].get('restores')==('1' if positive else '0') and results[0].get('errors')=='0' and num(results[0],'match')==start_match and frame(results[0])==start_match+1000,'Terminal counts agree with independently checked native trace')
    return dict(passed=not errors,errors=sorted(set(errors)),target=target,side=side,profile=profile,
                form_fields=form_fields,gameplay_fields=len(fields),scope=SCOPE,whole_character_integration_complete=False)


def verify(folder,target,side,profile,*,candidate=CANDIDATE,exe_sha=EXE):
    proof=verify_log((folder/'run.log').read_text(encoding='utf-8-sig'),target,side,profile)
    errors=proof['errors'];result=json.loads((folder/'result.json').read_text(encoding='utf-8-sig'))
    before=json.loads((folder/'input_hashes_before.json').read_text(encoding='utf-8-sig'))
    if (result.get('exit_code'),result.get('candidate'),result.get('executable_sha256'),result.get('payload_sha256'),result.get('target'),result.get('side'),result.get('profile'))!=(0,candidate,exe_sha,PAYLOAD,target,side,profile):errors.append('Explicit matched build and case identity')
    if before!=result.get('input_hashes'):errors.append('Frozen before/after launch inputs')
    build=json.loads((folder/'input_sources'/candidate/'build-info.json').read_text(encoding='utf-8-sig'))
    if (build.get('name'),build.get('executable_sha256'),build.get('payload_sha256'))!=(candidate,exe_sha,PAYLOAD):errors.append('Exact expected build record')
    checks=dict(build['input_hashes'])
    for file,expected in before.items():
        source=Path(file)
        # A later input-driver improvement cannot retroactively change this case.
        if source.suffix in ('.lua','.ps1','.json'):source=folder/'input_sources'/source.relative_to(ROOT)
        checks[str(source)]=expected
    for file,expected in checks.items():
        source=Path(file)
        if not source.is_file() or hashlib.sha256(source.read_bytes()).hexdigest().upper()!=expected:errors.append('Checked input: '+file)
    observer=(folder/'input_sources/mk2ks_human_shang_probe.lua').read_text()
    if re.search(r':write_|\.value\s*=(?!=)|load_state|loadstate',observer):errors.append('Observer cannot write guest state or load a state')
    proof['checked_inputs']=len(checks);proof['passed']=not errors
    return proof


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('case',type=Path);parser.add_argument('target',choices=['kano','sonya'])
    parser.add_argument('side',type=int,choices=[1,2]);parser.add_argument('profile');parser.add_argument('--output',type=Path)
    parser.add_argument('--candidate',default=CANDIDATE);parser.add_argument('--exe-sha',default=EXE)
    args=parser.parse_args();proof=verify(args.case,args.target,args.side,args.profile,candidate=args.candidate,exe_sha=args.exe_sha)
    if args.output:
        if args.output.exists():raise SystemExit('Refusing to overwrite proof')
        args.output.write_text(json.dumps(proof,indent=2)+'\n')
    print(json.dumps(proof,indent=2));raise SystemExit(0 if proof['passed'] else 1)
