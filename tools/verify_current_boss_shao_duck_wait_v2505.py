"""Independent bounded native campaign proof; incomplete towers never pass clear."""
import argparse
import hashlib
import json
import re
import struct
from pathlib import Path
from verify_p2_campaign import expected_orders
import verify_ball_register_source_v1837 as current_source
import verify_current_interrupt_v1870 as current_launch
NAME=current_source.NAME

def matched(folder,pins):
    result=json.loads((folder/'result.json').read_text(encoding='utf-8-sig'))
    build=json.loads((ROOT/NAME/'build-info.json').read_text(encoding='utf-8-sig'))
    before=json.loads((folder/'input_hashes_before.json').read_text(encoding='utf-8-sig'))
    assert result['candidate']==NAME and result['executable_sha256']==build['executable_sha256']
    assert result['payload_sha256']==build['payload_sha256']and before==result['input_hashes']
    assert result['exit_code']==0 and not result['cheats_enabled']and result['assistance']=='none'
    assert all(before.get(p)==h for p,h in build['input_hashes'].items())
    for p,h in before.items():
        assert current_launch.sha(p)==h,'Changed current campaign input '+p;pins[p]=h
        if Path(p).suffix in('.json','.lua','.ps1'):
            frozen=folder/'input_sources'/Path(p).name
            assert current_launch.sha(frozen)==h,'Changed frozen campaign input';pins[str(frozen)]=h
        if Path(p).suffix=='.lua':
            assert not re.search(r'write_u\d+|:write_|load_?state|\.value\s*=(?!=)',Path(p).read_text())
    pins.update(current_launch.source_pins())
    choices=list((folder/'input_sources').glob('run_current_boss_*v*.ps1'))
    assert len(choices)==1 and choices[0].name=='run_current_boss_shao_duck_wait_v2495.ps1','One exact current physical launcher'
    runner=choices[0].read_text().rstrip()+'\n'
    original=ROOT/'tools/run_current_boss_shao_crouch_exit_v2475.ps1'
    assert current_launch.sha(original)=='FE2B9F90EB775512CB8685B8319B782B542B6B9E97B977E3B9D52A59B030175C'
    restored=runner.replace('mk2ks_natural_campaign_boss_shao_duck_wait_v2494','mk2ks_natural_campaign_boss_shao_crouch_exit_v2461').replace('shao_duck_wait','shao_crouch_exit_escape')
    assert restored==original.read_text().rstrip()+'\n','Only declared stage16 physical driver and policy labels differ; entire launcher exact'
    pins[str(original)]=current_launch.sha(original)
    assert '-nocheat'in runner and '-noautoframeskip -frameskip 0'in runner



ROOT = Path(__file__).resolve().parents[1]
HEX = {'owner','a1','cpu_flags','cpu_body','human_pose','cpu_pose','human_vy','cpu_vy','hardware0','schedule','actor','main','human_actor','human_main','cpu_actor','cpu_main','entry','pc','at','a0','a9','a8','a13','mask','flags','body'}


def drawing_scope(fields, expected_side=None, expected_fighter=None):
    pairs=re.findall(r'(?:^|\s)(human_slot|fighter|writes|assistance)=(\S+)',fields)
    scope=dict(pairs)
    if len(pairs)!=4 or set(scope)!={'human_slot','fighter','writes','assistance'} or \
       scope.get('writes')!='0' or scope.get('assistance')!='none' or \
       scope.get('human_slot')not in('1','2') or scope.get('fighter')not in('kano','sonya') or \
       (expected_side is not None and scope['human_slot']!=str(expected_side)) or \
       (expected_fighter is not None and scope['fighter']!=expected_fighter):
        raise ValueError('Invalid actual drawing row scope: '+repr(scope))
    return scope


def parse(text, expected_side=None, expected_fighter=None):
    records=[]
    for match in re.finditer(r'^MK2_NAT_CAMPAIGN_(\w+) (.*)$',text,re.M):
        # Drawing rows are separately checked in full by the native raster/
        # cache/row-stream verifier. Do not retain millions of irrelevant
        # drawing dictionaries in the campaign-state proof; still validate
        # their declared unassisted physical scope against every actual line.
        if match[1].startswith(('FLOOR_','SHADOW_')):
            drawing_scope(match[2], expected_side, expected_fighter)
            continue
        row=dict(re.findall(r'(\w+)=([^\s]+)',match[2]))
        row.update(tag=match[1], event=match.start())
        for key,value in tuple(row.items()):
            if key in HEX and not (key in('flags','body')and ','in str(value)): row[key]=int(value,16)
            elif re.fullmatch(r'-?\d+',str(value)): row[key]=int(value)
        records.append(row)
    return records


def digest(path):
    h=hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda: stream.read(1024*1024),b''): h.update(block)
    return h.hexdigest().upper()


def restore_boss_observation_window(text):
    original=ROOT/'mk2ks_natural_campaign_floor_v1566.lua'
    assert digest(original)=='2D3880B339A6D5F7302E3D25B57F2C52AE0ACA857220908165EF96D2AD9C0C38'
    marker='local floor_origin,floor_pending=nil,nil\n-- Earlier read-only observation for the actual native Kintaro stage only.\n-- Gameplay controls, schedules, health, CPU and all other arena windows stay unchanged.\nlocal function floor_min_age()return p:read_u16(0x01061b30)==15 and 0 or 208 end'
    assert text.count(marker)==1
    restored=text.replace(marker,'local floor_origin,floor_pending=nil,nil')
    restored=restored.replace('frame-floor_origin<floor_min_age()','frame-floor_origin<208').replace('age<floor_min_age()','age<208').replace('frame-floor_origin>=(floor_min_age()==0 and 8 or 216)','frame-floor_origin>=216')
    assert restored==original.read_text(),'Only read-only boss capture window differs; all controls byte-exact'
    return restored

def restore_boss_input_policy(text):
    baseline=ROOT/'mk2ks_natural_campaign_probe_v850.lua'
    assert digest(baseline)=='EC7ADC60ABA59E44EA26E2AB403EBA03C4ADB742D7059811EF8CCEA755E2282D'
    changed=ROOT/'mk2ks_natural_campaign_boss_tactics_v1735.lua'
    assert digest(changed)=='5D9FEB182D5E0DD9E9A5045231869B26F4F0B4C58295722C279F2EA71732FE00'
    original=baseline.read_text()
    first=original.index("   elseif strategy=='zoning' and other.roster==12 then")
    last=original.index("   elseif strategy=='zoning' then",first+1)
    begin='   -- BEGIN actual-input boss tactics v1735; no guest/CPU/difficulty writes.\n'
    end='   -- END actual-input boss tactics v1735.\n'
    assert text.count(begin)==text.count(end)==1
    start=text.index(begin);stop=text.index(end,start)+len(end)
    restored=text[:start]+original[first:last]+text[stop:]
    assert restored==original,'Only actual human boss-button decisions differ; selection, health/win/ending observers and all ordinary controls exact'
    return restored

def restore_boss_evasion_policy(text):
    baseline=ROOT/'mk2ks_natural_campaign_probe_v850.lua'
    assert digest(baseline)=='EC7ADC60ABA59E44EA26E2AB403EBA03C4ADB742D7059811EF8CCEA755E2282D'
    assert digest(ROOT/'mk2ks_natural_campaign_boss_evasion_v1740.lua')=='4DCA2E6A3EE93A11E08F49B6EE79AEE47877077BDA178FBF2DA4AC8A6AAA6CBD'
    original=baseline.read_text()
    text=text.replace('\nlocal boss_escape_direction=nil -- v1740 physical evasion state only','',1)
    text=text.replace("   if (leg_tactic or strategy=='lowkick'or strategy=='throw') and other.roster~=12 and other.roster~=13 then","   if leg_tactic or strategy=='lowkick'or strategy=='throw'then",1)
    first=original.index("   elseif strategy=='zoning' and other.roster==12 then")
    last=original.index("   elseif strategy=='zoning' then",first+1)
    begin='   -- BEGIN actual-input boss tactics v1740; no guest/CPU/difficulty writes.\n'
    end='   -- END actual-input boss tactics v1740.\n'
    assert text.count(begin)==text.count(end)==1
    start=text.index(begin);stop=text.index(end,start)+len(end)
    restored=text[:start]+original[first:last]+text[stop:]
    assert restored==original,'Only boss physical human input decisions differ; all ordinary controls and native progression observers exact'
    return restored

def restore_boss_timing_policy(text):
    baseline=ROOT/'mk2ks_natural_campaign_boss_evasion_v1740.lua'
    assert digest(baseline)=='4DCA2E6A3EE93A11E08F49B6EE79AEE47877077BDA178FBF2DA4AC8A6AAA6CBD'
    old=baseline.read_text()
    start_marker='   -- BEGIN actual-input boss timing v2056; physical buttons only.\n'
    stop_marker='   -- END actual-input boss timing v2056.\n'
    old_start='   -- BEGIN actual-input boss tactics v1740; no guest/CPU/difficulty writes.\n'
    old_stop='   -- END actual-input boss tactics v1740.\n'
    assert text.count(start_marker)==text.count(stop_marker)==1
    a=text.index(start_marker);b=text.index(stop_marker,a)+len(stop_marker)
    c=old.index(old_start);d=old.index(old_stop,c)+len(old_stop)
    restored=text[:a]+old[c:d]+text[b:]
    declaration="local boss_policy=os.getenv('MK2KS_BOSS_PHYSICAL_POLICY')or'projectile'\nassert(boss_policy=='projectile'or boss_policy=='air_counter','Physical boss input policy only')\nlocal boss_last_jump,boss_jump_direction=-1000,nil -- v2056 actual human input timing"
    assert restored.count(declaration)==1
    restored=restored.replace(declaration,'local boss_escape_direction=nil -- v1740 physical evasion state only',1)
    assert restored==old,'Only boss human-button timing changed; all ordinary selection/combat/progression/ending observers remain byte-exact'
    return restore_boss_evasion_policy(restored)

def restore_boss_anticipation_policy(text):
    baseline=ROOT/'mk2ks_natural_campaign_boss_timing_v2056.lua'
    old=baseline.read_text()
    assert digest(baseline)=='A9BBBCBD4A6F5449A0A2D659BF1BB1A3B53EDDF50B4CF71E679AA92585CB8F1A'
    begin='   -- BEGIN actual-input boss anticipation v2112; physical buttons and read-only observation only.\n'
    end='   -- END actual-input boss anticipation v2112.\n'
    old_begin='   -- BEGIN actual-input boss timing v2056; physical buttons only.\n'
    old_end='   -- END actual-input boss timing v2056.\n'
    assert text.count(begin)==text.count(end)==1
    a=text.index(begin);b=text.index(end,a)+len(end)
    c=old.index(old_begin);d=old.index(old_end,c)+len(old_end)
    restored=text[:a]+old[c:d]+text[b:]
    declaration="local boss_policy=os.getenv('MK2KS_BOSS_PHYSICAL_POLICY')or'anticipate'\nassert(boss_policy=='anticipate'or boss_policy=='range_guard','Physical boss input policy only')\nlocal boss_last_jump,boss_jump_direction,boss_escape_origin=-1000,nil,nil -- v2112 physical attempt timing\nlocal boss_guard_until=-1000\nlocal boss_previous_airborne=false"
    previous="local boss_policy=os.getenv('MK2KS_BOSS_PHYSICAL_POLICY')or'projectile'\nassert(boss_policy=='projectile'or boss_policy=='air_counter','Physical boss input policy only')\nlocal boss_last_jump,boss_jump_direction=-1000,nil -- v2056 actual human input timing"
    assert restored.count(declaration)==1
    restored=restored.replace(declaration,previous,1)
    dump="  local raw=p:read_range(0xff800000,0xffffffff,8,8);assert(#raw==1048576)\n  local file=assert(io.open(assert(os.getenv('MK2KS_CAMPAIGN_OUT'))..'/guest_maincpu.bin','wb'));file:write(raw);file:close()\n"
    assert restored.count(dump)==1
    restored=restored.replace(dump,'',1)
    assert restored==old,'Only boss physical policy and read-only guest capture differ'
    return restore_boss_timing_policy(restored)

