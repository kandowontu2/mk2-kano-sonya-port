"""Compiled-source boundary audit only; not exhaustive original AI discovery."""
import json
import verify_native_source_sync as sync
sync.verify()
path=sync.ROOT/'mame-mkp/src/mame/midway/midtunit_m.cpp'
source=path.read_text()
out=sync.ROOT/'audit_current_native_dispatch_boundaries_checked'
assert not out.exists()
requirements={
 'decision19':[
  'ai_decision_table + 19 * 4',
  'std::copy_n(rom + rom_offset(0xff9b1db0), 17 * 4, rom + ai_decision_table);',
  'write32(ai_decision_table + 17 * 4, 0xff9b20d0);',
  'write32(ai_decision_table + 18 * 4, 0xff9b20d0);'],
 'round19':[
  'ai_round_callback_table + 19 * 4',
  'std::copy_n(rom + rom_offset(0xff9b2210), 17 * 4, rom + ai_round_callback_table);',
  'write32(ai_round_callback_table + 17 * 4, 0xff9b91b0);',
  'write32(ai_round_callback_table + 18 * 4, 0xff9b91b0);'],
 'specialFollowup24':[
  'ai_special_callback_table + 24 * 4',
  'std::copy_n(rom + rom_offset(0xff9b76d0), 17 * 4, rom + ai_special_callback_table);',
  'for (unsigned index = 17; index < 24; index++)',
  'write32(ai_special_callback_table + index * 4, 0xff9b91b0);'],
 'specialDispatch24':[
  'ai_special_actions + 24 * 4',
  'std::copy_n(rom + rom_offset(0xff8a5960), 22 * 4, rom + ai_special_actions);',
  'write32(ai_special_actions + 22 * 4, native_address(knife_action));',
  'write32(ai_special_actions + 23 * 4, native_address(ring_action));',
  'write32(ai_special_actions + 22 * 4, native_address(ai_variety_router));',
  'write32(ai_special_actions + 23 * 4, native_address(ai_variety_router + 0x40));'],
 'independentProjectileResponseRows':[
  'std::copy_n(rom + rom_offset(0xff8d2bd0), 17 * 4, rom + outer);',
  'write32(outer + 17 * 4, 0xff800000U + kano * 8);',
  'write32(outer + 18 * 4, 0xff800000U + sonya * 8);'],
 'closeStockFallback':[
  '0x0b40,0xffee,', '0x0b40,0xffed,',
  '0x09c0,7,                             // restore stock close-attack A0',
  '0xc080,0x9470,0xff9b']}
def gate(text):
    for name,needles in requirements.items():
        for needle in needles:assert needle in text,(name,needle)
gate(source)
faults=[]
for name,needles in requirements.items():
    needle=needles[-1]
    broken=source.replace(needle,'REMOVED_BOUNDARY_AUDIT_TOKEN')
    try:gate(broken)
    except AssertionError:faults.append(name)
    else:raise AssertionError('Boundary mutation accepted: '+name)
report=dict(passed=True,sourceSHA256=sync.sha(path),sourceMatchesCompiledInputs=True,
    scopedChecks=list(requirements),effectiveSourceFaultsRejected=faults,
    nativeGames=0,newBuilds=0,sourceChanged=False,
    allOriginalAiEnemyIdLookupsAudited=False,liveTableBytesRead=False,
    controllerLossesProveGameBug=False,fullCampaignAccepted=False,fullPortAccepted=False,
    scope='Six explicit compiled-source relocation/dispatch invariants. Shared combat callbacks are not identity rewrites. No exhaustive original-ROM lookup or runtime-AI acceptance claim.')
out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
