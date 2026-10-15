"""Authored stock-body waist pivots for Sonya's native leg-grab adaptation.

Points are in unflipped original composite coordinates relative to object
origin, measured on the gridded ROM-pose audit. They are adaptation data, not
claims about offsets present in the original MKII program. Runtime mirrors X
through the victim's native facing flag; neither body art nor IDs are altered.
"""

POINTS = {
    "kano": [(0, 65), (1, 65), (0, 57), (4, 74), (1, 92)],
    "kung_lao": [(1, 69), (0, 77), (4, 27), (12, 14), (7, 59)],
    "liu_kang": [(-1, 64), (-3, 66), (-9, 26), (12, 42), (9, 80)],
    "cage": [(0, 73), (-8, 57), (-6, 27), (7, 37), (3, 91)],
    "baraka": [(1, 75), (-8, 47), (0, 38), (-8, 45), (-5, 76)],
    "kitana": [(2, 68), (1, 65), (9, 39), (4, 40), (5, 61)],
    "shang_tsung": [(5, 65), (1, 72), (0, 42), (5, 69), (2, 79)],
    "raiden": [(6, 73), (-1, 74), (-8, 54), (3, 51), (-6, 62)],
    "sub_zero": [(-2, 78), (-5, 67), (-2, 39), (-4, 60), (-6, 76)],
    "jax": [(1, 77), (-4, 76), (-6, 62), (8, 54), (5, 67)],
}
ALIASES = {"mileena": "kitana", "jade": "kitana", "reptile": "sub_zero",
           "scorpion": "sub_zero", "smoke": "sub_zero", "noob": "sub_zero"}
ORIGINAL_KANO_OFFSETS = [(85, 0), (68, -41), (10, -80), (-56, -55), (-100, 0)]


def contact_points(name):
    return POINTS[ALIASES.get(name, name)]


def flip_indices(fighter_id):
    # Female ninjas and Shang have an extra near-upright lean. The third
    # paired phase must use their forward bend, not that preparation pose.
    return (0, 2, 3, -1) if fighter_id in (4, 5, 6, 16) else (0, 1, 2, -1)


def adapted_offsets(name):
    """Place each victim waist at the original Kano choreography pivot."""
    return [(dx - rx + x, dy + ry - y) for (dx, dy), (rx, ry), (x, y) in
            zip(ORIGINAL_KANO_OFFSETS, POINTS["kano"], contact_points(name), strict=True)]


if __name__ == "__main__":
    for name in POINTS:
        print(name, adapted_offsets(name))
