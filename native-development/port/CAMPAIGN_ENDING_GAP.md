# Native ending gap found in current candidate

audit_campaign_endings.py records current source hashes and direct-index paths
in CAMPAIGN_ENDING_AUDIT.json. MKEND.congrats obtains get_winner_ochar and
passes it directly to msg_rise and later show_a0_ending. IDs17/18 are real
added fighters, not original-roster indices.

MKEND.end_winner_text has19 pointers, but slots17/18 are txt_found_4 and
txt_found_5 (clue text), not Kano/Sonya congratulations. They cannot simply be
replaced globally without checking other clue consumers. UNZIP.end_text_1 and
end_text_2 each have12 three-longword rows. Both added IDs index beyond them.
The same routine derives compressed-story indices50/51 and52/53 without an
added-character story route. No successful campaign-ending runtime evidence
exists; prior finite fight/finisher checks do not cover this path.

Required fix: explicit own-identity congratulations dispatch preserving the
original clue indices, dedicated native Kano/Sonya story presentation/data,
and reproducible source integration. Do not map them to another fighter's
ending or add a custom emulator handler. Preserve the original12 ending paths.
Then verify assembly/ROM patches and actual post-boss ending/credits flow.
Current development ZIP remains a candidate and must not be promoted as a
complete playable release while this known defect remains.

Implementation in progress: ending_source.py supplies own17/18 dispatch before
the original lookups, separate KANO WINS/SONYA WINS strings, and dedicated
native text-only story routines returning to the existing cast/credits flow.
prepare_game_candidate.py now regenerates these changes. test_ending_source.py
compares the original tables and all following original bytes against the
canonical rebuild ZIP and rejects double integration. The independent clean
staging contains these two changed sources; the working ROM/development ZIP
have NOT yet been promoted. Clean compilation/runtime and final own ending
illustrations remain pending. Text-only screens are a provisional safety and
identity fix, not final native-feeling ending acceptance or campaign proof.

Both clean and working hidden compiles now exit0 with no created windows.
The two changed ASM files assemble without errors/warnings. Staging preserved
all other generated working files byte-for-byte (historical comments/ref
placement differ from regeneration, so no blanket source identity is claimed).
The independently compiled four program parts match the working build exactly.
Current program ROM has changed; earlier runtime receipts and development ZIP
remain historical until the new program is tested and packaged. No ending
runtime, full campaign, artwork or release acceptance follows from compilation.

Current run384 is the first stock-MAME regression on this ending-enabled link.
Its trace exactly reproduces373's observed Sonya round outcomes: two Baraka
wins, one Reptile win, then two losses. Correct own identity throughout, no
recorded missing/recovery/Lua fault. All26 ROM bytes requalify against clean
program/sound/graphics plus original art. This does NOT execute either ending.
The refreshed source audit now distinguishes the intercepted own routes from
the intentionally unchanged original fallback tables; it matches both current
source files exactly to their canonical-input transformations. It retains
addedCharacterEndingsRuntimeVerified=false. No forced-win, RAM write, debug
ending shortcut, GitHub publication or development ZIP refresh was performed.

Renderer-call fix: source audit of DIAGTEXT.ASM establishes lm_printf expects
A8=mess_mac followed by text and calls lm_setup before printf. The provisional
ks_story_show passed that descriptor directly to printf without initializing
font/position/formatter registers. It now uses jsrp lm_printf in both generator
and live UNZIP.ASM. test_ending_source checks the exact routine, and all original
tables/following bytes remain preserved. Working hidden compile exits0 in26.53s,
no window. Six source/PCM tests and the regenerated ending dispatch audit pass.

Independent clean inputs were verified;134 hash-pinned generated outputs
(2912350bytes) removed without touching sources. Only UNZIP.ASM regenerates;
hidden clean compilation is in progress. Existing development ZIP predates
this renderer fix and must not certify endings. Runtime story/artwork/credits
and complete earned campaigns remain unverified; this is a source-interface
correction, not a claim that either ending has now been seen in gameplay.

Renderer-fixed clean compilation exits0 in76.29s with no window. All129 objects
and four parts qualify byte-identical. Current410 completes the physical
Friendship/rejoin600-field regression with true identities/full starting health,
damage and no new cluck requests in the fresh match. All26 chips independently
requalify against410. The development ZIP was refreshed only after those gates
and both IPS decoders/archive roundtrip pass. Neither ending is exercised by
this runtime case; artwork/story/credits and earned campaign acceptance remain
false. See current patch-packager report for the new candidate hash.
