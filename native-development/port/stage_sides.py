"""Normalize read-only stage observations without changing controller inputs."""


def performer_first(rows, mirror):
    if not mirror:
        return rows
    def key(name):
        if name.startswith('p1'):return 'p2'+name[2:]
        if name.startswith('p2'):return 'p1'+name[2:]
        return name
    return [{key(name):value for name,value in row.items()} for row in rows]


def signed_word(value):
    value=int(value)
    assert 0<=value<=65535
    return value-65536 if value>=32768 else value


def tomb_command(actor, actor_x, victim_x):
    assert actor in (17,18)
    forward=8 if signed_word(actor_x)<signed_word(victim_x) else 7
    return [15-forward,5,5] if actor==17 else [6,forward,forward]
