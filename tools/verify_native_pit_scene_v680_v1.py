"""Real Pit victims in either physical slot, native phases and continuation.

The ROM read tap is 16-bit: its value is the low HALF of the full stream
pointer. Full runtime boot readouts and actual A9/group execution corroborate
the pointer; do not describe value=1000 as a malformed full pointer.
"""
import argparse
import hashlib
import json
import re
from pathlib import Path

from verify_native_pit_assets_v602 import verify as assets

ROOT = Path(__file__).resolve().parents[1]
NAME = 'diagnostic_v680_native_pit_initial_cache'
EXE = 'AD98FE42383F776BBD49BA4298EFD1F9F021FD2988C6B0A3956EE64316B44E82'
PAYLOAD = '1367D5A0D42C661CF555F42231A20A650C28E107AB9C80BD821C0BEA7EB4D5EF'


def need(ok, message):
    if not ok: raise ValueError(message)


def digest(path): return hashlib.sha256(Path(path).read_bytes()).hexdigest().upper()
def number(row, key): return int(row[key])
def hexnum(row, key): return int(row[key], 16)


def rows(log, tag):
    return [dict(re.findall(r'([a-zA-Z_][a-zA-Z_0-9]*)=([^\s]+)', line))
            for line in log.splitlines() if line.startswith('MK2_NAT_CAMPAIGN_'+tag+' ')]


