"""Read MKII-owned knockback and final-prone groups for each stock fighter."""
from pathlib import Path
import re

import build_mk2ks_mk3 as animation


NAMES = (
    "kung_lao", "liu_kang", "cage", "baraka", "kitana", "mileena",
    "shang_tsung", "raiden", "sub_zero", "reptile", "scorpion", "jax",
)


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    original = (root / "mk2/mk2-maincpu.bin").read_bytes()
    main = [animation.u32(original, animation.MK2_MAIN_TABLE + i * 4)
            for i in range(17)]
    special = [animation.u32(original, animation.MK2_SPECIAL_TABLE + i * 4)
               for i in range(17)]
    for fighter, name in enumerate(NAMES):
        start = main[fighter]
        end = min((address for address in main if address > start),
                  default=0xffe00000)
        spans = animation.sequence_spans(original, start, (start, end),
                                         (start, special[fighter]))

        def groups(row: int) -> list[int]:
            return [address for _, address, _ in animation.group_references(
                original, *spans[row], start, end)] if row in spans else []

        death, knockback = groups(15), groups(18)
        if len(death) < 7 or len(knockback) < 3:
            raise ValueError(f"missing stock reaction groups: {name}")
        trace = (root / f"diagnostic_v151_stock_prone_{name}/run.log").read_text()
        held = re.search(r"MK2_STOCK_VICTIM_HELD[^\n]*health=0 pose=([0-9A-F]{8})", trace)
        if held is None:
            raise ValueError(f"missing held-prone runtime evidence: {name}")
        terminal = int(held.group(1), 16)
        if terminal not in death:
            raise ValueError(f"held pose not in death row: {name} {terminal:08X}")
        final_index = death.index(terminal)
        if final_index < 2:
            raise ValueError(f"death row too short before held pose: {name}")
        proposed = (*knockback[:3], *death[final_index - 2:final_index + 1])
        print(f"{fighter:02d} {name:12s} death={len(death):02d} "
              f"knockback={len(knockback):02d} "
              f"proposed={','.join(f'{group:08X}' for group in proposed)}")


if __name__ == "__main__":
    main()
