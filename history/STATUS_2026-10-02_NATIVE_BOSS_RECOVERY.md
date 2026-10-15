# Native boss recovery checkpoint — not a cleared tower

The playable candidate is still `diagnostic_v680_native_pit_initial_cache`.
No gameplay source, executable, payload, production CMD or release ZIP changed.

Six v710 diagnostics genuinely select Liu Kang, Kano or Sonya in each physical
player slot. One explicitly declared stage-index fixture is applied after the
selection locks, before the CPU actor is constructed. This is NOT an unassisted
campaign. Neither health nor actor, identity, action, position or schedule is
written. Both native actors are constructed at full health and true IDs.

The independent verifier checks every consecutive same-episode victim/boss
field from the actual first native 56-damage stomp through initial Right
movement. The victim's native saved continuation is FF8392B0, waited action
0407, and waited Main is the actual Kintaro Main. Boss action clears at age 149
in both slots. The victim returns through original FF861350 at age 149 in P1
and 150 in P2, then the original player controller FF82F270/FF830D00. Physical
Right input produces position and pose movement two fields after that return.
All three characters have the same per-slot native recovery timing. The actual
guest wait/return/control instruction ranges match the original ROM.

The retained observer's legacy `attacker` label is misleading: it records A8,
which is the VICTIM in this native Kintaro coroutine. `attacker_main` is the
actual execution boss Main. The verifier checks that distinction explicitly.
Later samples can include KO/another round; only the continuous first episode
is accepted. The captured log's inherited generic RESULT scope does not override
the explicit stage-fixture prefix, runner and BOSS_RESULT scope.

Twenty-five baseline/corruption tests pass. Representative screenshots show
both new characters resuming their walk. The brief initial display delay is
also visible in the stock Liu Kang comparison, not proof of a port-only freeze.
This is not a full DMA/display, every-boss, choreography or audio certification.

Earlier v708 runs never reached the boss. V709 reached it but used a wrong A8
observer predicate and did not capture the recovery window. They retain their
explicit pre-boss health assistance and are not accepted as recovery evidence.

Native stomp recovery is preserved. Remaining work includes genuine complete
towers/bosses for both characters/slots, whole ending presentation and audio,
remaining finishers and broader combat/CPU/secret-stage regressions, then a
matching final production launcher and release ZIP. No material data was deleted.
