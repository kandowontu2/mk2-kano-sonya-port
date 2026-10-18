"""Physical attack selection from the native six-hit queue, never a queue write."""
def next_move(history):
    assert len(history)==6
    if history.count(0x200)<2:return 'mixkick'
    if history.count(0x201)<2:return 'mixpunch'
    return 'readyknife'


def air_attack_age(distance):
    assert distance>=0
    return max(10,min(28,(distance-80)//4))
