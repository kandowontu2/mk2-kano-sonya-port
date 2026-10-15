"""Actual unassisted mirror victims, every Pit episode and native palette choice.

Accepts schema11 only: earlier observers did not record every exit and their
palette self-reads were reentrant. Keeps those captures diagnostic, not green.
Does not claim tower clear, impact-raster/audio or whole-port acceptance.
"""
import argparse
import json
import re
import struct
from pathlib import Path

from verify_native_pit_scene_v602_v4 import (ROOT, NAME, EXE, PAYLOAD, assets,
                                            rows, need, number, hexnum, digest)


def verify_health(log, intervals):
    sentinels = {}
    for r in rows(log, 'HEALTH'):
        before, after, at = number(r, 'before'), number(r, 'after'), hexnum(r, 'at')
        need(at in (0x010602F0, 0x01060EC0), 'Actual physical HP cells')
        if max(before, after) > 166:
            need(65535 in (before, after) and
                 all(not start <= number(r, 'frame') <= impact+1 for start, impact in intervals),
                 'No sentinel/corruption in any actual Pit episode')
            sentinels.setdefault(number(r, 'frame'), []).append(r)
        else:
            need(0 <= before <= 166 and 0 <= after <= 166, 'No corrupted HP')
    for values in sentinels.values():
        need([(number(r, 'slot'), hexnum(r, 'at'), number(r, 'before'),
               number(r, 'after'), hexnum(r, 'pc')) for r in values] ==
             [(1,0x010602F0,161,65535,0xFF9DECE0), (2,0x01060EC0,161,65535,0xFF9DED10),
              (1,0x010602F0,65535,4,0xFF9DEF40), (2,0x01060EC0,65535,4,0xFF9DEF70)],
             'Exact stock paired same-field bar-refill sentinel sequence')


