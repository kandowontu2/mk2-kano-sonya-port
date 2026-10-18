"""Native own-ID kiss inflation dispatch; no original roster substitutions."""
from arm_rip_source import lookup

DIE = (
    lookup('inflate_animations', 'get_char_long', 'ks_kano_inflated',
           'ks_sonya_inflated', 'inf_ani'),
    lookup('inflate_palettes', 'get_char_long', 'ks_kano_primary_palette',
           'ks_sonya_primary_palette', 'inf_pal'),
    lookup('pop_palettes', 'get_char_long', 'ks_kano_primary_palette',
           'ks_sonya_primary_palette', 'pop_pal'),
)
DEATH = (lookup('kissed_coor_adj', 'get_his_char_word', '-04cH', '-04cH',
               'kiss_xy', other=True),)
WAIT_OLD = '\tmovi\tr_kissed,a7\n\tcalla\ttakeover_him\n\tsleep\t060H\n'
# Historical negative fixture for tests; never emitted by integrate().
WAIT_NEW = WAIT_OLD+'''	move *a13(p_otherguy),a0,l
\tmove *a0(ochar),a0,w
\tcmpi 17,a0
\tjreq ks_inf_wait_pop
\tcmpi 18,a0
\tjrne ks_inf_wait_done
ks_inf_wait_pop
\tmovi 0100H,a10 ; bounded native wait, never a permanent softlock
ks_inf_wait_loop
\tmove *a13(p_otherguy),a0,l
\tmove *a0(oflags2),a0,w
\tandi m_inviso,a0
\tjrne ks_inf_pop_done
\tsleep 1
\tdsj a10,ks_inf_wait_loop
\tjruc ks_inf_wait_done
ks_inf_pop_done
\tsleep 040H ; allow native explosion objects to develop
ks_inf_wait_done
'''


def integrate(text, file):
    assert file in ('MKDIE.ASM', 'MKDEATH.ASM')
    for old, new in DIE if file == 'MKDIE.ASM' else DEATH:
        assert text.count(old) == 1, (file, old)
        text = text.replace(old, new)
    if file == 'MKDEATH.ASM':
        assert text.count(WAIT_OLD) == 1
        # Keep native master timing. Effect processes may render after the
        # completion flag; diagnostics must observe that later lifecycle.
    if file == 'MKDIE.ASM':
        assert text.count('\ninflate_pose\n') == 1
        text = text.replace('\ninflate_pose\n',
            '\n\t.ref ks_kano_inflated,ks_sonya_inflated\n'
            '\t.ref ks_kano_primary_palette,ks_sonya_primary_palette\n'
            'inflate_pose\n')
    return text
