"""Original-ROM CPU close-attack state semantics; no emulator execution."""
import json
import subprocess
import verify_native_source_sync as sync
sync.verify()
out=sync.ROOT/'audit_current_stock_cpu_attack_state'
assert not out.exists()
rom=sync.ROOT/'mk2/mk2-maincpu.bin'
assert sync.sha(rom)=='45B3285496DB555EFAF4A3608A4F59845DD47A82E4A0593607E0592F47B36F23'
exe=sync.ROOT/'mame-mkp/unidasm.exe'
def disassemble(pc,count):
    result=subprocess.run([str(exe),str(rom),'-arch','tms34010','-skip',str((pc-0xff800000)//8),'-count',str(count),'-basepc',hex(pc)],capture_output=True,text=True,check=True)
    assert not result.stderr.strip()
    return result.stdout
attack=disassemble(0xff9b9470,1832)
setup=disassemble(0xff877bc0,448)
assert 'CALLA  FF877BC0h' in attack
assert attack.count('CALLA  FF835440h')==2
assert '*A13(1F0h)' not in attack
assert 'ORI    10h,A4' in setup and 'MOVE   A4,*A13(210h),0' in setup
assert '*A13(1F0h)' not in setup
source=(sync.ROOT/'mame-mkp/src/mame/midway/midtunit_m.cpp').read_text()
assert '0xc080,0x9470,0xff9b' in source
out.mkdir()
(out/'original-close-attack.asm.txt').write_text(attack)
(out/'original-setup.asm.txt').write_text(setup)
report=dict(originalRomVerified=True,stockCloseAttackEntry='FF9B9470',setup='FF877BC0',
    collisionHelper='FF835440',nativeActiveFlag='0010',
    explicitActionPublicationInInspectedRoutine=False,
    addedCloseRouterRetainsStockFallback=True,
    conclusion='CPU action771 with active flag0010 is compatible with original stock close-attack semantics; action alone cannot establish idle or a port defect.',
    observedTenHitsExactAttackSubtypeProven=False,fullPortAccepted=False,
    originalRomSHA256=sync.sha(rom),currentSourceSHA256=sync.sha(sync.ROOT/'mame-mkp/src/mame/midway/midtunit_m.cpp'))
(out/'report.json').write_text(json.dumps(report,indent=2))
print(json.dumps(report))
