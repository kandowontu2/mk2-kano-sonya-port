"""Native stock64 palette correction; preserve failed preflight and all gates."""
from pathlib import Path
base=Path(__file__).with_name('current_babality_ram_v5446.py')
source=base.read_text()
changes={
 "BASE=ROOT/'audit_v5447_current_babality_ram'":"BASE=ROOT/'audit_v5450_current_babality_ram'",
 "OUT=ROOT/'audit_v5448_current_babality_progress'":"OUT=ROOT/'audit_v5451_current_babality_progress'",
 "LUA=ROOT/'mk2ks_current_babality_ram_v5446.lua'":"LUA=ROOT/'mk2ks_current_babality_ram_v5449.lua'",
 "need(1<count<=32,'Original baby palette bounds')":"need(1<count<=(1<<((command>>12)&7)),'Original baby palette bounded by actual native source bit depth')",
 "for path in(LUA,ORIGINAL,Path(__file__).resolve(),":"for path in(LUA,ORIGINAL,ROOT/'mk2ks_current_babality_ram_v5446.lua',ROOT/'tools/current_babality_ram_v5446.py',Path(__file__).resolve(),",
}
for before,after in changes.items():
 assert source.count(before)==1,before
 source=source.replace(before,after)
exec(compile(source,str(base)+'.native_stock64_passive_observer','exec'),globals())
