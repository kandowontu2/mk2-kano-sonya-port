# Jax observation and physical-spacing comparison

Runs549 and550 use the same current native program and physical policy.
Run550 appends only a read-only object/process/screenshot observer for fields
10780–11000. Their entire campaign CSVs are byte-identical, SHA256
76DDBA02ECDB212B5EE27F5F4809F69F8F4417A14B7E5CCF9DE04B048F46AB19.
The observer introduces no game writes or input changes. Both full-ROM and
no-fault audits pass. It holds no whole-match pixel arrays.

The suspicious interval shows real Jax rapid punches in screenshots10900,
10920 and10940 while his process action tag remains0303. The original native
drone_rfp body is byte-for-byte preserved as source against the canonical ZIP:
it calls init_special (not init_special_act), and does not set p_action itself.
MOVES.init_special_act contains the action assignment before the init_special
label. Therefore0303 alone is not proof the CPU is idle. This observation does
not confirm the suspected persistent-projectile bug, nor prove every incoming
damage event. audit_campaign_damage_window.py pins this narrow evidence.

The prior Jax policy starts Rings at distances just above100, exposing Sonya
to a close-range punish during charge/recovery. The new optional physical-only
--campaign-jax-safe-ring policy fires only beyond240, keeps down/block at medium
range, attempts Leg Grab below100 and returns to guarding after the command.
It does not edit health, AI, difficulty, positions, actions, collision or ROMs.

Run551 earns Baraka and Reptile wins, then beats Jax2–0 without a continue;
Sonya's winning health is135 and93. She reaches Raiden (native7/map3) and loses
through three accepted normal paid continues, ending at27,148 fields. This is
the first exercised current run of the Raiden-specific guard/Ring/dive-recovery
Leg policy, which fails to clear Raiden. Raiden's eight round minima are
161,161,161,161,161,139,156,161. Do not rerun that policy unchanged as progress.

All26 current ROM bytes, true Sonya identity, no missing-animation marker,
no illegal-opcode recovery and no Lua fault pass. All23 source/art/roster/
coordinate/round/CPU/boss/IPS tests pass. The current program and development
IPS ZIP remain unchanged. Full campaigns, later enemies/bosses, earned endings,
cast/credits and final audio/visual acceptance remain unfinished.
