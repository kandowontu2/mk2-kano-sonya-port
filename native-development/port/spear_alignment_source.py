"""Own rope alignment rows; native identity and victim animations unchanged."""
from inventory_character_tables import source_tables

ALIGNMENTS=(124,124)

def integrate(text):
    table=source_tables(text)['spear_adjustments']
    assert all(row['type']=='word' for row in table['rows'])
    assert sum(len(row['values']) for row in table['rows'])==17
    lines=text.splitlines(keepends=True)
    at=table['rows'][-1]['line']
    lines[at:at]=[f'\t.word {ALIGNMENTS[0]},{ALIGNMENTS[1]} ; own Kano/Sonya rope alignment\n']
    return '\t.def spear_adjustments\n'+''.join(lines)