def restore_boss_held_response_policy(text):
    baseline=ROOT/'mk2ks_natural_campaign_boss_anticipation_v2112.lua'
    old=baseline.read_text()
    begin='   -- BEGIN actual-input boss held-input response v2121; physical buttons and read-only observation only.\n'
    end='   -- END actual-input boss held-input response v2121.\n'
    old_begin='   -- BEGIN actual-input boss anticipation v2112; physical buttons and read-only observation only.\n'
    old_end='   -- END actual-input boss anticipation v2112.\n'
    assert text.count(begin)==text.count(end)==1
    a=text.index(begin);b=text.index(end,a)+len(end)
    c=old.index(old_begin);d=old.index(old_end,c)+len(old_end)
    restored=text[:a]+old[c:d]+text[b:]
    assert restored==old,'Only actual held boss human-button decisions differ; entire ordinary campaign and read-only observers byte-exact'
    return restore_boss_anticipation_policy(restored)


def restore_boss_ground_evasion_policy(text):
    baseline=ROOT/'mk2ks_natural_campaign_boss_held_response_v2121.lua'
    old=baseline.read_text()
    begin='   -- BEGIN actual-input boss ground-evasion response v2130; physical buttons and read-only observation only.\n'
    end='   -- END actual-input boss ground-evasion response v2130.\n'
    old_begin='   -- BEGIN actual-input boss held-input response v2121; physical buttons and read-only observation only.\n'
    old_end='   -- END actual-input boss held-input response v2121.\n'
    assert text.count(begin)==text.count(end)==1
    a=text.index(begin);b=text.index(end,a)+len(end)
    c=old.index(old_begin);d=old.index(old_end,c)+len(old_end)
    restored=text[:a]+old[c:d]+text[b:]
    declaration="local boss_walk_direction,boss_walk_last_x,boss_walk_still=nil,nil,0\nlocal boss_walk_counter=-1000\nlocal boss_live_begin,boss_last_field=nil,nil\n"
    assert restored.count(declaration)==1
    restored=restored.replace(declaration,'',1)
    restored=restored.replace("or'walk_stomp'","or'anticipate'",1)
    restored=restored.replace("assert(boss_policy=='walk_stomp'or boss_policy=='walk_uppercut','Physical boss input policy only')","assert(boss_policy=='anticipate'or boss_policy=='range_guard','Physical boss input policy only')",1)
    assert restored==old,'Only grounded boss physical-button decisions differ; original campaign, selection, guest dump and native progression observers byte-exact'
    return restore_boss_held_response_policy(restored)


def restore_boss_delayed_counter_policy(text):
    baseline=ROOT/'mk2ks_natural_campaign_boss_ground_evasion_v2130.lua'
    old=baseline.read_text()
    begin='   -- BEGIN actual-input boss delayed-counter response v2140; physical buttons and read-only observation only.\n'
    end='   -- END actual-input boss delayed-counter response v2140.\n'
    old_begin='   -- BEGIN actual-input boss ground-evasion response v2130; physical buttons and read-only observation only.\n'
    old_end='   -- END actual-input boss ground-evasion response v2130.\n'
    assert text.count(begin)==text.count(end)==1
    a=text.index(begin);b=text.index(end,a)+len(end)
    c=old.index(old_begin);d=old.index(old_end,c)+len(old_end)
    restored=text[:a]+old[c:d]+text[b:]
    declaration='local boss_action_taps={}\n'
    assert restored.count(declaration)==1
    restored=restored.replace(declaration,'',1)
    assert restored==old,'Only boss physical counter timing and read-only own action tap differ; entire ordinary campaign and earlier native observers exact'
    return restore_boss_ground_evasion_policy(restored)


def restore_boss_clean_counter_policy(text):
    baseline=ROOT/'mk2ks_natural_campaign_boss_delayed_counter_v2140.lua'
    assert digest(baseline)=='6CE888B279C45274AA9B84263C5BDEEFE8B4B4FBD8B25B3E6129BAD23DBBDCAA'
    old=baseline.read_text()
    begin='   -- BEGIN actual-input boss clean-uppercut response v2174; physical buttons and read-only observation only.\n'
    end='   -- END actual-input boss clean-uppercut response v2174.\n'
    old_begin='   -- BEGIN actual-input boss delayed-counter response v2140; physical buttons and read-only observation only.\n'
    old_end='   -- END actual-input boss delayed-counter response v2140.\n'
    assert text.count(begin)==text.count(end)==1
    a=text.index(begin);b=text.index(end,a)+len(end)
    c=old.index(old_begin);d=old.index(old_end,c)+len(old_end)
    restored=text[:a]+old[c:d]+text[b:]
    restored=restored.replace("or'clean_counter'","or'walk_stomp'",1)
    restored=restored.replace("assert(boss_policy=='clean_counter'or boss_policy=='held_crouch','Physical boss input policy only')","assert(boss_policy=='walk_stomp'or boss_policy=='walk_uppercut','Physical boss input policy only')",1)
    assert restored.rstrip()+'\n'==old.rstrip()+'\n','Only boss physical buttons differ; original campaign/selection/health/win/ending observers exact, EOF normalized'
    return restore_boss_delayed_counter_policy(old)

def restore_boss_guarded_counter_policy(text):
    baseline=ROOT/'mk2ks_natural_campaign_boss_clean_uppercut_v2174.lua'
    assert digest(baseline)=='800D8D7E195897AC3EB4FC83CF9E8DA3D03C213F86D6C0399DBEA55286E21CB3'
    old=baseline.read_text()
    begin='   -- BEGIN actual-input boss clean-uppercut response v2192; physical buttons and read-only observation only.\n'
    end='   -- END actual-input boss clean-uppercut response v2192.\n'
    old_begin=begin.replace('v2192','v2174');old_end=end.replace('v2192','v2174')
    assert text.count(begin)==text.count(end)==1
    a=text.index(begin);b=text.index(end,a)+len(end)
    c=old.index(old_begin);d=old.index(old_end,c)+len(old_end)
    restored=text[:a]+old[c:d]+text[b:]
    restored=restored.replace("or'guarded_counter'","or'clean_counter'",1)
    restored=restored.replace("assert(boss_policy=='guarded_counter'or boss_policy=='guarded_frequent','Physical boss input policy only')","assert(boss_policy=='clean_counter'or boss_policy=='held_crouch','Physical boss input policy only')",1)
    assert restored.rstrip()+'\n'==old.rstrip()+'\n','Only physical boss guard/release timing differs; full ordinary campaign and every read-only observer exact'
    return restore_boss_clean_counter_policy(old)

def restore_boss_guarded_commit_policy(text):
    baseline=ROOT/'mk2ks_natural_campaign_boss_guarded_counter_v2192.lua'
    assert digest(baseline)=='0C89CC143EFA39130CE281B180ED2125400352B1F902B41AD1B56467870DF839'
    old=baseline.read_text()
    begin='   -- BEGIN actual-input boss clean-uppercut response v2200; physical buttons and read-only observation only.\n'
    end='   -- END actual-input boss clean-uppercut response v2200.\n'
    old_begin=begin.replace('v2200','v2192');old_end=end.replace('v2200','v2192')
    assert text.count(begin)==text.count(end)==1
    a=text.index(begin);b=text.index(end,a)+len(end)
    c=old.index(old_begin);d=old.index(old_end,c)+len(old_end)
    restored=text[:a]+old[c:d]+text[b:]
    restored=restored.replace("or'guarded_commit'","or'guarded_counter'",1)
    restored=restored.replace("assert(boss_policy=='guarded_commit'or boss_policy=='commit_frequent','Physical boss input policy only')","assert(boss_policy=='guarded_counter'or boss_policy=='guarded_frequent','Physical boss input policy only')",1)
    assert restored.rstrip()+'\n'==old.rstrip()+'\n','Only physical boss unblocked attack commitment differs; entire ordinary source and read-only observers exact'
    return restore_boss_guarded_counter_policy(old)

def restore_boss_guard_edge_policy(text):
    baseline=ROOT/'mk2ks_natural_campaign_boss_guarded_commit_v2200.lua'
    assert digest(baseline)=='C2EB719EC4C5535C6575692A812678C4BE6BD203035408401BBECFF0A2F4E8C7'
    old=baseline.read_text()
    begin='   -- BEGIN actual-input boss clean-uppercut response v2222; physical buttons and read-only observation only.\n'
    end='   -- END actual-input boss clean-uppercut response v2222.\n'
    old_begin=begin.replace('v2222','v2200');old_end=end.replace('v2222','v2200')
    assert text.count(begin)==text.count(end)==1
    a=text.index(begin);b=text.index(end,a)+len(end)
    c=old.index(old_begin);d=old.index(old_end,c)+len(old_end)
    restored=text[:a]+old[c:d]+text[b:]
    restored=restored.replace("or'guard_edge12'","or'guarded_commit'",1)
    restored=restored.replace("assert(boss_policy=='guard_edge12'or boss_policy=='guard_edge16','Physical boss input policy only')","assert(boss_policy=='guarded_commit'or boss_policy=='commit_frequent','Physical boss input policy only')",1)
    assert restored.rstrip()+'\n'==old.rstrip()+'\n','Only physical guard release/HP-edge timing differs; every ordinary control and native observer exact'
    return restore_boss_guarded_commit_policy(old)

def restore_boss_prepared_crouch_policy(text):
    baseline=ROOT/'mk2ks_natural_campaign_boss_guard_edge_v2222.lua'
    assert digest(baseline)=='8E3710AE08288366D65DDFBB2351816A65CD3C8E88DD7975DC4ED8627460A500'
    old=baseline.read_text()
    begin='   -- BEGIN actual-input boss clean-uppercut response v2250; physical buttons and read-only observation only.\n'
    end='   -- END actual-input boss clean-uppercut response v2250.\n'
    old_begin=begin.replace('v2250','v2222');old_end=end.replace('v2250','v2222')
    assert text.count(begin)==text.count(end)==1
    a=text.index(begin);b=text.index(end,a)+len(end)
    c=old.index(old_begin);d=old.index(old_end,c)+len(old_end)
    restored=text[:a]+old[c:d]+text[b:]
    restored=restored.replace("or'prep_stomp'","or'guard_edge12'",1)
    restored=restored.replace("assert(boss_policy=='prep_stomp'or boss_policy=='prep_stance','Physical boss input policy only')","assert(boss_policy=='guard_edge12'or boss_policy=='guard_edge16','Physical boss input policy only')",1)
    assert restored.rstrip()+'\n'==old.rstrip()+'\n','Only physical boss preparation/cancellation and declared read-only native handlers differ; all ordinary controls and existing native observers exact'
    return restore_boss_guard_edge_policy(old)

