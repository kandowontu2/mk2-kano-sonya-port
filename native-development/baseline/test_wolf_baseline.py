"""Run Wolf baseline using stock MK3 hardware and ROM socket definitions."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import zipfile
import wave
import array
import re
import os
import shutil
from test_rom_cache import prepare_archive
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
BUILD=HERE/'mk2-rebuild-main'
OUT=HERE/(sys.argv[1] if len(sys.argv)>1 else 'stock_wolf_test')
MAME=ROOT.parent/'mame0289/mame.exe'
def sha(b): return hashlib.sha256(b).hexdigest().upper()
def main():
    assert not OUT.exists()
    if '--campaign-boss-endurance' in sys.argv:
        assert all(flag in sys.argv for flag in ('--game','--campaign','--campaign-full','--campaign-extra-continues','--campaign-ending-window','--campaign-finale-window','--campaign-background-margin'))
    replacements={}
    game_candidate='--game' in sys.argv
    if '--normal-soak' in sys.argv:
        assert game_candidate and '--normal-moves' in sys.argv
    sound_tracks=[arg.split('=',1)[1] for arg in sys.argv if arg.startswith('--sound-chicken-track=')]
    assert len(sound_tracks)<=1 and all(track in ('1','2','3') for track in sound_tracks)
    sound_track=int(sound_tracks[0]) if sound_tracks else 0
    if sound_track:assert '--friend' in sys.argv and '--audio' in sys.argv and '--sound-chicken-muted' not in sys.argv
    if '--finisher-morph' in sys.argv:
        assert game_candidate and any(flag in sys.argv for flag in ('--extract','--kiss','--laser','--bubble','--friend','--baby'))
        if '--finisher-rejoin' in sys.argv:
            assert any(flag in sys.argv for flag in ('--extract','--kiss','--laser','--bubble'))
    if '--campaign-sonya-kintaro-evade' in sys.argv:
        assert game_candidate and '--campaign' in sys.argv and '--sonya' in sys.argv
    if '--campaign-sonya-kintaro-early-evade' in sys.argv:
        assert '--campaign-sonya-kintaro-evade' in sys.argv
    if '--campaign-sonya-kahn-guard' in sys.argv:
        assert game_candidate and '--campaign' in sys.argv and '--sonya' in sys.argv
    if '--campaign-sonya-kahn-contact-ready' in sys.argv:
        assert '--campaign-sonya-kahn-guard' in sys.argv
    if '--campaign-sonya-kahn-opening-jump' in sys.argv:
        assert '--campaign-sonya-kahn-guard' in sys.argv
    if '--campaign-capture-ending' in sys.argv:
        assert game_candidate and '--campaign' in sys.argv
    if '--campaign-ending-state' in sys.argv:
        assert '--campaign-capture-ending' in sys.argv
    if '--campaign-kano-sub-jump' in sys.argv:
        assert game_candidate and '--campaign' in sys.argv and '--campaign-subzero-guard' in sys.argv and '--sonya' not in sys.argv
    if '--campaign-kano-sub-jump-hold' in sys.argv:
        assert '--campaign-kano-sub-jump' in sys.argv
    if '--campaign-kano-sub-range-kick' in sys.argv:
        assert '--campaign-kano-sub-jump-hold' in sys.argv
    if '--campaign-kano-sub-ball' in sys.argv:
        assert game_candidate and '--campaign' in sys.argv and '--campaign-subzero-guard' in sys.argv and '--sonya' not in sys.argv
        assert '--campaign-kano-sub-jump' not in sys.argv
    if '--campaign-kano-sub-standing-charge' in sys.argv:
        assert '--campaign-kano-sub-ball' in sys.argv
    if '--campaign-kano-sub-adaptive-charge' in sys.argv:
        assert '--campaign-kano-sub-standing-charge' in sys.argv
    if '--campaign-kano-sub-ball-counter' in sys.argv:
        assert '--campaign-kano-sub-adaptive-charge' in sys.argv and '--campaign-subzero-rfp-duck' in sys.argv
    if '--campaign-kano-sub-recovery-counter' in sys.argv:
        assert '--campaign-kano-sub-ball-counter' in sys.argv
    if '--campaign-kano-sub-recovery-ball' in sys.argv:
        assert '--campaign-kano-sub-recovery-counter' in sys.argv
    if '--campaign-kano-sub-recharge' in sys.argv:
        assert '--campaign-kano-sub-recovery-ball' in sys.argv
    if '--campaign-kano-sub-approach' in sys.argv:
        assert '--campaign-kano-sub-recharge' in sys.argv
    if '--campaign-kano-sub-postball-guard' in sys.argv:
        assert '--campaign-kano-sub-recharge' in sys.argv
    if '--campaign-kano-sub-neutral-uppercut' in sys.argv:
        assert '--campaign-kano-sub-normal-throw' in sys.argv
    if '--campaign-kano-mileena-prepare' in sys.argv:
        assert '--campaign-kano-sub-neutral-uppercut' in sys.argv
    if '--campaign-kano-human-prepare' in sys.argv:
        assert '--campaign-kano-mileena-prepare' in sys.argv
    if '--campaign-kano-boss-guard' in sys.argv:
        assert '--campaign-kano-human-prepare' in sys.argv and '--campaign-subzero-rfp-duck' in sys.argv
        assert '--sonya' not in sys.argv
    if '--campaign-kano-kintaro-prepare' in sys.argv:
        assert '--campaign-kano-boss-guard' in sys.argv
    if '--campaign-kano-kintaro-jumpkick' in sys.argv:
        assert '--campaign-kano-boss-guard' in sys.argv
        assert '--campaign-kano-kintaro-prepare' not in sys.argv
    if '--campaign-kano-kintaro-wide-prepare' in sys.argv:
        assert '--campaign-kano-boss-guard' in sys.argv
        assert not any(flag in sys.argv for flag in ('--campaign-kano-kintaro-prepare','--campaign-kano-kintaro-jumpkick'))
    if '--campaign-kano-kintaro-blade' in sys.argv:
        assert '--campaign-kano-boss-guard' in sys.argv
        assert not any(flag in sys.argv for flag in ('--campaign-kano-kintaro-prepare','--campaign-kano-kintaro-jumpkick','--campaign-kano-kintaro-wide-prepare'))
    if '--campaign-kano-kintaro-knife' in sys.argv:
        assert '--campaign-kano-boss-guard' in sys.argv
        assert not any(flag in sys.argv for flag in ('--campaign-kano-kintaro-prepare','--campaign-kano-kintaro-jumpkick','--campaign-kano-kintaro-wide-prepare','--campaign-kano-kintaro-blade'))
    if '--campaign-kano-kintaro-mixed' in sys.argv:
        assert '--campaign-kano-boss-guard' in sys.argv
        assert not any(flag in sys.argv for flag in ('--campaign-kano-kintaro-prepare','--campaign-kano-kintaro-jumpkick','--campaign-kano-kintaro-wide-prepare','--campaign-kano-kintaro-blade','--campaign-kano-kintaro-knife'))
    if '--campaign-kano-kintaro-mixed-guard' in sys.argv:
        assert '--campaign-kano-kintaro-mixed' in sys.argv
    if '--campaign-kano-kintaro-knife-midrange' in sys.argv:
        assert '--campaign-kano-kintaro-knife' in sys.argv
    if '--campaign-kano-kintaro-knife-ready' in sys.argv:
        assert '--campaign-kano-kintaro-knife-midrange' in sys.argv
    if '--campaign-kano-kintaro-evade-counter' in sys.argv:
        assert '--campaign-kano-boss-guard' in sys.argv and '--campaign-subzero-rfp-duck' in sys.argv
        assert '--sonya' not in sys.argv
        assert not any(arg.startswith('--campaign-kano-kintaro-') and
                       arg!='--campaign-kano-kintaro-evade-counter' for arg in sys.argv)
    if '--campaign-kano-kintaro-short-kick' in sys.argv:
        assert '--campaign-kano-boss-guard' in sys.argv and '--campaign-subzero-rfp-duck' in sys.argv
        assert '--sonya' not in sys.argv
        assert not any(arg.startswith('--campaign-kano-kintaro-') and
                       arg!='--campaign-kano-kintaro-short-kick' for arg in sys.argv)
    if '--campaign-kano-kintaro-retreat-ball' in sys.argv:
        assert '--campaign-kano-boss-guard' in sys.argv and '--campaign-subzero-rfp-duck' in sys.argv
        assert '--sonya' not in sys.argv
        assert not any(arg.startswith('--campaign-kano-kintaro-') and
                       arg not in ('--campaign-kano-kintaro-retreat-ball','--campaign-kano-kintaro-retreat-ball-finish-knife') for arg in sys.argv)
    if '--campaign-kano-kintaro-retreat-ball-finish-knife' in sys.argv:
        assert '--campaign-kano-kintaro-retreat-ball' in sys.argv
    if '--campaign-kano-kintaro-fast-pulse' in sys.argv:
        assert '--campaign-kano-boss-guard' in sys.argv
        assert not any(flag in sys.argv for flag in ('--campaign-kano-kintaro-prepare','--campaign-kano-kintaro-wide-prepare','--campaign-kano-kintaro-jumpkick','--campaign-kano-kintaro-blade','--campaign-kano-kintaro-knife','--campaign-kano-kintaro-mixed'))
    if '--campaign-kano-kintaro-ready-counter' in sys.argv:
        assert '--campaign-kano-boss-guard' in sys.argv
        assert not any(flag in sys.argv for flag in ('--campaign-kano-kintaro-prepare','--campaign-kano-kintaro-wide-prepare','--campaign-kano-kintaro-jumpkick','--campaign-kano-kintaro-blade','--campaign-kano-kintaro-knife','--campaign-kano-kintaro-mixed','--campaign-kano-kintaro-fast-pulse'))
    ready_ranges=[arg.split('=',1)[1] for arg in sys.argv if arg.startswith('--campaign-kano-kintaro-ready-range=')]
    if '--campaign-kano-kintaro-early-counter' in sys.argv:
        assert '--campaign-kano-kintaro-ready-counter' in sys.argv
    if '--campaign-kano-kintaro-varied' in sys.argv:
        assert '--campaign-kano-boss-guard' in sys.argv and '--campaign-subzero-rfp-duck' in sys.argv
        assert '--sonya' not in sys.argv
        assert not any(arg.startswith('--campaign-kano-kintaro-') and arg not in ('--campaign-kano-kintaro-varied','--campaign-kano-kintaro-varied-counter','--campaign-kano-kintaro-varied-adaptive','--campaign-kano-kintaro-stomp-refresh','--campaign-kano-kintaro-stomp-momentum') for arg in sys.argv)
    if '--campaign-kano-kintaro-stomp-refresh' in sys.argv:
        assert '--campaign-kano-kintaro-varied' in sys.argv
    if '--campaign-kano-kintaro-stomp-momentum' in sys.argv:
        assert '--campaign-kano-kintaro-stomp-refresh' in sys.argv
    if '--campaign-kano-kintaro-varied-counter' in sys.argv:
        assert '--campaign-kano-kintaro-varied' in sys.argv
    if '--campaign-kano-kintaro-varied-adaptive' in sys.argv:
        assert '--campaign-kano-kintaro-varied' in sys.argv
        assert '--campaign-kano-kintaro-varied-counter' not in sys.argv
    assert len(ready_ranges)<=1 and (not ready_ranges or ready_ranges[0] in ('84','104','115'))
    assert not ready_ranges or '--campaign-kano-kintaro-ready-counter' in sys.argv
    if '--campaign-kano-sub-normal-throw' in sys.argv:
        assert game_candidate and '--campaign' in sys.argv and '--campaign-subzero-guard' in sys.argv
        assert not any(flag in sys.argv for flag in ('--sonya','--campaign-kano-sub-ball','--campaign-kano-sub-jump'))
    if '--morph-ball' in sys.argv:
        assert game_candidate and '--morph' in sys.argv
        assert '--morph-specials' not in sys.argv and '--morph-throws' not in sys.argv
    if '--morph-melee' in sys.argv:
        assert game_candidate and '--morph' in sys.argv
        assert not any(flag in sys.argv for flag in ('--morph-specials','--morph-throws','--morph-ball'))
    if '--morph-grapples' in sys.argv:
        assert game_candidate and '--morph' in sys.argv
        assert not any(flag in sys.argv for flag in ('--morph-specials','--morph-throws','--morph-ball','--morph-melee'))
    if '--morph-square' in sys.argv:
        assert game_candidate and '--morph' in sys.argv
        assert not any(flag in sys.argv for flag in ('--morph-specials','--morph-throws','--morph-ball','--morph-melee','--morph-grapples'))
    if '--choke-fast-command' in sys.argv:
        assert game_candidate and '--choke' in sys.argv
    if '--choke-crouch-entry' in sys.argv:
        assert '--choke-fast-command' in sys.argv
    if '--campaign-full' in sys.argv:
        assert game_candidate and '--campaign' in sys.argv and '--cpu-attract' not in sys.argv
    if '--campaign-extended' in sys.argv:
        assert '--campaign-full' in sys.argv
    if '--campaign-ending-window' in sys.argv:
        assert '--campaign-extended' in sys.argv
    if '--campaign-finale-window' in sys.argv:
        assert '--campaign-ending-window' in sys.argv
    if '--campaign-background-margin' in sys.argv:
        assert '--campaign-finale-window' in sys.argv
    if '--campaign-extra-continues' in sys.argv:
        assert '--campaign-extended' in sys.argv
    cycle_scene='--cycle' in sys.argv
    art_scene='--art' in sys.argv or cycle_scene
    assert not (game_candidate and art_scene), 'Choose gameplay or diagnostic, not both'
    for lane,n in [(0,'mk321u54.bin'),(1,'mk321u63.bin')]:
        prefix='P12' if game_candidate else ('C12' if cycle_scene else ('A12' if art_scene else 'U12'))
        source='srcp' if game_candidate else 'srcw'
        replacements[n]=b''.join((BUILD/f'{source}/rom/{prefix}{part}.{lane}').read_bytes() for part in ['F8','FC'])
        assert len(replacements[n])==524288
    # Both boards use four byte lanes; copy MKII's three 4-MiB banks to
    # the corresponding physical Wolf graphics sockets. No emulator remapping.
    with zipfile.ZipFile(ROOT/'roms/mk2.zip') as mk2:
        for bank,(first,second) in enumerate([(14,19),(16,20),(17,22)]):
            for lane,(letter,socket) in enumerate([('ug',first),('uj',first),('ug',second),('uj',second)]):
                src=f'l1_mortal_kombat_ii_game_rom_{letter}{socket}.{letter}{socket}'
                dest=f'l1_mortal_kombat_3_u{133-bank*4-lane}_game_rom.u{133-bank*4-lane}'
                replacements[dest]=mk2.read(src)
    for chip in range(2,6):
        sound_directory='soundp' if '--sound-candidate' in sys.argv else 'soundw'
        if '--sound-chicken-muted' in sys.argv or sound_track:
            assert '--sound-candidate' not in sys.argv
            control=HERE/(f'chicken_track{sound_track}_control' if sound_track else 'chicken_muted_control')
            assert (control/'OK.TXT').read_text().strip()=='DONE'
            assert not (control/'FAIL.TXT').exists()
            data=(control/f'U{chip}.ROM').read_bytes()
        else:
            data=(BUILD/f'{sound_directory}/U{chip}.ROM').read_bytes()
        assert len(data)==1048576
        replacements[f'l1_mortal_kombat_3_u{chip}_music_spch.u{chip}']=data
    environment=os.environ.copy()
    finisher_victims=[arg.split('=',1)[1] for arg in sys.argv if arg.startswith('--finisher-victim=')]
    assert len(finisher_victims)<=1
    if finisher_victims:
        assert game_candidate and sum(flag in sys.argv for flag in ('--extract','--laser','--kiss','--bubble'))==1
        assert int(finisher_victims[0]) in (*range(12),17,18)
        assert '--stock-victim' not in sys.argv and '--finisher-morph' not in sys.argv
    environment['KS_FINISHER_MORPH']='1' if '--finisher-morph' in sys.argv else '0'
    if '--finisher-morph' in sys.argv or finisher_victims:
        nav=(HERE.parent/'port/asm/KSNAV.ASM').read_text()
        for direction in ('up','down','left','right'):
            match=re.search(r'(?m)^ks_'+direction+r'_change\s*\n\s*\.word\s+([^\n]+)',nav)
            assert match
            environment['KS_SELECT_'+direction.upper()]=match[1].strip()
    probe=HERE/'probe.lua'
    if game_candidate:
        environment['KS_FINISH_REJOIN']='1' if '--finisher-rejoin' in sys.argv else '0'
        environment['KS_CAPTURE_FINISH']='1' if '--capture-finish' in sys.argv else '0'
        capture_background=[arg.split('=',1)[1] for arg in sys.argv if arg.startswith('--capture-background=')]
        assert len(capture_background)<=1
        capture_bg=int(capture_background[0]) if capture_background else -1
        assert capture_bg in (-1,0,1,6)
        environment['KS_CAPTURE_BACKGROUND']=str(capture_bg)
        if '--cpu-attract' in sys.argv:
            probe=HERE.parent/'port/diagnostics/cpu_attract_probe.lua'
            environment['KS_CPU_FIELDS']='42000' if '--cpu-long' in sys.argv else '30000'
            environment['KS_CPU_ACK_START']='2500' if '--startup-late' in sys.argv else '0'
        if '--campaign' in sys.argv:
            continue_args=[arg.split('=',1)[1] for arg in sys.argv if arg.startswith('--campaign-continues=')]
            assert len(continue_args)<=1
            continue_count=int(continue_args[0]) if continue_args else 0
            if '--campaign-boss-endurance' in sys.argv:
                assert 0<=continue_count<=64
            elif '--campaign-extra-continues' in sys.argv:
                assert 0<=continue_count<=32
            else:
                assert 0<=continue_count<=(20 if '--campaign-full' in sys.argv else 5)
            environment['KS_CAMPAIGN_EXTRA_CONTINUES']='1' if '--campaign-extra-continues' in sys.argv else '0'
            environment['KS_CAMPAIGN_CONTINUES']=str(continue_count)
            environment['KS_CAMPAIGN_FIELDS']='120000' if '--campaign-extended' in sys.argv else ('90000' if '--campaign-full' in sys.argv else ('45000' if '--campaign-long' in sys.argv else '30000'))
            environment['KS_CAMPAIGN_ENDING_WINDOW']='1' if '--campaign-ending-window' in sys.argv else '0'
            if '--campaign-ending-window' in sys.argv: environment['KS_CAMPAIGN_FIELDS']='150000'
            environment['KS_CAMPAIGN_FINALE_WINDOW']='1' if '--campaign-finale-window' in sys.argv else '0'
            if '--campaign-finale-window' in sys.argv: environment['KS_CAMPAIGN_FIELDS']='180000'
            environment['KS_CAMPAIGN_BOSS_ENDURANCE']='1' if '--campaign-boss-endurance' in sys.argv else '0'
            if '--campaign-boss-endurance' in sys.argv: environment['KS_CAMPAIGN_FIELDS']='300000'
            probe=HERE.parent/'port/diagnostics/campaign_probe.lua'
            environment['KS_CAMPAIGN_ACTOR']='18' if '--sonya' in sys.argv else '17'
            campaign_control=next((arg for arg in sys.argv if arg.startswith('--campaign-stock=')),None)
            if campaign_control:
                control_actor=int(campaign_control.split('=',1)[1]);assert control_actor in range(12)
                environment['KS_CAMPAIGN_ACTOR']=str(control_actor)
            environment['KS_CAMPAIGN_STYLE']='ball' if '--campaign-defensive-ball' in sys.argv else ('jumpkick' if '--campaign-jumpkick' in sys.argv else ('uppercut' if '--campaign-uppercut' in sys.argv else 'grapple'))
            if '--campaign-retreat-kick' in sys.argv:environment['KS_CAMPAIGN_STYLE']='retreatkick'
            if '--campaign-late-kick' in sys.argv:environment['KS_CAMPAIGN_STYLE']='latekick'
            if '--campaign-reptile-grapple' in sys.argv:environment['KS_CAMPAIGN_STYLE']='reptilegrapple'
            if '--campaign-sweep-jump' in sys.argv:environment['KS_CAMPAIGN_STYLE']='sweepjump'
            if '--campaign-jump-grapple' in sys.argv:environment['KS_CAMPAIGN_STYLE']='jumpgrapple'
            environment['KS_CAMPAIGN_DEFENSE']='1' if '--campaign-defense' in sys.argv else '0'
            environment['KS_CAMPAIGN_JAX_RING']='1' if '--campaign-jax-ring' in sys.argv else '0'
            environment['KS_CAMPAIGN_KANO_KNIFE']='1' if '--campaign-kano-knife' in sys.argv else '0'
            # Preserve the old misnamed flag as an explicit compatibility alias.
            environment['KS_CAMPAIGN_RAIDEN_KNIFE']='1' if any(flag in sys.argv for flag in ('--campaign-raiden-knife','--campaign-mileena-knife')) else '0'
            environment['KS_CAMPAIGN_FEMALE_ZONING']='1' if '--campaign-female-zoning' in sys.argv else '0'
            environment['KS_CAMPAIGN_FEMALE_COUNTER']='1' if '--campaign-female-counter' in sys.argv else '0'
            environment['KS_CAMPAIGN_COUNTER_TAKEOFF']='1' if '--campaign-counter-takeoff' in sys.argv else '0'
            environment['KS_CAMPAIGN_COUNTER_FORWARD']='1' if '--campaign-counter-forward' in sys.argv else '0'
            environment['KS_CAMPAIGN_KITANA_KNIFE_GUARD']='1' if '--campaign-kitana-knife-guard' in sys.argv else '0'
            environment['KS_CAMPAIGN_RAIDEN_COUNTER']='1' if '--campaign-raiden-counter' in sys.argv else '0'
            environment['KS_CAMPAIGN_RAIDEN_BIKE_PUNISH']='1' if '--campaign-raiden-bike-punish' in sys.argv else '0'
            environment['KS_CAMPAIGN_RAIDEN_FAST_BIKE']='1' if '--campaign-raiden-fast-bike' in sys.argv else '0'
            environment['KS_CAMPAIGN_RAIDEN_READY_BIKE']='1' if '--campaign-raiden-ready-bike' in sys.argv else '0'
            environment['KS_CAMPAIGN_RAIDEN_BACK_LEG']='1' if '--campaign-raiden-back-leg' in sys.argv else '0'
            environment['KS_CAMPAIGN_RAIDEN_SWEEP']='1' if '--campaign-raiden-sweep' in sys.argv else '0'
            environment['KS_CAMPAIGN_RAIDEN_JUMP']='1' if '--campaign-raiden-jump' in sys.argv else '0'
            environment['KS_CAMPAIGN_KITANA_JUMP']='1' if '--campaign-kitana-jump' in sys.argv else '0'
            environment['KS_CAMPAIGN_KITANA_READY_KNIFE']='1' if '--campaign-kitana-ready-knife' in sys.argv else '0'
            environment['KS_CAMPAIGN_KITANA_RFP_DUCK']='1' if '--campaign-kitana-rfp-duck' in sys.argv else '0'
            environment['KS_CAMPAIGN_LIU_RFP_DUCK']='1' if '--campaign-liu-rfp-duck' in sys.argv else '0'
            if '--campaign-subzero-observe' in sys.argv: assert '--campaign-subzero-guard' in sys.argv and '--sonya' not in sys.argv
            environment['KS_CAMPAIGN_SUBZERO_OBSERVE']='1' if '--campaign-subzero-observe' in sys.argv else '0'
            if '--campaign-subzero-rfp-duck' in sys.argv: assert '--campaign-subzero-guard' in sys.argv and '--sonya' not in sys.argv
            environment['KS_CAMPAIGN_SUBZERO_RFP_DUCK']='1' if '--campaign-subzero-rfp-duck' in sys.argv else '0'
            if '--campaign-sonya-kitana-rfp-duck' in sys.argv: assert '--sonya' in sys.argv and '--campaign-sonya-kitana-ring' in sys.argv
            environment['KS_CAMPAIGN_SONYA_KITANA_RFP_DUCK']='1' if '--campaign-sonya-kitana-rfp-duck' in sys.argv else '0'
            if '--campaign-sonya-kitana-recover-counter' in sys.argv: assert '--campaign-sonya-kitana-rfp-duck' in sys.argv
            environment['KS_CAMPAIGN_SONYA_KITANA_RECOVER_COUNTER']='1' if '--campaign-sonya-kitana-recover-counter' in sys.argv else '0'
            if '--campaign-sonya-kitana-recover-kick' in sys.argv: assert '--campaign-sonya-kitana-recover-counter' in sys.argv
            environment['KS_CAMPAIGN_SONYA_KITANA_RECOVER_KICK']='1' if '--campaign-sonya-kitana-recover-kick' in sys.argv else '0'
            if '--campaign-sonya-kitana-guard-leg' in sys.argv: assert '--campaign-sonya-kitana-rfp-duck' in sys.argv
            environment['KS_CAMPAIGN_SONYA_KITANA_GUARD_LEG']='1' if '--campaign-sonya-kitana-guard-leg' in sys.argv else '0'
            if '--campaign-sonya-liu-guard-leg' in sys.argv: assert '--sonya' in sys.argv
            environment['KS_CAMPAIGN_SONYA_LIU_GUARD_LEG']='1' if '--campaign-sonya-liu-guard-leg' in sys.argv else '0'
            if '--campaign-sonya-sub-guard-leg' in sys.argv: assert '--sonya' in sys.argv
            environment['KS_CAMPAIGN_SONYA_SUB_GUARD_LEG']='1' if '--campaign-sonya-sub-guard-leg' in sys.argv else '0'
            if '--campaign-sonya-sub-neutral-leg' in sys.argv: assert '--sonya' in sys.argv and '--campaign-sonya-sub-guard-leg' in sys.argv
            environment['KS_CAMPAIGN_SONYA_SUB_NEUTRAL_LEG']='1' if '--campaign-sonya-sub-neutral-leg' in sys.argv else '0'
            if '--campaign-sonya-mileena-guard-leg' in sys.argv: assert '--sonya' in sys.argv
            environment['KS_CAMPAIGN_SONYA_MILEENA_GUARD_LEG']='1' if '--campaign-sonya-mileena-guard-leg' in sys.argv else '0'
            if '--campaign-sonya-cage-guard-leg' in sys.argv: assert '--sonya' in sys.argv
            environment['KS_CAMPAIGN_SONYA_CAGE_GUARD_LEG']='1' if '--campaign-sonya-cage-guard-leg' in sys.argv else '0'
            if '--campaign-sonya-lao-guard-leg' in sys.argv: assert '--sonya' in sys.argv
            environment['KS_CAMPAIGN_SONYA_LAO_GUARD_LEG']='1' if '--campaign-sonya-lao-guard-leg' in sys.argv else '0'
            if '--campaign-sonya-scorpion-guard-leg' in sys.argv: assert '--sonya' in sys.argv
            environment['KS_CAMPAIGN_SONYA_SCORPION_GUARD_LEG']='1' if '--campaign-sonya-scorpion-guard-leg' in sys.argv else '0'
            if '--campaign-sonya-kintaro-guard' in sys.argv: assert '--sonya' in sys.argv
            environment['KS_CAMPAIGN_SONYA_KINTARO_GUARD']='1' if '--campaign-sonya-kintaro-guard' in sys.argv else '0'
            if '--campaign-sonya-shang-guard-leg' in sys.argv: assert '--sonya' in sys.argv
            environment['KS_CAMPAIGN_SONYA_SHANG_GUARD_LEG']='1' if '--campaign-sonya-shang-guard-leg' in sys.argv else '0'
            if '--campaign-sonya-own-guard-leg' in sys.argv: assert '--sonya' in sys.argv
            environment['KS_CAMPAIGN_SONYA_OWN_GUARD_LEG']='1' if '--campaign-sonya-own-guard-leg' in sys.argv else '0'
            if '--campaign-sonya-mileena-no-ring' in sys.argv: assert '--campaign-sonya-mileena-guard-leg' in sys.argv
            environment['KS_CAMPAIGN_SONYA_MILEENA_NO_RING']='1' if '--campaign-sonya-mileena-no-ring' in sys.argv else '0'
            if '--campaign-sonya-mileena-leg85' in sys.argv: assert '--campaign-sonya-mileena-guard-leg' in sys.argv
            environment['KS_CAMPAIGN_SONYA_MILEENA_LEG85']='1' if '--campaign-sonya-mileena-leg85' in sys.argv else '0'
            environment['KS_CAMPAIGN_KITANA_FAN_GUARD']='1' if '--campaign-kitana-fan-guard' in sys.argv else '0'
            knife_intervals=[arg.split('=',1)[1] for arg in sys.argv if arg.startswith('--campaign-kitana-knife-interval=')]
            assert len(knife_intervals)<=1
            knife_interval=int(knife_intervals[0]) if knife_intervals else 60
            assert 24<=knife_interval<=120
            environment['KS_CAMPAIGN_KITANA_KNIFE_INTERVAL']=str(knife_interval)
            liu_intervals=[arg.split('=',1)[1] for arg in sys.argv if arg.startswith('--campaign-liu-knife-interval=')]
            assert len(liu_intervals)<=1
            liu_interval=int(liu_intervals[0]) if liu_intervals else 60
            assert 24<=liu_interval<=120
            environment['KS_CAMPAIGN_LIU_KNIFE_INTERVAL']=str(liu_interval)
            subzero_intervals=[arg.split('=',1)[1] for arg in sys.argv if arg.startswith('--campaign-subzero-knife-interval=')]
            assert len(subzero_intervals)<=1
            if subzero_intervals:
                assert '--campaign-subzero-guard' in sys.argv and '--sonya' not in sys.argv
            subzero_interval=int(subzero_intervals[0]) if subzero_intervals else 60
            assert 24<=subzero_interval<=120
            environment['KS_CAMPAIGN_SUBZERO_KNIFE_INTERVAL']=str(subzero_interval)
            environment['KS_CAMPAIGN_LIU_KNIFE_GUARD']='1' if '--campaign-liu-knife-guard' in sys.argv else '0'
            if '--campaign-liu-retreat' in sys.argv: assert '--campaign-liu-knife-guard' in sys.argv and '--sonya' not in sys.argv
            environment['KS_CAMPAIGN_LIU_RETREAT']='1' if '--campaign-liu-retreat' in sys.argv else '0'
            if '--campaign-liu-choke' in sys.argv: assert '--campaign-liu-knife-guard' in sys.argv and '--sonya' not in sys.argv
            environment['KS_CAMPAIGN_LIU_CHOKE']='1' if '--campaign-liu-choke' in sys.argv else '0'
            if '--campaign-subzero-knife' in sys.argv: assert '--sonya' not in sys.argv
            environment['KS_CAMPAIGN_SUBZERO_KNIFE']='1' if '--campaign-subzero-knife' in sys.argv else '0'
            if '--campaign-subzero-guard' in sys.argv: assert '--campaign-subzero-knife' in sys.argv and '--sonya' not in sys.argv
            environment['KS_CAMPAIGN_SUBZERO_GUARD']='1' if '--campaign-subzero-guard' in sys.argv else '0'
            if '--campaign-subzero-choke' in sys.argv: assert '--campaign-subzero-guard' in sys.argv and '--sonya' not in sys.argv
            environment['KS_CAMPAIGN_SUBZERO_CHOKE']='1' if '--campaign-subzero-choke' in sys.argv else '0'
            if '--campaign-subzero-neutral-choke' in sys.argv:
                assert '--campaign-subzero-choke' in sys.argv and '--campaign-subzero-rfp-duck' in sys.argv
                assert '--sonya' not in sys.argv
            environment['KS_CAMPAIGN_SUBZERO_NEUTRAL_CHOKE']='1' if '--campaign-subzero-neutral-choke' in sys.argv else '0'
            if '--campaign-subzero-fast-choke' in sys.argv:
                assert '--campaign-subzero-neutral-choke' in sys.argv
            environment['KS_CAMPAIGN_SUBZERO_FAST_CHOKE']='1' if '--campaign-subzero-fast-choke' in sys.argv else '0'
            if '--campaign-subzero-crouch-ready' in sys.argv:
                assert '--campaign-subzero-rfp-duck' in sys.argv and '--campaign-subzero-guard' in sys.argv
                assert '--sonya' not in sys.argv
            environment['KS_CAMPAIGN_SUBZERO_CROUCH_READY']='1' if '--campaign-subzero-crouch-ready' in sys.argv else '0'
            if '--campaign-subzero-approach' in sys.argv: assert '--campaign-subzero-choke' in sys.argv
            environment['KS_CAMPAIGN_SUBZERO_APPROACH']='1' if '--campaign-subzero-approach' in sys.argv else '0'
            approach_fields=[arg.split('=',1)[1] for arg in sys.argv if arg.startswith('--campaign-subzero-approach-fields=')]
            assert len(approach_fields)<=1
            if approach_fields: assert '--campaign-subzero-approach' in sys.argv
            walk_fields=int(approach_fields[0]) if approach_fields else 6
            assert 6<=walk_fields<=30
            environment['KS_CAMPAIGN_SUBZERO_APPROACH_FIELDS']=str(walk_fields)
            environment['KS_CAMPAIGN_LIU_BALL']='1' if '--campaign-liu-ball' in sys.argv else '0'
            environment['KS_CAMPAIGN_SONYA_RAIDEN_RING']='1' if '--campaign-sonya-raiden-ring' in sys.argv else '0'
            if '--campaign-sonya-kitana-ring' in sys.argv: assert '--sonya' in sys.argv
            environment['KS_CAMPAIGN_SONYA_KITANA_RING']='1' if '--campaign-sonya-kitana-ring' in sys.argv else '0'
            if '--campaign-sonya-kitana-leg-counter' in sys.argv: assert '--sonya' in sys.argv and '--campaign-sonya-kitana-ring' in sys.argv
            environment['KS_CAMPAIGN_SONYA_KITANA_LEG_COUNTER']='1' if '--campaign-sonya-kitana-leg-counter' in sys.argv else '0'
            ring_intervals=[arg.split('=',1)[1] for arg in sys.argv if arg.startswith('--campaign-sonya-kitana-ring-interval=')]
            assert len(ring_intervals)<=1
            if ring_intervals: assert '--campaign-sonya-kitana-ring' in sys.argv
            ring_interval=int(ring_intervals[0]) if ring_intervals else 60
            assert 24<=ring_interval<=120
            environment['KS_CAMPAIGN_SONYA_KITANA_RING_INTERVAL']=str(ring_interval)
            environment['KS_CAMPAIGN_GUARD_AFTER_HIT']='1' if '--campaign-guard-after-hit' in sys.argv else '0'
            guard_fields=[arg.split('=',1)[1] for arg in sys.argv if arg.startswith('--campaign-post-hit-fields=')]
            assert len(guard_fields)<=1
            guard_length=int(guard_fields[0]) if guard_fields else 24
            assert 0<=guard_length<=64
            environment['KS_CAMPAIGN_POST_HIT_FIELDS']=str(guard_length)
            guard_targets=[arg.split('=',1)[1] for arg in sys.argv if arg.startswith('--campaign-post-hit-opponent=')]
            assert len(guard_targets)<=1
            guard_target=int(guard_targets[0]) if guard_targets else -1
            assert -1<=guard_target<=18
            environment['KS_CAMPAIGN_POST_HIT_OPPONENT']=str(guard_target)
            environment['KS_CAMPAIGN_JAX_SAFE_RING']='1' if '--campaign-jax-safe-ring' in sys.argv else '0'
            environment['KS_CAMPAIGN_MIXED_ZONING']='1' if '--campaign-mixed-zoning' in sys.argv else '0'
            environment['KS_CAMPAIGN_ROSTER_GUARD']='1' if '--campaign-roster-guard' in sys.argv else '0'
            environment['KS_CAMPAIGN_BACK_GUARD']='1' if '--campaign-back-guard' in sys.argv else '0'
            environment['KS_CAMPAIGN_KNIFE_GUARD']='1' if '--campaign-knife-guard' in sys.argv else '0'
            environment['KS_CAMPAIGN_JAX_SWEEP']='1' if '--campaign-jax-sweep' in sys.argv else '0'
            environment['KS_CAMPAIGN_JAX_THROW']='1' if '--campaign-jax-throw' in sys.argv else '0'
            environment['KS_CAMPAIGN_JAX_AIR']='1' if '--campaign-jax-air' in sys.argv else '0'
            environment['KS_CAMPAIGN_JAX_REACTIVE']='1' if '--campaign-jax-reactive' in sys.argv else '0'
            kick_age=next((arg for arg in sys.argv if arg.startswith('--campaign-kick-age=')),None)
            if kick_age:
                age=int(kick_age.split('=',1)[1]);assert 6<=age<=28
                environment['KS_CAMPAIGN_KICK_AGE']=str(age)
            nav=(HERE.parent/'port/asm/KSNAV.ASM').read_text()
            for direction in ('up','down','left','right'):
                match=re.search(r'(?m)^ks_'+direction+r'_change\s*\n\s*\.word\s+([^\n]+)',nav)
                assert match
                environment['KS_SELECT_'+direction.upper()]=match[1].strip()
        if '--liu-bike-victim' in sys.argv or '--orb-victim' in sys.argv or '--own-throw' in sys.argv or '--backbreak-victim' in sys.argv or '--shred-victim' in sys.argv or '--nut-victim' in sys.argv or '--freeze-victim' in sys.argv or '--lightning-victim' in sys.argv or '--spear-victim' in sys.argv or '--shock-victim' in sys.argv or '--dive-victim' in sys.argv or '--blockkick-victim' in sys.argv:
            probe=HERE.parent/'port/diagnostics/liu_bike_victim_probe.lua'
            environment['KS_BIKE_VICTIM']='18' if '--sonya' in sys.argv else '17'
            environment['KS_BIKE_MIRROR']='1' if '--mirror' in sys.argv else '0'
            environment['KS_ORB_VICTIM']='1' if '--orb-victim' in sys.argv else '0'
            environment['KS_BACKBREAK']='1' if '--backbreak-victim' in sys.argv else '0'
            environment['KS_SHRED']='1' if '--shred-victim' in sys.argv else '0'
            environment['KS_NUT']='1' if '--nut-victim' in sys.argv else '0'
            environment['KS_FREEZE']='1' if '--freeze-victim' in sys.argv else '0'
            environment['KS_LIGHTNING']='1' if '--lightning-victim' in sys.argv else '0'
            environment['KS_SPEAR']='1' if '--spear-victim' in sys.argv else '0'
            environment['KS_SHOCK']='1' if '--shock-victim' in sys.argv else '0'
            environment['KS_DIVE']='1' if '--dive-victim' in sys.argv else '0'
            environment['KS_BLOCKKICK']='1' if '--blockkick-victim' in sys.argv else '0'
            if '--nut-victim' in sys.argv and '--stock-victim' in sys.argv:
                environment['KS_BIKE_VICTIM']='1'
            environment['KS_OWN_THROW']='18' if '--own-throw' in sys.argv and '--sonya' in sys.argv else ('17' if '--own-throw' in sys.argv else '0')
            environment['KS_THROW_VICTIM']='1' if '--stock-victim' in sys.argv else '0'
            victim_option=next((arg for arg in sys.argv if arg.startswith('--throw-victim=')),None)
            environment['KS_THROW_OVERRIDE']='1' if victim_option else '0'
            if victim_option:
                victim=int(victim_option.split('=',1)[1])
                assert victim in (*range(12),17,18)
                environment['KS_THROW_VICTIM']=str(victim)
            nav=(HERE.parent/'port/asm/KSNAV.ASM').read_text()
            for direction in ('up','down','left','right'):
                match=re.search(r'(?m)^ks_'+direction+r'_change\s*\n\s*\.word\s+([^\n]+)',nav)
                assert match
                environment['KS_SELECT_'+direction.upper()]=match[1].strip()
            environment['KS_THROW_EDGE']='1' if '--throw-front-edge' in sys.argv else '0'
        if '--morph' in sys.argv:
            probe=HERE.parent/'port/diagnostics/morph_probe.lua'
            environment['KS_MORPH_MIRROR']='1' if '--mirror' in sys.argv else '0'
            environment['KS_MORPH_SPECIALS']='1' if '--morph-specials' in sys.argv else '0'
            environment['KS_MORPH_BALL']='1' if '--morph-ball' in sys.argv else '0'
            environment['KS_MORPH_MELEE']='1' if '--morph-melee' in sys.argv else '0'
            environment['KS_MORPH_GRAPPLES']='1' if '--morph-grapples' in sys.argv else '0'
            environment['KS_MORPH_SQUARE']='1' if '--morph-square' in sys.argv else '0'
            environment['KS_MORPH_THROWS']='1' if '--morph-throws' in sys.argv else '0'
            environment['KS_MORPH_LATE_THROW']='1' if '--morph-late-throw' in sys.argv else '0'
        if '--select-new' in sys.argv:
            probe=HERE.parent/'port/diagnostics/game_probe.lua'
        if '--normal-moves' in sys.argv:
            assert not any(flag in sys.argv for flag in ('--campaign','--special','--projectiles','--blade','--bike','--choke','--leg','--morph','--stage','--extract','--laser','--kiss','--bubble','--friend','--baby'))
            probe=HERE.parent/'port/diagnostics/normal_probe.lua'
            environment['KS_NORMAL_MIRROR']='1' if '--mirror' in sys.argv else '0'
            environment['KS_NORMAL_SOAK']='1' if '--normal-soak' in sys.argv else '0'
            normal_cases=[arg.split('=',1)[1] for arg in sys.argv if arg.startswith('--normal-case=')]
            normal_sides=[arg.split('=',1)[1] for arg in sys.argv if arg.startswith('--normal-attacker=')]
            assert len(normal_cases)<=1 and len(normal_sides)<=1
            if '--normal-soak' in sys.argv:
                assert not normal_cases and not normal_sides
                assert not any(flag in sys.argv for flag in ('--normal-block','--normal-low-block','--capture-move'))
            assert not normal_cases or normal_cases[0] in ('hp','lp','hk','lk','roundhouse','sweep','uppercut','jumpkick','jumppunch','duckpunch','duckhighkick','ducklowkick','flyingkick','flyingpunch')
            assert not normal_sides or normal_sides[0] in ('1','2')
            assert normal_cases or (not normal_sides and '--normal-block' not in sys.argv)
            environment['KS_NORMAL_CASE']=normal_cases[0] if normal_cases else ''
            environment['KS_NORMAL_ATTACKER']=normal_sides[0] if normal_sides else '1'
            environment['KS_NORMAL_BLOCK']='1' if '--normal-block' in sys.argv else '0'
            assert '--normal-low-block' not in sys.argv or ('--normal-block' in sys.argv and normal_cases)
            environment['KS_NORMAL_LOW_BLOCK']='1' if '--normal-low-block' in sys.argv else '0'
            normal_gaps=[arg.split('=',1)[1] for arg in sys.argv if arg.startswith('--normal-gap=')]
            assert len(normal_gaps)<=1 and (not normal_gaps or normal_gaps[0] in ('70','90','100','180','220'))
            assert not normal_gaps or normal_cases
            environment['KS_NORMAL_GAP']=normal_gaps[0] if normal_gaps else '70'
        if '--special' in sys.argv:
            probe=HERE.parent/'port/diagnostics/special_probe.lua'
            environment['KS_SPECIAL_PROFILE']='square' if '--square' in sys.argv else 'ball'
            environment['KS_SPECIAL_MIRROR']='1' if '--mirror' in sys.argv else '0'
        if '--projectiles' in sys.argv:
            probe=HERE.parent/'port/diagnostics/projectile_probe.lua'
            environment['KS_PROJECTILE_MIRROR']='1' if '--mirror' in sys.argv else '0'
        if '--blade' in sys.argv:
            probe=HERE.parent/'port/diagnostics/blade_probe.lua'
            environment['KS_PROJECTILE_MIRROR']='1' if '--mirror' in sys.argv else '0'
        if '--bike' in sys.argv:
            probe=HERE.parent/'port/diagnostics/bike_probe.lua'
            environment['KS_PROJECTILE_MIRROR']='1' if '--mirror' in sys.argv else '0'
            environment['KS_BIKE_AUDIO_TAIL']='1' if '--bike-audio-tail' in sys.argv else '0'
        if '--choke' in sys.argv:
            probe=HERE.parent/'port/diagnostics/choke_probe.lua'
            environment['KS_CHOKE_FAST_COMMAND']='1' if '--choke-fast-command' in sys.argv else '0'
            environment['KS_CHOKE_CROUCH_ENTRY']='1' if '--choke-crouch-entry' in sys.argv else '0'
            environment['KS_PROJECTILE_MIRROR']='1' if '--mirror' in sys.argv else '0'
            environment['KS_CHOKE_VICTIM']='1' if '--stock-victim' in sys.argv else '18'
            choke_victims=[arg.split('=',1)[1] for arg in sys.argv if arg.startswith('--choke-victim=')]
            choke_spacings=[arg.split('=',1)[1] for arg in sys.argv if arg.startswith('--choke-spacing=')]
            assert len(choke_victims)<=1 and len(choke_spacings)<=1
            if choke_victims:
                choke_victim=int(choke_victims[0]);assert choke_victim in (*range(12),18)
                environment['KS_CHOKE_VICTIM']=str(choke_victim)
                environment['KS_CHOKE_NAVIGATE']='1'
                nav=(HERE.parent/'port/asm/KSNAV.ASM').read_text()
                for direction in ('up','down','left','right'):
                    match=re.search(r'(?m)^ks_'+direction+r'_change\s*\n\s*\.word\s+([^\n]+)',nav)
                    assert match
                    environment['KS_SELECT_'+direction.upper()]=match[1].strip()
            if choke_spacings:
                choke_spacing=int(choke_spacings[0]);assert 40<=choke_spacing<=105
                environment['KS_CHOKE_SPACING']=str(choke_spacing)
        if '--leg' in sys.argv:
            probe=HERE.parent/'port/diagnostics/leg_probe.lua'
            environment['KS_PROJECTILE_MIRROR']='1' if '--mirror' in sys.argv else '0'
            environment['KS_LEG_VICTIM']='1' if '--stock-victim' in sys.argv else '17'
        if '--extract' in sys.argv:
            probe=HERE.parent/'port/diagnostics/extract_probe.lua'
            environment['KS_EXTRACT_MIRROR']='1' if '--mirror' in sys.argv else '0'
            environment['KS_EXTRACT_VICTIM']='1' if '--stock-victim' in sys.argv else '18'
        if '--baby' in sys.argv:
            probe=HERE.parent/'port/diagnostics/extract_probe.lua'
            environment['KS_EXTRACT_MIRROR']='1' if '--mirror' in sys.argv else '0'
            environment['KS_EXTRACT_VICTIM']='1'
            environment['KS_FINISH_KIND']='baby'
            environment['KS_BABY_SONYA']='1' if '--sonya' in sys.argv else '0'
            environment['KS_BABY_PUNCH_WINS']='1' if '--punch-wins' in sys.argv else '0'
            if '--own-victim' in sys.argv:
                environment['KS_EXTRACT_VICTIM']='17' if '--sonya' in sys.argv else '18'
        if '--friend' in sys.argv:
            environment['KS_FRIEND_REJOIN']='1' if '--friend-rejoin' in sys.argv else '0'
            probe=HERE.parent/'port/diagnostics/extract_probe.lua'
            environment['KS_EXTRACT_MIRROR']='1' if '--mirror' in sys.argv else '0'
            environment['KS_EXTRACT_VICTIM']='1' if '--stock-victim' in sys.argv else '17'
            if '--kano' in sys.argv and '--stock-victim' not in sys.argv:
                environment['KS_EXTRACT_VICTIM']='18'
            environment['KS_FRIEND_KANO']='1' if '--kano' in sys.argv else '0'
            environment['KS_FINISH_KIND']='friend'
            environment['KS_BABY_PUNCH_WINS']='1' if '--punch-wins' in sys.argv else '0'
        if '--stage' in sys.argv:
            probe=HERE.parent/'port/diagnostics/extract_probe.lua'
            environment['KS_EXTRACT_MIRROR']='1' if '--mirror' in sys.argv else '0'
            environment['KS_EXTRACT_VICTIM']='1'
            if '--own-victim' in sys.argv:
                environment['KS_EXTRACT_VICTIM']='17' if '--sonya' in sys.argv else '18'
            environment['KS_FINISH_KIND']='stage'
            environment['KS_DEADPOOL']='1' if '--deadpool' in sys.argv else '0'
            environment['KS_DEADPOOL_NO_CHORD']='1' if '--deadpool-no-chord' in sys.argv else '0'
            environment['KS_BABY_SONYA']='1' if '--sonya' in sys.argv else '0'
            environment['KS_STAGE_REMATCH']='1' if '--stage-rematch' in sys.argv else '0'
            environment['KS_PIT_PROGRESS']='1' if '--pit-progress' in sys.argv else '0'
            environment['KS_PIT_REJOIN']='1' if '--pit-rejoin' in sys.argv else '0'
            nav=(HERE.parent/'port/asm/KSNAV.ASM').read_text()
            for direction in ('up','down','left','right'):
                match=re.search(r'(?m)^ks_'+direction+r'_change\s*\n\s*\.word\s+([^\n]+)',nav)
                assert match
                environment['KS_SELECT_'+direction.upper()]=match[1].strip()
        if '--kiss' in sys.argv:
            environment['KS_FINISH_NONFLAWLESS']='1' if '--nonflawless' in sys.argv else '0'
            probe=HERE.parent/'port/diagnostics/extract_probe.lua'
            environment['KS_EXTRACT_MIRROR']='1' if '--mirror' in sys.argv else '0'
            environment['KS_EXTRACT_VICTIM']='1' if '--stock-victim' in sys.argv else '17'
            environment['KS_FINISH_KIND']='kiss'
        if '--bubble' in sys.argv:
            probe=HERE.parent/'port/diagnostics/extract_probe.lua'
            environment['KS_EXTRACT_MIRROR']='1' if '--mirror' in sys.argv else '0'
            environment['KS_EXTRACT_VICTIM']='1' if '--stock-victim' in sys.argv else '17'
            environment['KS_FINISH_KIND']='bubble'
            environment['KS_BUBBLE_BAD_HOLD']='1' if '--bad-hold' in sys.argv else '0'
        if '--laser' in sys.argv:
            probe=HERE.parent/'port/diagnostics/extract_probe.lua'
            environment['KS_EXTRACT_MIRROR']='1' if '--mirror' in sys.argv else '0'
            environment['KS_EXTRACT_VICTIM']='1' if '--stock-victim' in sys.argv else '18'
            environment['KS_FINISH_KIND']='laser'
            environment['KS_LASER_HELD_BLOCK']='1' if '--held-block' in sys.argv else '0'
        if any(flag in sys.argv for flag in ('--clap-victim','--fan-victim','--tongue-victim','--drain-victim','--torso-victim','--swipe-victim','--impale-victim','--superfreeze-victim','--arms-victim','--kitana-kiss-victim','--body-suck-victim','--shang-burst-victim','--raiden-burst-victim','--lao-split-victim')):
            probe=HERE.parent/'port/diagnostics/extract_probe.lua'
            environment['KS_FINISH_KIND']='drain' if '--drain-victim' in sys.argv else ('tongue' if '--tongue-victim' in sys.argv else 'fan')
            if '--clap-victim' in sys.argv:environment['KS_FINISH_KIND']='clap'
            if '--torso-victim' in sys.argv:environment['KS_FINISH_KIND']='torso'
            if '--swipe-victim' in sys.argv:environment['KS_FINISH_KIND']='swipe'
            if '--impale-victim' in sys.argv:environment['KS_FINISH_KIND']='impale'
            if '--superfreeze-victim' in sys.argv:environment['KS_FINISH_KIND']='superfreeze'
            if '--arms-victim' in sys.argv:environment['KS_FINISH_KIND']='arms'
            if '--kitana-kiss-victim' in sys.argv:environment['KS_FINISH_KIND']='kitana_kiss'
            if '--body-suck-victim' in sys.argv:environment['KS_FINISH_KIND']='bodysuck'
            if '--shang-burst-victim' in sys.argv:environment['KS_FINISH_KIND']='shangburst'
            if '--raiden-burst-victim' in sys.argv:environment['KS_FINISH_KIND']='raidenburst'
            if '--lao-split-victim' in sys.argv:environment['KS_FINISH_KIND']='laosplit'
            environment['KS_SHATTER']='1' if '--shatter-followup' in sys.argv else '0'
            environment['KS_EXTRACT_MIRROR']='1' if '--mirror' in sys.argv else '0'
            environment['KS_EXTRACT_VICTIM']='18' if '--sonya' in sys.argv else '17'
            if any(flag in sys.argv for flag in ('--drain-victim','--torso-victim','--swipe-victim','--impale-victim','--arms-victim')) and '--stock-victim' in sys.argv:
                environment['KS_EXTRACT_VICTIM']='1'
            arm_control=next((arg for arg in sys.argv if arg.startswith('--arms-control=')),None)
            kiss_control=next((arg for arg in sys.argv if arg.startswith('--kitkiss-control=')),None)
            ingestion_control=next((arg for arg in sys.argv if arg.startswith('--ingestion-control=')),None)
            burst_control=next((arg for arg in sys.argv if arg.startswith('--shang-burst-control=')),None)
            raiden_control=next((arg for arg in sys.argv if arg.startswith('--raiden-burst-control=')),None)
            split_control=next((arg for arg in sys.argv if arg.startswith('--lao-split-control=')),None)
            if split_control:
                assert '--lao-split-victim' in sys.argv
                original_actor=int(split_control.split('=',1)[1]);assert original_actor in range(12)
                environment['KS_EXTRACT_VICTIM']=str(original_actor)
            if raiden_control:
                assert '--raiden-burst-victim' in sys.argv
                original_actor=int(raiden_control.split('=',1)[1]);assert original_actor in range(12)
                environment['KS_EXTRACT_VICTIM']=str(original_actor)
            if burst_control:
                assert '--shang-burst-victim' in sys.argv
                original_actor=int(burst_control.split('=',1)[1]);assert original_actor in range(12)
                environment['KS_EXTRACT_VICTIM']=str(original_actor)
            if ingestion_control:
                assert '--body-suck-victim' in sys.argv
                original_actor=int(ingestion_control.split('=',1)[1]);assert original_actor in range(12)
                environment['KS_EXTRACT_VICTIM']=str(original_actor)
            if kiss_control:
                assert '--kitana-kiss-victim' in sys.argv
                original_actor=int(kiss_control.split('=',1)[1]);assert original_actor in range(12)
                environment['KS_EXTRACT_VICTIM']=str(original_actor)
            if arm_control:
                assert '--arms-victim' in sys.argv
                original_actor=int(arm_control.split('=',1)[1]);assert original_actor in range(12)
                environment['KS_EXTRACT_VICTIM']=str(original_actor)
            nav=(HERE.parent/'port/asm/KSNAV.ASM').read_text()
            for direction in ('up','down','left','right'):
                match=re.search(r'(?m)^ks_'+direction+r'_change\s*\n\s*\.word\s+([^\n]+)',nav)
                assert match
                environment['KS_SELECT_'+direction.upper()]=match[1].strip()
        if finisher_victims:
            environment['KS_EXTRACT_VICTIM']=finisher_victims[0]
        environment['KS_FINISHER_VICTIM_OVERRIDE']='1' if finisher_victims else '0'
        symbols={name:int(address,16) for address,name in re.findall(r'\b([0-9a-fA-F]{8})\s+([A-Za-z_]\w*)',(BUILD/'srcp/MK2P.MAP').read_text())}
        if '--normal-soak' in sys.argv:
            environment['KS_NORMAL_P1_STATE']=str(symbols['p1_state'])
            environment['KS_NORMAL_P2_STATE']=str(symbols['p2_state'])
            for direction in ('UP','DOWN','LEFT','RIGHT'):
                environment['KS_NORMAL_NAV_'+direction]=str(symbols['ks_'+direction.lower()+'_change'])
        if '--friend-lifecycle' in sys.argv:
            assert '--friend' in sys.argv
            listing=(BUILD/'srcp/KSFRIEND.LST').read_text()
            def local_label(name):
                return int(re.search(r'^\s+\d+\s+([0-9a-fA-F]{8})\s+'+name+r'\s*$',listing,re.M)[1],16)
            base=symbols['ks_sonya_friend']-local_label('ks_sonya_friend')
            image=bytearray(1048576)
            image[::2]=replacements['mk321u54.bin'];image[1::2]=replacements['mk321u63.bin']
            loop=base+local_label('ks_chicken_loop')
            offset=(loop-0xff800000)//8
            assert int.from_bytes(image[offset:offset+2],'little')==0x09e9
            environment['KS_CHICKEN_FRAMES']=str(int.from_bytes(image[offset+2:offset+6],'little'))
            # Sleep expands to MOVI + CALLA: saved wake is 0x50 bits later.
            environment['KS_CHICKEN_COMPLETE_WAKE']=str(base+local_label('ks_friend_complete')+0x50)
        environment['KS_RECOVERY_PC']=str(symbols['illegal_opcode']+0x50)
        if '--normal-strike-trace' in sys.argv:
            assert '--normal-moves' in sys.argv
            environment['KS_NORMAL_STRIKE_PC']=str(symbols['strike_check'])
        environment['KS_CAMPAIGN_GUARD_PC']=str(symbols['joy_block_loop']+0x50)
        environment['KS_CAMPAIGN_SONYA_KAHN_GUARD']='1' if '--campaign-sonya-kahn-guard' in sys.argv else '0'
        environment['KS_CAMPAIGN_SONYA_KAHN_CONTACT_READY']='1' if '--campaign-sonya-kahn-contact-ready' in sys.argv else '0'
        environment['KS_CAMPAIGN_SONYA_KAHN_OPENING_JUMP']='1' if '--campaign-sonya-kahn-opening-jump' in sys.argv else '0'
        environment['KS_CAMPAIGN_CAPTURE_ENDING']='1' if '--campaign-capture-ending' in sys.argv else '0'
        environment['KS_CAMPAIGN_ENDING_STATE']='1' if '--campaign-ending-state' in sys.argv else '0'
        environment['KS_CAMPAIGN_KANO_SUB_JUMP']='1' if '--campaign-kano-sub-jump' in sys.argv else '0'
        environment['KS_CAMPAIGN_KANO_SUB_JUMP_HOLD']='1' if '--campaign-kano-sub-jump-hold' in sys.argv else '0'
        environment['KS_CAMPAIGN_KANO_SUB_RANGE_KICK']='1' if '--campaign-kano-sub-range-kick' in sys.argv else '0'
        environment['KS_CAMPAIGN_KANO_SUB_BALL']='1' if '--campaign-kano-sub-ball' in sys.argv else '0'
        environment['KS_CAMPAIGN_KANO_SUB_STANDING_CHARGE']='1' if '--campaign-kano-sub-standing-charge' in sys.argv else '0'
        environment['KS_CAMPAIGN_KANO_SUB_ADAPTIVE_CHARGE']='1' if '--campaign-kano-sub-adaptive-charge' in sys.argv else '0'
        environment['KS_CAMPAIGN_KANO_SUB_BALL_COUNTER']='1' if '--campaign-kano-sub-ball-counter' in sys.argv else '0'
        environment['KS_CAMPAIGN_KANO_SUB_RECOVERY_COUNTER']='1' if '--campaign-kano-sub-recovery-counter' in sys.argv else '0'
        environment['KS_CAMPAIGN_KANO_SUB_RECOVERY_BALL']='1' if '--campaign-kano-sub-recovery-ball' in sys.argv else '0'
        environment['KS_CAMPAIGN_KANO_SUB_RECHARGE']='1' if '--campaign-kano-sub-recharge' in sys.argv else '0'
        environment['KS_CAMPAIGN_KANO_SUB_APPROACH']='1' if '--campaign-kano-sub-approach' in sys.argv else '0'
        environment['KS_CAMPAIGN_KANO_SUB_POSTBALL_GUARD']='1' if '--campaign-kano-sub-postball-guard' in sys.argv else '0'
        environment['KS_CAMPAIGN_KANO_SUB_NORMAL_THROW']='1' if '--campaign-kano-sub-normal-throw' in sys.argv else '0'
        environment['KS_CAMPAIGN_KANO_SUB_NEUTRAL_UPPERCUT']='1' if '--campaign-kano-sub-neutral-uppercut' in sys.argv else '0'
        environment['KS_CAMPAIGN_KANO_MILEENA_PREPARE']='1' if '--campaign-kano-mileena-prepare' in sys.argv else '0'
        environment['KS_CAMPAIGN_KANO_HUMAN_PREPARE']='1' if '--campaign-kano-human-prepare' in sys.argv else '0'
        environment['KS_CAMPAIGN_KANO_BOSS_GUARD']='1' if '--campaign-kano-boss-guard' in sys.argv else '0'
        environment['KS_CAMPAIGN_KANO_KINTARO_PREPARE']='1' if '--campaign-kano-kintaro-prepare' in sys.argv else '0'
        environment['KS_CAMPAIGN_KANO_KINTARO_JUMPKICK']='1' if '--campaign-kano-kintaro-jumpkick' in sys.argv else '0'
        environment['KS_CAMPAIGN_KANO_KINTARO_WIDE']='1' if '--campaign-kano-kintaro-wide-prepare' in sys.argv else '0'
        environment['KS_CAMPAIGN_KANO_KINTARO_BLADE']='1' if '--campaign-kano-kintaro-blade' in sys.argv else '0'
        environment['KS_CAMPAIGN_KANO_KINTARO_KNIFE']='1' if '--campaign-kano-kintaro-knife' in sys.argv else '0'
        environment['KS_CAMPAIGN_KANO_KINTARO_MIXED']='1' if '--campaign-kano-kintaro-mixed' in sys.argv else '0'
        environment['KS_CAMPAIGN_KANO_KINTARO_MIXED_GUARD']='1' if '--campaign-kano-kintaro-mixed-guard' in sys.argv else '0'
        environment['KS_CAMPAIGN_KANO_KINTARO_KNIFE_MIDRANGE']='1' if '--campaign-kano-kintaro-knife-midrange' in sys.argv else '0'
        environment['KS_CAMPAIGN_KANO_KINTARO_KNIFE_READY']='1' if '--campaign-kano-kintaro-knife-ready' in sys.argv else '0'
        environment['KS_CAMPAIGN_KANO_KINTARO_EVADE_COUNTER']='1' if '--campaign-kano-kintaro-evade-counter' in sys.argv else '0'
        environment['KS_CAMPAIGN_KANO_KINTARO_SHORT_KICK']='1' if '--campaign-kano-kintaro-short-kick' in sys.argv else '0'
        environment['KS_CAMPAIGN_KANO_KINTARO_RETREAT_BALL']='1' if '--campaign-kano-kintaro-retreat-ball' in sys.argv else '0'
        environment['KS_CAMPAIGN_KANO_KINTARO_RETREAT_BALL_FINISH_KNIFE']='1' if '--campaign-kano-kintaro-retreat-ball-finish-knife' in sys.argv else '0'
        environment['KS_CAMPAIGN_KANO_KINTARO_FAST_PULSE']='1' if '--campaign-kano-kintaro-fast-pulse' in sys.argv else '0'
        environment['KS_CAMPAIGN_KANO_KINTARO_READY']='1' if '--campaign-kano-kintaro-ready-counter' in sys.argv else '0'
        environment['KS_CAMPAIGN_KANO_KINTARO_EARLY_COUNTER']='1' if '--campaign-kano-kintaro-early-counter' in sys.argv else '0'
        environment['KS_CAMPAIGN_KANO_KINTARO_VARIED']='1' if '--campaign-kano-kintaro-varied' in sys.argv else '0'
        environment['KS_CAMPAIGN_KANO_KINTARO_VARIED_COUNTER']='1' if '--campaign-kano-kintaro-varied-counter' in sys.argv else '0'
        environment['KS_CAMPAIGN_KANO_KINTARO_VARIED_ADAPTIVE']='1' if '--campaign-kano-kintaro-varied-adaptive' in sys.argv else '0'
        environment['KS_CAMPAIGN_KANO_KINTARO_STOMP_REFRESH']='1' if '--campaign-kano-kintaro-stomp-refresh' in sys.argv else '0'
        environment['KS_CAMPAIGN_KANO_KINTARO_STOMP_MOMENTUM']='1' if '--campaign-kano-kintaro-stomp-momentum' in sys.argv else '0'
        if '--campaign-kano-kintaro-varied' in sys.argv:
            environment['KS_CAMPAIGN_BOSS_HITQ']=str(symbols['p2_hitq'])
        environment['KS_CAMPAIGN_KANO_KINTARO_READY_RANGE']=ready_ranges[0] if ready_ranges else '115'
        if '--campaign-ending-state' in sys.argv:
            for name in ('dlists','displayon','noflip','pageaddr','f_auto_erase','objlst','objlst2','scrntl','scrnlr'):
                assert 0x01000000<=symbols[name]<0x01400000
                environment['KS_ENDING_'+name.upper()]=str(symbols[name])
        if '--campaign-sonya-kahn-guard' in sys.argv or '--campaign-kano-boss-guard' in sys.argv:
            boss_listing=(BUILD/'srcp/MKBOSS.LST').read_text()
            def boss_local(label):
                return int(re.search(r'^\s+\d+\s+([0-9a-fA-F]{8})\s+(?:[0-9a-fA-F]{4,8}\s+)?'+label+r'\b',boss_listing,re.M)[1],16)
            boss_origin=symbols['kahn_start']-boss_local('kahn_start')
            charge_begin=boss_origin+boss_local('kahn_charge')
            charge_end=boss_origin+boss_local('kahn_post_dont_walk')
            assert 0xff800000<=charge_begin<charge_end<=0xffffffff and charge_end-charge_begin<=0x4000
            environment['KS_KAHN_CHARGE_BEGIN']=str(charge_begin)
            environment['KS_KAHN_CHARGE_END']=str(charge_end)
            contact_sleeps=[int(match[1],16) for match in re.finditer(r'^\s+\d+\s+([0-9a-fA-F]{8})\s+sleep\s+020H\b',boss_listing,re.M)
                            if charge_begin<=boss_origin+int(match[1],16)<charge_end]
            assert len(contact_sleeps)==1
            contact_wake=boss_origin+contact_sleeps[0]+0x50
            assert charge_begin<contact_wake<charge_end
            environment['KS_KAHN_CONTACT_WAKE']=str(contact_wake)
        environment['KS_CAMPAIGN_SONYA_KINTARO_EVADE']='1' if '--campaign-sonya-kintaro-evade' in sys.argv else '0'
        environment['KS_CAMPAIGN_SONYA_KINTARO_EARLY_EVADE']='1' if '--campaign-sonya-kintaro-early-evade' in sys.argv else '0'
        if '--campaign-sonya-kintaro-evade' in sys.argv or '--campaign-kano-boss-guard' in sys.argv:
            for name in ('left_edge','right_edge'):
                assert 0x01000000<=symbols[name]<0x01400000
                environment['KS_KINTARO_'+name.upper()]=str(symbols[name])
            screen_right=int(re.search(r'^scrrgt\s+\.set\s+(\d+)\s*$',(BUILD/'srcp/DISPEQU.ASM').read_text(),re.M)[1])
            assert 0<screen_right<=512
            environment['KS_KINTARO_SCREEN_RIGHT']=str(screen_right)
        if '--campaign-subzero-rfp-duck' in sys.argv or '--campaign-sonya-kitana-rfp-duck' in sys.argv or '--campaign-sonya-liu-guard-leg' in sys.argv or '--campaign-sonya-sub-guard-leg' in sys.argv or '--campaign-sonya-mileena-guard-leg' in sys.argv or '--campaign-sonya-cage-guard-leg' in sys.argv or '--campaign-sonya-lao-guard-leg' in sys.argv or '--campaign-sonya-scorpion-guard-leg' in sys.argv or '--campaign-sonya-own-guard-leg' in sys.argv or '--campaign-sonya-shang-guard-leg' in sys.argv or '--campaign-sonya-kintaro-guard' in sys.argv or '--campaign-sonya-kahn-guard' in sys.argv:
            environment['KS_GROUND_Y']=str(symbols['ground_y'])
            joy_listing=(BUILD/'srcp/JOY.LST').read_text()
            def joy_local(label):
                return int(re.search(r'^\s+\d+\s+([0-9a-fA-F]{8})\s+(?:[0-9a-fA-F]{4,8}\s+)?'+label+r'\b',joy_listing,re.M)[1],16)
            joy_origin=symbols['bt_null']-joy_local('bt_null')
            duck_buttons=joy_origin+joy_local('bt_duck')
            joy_image=bytearray(1048576)
            joy_image[::2]=replacements['mk321u54.bin'];joy_image[1::2]=replacements['mk321u63.bin']
            for index,label in enumerate(('joy_uppercut','joy_duck_punch','joy_duck_block','joy_duck_kickh','joy_duck_kickl')):
                offset=(duck_buttons+index*32-0xff800000)//8
                assert int.from_bytes(joy_image[offset:offset+4],'little')==joy_origin+joy_local(label)
            environment['KS_CAMPAIGN_DUCK_BUTTONS']=str(duck_buttons)
            stance_buttons=joy_origin+joy_local('bt_stance')
            for index,label in enumerate(('joy_hi_punch','joy_lo_punch','joy_block','joy_hi_kick','joy_med_kick')):
                offset=(stance_buttons+index*32-0xff800000)//8
                assert int.from_bytes(joy_image[offset:offset+4],'little')==joy_origin+joy_local(label)
            environment['KS_CAMPAIGN_STANCE_BUTTONS']=str(stance_buttons)
            environment['KS_CAMPAIGN_P1_BUTTONS']=str(symbols['p1_button'])
        if '--campaign-kitana-rfp-duck' in sys.argv or '--campaign-liu-rfp-duck' in sys.argv or '--campaign-subzero-observe' in sys.argv or '--campaign-subzero-rfp-duck' in sys.argv or '--campaign-sonya-kitana-rfp-duck' in sys.argv or '--campaign-sonya-liu-guard-leg' in sys.argv or '--campaign-sonya-sub-guard-leg' in sys.argv or '--campaign-sonya-mileena-guard-leg' in sys.argv or '--campaign-sonya-cage-guard-leg' in sys.argv or '--campaign-sonya-lao-guard-leg' in sys.argv or '--campaign-sonya-scorpion-guard-leg' in sys.argv or '--campaign-sonya-own-guard-leg' in sys.argv or '--campaign-sonya-shang-guard-leg' in sys.argv or '--campaign-sonya-kintaro-guard' in sys.argv:
            drone_listing=(BUILD/'srcp/MKDRONE.LST').read_text()
            def drone_local(name):
                return int(re.search(r'^\s+\d+\s+([0-9a-fA-F]{8})\s+(?:[0-9a-fA-F]{4}\s+)?'+name+r'\b',drone_listing,re.M)[1],16)
            drone_base=symbols['drone_entry']-drone_local('drone_entry')
            environment['KS_RFP_BEGIN']=str(drone_base+drone_local('drone_rfp'))
            environment['KS_RFP_END']=str(drone_base+drone_local('drone_flip_kick'))
            environment['KS_RFP_RECOVER']=str(drone_base+drone_local('drfp2'))
        if '--morph' in sys.argv:
            environment['KS_GROUND_Y']=str(symbols['ground_y'])
            environment['KS_MORPH_POSES']=','.join(str(symbols[f'ks_mo_{actor}_pose{phase}']) for actor in ('kano','sonya') for phase in range(3))
        if '--raiden-burst-victim' in sys.argv:
            # Read linked ROM metadata, never guest memory writes or a proxy ID.
            head_program=bytearray(1048576)
            head_program[::2]=replacements['mk321u54.bin']
            head_program[1::2]=replacements['mk321u63.bin']
            def head_pointer(address):
                at=(address-0xff800000)//8
                assert 0<=at<=len(head_program)-4
                return int.from_bytes(head_program[at:at+4],'little')
            head_identity=int(environment['KS_EXTRACT_VICTIM'])
            head_root=head_pointer(symbols['character_anitabs1']+head_identity*32)
            head_script=head_pointer(head_root+0x3d*32)
            head_images=[head_pointer(head_script+i*32) for i in range(7)]
            assert all(0xff800000<=v<=0xffffffff for v in head_images)
            environment['KS_FAN_IMAGES']=','.join(map(str,head_images))
        if '--lao-split-victim' in sys.argv:
            split_actor='sonya' if '--sonya' in sys.argv else 'kano'
            environment['KS_FAN_IMAGES']=','.join(str(symbols[f'ks_sp_{split_actor}_{role}_{kind}{index}']) for role,indices in (('whole',range(3)),('left',range(3,10)),('right',range(3,10))) for index in indices for kind in ('pose','frame'))
            if split_control:
                split_program=bytearray(1048576)
                split_program[::2]=replacements['mk321u54.bin']
                split_program[1::2]=replacements['mk321u63.bin']
                def split_pointer(address):
                    offset=(address-0xff800000)//8
                    assert 0<=offset<=len(split_program)-4
                    return int.from_bytes(split_program[offset:offset+4],'little')
                listing=(BUILD/'srcp/MKDEATH.LST').read_text()
                def split_local(label):
                    hits=re.findall(r'(?m)^\s*\d+\s+([0-9a-fA-F]{8})\s+'+re.escape(label)+r'\s*$',listing)
                    assert len(hits)==1,(label,hits)
                    return int(hits[0],16)
                table_address=symbols['disable_repell']-split_local('disable_repell')+split_local('split_in_2_tab')
                root=split_pointer(table_address+int(split_control.split('=',1)[1])*32)
                poses=[split_pointer(root+i*32) for i in range(12) if i not in (3,11)]
                assert len(poses)==10 and all(0xff800000<=p<=0xffffffff for p in poses)
                environment['KS_FAN_IMAGES']=','.join(map(str,poses))
        if '--arms-victim' in sys.argv:
            arm_actor='sonya' if '--sonya' in sys.argv else 'kano'
            environment['KS_FAN_IMAGES']=','.join(str(symbols[f'ks_ar_{arm_actor}_{role}{index}']) for role in ('body_pose','arm_frame') for index in range(5))
            environment['KS_FAN_IMAGES']+=','+str(symbols['GUSHER1'])
        environment['KS_MISSING_COUNT']=str(symbols['ks_missing_animation_count'])
        environment['KS_MISSING_TAG']=str(symbols['ks_missing_animation_tag'])
        environment['KS_MISSING_ACTOR']=str(symbols['ks_missing_animation_actor'])
        if any(flag in sys.argv for flag in ('--clap-victim','--fan-victim','--tongue-victim','--drain-victim','--torso-victim','--swipe-victim','--impale-victim')):
            victim='sonya' if '--sonya' in sys.argv else 'kano'
            environment['KS_FAN_IMAGES']=','.join(str(symbols[f'ks_{kind}_{victim}_{role}{i}']) for kind,role in (('dc','pose'),('hd','frame')) for i in range(7))
            if '--torso-victim' in sys.argv or '--swipe-victim' in sys.argv or '--impale-victim' in sys.argv:
                environment['KS_FAN_IMAGES']=','.join(str(symbols[f'ks_tr_{victim}_pose{i}']) for i in range(7))
                if '--swipe-victim' in sys.argv:
                    environment['KS_FAN_IMAGES']+=','+str(symbols[f'ks_sw_{victim}_pose5'])
                    environment['KS_SWIPE_FINAL']=str(symbols[f'ks_sw_{victim}_pose5'])
                    environment['KS_SWIPE_BOTTOM']='68' if victim=='sonya' else '67'
                environment['KS_TORSO_TABLE']=str(symbols['character_anitabs1'])
                if '--stock-victim' in sys.argv and any(flag in sys.argv for flag in ('--torso-victim','--swipe-victim')):
                    sys.path.insert(0,str(HERE.parent/'port'))
                    from native_lk_poses import resolve as resolve_lk_poses
                    native_poses=resolve_lk_poses(symbols,(BUILD/'srcp/MKLK.LST').read_text())
                    environment['KS_FAN_IMAGES']=','.join(str(address) for label,address in native_poses.items() if not label.startswith('a_'))
                    if '--swipe-victim' in sys.argv:
                        # Own-art landing snapshot calibration is not an original-Liu control gate.
                        environment['KS_SWIPE_FINAL']='0'
                        environment['KS_SWIPE_BOTTOM']='0'
            if '--drain-victim' in sys.argv:
                environment['KS_FAN_IMAGES']=','.join(str(symbols[f'ks_dr_{victim}_pose{i}']) for i in range(3))
                environment['KS_DRAIN_TABLE']=str(symbols['drain_table'])
                environment['KS_FINAL_DRAIN']=str(symbols['a_final_drain'])
        if '--backbreak-victim' in sys.argv:
            actor='sonya' if '--sonya' in sys.argv else 'kano'
            environment['KS_BACKBREAK_POSES']=','.join(str(symbols.get(f'ks_bk_{actor}_pose{i}',0)) for i in range(3))
        environment['KS_ACTIVE_LIST']=str(symbols['active'])
        environment['KS_OBJECT_LIST']=str(symbols['objlst'])
        environment['KS_PALRAM']=str(symbols['palram'])
        if '--pit-progress' in sys.argv:
            environment['KS_PIT_SEQUENCE']=str(symbols['ks_pit_kano_sequence' if '--sonya' in sys.argv else 'ks_pit_sonya_sequence'])
        if '--baby' in sys.argv:
            environment['KS_BABY_IMAGE']=str(symbols['ks_kano_baby' if '--sonya' in sys.argv else 'ks_sonya_baby'])
        environment['KS_LEG_GATE']=str(symbols.get('ks_leg_gate',0))
        if '--kitana-kiss-victim' in sys.argv:
            inflation_actor='sonya' if '--sonya' in sys.argv else 'kano'
            for phase in range(6):
                environment[f'KS_INFLATE_POSE_{phase}']=str(symbols[f'ks_inf_{inflation_actor}_pose{phase}'])
        if '--body-suck-victim' in sys.argv:
            ingestion_actor='sonya' if '--sonya' in sys.argv else 'kano'
            for phase in range(8):
                environment[f'KS_INGEST_POSE_{phase}']=str(symbols[f'ks_ing_{ingestion_actor}_pose{phase}'])
        if any(flag in sys.argv for flag in ('--extract','--kiss','--bubble','--laser','--baby','--friend','--stage','--clap-victim','--fan-victim','--tongue-victim','--drain-victim','--torso-victim','--swipe-victim','--impale-victim','--superfreeze-victim','--arms-victim','--kitana-kiss-victim','--body-suck-victim','--shang-burst-victim','--raiden-burst-victim','--lao-split-victim')):
            for label in ('winner_status','f_death','f_death2','ground_y','curback','f_thatsall'):
                environment['KS_'+label.upper()]=str(symbols[label])
        if '--friend' in sys.argv or '--stage' in sys.argv or '--baby' in sys.argv:
            for label in ('l_hp','l_lp','p1_bcq','p2_bcq','p1_jcq','p2_jcq'):
                environment['KS_'+label.upper()]=str(symbols[label])
        generated=HERE.parent/'port/generated_ending'
        for chip in range(114,122):
            name=f'l1_mortal_kombat_3_u{chip}_game_rom.u{chip}'
            replacements[name]=(generated/name).read_bytes()
    if art_scene:
        generated=HERE.parent/'port/generated_packed'
        for chip in range(114,122):
            name=f'l1_mortal_kombat_3_u{chip}_game_rom.u{chip}'
            replacements[name]=(generated/name).read_bytes()
        map_name='CYCTEST.MAP' if cycle_scene else 'ARTTEST.MAP'
        symbols={name:int(address,16) for address,name in re.findall(r'\b([0-9a-fA-F]{8})\s+([A-Za-z_]\w*)',(BUILD/'srcw'/map_name).read_text())}
        environment['KS_ART_KANO_PTR']=str(symbols['ks_art_kano_obj'])
        environment['KS_ART_SONYA_PTR']=str(symbols['ks_art_sonya_obj'])
        probe=HERE.parent/'port/diagnostics/art_probe.lua'
        if cycle_scene:
            environment['KS_ART_KANO_STAGE']=str(symbols['ks_art_kano_stage'])
            environment['KS_ART_SONYA_STAGE']=str(symbols['ks_art_sonya_stage'])
            probe=HERE.parent/'port/diagnostics/cycle_probe.lua'
    OUT.mkdir(); (OUT/'roms').mkdir()
    frozen_probe=OUT/'autoboot.lua'
    probe_bytes=probe.read_bytes()
    if '--campaign-projectile-observe' in sys.argv:
        assert '--campaign' in sys.argv and game_candidate and '--sonya' not in sys.argv
        assert not any(arg.startswith('--campaign-stock=') for arg in sys.argv)
        probe_bytes+=b'\n'+(HERE.parent/'port/diagnostics/liu_projectile_observer.lua').read_bytes()
    damage_window=[arg.split('=',1)[1] for arg in sys.argv if arg.startswith('--campaign-observe=')]
    assert len(damage_window)<=1
    if damage_window:
        assert '--campaign' in sys.argv
        damage_begin,damage_end=map(int,damage_window[0].split(':'))
        observation_limit=180000 if '--campaign-finale-window' in sys.argv else (150000 if '--campaign-ending-window' in sys.argv else (120000 if '--campaign-extended' in sys.argv else 90000))
        if '--campaign-boss-endurance' in sys.argv: observation_limit=300000
        assert 0<damage_begin<damage_end<=observation_limit and damage_end-damage_begin<=300
        environment['KS_DAMAGE_BEGIN']=str(damage_begin);environment['KS_DAMAGE_END']=str(damage_end)
        environment['KS_DAMAGE_JCQ']=str(symbols['p1_jcq'])
        environment['KS_DAMAGE_TICK']=str(symbols['tick'])
        environment['KS_DAMAGE_GROUND']=str(symbols['ground_y'])
        probe_bytes+=b'\n'+(HERE.parent/'port/diagnostics/campaign_damage_observer.lua').read_bytes()
    if '--ladder-roster-observe' in sys.argv:
        assert '--campaign' in sys.argv and game_candidate
        environment['KS_LADDER_MAP_POINTER']=str(symbols['map_start'])
        environment['KS_LADDER_WORLD_Y']=str(symbols['worldtly']+16)
        probe_bytes+=b'\n'+(HERE.parent/'port/diagnostics/ladder_roster_observer.lua').read_bytes()
    if '--selection-ui-observe' in sys.argv:
        assert game_candidate and any(flag in sys.argv for flag in ('--campaign','--special'))
        environment['KS_SELECTION_UI_BEGIN']='3000' if '--special' in sys.argv else '3500'
        probe_bytes+=b'\n'+(HERE.parent/'port/diagnostics/selection_ui_observer.lua').read_bytes()
    if '--friend-lifecycle' in sys.argv:
        probe_bytes+=b'\n'+(HERE.parent/'port/diagnostics/friend_lifecycle.lua').read_bytes()
    if '--normal-strike-trace' in sys.argv:
        probe_bytes+=b'\n'+(HERE.parent/'port/diagnostics/normal_strike_trace.lua').read_bytes()
    campaign_streams=[arg.split('=',1)[1] for arg in sys.argv if arg.startswith('--campaign-stream-pipe=')]
    assert len(campaign_streams)<=1
    if campaign_streams:
        assert game_candidate and '--campaign' in sys.argv and '--audio' in sys.argv and '--capture-move' not in sys.argv
        assert re.fullmatch(r'\\\\\.\\pipe\\mk2ks-[0-9a-f]{32}',campaign_streams[0])
        environment['KS_CAMPAIGN_STREAM_PIPE']=campaign_streams[0]
        environment['KS_CAMPAIGN_STREAM_MAX_FIELDS']=environment['KS_CAMPAIGN_FIELDS']
        probe_bytes+=b'\n'+(HERE.parent/'port/diagnostics/campaign_stream_capture.lua').read_bytes()
    if '--capture-move' in sys.argv:
        capture_pipes=[arg.split('=',1)[1] for arg in sys.argv if arg.startswith('--capture-pipe=')]
        assert len(capture_pipes)<=1
        environment.pop('KS_CAPTURE_PIPE',None)
        if capture_pipes:
            assert re.fullmatch(r'\\\\\.\\pipe\\mk2ks-[0-9a-f]{32}',capture_pipes[0])
            environment['KS_CAPTURE_PIPE']=capture_pipes[0]
        requested=[arg.split('=',1)[1] for arg in sys.argv if arg.startswith('--capture-action=')]
        assert len(requested)==1
        action=int(requested[0],0)
        normal_actions=(0x101,0x102,0x103,0x104,0x105,0x106,0x107,0x10e,0x10f,0x113,0x114,0x118,0x119,0x11a,0x200,0x201,0x507)
        assert action in (0x20b,0x211,0x117,0x216,0x207,0x212,0x204,0x219,0x404) or ('--normal-moves' in sys.argv and action in normal_actions)
        environment['KS_CAPTURE_NORMAL']='1' if '--normal-moves' in sys.argv and action in normal_actions else '0'
        environment['KS_CAPTURE_ACTION']=str(action)
        capture_sides=[arg.split('=',1)[1] for arg in sys.argv if arg.startswith('--capture-side=')]
        assert len(capture_sides)<=1
        capture_side=int(capture_sides[0]) if capture_sides else (2 if '--mirror' in sys.argv else 1)
        assert capture_side in (1,2)
        environment['KS_CAPTURE_SIDE']=str(capture_side)
        capture_starts=[arg.split('=',1)[1] for arg in sys.argv if arg.startswith('--capture-not-before=')]
        assert len(capture_starts)<=1
        capture_start=int(capture_starts[0]) if capture_starts else 0
        assert 0<=capture_start<=30000
        environment['KS_CAPTURE_NOT_BEFORE']=str(capture_start)
        capture_lengths=[arg.split('=',1)[1] for arg in sys.argv if arg.startswith('--capture-min-fields=')]
        assert len(capture_lengths)<=1
        capture_min=int(capture_lengths[0]) if capture_lengths else 0
        assert 0<=capture_min<=400
        environment['KS_CAPTURE_MIN_FIELDS']=str(capture_min)
        environment['KS_CAPTURE_MAX_FIELDS']='800' if action==0x404 else '400'
        probe_bytes+=b'\n'+(HERE.parent/'port/diagnostics/move_capture.lua').read_bytes()
    frozen_probe.write_bytes(probe_bytes)
    prepatched=next((arg.split('=',1)[1] for arg in sys.argv if arg.startswith('--prepatched-rom=')),None)
    if prepatched:
        source=Path(prepatched).resolve()
        with zipfile.ZipFile(source) as archive:
            assert len(archive.namelist())==len(set(archive.namelist()))==len(replacements)
            assert set(archive.namelist())==set(replacements)
            assert all(archive.read(name)==data for name,data in replacements.items())
        linked=True
        try: os.link(source,OUT/'roms/mk3.zip')
        except OSError:
            shutil.copyfile(source,OUT/'roms/mk3.zip');linked=False
        archive_storage=dict(prepatchedInput=str(source),archiveSHA256=sha(source.read_bytes()),hardLinked=linked,
                             exactCurrentChipSetVerified=True)
    else:
        archive_storage=prepare_archive(ROOT/'mk3.zip',replacements,HERE/'.test_rom_cache',OUT/'roms/mk3.zip')
    before=sha(MAME.read_bytes())
    guest_limit='2400' if '--campaign-extended' in sys.argv else ('1800' if '--campaign-full' in sys.argv else ('900' if any(flag in sys.argv for flag in ('--pit-progress','--campaign','--cpu-attract')) else ('360' if '--stage-rematch' in sys.argv else '225')))
    if '--campaign-ending-window' in sys.argv: guest_limit='3000'
    if '--campaign-finale-window' in sys.argv: guest_limit='3600'
    if '--campaign-boss-endurance' in sys.argv: guest_limit='6000'
    if '--normal-soak' in sys.argv: guest_limit='600'
    cmd=[str(MAME),'mk3','-rompath',str(OUT/'roms'),'-video','none','-sound','none','-nothrottle','-skip_gameinfo','-autoboot_script',str(frozen_probe),'-seconds_to_run',guest_limit,'-cfg_directory',str(OUT/'cfg'),'-nvram_directory',str(OUT/'nvram'),'-snapshot_directory',str(OUT/'snap')]
    audio=OUT/'native_dcs.wav'
    if '--audio' in sys.argv: cmd += ['-wavwrite',str(audio)]
    wall_limit=90 if any(flag in sys.argv for flag in ('--campaign-long','--cpu-long')) else 60
    if '--campaign-full' in sys.argv: wall_limit=300
    if '--campaign-background-margin' in sys.argv: wall_limit=420
    if '--campaign-boss-endurance' in sys.argv: wall_limit=720
    if '--normal-soak' in sys.argv: wall_limit=120
    if campaign_streams: wall_limit=720
    with (OUT/'mame.log').open('w') as log:
        try:
            p=subprocess.run(cmd,cwd=OUT,stdout=log,stderr=subprocess.STDOUT,timeout=wall_limit,env=environment,
                             creationflags=(subprocess.CREATE_NO_WINDOW|subprocess.BELOW_NORMAL_PRIORITY_CLASS) if os.name=='nt' else 0)
            status=dict(exitCode=p.returncode,timedOut=False)
        except subprocess.TimeoutExpired: status=dict(exitCode=None,timedOut=True)
    assert sha(MAME.read_bytes())==before
    report=dict(emulator=str(MAME),emulatorSHA256=before,stockHardware='mk3 Wolf-unit',customDriver=False,gameMemoryWrites=False,nativeArtDiagnostic=art_scene,nativeInitialPhaseMatrix=cycle_scene,
                nativeGameplayCandidate=game_candidate,playablePortVerified=False,diagnosticSoundTrack=sound_track,
                controllerSHA256=sha(frozen_probe.read_bytes()),testArguments=sys.argv[2:],wallTimeoutSeconds=wall_limit,guestSecondsLimit=int(guest_limit),
                replacementChips={n:sha(b) for n,b in replacements.items()},archiveStorage=archive_storage,**status)
    if audio.exists():
        with wave.open(str(audio),'rb') as w:
            assert w.getsampwidth()==2
            peak=0; frames=w.getnframes(); rate=w.getframerate(); channels=w.getnchannels()
            while block:=w.readframes(16384): peak=max(peak,max(map(abs,array.array('h',block)),default=0))
        report['nativeDCSAudio']=dict(peakPCM16=peak,frames=frames,rate=rate,channels=channels,
                                     nonSilent=peak>0,hostSampleDevice=False)
    (OUT/'execution.json').write_text(json.dumps(report,indent=2)); print(json.dumps(report,indent=2))
if __name__=='__main__': main()
