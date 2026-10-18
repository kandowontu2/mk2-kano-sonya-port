"""Require actual native command history, not merely an absent finisher."""
import csv


def verify_command(run, actor, kind, window, punch_used):
    path = run / 'eligibility_inputs.csv'
    matches = []
    with path.open() as stream:
        for row in csv.DictReader(stream):
            if row['frame'] not in window:
                continue
            forward = 8 if int(row['actorX']) < int(row['victimX']) else 7
            back = 15 - forward
            directions = [int(row[f'j{i}'], 16) >> 16 for i in range(4)]
            buttons = [int(row[f'b{i}'], 16) >> 16 for i in range(4)]
            expected = ([6, back, forward, back] if kind == 'friend' else
                        [6, 6, forward, forward] if actor == 17 else
                        [forward, 6, 6])
            if directions[:len(expected)] == expected and buttons[0] == (2 if kind == 'friend' else 4) and abs(int(row['actorX'])-int(row['victimX']))>=160:
                used=int(row['hpTimestamp']) > 0 or int(row['lpTimestamp']) > 0
                assert used==punch_used
                matches.append(int(row['frame']))
    assert matches, 'No native finisher command observed in the required eligibility window'
    return path, matches

def verify_punch_rejection(run, actor, kind, window):
    return verify_command(run,actor,kind,window,True)