def restore_boss_stomp_window_policy(text):
    baseline=ROOT/'mk2ks_natural_campaign_boss_prepared_crouch_v2250.lua'
    assert digest(baseline)=='5D79EB3E7529896651F775040DECB0BC1DE951A059A4ECEE10FDA94B24C18433'
    old=baseline.read_text()
    begin='   -- BEGIN actual-input boss clean-uppercut response v2283; physical buttons and read-only observation only.\n'
    end='   -- END actual-input boss clean-uppercut response v2283.\n'
    old_begin=begin.replace('v2283','v2250');old_end=end.replace('v2283','v2250')
    a=text.index(begin);b=text.index(end)+len(end)
    c=old.index(old_begin);d=old.index(old_end)+len(old_end)
    restored=text[:a]+old[c:d]+text[b:]
    restored=restored.replace("or'window_guard'","or'prep_stomp'",1)
    restored=restored.replace("assert(boss_policy=='window_guard'or boss_policy=='window_escape','Physical boss input policy only')","assert(boss_policy=='prep_stomp'or boss_policy=='prep_stance','Physical boss input policy only')",1)
    assert restored.rstrip()+'\n'==old.rstrip()+'\n','Only physical stomp-height/crouch/jump inputs and plan direction differ; original native observers and all ordinary control/selection/progression gates exact'
    return restore_boss_prepared_crouch_policy(old)

def restore_boss_escape_hold_policy(text):
    baseline=ROOT/'mk2ks_natural_campaign_boss_stomp_window_v2283.lua'
    assert digest(baseline)=='682274DCF945E2F4D76256C451D27D85190F8E47E623478CE4AD9750DE47FB52'
    old=baseline.read_text()
    begin='   -- BEGIN actual-input boss clean-uppercut response v2289; physical buttons and read-only observation only.\n'
    end='   -- END actual-input boss clean-uppercut response v2289.\n'
    old_begin=begin.replace('v2289','v2283');old_end=end.replace('v2289','v2283')
    a=text.index(begin);b=text.index(end)+len(end)
    c=old.index(old_begin);d=old.index(old_end)+len(old_end)
    restored=text[:a]+old[c:d]+text[b:]
    restored=restored.replace("or'escape_hold_close'","or'window_guard'",1)
    restored=restored.replace("assert(boss_policy=='escape_hold_close'or boss_policy=='escape_hold_early','Physical boss input policy only')","assert(boss_policy=='window_guard'or boss_policy=='window_escape','Physical boss input policy only')",1)
    assert restored.rstrip()+'\n'==old.rstrip()+'\n','Only physical jump hold/spacing and nonconflicting jump-plan inputs differ; every existing native observer, ordinary control and true-ID/progression/ending route exact'
    return restore_boss_stomp_window_policy(old)

def restore_boss_active_escape_policy(text):
    baseline=ROOT/'mk2ks_natural_campaign_boss_stomp_escape_hold_v2289.lua'
    assert digest(baseline)=='ACBBB1793F5EC961C5FEAC50FCFDCD6BF506F52E764C7A75AC4B4B3121AA9DFF'
    old=baseline.read_text()
    assert text.count('local quiet=false -- v2306: no artificial guard-only opening delay')==1
    restored=text.replace('local quiet=false -- v2306: no artificial guard-only opening delay','local quiet=frame-boss_live_begin<120')
    restored=restored.replace('v2306','v2289').replace('escape_active_','escape_hold_')
    assert restored.rstrip()+'\n'==old.rstrip()+'\n','Only physical opening delay and declared policy labels differ; all native observations, ordinary inputs, selection, progression and endings remain exact'
    return restore_boss_escape_hold_policy(old)

def restore_boss_late_airkick_policy(text):
    baseline=ROOT/'mk2ks_natural_campaign_boss_active_escape_v2306.lua'
    assert digest(baseline)=='0225533F4C1B1413F0C0ED9C40529B3AFCB7FD849246B8B654E00E227A3A1440'
    old=baseline.read_text()
    branch="     local kick_vy=p:read_u32(human.actor+0x60)\n     local kick_vy_min=boss_policy=='late_descend'and 0x20000 or 0\n     if kick_vy>=kick_vy_min and kick_vy<0x80000000 and frame%6<3 then press('High Kick')end"
    assert text.count(branch)==1
    restored=text.replace(branch,"     if frame%6<3 then press('High Kick')end",1)
    restored=restored.replace('v2332','v2306')
    replacements=(
      ("or'late_apex'","or'escape_active_close'"),
      ("assert(boss_policy=='late_apex'or boss_policy=='late_descend','Physical boss input policy only')","assert(boss_policy=='escape_active_close'or boss_policy=='escape_active_early','Physical boss input policy only')"),
      ("local preparation_gap=170","local preparation_gap=boss_policy=='escape_active_early'and 170 or 110"),
      ("local jump_gap=145","local jump_gap=boss_policy=='escape_active_early'and 145 or 95"))
    for before,after in replacements:
        assert restored.count(before)==1
        restored=restored.replace(before,after,1)
    assert restored.rstrip()+'\n'==old.rstrip()+'\n','Only physical late-kick velocity gate, early spacing constants, policy labels and revision comments differ; entire native observers, ordinary controls, selection, progression and ending code exact'
    return restore_boss_active_escape_policy(old)

def restore_boss_recycled_actor_observation(text):
    baseline=ROOT/'mk2ks_natural_campaign_boss_late_airkick_v2332.lua'
    assert digest(baseline)=='E56CC356144E992A7235655C86D0FE0321225B881E55DDC041732E9E94997E95'
    old=baseline.read_text()
    replacements=(
      ('local observed_main=human.main','local observed_main,observed_actor=human.main,human.actor'),
      ('      local current_stage=p:read_u16(0x01061b30)\n      local observed_actor=p:read_u32(slots[side].actor)\n      if at~=observed_main','      local current_stage=p:read_u16(0x01061b30)\n      if at~=observed_main'),
      ('p:read_u32(slots[side].main)~=observed_main or observed_actor<0x01000000 or observed_actor>=0x01100000 or','p:read_u32(slots[side].main)~=observed_main or p:read_u32(slots[side].actor)~=observed_actor or'))
    restored=text
    for before,after in replacements:
        assert restored.count(before)==1
        restored=restored.replace(before,after,1)
    assert restored.rstrip()+'\n'==old.rstrip()+'\n','Only current-actor read-only action observation changes; every control, native state/health/win/selection/ending observer and all game bytes stay exact'
    return restore_boss_late_airkick_policy(old)

def restore_shao_grounded_hp_policy(text):
    baseline=ROOT/'mk2ks_natural_campaign_boss_late_airkick_observed_v2344.lua'
    assert digest(baseline)=='1CEB5086FEBCAB6107D65F8E25179C9B1A4A6936CB9E65335DC307FD6A951094'
    old=baseline.read_text()
    branch="    if stage==16 then\n     -- Native fresh crouching HP versus Shao; never write health/AI/action.\n     local shao_gap=boss_policy=='shao_hp_early'and 125 or 95\n     if frame-boss_walk_counter<36 then\n      local age=frame-boss_walk_counter\n      if human.action~=0x107 and not can_crouch then\n       log('BOSS_CANCEL',string.format('policy=%s start=%d stage=%d human_actor=%08X human_main=%08X human_id=%d human_action=%d flags=%04X body=%04X height=%d health=%d,%d reason=actual_native_nonstance',\n        boss_policy,boss_walk_counter,stage,human.actor,human.main,human.id,human.action,human.flags,human.body,height,human.hp,other.hp))\n       boss_walk_counter=-1000;boss_walk_last_x=nil;press('Down');press('Block')\n      else\n       boss_walk_last_x=boss_walk_last_x or frame\n       press('Down');if age<=2 then press('High Punch')end\n      end\n     elseif gap<170 then\n      boss_walk_last_x=boss_walk_last_x or frame;press('Down')\n      if can_crouch and frame-boss_walk_last_x>=12 and gap<shao_gap and cpu_height<20 and frame-last_uppercut>=30 then\n       boss_walk_counter=frame;last_uppercut=frame\n       decision('shao_grounded_uppercut_attempt');press('High Punch')\n      end\n     else\n      boss_walk_last_x=nil;press('Down');press('Block')\n     end\n    elseif quiet then\n     boss_walk_last_x=nil;press('Block')"
    declaration="local boss_policy=os.getenv('MK2KS_BOSS_PHYSICAL_POLICY')or'shao_hp_close'\nassert(boss_policy=='shao_hp_close'or boss_policy=='shao_hp_early','Physical boss input policy only')"
    assert text.count(branch)==text.count(declaration)==1
    restored=text.replace(branch,"    if quiet then\n     boss_walk_last_x=nil;press('Block')",1).replace(declaration,"local boss_policy=os.getenv('MK2KS_BOSS_PHYSICAL_POLICY')or'late_apex'\nassert(boss_policy=='late_apex'or boss_policy=='late_descend','Physical boss input policy only')",1)
    assert restored.rstrip()+'\n'==old.rstrip()+'\n','Only boss16 physical fresh-HP decisions and declared policy labels differ; whole Kintaro, ordinary controls, selection, native actor/action/health/win/progression and ending observers exact'
    return restore_boss_recycled_actor_observation(old)

def restore_shao_midrange_hp_policy(text):
    baseline=ROOT/'mk2ks_natural_campaign_boss_shao_grounded_hp_v2361.lua'
    assert digest(baseline)=='ADF5699F4ECEBDA4CA3763650CD63F1F4F41E39606ADAD7C2EC80B296EACC66F'
    old=baseline.read_text()
    declaration="local boss_policy=os.getenv('MK2KS_BOSS_PHYSICAL_POLICY')or'shao_hp_mid110'\nassert(boss_policy=='shao_hp_mid110'or boss_policy=='shao_hp_mid115','Physical boss input policy only')"
    gap="local shao_gap=boss_policy=='shao_hp_mid115'and 115 or 110"
    assert text.count(declaration)==text.count(gap)==1
    restored=text.replace(declaration,"local boss_policy=os.getenv('MK2KS_BOSS_PHYSICAL_POLICY')or'shao_hp_close'\nassert(boss_policy=='shao_hp_close'or boss_policy=='shao_hp_early','Physical boss input policy only')",1).replace(gap,"local shao_gap=boss_policy=='shao_hp_early'and 125 or 95",1)
    assert restored.rstrip()+'\n'==old.rstrip()+'\n','Only declared intermediate Shao human-button distances and policy labels differ; every ordinary/Kintaro control, observer, selection, identity, health/win/ending path and game byte exact'
    return restore_shao_grounded_hp_policy(old)

