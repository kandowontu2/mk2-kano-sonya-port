# Current complete dispatch wiring check

qualify_all_roster_roots.py checks the current6AE0 linked program, not only the
generated root-coverage report. The report's KSROOT source hash matches both
generated_roster_roots/KSROOT.ASM and the actually compiled srcp/KSROOT.ASM.
Both own actors have66 main slots and7 special slots with no declared gaps.

The checker follows each native get_char_ani/get_char_ani2 MOVI table immediate
from actual program bytes and verifies each own identity17/18 dispatch entry.
Every one of146 linked cells matches its ASM root symbol, has an in-ROM nonzero
target, and is not a missing-root source reference. The native DUMMY slot40h
explicitly aliases that actor's own stance, as does slot00h; this is not a proxy
fighter substitution. Some local labels are not exported in the linker map:
their table addresses are read from the real getter instruction, with the
source getter contract checked, rather than invented from guessed addresses.

ALL_ROSTER_ROOTS_QUALIFICATION.json pins current script, generated/compiled
KSROOT, coverage report, MKGUYS source, map and all four program parts, and
records all146 symbols/linked addresses. Program SHA256 remains
6AE0A069BDFCF4AB2E2F2A1E3B0B7481735AC2654E0036D9331280037BB8BAF9.

Regression tests reject missing targets, wrong cell counts, expression targets
and invalid/misaligned/out-of-image bit addresses.278 local tests pass. This
is complete dispatch-cell coverage, not complete behavior/art/indirect-caller
or audiovisual acceptance. Full-port/release flags remain false. No compiler
or emulator was launched and no production ASM/ROM/package changed.
