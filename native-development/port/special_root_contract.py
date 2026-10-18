"""Own actor-specific anitab2 ABI. These are not Liu Kang's slot meanings.

Native get_char_ani2 selects by A8.ochar and returns a script in A9. Each caller
below keeps the exact existing script and consumer; only pointer lookup changes.
Projectile slot6 is used with the projectile's inherited true thrower character.
"""
ROLES = ('travelling_special', 'strike_special', 'grab_special', 'fatality_one',
         'fatality_two', 'friendship_intro', 'projectile_impact')
ROOTS = {
    'kano': ('ks_ball_animation', 'ks_blade_animation', 'ks_choke_intro',
             'ks_extract_intro', 'ks_laser_phase0', 'ks_friend_kano_body', 'ks_knife_impact'),
    'sonya': ('ks_square_animation', 'ks_bike_intro', 'ks_leg_intro',
              'ks_finish_sonya_kiss', 'ks_finish_sonya_kiss', 'ks_friend_sonya_intro', 'ks_ring_impact'),
}
CALLERS = {
    'kano': ('KANOMOV.ASM', 'KSBLADE.ASM', 'KSCHOKE.ASM', 'KSFATAL.ASM',
             'KSLASER.ASM', 'KSFRIEND.ASM', 'KSPROJ.ASM'),
    'sonya': ('SONYAMOV.ASM', 'KSBIKE.ASM', 'KSLEG.ASM', 'KSKISS.ASM',
              'KSBUBBLE.ASM', 'KSFRIEND.ASM', 'KSPROJ.ASM'),
}
