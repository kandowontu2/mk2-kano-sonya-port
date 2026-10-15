"""Exact source check: CPU variety router is retained, not a new feature here."""
from pathlib import Path
code=Path(__file__).with_name('audit_current_historical_campaign_transfer.py').read_text()
old="assert 'constexpr unsigned ai_variety_router = 0xf7800;' in current and 'constexpr unsigned ai_variety_router = 0xf7800;' not in old"
new="""assert 'constexpr unsigned ai_variety_router = 0xf7800;' in current and 'constexpr unsigned ai_variety_router = 0xf7800;' in old
router_start='// CPU specials enter through FF8A5900'
router_end="// MKII's Pit/Tomb finishers"
assert segment(old,router_start,router_end)==segment(current,router_start,router_end)"""
assert code.count(old)==1
code=code.replace(old,new)
code=code.replace('currentAddsCpuVarietyRouter=True','currentAddsCpuVarietyRouter=False,cpuRoutingSourceUnchanged=True')
code=code.replace('Expanded CPU gameplay and other source changes prevent automatic whole-build campaign transfer.','CPU routing source is identical, but other substantial source changes prevent automatic whole-build campaign transfer.')
code=code.replace('currentCpuRoutingChanged=True','currentCpuRoutingChanged=False')
exec(compile(code,__file__,'exec'),{'__file__':__file__})
