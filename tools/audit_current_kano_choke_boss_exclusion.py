"""Compiled-source boss immunity boundary; not a runtime contact claim."""
import json
import verify_native_source_sync as sync
sync.verify()
path=sync.ROOT/'mame-mkp/src/mame/midway/midtunit_m.cpp'
source=path.read_text();out=sync.ROOT/'audit_current_kano_choke_boss_exclusion_checked'
assert not out.exists()
start=source.index('leg_cursor=choke_action; leg_limit=choke_wait;')
end=source.index('// Sonya B,B,D+HK',start)
body=source[start:end]
needles=['leg_code({0xb7aa,0x0140,0xb540,0x01f0,0x0b40,0xfff3});',
 'unsigned const choke_boss1=leg_branch(0xca80,0);',
 'leg_code({0x0b40,0xfff2}); unsigned const choke_boss2=leg_branch(0xca80,0);',
 'leg_movi(0,native_address(choke_attack)); leg_call(0xff835440);',
 'write32(choke_boss1,native_address(leg_cursor)); write32(choke_boss2,native_address(leg_cursor));']
def gate(text,section):
    assert 'if (id==12 || id==13) { write32(choke_victims+id*4,0); continue; }' in text
    assert all(n in section for n in needles)
    assert section.index(needles[0])<section.index(needles[3])<section.index(needles[4])
gate(source,body)
for n in needles:
    try:gate(source,body.replace(n,'',1))
    except AssertionError:pass
    else:raise AssertionError('Boss exclusion fault accepted')
report=dict(compiledSourceBossExclusionChecked=True,bossIDs=[12,13],bossNames=['Kintaro','Shao Kahn'],
    victimTableRowsZero=True,bossComparisonBeforeCollision=True,removedGuardFaultsRejected=len(needles),
    sourceSHA256=sync.sha(path),runtimeBossChokeAttempted=False,fullPortAccepted=False)
out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
