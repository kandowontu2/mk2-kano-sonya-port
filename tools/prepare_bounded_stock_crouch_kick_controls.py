"""Select stock control fighters using normal CSS inputs, not guest writes."""
import json
import verify_native_source_sync as sync

def main():
    root = sync.ROOT
    sync.verify()
    old = root/'audit_bounded_crouch_kick_pain_preparation'
    out = root/'audit_bounded_stock_crouch_kick_preparation'
    assert not out.exists()
    out.mkdir()
    source = (old/'prepared_observer.lua').read_text()
    needle = 'local spec=assert(specs[move]);assert(side==1 or side==2)'
    assert source.count(needle) == 1
    for fighter, ident in (('baraka', 3), ('mileena', 5)):
        lua = source.replace(needle, needle+f'\nspec={{ {ident}, spec[2] }} -- normal player-select target only')
        target = out/f'{fighter}_observer.lua'
        target.write_text(lua)
        runner = (old/'run_sonya.ps1').read_text()
        runner = runner.replace(old.name+'/prepared_observer.lua', out.name+'/'+target.name)
        runner = runner.replace(sync.sha(old/'prepared_observer.lua'), sync.sha(target))
        runner = runner.replace('audit_bounded_sonya_crouch_kick_pain_runtime',
                                f'audit_bounded_{fighter}_crouch_kick_control_runtime')
        (out/f'run_{fighter}.ps1').write_text(runner)
    (out/'report.json').write_text(json.dumps(dict(prepared=True, acceptance=False,
                                                policy='physical CSS and crouch LowKick')))

if __name__ == '__main__':
    main()
