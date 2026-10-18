"""Extend native frozen/lightning palette lookup for true IDs17/18."""
from inventory_character_tables import source_tables

def integrate(text):
    table=source_tables(text)['ochar_froze_pals']
    assert all(row['type']=='long' for row in table['rows'])
    assert sum(len(row['values']) for row in table['rows'])==17
    lines=text.splitlines(keepends=True)
    at=table['rows'][-1]['line']
    lines[at:at]=['\t.long ks_kano_frozen_palette,ks_sonya_frozen_palette\n']
    return '\t.ref ks_kano_frozen_palette,ks_sonya_frozen_palette\n'+''.join(lines)
