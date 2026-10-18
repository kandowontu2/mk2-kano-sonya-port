"""Recheck explicit existing current audio recordings; no emulator/compiler."""
import sys
from requalify_recorded_finishers import check

def main():
    assert len(sys.argv)==1
    for track in range(4):check('qualify_chicken_muted_control.py','--keep-track',str(track))
    pairs=[('stock_wolf_6ae0_audio_native','stock_wolf_6ae0_audio_control',['--muted-control']),
           *[(f'stock_wolf_6ae0_audio_track{track}','stock_wolf_6ae0_audio_track1_muted',[f'--single-track={track}']) for track in (1,2,3)],
           ('stock_wolf_6ae0_audio_p2_native','stock_wolf_6ae0_audio_p2_muted',['--muted-control']),
           ('stock_wolf_6ae0_audio_p2_track3','stock_wolf_6ae0_audio_p2_muted',['--single-track=3'])]
    for native,control,options in pairs:
        check('inspect_chicken_events.py',native,control,*options)
        print('EVENTS',native,flush=True)
    for track in (1,2,3):check('inspect_chicken_isolated.py',str(track))
    check('inspect_chicken_isolated.py','3','--mirror')
    check('inspect_chicken_convergence.py')
    check('inspect_chicken_convergence.py','--mirror')
    check('inspect_chicken_track_sum.py')
    print('Six paired event proofs, four isolated analyses, two convergence checks and one native track-sum diagnostic refreshed.',flush=True)

if __name__=='__main__':main()
