"""Read-only diagnosis of the actual failed semantic fault suite; no replay."""
import gzip
import inspect
import json
import re
import qualify_native_sonya_first_six_global_reset as checked


def model():
    source=inspect.getsource(checked.run)
    source=source[:source.index('    source=inspect.getsource(paid.run)')]+"    return scope\n"
    source=source.replace('proof=kernel()',"proof=json.loads((INIT/'native_reset_kernel_report.json').read_text())['proof']")
    scope=dict(vars(checked),__file__=__file__)
    exec(compile(source,__file__+'::whole_source_checked_native_health_factory','exec'),scope)
    health=scope['run']()
    source=inspect.getsource(checked.paid.run)
    source=source[:source.index('    source=inspect.getsource(prior.run)')]+"    return scope\n"
    source=source.replace('scope=dict(vars(prior),__file__=__file__,OUT=OUT)',
        'scope=dict(vars(prior),__file__=__file__,OUT=OUT,health_history=health_history)')
    exec(compile(source,__file__+'::whole_actual_paid_control_and_six_fight_contract_factory','exec'),health)
    return health['run']()


def run():
    scope=model();prior=checked.paid.prior
    text=gzip.open(prior.FOLDER/'run.log.gz','rt',encoding='utf-8').read()
    rows={tag:[dict(re.findall(r'(\w+)=([^\s]+)',line)) for line in text.splitlines() if line.startswith('MK2_NAT_CAMPAIGN_'+tag+' ')] for tag in prior.COUNTS}
    scope['fields'](rows)
    source=inspect.getsource(prior.run)
    first=source.index('    trials=[]');last=source.index('    for tag,index in ',first)
    trials=source[first:last]
    addition="\n    first_loss=int(rows['LOSS'][0]['frame'])\n    for button,age in (('Coin',20),('Coin',270),('Start',310)):\n        index=next(i for i,q in enumerate(rows['INPUT']) if q['button']==button and int(q['frame'])==first_loss+age)\n        trials.append(('INPUT',index,'button','High_Punch'))"
    trials=trials.replace("raise ValueError('False native ladder evidence admitted')", "print(json.dumps(dict(admittedTrial=(tag,index,key,value),actualOriginalRow=rows[tag][index],gameplayAcceptance=False)),flush=True)")
    scope.update(rows=rows,faults=[],json=json)
    exec(compile('def inspect_faults():\n'+trials+addition+'\n    return faults\n',__file__+'::actual_fault_diagnosis_only','exec'),scope)
    result=scope['inspect_faults']()
    print(json.dumps(dict(diagnosticOnly=True,originalFaultsRejected=len(result),gameplayAccepted=False)),flush=True)


if __name__=='__main__':run()
