"""Finite fresh-match identity/state/palette checks after original fatalities."""
import csv

def verify(rows,events,palettes,performer_side,performer,victim):
    assert performer_side in (1,2)
    starts=[int(row['frame']) for row in events if row['phase']=='combat']
    selections=[int(row['frame']) for row in events if row['phase']=='selection']
    assert len(starts)==len(selections)==1 and selections[0]<starts[0]
    expected=list(range(starts[0],starts[0]+600))
    fresh=[row for row in rows if int(row['frame'])>=starts[0]]
    assert [int(row['frame']) for row in fresh]==expected
    owner=f'p{performer_side}';other=f'p{3-performer_side}'
    assert all(row['mode']=='2' and row['death']==row['winner']==row['missing']=='0' and
               row[owner+'char']==str(performer) and row[other+'char']==str(victim) for row in fresh)
    assert fresh[0]['p1hp']==fresh[0]['p2hp']=='161'
    assert any(int(row[other+'hp'])<161 for row in fresh)
    assert [int(row['frame']) for row in palettes]==expected
    colors=0
    for row in palettes:
        for side in (1,2):
            assert row[f'p{side}source']==row[f'initialP{side}source']
            assert row[f'p{side}rgbMismatch']=='0'
            count=int(row[f'p{side}colors']);assert 1<=count<=256
            colors+=count
    return dict(freshCombatFields=600,freshHardwarePaletteColorComparisons=colors,
                freshMatchFrame=starts[0],freshIdentitiesAndResetVerified=True)

def verify_folder(folder,rows,performer_side,performer,victim):
    with (folder/'finisher_rejoin_events.csv').open() as stream:events=list(csv.DictReader(stream))
    with (folder/'finisher_cleanup.csv').open() as stream:palettes=list(csv.DictReader(stream))
    return verify(rows,events,palettes,performer_side,performer,victim)
