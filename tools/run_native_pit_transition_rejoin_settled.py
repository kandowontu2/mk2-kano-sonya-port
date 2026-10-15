"""Full original Pit trial; plan later physical selection from initialized cursor.

Preserve actual empty-route/wrong-Reptile confirmation. Only later ordinary
input planning changes, never the guest, initial earned trajectory or gates.
"""
import json
from pathlib import Path
import run_native_pit_transition_rejoin_literal_checked as original

ROOT,need,sha,once=original.ROOT,original.need,original.sha,original.once
RACE_FOLDER=ROOT/'audit_native_pit_transition_rejoin_literal_checked_kano_p1_ram'
RACE_OUTPUT=ROOT/'audit_native_pit_transition_rejoin_literal_checked_kano_p1_checked'
RACE_RECEIPT=RACE_OUTPUT/'cursor_initialization_race_preservation_and_ram_retirement.json'
preserved=json.loads(RACE_RECEIPT.read_text())
need(preserved['passed']and preserved['preservationAndRAMRetirementOnly']and not preserved['fullOriginalTrialAccepted']and
     preserved['actualInitialFullPitScene']['passed']and preserved['initialIndependentFields']==677 and
     preserved['laterSourceDefinedNativeFields']==2923 and preserved['originalNativeRasterBuffersReleased']==57 and
     preserved['reviewServerClosed']and preserved['originalCaptureRAMDictionaryCleared']and
     preserved['actualWronglyConfirmedOpponent']==9 and preserved['intendedOpponent']==18 and
     not preserved['actualIntendedAdmission']and all(sha(p)==h for p,h in preserved['inputHashes'].items()),
     'Entire original actual cursor race/failure/scene proof preserved; no previous native game remains')


def settled_source_proof():
    original.exact_expanded_source()
    for family,old,new in(
        ('display',"dofile('mk2ks_native_pit_rejoin_provenance.lua')","dofile('mk2ks_native_pit_rejoin_settled_provenance.lua')"),
        ('timing_display',"io.open('mk2ks_native_pit_rejoin_expanded_display.lua','rb')","io.open('mk2ks_native_pit_rejoin_settled_display.lua','rb')"),
        ('scanout_display',"io.open('mk2ks_native_pit_rejoin_expanded_timing_display.lua','rb')","io.open('mk2ks_native_pit_rejoin_settled_timing_display.lua','rb')")):
        expected=once((ROOT/('mk2ks_native_pit_rejoin_expanded_'+family+'.lua')).read_text(),old,new)
        if family=='timing_display':
            expected=once(expected,"dofile('mk2ks_native_pit_rejoin_provenance.lua')","dofile('mk2ks_native_pit_rejoin_settled_provenance.lua')")
        need((ROOT/('mk2ks_native_pit_rejoin_settled_'+family+'.lua')).read_text()==expected,
             'Whole original observer/timing/transport, only exact declared later driver targets '+family)
    driver=(ROOT/'mk2ks_native_pit_rejoin_settled_driver.lua').read_text()
    need(driver.count('once(')==5 and "if css_age==56 then"in driver and 'local cursor=p:read_u16(slots[n].roster)'in driver and
         "for i,key in ipairs(join_css[n].path or{})do"in driver and 'p:read_u16(slots[n].roster)<=18'in driver and
         "io.open('mk2ks_native_tomb_rejoin_driver.lua','rb')"in driver,
         'Exactly four later-planner substitutions, ordinary cursor reads and original roster guard')


source=original.source
source=once(source,"PREFIX='audit_native_pit_transition_rejoin_literal_checked'","PREFIX='audit_native_pit_transition_rejoin_settled'")
source=once(source,"leaf = f'audit_native_pit_transition_rejoin_literal_checked_{fighter}_p{side}'",
                   "leaf = f'audit_native_pit_transition_rejoin_settled_{fighter}_p{side}'")
old="LUA=(ROOT/'mk2ks_native_pit_rejoin_provenance.lua',)+tuple(ROOT/('mk2ks_native_pit_rejoin_expanded_'+name+'.lua')for name in('display','timing_display','scanout_display'))"
new="LUA=tuple(ROOT/('mk2ks_native_pit_rejoin_settled_'+name+'.lua')for name in('driver','provenance','display','timing_display','scanout_display'))"
source=once(source,old,new)
source=once(source,'    exact_expanded_source()','    settled_source_proof()')
source=once(source,"    for p in(*LUA,Path(__file__).resolve(),expanded_source_path,literal_failure,",
    "    for p in(*LUA,Path(__file__).resolve(),literal_source_path,race_receipt,race_output/'report.json',"
    "*(p for p in race_folder.rglob('*')if p.is_file()),expanded_source_path,literal_failure,")
scope=dict(__name__=__name__,__file__=__file__,original_source_path=original.original_source_path,
           failure_path=original.failure_path,source_bound_path=original.source_bound_path,
           failed_native_folder=original.failed_native_folder,failed_native_output=original.failed_native_output,
           expanded_source_path=original.expanded_source_path,literal_failure=original.literal_failure,
           strip_lua_strings=original.strip_lua_strings,settled_source_proof=settled_source_proof,
           literal_source_path=Path(original.__file__),race_receipt=RACE_RECEIPT,race_output=RACE_OUTPUT,race_folder=RACE_FOLDER)
exec(compile(source,__file__+'::whole_original_Pit_trial_only_later_initialized_cursor_input_plan','exec'),scope)
globals().update({k:v for k,v in scope.items()if not k.startswith('__')})
