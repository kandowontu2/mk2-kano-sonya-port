# Campaign opponent-name correction

Authoritative MAINEQU.ASM constants and the actual captured fight frame agree:
native ID 5 is MILEENA; native ID 7 is RAIDEN. Earlier notes repeatedly called
ID 7 "Mileena". That was a reporting/controller-classification error, not a
character-identity substitution in the ROM. The screenshot
baseline/stock_wolf_game545/snap/campaign_13884_mode2.png visibly shows RAIDEN.

Correct identities of the previously reported stopping points: Kano reached
KITANA (ID 4, map 4), Sonya reached RAIDEN (ID 7, map 3). Earlier Kano "Mileena wins" at map 3 are
Raiden wins. No actual Mileena match can be inferred from those receipts.
Historical raw traces, controller snapshots and audit receipts are retained.
Their numeric IDs remain evidence; incorrect prose names do not.

native_roster.py now verifies all original IDs against MAINEQU.ASM and adds the
own IDs 17/18. New campaign audits attach source-checked opponent names and
roster-source hashes rather than guessing from the selection layout. Tests
explicitly distinguish 5/Mileena from 7/Raiden.

The previously named --campaign-mileena-knife policy actually targets ID 7.
Its behavior is preserved under the correctly named --campaign-raiden-knife;
the old CLI spelling remains a documented compatibility alias, not a new
Mileena policy. Kitana/Mileena zoning/counter/guard conditions now use IDs 4/5,
not 4/7. Sonya tests that applied those policies at map 3 were testing Raiden
with a wrongly classified controller strategy. Those results do not qualify
a strategy against Mileena and should not be repeated under the old claim.

These corrections do not change the game ROM, its native IDs, difficulty or AI.
Full campaigns, later CPU/boss coverage and earned ending/credits runtime remain
unfinished. The actor-name correction does not convert losses into wins.

Fresh run549 on the cast-enabled program does not reach Raiden: Sonya clears
Baraka/Reptile and loses Jax through three paid continues (24,264 fields).
The new Raiden-specific Ring/guard/dive-recovery Leg policy is therefore
unexercised, not a tested failure or success against Raiden. The current audit
records actual names alongside IDs and passes all26-ROM/identity/no-fault checks.

Current run551's distinct Jax-safe spacing policy now clears Jax2–0 at135/93
health and reaches Raiden/map3. The Raiden policy is exercised here and fails
across three paid continues; see JAX_DAMAGE_AND_SPACING_CURRENT.md. This is
the current-link Raiden stopping point, not an inherited earlier-link claim.