def restore_shao_opening_guard_policy(text):
    baseline=ROOT/'mk2ks_natural_campaign_boss_shao_midrange_hp_v2374.lua'
    assert digest(baseline)=='CFF23AEBDB64CE845114BF5E18F32D69ABCE760914C7518541927004C17BE303'
    old=baseline.read_text()
    branch="    if stage==16 then\n     -- Only current visible CPU poses select physical defense/preparation.\n     -- No future state, attack/health/AI/position writes or game byte changes.\n     local taunt_pose=other.pose==0xff9a37e0 or other.pose==0xff9a3880 or other.pose==0xff9a3920\n     local walk_pose=other.pose==0xff99f600 or other.pose==0xff99f680 or other.pose==0xff99f700 or\n       other.pose==0xff99f780 or other.pose==0xff99f7e0 or other.pose==0xff99f860 or\n       other.pose==0xff99f8e0 or other.pose==0xff99f960 or other.pose==0xff99f9e0\n     local clear_body=other.body&0x0c==0\n     local prepare=clear_body and cpu_height<20 and\n       ((taunt_pose and gap<125)or(boss_policy=='shao_walk_guard'and walk_pose and gap<145))\n     local opening=clear_body and cpu_height<20 and\n       ((taunt_pose and gap<125)or(boss_policy=='shao_walk_guard'and other.pose==0xff99f600 and gap<95))\n     if frame-boss_walk_counter<36 then\n      local age=frame-boss_walk_counter\n      if human.action~=0x107 and not can_crouch then\n       log('BOSS_CANCEL',string.format('policy=%s start=%d stage=%d human_actor=%08X human_main=%08X human_id=%d human_action=%d flags=%04X body=%04X height=%d health=%d,%d reason=actual_native_nonstance',\n        boss_policy,boss_walk_counter,stage,human.actor,human.main,human.id,human.action,human.flags,human.body,height,human.hp,other.hp))\n       boss_walk_counter=-1000;boss_walk_last_x=nil;press('Down');press('Block')\n      else\n       boss_walk_last_x=boss_walk_last_x or frame\n       press('Down');if age<=2 then press('High Punch')end\n      end\n     elseif prepare then\n      boss_walk_last_x=boss_walk_last_x or frame;press('Down')\n      if can_crouch and frame-boss_walk_last_x>=12 and opening and frame-last_uppercut>=30 then\n       boss_walk_counter=frame;last_uppercut=frame\n       decision('shao_opening_uppercut_attempt');press('High Punch')\n      end\n     else\n      boss_walk_last_x=nil;press('Down');press('Block')\n     end\n"
    declaration="local boss_policy=os.getenv('MK2KS_BOSS_PHYSICAL_POLICY')or'shao_taunt_guard'\nassert(boss_policy=='shao_taunt_guard'or boss_policy=='shao_walk_guard','Physical boss input policy only')"
    assert text.count(branch)==text.count(declaration)==1
    first=old.index("    if stage==16 then\\n".replace('\\n','\n'));last=old.index("    elseif quiet then\\n".replace('\\n','\n'),first)
    restored=text.replace(branch,old[first:last],1).replace(declaration,"local boss_policy=os.getenv('MK2KS_BOSS_PHYSICAL_POLICY')or'shao_hp_mid110'\nassert(boss_policy=='shao_hp_mid110'or boss_policy=='shao_hp_mid115','Physical boss input policy only')",1)
    assert restored.rstrip()+'\\n'==old.rstrip()+'\\n','Only boss16 physical visible-pose defense/preparation/HP decisions and policy labels differ; every native observer, true-ID, ordinary/Kintaro control, health/win/progression/ending path and game byte exact'
    return restore_shao_midrange_hp_policy(old)

def restore_shao_opening_escape_policy(text):
    baseline=ROOT/'mk2ks_natural_campaign_boss_shao_opening_guard_v2395.lua'
    assert digest(baseline)=='9502AC7A04F2702ED69AB8D884C2D69B1EC0B302F7FA65671E0EE5C4A0962247'
    old=baseline.read_text()
    branch="    if stage==16 then\n     -- Measured current-pose openings remain unchanged; escape close\n     -- pressure through ordinary physical movement, not guest/AI writes.\n     local taunt_pose=other.pose==0xff9a37e0 or other.pose==0xff9a3880 or other.pose==0xff9a3920\n     local walk_pose=other.pose==0xff99f600 or other.pose==0xff99f680 or other.pose==0xff99f700 or\n       other.pose==0xff99f780 or other.pose==0xff99f7e0 or other.pose==0xff99f860 or\n       other.pose==0xff99f8e0 or other.pose==0xff99f960 or other.pose==0xff99f9e0\n     local clear_body=other.body&0x0c==0\n     local prepare=clear_body and cpu_height<20 and\n       ((taunt_pose and gap<125)or(walk_pose and gap<145))\n     local opening=clear_body and cpu_height<20 and\n       ((taunt_pose and gap<125)or(other.pose==0xff99f600 and gap<95))\n     if frame-boss_walk_counter<36 then\n      local age=frame-boss_walk_counter\n      if human.action~=0x107 and not can_crouch then\n       log('BOSS_CANCEL',string.format('policy=%s start=%d stage=%d human_actor=%08X human_main=%08X human_id=%d human_action=%d flags=%04X body=%04X height=%d health=%d,%d reason=actual_native_nonstance',\n        boss_policy,boss_walk_counter,stage,human.actor,human.main,human.id,human.action,human.flags,human.body,height,human.hp,other.hp))\n       boss_walk_counter=-1000;boss_walk_last_x=nil;press('Down');press('Block')\n      else\n       boss_walk_last_x=boss_walk_last_x or frame\n       press('Down');if age<=2 then press('High Punch')end\n      end\n     elseif frame-boss_last_jump<16 then\n      boss_walk_last_x=nil;press('Up');press(boss_jump_direction)\n     elseif height>8 then\n      boss_walk_last_x=nil\n      if frame-boss_last_jump<48 then press(boss_jump_direction)end\n      local kick_vy=p:read_u32(human.actor+0x60)\n      if kick_vy<0x80000000 and frame%6<3 then press('High Kick')end\n     elseif prepare then\n      boss_walk_last_x=boss_walk_last_x or frame;press('Down')\n      if can_crouch and frame-boss_walk_last_x>=12 and opening and frame-last_uppercut>=30 then\n       boss_walk_counter=frame;last_uppercut=frame\n       decision('shao_opening_uppercut_attempt');press('High Punch')\n      end\n     elseif can_crouch and gap<170 and cpu_height<20 and frame-boss_last_jump>=60 then\n      boss_last_jump=frame;boss_jump_direction=forward;boss_walk_last_x=nil\n      decision('shao_pressure_escape_jumpkick_attempt',boss_jump_direction)\n      press('Up');press(boss_jump_direction)\n     else\n      boss_walk_last_x=nil;press(back)\n     end\n"
    previous="    if stage==16 then\n     -- Only current visible CPU poses select physical defense/preparation.\n     -- No future state, attack/health/AI/position writes or game byte changes.\n     local taunt_pose=other.pose==0xff9a37e0 or other.pose==0xff9a3880 or other.pose==0xff9a3920\n     local walk_pose=other.pose==0xff99f600 or other.pose==0xff99f680 or other.pose==0xff99f700 or\n       other.pose==0xff99f780 or other.pose==0xff99f7e0 or other.pose==0xff99f860 or\n       other.pose==0xff99f8e0 or other.pose==0xff99f960 or other.pose==0xff99f9e0\n     local clear_body=other.body&0x0c==0\n     local prepare=clear_body and cpu_height<20 and\n       ((taunt_pose and gap<125)or(boss_policy=='shao_walk_guard'and walk_pose and gap<145))\n     local opening=clear_body and cpu_height<20 and\n       ((taunt_pose and gap<125)or(boss_policy=='shao_walk_guard'and other.pose==0xff99f600 and gap<95))\n     if frame-boss_walk_counter<36 then\n      local age=frame-boss_walk_counter\n      if human.action~=0x107 and not can_crouch then\n       log('BOSS_CANCEL',string.format('policy=%s start=%d stage=%d human_actor=%08X human_main=%08X human_id=%d human_action=%d flags=%04X body=%04X height=%d health=%d,%d reason=actual_native_nonstance',\n        boss_policy,boss_walk_counter,stage,human.actor,human.main,human.id,human.action,human.flags,human.body,height,human.hp,other.hp))\n       boss_walk_counter=-1000;boss_walk_last_x=nil;press('Down');press('Block')\n      else\n       boss_walk_last_x=boss_walk_last_x or frame\n       press('Down');if age<=2 then press('High Punch')end\n      end\n     elseif prepare then\n      boss_walk_last_x=boss_walk_last_x or frame;press('Down')\n      if can_crouch and frame-boss_walk_last_x>=12 and opening and frame-last_uppercut>=30 then\n       boss_walk_counter=frame;last_uppercut=frame\n       decision('shao_opening_uppercut_attempt');press('High Punch')\n      end\n     else\n      boss_walk_last_x=nil;press('Down');press('Block')\n     end\n"
    declaration="local boss_policy=os.getenv('MK2KS_BOSS_PHYSICAL_POLICY')or'shao_walk_escape'\nassert(boss_policy=='shao_walk_escape','Physical boss input policy only')"
    old_declaration="local boss_policy=os.getenv('MK2KS_BOSS_PHYSICAL_POLICY')or'shao_taunt_guard'\nassert(boss_policy=='shao_taunt_guard'or boss_policy=='shao_walk_guard','Physical boss input policy only')"
    assert text.count(branch)==text.count(declaration)==1
    restored=text.replace(branch,previous,1).replace(declaration,old_declaration,1)
    assert restored==old,'Only stage16 physical human movement differs; entire ordinary/Kintaro controls and all native observers exact'
    return restore_shao_opening_guard_policy(restored)


