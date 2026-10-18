"""Own knockdown pose and relative hand lineup for Raiden's flying tackle."""
from inventory_character_tables import source_tables

POSES=(0,0)
ADJUSTMENTS=((-72,0),(-72,0))

def integrate(text):
    tables=source_tables(text);lines=text.splitlines(keepends=True)
    insertions=[]
    for name,count,row in (
        ('ochar_dived_poses',17,'\t.word 0,0 ; own Kano/Sonya knockdown frame\n'),
        ('ochar_dived_adjust',34,'\t.word -048H,000H,-048H,000H ; own Kano/Sonya hand lineup\n')):
        table=tables[name]
        assert all(entry['type']=='word' for entry in table['rows'])
        assert sum(len(entry['values']) for entry in table['rows'])==count
        insertions.append((table['rows'][-1]['line'],row))
    for at,row in sorted(insertions,reverse=True):lines[at:at]=[row]
    return '\t.def ochar_dived_poses,ochar_dived_adjust\n'+''.join(lines)
