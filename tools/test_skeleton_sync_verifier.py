import unittest

from verify_skeleton_sync import ARMS, BONES, verify


def trace(side=1, pauses=None, arms=ARMS, owner_id=17):
    lines = []
    frame = 100
    for index, (bone, arm) in enumerate(zip(BONES, arms)):
        if index:
            frame += pauses[index - 1] if pauses else 8
        own = f"01034E90:{owner_id:04X}:{arm:08X}:0000:500:82:01050000:0001"
        other = "010350A0:0004:FF9520E0:0000:560:82:01050100:0002"
        actors = (own, other) if side == 1 else (other, own)
        lines.append(f"MK2_FINISH_ACTORS frame={frame} age=0 mode=3 p1={actors[0]} p2={actors[1]}")
        lines.append(f"MK2_FINISH_SKELETON frame={frame} age=0 pose={bone:08X}")
    return "\n".join(lines)


class SkeletonSyncVerifierTests(unittest.TestCase):
    def test_both_player_sides(self):
        for side in (1, 2):
            self.assertTrue(verify(trace(side), side)["passed"])

    def test_serialized_old_pull_is_rejected(self):
        old_arms = (ARMS[0],) + (ARMS[-1],) * 5
        self.assertFalse(verify(trace(pauses=(40, 8, 8, 8, 8), arms=old_arms), 1)["passed"])

    def test_wrong_owner_identity_is_rejected(self):
        self.assertFalse(verify(trace(owner_id=1), 1)["passed"])

    def test_wrong_side_is_rejected(self):
        self.assertFalse(verify(trace(side=2), 1)["passed"])

    def test_missing_phase_is_rejected(self):
        self.assertFalse(verify("\n".join(trace().splitlines()[:-2]), 1)["passed"])

    def test_empty_log_is_rejected(self):
        self.assertFalse(verify("", 1)["passed"])


if __name__ == "__main__":
    unittest.main()