def restore_shao_crouch_exit_policy(text):
    import verify_current_boss_shao_crouch_exit_v2476 as predecessor
    baseline=ROOT/'mk2ks_natural_campaign_boss_shao_crouch_exit_v2461.lua'
    assert digest(baseline)=='C0642D3C62B62E3A2F836E15DF8479714F03E6F20BFE956E5BF3008B3502CFC5'
    new="    if stage==16 then\n     -- Measured jump attempts were often hit during original crouch exit.\n     -- Keep ordinary physical Down instead; no native/game/AI/health writes.\n     local taunt_pose=other.pose==0xff9a37e0 or other.pose==0xff9a3880 or other.pose==0xff9a3920\n     local clear_body=other.body&0x0c==0\n     local opening=clear_body and cpu_height<20 and\n       ((taunt_pose and gap<125)or(other.pose==0xff99f600 and gap<95))\n     if frame-boss_walk_counter<36 then\n      local age=frame-boss_walk_counter\n      if human.action~=0x107 and not can_crouch then\n       log('BOSS_CANCEL',string.format('policy=%s start=%d stage=%d human_actor=%08X human_main=%08X human_id=%d human_action=%d flags=%04X body=%04X height=%d health=%d,%d reason=actual_native_nonstance',\n        boss_policy,boss_walk_counter,stage,human.actor,human.main,human.id,human.action,human.flags,human.body,height,human.hp,other.hp))\n       boss_walk_counter=-1000;boss_walk_last_x=nil;press('Down');press('Block')\n      else\n       boss_walk_last_x=boss_walk_last_x or frame\n       press('Down');if age<=2 then press('High Punch')end\n      end\n     else\n      boss_walk_last_x=boss_walk_last_x or frame;press('Down')\n      if can_crouch and frame-boss_walk_last_x>=12 and opening and frame-last_uppercut>=30 then\n       boss_walk_counter=frame;last_uppercut=frame\n       decision('shao_opening_uppercut_attempt');press('High Punch')\n      end\n     end\n"
    old="    if stage==16 then\n     -- Measured current-pose openings remain unchanged; escape close\n     -- pressure through ordinary physical movement, not guest/AI writes.\n     local taunt_pose=other.pose==0xff9a37e0 or other.pose==0xff9a3880 or other.pose==0xff9a3920\n     local walk_pose=other.pose==0xff99f600 or other.pose==0xff99f680 or other.pose==0xff99f700 or\n       other.pose==0xff99f780 or other.pose==0xff99f7e0 or other.pose==0xff99f860 or\n       other.pose==0xff99f8e0 or other.pose==0xff99f960 or other.pose==0xff99f9e0\n     local clear_body=other.body&0x0c==0\n     local prepare=clear_body and cpu_height<20 and\n       ((taunt_pose and gap<125)or(walk_pose and gap<145))\n     local opening=clear_body and cpu_height<20 and\n       ((taunt_pose and gap<125)or(other.pose==0xff99f600 and gap<95))\n     if frame-boss_walk_counter<36 then\n      local age=frame-boss_walk_counter\n      if human.action~=0x107 and not can_crouch then\n       log('BOSS_CANCEL',string.format('policy=%s start=%d stage=%d human_actor=%08X human_main=%08X human_id=%d human_action=%d flags=%04X body=%04X height=%d health=%d,%d reason=actual_native_nonstance',\n        boss_policy,boss_walk_counter,stage,human.actor,human.main,human.id,human.action,human.flags,human.body,height,human.hp,other.hp))\n       boss_walk_counter=-1000;boss_walk_last_x=nil;press('Down');press('Block')\n      else\n       boss_walk_last_x=boss_walk_last_x or frame\n       press('Down');if age<=2 then press('High Punch')end\n      end\n     elseif frame-boss_last_jump<16 then\n      boss_walk_last_x=nil;press('Up');press(boss_jump_direction)\n     elseif height>8 then\n      boss_walk_last_x=nil\n      if frame-boss_last_jump<48 then press(boss_jump_direction)end\n      local kick_vy=p:read_u32(human.actor+0x60)\n      if kick_vy<0x80000000 and frame%6<3 then press('High Kick')end\n     elseif prepare then\n      boss_walk_last_x=boss_walk_last_x or frame;press('Down')\n      if can_crouch and frame-boss_walk_last_x>=12 and opening and frame-last_uppercut>=30 then\n       boss_walk_counter=frame;last_uppercut=frame\n       decision('shao_opening_uppercut_attempt');press('High Punch')\n      end\n     elseif (can_crouch or(height==0 and human.flags&0x0c==0 and human.body&0x0c==0 and human.action==0x301)) and gap<170 and cpu_height<20 and frame-boss_last_jump>=60 then\n      boss_last_jump=frame;boss_jump_direction=forward;boss_walk_last_x=nil\n      decision('shao_pressure_escape_jumpkick_attempt',boss_jump_direction)\n      press('Up');press(boss_jump_direction)\n     else\n      boss_walk_last_x=nil;press(back)\n     end\n"
    assert text.count(new)==1,'One exact declared physical crouch-wait branch'
    restored=text.replace(new,old,1).replace('shao_duck_wait','shao_crouch_exit_escape')
    assert restored==baseline.read_text().rstrip()+'\n','Only stage16 physical Down/counter policy differs; all ordinary/Kintaro controls and native observers/IDs/health/wins/progression/endings exact'
    return predecessor.restore_shao_crouch_exit_policy(restored)


