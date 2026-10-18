# Native freeze/shatter follow-up

The first physical follow-up trials 195/196 never reached the command:
the observer tried to walk within 60 pixels, but normal collision spacing
kept the fighters roughly 62 pixels apart. Its approach target is now 68,
inside the native 045h close-range command gate. No game collision or
fatality gate was changed.

Trials 197/198 then exposed the actual defect. `r_shatter_punch` directly
indexes a 12-entry `frozen_legs` table by true victim ID. Sonya entered
illegal-opcode recovery at frame5327; Kano happened to survive the invalid
lookup. This is distinct from `r_pitched`, which is not this reaction.

`superfreeze_source.py` now also handles own IDs before that lookup. Each
uses its own main39 part6 lower body and own frozen palette. All other IDs
retain the original palette/table path. The native ice-burst process,
sound, screen shake, uppercut reaction and death-blow completion remain.
The own body is retained throughout; no Jax proxy or emulator hack.

Hidden native compilation passed in 19.16 seconds without a window.
Current stock MAME runs 199–202 each completed 9,000 fields, covering both
characters on both physical player sides. Each controller won two natural
rounds, performed deep freeze (143 observed fields) then the source-defined
forward/down/forward/forward+HP close follow-up. Native fatality state2
lasted65 fields and reachedffff completion. Own lower-body poses were
observed for40/41 fields, including completion, with true identity retained.
No missing-art, illegal recovery, Lua errors or guest-memory writes.

`qualify_shatter_victims.py` pins exact current program/graphics bytes,
stock emulator/controller hashes, source dispatches, natural KOs, true
victim IDs, frozen own poses, fatality timing and own legs at completion.
`SHATTER_VICTIM_QUALIFICATION.json` records the bounded proof. Current
lane hashes: 2A524EBCB6FC20BF72339AEA2F834472183A82F8165E1245E49B0CD5EDCDFA85
and 3D3FCB9DD887346AA52F423D4F91BCB3C51F331F38F3CDC77D57FC79D182ACD1.

Viewed captures199/200 show the native burst and own blue lower bodies.
The final crystalline ice artwork is still unfinished; original-roster
runtime controls and broader timing/interruption tests remain open.
Source preparation has zero structural-token differences, but no fresh
byte-identical clean-build proof. Older link reports are historical.
No release was promoted; the full port is not yet qualified.
