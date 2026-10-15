"""Six owned ground-pound windows; guard-state correlation is finite, not universal."""
import copy,json,re
import verify_native_source_sync as sync

def gate(rows):
    native=[r for t,r in rows if t=='JAX_GROUND_NATIVE']
    plans=[r for t,r in rows if t=='SONYA_JAX_POUND_JUMP_PLAN']
    entries=[r for r in native if r['kind']=='ground_entry'];assert len(entries)==6
    result=[]
    for entry in entries:
        start=int(entry['frame'])
        p=next(r for r in plans if int(r['frame'])==start+1)
        stop=next(r for r in native if r['kind']=='ground_result' and int(r['frame'])==start+16)
        assert entry['h_actor']==stop['h_actor'] and entry['c_actor']==stop['c_actor'] and stop['h_owner']==stop['h_actor'] and stop['c_owner']==stop['c_actor']
        assert entry['h_id']==stop['h_id']=='18' and entry['c_id']==stop['c_id']=='11'
        expected='0' if p['action']=='1793' else '1'
        assert p['action'] in ('771','1792','1793') and stop['carry']==expected
        if expected=='0':
            assert stop['h_vy']=='00000000' and stop['h_y']==stop['h_floor']
            path=next(r for r in native if r['kind']=='ground_damage' and r['frame']==stop['frame'])
            assert path['a8']==path['c_actor'] and path['a13']==path['c_main']
            damage=next(r for t,r in rows if t=='HEALTH' and r['slot']=='2' and r['frame']==stop['frame'])
            assert int(damage['before'])-int(damage['after'])==21 and damage['a8']==stop['h_actor'] and damage['a13']==stop['c_main']
        else:
            assert stop['h_vy']!='00000000' or stop['h_y']!=stop['h_floor']
        windows=[r for r in plans if start<int(r['frame'])<=start+16]
        jumps=[r for r in native if r['kind']=='human_jump' and start<int(r['frame'])<start+60 and r['h_actor']==entry['h_actor']]
        result.append(dict(entry=entry,guardAtFirstPhysicalJumpAttempt=p['action'],physicalPlansUntilGroundGate=windows,
                           actualGroundResult=stop,firstActualJumpAfterEntry=jumps[0] if jumps else None))
    assert sum(r['guardAtFirstPhysicalJumpAttempt']=='1793' for r in result)==2
    return result

def main():
    sync.verify();root=sync.ROOT;out=root/'audit_current_jax_guard_jump_windows_checked';assert not out.exists()
    log=root/'audit_current_sonya_p2_jax_deferred_ground_taps_runtime/run.log'
    checked=root/'audit_current_sonya_p2_jax_deferred_ground_taps_checked/report.json'
    assert json.loads(checked.read_text())['logSHA256']==sync.sha(log)
    rows=[(s.split()[0].removeprefix('MK2_NAT_CAMPAIGN_'),dict(re.findall(r'(\w+)=([^\s]+)',s))) for s in log.read_text().splitlines() if s.startswith('MK2_NAT_CAMPAIGN_')]
    proof=gate(rows);faults=[]
    for kind in ('lost_carry_skip','wrong_guard_state','unowned_ground_damage','wrong_actual_damage'):
        bad=copy.deepcopy(rows)
        if kind=='lost_carry_skip':next(r for t,r in bad if t=='JAX_GROUND_NATIVE' and r['kind']=='ground_result' and r['carry']=='1')['carry']='0'
        elif kind=='wrong_guard_state':next(r for t,r in bad if t=='SONYA_JAX_POUND_JUMP_PLAN' and r['frame']=='109097')['action']='1792'
        elif kind=='unowned_ground_damage':next(r for t,r in bad if t=='JAX_GROUND_NATIVE' and r['kind']=='ground_damage')['a13']='00000000'
        else:next(r for t,r in bad if t=='HEALTH' and r['slot']=='2' and r['frame']=='109112')['after']='25'
        try:gate(bad)
        except AssertionError:faults.append(kind)
        else:raise AssertionError('Fault admitted '+kind)
    report=dict(passed=True,episodes=proof,effectiveFaultsRejected=faults,
                nativeFirstGroundCarryResults=dict(idle771='2 skips / 2 observed',standingGuard1792='2 skips / 2 observed',crouchedGuard1793='2 grounded damage paths / 2 observed'),
                targetedNextPhysicalChange='Stage8-only non-leg guard/default uses standing Block rather than Down+Block; preserve leg Down7/LPBlock chord, ground-pound jump priority and all other stages.',
                causalityLimit='Both missed jumps begin actual crouched guard1793 then rise769 before action0; no leg commitment at their first jump plans. Finite correlation plus native gate/damage ownership, not universal proof crouch causes all missed jumps or a port defect. Need physical successor replay.',
                inputHashes={str(p):sync.sha(p) for p in (log,checked)},newEmulatorRuns=0,fullPortAcceptance=False)
    out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(dict(passed=True,episodes=6,faults=len(faults))))

if __name__=='__main__':main()
