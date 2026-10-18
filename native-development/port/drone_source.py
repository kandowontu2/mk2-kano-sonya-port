"""Deliberate native AI table extensions; no actor-ID substitution."""
from inventory_character_tables import source_tables

# Generic non-signature reaction thresholds, in original engine coordinates.
# These choices do not grant either actor another fighter's special move.
SCALAR_EXTENSIONS={
    'backflipper_x_dist':('050H','050H'),
    'rh_air_distances':('040H','040H'),
    'divesd_x_dist':('080H','080H'),
    'fntele_heights':('070H','070H'),
    'superkang_zap_dist':('0d0H','0d0H'),
}
DISPATCH_TABLES=(
    'ochar_drone_start','rt_special_start','ochar_propells','zap_offsets',
    'ochar_superk_sd','angle_towards_reactions','close_out_of_air',
    'med_out_of_air','ochar_avoid_pro','skull_escape','ochar_fatality_distances',
)
DISPATCH_EXTENSIONS={
    'ochar_drone_start':('generic_drone_start','generic_drone_start'),
    'rt_special_start':('ks_ai_kano_special','ks_ai_sonya_special'),
    'ochar_propells':('ks_ai_kano_propell','ks_ai_sonya_air'),
    'zap_offsets':('-1','-1'), # Own projectile hooks precede generic zap lookup.
    'ochar_superk_sd':('drone_uppercut_jump','drone_uppercut_jump'),
    'angle_towards_reactions':('simple_angle','ks_ai_sonya_air'),
    'close_out_of_air':('quick_flip_attack','ks_ai_sonya_air'),
    'med_out_of_air':('rh_ooa','ks_ai_sonya_air'),
    'ochar_avoid_pro':('ks_ai_kano_propell','ks_ai_sonya_projectile'),
    'skull_escape':('ks_ai_kano_propell','0'),
}

def integrate_dispatch(text):
    for name,extra in DISPATCH_EXTENSIONS.items():
        table=source_tables(text)[name]
        values=[v for row in table['rows'] for v in row['values']]
        assert len(values)==17,name
        kind=table['rows'][0]['type']
        lines=text.splitlines(keepends=True)
        lines[table['rows'][-1]['line']:table['rows'][-1]['line']]=[
            f'\t.{kind} {extra[0]} ; MK2KS17\n',f'\t.{kind} {extra[1]} ; MK2KS18\n']
        text=''.join(lines)
    table=source_tables(text)['ochar_fatality_distances']
    assert sum(len(row['values']) for row in table['rows'])==24
    lines=text.splitlines(keepends=True)
    lines[table['rows'][-1]['line']:table['rows'][-1]['line']]=[
        '\t.word 0,0,0,0 ; reserved boss slots12/13\n',
        '\t.word 0a0h,050h,0a0h,050h,04ah,04ah ; hidden native families14..16\n',
        '\t.word 040h,0c0h ; Kano extraction / eye laser\n',
        '\t.word 0c0h,0e0h ; Sonya flame kiss / death orb\n']
    text=''.join(lines)
    for label in ('drone_zap_jsrp','drone_reverse_zap_jump'):
        short='ks_ai_zap' if label=='drone_zap_jsrp' else 'ks_ai_zrev'
        marker='\n'+label+'\n'
        assert text.count(marker)==1,label
        text=text.replace(marker,marker+
            f'\tmove *a8(ochar),a0,w\n\tcmpi 17,a0\n\tjrne {short}_s\n'
            f'\tjauc ks_ai_kano_projectile\n{short}_s\n'
            f'\tcmpi 18,a0\n\tjrne {short}_o\n'
            f'\tjauc ks_ai_sonya_projectile\n{short}_o\n')
    names=sorted({v for values in DISPATCH_EXTENSIONS.values() for v in values if v.startswith('ks_ai_')}|{'ks_ai_kano_projectile','ks_ai_sonya_projectile'})
    text=''.join('\t.def '+name+'\n' for name in DISPATCH_TABLES)+''.join('\t.ref '+name+'\n' for name in names)+text
    return text

def integrate(text):
    for name,extra in SCALAR_EXTENSIONS.items():
        table=source_tables(text)[name]
        values=[value for row in table['rows'] for value in row['values']]
        assert len(values)==17 and all(row['type']=='word' for row in table['rows']),name
        lines=text.splitlines(keepends=True)
        at=table['rows'][-1]['line']
        lines[at:at]=['; MK2KS own-identity common AI thresholds\n',
                      f'\t.word {extra[0]} ; 17 - Kano\n',f'\t.word {extra[1]} ; 18 - Sonya\n']
        text=''.join(lines)
        result=source_tables(text)[name]
        assert [v for row in result['rows'] for v in row['values']]==values+list(extra)
    # Export names for linked-ROM verification; this adds no executable code.
    return integrate_dispatch(''.join('\t.def '+name+'\n' for name in SCALAR_EXTENSIONS)+text)

def audit(text):
    tables=source_tables(text)
    report={}
    for name in (*SCALAR_EXTENSIONS,*DISPATCH_TABLES):
        table=tables[name]
        bits=sum({'word':16,'long':32,'byte':8}[row['type']]*len(row['values']) for row in table['rows'])
        stride=32 if name=='ochar_fatality_distances' or table['rows'][0]['type']=='long' else 16
        assert bits%stride==0,name
        report[name]={'entries':bits//stride,'coversAddedIDs':bits//stride>=19,'strideBits':stride}
    return {'tables':report,'allListedTablesCoverAddedIDs':all(t['coversAddedIDs'] for t in report.values()),
            'exhaustiveSafetyAudit':False,'cpuGameplayVerified':False,'fullPortVerified':False}

def integrate_attract(text):
    # Fourteen official selectable fighters, not boss slots12/13.
    for player in (1,2):
        pattern=f'\tmovk\t12,a0\n\tcalla\trandu\n\tdec\ta0\n\tmove\ta0,@p{player}_char,w'
        assert text.count(pattern)==1,player
        replacement=(f'\tmovk\t14,a0\n\tcalla\trandu\n\tdec\ta0\n'
                     f'\tcmpi 12,a0\n\tjrlo ks_demo_p{player}_ready\n\taddk 5,a0\n'
                     f'ks_demo_p{player}_ready\n\tmove\ta0,@p{player}_char,w')
        text=text.replace(pattern,replacement)
    return text

def integrate_demo_game(text):
    # Keep the original bio fighter on P1; include new CPU opponents on P2.
    pattern='\tmovk\t12,a0\n\tcalla\trandu\n\tdec\ta0\n\tmove\ta0,@p2_char,w\t\t; random player 2'
    assert text.count(pattern)==1
    return text.replace(pattern,
        '\tmovk\t14,a0\n\tcalla\trandu\n\tdec\ta0\n'
        '\tcmpi 12,a0\n\tjrlo ks_demo_cpu_ready\n\taddk 5,a0\n'
        'ks_demo_cpu_ready\n\tmove\ta0,@p2_char,w\t\t; random official roster CPU')
