"""Bounded source-timing/round-boundary faults; preserve first streamed proof."""
import inspect,json,traceback
from pathlib import Path
import qualify_saved_square_owner_eof_streamed as prior

OUT=prior.ROOT/'audit_saved_square_owner_eof_streamed_faults_checked'
parent=prior.OUT/'report.json'
proof=json.loads(parent.read_text())
assert proof['passed']
scope=dict(vars(prior),OUT=OUT,__file__=__file__)
source=inspect.getsource(prior.main)
old="if tag in data:data[tag].append(dict(prior.RX.findall(line)))"
new="""if tag in data:
                data[tag].append(dict(prior.RX.findall(line)))
                prior.need(len(data[tag])<=20000,'Bounded actual record inventory')
                if len(data[tag])%256==0:peak()"""
assert source.count(old)==1; source=source.replace(old,new,1)
marker="    prior.need(gate(data,lengths)==positive,'Whole unmodified owner positive restored')"
extra="""    for label,change in (
        ('missing_owner_snapshot',lambda d:d['MK2_VOICE_OWNER'].pop()),
        ('duplicate_owner_snapshot',lambda d:d['MK2_VOICE_OWNER'].append(copy.deepcopy(d['MK2_VOICE_OWNER'][-1]))),
        ('terminal_dangling_id',lambda d:d['MK2_VOICE_OWNER'][-1].update(id='18')),
        ('wrong_native_launch_clock',lambda d:next(r for r in d['MK2_MAUDIO_SOUND'] if r['word']=='6B00').update(seconds='47.100000000000')),
        ('wrong_instruction_boundary_opcode',lambda d:next(r for r in d['MK2_SONYA_CHOICE_EVENT'] if r['kind']=='square').update(opcode='C081')),
        ('wrong_next_physical_mode',lambda d:next(r for r in d['MK2_CPU_ROUND_FIELD'] if r['frame']=='2572' and r['slot']=='2').update(mode='7')),
        ('unrelated_mode_waiver',lambda d:next(r for r in d['MK2_CPU_ROUND_FIELD'] if r['frame']=='2600' and r['slot']=='2').update(mode='7')),
        ('owner_retained_after_source_eof',lambda d:next(r for r in d['MK2_VOICE_OWNER'] if r['slot']=='2' and r['serial']==positive['sourceDerivedRetirements'][0]['firstActualZeroSnapshot']['serial']).update(actor='010350A0',main='0106BF30',health='161',id='18',mode='2')),
    ):
        bad=copy.deepcopy(data);change(bad)
        try:gate(bad,lengths)
        except AssertionError as error:faults.append(dict(field=label,rejected=str(error)))
        else:raise AssertionError('Timing/boundary fault admitted: '+label)
        del bad;peak()
    try:gate(data,{0x6b00:50312})
    except AssertionError as error:faults.append(dict(field='wrong_actual_clip_length',rejected=str(error)))
    else:raise AssertionError('Wrong source duration admitted')
"""
assert source.count(marker)==1;source=source.replace(marker,extra+marker,1)
old="for p in (Path(__file__),Path(prior.__file__),CAPTURE,clip,BASE/'run.log.gz'):"
new="for p in (Path(__file__),first_stream_source,parent_proof,Path(prior.__file__),CAPTURE,clip,BASE/'run.log.gz'):"
assert source.count(old)==1;source=source.replace(old,new,1)
scope.update(first_stream_source=Path(prior.__file__),parent_proof=parent)
exec(compile(source,__file__+'::whole_streamed_positive_effective_timing_faults','exec'),scope)

if __name__=='__main__':
    try:scope['main']()
    except BaseException:
        OUT.mkdir(exist_ok=True);(OUT/'failure.json').write_text(json.dumps(dict(passed=False,error=traceback.format_exc()),indent=2)+'\n');raise
