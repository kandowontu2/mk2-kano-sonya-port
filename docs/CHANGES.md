# Reading every native integration change

The complete tracked-file diff is `patches/native-integration.patch`.
The full current source is in `mame-overlay/`; use the diff for review and the
overlay for building. `SOURCE_MANIFEST.json` pins all 15 compile inputs.

## Architecture

Kano and Sonya use real roster/actor identities 17 and 18. The implementation
initializes expanded native TMS34010 tables and code paths, imports character
data through a separate donor ROM window, and lets the native MKII engine run
the resulting game. It is not a visual overlay that renames Liu Kang during a
match. Earlier prototypes did use cloned native animation grammar; historical
builder comments describe those stages and should not be mistaken for the
final actor identity.

The custom emulator is required: an unmodified MAME executable does not contain
this integration. Both the host source changes and asset-building tools are
included here; copyrighted input/output data is not.

## File-by-file map

| Source, relative to `mame-overlay/` | Responsibility |
| --- | --- |
| `src/mame/midway/midtunit_m.cpp` | Main integration initializer; guarded native table/code construction, character parameters, selector and ladder registration, move parsers/bodies, CPU dispatch, contact/reaction/victim paths, finisher and morph integration, ending/attract handling, native audio dispatch/lifetimes. Read `init_mk2ks()` and the following helper methods. |
| `src/mame/midway/midtunit.cpp` | Machine/ROM configuration and `mk2ks` registration, donor and custom data regions, input and device integration. ROM names/hashes identify external requirements, not bundled ROM data. |
| `src/mame/midway/midtunit.h` | State declarations, timers and helper interfaces used by the integration. |
| `src/mame/midway/midtunit_v.cpp` and `.h` | Native video/graphics addressing and imported sprite rendering support. |
| `src/mame/midway/mk2ks_native_picture.h` | New initialization-time decoder for the donor picture format. This is decoder code, not an embedded image pack. |
| `src/devices/cpu/tms34010/tms34010.cpp` and `.h` | TMS34010 integration hooks and mapped execution support. These changes are explicit in the diff; they must not be omitted by rebuilding only the driver. |
| `src/devices/cpu/tms34010/34010gfx.hxx` and `34010ops.hxx` | Pinned compile dependencies, included even where unchanged against upstream. |
| `src/mame/mame.lst` | Adds the `mk2ks` game entry. |
| `src/frontend/mame/mame.cpp`, `src/frontend/mame/ui/slider.h`, `src/osd/modules/lib/osdlib.h`, `src/osd/modules/monitor/monitor_module.h` | Small frontend/build compatibility changes; review their exact short hunks in the diff rather than inferring gameplay changes. |

## Feature reading order

1. **Identity and parameters:** expanded native table layouts, ID predicates,
   attack/projectile response descriptors and original ownership semantics.
2. **Presentation:** dedicated top-row portraits; native cursor border/player
   number; independent previews; ladder portraits; name masks and shadows;
   cleanup during transitions. Selection art must not persist into fights.
3. **Combat:** eight specials, ordinary controls, true per-character CPU dispatch,
   paired grabs, hit/block/miss, interruption, recovery and KO paths.
4. **Rendering:** native compressed donor streams, palette/format tags, source
   addressing, pivots/floor placement and the native floor-shadow scanner.
5. **Finishers and victims:** two fatalities per character, Friendship,
   Babality, Pit/Tomb/Dead Pool, stock fatality victim compatibility, morph
   performer/victim lifetimes and native teardown.
6. **Audio:** imported samples and native DCS routing, hit/victim/announcer
   choices, channel ownership, priorities, finite playback and cleanup.
7. **Campaigns:** genuine ladder identities and schedules, bosses, original
   transition contexts, both own ending pages, attract/continue/join routes.

Source comments explain local preconditions and storage/layout guards. Builders
and qualifiers under `tools/` retain narrower experiments, failed attempts and
successors rather than hiding the work behind a single finished patch.

## Development history versus current source

Dated `history/STATUS_*.md` notes and versioned tools preserve technical
milestones. They are not all current, independently valid, or safe to execute
against the latest build. Some deliberately force diagnostic conditions and
are not evidence of an unassisted campaign. There is no fabricated claim that
each numbered file corresponds to a Git commit or successful build.

Two known final documentation mismatches are preserved transparently: the
historical finishline text references a superseded ZIP, and source-sync tools
refer to private runtime receipts. The matched player archive is the lean
2026-10-15 PLAYER package; its custom EXE/payload hashes are in the source
manifest. Publishing code does not republish that game-data package.
