"""Four cold two-human leg cases: standing vs preheld crouch, both slots."""
import verify_native_source_sync as sync
sync.verify()
base=sync.ROOT/'audit_bounded_current_special_cycles_preparation'
out=sync.ROOT/'audit_current_leg_stance_comparison_preparation'
assert not out.exists();out.mkdir()
for stance in ('standing','crouched'):
    source=(base/'cycles.lua').read_text()
    if stance=='crouched':
        old="    pulse(side,'Down',age,0,7);pulse(side,'Low Punch',age,3,4);pulse(side,'Block',age,3,4)"
        new="""    pulse(side,'Down',age,0,37);pulse(side,'Low Punch',age,33,4);pulse(side,'Block',age,33,4)
    if age==30 then
     assert(own.id==18 and own.owner==own.actor and own.action==770 and own.y==own.floor)
     log('PREHELD_CROUCH',string.format('actor=%08X main=%08X id=%d action=%d flags=%04X',own.actor,own.main,own.id,own.action,own.flags))
    end"""
        assert source.count(old)==1;source=source.replace(old,new)
    assert ':write_' not in source and ':snapshot(' not in source
    lua=out/(stance+'.lua');lua.write_text(source)
    for side in (1,2):
        runner=(base/f'run_leg_p{side}.ps1').read_text()
        runner=runner.replace(base.name+'/cycles.lua',out.name+'/'+stance+'.lua').replace(sync.sha(base/'cycles.lua'),sync.sha(lua))
        runner=runner.replace(f'audit_bounded_current_special_cycles_leg_p{side}',f'audit_current_leg_stance_{stance}_p{side}')
        runner=runner.replace("$env:MK2KS_HUMAN_SPECIAL_VICTIM='sub_zero'","$env:MK2KS_HUMAN_SPECIAL_VICTIM='baraka'")
        runner=runner.replace("$env:MK2KS_HUMAN_SPECIAL_VICTIM='kitana'","$env:MK2KS_HUMAN_SPECIAL_VICTIM='baraka'")
        if '$env:MK2KS_HUMAN_SPECIAL_VICTIM=' not in runner:runner=runner.replace("$env:MK2KS_HUMAN_SPECIAL_MOVE='leg'","$env:MK2KS_HUMAN_SPECIAL_MOVE='leg'\n$env:MK2KS_HUMAN_SPECIAL_VICTIM='baraka'")
        (out/f'run_{stance}_p{side}.ps1').write_text(runner)
print('4cases/2cycles each; nativehumanBaraka victim; no media/guestwrites')
