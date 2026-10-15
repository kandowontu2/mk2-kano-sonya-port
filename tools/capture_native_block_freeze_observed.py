"""Whole physical test host, corrected launch observers, no gameplay writes."""
import code,gzip,inspect,json,os
from pathlib import Path
import capture_native_block_freeze_diagnostic as prior

ROOT,need=prior.ROOT,prior.need
LUA='mk2ks_native_block_freeze_observed.lua'

def run(fighter,side,policy):
    need(policy in ('none','held','reactive'),'Only declared physical Block policy')
    need(not prior.census.census(),'No live native game before independent cold boot')
    source=prior.capture_source()
    before='audit_native_block_freeze_setup_checked_{fighter}_p{side}'
    need(source.count(before)==1,'Whole prior terminal transport')
    source=source.replace(before,f'audit_native_block_freeze_observed_{policy}_{{fighter}}_p{{side}}')
    before="MK2KS_STOCK_GAP='168')"
    need(source.count(before)==1,'Exact physical policy environment')
    source=source.replace(before,f"MK2KS_STOCK_GAP='168',MK2KS_BLOCK_POLICY='{policy}')")
    scope=dict(vars(prior.original),__file__=__file__,native=prior.native,census=prior.census,
               LUA=LUA,read_log=prior.read_log,gzip=gzip)
    exec(compile(source,__file__+'::whole_original_physical_host','exec'),scope)
    c=scope['capture'](fighter,side)
    folder=ROOT/f'audit_native_block_freeze_observed_{policy}_{fighter}_p{side}'
    files=[Path(__file__),Path(prior.__file__),ROOT/LUA,ROOT/'mk2ks_normal_subzero_freeze_v5031.lua',ROOT/'mk2ks_stock_fatality_v1021.lua']
    with gzip.open(folder/'executed_corrected_observer_sources.json.gz','wt',encoding='utf-8') as stream:
        json.dump(dict(host=source,files={str(p):p.read_text() for p in files}),stream)
    return c

if __name__=='__main__':
    captures={}
    jobs=[('kano',2,'none'),('liu_kang',2,'held'),('kano',2,'held'),('sonya',2,'held'),
          ('kano',2,'reactive'),('sonya',2,'reactive')]
    for fighter,side,policy in jobs:
        captures[f'{fighter}_p{side}_{policy}']=run(fighter,side,policy)
    code.interact(banner='Actual terminal native Freeze/Block comparisons, images retained in RAM.',local=dict(captures=captures))
