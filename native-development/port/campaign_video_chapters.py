"""Native-trace chapter plan; it does not establish a campaign victory."""


def chapter_plan(rows, clock, names, winning_attempts, ending_frame):
    start = clock['firstGuestFrame']; limit = start + clock['frames']
    assert start <= ending_frame < limit
    first = {}; winners = {}
    for row in rows:
        frame = int(row['frame'])
        if row['mode'] != '2' or not start <= frame < limit:
            continue
        position = int(row['map']); opponent = int(row['p2selected'])
        if opponent not in names:
            continue
        first.setdefault(position, (frame, opponent))
        if winning_attempts.get(position) == int(row['attempt']):
            winners.setdefault(position, (frame, opponent))
    assert first, 'No recorded native matchup'
    events = [(start, 'CHARACTER SELECT', 'selection', None)]
    for position, (frame, opponent) in first.items():
        events.append((frame, names[opponent], 'matchup', position))
        if position in winners and winners[position][0] != frame:
            win_frame, win_opponent = winners[position]
            assert win_opponent == opponent, 'Matchup identity changed across attempts'
            events.append((win_frame, names[opponent] + ' - CLEAR ATTEMPT', 'winning_attempt', position))
    events.append((ending_frame, 'ENDING', 'ending', None))
    # One event per native field prevents zero-length chapters at boundaries.
    unique = {event[0]: event for event in events}
    ordered = sorted(unique.values())
    duration = round(clock['frames'] / clock['rate'] * 1000)
    result = []
    for index, (frame, title, kind, position) in enumerate(ordered):
        begin = round((frame - start) / clock['rate'] * 1000)
        end = (round((ordered[index+1][0] - start) / clock['rate'] * 1000)
               if index+1 < len(ordered) else duration)
        assert 0 <= begin < end <= duration
        result.append(dict(title=title, startMilliseconds=begin, endMilliseconds=end,
                           nativeFrame=frame, kind=kind, map=position))
    return result


def metadata(chapters):
    lines = [';FFMETADATA1']
    for chapter in chapters:
        assert not any(c in chapter['title'] for c in '\n\r\\;=#')
        lines += ['[CHAPTER]', 'TIMEBASE=1/1000',
                  'START=' + str(chapter['startMilliseconds']),
                  'END=' + str(chapter['endMilliseconds']), 'title=' + chapter['title']]
    return '\n'.join(lines) + '\n'