def verify_log(log, fighter, reference, side=2):
    need(fighter in ('kano', 'sonya') and side == 2, 'Declared actual P2 mirror case')
    identity = 17 if fighter == 'kano' else 18
    sequence = 0xFF181000 if identity == 17 else 0xFF181200
    first_group = 0xFF182000+(identity-17)*6*64
    first_frame = 0xFF184000+(identity-17)*6*128
    need(not re.search(r'\[LUA ERROR\]|fatal error|access violation|stack traceback|REENTRY', log, re.I),
         'No observer/emulator error or reset reentry')
    observed = [line for line in log.splitlines() if line.startswith('MK2_NAT_CAMPAIGN_')]
    need(observed and all(f'human_slot={side} fighter={fighter} writes=0 assistance=none ' in line
                          for line in observed), 'All observations are declared slot and input-only')
    terminal = rows(log, 'RESULT')
    need(len(terminal) == 1, 'One actual terminal result')
    terminal = terminal[0]
    count = number(terminal, 'pit_episodes')
    need(number(terminal, 'schema') == 11 and count >= 1 and
         number(terminal, 'pit_lookups') == 2*count and number(terminal, 'frame') >= 49000 and
         number(terminal, 'reset') == number(terminal, 'ending') == -1,
         'Complete no-reset schema11 run, every episode accounted, not a tower clear')
    need(not any(hexnum(r,'entry') == 0xFFFFFFE0 for r in rows(log,'BOUNDARY')), 'No reset fetch')
    for tag in ('INPUT', 'HEALTH', 'FIGHT', 'STATE'):
        need(rows(log,tag) == rows(reference,tag), 'Exact unchanged full-run replay: '+tag)
    operands, coordinates, rom = rows(log,'PIT_OPERANDS'), rows(log,'PIT_COORDINATES'), rows(log,'PIT_ROM')
    need(len(operands)==1 and hexnum(operands[0],'first')==hexnum(operands[0],'second')==0xFF180800,
         'Both extended scene operands')
    need(len(coordinates)==1 and tuple(hexnum(coordinates[0],key) for key in ('operand','kano','sonya')) ==
         (0xFF180C00,0x004000C0,0x004000C0), 'Own native coordinate rows')
    need(len(rom)==19 and {number(r,'id'):hexnum(r,'value')for r in rom}[identity]==sequence,
         'Actual runtime own stream pointer')
    lookups, exits = rows(log,'PIT_LOOKUP'), rows(log,'PIT_EXIT')
    need(len(lookups)==2*count and len(exits)==count and
         [number(r,'episode')for r in lookups]==[i for i in range(1,count+1)for _ in range(2)] and
         [number(r,'episode')for r in exits]==list(range(1,count+1)), 'No omitted/duplicated episode')
    reference_lookups=rows(reference,'PIT_LOOKUP')
    keys=('frame','at','value','mask','pc','a8','a13','id','a1','table_slot','mode')
    need([tuple(r[k]for k in keys)for r in lookups]==
         [tuple(r[k]for k in keys)for r in reference_lookups],
         'Every actual native lookup also matches the complete original observer replay')
    all_draws=[r for r in rows(log,'DRAW')if hexnum(r,'entry')==0xFF838790 and
               first_group <= hexnum(r,'a0') <= first_group+5*64]
    need(len(all_draws)==21*count, 'All own fall/impact draws, not only first scene')
    # The same copier also draws the original bridge fall before the separate
    # front-facing constructor. Bind the latter to its actual owner/time;
    # don't silently drop an invalid source within that owner's scene.
    all_components=[r for r in rows(log,'COMPONENT')if any(
        number(lookups[i],'frame') <= number(r,'frame') <= number(lookups[i+1],'frame') and
        hexnum(r,'a8')==hexnum(lookups[i],'a8') and hexnum(r,'a13')==hexnum(lookups[i],'a13')
        for i in range(0,len(lookups),2))]
    need(len(all_components)==42*count, 'All bounded component reads, not only first scene')
    constructors, palettes = rows(log,'PIT_CONSTRUCTOR'), rows(log,'PIT_PALETTE')
    need(len(constructors)==2*count and len(palettes)==count, 'Nonreentrant complete constructor/palette reads')
    original=(ROOT/'mk3/mk3-maincpu.bin').read_bytes()
    palette_at=0x92BBC if fighter=='kano' else 0x92CF2
    colors=(0,)+struct.unpack_from('<64H',original,palette_at+4)
    palette_pointer=0xFFFED000 if fighter=='kano' else 0xFFFED800
    episodes=[]
    for index in range(count):
        a,b=lookups[2*index:2*index+2]
        episode=index+1
        actor,main=hexnum(a,'a8'),hexnum(a,'a13')
        start,impact=number(a,'frame'),number(b,'frame')
        need(impact==start+59,'Original native fall duration')
        for r in (a,b):
            need(tuple(hexnum(r,k) for k in ('at','value','mask','pc','a1','a8','a13'))==
                 (0xFF180800+identity*32,sequence&0xFFFF,0xFFFF,0xFF83B850,0xFF180800,actor,main) and
                 number(r,'id')==number(r,'table_slot')==identity and number(r,'mode')==9,
                 'Actual low-half lookup, true identity and same cinematic owner')
        entry,returned=constructors[2*index:2*index+2]
        need((number(entry,'episode'),number(entry,'frame'),hexnum(entry,'entry'),hexnum(entry,'pc'),
              hexnum(entry,'a0'),hexnum(entry,'a1'),hexnum(entry,'a2'),hexnum(entry,'a13'))==
             (episode,start,0xFF906EF0,0xFF906F00,identity,0,0,main), 'Stock Pit constructor A1/A2 cleared')
        need((number(returned,'episode'),number(returned,'frame'),hexnum(returned,'entry'),hexnum(returned,'pc'),
              hexnum(returned,'a8'),hexnum(returned,'a13'),number(returned,'id'),hexnum(returned,'body'))==
             (episode,start,0xFF85BC10,0xFF85BC20,actor,main,identity,2), 'Actual own normal body constructed')
        palette=palettes[index]
        need((number(palette,'episode'),number(palette,'frame'),number(palette,'variant'),number(palette,'id'),
              hexnum(palette,'table'),hexnum(palette,'at'),hexnum(palette,'pointer'),hexnum(palette,'value'),
              hexnum(palette,'mask'),hexnum(palette,'pc'),hexnum(palette,'a8'),hexnum(palette,'a13'))==
             (episode,start,0,identity,0xFFFEC000,0xFFFEC000+identity*32,palette_pointer,palette_pointer&0xFFFF,
              0xFFFF,0xFF9071A0,actor,main) and number(palette,'count')==65 and
             tuple(int(c,16)for c in palette['colors'].split(','))==colors, 'Actual own full normal source palette')
        prior=[r for r in rows(log,'BODY')if number(r,'frame')<start]
        need(prior,'Actual preceding mirror body observation')
        prior=prior[-1]
        bodies=tuple(int(c,16)for c in prior['bodies'].split(','))
        need(prior['human']==prior['cpu']==f'{identity}:{identity}' and
             bodies[0]&0x40 and not bodies[1]&0x40,'Actual alternate human / normal CPU mirror before Pit')
        draws=all_draws[21*index:21*index+21]
        components=all_components[42*index:42*index+42]
        for step,r in enumerate(draws):
            phase=step%5 if step<20 else 5
            at=start+1+step*3 if step<20 else impact
            need((hexnum(r,'a0'),number(r,'frame'),number(r,'actor_id'),hexnum(r,'a8'),hexnum(r,'a13'),
                  number(r,'x'),number(r,'y'),hexnum(r,'cache'),hexnum(r,'flags'),hexnum(r,'bank'))==
                 (first_group+phase*64,at,identity,actor,main,192,64,0x0105F230,2,hexnum(returned,'bank')),
                 'Every original-cadence own normal draw at physical P2 cache')
            parts=components[2*step:2*step+2]
            need([(number(c,'frame'),hexnum(c,'source'),hexnum(c,'value'),hexnum(c,'dst'),hexnum(c,'a8'),hexnum(c,'a13'))for c in parts]==
                 [(at,first_group+phase*64,first_frame+phase*128,0x0105F230,actor,main),
                  (at,first_group+phase*64+32,0,0x0105F2A0,actor,main)], 'Every bounded component/stop, no overwrite')
        exit=exits[index];end=number(exit,'frame')
        need((number(exit,'enter'),number(exit,'lookups'),number(exit,'total_lookups'),number(exit,'mode'))==
             (start,2,2*episode,5) and end==impact+2,'Each actual native scene completes')
        need(any(hexnum(r,'at')==0x010601D0 and number(r,'before')==9 and number(r,'after')==5 and
                 hexnum(r,'pc')==0xFF820390 and number(r,'frame')==end-1 for r in rows(log,'TRANSITION')),
             'Original native completion, not observer skip')
        losses=[r for r in rows(log,'LOSS')if number(r,'frame')>end]
        selections=[r for r in rows(log,'SELECT')if number(r,'frame')>end]
        fights=[r for r in rows(log,'FIGHT')if number(r,'frame')>end]
        need(losses and selections and fights,'Each Pit followed by paid continue and next fight')
        loss,selection,fight=losses[0],selections[0],fights[0]
        need(number(selection,'continue')==number(loss,'frame') and number(selection,'target')==identity and
             number(fight,'selection')==number(selection,'number') and fight['human']==fight['cpu']==f'{identity}:{identity}',
             'Each continued mirror fight retains own identity')
        for button in ('Coin','Start'):
            need(any(r['button']==button and number(loss,'frame')<number(r,'frame')<number(selection,'frame')
                     for r in rows(log,'INPUT')),'Actual paid continue '+button)
        live=[r for r in rows(log,'LIVE')if number(r,'selection')==number(selection,'number') and
              number(r,'frame')>=number(fight,'frame')]
        need(len(live)>=10 and number(live[-1],'frame')-number(live[0],'frame')>=300 and
             all(r['human']==f'{identity}:{identity}' for r in live),'Sustained own post-Pit fight')
        episodes.append(dict(episode=episode,pit_enter=start,pit_impact=impact,pit_exit=end,next_fight=number(fight,'frame'),
                             native_falling_groups=20,native_impact_groups=1,bounded_component_reads=42,
                             actual_pre_Pit_costume='alternate',actual_native_Pit_palette='normal',palette_colors=65))
    verify_health(log,[(e['pit_enter'],e['pit_impact'])for e in episodes])
    need(all(0<=number(r,'mode')<=13 and all(0<=int(h)<=166 for h in r['health'].split(','))for r in rows(log,'STATE')),
         'No gameplay-global corruption')
    return dict(passed=True,fighter=fighter,human_slot=side,actual_id=identity,episodes=episodes,
                terminal_frame=number(terminal,'frame'),reset_observed=False,fullPortAcceptance=False,
                scope='Actual P2 mirror victims: every native Pit episode, original normal-palette reconstruction, bounded draws and paid continues. Not cleared towers, complete impact raster/audio or whole-port acceptance.')


