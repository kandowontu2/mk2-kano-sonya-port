"""Explicit raw-action bounds audit of common drone_beware, not all callers."""
import hashlib
import json
import zipfile
from pathlib import Path
from inventory_character_tables import source_tables
from prepare_game_candidate import ZIP
from drone_source import integrate as original_extensions
from cpu_action_source import integrate, ROUTES

PORT=Path(__file__).resolve().parent;SRC=PORT.parent/'baseline/mk2-rebuild-main/srcp'
raw=(SRC/'MKDRONE.ASM').read_bytes();text=raw.decode('cp437').replace('\r\n','\n')
with zipfile.ZipFile(ZIP) as archive:
    canonical=archive.read('mk2-rebuild-main/src/MKDRONE.ASM').decode('cp437').replace('\r\n','\n')
def executable_source(value):
    # The build preparer relocates/consolidates .def/.ref declarations and adds
    # a newline after DOS EOF. Neither changes executable instructions/data.
    return '\n'.join(line for line in value.rstrip('\n\x1a').splitlines()
                     if not line.strip().startswith(('.def ','.def\t','.ref ','.ref\t')))
assert executable_source(text)==executable_source(integrate(original_extensions(canonical))), 'Current executable dispatcher differs from audited generator'
tables=source_tables(text)
names={0:'counter_proj_table',1:'counter_attack_table',2:'counter_propell',6:'counter_sitting_duck'}
values={category:[value for row in tables[name]['rows'] for value in row['values']]
        for category,name in names.items()}
cases=[]
for action in (0x20b,0x207,0x211,0x212,0x117,0x216,0x217,0x219,0x21a,0x204,0x214,0x618,0x61a,0x61b):
    category,index=action>>8,action&255
    entries=values[category]
    cases.append(dict(action=f'{action:04X}',category=category,index=index,
        table=names[category],tableEntries=len(entries),inBounds=index<len(entries),
        reaction=entries[index] if index<len(entries) else None))
effective=[]
for identity in (17,18):
    for case in cases:
        action=int(case['action'],16)
        intercepted=action in ROUTES[identity]
        effective.append(dict(identity=identity,action=case['action'],
            intercepted=intercepted,
            effectiveReaction=ROUTES[identity][action] if intercepted else case['reaction'],
            originalTableAccessed=not intercepted,
            effectiveLookupInBounds=intercepted or case['inBounds']))
report=dict(scope='Raw legacy table limits and identity-aware native dispatch, separately reported',
    sourceSHA256=hashlib.sha256(raw).hexdigest().upper(),cases=cases,
    allListedTagsInBounds=all(case['inBounds'] for case in cases),
    rawBoundsDescribeLegacyTablesOnly=True,executableDispatcherMatchesCanonicalTransform=True,
    effectiveCases=effective,
    effectiveCasesIncludeCrossCharacterTags=True,
    crossCharacterTagsAreNotReachabilityProof=True,
    declaredOwnRoutes=[dict(identity=identity,action=f'{action:04X}',reaction=reaction,
                           originalTableAccessed=False)
                       for identity,routes in ROUTES.items() for action,reaction in routes.items()],
    allDeclaredOwnRoutesBypassLegacyTables=True,
    allListedEffectiveLookupsInBounds=all(case['effectiveLookupInBounds'] for case in effective),
    bossCategoryHelperAloneSufficient=False,runtimeCPUBehaviorVerified=False,releaseReady=False)
(PORT/'CPU_ACTION_LOOKUP_AUDIT.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
