"""Extend native Pit scene tables with explicit own victim data."""
from inventory_character_tables import source_tables

def integrate(text):
    for label,row in [
        ('ochar_fall_coor','0,0,0004000c0h,0004000c0h,0003600c0h,0004000c0h,0004000c0h'),
        ('ochar_pit_falls','0,0,a_nj_fall,a_nj_fall,a_fn_fall,ks_pit_kano_sequence,ks_pit_sonya_sequence')]:
        table=source_tables(text)[label]
        assert sum(len(r['values']) for r in table['rows'])==12
        assert all(r['type']=='long' for r in table['rows'])
        lines=text.splitlines(keepends=True)
        lines[table['rows'][-1]['line']:table['rows'][-1]['line']]=['; MK2KS explicit nineteen-row native Pit table.\n','\t.long '+row+'\n']
        text=''.join(lines)
    return '\t.ref ks_pit_kano_sequence,ks_pit_sonya_sequence\n'+text