def verify(folder, check_hashes=True, text_override=None):
    # Exact current provenance is mandatory even for in-memory log regressions.
    current_inputs={};matched(folder,current_inputs)
    if text_override is None:
        # Before the actual first boss, every native record must equal the
        # earlier accepted current-build campaign under the same buttons.
        meta=json.loads((folder/'result.json').read_text(encoding='utf-8-sig'))
        if meta['player']=='kano'and meta['human_slot']==1 and meta['strategy']=='zoning'and meta['boot_frame']==600:
            baseline=ROOT/'audit_v2053_current_kano_p1_zoning_campaign/run.log'
            actual=(folder/'run.log').read_text(encoding='utf-8-sig')
            old=baseline.read_text(encoding='utf-8-sig')
            stage_marker=re.search(r'^MK2_NAT_CAMPAIGN_STAGE frame=(\d+).* stage=15 ',old,re.M)
            assert stage_marker,'Accepted original cold route reaches first boss'
            until=int(stage_marker[1])
            def before(text):
                return [line for line in text.splitlines()if line.startswith('MK2_NAT_CAMPAIGN_')and (m:=re.search(r' frame=(\d+)',line))and int(m[1])<until]
            assert before(actual)==before(old),'Boss-only policy leaves entire ordinary campaign and true selection trajectory byte-exact'
            current_inputs[str(baseline)]=digest(baseline)
    result=json.loads((folder/'result.json').read_text(encoding='utf-8-sig'))
    text=text_override if text_override is not None else (folder/'run.log').read_text(encoding='utf-8-sig')
    errors=[]
    need=lambda ok,label: errors.append(label) if not ok else None
    side=result['human_slot'];identity={'kano':17,'sonya':18}[result['player']]
    need(side in (1,2) and result['cpu_slot']==3-side, 'Actual physical slots')
    need(result['exit_code']==0 and result['assistance']=='none', 'Terminal unassisted capture')
    need(result['candidate']==NAME,'Current candidate')
    if check_hashes:
        for name,sha in result['input_hashes'].items():
            need(digest(Path(name))==sha,'Frozen input changed: '+name)
    harnesses=list((folder/'input_sources').glob('mk2ks_natural_campaign_*v*.lua'))
    need(len(harnesses)==1 and harnesses[0].name=='mk2ks_natural_campaign_boss_shao_duck_wait_v2494.lua',
         'One actual whitelisted frozen current physical-input driver')
    harness=harnesses[0]if len(harnesses)==1 else folder/'missing_current_driver.lua'
    if harness.is_file():
        source=harness.read_text()
        if harness.name=='mk2ks_natural_campaign_boss_shao_duck_wait_v2494.lua':
            source=restore_shao_crouch_exit_policy(source)
            current_inputs[str(ROOT/'mk2ks_natural_campaign_boss_shao_opening_escape_v2419.lua')]=digest(ROOT/'mk2ks_natural_campaign_boss_shao_opening_escape_v2419.lua')
            current_inputs[str(ROOT/'mk2ks_natural_campaign_boss_shao_opening_guard_v2395.lua')]=digest(ROOT/'mk2ks_natural_campaign_boss_shao_opening_guard_v2395.lua')
            current_inputs[str(ROOT/'mk2ks_natural_campaign_boss_shao_midrange_hp_v2374.lua')]=digest(ROOT/'mk2ks_natural_campaign_boss_shao_midrange_hp_v2374.lua')
            for name in('mk2ks_natural_campaign_boss_shao_grounded_hp_v2361.lua','mk2ks_natural_campaign_boss_late_airkick_observed_v2344.lua','mk2ks_natural_campaign_boss_late_airkick_v2332.lua','mk2ks_natural_campaign_boss_active_escape_v2306.lua','mk2ks_natural_campaign_boss_stomp_escape_hold_v2289.lua','mk2ks_natural_campaign_boss_stomp_window_v2283.lua','mk2ks_natural_campaign_boss_prepared_crouch_v2250.lua','mk2ks_natural_campaign_boss_guard_edge_v2222.lua','mk2ks_natural_campaign_boss_guarded_commit_v2200.lua','mk2ks_natural_campaign_boss_guarded_counter_v2192.lua','mk2ks_natural_campaign_boss_clean_uppercut_v2174.lua','mk2ks_natural_campaign_boss_delayed_counter_v2140.lua','mk2ks_natural_campaign_boss_ground_evasion_v2130.lua','mk2ks_natural_campaign_boss_held_response_v2121.lua','mk2ks_natural_campaign_boss_anticipation_v2112.lua','mk2ks_natural_campaign_boss_timing_v2056.lua','mk2ks_natural_campaign_boss_evasion_v1740.lua','mk2ks_natural_campaign_probe_v850.lua'):
                current_inputs[str(ROOT/name)]=digest(ROOT/name)
        if harness.name=='mk2ks_natural_campaign_boss_stomp_window_v2283.lua':
            source=restore_boss_stomp_window_policy(source)
            for name in('mk2ks_natural_campaign_boss_prepared_crouch_v2250.lua','mk2ks_natural_campaign_boss_guard_edge_v2222.lua','mk2ks_natural_campaign_boss_guarded_commit_v2200.lua','mk2ks_natural_campaign_boss_guarded_counter_v2192.lua','mk2ks_natural_campaign_boss_clean_uppercut_v2174.lua','mk2ks_natural_campaign_boss_delayed_counter_v2140.lua','mk2ks_natural_campaign_boss_ground_evasion_v2130.lua','mk2ks_natural_campaign_boss_held_response_v2121.lua','mk2ks_natural_campaign_boss_anticipation_v2112.lua','mk2ks_natural_campaign_boss_timing_v2056.lua','mk2ks_natural_campaign_boss_evasion_v1740.lua','mk2ks_natural_campaign_probe_v850.lua'):
                current_inputs[str(ROOT/name)]=digest(ROOT/name)
        if harness.name=='mk2ks_natural_campaign_boss_prepared_crouch_v2250.lua':
            source=restore_boss_prepared_crouch_policy(source)
            for name in('mk2ks_natural_campaign_boss_guard_edge_v2222.lua','mk2ks_natural_campaign_boss_guarded_commit_v2200.lua','mk2ks_natural_campaign_boss_guarded_counter_v2192.lua','mk2ks_natural_campaign_boss_clean_uppercut_v2174.lua','mk2ks_natural_campaign_boss_delayed_counter_v2140.lua','mk2ks_natural_campaign_boss_ground_evasion_v2130.lua','mk2ks_natural_campaign_boss_held_response_v2121.lua','mk2ks_natural_campaign_boss_anticipation_v2112.lua','mk2ks_natural_campaign_boss_timing_v2056.lua','mk2ks_natural_campaign_boss_evasion_v1740.lua','mk2ks_natural_campaign_probe_v850.lua'):
                current_inputs[str(ROOT/name)]=digest(ROOT/name)
        if harness.name=='mk2ks_natural_campaign_boss_guard_edge_v2222.lua':
            source=restore_boss_guard_edge_policy(source)
            for name in('mk2ks_natural_campaign_boss_guarded_commit_v2200.lua','mk2ks_natural_campaign_boss_guarded_counter_v2192.lua','mk2ks_natural_campaign_boss_clean_uppercut_v2174.lua','mk2ks_natural_campaign_boss_delayed_counter_v2140.lua','mk2ks_natural_campaign_boss_ground_evasion_v2130.lua','mk2ks_natural_campaign_boss_held_response_v2121.lua','mk2ks_natural_campaign_boss_anticipation_v2112.lua','mk2ks_natural_campaign_boss_timing_v2056.lua','mk2ks_natural_campaign_boss_evasion_v1740.lua','mk2ks_natural_campaign_probe_v850.lua'):
                current_inputs[str(ROOT/name)]=digest(ROOT/name)
        if harness.name=='mk2ks_natural_campaign_boss_guarded_commit_v2200.lua':
            source=restore_boss_guarded_commit_policy(source)
            for name in('mk2ks_natural_campaign_boss_guarded_counter_v2192.lua','mk2ks_natural_campaign_boss_clean_uppercut_v2174.lua','mk2ks_natural_campaign_boss_delayed_counter_v2140.lua','mk2ks_natural_campaign_boss_ground_evasion_v2130.lua','mk2ks_natural_campaign_boss_held_response_v2121.lua','mk2ks_natural_campaign_boss_anticipation_v2112.lua','mk2ks_natural_campaign_boss_timing_v2056.lua','mk2ks_natural_campaign_boss_evasion_v1740.lua','mk2ks_natural_campaign_probe_v850.lua'):
                current_inputs[str(ROOT/name)]=digest(ROOT/name)
        if harness.name=='mk2ks_natural_campaign_boss_guarded_counter_v2192.lua':
            source=restore_boss_guarded_counter_policy(source)
            for name in('mk2ks_natural_campaign_boss_clean_uppercut_v2174.lua','mk2ks_natural_campaign_boss_delayed_counter_v2140.lua','mk2ks_natural_campaign_boss_ground_evasion_v2130.lua','mk2ks_natural_campaign_boss_held_response_v2121.lua','mk2ks_natural_campaign_boss_anticipation_v2112.lua','mk2ks_natural_campaign_boss_timing_v2056.lua','mk2ks_natural_campaign_boss_evasion_v1740.lua','mk2ks_natural_campaign_probe_v850.lua'):
                current_inputs[str(ROOT/name)]=digest(ROOT/name)
        if harness.name=='mk2ks_natural_campaign_boss_clean_uppercut_v2174.lua':
            source=restore_boss_clean_counter_policy(source)
            for name in('mk2ks_natural_campaign_boss_delayed_counter_v2140.lua','mk2ks_natural_campaign_boss_ground_evasion_v2130.lua','mk2ks_natural_campaign_boss_held_response_v2121.lua','mk2ks_natural_campaign_boss_anticipation_v2112.lua','mk2ks_natural_campaign_boss_timing_v2056.lua','mk2ks_natural_campaign_boss_evasion_v1740.lua','mk2ks_natural_campaign_probe_v850.lua'):
                current_inputs[str(ROOT/name)]=digest(ROOT/name)
        if harness.name=='mk2ks_natural_campaign_boss_delayed_counter_v2140.lua':
            source=restore_boss_delayed_counter_policy(source)
            for name in('mk2ks_natural_campaign_boss_ground_evasion_v2130.lua','mk2ks_natural_campaign_boss_held_response_v2121.lua','mk2ks_natural_campaign_boss_anticipation_v2112.lua','mk2ks_natural_campaign_boss_timing_v2056.lua','mk2ks_natural_campaign_boss_evasion_v1740.lua','mk2ks_natural_campaign_probe_v850.lua'):
                current_inputs[str(ROOT/name)]=digest(ROOT/name)
        if harness.name=='mk2ks_natural_campaign_boss_ground_evasion_v2130.lua':
            source=restore_boss_ground_evasion_policy(source)
            for name in('mk2ks_natural_campaign_boss_held_response_v2121.lua','mk2ks_natural_campaign_boss_anticipation_v2112.lua','mk2ks_natural_campaign_boss_timing_v2056.lua','mk2ks_natural_campaign_boss_evasion_v1740.lua','mk2ks_natural_campaign_probe_v850.lua'):
                current_inputs[str(ROOT/name)]=digest(ROOT/name)
        if harness.name=='mk2ks_natural_campaign_boss_held_response_v2121.lua':
            source=restore_boss_held_response_policy(source)
            for name in('mk2ks_natural_campaign_boss_anticipation_v2112.lua','mk2ks_natural_campaign_boss_timing_v2056.lua','mk2ks_natural_campaign_boss_evasion_v1740.lua','mk2ks_natural_campaign_probe_v850.lua'):
                current_inputs[str(ROOT/name)]=digest(ROOT/name)
        if harness.name=='mk2ks_natural_campaign_boss_anticipation_v2112.lua':
            source=restore_boss_anticipation_policy(source)
            for name in('mk2ks_natural_campaign_boss_timing_v2056.lua','mk2ks_natural_campaign_boss_evasion_v1740.lua','mk2ks_natural_campaign_probe_v850.lua'):
                current_inputs[str(ROOT/name)]=digest(ROOT/name)
        if harness.name=='mk2ks_natural_campaign_boss_timing_v2056.lua':
            source=restore_boss_timing_policy(source)
            current_inputs[str(ROOT/'mk2ks_natural_campaign_boss_evasion_v1740.lua')]=digest(ROOT/'mk2ks_natural_campaign_boss_evasion_v1740.lua')
            current_inputs[str(ROOT/'mk2ks_natural_campaign_probe_v850.lua')]=digest(ROOT/'mk2ks_natural_campaign_probe_v850.lua')
        if harness.name=='mk2ks_natural_campaign_boss_evasion_v1740.lua':
            source=restore_boss_evasion_policy(source)
            current_inputs[str(ROOT/'mk2ks_natural_campaign_probe_v850.lua')]=digest(ROOT/'mk2ks_natural_campaign_probe_v850.lua')
        if harness.name=='mk2ks_natural_campaign_boss_tactics_v1735.lua':
            source=restore_boss_input_policy(source)
            current_inputs[str(ROOT/'mk2ks_natural_campaign_probe_v850.lua')]=digest(ROOT/'mk2ks_natural_campaign_probe_v850.lua')
        if harness.name=='mk2ks_natural_campaign_floor_v1698.lua':
            source=restore_boss_observation_window(source)
            current_inputs[str(ROOT/'mk2ks_natural_campaign_floor_v1566.lua')]=digest(ROOT/'mk2ks_natural_campaign_floor_v1566.lua')
        need(not re.search(r':write_|\bload\s*\(|\bdofile\s*\(|\beval\b',source),'No guest writes/dynamic delegated code')
        need('roster)<=18 then' in source,'Wait for valid native continue selection ID')
        if harness.name in('mk2ks_natural_campaign_floor_v1560.lua','mk2ks_natural_campaign_floor_v1566.lua','mk2ks_natural_campaign_floor_v1698.lua'):
            baseline=ROOT/'mk2ks_natural_campaign_probe_v850.lua'
            need(digest(baseline)=='EC7ADC60ABA59E44EA26E2AB403EBA03C4ADB742D7059811EF8CCEA755E2282D','Exact immutable accepted physical-input policy')
            current_inputs[str(baseline)]=digest(baseline)
            removed=re.sub(r'-- Read-only native drawing observer, layered over the byte-exact v850 input policy\.[\s\S]*?(?=local adjacency=)', '', source, count=1)
            removed=re.sub(r"   floor_origin=frame;floor_epoch=floor_epoch\+1;floor_latches=\{\};floor_queues=\{\}\n   log\('FLOOR_BEGIN',[^\n]*\n", '', removed, count=1)
            removed=removed.replace('  if frame-floor_origin>=216 and frame-floor_origin<=336 and frame%8==0 then floor_pending=true end\n','',1)
            removed=re.sub(r" log\('FLOOR_RESULT',[^\n]*\n", '', removed, count=1)
            need(removed==baseline.read_text(),'Entire remaining driver exactly equals accepted v850: all physical gameplay inputs untouched')
    need(not re.search(r'\[LUA ERROR\]|fatal error|access violation|exception at',text,re.I),'No observer or native runtime errors')
    rows=parse(text,side,result['player'])

    actions=[r for r in rows if r['tag']=='BOSS_ACTION']
    for r in actions:
        need(r['stage']in(15,16)and r['id']==r['roster']==identity and r['state']==1 and
             r['owner']==r['actor']and r['at']==r['main']+0x1f0 and
             all(0x01000000<=r[k]<0x01100000 for k in('actor','main'))and
             all(0<int(h)<=161 for h in r['health'].split(',')),'Actual read-only own human live boss action word store')
    uppercuts=[r for r in actions if r['after']==0x107]
    for r in uppercuts:
        need(r['pc']==0xff83c340 and r['mask']==0xffff and
             r['a1']&0xffff==0x107 and r['a8']==r['actor']and r['a13']==r['main'],
             'Actual original HUMAN uppercut107 action assignment and physical human actor/Main registers; CPU106 is a distinct path')

    plans=[r for r in rows if r['tag']=='BOSS_PLAN']
    for r in plans:
        need(r['policy']==result['boss_policy']and r['policy']=='shao_duck_wait','Declared actual physical boss policy')
        need(r['stage']in(15,16)and r['human_id']==identity and r['cpu_id']==(12 if r['stage']==15 else 13),'True own identity and actual scheduled boss')
        need(r['height']<=8,'Every held boss physical attempt is grounded; native crouch/recovery/hit state may ignore it and no successful activation is implied')
        need(all(0x01000000<=r[k]<0x01100000 for k in('human_actor','human_main','cpu_actor','cpu_main')),'Physical Main/actor context')
        need(all(0<int(h)<=161 for h in r['health'].split(',')),'No plan after native KO')
    fields=[r for r in rows if r['tag']=='BOSS_FIELD']
    responses=[r for r in rows if r['tag']=='BOSS_RESPONSE']
    for r in fields:
        need(r['policy']==result['boss_policy']and r['stage']in(15,16),'Declared current boss field scope')
        need(r['human_id']==identity and r['cpu_id']==(12 if r['stage']==15 else 13),'Actual native boss/human field IDs')
        need(r['gap']==abs(r['h_x']-r['c_x'])and r['height']==r['h_floor']-r['h_y']and r['cpu_height']==r['c_floor']-r['c_y'],'Actual native field geometry, no supplied positions')
        need(all(0x01000000<=r[k]<0x01100000 for k in('human_actor','human_main','cpu_actor','cpu_main')),'Read-only live boss field actor/Main context')
        need(all(0<int(h)<=161 for h in r['health'].split(',')),'No physical control observation past KO')
    field_at={r['frame']:r for r in fields}
    need(len(field_at)==len(fields),'Unique actual pre-input boss field')
    for r in plans:
        f=field_at.get(r['frame'])
        need(f is not None and all(r[k]==f[k]for k in('policy','stage','human_actor','human_main','cpu_actor','cpu_main','human_id','cpu_id','gap','height','cpu_height','human_action','cpu_action','flags','body','health')),'Every physical attempt equals its actual before-input native field')
        need(r['scope']=='physical_attempt_not_assumed_activation','Do not promote an intended physical input to an actual native move')
    for r in responses:
        f=field_at.get(r['frame'])
        need(f is not None and r['kind']=='actual_airborne'and f['height']>8 and r['height']==f['height']and
             r['actor']==f['human_actor']and r['main']==f['human_main']and r['id']==identity and
             r['x']==f['h_x']and r['y']==f['h_y'],'Actual completed motion observation, not a forced/assumed jump')
        previous=field_at.get(r['frame']-1)
        need(previous is None or previous['height']<=8,'Observed transition from ground to actual airborne state')
    if harness.name=='mk2ks_natural_campaign_boss_shao_duck_wait_v2494.lua':
        boss_frames=set(field_at)
        actual_boss_inputs=[r for r in rows if r['tag']=='INPUT'and r['frame']in boss_frames]
        actual_keys={(r['frame'],r['button'])for r in actual_boss_inputs}
        need(len(actual_keys)==len(actual_boss_inputs),'Unique real boss input fields')
        need(all(r['button']in('Down','High_Punch','Block','Up','Left','Right','High_Kick')for r in actual_boss_inputs),'Only declared physical crouch/counter/jumpkick/guard buttons')
        input_at={}
        for at,key in actual_keys:input_at.setdefault(at,set()).add(key)
        plan_at={r['frame']:r for r in plans};need(len(plan_at)==len(plans),'Unique physical boss plans')
        cancels=[r for r in rows if r['tag']=='BOSS_CANCEL']
        cancel_at={r['frame']:r for r in cancels};need(len(cancel_at)==len(cancels),'Unique physical boss cancellation')
        first=down_since=None;command=previous=-1000;jump=-1000;direction=None
        escape=True
        preparation_gap=170
        jump_gap=145
        kick_vy_min=0x20000 if result['boss_policy']=='late_descend'else 0
        for frame in sorted(boss_frames):
            f=field_at[frame]
            if frame-1 not in boss_frames:first=frame;command=-1000;down_since=None;jump=-1000;direction=None
            expected=set();should_plan=None;should_cancel=False;old_command=command;planned_direction='none'
            stance=f['height']==0 and not f['flags']&0x0c and not f['body']&0x0c and f['human_action']in(0x303,0x302,0x304)
            descending=0<f['cpu_vy']<0x80000000
            forward='Right'if f['h_x']<f['c_x']else'Left'
            if f['stage']==16:
                taunt_pose=f['cpu_pose']in(0xff9a37e0,0xff9a3880,0xff9a3920)
                clear_body=not f['cpu_body']&0x0c
                opening=clear_body and f['cpu_height']<20 and ((taunt_pose and f['gap']<125)or(f['cpu_pose']==0xff99f600 and f['gap']<95))
                if frame-command<36:
                    age=frame-command
                    if f['human_action']!=0x107 and not stance:
                        expected={'Down','Block'};should_cancel=True;command=-1000;down_since=None
                    else:
                        if down_since is None:down_since=frame
                        expected={'Down'}
                        if age<=2:expected.add('High_Punch')
                else:
                    if down_since is None:down_since=frame
                    expected={'Down'}
                    if stance and frame-down_since>=12 and opening and frame-previous>=30:
                        should_plan='shao_opening_uppercut_attempt';command=previous=frame;expected.add('High_Punch')
            elif False:expected={'Block'};down_since=None # No artificial opening delay; independently replay the active policy from the first field.
            elif frame-command<36:
                age=frame-command
                if f['human_action']!=0x107 and not stance:
                    expected={'Down','Block'};should_cancel=True;command=-1000;down_since=None
                else:
                    if down_since is None:down_since=frame
                    expected={'Down'}
                    if age<=2:expected.add('High_Punch')
            elif escape and frame-jump<16:
                down_since=None;expected={'Up',direction}
            elif escape and f['height']>8:
                down_since=None
                if frame-jump<48:expected.add(direction)
                if kick_vy_min<=f['human_vy']<0x80000000 and frame%6<3:expected.add('High_Kick')
            elif f['cpu_action']==0x407:
                if down_since is None:down_since=frame
                expected={'Down'}
                if stance and f['gap']<95 and frame-down_since>=12 and frame-previous>=30 and descending and 160<f['cpu_height']<=240:
                    should_plan='descending_stomp_uppercut_attempt';command=previous=frame;expected.add('High_Punch')
            elif escape and f['gap']<preparation_gap:
                if down_since is None:down_since=frame
                expected={'Down'}
                if stance and frame-down_since>=12 and f['gap']<jump_gap and f['cpu_height']<20 and frame-jump>=60:
                    should_plan='close_pressure_jumpkick_attempt';jump=frame;direction=forward;planned_direction=direction
                    down_since=None;expected={'Up',direction}
            else:expected={'Down','Block'};down_since=None
            need(input_at.get(frame,set())==expected,'Every actual boss-only crouch-wait/opening/descending-stomp/guard input equals independently replayed native state and height policy')
            need((frame in plan_at)==(should_plan is not None),'Every physical stomp/escape/Shao plan follows measured actual native height/stance/cooldown/preparation')
            need((frame in cancel_at)==should_cancel,'Every physical cancellation follows actual nonstance, never native107')
            if frame in plan_at:
                need(plan_at[frame]['move']==should_plan and plan_at[frame]['direction']==planned_direction,'Only actual measured stomp/Shao crouching counter or declared physical forward jumpkick plan')
            if frame in cancel_at:
                r=cancel_at[frame]
                need(r['start']==old_command and r['reason']=='actual_native_nonstance'and
                     all(r[k]==f[k]for k in('policy','stage','human_actor','human_main','human_id','human_action','flags','body','height','health')),
                     'Actual physical cancellation provenance equals its before-input native field')
        handlers=[r for r in rows if r['tag']=='BOSS_HANDLER']
        allowed={0xff82f9f0,0xff8300c0,0xff830200,0xff832040,0xff877d80,0xff837e40,0xff8304d0,0xff870dc0,0xff82fd70,0xff831360}
        for r in handlers:
            need(r['entry']not in(0xff82fd70,0xff831360)or r['stage']==16,'Extended native crouch/jump observations are stage16 only')
            need(r['policy']==result['boss_policy']and r['stage']in(15,16)and r['entry']in allowed and r['pc']==r['entry']+16 and
                 r['id']==r['roster']==identity and r['state']==1 and r['owner']==r['actor']==r['a8']and r['main']==r['a13']and
                 all(0x01000000<=r[k]<0x01100000 for k in('actor','main'))and
                 all(0<int(h)<=161 for h in r['health'].split(',')),'Actual native boss handler instruction/true own actor/Main/register provenance')
            if r['frame']in field_at:
                f=field_at[r['frame']]
                need(r['actor']==f['human_actor']and r['main']==f['human_main'],'Actual handler belongs to same-field physical human')
        need(not any(r['tag']=='SPECIAL'and r['stage']in(15,16)for r in rows),'No special/proxy attack credited at bosses')
    specials=[r for r in rows if r['tag']=='SPECIAL']
    moves={'knife':(17,0xffffb000,32),'ball':(17,0xffffde00,48),'blade':(17,0xfff8cc00,48),'choke':(17,0xfff91400,48),
           'ring':(18,0xffffb400,32),'square':(18,0xffffca00,48),'bicycle':(18,0xfff9a400,48),'leg':(18,0xfff80800,48)}
    if result['strategy']in('leg','defensive_leg'):
        need(any(r['move']=='leg'for r in specials),'Actual leg entries, not just planned inputs')
    elif result['strategy']=='zoning':
        need(any(r['move']==('knife'if identity==17 else'ring')for r in specials),'Actual native zoning projectile entries')
    for row in specials:
        move_identity,entry,delta=moves.get(row['move'],(-1,-1,-1))
        if harness.name=='mk2ks_natural_campaign_probe_v842.lua':
            # The preserved original projectile-only observer fixes its tap
            # to entry+16 but predates the explicit at field. It cannot stand
            # in for the new four-move observation schema.
            need(row['move']==('knife'if identity==17 else'ring')and 'at'not in row,
                 'Exact original projectile-only schema, never substituted for a new move')
            observed_at=entry+16
        else:observed_at=row['at']
        need(move_identity==identity and row['entry']==entry and observed_at==entry+16 and row['pc']==entry+delta and
             row['actor']==row['a8'] and row['main']==row['a13'] and
             row['id']==row['roster']==identity and
             all(0x01000000<=row[k]<0x01100000 for k in('actor','main')),
             'Actual native special instruction fetch and true human actor/Main registers')
    need(all(r.get('writes')==0 and r.get('assistance')=='none' and r.get('human_slot')==side and
             r.get('fighter')==result['player'] for r in rows),'Every native record scope')
    boots=[r for r in rows if r['tag']=='BOOT']
    need(len(boots)==1 and boots[0]['schema']==30,'Exactly one current cold driver')
    orders=expected_orders();schedules={}
    for row in [r for r in rows if r['tag']=='ROM']:
        n=row['order'];ids=tuple(map(int,row['ids'].split(',')))
        need(n in range(6) and n not in schedules,'Unique original schedule')
        if n in range(6):need(ids==orders[n] and row['list']==f'{0xfffa3000+n*0x180:08X}' and row['table']=='FFFA2C00','Original-derived true-ID schedule')
        schedules[n]=ids
    need(set(schedules)==set(range(6)),'All six actual schedules')
    stages=[r for r in rows if r['tag']=='STAGE']
    wins=[r for r in rows if r['tag']=='WIN']
    losses=[r for r in rows if r['tag']=='LOSS']
    live=[r for r in rows if r['tag']=='LIVE']
    states=[r for r in rows if r['tag']=='STATE']
    need(bool(stages) and stages[0]['stage']==0,'Cold natural campaign begins at zero')
    schedule=stages[0]['schedule'] if stages else -1
    order=next((n for n in range(6) if schedule==0xfffa3000+n*0x180),None)
    need(order is not None,'Selected native schedule pointer')
    need(all(r['schedule']==schedule for r in stages+live),'Schedule unchanged throughout campaign')
    original=(ROOT/'mk2/mk2-maincpu.bin').read_bytes()
    guest_path=folder/'guest_maincpu.bin'
    guest=guest_path.read_bytes()
    need(guest==current_source.expected()[0],'Same-candidate initialized guest independently reconstructed; not a campaign-time ROM dump')
    need(hashlib.sha256(original).hexdigest().upper()=='45B3285496DB555EFAF4A3608A4F59845DD47A82E4A0593607E0592F47B36F23',
         'Exact original native program')
    need(guest==current_source.expected()[0],
         'Actual exact-current same-candidate guest snapshot')
    current_inputs[str(guest_path)]=hashlib.sha256(guest).hexdigest().upper()
    current_inputs[str(ROOT/'mk2/mk2-maincpu.bin')]=hashlib.sha256(original).hexdigest().upper()
    # Original human attack selects main-animation28, then assigns107.
    # Do not confuse it with the separate CPU106 wrapper at FF870880.
    for address,words in ((0xff870e30,(0x1b89,)),(0xff870f50,(0x09c1,0x0107)),
                          (0xff871000,(0xc080,0x73f0,0xff83))):
        at=(address-0xff800000)//8
        need(struct.unpack_from('<'+'H'*len(words),original,at)==words and
             guest[at:at+len(words)*2]==original[at:at+len(words)*2],
             'Source-bound original HUMAN uppercut animation28/action107/native attack route')
    first=(0xff870dc0-0xff800000)//8;last=(0xff871030-0xff800000)//8
    need(guest[first:last]==original[first:last],'Entire original human uppercut routine unchanged')
    original_action_store=(0xff83c330-0xff800000)//8
    need(guest[original_action_store:original_action_store+4]==original[original_action_store:original_action_store+4],
         'Original action assignment instruction and operand unchanged')
    word=lambda a:struct.unpack_from('<H',original,(a-0xff800000)//8)[0]
    need((word(0xff8366c0),word(0xff8366f0))==(0x4541,0x8026),'Original native damage subtract/store instructions')
    for address,words in ((0xff86e650,(0xb128,0x1f0)),(0xffa166e0,(0xb008,0x1f0))):
        need(struct.unpack_from('<2H',original,(address-0xff800000)//8)==words,'Original Shang store signature')
    # All observed health writes, including zero damage and positive native
    # bar/reset stores, must come from the actual original per-slot writer.
    # Do not count health-bar animation as earned damage or healing assistance.
    health_pcs={1:{0xff836700,0xff825930,0xff9dece0,0xff9def40},
                2:{0xff836700,0xff825960,0xff9ded10,0xff9def70}}
    for pc in sorted((health_pcs[1]|health_pcs[2])-{0xff836700}):
        at=(pc-48-0xff800000)//8
        need(guest[at:at+6]==original[at:at+6],'Actual unchanged original absolute health-store instruction')
        instruction=struct.unpack_from('<3H',original,at)
        slot=1 if pc in health_pcs[1]else 2
        need(instruction in((0x0580,0x02f0 if slot==1 else 0x0ec0,0x0106),
                            (0x058a,0x02f0 if slot==1 else 0x0ec0,0x0106)),
             'Exact original native absolute store and physical health address')
    at=(0xff8366c0-0xff800000)//8
    need(guest[at:at+8]==original[at:at+8],'Actual unchanged original collision subtract/store code')
    for row in(r for r in rows if r['tag']=='HEALTH'):
        slot=row['slot']
        need(slot in health_pcs and row['pc']in health_pcs.get(slot,set())and
             row['at']==(0x010602f0 if slot==1 else 0x01060ec0),
             'Every observed health store uses its exact original writer and physical slot')
        if row['pc']==0xff836700:
            need(0<=row['after']<=row['before']<=161,'Original collision never heals or supplies health')
    morph_ids=(0,1,2,3,4,5,5,7,8,9,10,11,17,18)
    need(struct.unpack_from('<14H',guest,0xf9040)==morph_ids,'Native fourteen-choice morph roster includes true Kano/Sonya, preserving original stock mapping')
    id_writes=[r for r in rows if r['tag']=='CPU_ID']
    for row in id_writes:
        pc=row['pc'];new=row['after']
        need(row['mask']==0xffff and row['a8']==row['actor'] and
             ((pc==0xff86e670 and new in morph_ids and new==row['a9']&0xffff) or
              (pc==0xffa16700 and new==6 and new==row['a0']&0xffff)), 'Original CPU morph/restore provenance')
    for row in live:
        stage=row['stage'];human=tuple(map(int,row['human'].split(':')));cpu=tuple(map(int,row['cpu'].split(':')))
        need(human==(identity,identity),'True live human ID/Main, no proxy')
        need(all(0x01000000<=row[k]<0x01100000 for k in ('human_actor','human_main','cpu_actor','cpu_main')),'Actual live actor/Main pointers')
        need(order is not None and stage in range(17),'Valid live native stage')
        if order is None or stage not in range(17):continue
        expected=orders[order][stage]
        owned=cpu==(expected,expected)
        if not owned and expected==6 and stage==14 and cpu[0]==6:
            previous=[r for r in id_writes if r['event']<row['event'] and r['actor']==row['cpu_actor']]
            owned=bool(previous and previous[-1]['after']==cpu[1] and previous[-1]['a13']==row['cpu_main'])
        need(owned,'Scheduled CPU true ID or original proven morph')
    for row in wins:
        slot=row['slot'];id_=row['id'];hp=tuple(map(int,row['health'].split(',')))
        need(row['entry']==0xfffef800+id_*32 and row['pc']==0xff8296b0,'Actual native winner-table call')
        need(slot in (1,2) and hp[slot-1]>hp[2-slot],'Native winning health, not fabricated KO')
        need(slot!=side or id_==identity,'Own actual winning fighter')
        following=[r for r in states if r['frame']==row['frame']+1]
        need(bool(following) and following[0]['mode'] in (5,11) and following[0]['winner']==slot and following[0]['health']==row['health'],'Matching next-field native winner scene')
    for before,after in zip(stages,stages[1:]):
        jump=after['stage']-before['stage']
        need(jump==1 or(jump==2 and before['stage']==12 and after['stage']==14 and orders[order][13]==14),'Only original endurance sentinel may be skipped')
        last_loss=max([r['event'] for r in losses if r['event']<after['event'] and r['stage']==before['stage']]+[before['event']])
        earned=[r for r in wins if last_loss<r['event']<after['event'] and r['stage']==before['stage'] and r['slot']==side]
        need(len(earned)>=2,'Advance after two wins in actual successful attempt, not accumulated failed matches')
    selections=[r for r in rows if r['tag']=='SELECT']
    inputs=[r for r in rows if r['tag']=='INPUT']
    need([r['number'] for r in selections]==list(range(1,len(selections)+1)),'Sequential genuine selections')
    for selection in selections:
        need(selection['target']==identity and selection['initial']<=18 and selection['schedule']==schedule,'Actual native selection target/starting ID/schedule')
        confirmed=[r for r in rows if r['tag']=='SELECT_ID' and r['number']==selection['number']]
        need(len(confirmed)==2 and all(r['roster']==identity and r['state']==3 for r in confirmed),'Own true ID before native confirm')
        if selection['number']>1:
            preceding=[r for r in losses if r['event']<selection['event']]
            need(bool(preceding),'Continue follows actual native loss')
            if not preceding:continue
            loss=preceding[-1]
            need(selection['continue']==loss['frame'] and selection['stage']==loss['stage'],'Original continue retains its lost stage')
            events=[r for r in inputs if loss['event']<r['event']<selection['event']]
            need(any(r['button']=='Coin' for r in events) and any(r['button']=='Start' for r in events),'Coin and start inputs before real continue selection')
    negative=[r for r in rows if r['tag']=='HEALTH' and r['after']<r['before']]
    damage=[r for r in negative if r['pc']==0xff836700]
    need(bool(damage),'Actual original combat damage stores')
    # Other original stores include round/health-bar teardown; do not mistake
    # their real native writes for combat damage or count them as earned hits.
    need(all(r['pc'] in (0xff836700,0xff9def40,0xff9def70) for r in negative),'Only observed original combat/health-bar writers, no other health decrement writer')
    own_wins=[r for r in wins if r['slot']==side]
    boss_damage=[r for r in damage if r['slot']==3-side and r['frame']in field_at and
                 r['a8']==field_at[r['frame']]['human_actor']and r['a13']==field_at[r['frame']]['human_main']]
    actual_boss_uppercut_damage=[r for r in boss_damage if field_at[r['frame']]['human_action']==0x107]
    starts=[r for r in rows if r['tag']=='ENDING_START']
    completed=[r for r in rows if r['tag']=='ENDING_COMPLETED']
    mandatory=list(range(13))+[14,15,16]
    reached=[r['stage'] for r in stages]
    clear=(not errors and reached==mandatory and any(r['stage']==16 for r in own_wins) and len(starts)==len(completed)==1)
    if clear:
        start,end=starts[0],completed[0]
        need(start['winner']==side and start['roster']==identity and start['actors']=='00000000,00000000','Owned boss ending retirement')
        need(end['frame']-start['frame']==end['age'] and end['age']>1200 and end['mode']==11,'Actual ending completion chronology')
        need(min(map(int,end['pictures'].split(',')))>0 and min(map(int,end['texts'].split(',')))>0,'Both own native picture/story pages')
        need(tuple(map(int,end['roster'].split(',')))[side-1]!=identity,'Original return to attract roster')
    finals=[r for r in rows if r['tag']=='RESULT']
    need(len(finals)==1 and finals[0]['schema']==30 and finals[0]['native_win_reads']==len(wins) and
         finals[0]['seen_stages']==len(stages),'Terminal native accounting')
    return dict(passed=not errors,bounded_campaign_evidence_proven=not errors,
                unassisted_clear_proven=clear and not errors,errors=sorted(set(errors)),
                player=result['player'],human_slot=side,stages_reached=reached,
                native_own_round_wins=len(own_wins),native_combat_damage_stores=len(damage),
                paid_continue_losses=len(losses),ending_starts=len(starts),ending_completions=len(completed),
                native_owned_special_entries=len(specials),actualNativeUppercutAssignments=len(uppercuts),actualBossOwnedDamageStores=len(boss_damage),actualBossUppercutDamageStores=len(actual_boss_uppercut_damage),actualBossUppercutDamage=sum(r['before']-r['after']for r in actual_boss_uppercut_damage),actualBossRoundWins=sum(r['stage']in(15,16)for r in own_wins),humanUppercutNativeAction='0107',cpu106NeverUsedToClassifyHumanUppercut=True,uppercutAssignmentFrames=[r['frame']for r in uppercuts],readOnlyOwnActionStores=len(actions),physicalBossPlans=len(plans),physicalStompPlans=sum(r['move']=='descending_stomp_uppercut_attempt'for r in plans),physicalJumpkickPlans=sum(r['move']in('close_pressure_jumpkick_attempt','shao_pressure_escape_jumpkick_attempt')for r in plans),observedBossFields=len(fields),observedAirborneTransitions=len(responses),physicalAttemptsNeverAssumedActivations=True,physicalCommandCancellations=sum(r['tag']=='BOSS_CANCEL'for r in rows),nativeBossHandlerFetches=sum(r['tag']=='BOSS_HANDLER'for r in rows),nativeBossHPDispatches=sum(r['tag']=='BOSS_HANDLER'and r['entry']==0xff8300c0 for r in rows),nativeHumanUppercutEntryFetches=sum(r['tag']=='BOSS_HANDLER'and r['entry']==0xff870dc0 for r in rows),bossPolicy=result['boss_policy'],native_special_moves={move:sum(r['move']==move for r in specials)for move in moves
                                                                              if any(r['move']==move for r in specials)},inputHashes=current_inputs,
                fullPortAcceptance=False,scope='Actual input-only native campaign progression/ownership/damage/win calls; no universal combat, all-ending pixels/audio or whole-port acceptance')


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('folder',type=Path)
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args()
    if args.output.exists():raise ValueError('Refusing to overwrite evidence')
    report=verify(args.folder)
    for path in args.folder.rglob('*'):
        if path.is_file():report['inputHashes'][str(path.resolve())]=digest(path)
    for path in(Path(__file__),ROOT/'tools/verify_active_launch_timer_v1520.py',ROOT/'tools/verify_p2_campaign.py'):
        report['inputHashes'][str(path.resolve())]=digest(path)
    current_launch.module_pins(report['inputHashes'])
    args.output.mkdir();(args.output/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:value for k,value in report.items()if k!='inputHashes'},indent=2))
    raise SystemExit(0 if report['passed']else 1)
