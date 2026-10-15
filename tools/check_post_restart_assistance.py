"""Prove tower assistance stops before the actual post-ending attract."""
import argparse
import json
import re
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]

def verify(log,fighter,source_side=1,all_regen=False):
    errors=[]
    if source_side not in (1,2):raise ValueError('Invalid source side')
    attract=re.findall(r'MK2_RESTART_ATTRACT frame=(\d+)',log)
    if len(attract)!=1:return {'passed':False,'errors':['Missing actual post-ending attract']}
    ending=int(attract[0])
    if source_side==2:
        # Unlike P1 regeneration (only a final counter), the P2 helper logs
        # EVERY write on BOTH sides. Compare exact accounting and chronology
        # in this run, not unrelated health totals from a different input path.
        pattern=r'MK2_P2_TOWER_RESULT[^\r\n]* health_writes=(\d+) regen_writes=(\d+) assistance=health_only'
        actual=re.findall(pattern,log)
        if len(actual)!=1 or int(actual[0][0])!=32 or int(actual[0][1])<=0:
            errors.append('Missing or incomplete P2 tower health-assistance counters')
        writes=re.findall(r'MK2_P2_TOWER_HEALTH frame=(\d+) side=(\d+) stage=(\d+) old=(\d+) new=(\d+)',log)
        if len(actual)!=1 or tuple(str(sum(w[1]==str(side) for w in writes)) for side in (1,2))!=actual[0]:
            errors.append('P2 health-write event accounting differs')
        if any(int(w[0])>=ending for w in writes):errors.append('P2 health assistance continued after ending')
        for frame,side,stage,old,new in writes:
            if int(stage) not in range(17) or not ((side=='1' and old=='161' and new=='1') or
                (side=='2' and 0<int(old)<161 and new=='161')):
                errors.append('Invalid or undeclared P2 health mutation')
        return {'passed':not errors,'errors':errors,'fighter':fighter,'restart_health_assistance_excluded':not errors,
                'proof_scope':'all_actual_p2_helper_write_events_and_exact_counters_before_attract',
                'last_assistance_frame':max((int(w[0]) for w in writes),default=None),
                'actual_attract_frame':ending,'native_tower_health_writes':len(writes)}
    if all_regen:
        counters=re.findall(r'MK2KS_CPU_DIAGNOSTIC_P1_REGEN_RESULT enabled=true writes=(\d+)',log)
        regen=re.findall(r'MK2KS_DIAGNOSTIC_P1_REGEN frame=(\d+) old=(\d+)',log)
        writes=re.findall(r'MK2KS_DIAGNOSTIC_HEALTH_WRITE frame=(\d+) stage=(\d+) cpu=(\d+) old=161 new=(\d+)',log)
        health=re.findall(r'MK2KS_CPU_DIAGNOSTIC_HEALTH_RESULT[^\r\n]* writes=(\d+)',log)
        if len(counters)!=1 or len(regen)!=int(counters[0]) or not regen:
            errors.append('Every actual P1 regeneration event must match its declared counter')
        if any(int(frame)>=ending or not 0<int(old)<161 for frame,old in regen):
            errors.append('P1 health regeneration continued after ending or has invalid values')
        if len(health)!=1 or health[0]!='32' or len(writes)!=32:
            errors.append('Exact original 32 native CPU health-assistance events required')
        if any(int(frame)>=ending or not 0<=int(stage)<=16 or new!='1' for frame,stage,cpu,new in writes):
            errors.append('CPU health assistance continued after ending or has invalid values')
        if len({int(frame) for frame,old in regen})!=len(regen):errors.append('Duplicate regeneration frame')
        return {'passed':not errors,'errors':errors,'fighter':fighter,'restart_health_assistance_excluded':not errors,
                'proof_scope':'all_actual_p1_regeneration_and_cpu_health_write_events_before_attract',
                'actual_attract_frame':ending,'native_tower_health_writes':len(writes),'actual_regeneration_writes':len(regen)}
    baseline=(ROOT/f'audit_v276_full_p1_photos_{fighter}/run.log').read_text(encoding='utf-8-sig')
    for tag in ('CPU_DIAGNOSTIC_HEALTH_RESULT','CPU_DIAGNOSTIC_P1_REGEN_RESULT'):
        pattern=r'MK2KS_'+tag+r'[^\r\n]* writes=(\d+)'
        prior,actual=re.findall(pattern,baseline),re.findall(pattern,log)
        if len(prior)!=1 or len(actual)!=1 or prior!=actual:
            errors.append('Health-assistance counter differs from completed original tower: '+tag)
    writes=[int(v) for v in re.findall(r'MK2KS_DIAGNOSTIC_HEALTH_WRITE frame=(\d+)',log)]
    if len(writes)!=32 or any(v>=ending for v in writes):errors.append('CPU health assistance continued after ending')
    return {'passed':not errors,'errors':errors,'fighter':fighter,'restart_health_assistance_excluded':not errors,
            'baseline_scope':'same_full_p1_tower_before_restart','native_tower_health_writes':len(writes)}

def main():
    parser=argparse.ArgumentParser();parser.add_argument('log',type=Path)
    parser.add_argument('--fighter',choices=('kano','sonya'),required=True)
    parser.add_argument('--source-side',type=int,choices=(1,2),default=1)
    parser.add_argument('--all-regen',action='store_true')
    args=parser.parse_args();result=verify(args.log.read_text(encoding='utf-8-sig'),args.fighter,args.source_side,args.all_regen)
    print(json.dumps(result,indent=2));raise SystemExit(0 if result['passed'] else 1)

if __name__=='__main__':main()
