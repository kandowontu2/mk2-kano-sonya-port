"""Full earned1731 contract for true mirrors; original native RNG drop physics.

Only the opponent's expected identity changes to the selected performer's ID.
Every earned health, paid selection, parser, input, range, action, 801field and
retirement gate is retained. An unpressed drop still requires original guest
code, actual RNG registers, owned task and exact original phase chronology.
"""
import hashlib,inspect
import native_tomb_drop_qualification_v3643 as native
ROOT,need=native.ROOT,native.need

drop_source=inspect.getsource(native.qualify_drop)
old="victim_id=18 if fighter=='kano'else 17"
need(drop_source.count(old)==1,'Exact original drop victim expectation')
drop_source=drop_source.replace(old,"victim_id=17 if fighter=='kano'else 18")
scope=dict(native.__dict__)
exec(compile(drop_source,'<entire3643_original_drop_true_mirror>','exec'),scope)
contract_source=native.source
old='victim = 18 if own == 17 else 17'
need(contract_source.count(old)==1,'Exact original full1731 victim expectation')
contract_source=contract_source.replace(old,'victim = own')
scope.update(native.legacy.__dict__)
exec(compile(contract_source,'<entire1731_full_contract_true_mirror_native_drop>','exec'),scope)
check_log=scope['check_log']
CONTRACT_SHA256=hashlib.sha256(contract_source.encode()).hexdigest().upper()
DROP_SHA256=hashlib.sha256(drop_source.encode()).hexdigest().upper()

def actual_faults(text,fighter,side,guest):
    """Alter actual observed records, never invent successful native events."""
    cases={}
    lines=text.splitlines()
    for tag,key,value in (
        ('BOOT','victim_id','1'),('SELECT_ID','actual','1'),
        ('MATCH','ids','1,1'),('DAMAGE','pc','FF836701'),
        ('DAMAGE','before','160'),('WINDOW','damage','321'),
        ('COMMAND','gap','130'),('FIELD','victim_id','1'),
        ('RESULT','action','-1'),('RESULT','frame','1')):
        import re
        index=next(i for i,s in enumerate(lines)if s.startswith('MK2_STAGE_'+tag+' ')and re.search(r'\b'+key+'=',s))
        altered=list(lines)
        altered[index]=re.sub(r'\b'+key+r'=[^\s]+',key+'='+value,altered[index],count=1)
        try:check_log('\n'.join(altered)+'\n',fighter,side,1,guest=guest)
        except Exception as error:cases[tag+':'+key]=str(error)
        else:raise AssertionError('Actual fault not rejected: '+tag+':'+key)
    for entry in ('FFFAA200'if fighter=='kano'else'FFFAA400','FF8BDFE0'):
        index=next(i for i,s in enumerate(lines)if s.startswith('MK2_STAGE_ENTRY ')and 'entry='+entry in s)
        altered=lines[:index]+lines[index+1:]
        try:check_log('\n'.join(altered)+'\n',fighter,side,1,guest=guest)
        except Exception as error:cases['missing:'+entry]=str(error)
        else:raise AssertionError('Missing actual entry not rejected: '+entry)
    need(len(cases)==12,'All actual mirror health/identity/action/cleanup faults rejected')
    return cases