def verify_log(log, fighter, reference=None, side=1):
    need(fighter in ('kano','sonya'), 'Declared own character')
    need(side in (1,2),'Actual declared physical slot')
    identity = 17 if fighter=='kano' else 18
    sequence = 0xFF181000 if identity==17 else 0xFF181200
    first_group = 0xFF182000 + (identity-17)*6*64
    first_frame = 0xFF184000 + (identity-17)*6*128
    need(not re.search(r'\[LUA ERROR\]|fatal error|access violation|stack traceback|REENTRY',log,re.I), 'No observer/emulator error or reset reentry')
    observations = [line for line in log.splitlines() if line.startswith('MK2_NAT_CAMPAIGN_')]
    need(observations and all(f'human_slot={side} fighter={fighter} writes=0 assistance=none ' in line for line in observations), 'All observations are actual declared slot and input-only')
    result = rows(log,'RESULT')
    need(len(result)==1, 'One complete terminal observer')
    result = result[0]
    need(number(result,'schema')==12 and number(result,'reset')==-1 and number(result,'ending')==-1 and
         number(result,'pit_episodes')>=1 and number(result,'pit_lookups')==2*number(result,'pit_episodes') and
         number(result,'frame')>=21000, 'Complete bounded no-reset run and every recorded episode, not a tower clear')
    need(not any(hexnum(r,'entry')==0xFFFFFFE0 for r in rows(log,'BOUNDARY')), 'No actual native reset-vector fetch')
    operands=rows(log,'PIT_OPERANDS');positions=rows(log,'PIT_COORDINATES');rom=rows(log,'PIT_ROM')
    need(len(operands)==1 and hexnum(operands[0],'first')==hexnum(operands[0],'second')==0xFF180800,'Both actual scene operands extended')
    need(len(positions)==1 and tuple(hexnum(positions[0],k)for k in ('operand','kano','sonya'))==
         (0xFF180C00,0x004000C0,0x004000C0),'Native constructor has own centered coordinate rows')
    need(len(rom)==19 and {number(r,'id'):hexnum(r,'value')for r in rom}[identity]==sequence,'Full actual own runtime stream pointer')
    lookups=rows(log,'PIT_LOOKUP');exits=rows(log,'PIT_EXIT');episodes=[]
    count=number(result,'pit_episodes')
    need(len(lookups)==2*count and len(exits)==count,'Every episode has exactly fall/impact and native exit')
    need([number(r,'episode')for r in lookups]==[i for i in range(1,count+1)for _ in range(2)] and
         [number(r,'episode')for r in exits]==list(range(1,count+1)),'Complete ordered actual episodes')
    components=rows(log,'COMPONENT')
    cache=0x0105ED30 if side==1 else 0x0105F230
    for episode in range(count):
        pair=lookups[episode*2:episode*2+2]
        actor,main=hexnum(pair[0],'a8'),hexnum(pair[0],'a13')
        for r in pair:
            need((hexnum(r,'at'),hexnum(r,'value'),hexnum(r,'mask'),hexnum(r,'pc'),hexnum(r,'a1'),number(r,'id'),
                  number(r,'table_slot'),number(r,'mode'),hexnum(r,'a8'),hexnum(r,'a13'))==
                 (0xFF180800+identity*32,sequence&0xFFFF,0xFFFF,0xFF83B850,0xFF180800,identity,identity,9,actor,main),
                 'Actual native load low-half, true ID and same cinematic owner')
        enter,hit=number(pair[0],'frame'),number(pair[1],'frame')
        need(hit-enter==59,'Exact complete original sixty-field fall duration')
        draws=[r for r in rows(log,'DRAW') if hexnum(r,'entry')==0xFF838790 and
               enter<=number(r,'frame')<=hit and first_group<=hexnum(r,'a0')<=first_group+5*64]
        need(len(draws)==22,'One synchronous preload, twenty original-cadence falling groups and own impact')
        for index,r in enumerate(draws):
            phase=0 if index==0 else (index-1)%5 if index<=20 else 5
            expected_frame=enter if index==0 else enter+1+(index-1)*3 if index<=20 else hit
            need((hexnum(r,'a0'),number(r,'frame'),number(r,'actor_id'),hexnum(r,'a8'),hexnum(r,'a13'),hexnum(r,'cache'))==
                 (first_group+phase*64,expected_frame,identity,actor,main,cache),
                 'Exact native preload/stream/cadence/real owner and physical cache')
            if index:
                need((number(r,'x'),number(r,'y'))==(192,64),'Native centered constructor origin')
            parts=[c for c in components if number(c,'frame')==expected_frame and hexnum(c,'a8')==actor and
                   first_group+phase*64<=hexnum(c,'source')<=first_group+phase*64+32]
            need(tuple((hexnum(c,'source'),hexnum(c,'value'),hexnum(c,'dst'),hexnum(c,'a13'))for c in parts)==
                 ((first_group+phase*64,first_frame+phase*128,cache,main),
                  (first_group+phase*64+32,0,cache+112,main)), 'Exact bounded native component-cache copy and zero terminator')
        end=exits[episode]
        exit_at=number(end,'frame')
        need((number(end,'enter'),number(end,'lookups'),number(end,'mode'),number(end,'total_lookups'),exit_at)==
             (enter,2,5,(episode+1)*2,hit+2),'Actual native scene completion for every episode')
        need(any(hexnum(r,'at')==0x010601D0 and number(r,'before')==9 and number(r,'after')==5 and
                 hexnum(r,'pc')==0xFF820390 and number(r,'frame')==exit_at-1 for r in rows(log,'TRANSITION')),
             'Original native completion, not observer exit/reset')
        losses=[r for r in rows(log,'LOSS')if number(r,'frame')>exit_at]
        selections=[r for r in rows(log,'SELECT')if number(r,'frame')>exit_at]
        fights=[r for r in rows(log,'FIGHT')if number(r,'frame')>exit_at]
        need(losses and selections and fights,'Each actual scene has loss/paid continue/reselection/fight')
        loss,selection,fight=losses[0],selections[0],fights[0]
        need(number(selection,'continue')==number(loss,'frame') and number(selection,'target')==identity and
             number(fight,'selection')==number(selection,'number') and fight['human']==f'{identity}:{identity}',
             'Every continued fight owns actual selected identity')
        for button in ('Coin','Start'):
            need(any(r['button']==button and number(loss,'frame')<number(r,'frame')<number(selection,'frame')for r in rows(log,'INPUT')),
                 'Genuine paid-continue button '+button)
        live=[r for r in rows(log,'LIVE')if number(r,'selection')==number(selection,'number') and number(r,'frame')>=number(fight,'frame')]
        need(len(live)>=10 and number(live[-1],'frame')-number(live[0],'frame')>=300 and all(r['human']==f'{identity}:{identity}'for r in live),
             'Sustained post-Pit fight after every episode')
        episodes.append(dict(number=episode+1,actor=actor,main=main,pit_enter=enter,pit_impact=hit,pit_exit=exit_at,next_fight=number(fight,'frame')))
    start,impact,exit_at=(episodes[0][k]for k in ('pit_enter','pit_impact','pit_exit'))
    health=rows(log,'HEALTH')
    sentinels={}
    for r in health:
        before,after=number(r,'before'),number(r,'after')
        need(hexnum(r,'at') in (0x010602F0,0x01060EC0),'Actual physical HP cells')
        if before>166 or after>166:
            # Original FF9DEC90 writes FFFF to BOTH HP cells before the
            # FF9DEEB0 bar-refill loop writes 4 in the SAME field. This is
            # stock scene-init bookkeeping, not the Pit's 7E7E overrun.
            need(65535 in (before,after) and not any(e['pit_enter']<=number(r,'frame')<=e['pit_impact']+1 for e in episodes),
                 'No sentinel/corruption during actual Pit execution')
            sentinels.setdefault(number(r,'frame'),[]).append(r)
        else:
            need(0<=before<=166 and 0<=after<=166,'Physical HP globals never corrupted')
    for frame,values in sentinels.items():
        actual=[(number(r,'slot'),hexnum(r,'at'),number(r,'before'),number(r,'after'),hexnum(r,'pc'))for r in values]
        need(actual==[(1,0x010602F0,161,65535,0xFF9DECE0),(2,0x01060EC0,161,65535,0xFF9DED10),
                      (1,0x010602F0,65535,4,0xFF9DEF40),(2,0x01060EC0,65535,4,0xFF9DEF70)],
             'Exact original paired same-field FFFF-to-4 bar-refill sequence')
    for r in rows(log,'STATE'):
        # Mode13 is the original arena intro between native selection and
        # fight mode2 (present in the unchanged baseline before this patch).
        need(0<=number(r,'mode')<=13 and all(0<=int(h)<=166 for h in r['health'].split(',')), 'No gameplay-global corruption')
    if reference is not None:
        for tag in ('INPUT','HEALTH','FIGHT','STATE'):
            prefix=lambda text:[r for r in rows(text,tag) if number(r,'frame')<=start]
            need(prefix(log)==prefix(reference),'Unchanged pre-Pit actual '+tag+' replay')
    return dict(passed=True,fighter=fighter,human_slot=side,actual_id=identity,pit_enter=start,pit_impact=impact,
                pit_exit=exit_at,native_initial_groups=1,native_falling_groups=20,native_impact_groups=1,bounded_component_reads=44,
                episodes=episodes,next_fight=episodes[0]['next_fight'],terminal_frame=number(result,'frame'),reset_observed=False,
                scope='actual_declared_slot_Pit_victim_phases_centered_origin_cache_cleanup_and_paid_continue_not_alternate_visual_audio_or_full_campaign',
                fullPortAcceptance=False)


