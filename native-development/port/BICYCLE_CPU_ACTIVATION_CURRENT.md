# Native Bicycle command recognition against CPU Raiden

Run554 repeats553 with a bounded read-only joystick queue/object/process
observer for13790–13830. The complete campaign traces are byte-identical:
4375206F5A9A4060B7BEEACAD68C80795B4BC45CB2E876E310932033677C7631.
All26 current ROMs/own identities/no-fault checks pass. No game or input writes
are added by the observer, and snapshots remain windowless.

The actual native queue explains the rejected Bicycle. At HK13814–13817 the
newest direction codes are6,7,6 (Down,Left,Down), not the required6,7,7.
The oldest age is25–28 ticks, within the actual command table's36-tick limit;
this is a pattern failure, not simply an overly slow command. The first Back
arrived while native action0301 was rising from duck and did not enter the
queue. The second Back and Down did enter it. Ordinary HK0103 follows.

The optional --campaign-raiden-ready-bike policy releases the guard and waits
for native grounded stance0303 before beginning the first Back and resetting
the command clock. Run555 retains the earlier Baraka/Reptile/Jax wins (Jax2–0
at135/93 HP). Its observed HK interval13821–13824 now has actual queue6,7,7,
oldest age10–13 ticks, and native Bicycle0204 appears13823. Three genuine
Bicycle episodes occur across this run. The actual game command implementation
was not edited or bypassed; this corrects physical test-controller timing.

Raiden still wins all four sampled rounds through one ordinary paid continue,
ending20,829 fields. His minima126,161,126,126 do not establish a successful
Bicycle punish; other Leg holds occur too. Do not attribute35 damage to Bicycle
without per-hit evidence. This confirms activation in the CPU matchup, not
effectiveness, complete recovery, all edge cases or campaign completion.

audit_campaign_bike_queue.py records the observed patterns and separately
reports actual activation. Current program/IPS archive is unchanged. Full
campaigns, bosses, earned ending/cast/credits and final audio/visual acceptance
remain open. Future work should improve active-move spacing/recovery rather
than repeat the rejected-input policies or change game code to accommodate them.
