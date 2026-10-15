"""Whole Pit trial, exact expanded settled driver with original inner safety guard.

Preserve the actual zero-field startup failure: the outer wrapper matched
the inner wrapper's quoted ':write_' safety key. Execute the expanded original
driver instead; retain that original guard on the actual generated controller.
"""
import json
from pathlib import Path
import run_native_pit_transition_rejoin_settled_bytes as original

ROOT,need,sha,once=original.ROOT,original.need,original.sha,original.once
FAILED_FOLDER=ROOT/'audit_native_pit_transition_rejoin_settled_bytes_kano_p1_ram'
FAILED_REPORT=ROOT/'audit_native_pit_transition_rejoin_settled_bytes_kano_p1_checked/report.json'
failure=json.loads(FAILED_REPORT.read_text());meta=json.loads((FAILED_FOLDER/'result.json').read_text())
need(not failure['passed']and meta['captureCompleted']and meta['exit_code']==3 and
     meta['ramGuestSHA256']is None and meta['observedRGBFields']==meta['modelExactFields']==0 and
     not meta['modelErrors']and 'mk2ks_native_pit_rejoin_settled_driver.lua:16: assertion failed!'
     in(FAILED_FOLDER/'stderr.log').read_text()and all(sha(p)==h for p,h in meta['input_hashes'].items()),
     'Whole actual quoted-key startup failure and executed inputs frozen; no gameplay happened')


def direct_source_proof():
    original.settled_source_proof()
    driver=(ROOT/'mk2ks_native_tomb_rejoin_driver.lua').read_text()
    for old,new in(
        ('if mode==4 and p:read_u16(slots[n].state)==3 then',
         'if mode==4 and p:read_u16(slots[n].state)==3 and p:read_u16(slots[n].roster)<=18 then'),
        ("join_css[n]={at=frame,path=route(p:read_u16(slots[n].roster),target)}\n     join_log('SELECT','slot='..n..' target='..target..' route='..table.concat(join_css[n].path,','))",
         "join_css[n]={at=frame,path=nil}\n     join_log('SELECT_OPEN','slot='..n..' previous_roster='..p:read_u16(slots[n].roster)..' target='..target)"),
        ('local css_age=frame-join_css[n].at',
         "local css_age=frame-join_css[n].at\n    if css_age==56 then\n     local cursor=p:read_u16(slots[n].roster)\n     join_css[n].path=route(cursor,target)\n     join_log('SELECT','slot='..n..' start='..cursor..' target='..target..' route='..table.concat(join_css[n].path,','))\n    end"),
        ('for i,key in ipairs(join_css[n].path)do','for i,key in ipairs(join_css[n].path or{})do')):
        driver=once(driver,old,new)
    need((ROOT/'mk2ks_native_pit_rejoin_direct_driver.lua').read_text()==driver,
         'Entire original controller construction and inner guest-write guard; only four exact later route changes')
    for family,base,changes in(
        ('provenance','mk2ks_native_pit_rejoin_provenance.lua',
         (("dofile('mk2ks_native_tomb_rejoin_guarded_driver.lua')","dofile('mk2ks_native_pit_rejoin_direct_driver.lua')"),)),
        ('display','mk2ks_native_pit_rejoin_settled_display.lua',
         (("dofile('mk2ks_native_pit_rejoin_settled_provenance.lua')","dofile('mk2ks_native_pit_rejoin_direct_provenance.lua')"),)),
        ('timing_display','mk2ks_native_pit_rejoin_settled_timing_display.lua',
         (("io.open('mk2ks_native_pit_rejoin_settled_display.lua','rb')","io.open('mk2ks_native_pit_rejoin_direct_display.lua','rb')"),
          ("dofile('mk2ks_native_pit_rejoin_settled_provenance.lua')","dofile('mk2ks_native_pit_rejoin_direct_provenance.lua')"))),
        ('scanout_display','mk2ks_native_pit_rejoin_settled_scanout_display.lua',
         (("io.open('mk2ks_native_pit_rejoin_settled_timing_display.lua','rb')","io.open('mk2ks_native_pit_rejoin_direct_timing_display.lua','rb')"),))):
        expected=(ROOT/base).read_text()
        for old,new in changes:expected=once(expected,old,new)
        need((ROOT/('mk2ks_native_pit_rejoin_direct_'+family+'.lua')).read_text()==expected,
             'Entire already proven observer/transport/timing, exact direct-driver target '+family)


source=original.source
source=once(source,"PREFIX='audit_native_pit_transition_rejoin_settled_bytes'","PREFIX='audit_native_pit_transition_rejoin_direct'")
source=once(source,"leaf = f'audit_native_pit_transition_rejoin_settled_bytes_{fighter}_p{side}'",
                   "leaf = f'audit_native_pit_transition_rejoin_direct_{fighter}_p{side}'")
source=once(source,"LUA=tuple(ROOT/('mk2ks_native_pit_rejoin_settled_'+name+'.lua')for name in('driver','provenance','display','timing_display','scanout_display'))",
                   "LUA=tuple(ROOT/('mk2ks_native_pit_rejoin_direct_'+name+'.lua')for name in('driver','provenance','display','timing_display','scanout_display'))")
source=once(source,'    settled_source_proof()','    direct_source_proof()')
source=once(source,"    for p in(*LUA,Path(__file__).resolve(),settled_source_path,byte_failure,",
    "    for p in(*LUA,Path(__file__).resolve(),bytes_source_path,direct_failure,"
    "*(p for p in direct_failed_folder.rglob('*')if p.is_file()),settled_source_path,byte_failure,")
scope=dict(__name__=__name__,__file__=__file__,original_source_path=original.original_source_path,
           failure_path=original.failure_path,source_bound_path=original.source_bound_path,
           failed_native_folder=original.failed_native_folder,failed_native_output=original.failed_native_output,
           expanded_source_path=original.expanded_source_path,literal_failure=original.literal_failure,
           strip_lua_strings=original.strip_lua_strings,direct_source_proof=direct_source_proof,
           literal_source_path=original.literal_source_path,race_receipt=original.race_receipt,
           race_output=original.race_output,race_folder=original.race_folder,
           settled_source_path=original.settled_source_path,byte_failure=original.byte_failure,
           bytes_source_path=Path(original.__file__),direct_failure=FAILED_REPORT,direct_failed_folder=FAILED_FOLDER)
exec(compile(source,__file__+'::entire_original_Pit_trial_exact_expanded_initialized_cursor_controller','exec'),scope)
globals().update({k:v for k,v in scope.items()if not k.startswith('__')})
