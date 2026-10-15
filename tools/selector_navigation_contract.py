"""Selection expectations derived from the requested fourteen-cell layout.

This contract never reads the driver's maps to choose the expected destination.
The two overhanging top-row cells descend to the nearest stock column.
"""
from collections import deque

ROWS = ((17, 1, 0, 2, 9, 18), (8, 6, 4, 11), (5, 3, 10, 7))
DIRECTIONS = ('up', 'down', 'left', 'right')
CELLS = tuple(n for row in ROWS for n in row)
XY = {n: (23 + 60 * col, 24 + 75 * row)
      for row, ids in enumerate(ROWS)
      for col, n in enumerate(ids, 0 if row == 0 else 1)}


def target(origin, direction):
    row, col = next((r, ids.index(origin)) for r, ids in enumerate(ROWS) if origin in ids)
    if direction in ('left', 'right'):
        destination = max(0, min(len(ROWS[row]) - 1, col + (-1 if direction == 'left' else 1)))
        return ROWS[row][destination]
    if direction == 'up':
        return origin if row == 0 else ROWS[row - 1][col + (1 if row == 1 else 0)]
    if direction == 'down':
        return origin if row == 2 else ROWS[row + 1][max(0, min(3, col - 1)) if row == 0 else col]
    raise ValueError(direction)


def shortest(origin, destination):
    queue = deque([(origin, [])]); seen = {origin}
    while queue:
        cell, path = queue.popleft()
        if cell == destination:
            return path
        for direction in DIRECTIONS:
            other = target(cell, direction)
            if other not in seen:
                seen.add(other); queue.append((other, path + [direction]))
    raise ValueError('Disconnected required selection layout')


def plan(start, direction):
    remaining = set(CELLS); current = start; steps = []
    while remaining:
        origin = min(remaining, key=lambda cell: (len(shortest(current, cell)), CELLS.index(cell)))
        for move in shortest(current, origin):
            other = target(current, move)
            steps.append(dict(origin=current, direction=move, destination=other, test=False))
            current = other
        other = target(current, direction)
        steps.append(dict(origin=current, direction=direction, destination=other, test=True))
        current = other; remaining.remove(origin)
    # Every case finishes on a true own fighter and confirms through native input.
    finish = 17 if start == 1 else 18
    for move in shortest(current, finish):
        other = target(current, move)
        steps.append(dict(origin=current, direction=move, destination=other, test=False))
        current = other
    assert current == finish
    assert {s['origin'] for s in steps if s['test']} == set(CELLS)
    assert all(s['destination'] == target(s['origin'], s['direction']) for s in steps)
    return steps


def lua_plan(steps):
    return 'return {' + ','.join('{%d,"%s",%d,%s}' % (
        s['origin'], s['direction'], s['destination'], str(s['test']).lower()) for s in steps) + '}'


if __name__ == '__main__':
    import json
    print(json.dumps({direction: {str(slot): dict(steps=len(plan(start, direction)),
        lastCheckAge=65 + (len(plan(start, direction)) - 1) * 12 + 10)
        for slot, start in ((1, 1), (2, 9))} for direction in DIRECTIONS}, indent=2))
