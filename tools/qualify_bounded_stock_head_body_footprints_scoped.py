"""Separate added observer tags from the unchanged qualified driver trace."""
import json
from pathlib import Path
import qualify_bounded_stock_head_body_footprints as original

sync=original.sync
raw_states=original.states

def driver_states(folder,fighter):
    rows=raw_states(folder,fighter)
    return [(tag,row) for tag,row in rows if not tag.startswith('IDLE_')
            and tag not in ('COMPLETE_FOOTPRINT','CONTACT_HEALTH','CONTACT_THROW')]

def main():
    # The failed predecessor is preserved. Reuse its unchanged pixel/state gates.
    original.states=driver_states
    original.main()
    path=sync.ROOT/'audit_bounded_stock_head_body_footprints_checked/report.json'
    report=json.loads(path.read_text())
    report['scopedCheckerSha256']=sync.sha(Path(__file__))
    report['observerTagsExcludedFromDriverComparison']=True
    path.write_text(json.dumps(report,indent=2)+'\n')

if __name__=='__main__':main()
