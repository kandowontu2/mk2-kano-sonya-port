"""Own-ID victim pose/lineup for Raiden's native close shock."""
from inventory_character_tables import source_tables

# High byte: main animation 23; next byte: frame zero. Signed low bytes:
# x=-64, y=-32 relative to Raiden. Victim is posed once; shock_shake
# advances Raiden's restored animation pointer, not the victim's sequence.
ENTRIES=(0x2300c0e0,0x2300c0e0)

def integrate(text):
    table=source_tables(text)['shocker_info']
    assert all(row['type']=='long' for row in table['rows'])
    assert sum(len(row['values']) for row in table['rows'])==17
    lines=text.splitlines(keepends=True)
    lines[table['rows'][-1]['line']:table['rows'][-1]['line']]=[
        '\t.long 02300c0e0H,02300c0e0H ; own Kano/Sonya shock pose and lineup\n']
    return '\t.def shocker_info\n'+''.join(lines)
