"""Keep every owned death byte strict; exclude separately owned split artwork.

5476 read-only comparison proves all40 header bytes,560 descriptor bytes and
51056 corrected pixels exact. Differences begin172000, where compiled current
split-art code owns another allocation. Do not require that legitimate art to
remain erased as it was in the old1002 payload. No gameplay tolerance changes.
"""
import json
from pathlib import Path
import current_reptile_victims_ram_v5467 as canonical5467

failed=canonical5467.ROOT/'audit_v5475_current_reptile_victims_progress/progress.json'
status=json.loads(failed.read_text())
canonical5467.need(not status['passed']and status['error']=="ValueError('Entire current native-death allocation exactly equals original source-PNG art plus qualified original1014 head-order/diagonals')"and
                  not status['completedCases'],'Preserved old erased-space reference failure, no native boots')
base=Path(__file__).with_name('current_reptile_victims_ram_v5473.py')
source=base.read_text()
before="source=source.replace('original.','canonical5467.')"
after=before+'''
wide="need(payload[0x160000:0x180000]==expected[0x160000:0x180000],\\n         'Entire current native-death allocation exactly equals original source-PNG art plus qualified original1014 head-order/diagonals')"
owned="count=struct.unpack_from('<I',expected,0x160008)[0]\\n    need(payload[0x160000:0x160028]==expected[0x160000:0x160028]and payload[0x160400:0x160630]==expected[0x160400:0x160630]and payload[0x164000:0x164000+count]==expected[0x164000:0x164000+count], 'Every owned current death header/descriptor/pixel exactly equals original900 and1014 source-PNG encoding')"
canonical5467.need(source.count(wide)==1,'Exact whole owned-death versus unrelated split-allocation boundary')
source=source.replace(wide,owned)
'''
canonical5467.need(source.count(before)==1,'One original canonical-binding adaptation boundary')
source=source.replace(before,after)
changes={
 'audit_v5474_current_reptile_victims_ram':'audit_v5478_current_reptile_victims_ram',
 'audit_v5475_current_reptile_victims_progress':'audit_v5479_current_reptile_victims_progress',
 "ROOT/'audit_v5472_current_reptile_victims_progress/progress.json')":
 "ROOT/'audit_v5472_current_reptile_victims_progress/progress.json',ROOT/'tools/current_reptile_victims_ram_v5473.py',ROOT/'audit_v5475_current_reptile_victims_progress/progress.json',ROOT/'tools/inspect_current_head_source_spans_v5476.py')",
}
for before,after in changes.items():
    canonical5467.need(source.count(before)==1,'Exact fresh owned-allocation scope adaptation: '+before)
    source=source.replace(before,after)
exec(compile(source,__file__+'.whole5473_exact_owned_death_spans_not_neighboring_split_art','exec'),globals())