def check_capture(folder,fighter,side):
    folder=Path(folder)
    metadata=json.loads((folder/'result.json').read_text(encoding='utf-8-sig'))
    manifest=json.loads((folder/'input_hashes_before.json').read_text(encoding='utf-8-sig'))
    need((metadata['exit_code'],metadata['candidate'],metadata['executable_sha256'],metadata['payload_sha256'],
          metadata['player'],metadata['human_slot'],metadata['assistance'])==(0,NAME,EXE,PAYLOAD,fighter,side,'none'),
         'Exact complete matched input-only launch')
    need(manifest==metadata['input_hashes'],'Actual before/after input inventory')
    for path,expected in manifest.items():need(digest(path)==expected,'Changed capture input: '+path)
    return folder


def verify(folder,fighter,reference_folder):
    folder=check_capture(folder,fighter,2);reference_folder=check_capture(reference_folder,fighter,2)
    build=json.loads((ROOT/NAME/'build-info.json').read_text(encoding='utf-8-sig'))
    need((build['name'],build['executable_sha256'],build['payload_sha256'])==(NAME,EXE,PAYLOAD),'Exact compiled candidate')
    for path,expected in build['input_hashes'].items():need(digest(path)==expected,'Changed build input: '+path)
    observer=(folder/'input_sources/mk2ks_natural_campaign_probe_v11.lua').read_text()
    need(not re.search(r'write_u\d+|:write_|load_?state|\.value\s*=(?!=)|dofile\(',observer),'No observer guest writes')
    need('-nocheat' in (folder/'input_sources/run_natural_campaign_probe_v11.ps1').read_text(),'No cheats')
    proof=verify_log((folder/'run.log').read_text(encoding='utf-8-sig'),fighter,
                     (reference_folder/'run.log').read_text(encoding='utf-8-sig'))
    proof['asset_integrity']=assets((ROOT/NAME/'roms/mk2ks/mk2ks.mdata').read_bytes(),
                                   (ROOT/'diagnostic_v545_native_roll_edge_clearance/roms/mk2ks/mk2ks.mdata').read_bytes(),
                                   (ROOT/'mk2/mk2-maincpu.bin').read_bytes())
    for episode in proof['episodes']:
        end=episode['pit_exit']
        need((folder/'snap'/f'campaign_pit_post_{((end+2)//3)*3}.png').is_file(),'Each post-impact raster retained')
    return proof


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('folder',type=Path);parser.add_argument('fighter',choices=('kano','sonya'))
    parser.add_argument('reference',type=Path);args=parser.parse_args()
    print(json.dumps(verify(args.folder,args.fighter,args.reference),indent=2))
