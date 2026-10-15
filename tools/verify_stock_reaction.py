"""Input-only native freeze/lightning contact, owned palettes and control return.

This is not all stock specials, every rendered pixel, audio, or tower acceptance.
"""
import argparse
import hashlib
import json
import re
import struct
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
NAME='diagnostic_v357_native_morph_palette'
EXE='4E71EFACF4837B6D32A3FF92BBE9A28B6D56C2AEFD68E165D35D6D14D95383AD'
PAYLOAD='82FE153FB56B46A6F9D42F493451AC3D59AD61713433714ACA7704E2881F8951'
SCOPE='native_stock_freeze_lightning_hits_owned_palette_RAM_and_post_reaction_walk_jump_punch_both_slots_not_all_projectiles_bitmap_audio_or_full_goal'


def rows(log,prefix,tag):
    return [dict(re.findall(r'(\w+)=([^\s]+)',line)) for line in log.splitlines() if line.startswith(prefix+tag+' ')]


def references(victim):
    stock=(ROOT/'mk2/mk2-maincpu.bin').read_bytes();donor=(ROOT/'mk3/mk3-maincpu.bin').read_bytes()
    if hashlib.sha256(stock).hexdigest().upper()!='45B3285496DB555EFAF4A3608A4F59845DD47A82E4A0593607E0592F47B36F23' or hashlib.sha256(donor).hexdigest().upper()!='1BC7A53A023F15B20F01398F87E38478A27C670DF27EA320E36125D0957EE651':
        raise ValueError('Exact original native/donor palette references required')
    def dword(at):return struct.unpack_from('<I',stock,(at-0xff800000)//8)[0]
    def palette(program,at):
        count=struct.unpack_from('<H',program,at)[0]
        return tuple(v&0x7fff for v in struct.unpack_from(f'<{count}H',program,at+2))
    if victim=='cage':
        normal=dword(dword(0xff906f40)+2*32);blue=dword(0xff9109e0+2*32)
        return palette(stock,(blue-0xff800000)//8),palette(stock,(normal-0xff800000)//8),blue
    descriptor={'kano':0x092bbc,'sonya':0x092cf2}[victim]
    blue={'kano':0xffa66010,'sonya':0xffa643a0}[victim]
    normal=(0,*struct.unpack_from('<64H',donor,descriptor+4))[:64]
    return palette(donor,(blue-0xff800000)//8),tuple(v&0x7fff for v in normal),{'kano':0xfffacd00,'sonya':0xfffad200}[victim]


def verify_log(log,victim,effect,side):
    if victim not in ('kano','sonya','cage') or effect not in ('freeze','shock') or side not in (1,2):raise ValueError('Declared native fixture required')
    errors=[]
    def need(ok,label):
        if not ok:errors.append(label)
    def own(tag):return rows(log,'MK2_STOCK_REACTION_',tag)
    def blue(tag):return rows(log,'MK2_BLUE_',tag)
    def n(row,key):
        try:return int(row.get(key,''))
        except ValueError:return -1
    fields=own('FIELD');matches=own('MATCH');results=own('RESULT');contacts=own('DAMAGE');ready=own('READY')
    id={'kano':17,'sonya':18,'cage':2}[victim];attack=8 if effect=='freeze' else 7
    need(not re.search(r'Fatal error|stack traceback|Lua error|\[LUA ERROR\]|access violation',log,re.I),'No emulator/Lua errors')
    need(not own('ERROR') and len(matches)==len(results)==1,'One actual cold selected match and terminal observer result')
    all_rows=sum((own(tag) for tag in ('MATCH','FIELD','RESULT','INPUT','DAMAGE','READY')),[])
    need(all(r.get('side')==str(side) and r.get('victim')==victim and r.get('effect')==effect and r.get('writes')=='0' and r.get('assistance')=='none' for r in all_rows),'Every observer row retains declared no-assistance context')
    need(len(fields)==1301 and [n(r,'age') for r in fields]==list(range(1301)),'Every field through post-reaction controls')
    if not matches or not fields:return dict(passed=False,errors=errors,scope=SCOPE,whole_character_integration_complete=False)
    match=matches[0];first=n(match,'frame')
    actor,main,attacker,attack_main=[match.get(k) for k in ('actor','main','attacker','attack_main')]
    need(len({actor,main,attacker,attack_main})==4 and all(0x01000000<=int(a or '0',16)<0x01100000 for a in (actor,main,attacker,attack_main)),'Distinct native actors and Main processes')
    need(match.get('id')==str(id) and match.get('attack_id')==str(attack) and match.get('hp1')==match.get('hp2')=='161','Actual original/new starting bodies and full native health')
    need([n(r,'frame') for r in fields]==list(range(first,first+1301)),'Consecutive real frame timeline')
    need(all(r.get('actor')==r.get('published')==actor and r.get('main')==r.get('published_main')==main and r.get('attacker')==attacker and r.get('attack_main')==attack_main and r.get('mode')=='2' and r.get('own_state')==r.get('attack_state')=='1' and r.get('id')==r.get('own_roster')==str(id) and r.get('attack_id')==r.get('attack_roster')==str(attack) and 0<n(r,'hp')<=161 and r.get('attack_hp')=='161' for r in fields),'Both real selected identities and controllers remain published through every contact and recovery')
    expected_blue,expected_normal,record=references(victim)
    def colors(r):return tuple(int(v,16) for v in r.get('colors','').split(',') if v)
    need(all(len(colors(r))==64 and int(r.get('bank','FFFF'),16)<0x8000 for r in fields),'Full actual owned palette bank capture')
    def same(r,expected):return colors(r)[1:64]==expected[1:64]
    blue_fields=sum(same(r,expected_blue) for r in fields)
    need(blue_fields>=10,'Actual owned RGB555 freeze/shock colors equal original source, not queue arguments only')
    need(all(same(r,expected_normal) for r in fields if n(r,'age')>=1100),'Original normal opaque colors restored throughout later controls')
    table=blue('TABLE');queues=blue('QUEUE');lookups=blue('LOOKUP');summary=blue('RESULT')
    need(len(table)==1 and int(table[0].get('record','0'),16)==record,'Own native blue palette record, not a stock proxy')
    need(queues and all(int(r.get('source','0'),16)==record+16 and r.get('count')=='64' for r in queues),'Valid bounded owned native palette copy')
    pc='FF910970' if effect=='freeze' else 'FF8DADA0'
    need(len(lookups)==len(contacts)==4 and all(r.get('pc')==pc for r in lookups),'Four actual original stock reaction lookups and contacts')
    health=161;windows=[]
    for index,contact in enumerate(contacts):
        at=n(contact,'frame');next_at=n(contacts[index+1],'frame') if index+1<len(contacts) else first+1100
        need(contact.get('actor')==actor and contact.get('main')==main and contact.get('pc')=='FF836700' and contact.get('address')==('010602F0' if side==1 else '01060EC0') and n(contact,'old')==health and n(contact,'new')==health-(0 if effect=='freeze' else 22),'Original slot-specific health store and exact stock projectile damage')
        health=n(contact,'new')
        returns=[r for r in ready if at<n(r,'frame')<next_at and r.get('actor')==actor and r.get('main')==main and r.get('pc')=='FF861360']
        need(bool(returns),'Every contact returns through actual owned native ready code')
        if returns:
            end=n(returns[0],'frame')
            active=[r for r in fields if at<=n(r,'frame')<=end+4]
            need(sum(same(r,expected_blue) for r in active)>=3,'Every actual contact displays original blue body colors')
            need(any(same(r,expected_normal) for r in active if n(r,'frame')>=end),'Each contact restores normal palette at native recovery')
            windows.append(dict(contact_frame=at,ready_frame=end))
    # Bind every sampled HP value to actual native stores, including zero-damage freeze.
    health=161;index=0
    for r in fields:
        while index<len(contacts) and n(contacts[index],'frame')<n(r,'frame'):
            health=n(contacts[index],'new');index+=1
        if not any(n(c,'frame')==n(r,'frame') for c in contacts):need(n(r,'hp')==health,'No silent health writes outside original stock ledger')
    byage={n(r,'age'):r for r in fields}
    inputs=own('INPUT');buttons=[(n(r,'age'),r.get('buttons')) for r in inputs]
    expected=[(i,'Right' if side==1 else 'Left') for i in range(1140,1156)]+[(i,'Up') for i in range(1180,1183)]+[(i,'High_Punch') for i in range(1260,1264)]
    need(buttons==expected,'Actual post-reaction walking, jump and punch controls')
    walking=[r for r in fields if 1140<n(r,'age')<=1160]
    need(any(r.get('vx')!='00000000' for r in walking) and abs(n(byage.get(1160,{}),'x')-n(byage.get(1140,{}),'x'))>=20,'Victim walks naturally after stock reactions')
    need(any(n(r,'y')<n(r,'floor') and r.get('vy')!='00000000' for r in fields if 1180<n(r,'age')<1240),'Victim performs actual airborne jump after thaw/shock')
    need(any(r.get('action')=='0101' for r in fields if 1260<n(r,'age')<1290),'Victim punches afterward, not merely receives input')
    need(all(r.get('vx')==r.get('vy')==r.get('trail')=='00000000' and n(r,'y')==n(r,'floor') for r in fields if n(r,'age')>=1290),'Clean grounded final control, no persistent child/velocity')
    need(len(summary)==1 and summary[0].get('pass')=='true' and summary[0].get('errors')==summary[0].get('bad_queues')=='0','Native blue observer checks also pass')
    need('MK2KS_STABILITY stalled_frames=0 trap_frames=0' in log and 'MK2KS_DISPLAY_RESULT pass=true ' in log,'Current display and stability observers pass')
    if victim!='cage':
        need('MK2KS_EXIT_RESULT pass=true ' in log and 'MK2KS_HUD_SHADOW_RESULT pass=true ' in log,'Current added-character selection and name-shadow observers pass')
    else:
        # The inherited custom-name observer reports false for stock characters
        # because it performs zero custom-name checks, not because Cage is broken.
        exits=rows(log,'MK2KS_','EXIT_RESULT');shadows=rows(log,'MK2KS_','HUD_SHADOW_RESULT')
        need(len(exits)==len(shadows)==1 and exits[0].get('fighter')=='cage' and all(exits[0].get(k)=='0' for k in ('leaks','identity_errors','name_checks','name_errors')) and shadows[0].get('checks')==shadows[0].get('errors')=='0','Stock control has no leaks/identity errors; custom-name checks are explicitly inapplicable')
    need(n(results[0],'match')==first and results[0].get('fields')=='1301','Terminal count matches actual full timeline')
    return dict(passed=not errors,errors=sorted(set(errors)),victim=victim,effect=effect,side=side,fields=len(fields),contacts=len(contacts),blue_palette_fields=blue_fields,contact_windows=windows,stock_control_custom_name_checks='inapplicable_zero_checks' if victim=='cage' else 'required',scope=SCOPE,whole_character_integration_complete=False)


def verify(folder,victim,effect,side):
    proof=verify_log((folder/'run.log').read_text(encoding='utf-8-sig'),victim,effect,side)
    meta=json.loads((folder/'result.json').read_text(encoding='utf-8-sig'))
    errors=proof['errors'];before=json.loads((folder/'input_hashes_before.json').read_text(encoding='utf-8-sig'))
    if (meta.get('candidate'),meta.get('executable_sha256'),meta.get('payload_sha256'),meta.get('exit_code'),meta.get('victim'),meta.get('effect'),meta.get('side'),meta.get('assistance'))!=(NAME,EXE,PAYLOAD,0,victim,effect,side,'none'):errors.append('Exact matched current runtime fixture identity')
    if before!=meta.get('input_hashes'):errors.append('Unchanged before/after observed inputs')
    build=json.loads((folder/'input_sources/build-info.json').read_text(encoding='utf-8-sig'))
    checks=dict(before,**build['input_hashes'])
    for file,expected in checks.items():
        path=Path(file)
        if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest().upper()!=expected:errors.append('Exact checked input: '+file)
    for name in ('mk2ks_stock_reaction_probe.lua','mk2ks_blue_palette_test.lua','mk2ks_native_shang_morph.lua'):
        if re.search(r':write_|\.value\s*=(?!=)|load_state|loadstate',(folder/'input_sources'/name).read_text()):errors.append('No guest-state assistance in native probe: '+name)
    proof.update(passed=not errors,checked_inputs=len(checks))
    return proof


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('case',type=Path);parser.add_argument('victim');parser.add_argument('effect');parser.add_argument('side',type=int);parser.add_argument('--output',type=Path)
    args=parser.parse_args();proof=verify(args.case,args.victim,args.effect,args.side)
    if args.output:
        if args.output.exists():raise SystemExit('Refusing to overwrite evidence')
        args.output.write_text(json.dumps(proof,indent=2)+'\n')
    print(json.dumps(proof,indent=2));raise SystemExit(0 if proof['passed'] else 1)
