# Native ending page-object cleanup correction

Inspection of UTIL.clr_scrn establishes that it clears screen memory and
temporarily gates display; it does not release object lists or palette slots.
The initial two-page object-based presentation therefore lacked object cleanup
between pages and before returning to credits. This was found by source review,
not by claiming an earned ending had been observed.

The original MKAMODE.one_story_screen calls murder_myoinit_score after its
view interval. MKUTIL.murder_myoinit_score calls murder_myoinit, which runs
oinit, clears sound bookkeeping, removes disposable processes and restores the
score palette. MKDISP.oinit resets object lists/free pool, palettes, clipping
and background state. The new own-ending loop now uses that same reset at
each page boundary and on final return. Its A12 cursor save remains outside
the call and is restored afterward; the current ending process follows the
same native calling convention as the original story presenter.

Source regression checks require both cleanup calls in the correct positions.
The working hidden compile passes (26.95 seconds, no created window). Actual
linked-ROM inspection verifies two cleanup CALLA instructions, two framebuffer
clear calls, one image allocation/insertion path and correct image/text/palette
pointers. Current program SHA256:
DCB62D8DA3A1E89330D1101C4370D44A24580AAADC26CAC632699C769179194B.
All 20 ending/art/coordinate/round/CPU/boss/IPS tests pass.

An independent clean compile has been started from verified refreshed inputs.
Only 135 hash-pinned generated outputs (2,918,866 bytes) were removed; source
and rebuild inputs were preserved. Clean byte comparison and a fresh runtime
regression must finish before updating their acceptance. Actual earned ending
rendering, page transitions, cleanup and credits return remain unverified.
No development ZIP or release was promoted.

Independent clean compile completed: exit0, no window, 79.92 seconds. All 130
fresh linked objects are present and all four program parts match the working
build byte-for-byte. Fresh stock-MAME run 547 completed a physical Sonya
Friendship/reselection/rematch. It verifies all 26 current ROMs, own identities,
full starting health, live damage, state reset, 600 consecutive combat fields
and 78,000 hardware palette comparisons. The observed dance/completion contexts
are absent after selection, with no new cluck commands. This regression does
not execute the ending and cannot certify page cleanup or credits runtime.

Further source review finds the native MKEND.cast_table still contains only
the original twelve fighters. An own Kano/Sonya cast pair and verified credits
presentation remain a real integration gap, separate from the ending picture
loop and campaign-controller failures.
