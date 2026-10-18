"""Dedicated own throw entry before incompatible native ID arithmetic."""
from inventory_character_tables import source_tables

def extend_back_break_alignment(text):
    table=source_tables(text)['back_break_adjusts']
    original=[v for row in table['rows'] for v in row['values']]
    assert len(original)==34 and all(row['type']=='word' for row in table['rows'])
    lines=text.splitlines(keepends=True)
    at=table['rows'][-1]['line']
    lines[at:at]=[
        '; MK2KS explicit alignment slots: standing-size initial calibration.\n',
        '; Bent-back own art and final knee alignment remain unqualified.\n',
        '\t.word 00ah,-04bh ; 17 - Kano\n',
        '\t.word 00ah,-04bh ; 18 - Sonya\n']
    result=''.join(lines)
    assert [v for row in source_tables(result)['back_break_adjusts']['rows'] for v in row['values']]==original+['00ah','-04bh','00ah','-04bh']
    return '\t.def back_break_adjusts\n'+result

def integrate(text):
    marker='\ndo_body_slam\n'
    assert text.count(marker)==1
    text=text.replace(marker,marker+
        '\tmove *a8(ochar),a0,w\n\tcmpi 17,a0\n\tjrne ks_throw_sonya_check\n'
        '\tjauc ks_kano_throw\nks_throw_sonya_check\n'
        '\tcmpi 18,a0\n\tjrne ks_throw_original\n'
        '\tjauc ks_sonya_throw\nks_throw_original\n')
    return extend_back_break_alignment('\t.ref ks_kano_throw,ks_sonya_throw\n'+text)
