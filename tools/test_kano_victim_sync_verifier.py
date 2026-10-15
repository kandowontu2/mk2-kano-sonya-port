import unittest
from pathlib import Path

import build_mk2ks_mk3 as b

from verify_kano_victim_sync import OFFSETS, PAIRED_ARMS, VICTIMS, verify
from verify_skeleton_sync import ARMS, BONES


def trace(victim="sonya", side=1, offsets=OFFSETS, wrong_id=False):
    identity, groups = VICTIMS[victim]
    events = {}
    for group, offset, arm in zip(groups, offsets, PAIRED_ARMS):
        events[100 + offset] = [arm, group]
    for index, arm in enumerate(ARMS):
        when = 100 + index * 8
        previous = max(key for key in events if key <= when)
        events.setdefault(when, [arm, events[previous][1]])
    lines = []
    for when, (arm, group) in sorted(events.items()):
        own = f"01034E90:0011:{arm:08X}:0000:500:82:01050000:0001"
        other = f"010350A0:{(1 if wrong_id else identity):04X}:{group:08X}:0000:560:82:01050100:0002"
        actors = (own, other) if side == 1 else (other, own)
        lines.append(f"MK2_FINISH_ACTORS frame={when} age=0 mode=3 p1={actors[0]} p2={actors[1]}")
        if 100 <= when <= 140 and (when - 100) % 8 == 0:
            lines.append(f"MK2_FINISH_SKELETON frame={when} age=0 pose={BONES[(when-100)//8]:08X}")
    return "\n".join(lines)


class KanoVictimSyncVerifierTests(unittest.TestCase):
    def test_stock_bodies_match_original_rom_not_candidate(self):
        program=(Path(__file__).resolve().parent.parent/"mk2/mk2-maincpu.bin").read_bytes()
        roots=[b.u32(program,b.MK2_MAIN_TABLE+i*4) for i in range(17)]
        for victim,(identity,groups) in VICTIMS.items():
            if identity>=12:
                continue
            root=roots[identity]
            end=min(value for value in set(roots)|{0xff9a0000} if value>root)
            special=b.u32(program,b.MK2_SPECIAL_TABLE+identity*4)
            spans=b.sequence_spans(program,root,(root,end),(root,special))
            headed=list(dict((ptr,frames) for _,ptr,frames in
                             b.group_references(program,*spans[55],root,end)))
            headless=list(dict((ptr,frames) for _,ptr,frames in
                               b.group_references(program,*spans[60],root,end)))
            with self.subTest(victim=victim):
                self.assertEqual(groups,(headed[2],*(headless[index] for index in (0,1,3,5,6))))

    def test_previous_headed_subzero_fall_is_rejected(self):
        previous=(0xFF97BFD0,0xFF97C030,0xFF97C070,0xFF97BA10,0xFF97BA70,0xFF97BAD0)
        for victim in ("sub_zero","reptile","scorpion"):
            for side in (1,2):
                log=trace(victim,side)
                for current,old in zip(VICTIMS[victim][1],previous):
                    log=log.replace(f"{current:08X}",f"{old:08X}")
                self.assertFalse(verify(log,side,victim)["passed"])

    def test_jax_requires_native_fatality_body(self):
        expected=(0xFF991950,0xFF997980,0xFF9979E0,0xFF997AA0,0xFF997B60,0xFF997BE0)
        self.assertEqual(VICTIMS["jax"],(11,expected))
        rejected=(0xFE9B3110,0xFE9B3190,0xFE9B3210,0xFE9B3290,0xFE9B32F0,0xFE9B3330)
        for side in (1,2):
            log=trace("jax",side)
            for native,donor in zip(expected,rejected):
                log=log.replace(f"{native:08X}",f"{donor:08X}")
            self.assertFalse(verify(log,side,"jax")["passed"])

    def test_native_mk2_identity_mapping(self):
        names=("kung_lao", "liu_kang", "cage", "baraka", "kitana", "mileena",
               "shang_tsung", "raiden", "sub_zero", "reptile", "scorpion", "jax")
        expected=dict(zip(names, range(12))) | {"kano": 17, "sonya": 18}
        self.assertEqual({name: value[0] for name, value in VICTIMS.items()}, expected)

    def test_all_selectable_victims_both_sides(self):
        for victim in VICTIMS:
            for side in (1, 2):
                with self.subTest(victim=victim, side=side):
                    self.assertTrue(verify(trace(victim, side), side, victim)["passed"])

    def test_previous_serial_sequence_fails(self):
        self.assertFalse(verify(trace(offsets=(-4, 48, 56, 64, 72, 80)), 1, "sonya")["passed"])

    def test_early_windup_cannot_be_hidden_by_a_repeat(self):
        lines=trace(offsets=(-60, 0, 8, 76, 84, 92)).splitlines()
        repeated=lines[0].replace("frame=40", "frame=41")
        lines.insert(1, repeated)
        self.assertFalse(verify("\n".join(lines), 1, "sonya")["passed"])

    def test_wrong_victim_identity_fails(self):
        self.assertFalse(verify(trace(wrong_id=True), 1, "sonya")["passed"])

    def test_wrong_side_fails(self):
        self.assertFalse(verify(trace(side=2), 1, "sonya")["passed"])

    def test_missing_final_phase_fails(self):
        self.assertFalse(verify("\n".join(trace().splitlines()[:-1]), 1, "sonya")["passed"])

    def test_wrong_victim_art_fails(self):
        self.assertFalse(verify(trace("kano"), 1, "sonya")["passed"])

    def test_empty_log_fails(self):
        self.assertFalse(verify("", 1, "sonya")["passed"])


if __name__ == "__main__":
    unittest.main()
