"""Read-only exact source anchors; no emulator or game state involved."""
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1]
if __name__=='__main__':
    text=(ROOT/'mk2ks_native_kano_p2_postending_sonya.lua').read_text()
    helper=text.split('local helper=[[\n',1)[1].split('\n]]\none(',1)[0]
    anchors=['sample(2),sample(1)','slot=2 target=18','if row[1]==18 then',
             'human.id==18 and human.roster==18',' id=18','identity=18 input=']
    base=(ROOT/'mk2ks_sonya_extended_guard_base_ram_v5201.lua').read_text()
    print(json.dumps(dict(helperCounts={a:helper.count(a) for a in anchors},
        baseCounts={a:base.count(a) for a in ("local source=file:read('a');file:close()",
                                             "local source=file:read('*a');file:close()")}),indent=2))