def verify(folder,fighter,reference_folder=None,side=1):
    folder=Path(folder)
    reference_folder=Path(reference_folder)if reference_folder is not None else None
    metadata=json.loads((folder/'result.json').read_text(encoding='utf-8-sig'))
    manifest=json.loads((folder/'input_hashes_before.json').read_text(encoding='utf-8-sig'))
    build=json.loads((ROOT/NAME/'build-info.json').read_text(encoding='utf-8-sig'))
    need((metadata['exit_code'],metadata['candidate'],metadata['executable_sha256'],metadata['payload_sha256'],
          metadata['player'],metadata['human_slot'],metadata['assistance'])==(0,NAME,EXE,PAYLOAD,fighter,side,'none'), 'Exact terminal matched launch')
    need(manifest==metadata['input_hashes'],'Input hashes checked before/after capture')
    need((build['name'],build['executable_sha256'],build['payload_sha256'])==(NAME,EXE,PAYLOAD),'Exact compiled candidate')
    for path,expected in {**manifest,**build['input_hashes']}.items(): need(digest(path)==expected,'Input changed: '+path)
    need(digest(ROOT/NAME/'mkport_candidate.exe')==EXE and digest(ROOT/NAME/'roms/mk2ks/mk2ks.mdata')==PAYLOAD,'Actual executable/payload')
    observer=(folder/'input_sources/mk2ks_natural_campaign_probe_v12.lua').read_text()
    need(not re.search(r'write_u\d+|:write_|load_?state|\.value\s*=(?!=)|dofile\(',observer),'Observer supplies no guest state')
    display=(folder/'input_sources/mk2ks_natural_pit_display_v680_v1.lua').read_text()
    need("dofile('mk2ks_natural_campaign_probe_v12.lua')" in display,'Exact real-input scenario with updated read-only provenance')
    need(not re.search(r'write_u\d+|:write_|load_?state|\.value\s*=(?!=)',display),'Display observer supplies no guest state')
    runner_names=[name for name in ('run_natural_pit_raster_v680_v1.ps1',)
                  if (folder/'input_sources'/name).is_file()]
    need(len(runner_names)==1,'Exactly one actual declared current Pit runner')
    runner=(folder/'input_sources'/runner_names[0]).read_text()
    if runner_names[0].startswith('run_natural_pit_raster_'):
        name=runner_names[0].replace('run_natural_pit_raster_','mk2ks_natural_pit_raster_').replace('.ps1','.lua')
        raster=(folder/'input_sources'/name).read_text()
        need("dofile('mk2ks_natural_pit_display_v680_v1.lua')" in raster,'Exact nested current Pit scenario')
        need(not re.search(r'write_u\d+|:write_|load_?state|\.value\s*=(?!=)',raster),'Raster observer supplies no guest state')
    need('-nocheat' in runner and '-noautoframeskip -frameskip 0' in runner and
         ('-wavwrite' in runner or 'register_sound_update' in raster),'Cheat-disabled complete native display/audio capture')
    asset_proof=assets((ROOT/NAME/'roms/mk2ks/mk2ks.mdata').read_bytes(),
                       (ROOT/'diagnostic_v545_native_roll_edge_clearance/roms/mk2ks/mk2ks.mdata').read_bytes(),
                       (ROOT/'mk2/mk2-maincpu.bin').read_bytes())
    reference=(reference_folder/'run.log').read_text(encoding='utf-8-sig')if reference_folder is not None else None
    proof=verify_log((folder/'run.log').read_text(encoding='utf-8-sig'),fighter,reference,side)
    need((folder/'snap'/f"campaign_pit_post_{((proof['pit_exit']+2)//3)*3}.png").is_file(),'Post-impact rendered evidence retained')
    proof['asset_integrity']=asset_proof
    return proof


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('folder',type=Path);parser.add_argument('fighter',choices=('kano','sonya'))
    parser.add_argument('--reference',type=Path);parser.add_argument('--side',type=int,choices=(1,2),default=1);args=parser.parse_args()
    print(json.dumps(verify(args.folder,args.fighter,args.reference,args.side),indent=2))
