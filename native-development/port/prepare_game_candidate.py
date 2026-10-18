"""Prepare an isolated, source-linked native roster candidate (not a release).

Each data extension checks its original typed size. No emulator modification,
ROM-memory dump or implicit replacement of an actor ID is used.
"""
import difflib
import hashlib
import json
import re
import zipfile
from pathlib import Path
from inventory_character_tables import source_tables
from morph_source import add_morphs,add_morph_art
from baby_source import add_baby_images,add_baby_commands
from friendship_source import integrate as integrate_friendship
from pit_source import integrate as integrate_pit
from drone_source import integrate as integrate_drone,integrate_attract,integrate_demo_game
from throw_source import integrate as integrate_throw
from deadpool_source import integrate as integrate_deadpool,integrate_wait as integrate_deadpool_wait
from dcs_source import integrate as integrate_dcs
from announcer_source import integrate as integrate_announcer
from ending_source import winner as integrate_ending_winner,story as integrate_ending_story,cast as integrate_ending_cast
from boss_category_source import integrate as integrate_boss_categories
from cpu_action_source import integrate as integrate_cpu_actions
from frozen_palette_source import integrate as integrate_frozen_palettes
from shadow_bank_source import integrate as integrate_shadow_banks
from spear_alignment_source import integrate as integrate_spear_alignment
from shocker_alignment_source import integrate as integrate_shocker_alignment
from dive_alignment_source import integrate as integrate_dive_alignment
from blocked_flying_source import integrate as integrate_blocked_flying
from superfreeze_source import integrate as integrate_superfreeze
from leg_ground_source import integrate as integrate_leg_ground
from arm_rip_source import integrate as integrate_arm_rip
from kiss_setup_source import integrate as integrate_kiss_setup
from kiss_inflate_source import integrate as integrate_kiss_inflate
from ingestion_source import integrate as integrate_ingestion
from shang_burst_source import integrate as integrate_shang_burst
from lao_split_source import integrate as integrate_lao_split
from ladder_source import selector as integrate_ladder_selector,difficulty as integrate_ladder_difficulty,secrets as integrate_ladder_secrets
HERE=Path(__file__).resolve().parent
BASE=HERE.parent/'baseline/mk2-rebuild-main'
DEST=BASE/'srcp'
ZIP=Path('C:/Users/kando/Downloads/mk2-rebuild-main.zip')
def sha(b):return hashlib.sha256(b).hexdigest().upper()
def main(audit=False):
    if not audit:
        assert not DEST.exists(),'Never overwrite a source candidate'
    assert sha(ZIP.read_bytes())=='2EE5C1FAD3122B6A7FE20AEF948CF96E54D4625DA073CA64273372817961A4A5'
    with zipfile.ZipFile(ZIP) as z:
        originals={Path(n).name:z.read(n).decode('cp437') for n in z.namelist() if n.startswith('mk2-rebuild-main/src/') and n.count('/')==2 and not n.endswith('/')}
    texts=dict(originals)
    for active,chosen in [('WEQU.ASM','W-EQU.ASM'),('SYSEQU.ASM','SYSEQUW.ASM'),('MAINEQU.ASM','MAINEQUW.ASM')]:texts[active]=texts[chosen]
    changes=[]
    def append(file,label,expected_bits,rows,before_zero=False):
        text=texts[file]; table=source_tables(text)[label]
        bits=sum({'word':16,'long':32,'byte':8}[r['type']]*len(r['values']) for r in table['rows'])
        assert bits==expected_bits,(file,label,bits,expected_bits)
        at=table['rows'][-1]['line']
        if before_zero:
            assert table['rows'][-1]['values']==['0'];at-=1
        lines=text.splitlines(keepends=True)
        lines[at:at]=['; MK2KS native source extension\n']+[row+'\n' for row in rows]
        texts[file]=''.join(lines);changes.append(dict(file=file,table=label,originalBits=bits,added=rows))
    def refs(file,names):
        texts[file]=''.join('\t.ref '+name+'\n' for name in names)+texts[file]
    for file in ('MAINEQUW.ASM','MAINEQU.ASM'):
        marker='ft_jade\t\t.set\t16\t; jade the bitch'
        assert texts[file].count(marker)==1
        texts[file]=texts[file].replace(marker,marker+'\nft_kano\t\t.set\t17\nft_sonya\t.set\t18')
    for label,kind,extra in [
        ('character_anitabs1','long',['ks_kano_anitab1','ks_sonya_anitab1']),
        ('character_anitabs2','long',['ks_kano_anitab2','ks_sonya_anitab2']),
        ('character_palettes_1','long',['ks_kano_primary_palette','ks_sonya_primary_palette']),
        ('character_palettes_2','long',['ks_kano_alternate_palette','ks_sonya_alternate_palette']),
        ('shadow_adjustments','word',['2','2']),('stance_speeds','word',['5','5']),
        ('ochar_ground_offsets','word',['131','132'])]:
        append('MKGUYS.ASM',label,17*(32 if kind=='long' else 16),['\t.'+kind+' '+v for v in extra])
    for label in ('walk_forward_info','walk_backward_info'):
        pair='5,02800h' if label=='walk_forward_info' else '6,02000h'
        append('MKGUYS.ASM',label,17*32,['\t.word '+pair,'\t.word '+pair])
    # Authored death sprites use the own body color indices, including their
    # painted neck wounds. A Liu bloody palette cannot recolor these indices.
    append('MKGUYS.ASM','bloody_palettes',15*64,[
        '\t.long noob_p,noob_p','\t.long JADE_P,JADE_P',
        '\t.long ks_kano_primary_palette,ks_kano_alternate_palette',
        '\t.long ks_sonya_primary_palette,ks_sonya_alternate_palette'])
    # Explicit native victim records; own alignment remains a visual test gate.
    append('MKDEATH.ASM','head_lineups',16*64,[
        '\t.word -0b8h,-5,010h,020h ; Jade',
        '\t.word -0bbh,0,010h,020h ; Kano: own main10 second pose',
        '\t.word -0bbh,-1,010h,020h ; Sonya: own132 vs Reptile131 ground offset'])
    # match_him_with_me_f copies Jax's139-pixel grounded animation anchor.
    # Restore each own body ground plane (131/132) after that copy. Keep
    # the standard96-pixel horizontal lineup; visual clap contact is a gate.
    append('MKDEATH.ASM','clapped_lineups',16*32,[
        '\t.word -060h,0 ; Jade: native standard horizontal lineup',
        '\t.word -060h,8 ; Kano: Jax139 minus own131',
        '\t.word -060h,7 ; Sonya: Jax139 minus own132'])
    append('MKFX.ASM','drain_table',16*32,[
        '\t.long a_fn1drained,ks_kano_drain_shrink,ks_sonya_drain_shrink'])
    append('MKFX.ASM','alternate_suck_pals',12*32,[
        '\t.long TMG_SK_P,TMG_SK_P,TMG_SK_P,TMG_SK_P,TMG_SK_P',
        '\t.long ks_kano_primary_palette,ks_sonya_primary_palette'])
    refs('MKFX.ASM',['ks_kano_drain_shrink','ks_sonya_drain_shrink',
                       'ks_kano_primary_palette','ks_sonya_primary_palette'])
    for label in ('menu_ochars','unxlate_table'):
        append('MKGUYS.ASM',label,12*16,['\t.word 17,18'])
    refs('MKGUYS.ASM',['ks_kano_anitab1','ks_sonya_anitab1','ks_kano_anitab2','ks_sonya_anitab2',
        'ks_kano_primary_palette','ks_sonya_primary_palette','ks_kano_alternate_palette','ks_sonya_alternate_palette'])
    # Independent descriptor allocations, seeded from the common native attack
    # family for first combat tests. Final own-hitbox/move acceptance is pending.
    text=texts['MKSTK.ASM'];start=text.index('\nlk_strikes\n');end=text.index('\nhh_strikes\n',start)
    seed=text[start:end];labels=re.findall(r'^([A-Za-z_]\w*)\s*(?:\n|\.)',seed,re.M)
    assert 'lk_strikes' in labels and len(labels)>=24
    clones=[]
    for fighter in ('kano','sonya'):
        mapping={label:f'ks_{fighter}_{label}' for label in labels}
        clones.append(re.sub(r'\b[A-Za-z_]\w*\b',lambda m:mapping.get(m[0],m[0]),seed))
    texts['MKSTK.ASM']=text[:end]+''.join(clones)+text[end:]
    append('MKSTK.ASM','strike_tables',17*32,['\t.long ks_kano_lk_strikes','\t.long ks_sonya_lk_strikes'])
    for fighter,geometry in [('kano','35,-24,51,50'),('sonya','108,35,36,11')]:
        old=f'\t.long\tks_{fighter}_stk_lkzap4'
        new=f'\t.long ks_{fighter}_stk_projectile'
        assert texts['MKSTK.ASM'].count(old)==1
        texts['MKSTK.ASM']=texts['MKSTK.ASM'].replace(old,new)
        descriptor=f'\nks_{fighter}_stk_projectile\n\t.word {geometry}\n\t.word 01110h,01605h\n\t.long 0\n\t.word sf_squeeze\n'
        texts['MKSTK.ASM']=texts['MKSTK.ASM'].replace('\nhh_strikes\n',descriptor+'\nhh_strikes\n')
    append('MKSTK.ASM','ks_sonya_lk_strikes',23*32,['\t.long ks_sonya_stk_ring_close'])
    texts['MKSTK.ASM']=texts['MKSTK.ASM'].replace('\nhh_strikes\n','\nks_sonya_stk_ring_close\n\t.word 77,35,47,27\n\t.word 01110h,01605h\n\t.long 0\n\t.word sf_squeeze\n\nhh_strikes\n')
    append('MKZAP.ASM','p1p2_proj_pids',16*32,['\t.word pid_proj1,pid_proj2']*3)
    append('MKZAP.ASM','ochar_proj_oids',12*32,['\t.word 0,0']*5+['\t.word 0711h,0711h','\t.word 0712h,0712h'])
    texts['MKZAP.ASM']='\t.def delete_proj_and_die,dead_projectile,proj_strike_check,tell_world_stk\n'+texts['MKZAP.ASM']
    text=texts['MKREACT.ASM'];start=text.index('\nreact_to_lk\n');end=text.index('\nreact_to_hh\n',start)
    seed=text[start:end]
    texts['MKREACT.ASM']=text[:end]+seed.replace('react_to_lk','ks_react_to_kano')+seed.replace('react_to_lk','ks_react_to_sonya')+text[end:]
    append('MKREACT.ASM','reaction_tables',17*32,['\t.long ks_react_to_kano','\t.long ks_react_to_sonya'])
    append('MKREACT.ASM','ks_react_to_kano',25*32,['\t.long ks_blade_hurt'])
    append('MKREACT.ASM','ks_react_to_kano',26*32,['\t.long ks_choke_wait'])
    refs('MKREACT.ASM',['ks_choke_wait'])
    append('MKREACT.ASM','ks_react_to_sonya',25*32,['\t.long ks_leg_wait,ks_bike_wait'])
    refs('MKREACT.ASM',['ks_leg_wait'])
    append('MKREACT.ASM','getup_speeds',17*16,['\t.word 4,4'])
    refs('MKREACT.ASM',['ks_bike_wait','illegal_opcode'])
    refs('MKREACT.ASM',['ks_blade_hurt'])
    texts['MKREACT.ASM']='\t.def reaction_start_abc,airborn_hit_no_sound,land_on_my_back\n'+texts['MKREACT.ASM']
    append('MKREACT.ASM','block_starts',17*32,['\t.long 0,0'])
    append('MKREACT.ASM','rs_calls',17*32,['\t.long 0,0'])
    append('MKREACT.ASM','post_fb_xfers',17*32,['\t.long tossed_flight,tossed_flight'])
    # Ordinary movement/attack rates, not a proxy fighter's special handlers.
    append('JOY.ASM','ochar_damage_table',17*32,['\t.long 0,0'])
    append('JOY.ASM','ochar_power_punches',12*32,['\t.long 0,0,0,0,0,0,0'])
    old='\tcallr\tstrike_check_a0\t\t; additional strike checks\n'
    assert texts['JOY.ASM'].count(old)==1
    texts['JOY.ASM']=texts['JOY.ASM'].replace(old,old+'\tjrnc\tpsl2\n\tclr\ta11\n\tnot\ta11\t\t\t; consume late-hit collision window\n')
    append('MAIN.ASM','winner_text',17*32,['\t.long ks_pf_kano_win,ks_pf_sonya_win'])
    append('MAIN.ASM','winner_speech',17*16,['\t.word 0,0'])
    texts['MAIN.ASM']=texts['MAIN.ASM'].replace('\npf_times_up\n','\nks_pf_kano_win\n\tmess_mac rd15font,2,200,038H,bpal_flash1*010000H,strcnrmos_scr,0\n\t.byte "KANO WINS",0\n\t.even\nks_pf_sonya_win\n\tmess_mac rd15font,2,200,038H,bpal_flash1*010000H,strcnrmos_scr,0\n\t.byte "SONYA WINS",0\n\t.even\n\npf_times_up\n')
    for label,words in [('elbow_pauses','14,14'),('elbow_speeds','2,2'),('round_speeds','3,3')]:
        append('MOVES.ASM',label,17*16,['\t.word '+words])
    append('MOVES.ASM','knee_hit_sleeps',15*16,['\t.word 20,20,20,20'])
    append('MOVES.ASM','ta_speeds',17*32,['\t.word 2,0,2,0'])
    tables=source_tables(texts['MOVES.ASM'])
    for label in sorted(n for n in tables if n.startswith('char_')):
        table=tables[label]
        if not all(r['type']=='long' for r in table['rows']):continue
        count=sum(len(r['values']) for r in table['rows'])
        assert count==12,(label,count)
        kano={'char_lo_kick':'ks_baby_kick','char_lok_open':'ks_kano_lk_release','char_hi_punch':'ks_kano_high_punch','char_lo_punch':'ks_kano_low_punch','char_hi_kick':'ks_kano_high_kick'}.get(label,'sucide')
        sonya={'char_lo_kick':'ks_baby_kick','char_hi_punch':'ks_sonya_high_punch','char_lo_punch':'ks_sonya_low_punch','char_hi_kick':'ks_sonya_high_kick','char_block':'ks_sonya_block','char_hik_open':'ks_sonya_block'}.get(label,'sucide')
        append('MOVES.ASM',label,12*32,['\t.long sucide,sucide,sucide,sucide,sucide',f'\t.long {kano},{sonya}'])
    refs('MOVES.ASM',['ks_kano_lk_release','ks_sonya_high_punch','ks_kano_high_punch','ks_sonya_low_punch'])
    refs('MOVES.ASM',['ks_sonya_high_kick'])
    refs('MOVES.ASM',['ks_kano_low_punch'])
    refs('MOVES.ASM',['ks_sonya_block'])
    refs('MOVES.ASM',['ks_kano_high_kick'])
    refs('MOVES.ASM',['ks_baby_kick'])
    texts['MOVES.ASM']='\t.def fatality_xfer_close,fatality_xfer,button_look_lr\n'+texts['MOVES.ASM']
    texts['MOVES.ASM']='\t.def button_mask,do_switches_match\n'+texts['MOVES.ASM']
    texts['MOVES.ASM']='\t.def check_dtp\n'+texts['MOVES.ASM']
    texts['MOVES.ASM']=add_morphs(texts['MOVES.ASM'])
    texts['MOVES.ASM'],count=re.subn(r'(?m)^(\tcmpi\tft_jade,a2[^\n]*\n\tjreq\tuseless_splits[^\n]*\n)',
        r'\1\tcmpi 18,a2\n\tjreq useless_splits ; Sonya follows native female immunity\n',texts['MOVES.ASM'])
    assert count==1,count
    texts['MKST.ASM']=add_morph_art(texts['MKST.ASM'])
    texts['MKBABY.ASM']=add_baby_images(texts['MKBABY.ASM'])
    texts['MKBABY.ASM']=add_baby_commands(texts['MKBABY.ASM'])
    texts['MKFRIEND.ASM']='\t.def friendship_start,friendship_end,fs_get_tsl\n'+texts['MKFRIEND.ASM']
    texts['MKFRIEND.ASM']=integrate_friendship(texts['MKFRIEND.ASM'])
    texts['MKFALL.ASM']=integrate_pit(texts['MKFALL.ASM'])
    texts['MKDRONE.ASM']=integrate_drone(texts['MKDRONE.ASM'])
    texts['MKDRONE.ASM']=integrate_cpu_actions(texts['MKDRONE.ASM'])
    texts['MKBOSS.ASM']=integrate_boss_categories(texts['MKBOSS.ASM'])
    texts['MKAMODE.ASM']=integrate_attract(texts['MKAMODE.ASM'])
    texts['MAIN.ASM']=integrate_demo_game(texts['MAIN.ASM'])
    texts['MKSLAM.ASM']=integrate_throw(texts['MKSLAM.ASM'])
    texts['MOVES.ASM']=integrate_deadpool(texts['MOVES.ASM'])
    texts['BGND.ASM']=integrate_deadpool_wait(texts['BGND.ASM'])
    texts['MKSOUND.ASM']=integrate_dcs(texts['MKSOUND.ASM'])
    texts['MKEND.ASM']=integrate_ending_cast(integrate_ending_winner(texts['MKEND.ASM']))
    texts['UNZIP.ASM']=integrate_ending_story(texts['UNZIP.ASM'])
    texts['MKSOUND.ASM'],texts['MKSEL.ASM'],texts['MAIN.ASM']=integrate_announcer(
        texts['MKSOUND.ASM'],texts['MKSEL.ASM'],texts['MAIN.ASM'])
    texts['MKGUYS.ASM']=integrate_frozen_palettes(texts['MKGUYS.ASM'])
    texts['MKDISP.ASM']=integrate_shadow_banks(texts['MKDISP.ASM'])
    texts['MKZAP.ASM']=integrate_spear_alignment(texts['MKZAP.ASM'])
    texts['MOVES.ASM']=integrate_shocker_alignment(texts['MOVES.ASM'])
    texts['MKPROP.ASM']=integrate_dive_alignment(texts['MKPROP.ASM'])
    texts['MKREACT.ASM']=integrate_blocked_flying(texts['MKREACT.ASM'])
    texts['MKDEATH.ASM']=integrate_superfreeze(texts['MKDEATH.ASM'])
    for file in ('MKDEATH.ASM','MKBLOOD.ASM'):texts[file]=integrate_arm_rip(texts[file],file)
    texts['MKDEATH.ASM']=integrate_kiss_setup(texts['MKDEATH.ASM'])
    for file in ('MKDEATH.ASM','MKDIE.ASM'):texts[file]=integrate_kiss_inflate(texts[file],file)
    texts['MKDIE.ASM']=integrate_ingestion(texts['MKDIE.ASM'])
    texts['MKDEATH.ASM']=integrate_shang_burst(texts['MKDEATH.ASM'])
    texts['MKDEATH.ASM']=integrate_lao_split(texts['MKDEATH.ASM'])
    texts['MKDEATH.ASM']=integrate_leg_ground(texts['MKDEATH.ASM'])
    # Wolf LP/LK are in the main input longword, unlike the T-unit harness.
    old='\nbutton_mask\n'
    assert texts['MOVES.ASM'].count(old)==1
    wolf_mask='''\t.if wunit
* Wolf LP/LK occupy the upper half of the main input longword, not switch2.
* Keep P1's native bits; translate P2 LP/LK into the engine's fake mask bits.
\tmove\t@switch,a2,l
\tnot\ta2
\tmove\ta2,a3
\tandi\tp1b0|p1b1|p1b2|p1b3|p1b4|p2b0|p2b2|p2b3,a2
\tbtst\t20,a3
\tjreq\twbmask1
\tori\tf2b1,a2
wbmask1
\tbtst\t21,a3
\tjreq\twbmask2
\tori\tf2b4,a2
wbmask2
* MKII also treats the Wolf harness Run input as the redundant Block button.
\tbtst\t18,a3
\tjreq\twbmask3
\tori\tf1b2,a2
wbmask3
\tbtst\t22,a3
\tjreq\twbmask4
\tori\tf2b2,a2
wbmask4
\t.else
'''
    texts['MOVES.ASM']=texts['MOVES.ASM'].replace(old,old+wolf_mask)
    old='bmask4\tandi\tp1b1|p1b4,a3\t\t\t; we dont need em any more\n\tor\ta3,a2\n'
    assert texts['MOVES.ASM'].count(old)==1
    texts['MOVES.ASM']=texts['MOVES.ASM'].replace(old,old+'\t.endif\n')
    refs('MKDISP.ASM',['ks_pair_boundary'])
    old='\ngravity_n_bounds\n'
    assert texts['MKDISP.ASM'].count(old)==1
    texts['MKDISP.ASM']=texts['MKDISP.ASM'].replace(old,old+'\tcalla ks_pair_boundary\n\tjrc kib7\n')
    exports=json.loads((HERE/'generated_leg/SOURCE_EXPORTS.json').read_text())
    for file,labels in exports.items():
        assert re.fullmatch(r'MK[A-Z0-9]+\.ASM',file) and file in texts
        texts[file]=''.join('\t.def '+label+'\n' for label in labels)+texts[file]
    exports=json.loads((HERE/'generated_extract/SOURCE_EXPORTS.json').read_text())
    for file,labels in exports.items():
        for label,alias in labels.items():
            pattern=r'(?m)^'+re.escape(label)+r'(?=\s)'
            texts[file],count=re.subn(pattern,alias+'\n'+label,texts[file])
            assert count==1,(file,label,count)
            texts[file]='\t.def '+alias+'\n'+texts[file]
    old='rsnd_ochar\n\tmove\t*a8(ochar),a2,w\n'
    assert texts['MKSOUND.ASM'].count(old)==1
    texts['MKSOUND.ASM']=texts['MKSOUND.ASM'].replace(old,old+'\tcmpi\tft_sonya,a2\n\tjreq\trsnd_female\n')
    append('MKSLAM.ASM','throw_ani_speeds',17*16,['\t.word 4,4'])
    refs('MKDEATH.ASM',['ks_kano_extract','ks_sonya_flame_kiss','ks_sonya_bubble','ks_kano_laser'])
    texts['MKDEATH.ASM']='\t.def disable_repell\n'+texts['MKDEATH.ASM']
    texts['MKDIE.ASM']='\t.def explode,exp_burst,bone_land\n'+texts['MKDIE.ASM']
    # A short-lived multipart object can retire before its dummy ever wakes.
    # Both native dummy entry points must be recognized; keep non-dummies alive.
    old='kmo_proc\n\tmove\t*a2(oslink),a0,l\t; proc\n\tmove\t*a0(pwake),a1,l\n'
    assert texts['MKUTIL.ASM'].count(old)==1
    texts['MKUTIL.ASM']=texts['MKUTIL.ASM'].replace(old,
        'kmo_proc\n\tmove\t*a2(oslink),a0,l\t; proc\n\tmove\ta0,a0\n\tjreq\tkmop3\n'
        '\tmove\t*a0(pwake),a1,l\n\tcmpi\tmulti_dummy_proc,a1\t; never-woken multipart dummy\n\tjreq\tkmopkill\n')
    old='\tcalla\tkill\t\t\t; yes, kill proc\nkmop3'
    assert texts['MKUTIL.ASM'].count(old)==1
    texts['MKUTIL.ASM']=texts['MKUTIL.ASM'].replace(old,'kmopkill'+old+'')
    append('MKDEATH.ASM','db1_table',12*32,[
        '\t.long null_death_blow,null_death_blow,null_death_blow,null_death_blow,null_death_blow',
        '\t.long ks_kano_extract,ks_sonya_flame_kiss'])
    append('MKDEATH.ASM','db2_table',12*32,[
        '\t.long null_death_blow,null_death_blow,null_death_blow,null_death_blow,null_death_blow',
        '\t.long ks_kano_laser,ks_sonya_bubble'])
    append('MKSLAM.ASM','ochar_nonflip_adjx',17*16,['\t.word 0,0'])
    append('MKCANNED.ASM','victory_jumps',17*32,['\t.long generic_victory,generic_victory'])
    # Valid empty native images avoid mislabeled Liu bars in the development
    # candidate. Correct own name images/shadows remain an explicit release gate.
    append('MKDISP.ASM','p1_powerbar_names',17*64,['\t.long ks_bar_kano,0001e001dh','\t.long ks_bar_sonya,0001e001dh'])
    append('MKDISP.ASM','p2_powerbar_names',17*64,['\t.long ks_bar_kano,0001e0149h','\t.long ks_bar_sonya,0001e0140h'])
    refs('MKDISP.ASM',['ks_bar_kano','ks_bar_sonya'])
    # Real selector: append dedicated native photos, preserve stock border and
    # player-number construction, replace directional calculations in source.
    append('MKSEL.ASM','mug_shot_table',12*64+32,[
        '\t.long ks_kano_selector','\t.word 23,24','\t.long ks_sonya_selector','\t.word 323,24'],True)
    append('MKSEL.ASM','picked_palettes',12*32,[
        '\t.long BOX1D_P,BOX1D_P,BOX1D_P,BOX1D_P,BOX1D_P',
        '\t.long ks_kano_locked_palette,ks_sonya_locked_palette'])
    append('MKSEL.ASM','mini_mug_table',17*32,['\t.long ks_kano_ladder,ks_sonya_ladder'])
    text=texts['MKSEL.ASM']
    mapped={'mto_table':'ks_menu_ids','otm_table':'ks_id_menu','up_change':'ks_up_change','down_change':'ks_down_change',
            'left_change':'ks_left_change','right_change':'ks_right_change','upsans':'ks_up_sans','dnsans':'ks_down_sans',
            'lfsans':'ks_left_sans','rtsans':'ks_right_sans'}
    for old,new in mapped.items():text=re.sub(r'\b'+old+r'(?=\s*,)',new,text)
    a=text.index('\nis_move_legal\n');b=text.index('\nupsans',a)
    text=text[:a]+'\nis_move_legal\n\tjauc ks_move_legal\n'+text[b:]
    pattern=r'\tsll\s+4,a1[^\n]*\n\tadd\s+a2,a1[^\n]*\n\tmove\s+\*a1,a1,w[^\n]*'
    text,n=re.subn(pattern,'\tcalla ks_cursor_destination',text);assert n==2,n
    text,n=re.subn(r'\tmovk\s+12,a0(?=\s*\n)', '\tmovk 14,a0',text);assert n==1,n
    texts['MKSEL.ASM']=text
    refs('MKSEL.ASM',list(mapped.values())+['ks_cursor_destination','ks_move_legal','ks_kano_selector','ks_sonya_selector',
            'ks_kano_locked_palette','ks_sonya_locked_palette','ks_kano_ladder','ks_sonya_ladder'])
    texts['MKSEL.ASM']=integrate_ladder_selector(texts['MKSEL.ASM'])
    texts['MAIN.ASM']=integrate_ladder_difficulty(texts['MAIN.ASM'])
    texts['MKTOAST.ASM']=integrate_ladder_secrets(texts['MKTOAST.ASM'])
    if not audit:
        DEST.mkdir()
    generated={}
    # Original root source/include text only. No stale objects, disassemblies,
    # executable tools or private data are copied into this source candidate.
    allowed={'.ASM','.TBL','.HDR','.GLO','.H','.EQU','.INI','.CMD'}
    for name,text in texts.items():
        if Path(name).suffix.upper() in allowed or name.upper()=='MAKEFILE':
            generated[name]=text.replace('\r\n','\n').replace('\n','\r\n').encode('cp437')
            if not audit:
                (DEST/name).write_bytes(generated[name])
    modules={}
    for folder in ('asm','generated_packed','generated_templates_candidate','generated_roster_roots','generated_ui_packed','generated_projectiles','generated_blade','generated_bike','generated_choke','generated_leg','generated_finishers','generated_extract','generated_kiss','generated_bubble','generated_laser','generated_baby','generated_names','generated_friendship','generated_pit','generated_throw','generated_backbreak','generated_frozen','generated_arm_rip','generated_inflation_v3','generated_ingestion','generated_split'):
        for p in (HERE/folder).glob('*.ASM'):
            assert p.name not in modules,p.name
            modules[p.name]=p.read_bytes();generated[p.name]=modules[p.name]
            if not audit:
                (DEST/p.name).write_bytes(modules[p.name])
    for p in list((HERE/'generated_heads').glob('*.ASM'))+list((HERE/'generated_decap').glob('*.ASM'))+list((HERE/'generated_drain').glob('*.ASM'))+list((HERE/'generated_torso').glob('*.ASM')):
        assert p.name not in modules,p.name
        modules[p.name]=p.read_bytes();generated[p.name]=modules[p.name]
        if not audit:
            (DEST/p.name).write_bytes(modules[p.name])
    for p in list((HERE/'generated_reactions').glob('*.ASM'))+list((HERE/'generated_nut').glob('*.ASM'))+list((HERE/'generated_impale').glob('*.ASM')):
        assert p.name not in modules,p.name
        modules[p.name]=p.read_bytes();generated[p.name]=modules[p.name]
        if not audit:
            (DEST/p.name).write_bytes(modules[p.name])
    link=texts['MK2NEWW.CMD'].replace('-o mk2neww.out','-o MK2P.OUT').replace('-m mk2new.map','-m MK2P.MAP')
    marker='MEMORY        ';assert link.count(marker)==1
    for p in (HERE/'generated_morph').glob('*.ASM'):
        assert p.name not in modules
        modules[p.name]=p.read_bytes()
        generated[p.name]=modules[p.name]
        if not audit:(DEST/p.name).write_bytes(modules[p.name])
    for p in (HERE/'generated_ending').glob('*.ASM'):
        assert p.name not in modules
        modules[p.name]=p.read_bytes();generated[p.name]=modules[p.name]
        if not audit:(DEST/p.name).write_bytes(modules[p.name])
    module_order=(HERE/'native_module_order.txt').read_text().splitlines()
    assert len(module_order)==len(set(module_order))==len(modules)
    assert set(module_order)=={Path(n).with_suffix('.OBJ').name for n in modules}
    link=link.replace(marker,'\n'.join(module_order)+'\n\n'+marker)
    generated['MK2NEWW.CMD']=link.replace('\r\n','\n').replace('\n','\r\n').encode('utf-8')
    if not audit:
        (DEST/'MK2NEWW.CMD').write_text(link)
    if audit:
        return generated
    patches={}
    for name,text in texts.items():
        if name in originals and text!=originals[name]:
            diff=''.join(difflib.unified_diff(originals[name].splitlines(keepends=True),text.splitlines(keepends=True),fromfile='base/'+name,tofile='port/'+name))
            patches[name]=diff
    result=dict(sourceCandidate=str(DEST),changedOriginalFiles=sorted(patches),dataExtensions=changes,
                patches=patches,originalInputSHA256=sha(ZIP.read_bytes()),nativeActorIDs=[17,18],
                compiled=False,playable=False,releaseReady=False,
                explicitGaps=['original special-root caller reachability audit',
                              'native move/selection/winner audio and final mix',
                              'AI and remaining secondary character-table acceptance',
                              'full campaign progression/completion qualification',
                              'all gameplay, victim, interruption, edge and UI acceptance',
                              'reproducible clean build and ROM-patch release validation'])
    (HERE/'GAME_CANDIDATE_PREPARATION.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ('patches','dataExtensions')},indent=2))
if __name__=='__main__':main()
