from qualify_bounded_current_friendships import fields
import verify_native_source_sync as sync
for kind in ('friendship','babality'):
    prefix='MK2_FRIEND_' if kind=='friendship' else 'MK2_NATIVE_BABY_'
    for fighter in ('kano','sonya'):
        for side in (1,2):
            case=sync.ROOT/f'audit_bounded_rejoin_both_selectors_{kind}_{fighter}_p{side}_runtime/run.log'
            old=sync.ROOT/f'audit_bounded_current_{kind}_{fighter}_p{side}_runtime/run.log'
            original=old.read_text()
            cutoff=int(fields(next(line for line in original.splitlines() if line.startswith(prefix+'RESULT')))['frame'])
            def core(text): return [line for line in text.splitlines() if line.startswith(prefix) and not line.startswith(prefix+'RESULT') and not line.startswith(prefix+'REJOIN') and int(fields(line)['frame'])<cutoff]
            actual,expected=core(case.read_text()),core(original)
            if actual!=expected:
                print(kind,fighter,side,'lengths',len(actual),len(expected))
                for a,b in zip(actual,expected):
                    if a!=b: print('ACTUAL',a,'BASELINE',b,sep='\n');break
