# Current sampled floor-shadow regression

The old bank-shadow verifier required historical158/159 names in the frozen
report, so it could not qualify after that report was refreshed to current6AE0.
It now checks all current frozen-prerequisite pins and follows its explicit
Kano/Sonya victim-player2 cases. Both current runtime archives are independently
verified against all26 actual ROM bytes and their frozen-controller receipts.

The historical pre-fix/fixed image pairs remain historical delta baselines,
not current runtime evidence. Their differences are required to stay within
the bounded floor-shadow region (X230..339,Y190..232), with no above-floor
changes. Current freeze160/320 captures match every corrected pixel in those
delta masks:704+620 Kano pixels and630+553 Sonya pixels, total2507. Attacker/
victim identities and X coordinates match the historical fixed snapshots at
each sampled field. Current captures and historical baselines, traces, source
and receipts are all pinned in SHADOW_BANK_QUALIFICATION.json.

The original36 bank-translation/control-bit model cases and native source
bank-read/restore contract checks remain. The report explicitly labels its
historical baseline and current four-capture regression. This is finite
current shadow-fix pixel evidence, not every animation, side, arena or hardware
control transition. Full-port/release acceptance remains false.

Two new tests reject a changed current fix pixel, an empty delta and an
above-floor delta. All287 local tests pass. No emulator/compiler was launched
for this check, and the production ROM/package is unchanged.
