# Development patch packager refresh

The packager had three obsolete hardcoded inputs: generated_impale graphics,
SoundW output, and stock_deadpool_late123 receipt. It now uses the verified
current graphics directory, SoundP sockets and a required explicit
--runtime-run=NAME argument. All26 target chip hashes must still equal the
selected successful stock-MAME receipt before patch creation proceeds.

Current graphics-directory/socket hashes and nine IPS/morph source tests pass.
This edit does not itself create or promote a new ZIP. Existing development
patch ZIP remains historical. Clean current-link rebuild, generated-output
refresh/roundtrip handling, source closure and minimal-package acceptance
must be verified before regenerating it; final release gates remain open.
No ROMs, emulator or GitHub release was changed by this script correction.

Follow-up: the current clean program/graphics proof now passes and the
development package was regenerated with --refresh-generated and an explicit
stock_wolf_game358 receipt. All26 chips match;14 IPS patches pass two decoders
and the actual archive patch roundtrip. The old hash-verified generated
roundtrip archive was replaced after verifying the fresh candidate. The ZIP
is5,429,999 bytes, SHA256097CACB6C7EA170E7C09213D3E15445762C66726EA80AD584854E1D10290AB66.
No final release or GitHub publication occurred. Full port/release gates remain
false in manifest and packaging verification.

Latest refresh: current pop-cue program/SoundP, full graphics chain and all26
chips independently requalified against stock_wolf_game365. The refreshed ZIP
adds the source-checked MOVELIST_NATIVE.txt and corrects rebuild wording.
Both IPS decoders and actual patcher archive roundtrip pass. ZIP5,432,896 bytes,
SHA256811C07A05ED9499576C9181F158F87D880A81E3DC9A82EB83675E6205E87C15A.
This supersedes the previous development ZIP, not the remaining gameplay,
campaign, audiovisual or final publication gates.

Current refresh389 includes native Ball cue and provisional own text endings,
with explicit ending artwork/runtime warnings and four additional source/helper
files. All26 clean rebuilt chips match389; two IPS decoders and actual archive
roundtrip pass. ZIP5,442,592bytes, SHA256
B2E869EE8D80DE75266F4AAC0FD140469ACF455566DF384BEB2B36D68451309E.
It replaces the prior hash-verified generated candidate/roundtrip; no extra
release copy or GitHub publication. Full port and release flags remain false.

Current guarded Friendship16-clip refresh395: all26 independently rebuilt ROM
chips match the stock-MAME input;14 IPS patches pass both decoders and actual
archive roundtrip. The minimal development ZIP is5,447,151bytes, SHA256
4B371CC9E8640A956D2C56343730751EC93991C67C48ED4102D3CA78E8493500.
It includes native Friendship source/PCM generators and explicit unfinished
overlapping-cluck/cleanup, campaign and ending warnings. Previous generated
ZIP/roundtrip replaced after hash validation, not retained as an extra release.
No final release/publication or broad acceptance follows from packaging.

Renderer-call correction refresh410: the only game-source delta from395 is
UNZIP's dedicated text routine using lm_printf instead of uninitialized printf.
Clean program/all26-chip proof and physical post-Friendship rejoin regression
pass. The development ZIP5,447,150bytes, SHA256
E5DA5D0B2F5E0D59370899E50B193EB02C5A876F81BF28726394322F2AA00631
passes both IPS decoders/actual roundtrip and replaces the prior generated
candidate. No extra old release copy retained. Ending runtime/artwork, campaign
and audio warnings remain; this is not a final GitHub release.
