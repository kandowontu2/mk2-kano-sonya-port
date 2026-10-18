"""Readonly campaign round segmentation using native counters, not HP heuristics."""

def require_clean_runtime_log(log):
    """Checksum warnings are expected for patches; Lua/fatal failures are not."""
    assert '[LUA ERROR]' not in log, 'Lua runtime failure'
    assert 'fatal error:' not in log.lower(), 'Fatal emulator failure'

def sampled_action_tag_episodes(fight):
    """Observed tag runs only; interruptions can leave stale native tags."""
    counts={};previous=None
    for row in fight:
        context=(row.get('attempt','0'),row['map'],row['round'],row['p2char'])
        action=f"{int(row['p1action']):04x}"
        key=(context,action)
        if key!=previous:
            bucket=counts.setdefault(int(row['p2char']),{})
            bucket[action]=bucket.get(action,0)+1
        previous=key
    return counts

def split_rounds(fight):
    rounds=[];previous=None
    for row in fight:
        key=(row.get('attempt','0'),row['map'],row['round'])
        if previous is None or key!=previous:
            rounds.append(dict(firstFrame=int(row['frame']),opponent=int(row['p2char']),
                map=int(row['map']),nativeRound=int(row['round']),attempt=int(row.get('attempt','0')),
                minimumPlayerHP=int(row['p1hp']),minimumCPUHP=int(row['p2hp'])))
        rounds[-1]['minimumPlayerHP']=min(rounds[-1]['minimumPlayerHP'],int(row['p1hp']))
        rounds[-1]['minimumCPUHP']=min(rounds[-1]['minimumCPUHP'],int(row['p2hp']))
        previous=key
    return rounds


def native_round_wins(rows, rounds):
    """One native winning result per attempt/map/round, never HP minima alone."""
    wins={}
    for data in rounds:
        key=(data['attempt'],data['map'],data['nativeRound'])
        result=[row for row in rows if int(row['map'])==data['map']
                and int(row['round'])==data['nativeRound']
                and int(row.get('attempt','0'))==data['attempt']
                and int(row['frame'])>=data['firstFrame']
                and row['mode']=='5' and row['winner']=='1'
                and int(row['p1hp'])>0 and row['p2hp']=='0'
                and 0<int(row['p1match'])<=2 and 0<=int(row['p2match'])<=1]
        if result:
            row=result[-1]
            wins[key]=dict(map=data['map'],opponent=data['opponent'],
                nativeRound=data['nativeRound'],attempt=data['attempt'],
                resultFrame=int(row['frame']),playerRoundWins=int(row['p1match']),
                cpuRoundWins=int(row['p2match']))
    return sorted(wins.values(),key=lambda row:row['resultFrame'])


def completed_native_matches(wins):
    """Require counter1 then counter2 on distinct rounds of the SAME attempt."""
    groups={}
    for row in wins:groups.setdefault((row['map'],row['attempt']),[]).append(row)
    completed=[]
    for (position,attempt),rounds in groups.items():
        ordered=sorted(rounds,key=lambda row:row['resultFrame'])
        if ([row['playerRoundWins'] for row in ordered]==[1,2]
                and len({row['nativeRound'] for row in ordered})==2
                and len({row['opponent'] for row in ordered})==1):
            completed.append(dict(map=position,attempt=attempt,
                opponent=ordered[0]['opponent'],nativeResults=ordered))
    return completed
