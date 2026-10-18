"""Read-only selected-Shang/active-own identity evidence for finite finishers."""
import csv

def verify(run,running,actor):
    assert running
    rows=list(csv.DictReader((run/'morph_finish.csv').open()))
    index={r['frame']:r for r in rows}
    assert len(index)==len(rows)
    assert all(index[r['frame']]['selected']=='6' and index[r['frame']]['actual']==str(actor) for r in running)
    first=int(running[0]['frame'])
    assert any(r['selected']==r['actual']=='6' and r['winner']=='3' and int(r['frame'])<first for r in rows)
    return dict(selectedCharacter=6,activeFinisherCharacter=actor,transformedFinisher=True)
