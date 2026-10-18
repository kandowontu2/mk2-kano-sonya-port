# Current034F native morph regression

Program034F1179440C024A041A330F349A5F8F6C1EF3B919DC1FB701115223C15CB4F7.
Stock729/730 physical Player1/Player2 --morph-specials and731/732
--morph-throws --morph-late-throw exit normally at9000 fields. All pass
qualify_morph.py with actual26 current chip bytes, stock MAME hash,
frozen input-only controller, own identities/poses, no missing markers/
Lua faults and automatic native returns. No game/ROM changes were made.

Both special cases retain selected Shang6 while active IDs follow
6→17→6→18→6→18→6. Each own identity lasts524 fields. Kano Knife and Sonya
Ring activate and deal22 damage. Both physical Sonya button-order routes
and Kano's native command are observed. qualify_morph_art_trace.py729/730
also verifies all three intermediate poses, forward/reverse ordering,
four-field cadence and measured entry/reverse grounding on both sides.
This is finite trace verification, not comprehensive visual/palette approval.

Both late-throw cases start the paired throw before nominal expiry and
remain transformed through it. Kano has28 owner-action fields and34
damage; Sonya52 fields and34 damage. Native return occurs13 fields after
the final throw field, not mid-hold. Own durations are554/582 fields, then
the later idle Sonya morph returns after524. Physical fight-field windows
are Kano662–689→return702; Sonya1542–1593→return1606. Neither identity nor
timer was forced by the controller.119 selected local tests pass.

These close current-link Knife/Ring and paired-throw expiry fixtures,
not all transformed specials/finishers, interruption/edge/boss/victim
coverage, complete palette/audio acceptance or campaign completion.
Stage finishers and full campaigns/earned endings still need current
runtime evidence. All four runs stayed headless, sequential and below-
normal priority without large media capture. Per-run qualification.json
and MORPH_ART_TRACE_QUALIFICATION.json contain authoritative evidence.
