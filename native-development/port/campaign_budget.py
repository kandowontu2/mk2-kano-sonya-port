"""Read-only declared campaign budgets; extra attempts never imply a clear."""

def budget(arguments):
    values=[arg.split('=',1)[1] for arg in arguments if arg.startswith('--campaign-continues=')]
    assert len(values)<=1
    continues=int(values[0]) if values else 0
    fields=120000 if '--campaign-extended' in arguments else (90000 if '--campaign-full' in arguments else (45000 if '--campaign-long' in arguments else 30000))
    if '--campaign-ending-window' in arguments:fields=150000
    if '--campaign-finale-window' in arguments:fields=180000
    if '--campaign-boss-endurance' in arguments:
        assert all(flag in arguments for flag in ('--game','--campaign','--campaign-full','--campaign-extra-continues','--campaign-ending-window','--campaign-finale-window','--campaign-background-margin'))
        maximum=64;fields=300000
    else:
        maximum=32 if '--campaign-extra-continues' in arguments else (20 if '--campaign-full' in arguments else 5)
    assert 0<=continues<=maximum
    return dict(continueLimit=continues,fieldLimit=fields,endurance='--campaign-boss-endurance' in arguments)
